#!/usr/bin/env python3
"""One bounded Runpod exact-Apéry pilot. Cloud actions occur only when invoked.

The server auto-termination and detached local cleanup watchdog are independent.
Only the pod with this invocation's unique name/id may be deleted. API responses,
environment variables, credentials and SSH private keys are never logged.
"""

import argparse
import datetime as dt
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import shlex
import signal
import subprocess
import sys
import tarfile
import time


IMAGE = "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04"
DEFAULT_GPU = "NVIDIA GeForce RTX 3090"
CAP = 1.0
FILES = ("apery.hpp", "gpu.hpp", "scan_cuda.cu", "driver.cpp", "verify_scan.py")
LEASE_FIELDS = {"id", "name", "created", "deadline", "gpu", "price", "watchdogPID"}
REMOTE = "/workspace/wilf-apery"


class PilotError(RuntimeError):
    """Only locally constructed, nonsecret messages belong in this exception."""


class Promoted(PilotError):
    def __init__(self, code):
        super().__init__("CPU self-test promoted a witness; search stopped")
        self.code = code


def utc(epoch=None):
    return dt.datetime.fromtimestamp(time.time() if epoch is None else epoch,
                                    dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def epoch(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def note(message):
    print(message, flush=True)


def run(argv, timeout=30, data=None):
    try:
        return subprocess.run(argv, input=data, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise PilotError("subprocess timed out; raw command output withheld") from None
    except OSError:
        raise PilotError("subprocess could not start; raw error withheld") from None


def parse_json(raw):
    text = raw.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Some CLI versions put a status line ahead of their JSON result.
        decoder = json.JSONDecoder()
        for pos, char in enumerate(text):
            if char in "[{":
                try:
                    value, _ = decoder.raw_decode(text[pos:])
                    return value
                except json.JSONDecodeError:
                    pass
    raise PilotError("CLI returned no parseable JSON; raw response withheld")


def ctl(*args, timeout=30, checked=True):
    result = run(["runpodctl", *args, "--output", "json"], timeout=timeout)
    if checked and result.returncode:
        raise PilotError("runpodctl operation failed (exit %d); response withheld" % result.returncode)
    return result


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def norm(value):
    return "".join(c.lower() for c in str(value) if c.isalnum())


def numeric(value):
    if isinstance(value, bool):
        return None
    try:
        number = float(str(value).replace("$", "").strip())
        return number if math.isfinite(number) and number >= 0 else None
    except (TypeError, ValueError):
        return None


def secure_price(record):
    prices = []

    def visit(value, path=()):
        if not isinstance(value, dict):
            return
        for key, child in value.items():
            name = norm(key)
            context = path + (name,)
            explicitly_secure = name in {"secureprice", "securepriceperhr", "securepriceperhour", "securecloudprice", "secureondemandprice",
                                         "securehourlyprice", "securecloudondemandprice"}
            nested_secure = any("secure" in part for part in path) and name in {
                "price", "ondemandprice", "uninterruptableprice", "costperhr", "costperhour"}
            if explicitly_secure or nested_secure:
                price = numeric(child)
                if price is not None:
                    prices.append(price)
            if isinstance(child, dict):
                visit(child, context)
            elif isinstance(child, list):
                for item in child:
                    visit(item, context)

    if record.get("secureCloud") is False:
        return None
    visit(record)
    return min(prices) if prices else None


def reported_costs(value):
    answer = []
    for record in objects(value):
        for key, val in record.items():
            if norm(key) in {"costperhr", "costperhour", "hourlyprice", "priceperhour", "adjustedcostperhr"}:
                price = numeric(val)
                if price is not None:
                    answer.append(price)
    return answer


def own_records(value):
    return [record for record in objects(value)
            if isinstance(record.get("id"), str)
            and ("name" in record or "desiredStatus" in record or "runtimeStatus" in record)]


def inventory(raw):
    value = parse_json(raw)
    if not isinstance(value, list) or any(not isinstance(pod, dict) or not isinstance(pod.get("id"), str) for pod in value):
        raise PilotError("unrecognized pod inventory; absence is not established")
    return value


def select_gpu(catalog, requested, existing):
    names = [requested]
    if not existing:
        names += ["NVIDIA A40", "NVIDIA RTX A6000"]
    for wanted in names:
        for record in objects(catalog):
            labels = [record.get(key, "") for key in ("gpuId", "id", "name", "displayName", "gpuTypeId")]
            if not any(norm(label) == norm(wanted) for label in labels):
                continue
            price = secure_price(record)
            if price is None or price > CAP:
                continue
            if record.get("available") is False:
                continue
            stock = norm(record.get("stockStatus", record.get("availability", "")))
            if stock in {"none", "outofstock", "unavailable", "false", "0"}:
                continue
            gpu_id = record.get("gpuId", record.get("id", record.get("gpuTypeId", wanted)))
            return str(gpu_id), price
    raise PilotError("no permitted secure GPU with a known price <= $1/hour; no pod created")


def save_lease(path, lease):
    if set(lease) != LEASE_FIELDS:
        raise PilotError("internal lease whitelist mismatch")
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(lease, indent=2) + "\n")
    temporary.chmod(0o600)
    temporary.replace(path)


def task_id(value, name):
    for record in objects(value):
        if record.get("name") == name and isinstance(record.get("id"), str):
            return record["id"]
    if isinstance(value, dict):
        candidate = value.get("id", value.get("podId"))
        if isinstance(candidate, str):
            return candidate
    return None


def discover_task(name):
    result = ctl("pod", "list", "--all", timeout=20, checked=False)
    if result.returncode:
        return None
    matches = {r["id"] for r in inventory(result.stdout) if r.get("name") == name}
    if len(matches) > 1:
        raise PilotError("multiple exact-name matches; refusing ambiguous cleanup")
    return next(iter(matches), None)


def absent(pod_id):
    result = ctl("pod", "get", pod_id, timeout=20, checked=False)
    if result.returncode:
        message = (result.stdout + result.stderr).decode("utf-8", errors="replace").lower()
        if any(token in message for token in ("not found", "does not exist", "404")):
            return True
    listing = ctl("pod", "list", "--all", timeout=20, checked=False)
    if listing.returncode:
        return False
    return not any(r.get("id") == pod_id for r in inventory(listing.stdout))


def cleanup_once(lease):
    pod_id = lease.get("id") or discover_task(lease["name"])
    if not pod_id:
        # A successful exact-name inventory is required before concluding that
        # an unobserved create did not leave a pod behind.
        listing = ctl("pod", "list", "--all", timeout=20, checked=False)
        if listing.returncode:
            return False
        return not any(r.get("name") == lease["name"] for r in inventory(listing.stdout))
    found = ctl("pod", "get", pod_id, timeout=20, checked=False)
    if not found.returncode:
        records = [r for r in objects(parse_json(found.stdout)) if r.get("id") == pod_id]
        if records and any(r.get("name") not in (None, lease["name"]) for r in records):
            raise PilotError("task pod identity mismatch; refusing deletion")
    ctl("pod", "delete", pod_id, timeout=25, checked=False)
    return absent(pod_id)


def watchdog(lease_path):
    """Detached cleanup only: it never starts or changes a research workload."""
    lease_path = Path(lease_path).resolve()
    done = lease_path.parent / "cleanup.done"
    while not done.exists():
        try:
            lease = json.loads(lease_path.read_text())
            if set(lease) != LEASE_FIELDS:
                return 2
            remaining = epoch(lease["deadline"]) - time.time()
            if remaining > 0:
                time.sleep(min(5, remaining))
                continue
            if cleanup_once(lease):
                done.write_text("pod absence confirmed by watchdog at " + utc() + "\n")
                note("Task pod absence confirmed.")
                return 0
            note("Task pod cleanup not yet confirmed; retrying.")
        except Exception:
            note("Cleanup observation failed; details withheld; retrying.")
        time.sleep(5)
    return 0


def time_left(deadline, reserve=60, maximum=None):
    seconds = deadline - time.time() - reserve
    if seconds < 1:
        raise PilotError("pilot deadline reached; preserving cleanup reserve")
    return max(1, int(min(seconds, maximum if maximum is not None else seconds)))


def ssh_command(info, pod, key, known_hosts):
    # Prefer a direct public mapping if the API provides one.
    for record in objects(pod):
        ip = record.get("publicIp", record.get("publicIP"))
        ports = record.get("portMappings")
        if isinstance(ip, str) and isinstance(ports, dict):
            port = ports.get("22", ports.get("22/tcp"))
            if isinstance(port, dict):
                port = port.get("publicPort", port.get("port"))
            if str(port).isdigit() and 1 <= int(port) <= 65535:
                base = ["ssh", "-p", str(port), "root@" + ip]
                break
    else:
        strings = []

        def collect(value):
            if isinstance(value, str):
                strings.extend(line.strip() for line in value.splitlines() if line.strip().startswith("ssh "))
            elif isinstance(value, dict):
                for child in value.values():
                    collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)

        collect(info)
        if not strings:
            raise PilotError("SSH command not yet available")
        tokens = shlex.split(strings[0])
        base = ["ssh"]
        i = 1
        while i < len(tokens):
            token = tokens[i]
            if token == "-i":
                i += 2
                continue
            if token.startswith("-i") and len(token) > 2:
                i += 1
                continue
            if token == "-o" and i + 1 < len(tokens):
                option = tokens[i + 1]
                if norm(option.split("=", 1)[0]) in {"identityfile", "identitiesonly", "batchmode", "stricthostkeychecking", "connecttimeout", "userknownhostsfile"}:
                    i += 2
                    continue
            if token.startswith("-o") and norm(token[2:].split("=", 1)[0]) in {"identityfile", "identitiesonly", "batchmode", "stricthostkeychecking", "connecttimeout", "userknownhostsfile"}:
                i += 1
                continue
            if token not in ("-t", "-tt"):
                base.append(token)
            i += 1
    options = ["-T", "-i", str(key), "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes",
               "-o", "StrictHostKeyChecking=accept-new", "-o", "ConnectTimeout=5",
               "-o", "UserKnownHostsFile=" + str(known_hosts)]
    return ["ssh", *options, *base[1:]]


def upload(ssh, source, deadline):
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode="w") as tar:
        for name in FILES:
            tar.add(source / name, arcname=name, recursive=False)
    command = "mkdir -p %s/results && tar -xf - -C %s" % (REMOTE, REMOTE)
    result = run([*ssh, command], timeout=time_left(deadline, maximum=45), data=archive.getvalue())
    if result.returncode:
        raise PilotError("source upload failed; SSH details withheld")


def remote_job(ssh, deadline, label, argv=None, shell=None, extension="jsonl"):
    seconds = time_left(deadline)
    command = shlex.join(argv) if argv is not None else shell
    if command is None:
        raise PilotError("empty remote job")
    # sshd does not inherit the CUDA PATH from this image's container entrypoint.
    # Set it for every stage, including nvcc and compute-sanitizer discovery.
    command = ("export PATH=/usr/local/cuda/bin:/usr/local/nvidia/bin:"
               "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH; "
               + command)
    # A remote timeout survives a broken controller/SSH connection.
    script = ("cd %s && timeout --signal=TERM --kill-after=5s %ss bash -c %s "
              "> results/%s.%s 2> results/%s.stderr" %
              (REMOTE, seconds, shlex.quote(command), label, extension, label))
    note("Running " + label + ".")
    result = run([*ssh, script], timeout=seconds + 8)
    if result.returncode in (3, 4) and (label.startswith(("bench_", "mutate_"))
                                       or label in {"cpu_selftest", "gpu_selftest", "memcheck"}):
        return result.returncode
    if result.returncode:
        raise PilotError("remote stage %s failed (exit %d); logs retained remotely" % (label, result.returncode))
    return 0


def effective_threads(ssh, deadline):
    program = '''import json, math, os, pathlib, subprocess
count = os.cpu_count() or 1
try: affinity = len(os.sched_getaffinity(0))
except (AttributeError, OSError):
    try: affinity = int(subprocess.check_output(["nproc"], text=True).strip())
    except Exception: affinity = count
quota = None
try:
    value, period = pathlib.Path("/sys/fs/cgroup/cpu.max").read_text().split()
    if value != "max": quota = int(value) / int(period)
except (OSError, ValueError, ZeroDivisionError): pass
if quota is None:
    for base in ("/sys/fs/cgroup/cpu", "/sys/fs/cgroup"):
        try:
            q = int(pathlib.Path(base, "cpu.cfs_quota_us").read_text())
            p = int(pathlib.Path(base, "cpu.cfs_period_us").read_text())
            if q > 0 and p > 0: quota = q / p; break
        except (OSError, ValueError): pass
effective = min(count, affinity, quota if quota is not None else max(count, affinity))
threads = max(1, min(8, math.floor(effective)))
print(json.dumps({"os_cpu_count": count, "affinity_cpus": affinity, "quota_cpus": quota,
                  "effective_cpus": effective, "benchmark_threads": threads}))
'''
    remote_job(ssh, deadline, "cpu_resources", argv=["python3", "-c", program])
    result = run([*ssh, "cat %s/results/cpu_resources.jsonl" % REMOTE],
                 timeout=time_left(deadline, maximum=15))
    if result.returncode:
        raise PilotError("CPU quota observation failed")
    resources = parse_json(result.stdout)
    threads = resources.get("benchmark_threads")
    if not isinstance(threads, int) or not 1 <= threads <= 8:
        raise PilotError("invalid CPU quota observation")
    note(json.dumps({key: resources.get(key) for key in
                     ("os_cpu_count", "affinity_cpus", "quota_cpus", "effective_cpus", "benchmark_threads")}, sort_keys=True))
    return threads


def download(ssh, output):
    result = run([*ssh, "cd %s && tar -cf - results" % REMOTE], timeout=35)
    if result.returncode:
        raise PilotError("result download failed; SSH details withheld")
    if len(result.stdout) > 256 * 1024 * 1024:
        raise PilotError("result archive exceeds safety bound")
    total = 0
    with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r:") as tar:
        for member in tar:
            path = PurePosixPath(member.name)
            if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != "results":
                raise PilotError("unsafe result archive path rejected")
            if member.isdir():
                continue
            if not member.isfile():
                raise PilotError("nonregular result archive entry rejected")
            total += member.size
            if total > 256 * 1024 * 1024:
                raise PilotError("expanded results exceed safety bound")
            destination = output.joinpath(*path.parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.is_symlink() or any(p.is_symlink() for p in destination.parents if p != output.parent):
                raise PilotError("symlink in result destination rejected")
            extracted = tar.extractfile(member)
            if extracted is None:
                raise PilotError("result archive member could not be read")
            with extracted, destination.open("wb") as target:
                while True:
                    chunk = extracted.read(1024 * 1024)
                    if not chunk:
                        break
                    target.write(chunk)


def pilot(args):
    if not 1 <= args.minutes <= 20:
        raise PilotError("--minutes must lie in [1,20]")
    source = Path(__file__).resolve().parent
    for filename in FILES:
        if not (source / filename).is_file():
            raise PilotError("required local source missing: " + filename)
    output = Path(args.output).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=False)
    output.chmod(0o700)
    key = Path(args.key).expanduser().resolve()
    key.parent.mkdir(parents=True, exist_ok=True)
    if not key.exists():
        result = run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C", "wilf-apery-pilot", "-f", str(key)])
        if result.returncode:
            raise PilotError("task SSH key generation failed")
    public = Path(str(key) + ".pub")
    if not public.exists():
        derived = run(["ssh-keygen", "-y", "-f", str(key)])
        if derived.returncode:
            raise PilotError("task public key derivation failed")
        public.write_bytes(derived.stdout)
    registration = ctl("ssh", "add-key", "--key-file", str(public), checked=False)
    if registration.returncode:
        message = (registration.stdout + registration.stderr).decode("utf-8", errors="replace").lower()
        if not any(token in message for token in ("already exists", "already registered", "duplicate")):
            raise PilotError("task public key registration failed; response withheld")
    existing = inventory(ctl("pod", "list", "--all").stdout)
    catalog = parse_json(ctl("gpu", "list").stdout)
    gpu, price = select_gpu(catalog, args.gpu_id, existing)
    created = time.time()
    deadline = created + args.minutes * 60
    name = "wilf-apery-pilot-" + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + str(os.getpid())
    lease = {"id": None, "name": name, "created": utc(created), "deadline": utc(deadline),
             "gpu": gpu, "price": price, "watchdogPID": None}
    lease_path = output / "lease.json"
    save_lease(lease_path, lease)
    with (output / "watchdog.log").open("ab", buffering=0) as log:
        watcher = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "--watchdog", str(lease_path)],
                                   stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                                   start_new_session=True, close_fds=True)
    lease["watchdogPID"] = watcher.pid
    save_lease(lease_path, lease)
    ssh = None
    outcome = {"status": "failed", "pod_id": None, "name": name, "deadline": lease["deadline"],
               "gpu": gpu, "catalog_secure_price": price, "output": str(output),
               "public_key_cleanup": "Task public key remains registered; remove only this key if desired."}
    create_attempted = False

    def interrupted(signum, frame):
        raise PilotError("controller interrupted; cleanup requested")

    old_handlers = {sig: signal.signal(sig, interrupted) for sig in (signal.SIGTERM, signal.SIGINT)}
    try:
        note("Starting one secure task pod at catalog price $%.4f/hour; deadline %s." % (price, lease["deadline"]))
        create_attempted = True
        result = ctl("pod", "create", "--name", name, "--gpu-id", gpu, "--gpu-count", "1",
                     "--cloud-type", "SECURE", "--compute-type", "GPU", "--image", IMAGE,
                     "--container-disk-in-gb", "20", "--volume-in-gb", "0", "--ports", "22/tcp",
                     "--ssh", "--terminate-after", lease["deadline"],
                     timeout=min(120, time_left(deadline)), checked=False)
        if result.returncode:
            raise PilotError("single pod create attempt failed; no rental retry")
        pod = parse_json(result.stdout)
        lease["id"] = task_id(pod, name)
        if not lease["id"]:
            lease["id"] = discover_task(name)
        if not lease["id"]:
            raise PilotError("create returned no observable task ID; watchdog retains exact-name cleanup")
        save_lease(lease_path, lease)
        outcome["pod_id"] = lease["id"]
        note(json.dumps(lease, sort_keys=True))
        for cost in reported_costs(pod):
            if cost > CAP:
                raise PilotError("reported pod cost exceeds $1/hour; deleting immediately")
        observation_end = min(time.time() + 300, deadline - 75)
        while time.time() < observation_end:
            current = ctl("pod", "get", lease["id"], timeout=time_left(deadline, maximum=20), checked=False)
            if not current.returncode:
                pod = parse_json(current.stdout)
                if any(cost > CAP for cost in reported_costs(pod)):
                    raise PilotError("reported pod cost exceeds $1/hour; deleting immediately")
            info_result = ctl("ssh", "info", lease["id"], timeout=time_left(deadline, maximum=20), checked=False)
            if not info_result.returncode:
                try:
                    try:
                        info = parse_json(info_result.stdout)
                    except PilotError:
                        info = info_result.stdout.decode("utf-8", errors="replace")
                    candidate = ssh_command(info, pod, key, output / "known_hosts")
                    probe = run([*candidate, "true"], timeout=time_left(deadline, maximum=10))
                    if not probe.returncode:
                        ssh = candidate
                        break
                except PilotError:
                    pass
            time.sleep(min(5, max(0, observation_end - time.time())))
        if ssh is None:
            raise PilotError("SSH observation timed out; no restart or replacement rental")
        upload(ssh, source, deadline)
        remote_job(ssh, deadline, "hardware", shell="uname -a; lscpu; nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader; sha256sum apery.hpp gpu.hpp scan_cuda.cu driver.cpp verify_scan.py; nvcc --version", extension="txt")
        threads = effective_threads(ssh, deadline)
        outcome["cpu_threads"] = threads
        remote_job(ssh, deadline, "cpu_compile", argv=["g++", "-std=c++17", "-O3", "-pthread", "-Wall", "-Wextra", "-Werror", "driver.cpp", "-o", "scan_cpu"], extension="log")
        cpu_promoted = remote_job(ssh, deadline, "cpu_selftest", argv=["./scan_cpu", "--self-test", "1000"])
        if cpu_promoted:
            raise Promoted(cpu_promoted)
        remote_job(ssh, deadline, "gpu_compile", argv=["nvcc", "-std=c++17", "-O3", "-DWILF_CUDA", "-arch=sm_86", "-maxrregcount=64", "-Xptxas=-v", "-Xcompiler=-pthread", "driver.cpp", "scan_cuda.cu", "-o", "scan_gpu"], extension="log")
        promoted = remote_job(ssh, deadline, "gpu_selftest", argv=["./scan_gpu", "--self-test", "100"])
        if not promoted:
            promoted = remote_job(ssh, deadline, "memcheck", shell='''if command -v compute-sanitizer >/dev/null 2>&1; then compute-sanitizer --tool memcheck --error-exitcode 9 ./scan_gpu --self-test 5; else printf '%s\n' '{"kind":"memcheck_unavailable"}'; fi''')
        if not promoted:
            for index, (m, k) in enumerate(((63, 8), (127, 8), (256, 12), (512, 12), (1024, 12))):
                promoted = remote_job(ssh, deadline, "bench_%d" % m,
                                      argv=["./scan_gpu", "--bench", "4096", str(4500 + index), str(threads), str(m), str(k)])
                if promoted:
                    break
        if not promoted:
            anchor = [239, 282, 295, 318, 333, 379, 386, 390, 400, 405, 407]
            for bucket, m in enumerate((61, 63, 67, 71)):
                promoted = remote_job(ssh, deadline, "mutate_%d" % m,
                                      argv=["./scan_gpu", "--mutate", "4096", str(4501 + bucket), str(threads), str(m), *map(str, anchor)])
                if promoted:
                    break
        # Verification remains permitted after a promoted exit; no more search.
        if promoted:
            outcome["status"] = "promoted_witness_unverified"
            outcome["promoted_exit"] = promoted
        remote_job(ssh, deadline, "verification", shell="python3 verify_scan.py results/*.jsonl --output results/verified.json", extension="log")
        outcome["status"] = "promoted_witness" if promoted else "completed"
        outcome["promoted_exit"] = promoted
    except Promoted as exc:
        outcome["status"] = "promoted_witness_unverified"
        outcome["promoted_exit"] = exc.code
        note("CPU self-test promoted a witness; further search stopped.")
        try:
            remote_job(ssh, deadline, "verification", shell="python3 verify_scan.py results/*.jsonl --output results/verified.json", extension="log")
            outcome["status"] = "promoted_witness"
        except PilotError as verification_error:
            outcome["error"] = str(verification_error)
    except PilotError as exc:
        outcome["error"] = str(exc)
        note("Pilot stopped: " + str(exc))
    except Exception as exc:
        outcome["error"] = "unexpected " + type(exc).__name__ + "; details withheld"
        note("Pilot stopped unexpectedly; details withheld.")
    finally:
        # A second SIGTERM must not interrupt deletion after cleanup begins.
        for sig in old_handlers:
            signal.signal(sig, signal.SIG_IGN)
        if ssh is not None:
            try:
                download(ssh, output)
                outcome["results_downloaded"] = True
            except Exception:
                outcome["results_downloaded"] = False
                note("Result download failed; raw SSH/API details withheld.")
        confirmed = False
        if create_attempted:
            cleanup_end = time.time() + 120
            while time.time() < cleanup_end:
                try:
                    if cleanup_once(lease):
                        confirmed = True
                        (output / "cleanup.done").write_text("pod absence confirmed at " + utc() + "\n")
                        break
                except Exception:
                    pass
                time.sleep(3)
        else:
            confirmed = True
            (output / "cleanup.done").write_text("no create attempted\n")
        outcome["pod_absence_confirmed"] = confirmed
        if not confirmed:
            outcome["status"] = "cleanup_unconfirmed"
            note("Task pod absence is NOT confirmed; detached watchdog continues exact-task deletion retries.")
        (output / "summary.json").write_text(json.dumps(outcome, indent=2) + "\n")
        note(json.dumps(outcome, sort_keys=True))
        for sig, handler in old_handlers.items():
            signal.signal(sig, handler)
    return 0 if outcome["status"] in ("completed", "promoted_witness") and confirmed else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gpu-id", default=DEFAULT_GPU)
    parser.add_argument("--minutes", type=int, default=20)
    parser.add_argument("--output", default="data/runpod_pilot_" + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S"))
    parser.add_argument("--key", default="~/.ssh/wilf_runpod_ed25519")
    parser.add_argument("--watchdog", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.watchdog:
        return watchdog(args.watchdog)
    try:
        return pilot(args)
    except PilotError as exc:
        note("Preflight stopped: " + str(exc))
        return 1
    except Exception as exc:
        note("Preflight stopped: " + type(exc).__name__ + "; raw details withheld.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
