"""Lead's independent re-implementation of the finite certificate of Theorem T2-SMALL (P5_REPORT section 39),
written from the report text (sections 24-27, 31-39) only; no codex code is imported or consulted.

Primary regime 3m<c<=4m, 7<=a<=13, alpha>=3 low A directions.  A counterexample (W<=-1) must satisfy all of:
  WAbar+Hhat<=-1                         (HOT-ALL with T,X_SR>=0; Hhat=0, or H_cold when beta>=1: COLD-HIGH)
  f_R+b*B_f<=-1                          (fixed-arc payment, R-EXACT lower bound, C/E remainder >=0)
  delta<=Bbig-D3-b*B_H-1                 (DELTA-UP, C/E remainder >=0)
  3delta>=(a-1)(b+1)+(a+1)(q2+u)+D3+(b+2)q2+b*u-3K+1     (LOW-FIN = I-LOW with eta<=3delta)
  b<=B-CUT, b*bc<=B0 (B-NEIGH), m_low<=m_up, delta<=m_up-2,
  WINDOW-SP (short, wide), WINDOW-COUNT (short, wide cubic; PSID wide), PSID short,
  JOINT-SP, JOINT-COUNT, PSP on the alpha+R joint directions.
Differences from the report's loop (all of them enlarge the enumerated set):
  * no use of LC>=(a+1)q2 in the base/t range: for each (u0,u1) the t range is cut by WAbar<=-1 exactly;
  * B-NEIGH bracket bc=u+min(2r,2a-r) is replaced by max(0,bc);
  * MIX-GAP completion (section 38) is applied only with the command-line option 'mix'.
MIX-GAP completion: Delta_d(x)=(d+2)x-3x^<2>, d0=a+b; Gamma=min_{q<=x<=C(d0+1,2)-r-1} Delta_{d0}(x)-2(a-1)r.
If B0<Gamma every AB/BB pair is in I3; then rem=B0-b*u-2br, t_all<=t+br+rem//3,
eps_all=t_all-[C(d0+2,3)-(C(d0+1,2)-r)^<2>]; impossible if rem<0 or eps_all<0; else
m_low2=max(SP on d0+1-r directions, PSP on d0+1), m_up2=C(d0+3,3)-r(1+b)-t+K+c(d0+1)+e with
c(c+1+q+q2+u+ab+B)+e(3a+2b+c+q+q2+u+ab+B)<=rem, B=C(b+1,2); impossible if m_low2>m_up2.
usage: python lead_t2small.py amin amax [mix]"""
import sys
from math import comb, isqrt

def C(n, k): return comb(n, k) if n >= k >= 0 else 0

def mac2(x):  # x^<2>: x = C(k2,2)+C(k1,1), k2>k1>=0
    if x <= 0: return 0
    k2 = 2
    while C(k2+1, 2) <= x: k2 += 1
    k1 = x-C(k2, 2)
    return C(k2+1, 3)+C(k1+1, 2)

def mac3(x):  # x^<3>: x = C(k3,3)+C(k2,2)+C(k1,1)
    if x <= 0: return 0
    k3 = 3
    while C(k3+1, 3) <= x: k3 += 1
    rem = x-C(k3, 3); v = C(k3+1, 4)
    if rem > 0:
        k2 = 2
        while C(k2+1, 2) <= rem: k2 += 1
        k1 = rem-C(k2, 2)
        v += C(k2+1, 3)+C(k1+1, 2)
    return v

def lam2(n):  # 2*lambda_n
    if n <= 1: return 0
    if n == 2: return 2
    if n == 3: return 4
    if n == 4: return 8
    return 3*n if n % 3 == 0 else 3*(n-1)

def Hn(n): return n*(C(n, 2)+1)

def psp(n, r, eps):  # PSP lower bound for 3s-2 (or m)
    er = C(r+1, 2)
    return Hn(n)-4*er-9*(n*er+(r+1)*eps+C(eps, 2))

def sp_ok(len3, n, eps):  # 3s-2 >= H(n)-lambda_n eps, doubled
    return 2*len3 >= 2*Hn(n)-lam2(n)*eps

# sanity of the Macaulay functions against brute force on small cases is in selftest()
def selftest():
    for x in range(0, 200):
        assert mac2(x) >= 0 and mac3(x) >= 0
    for al in range(1, 10):
        assert mac2(C(al+1, 2)) == C(al+2, 3) and mac3(C(al+2, 3)) == C(al+3, 4)
    assert mac2(1) == 1 and mac2(2) == 2 and mac2(3) == 4 and mac3(1) == 1 and mac3(3) == 3 and mac3(4) == 5

_gam = {}
def Gamma(a, d0, q, r):
    key = (a, d0, q, r)
    if key in _gam: return _gam[key]
    hi = C(d0+1, 2)-r-1
    best = None
    for x in range(q, hi+1):
        v = (d0+2)*x-3*mac2(x)
        if best is None or v < best: best = v
    res = None if best is None else best-2*(a-1)*r
    _gam[key] = res
    return res

def mixgap_kills(a, b, r, q, q2, u, t, K, B0):
    d0 = a+b
    G = Gamma(a, d0, q, r)
    if G is not None and B0 >= G: return False   # completion not forced
    rem = B0-b*u-2*b*r
    if rem < 0: return True
    tall = t+b*r+rem//3
    eall = tall-(C(d0+2, 3)-mac2(C(d0+1, 2)-r))
    if eall < 0: return True
    ng = max(0, d0+1-r)
    mlow2 = max(-((-(2*Hn(ng)-lam2(ng)*eall))//2), psp(d0+1, r, eall))
    BB = C(b+1, 2); base = q+q2+u+a*b+BB
    mup2 = None; cc = 0
    while cc*(cc+1+base) <= rem:
        ee = (rem-cc*(cc+1+base))//(3*a+2*b+cc+base)
        v = C(d0+3, 3)-r*(1+b)-t+K+cc*(d0+1)+ee
        mup2 = v if mup2 is None or v > mup2 else mup2
        cc += 1
    return mlow2 > mup2

MIX = False

def run(a):
    Q = C(a+1, 2); U = C(a+2, 3); F = C(a+1, 3)
    sq = isqrt(2*F+1)
    nbase = nu = nprof = npre = 0; surv = []; nmix = [0]
    for alpha in range(3, a+1):
        p = a-alpha; Qa = C(alpha+1, 2); Ua = C(alpha+2, 3)
        for r in range(0, Q+1):
            q = Q-r; tf = U-mac2(q)
            for n0 in range(max(0, Qa-r), Qa+1):
                rLL = Qa-n0
                for l in range(0, alpha*p+1):
                    q2 = n0+l
                    if q2 > q: break
                    E = min(p, l+r)
                    if p > 0:
                        kk, z = divmod(l, p); Smin = kk*p*(a+2-p)+z*(a+2-z)
                    else:
                        Smin = 0
                    CEok = (q+q2+2 >= 2*(alpha+E))
                    base_hit = False
                    m2q2 = mac2(q2)
                    for u0 in range(0, Ua+1):
                        if u0 > m2q2: break
                        K0 = min(mac3(u0), (alpha+3)*u0//4)
                        u1max = min(p*n0, (alpha+1)*l//2, m2q2-u0)
                        for u1 in range(0, u1max+1):
                            K1 = (alpha+2)*u1//3; K = K0+K1; u = u0+u1
                            LCbar = (a+1)*(q2+u)-4*K
                            tmax = min((F-LCbar+(a-3)*r-1)//4, U-u0-u1)
                            for t in range(tf, tmax+1):
                                base_hit = True; nu += 1
                                assert CEok, (a, alpha, r, n0, l)
                                eps = t-tf; D3 = 3*t-(a+2)*r
                                WAbar = -F+LCbar-(a-3)*r+4*t
                                assert WAbar <= -1
                                c0lo = max(u0, Ua-t, Ua-alpha*rLL-eps); c0hi = min(mac2(n0), U-t-u1)
                                for c0 in range(c0lo, c0hi+1):
                                    t0 = Ua-c0
                                    bmx = 0
                                    for be in range(n0, -1, -1):
                                        if mac2(Qa-be) >= Ua-u0-t0: bmx = be; break
                                    else:
                                        continue  # even beta=0 violates COLD-MAC: impossible
                                    branches = [(0, 0)]
                                    if bmx >= 1:
                                        hc = max(0, C(p-E+2, 3)-t+t0)
                                        mn = None
                                        for j in range(0, E+1):
                                            nj = p-j; rj = max(0, r-rLL-max(0, j-l))
                                            v = C(nj+2, 3)-nj*rj-eps
                                            mn = v if mn is None or v < mn else mn
                                        branches.append((bmx, max(hc, mn)))
                                    betaH = min(n0, u0+t0)
                                    CH = alpha+n0+c0+l+E+C(E+2, 3)+(n0+alpha*E)*p
                                    Bbig = 2*CH-(a-1)-(a+3)*q2-(a+1)*u+5*K
                                    BH = a-1+q2+u-2*(alpha+E+l+betaH)
                                    bc = max(0, u+min(2*r, 2*a-r))
                                    ng = max(0, a+1-r)
                                    mlow = max(-((-(2*Hn(ng)-lam2(ng)*eps))//2), psp(a+1, r, eps))
                                    for (beta, Hh) in branches:
                                        if WAbar+Hh >= 0: continue
                                        B0 = -WAbar-Hh-1
                                        Bf = a-1+q2+u-2*alpha-2*beta
                                        bcut = max(3, (B0+2)//2, sq-a)
                                        if bc > 0: bcut = min(bcut, B0//bc)
                                        for R in range(0, p+1):
                                            fR = (D3+a-1-2*alpha-2*beta-2*c0+(a+3)*n0+Smin-2*n0*R
                                                  +(a+1)*u0-5*K0+(a+3)*u1-3*K1)
                                            for b in range(0, bcut+1):
                                                if fR+b*Bf > -1:
                                                    if Bf > 0: break
                                                    continue
                                                budget = B0-b*bc
                                                if budget < 0: break
                                                mup = None; cc = 0
                                                while cc*(cc+1+q+q2+u) <= budget:
                                                    ee = (budget-cc*(cc+1+q+q2+u))//(3*a+2*b+cc+q+q2+u)
                                                    v = C(a+b+3, 3)-r*(1+b)-t+K+cc*(a+b+1)+ee
                                                    mup = v if mup is None or v > mup else mup
                                                    cc += 1
                                                npre += 1
                                                if mlow > mup: continue
                                                dmax = min(Bbig-D3-b*BH-1, mup-2)
                                                need = (a-1)*(b+1)+(a+1)*(q2+u)+D3+(b+2)*q2+b*u-3*K+1
                                                dmin = max(1, -((-need)//3))
                                                if dmin > dmax: continue
                                                nprof += 1
                                                if MIX and mixgap_kills(a, b, r, q, q2, u, t, K, B0):
                                                    nmix[0] += 1; continue
                                                ok = []
                                                for delta in range(dmin, dmax+1):
                                                    w = (delta+1)//2
                                                    ns = max(0, R-l-2*r); nw = max(0, R-r); nc = max(0, R-l-r)
                                                    if not sp_ok(3*w-2, ns, eps): continue
                                                    if not sp_ok(3*delta-2, nw, eps): continue
                                                    if C(nc+2, 3)-t > 3*w-2: continue
                                                    if C(R+2, 3)-t > 3*delta-2: continue
                                                    if R*(R-1) > 2*delta-2+2*r*(r+1): continue
                                                    if nc*(nc-1) > 2*w-2+2*r*(r+1): continue
                                                    sj = (3*delta+1)//2
                                                    nj = max(0, alpha+R-r)
                                                    if not sp_ok(3*sj-2, nj, eps): continue
                                                    if C(alpha+R+2, 3)-t > 3*sj-2: continue
                                                    if psp(alpha+R, r, eps) > 3*sj-2: continue
                                                    ok.append(delta)
                                                if ok:
                                                    surv.append(dict(a=a, alpha=alpha, r=r, n0=n0, l=l, t=t, u0=u0,
                                                                     u1=u1, c0=c0, beta=beta, R=R, b=b,
                                                                     deltas=(ok[0], ok[-1], len(ok)), WAbar=WAbar,
                                                                     Hhat=Hh, mup=mup, mlow=mlow))
                    if base_hit: nbase += 1
    return nbase, nu, npre, nprof, surv, nmix[0]

if __name__ == '__main__':
    selftest()
    amin, amax = int(sys.argv[1]), int(sys.argv[2]); MIX = 'mix' in sys.argv[3:]
    tot = []
    for a in range(amin, amax+1):
        nb, nu, npre, npf, sv, nmx = run(a)
        tot += sv
        print(f"a={a} base states={nb} u-states={nu} profiles reaching cardinality test={npre} with nonempty delta range={npf} killed by MIX-GAP={nmx} survivors={len(sv)}", flush=True)
        for s in sv[:8]: print("   ", s, flush=True)
    print("total survivors", len(tot))
