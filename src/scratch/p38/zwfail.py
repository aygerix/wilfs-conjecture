# zwfail: the residual S with mu <= e where e z < c_U (ZW needs Delta3): print structure.
import sys
exec(open('zwid.py').read().split('rows = []')[0])
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            m = int(t[1]); A = list(map(int, t[15:]))
            if A[0] > len(A) + 1: continue
            r = analyse(m, A)
            if r['e'] * r['z'] < r['cU']:
                print(f"m={m} A={A} mu={A[0]} z={r['z']} ez={r['e']*r['z']} cU={r['cU']} D3={r['D3']} N<={r['Nlt']} Nns={r['Nns']} Ov={r['Ov']} Q'={r['Qp']} m/mu={m/A[0]:.1f}")
