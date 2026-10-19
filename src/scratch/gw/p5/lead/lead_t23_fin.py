"""Lead's independent re-implementation of the finite certificate of Theorem T2.3F (P5_REPORT section 27),
written from the report text only.  For alpha=3, r=r_A in {0,1,2}, 0<=l<=4-2r, 6-r<=n0<=6, it enumerates all
count profiles (a,r,l,n0,t,R,b) admitted by FIN, then every delta in FIN's range, and applies PSID (3L-PACK),
WINDOW-SP and WINDOW-COUNT.  A profile survives if some delta passes all of them.
At a=13 the b coefficient B_f is replaced by max(1,B_f) (report section 27).
usage: python lead_t23_fin.py amin amax"""
import sys
from math import comb

def lam2(n):  # doubled lambda_n
    if n <= 1: return 0
    if n == 2: return 2
    if n == 3: return 4
    if n == 4: return 8
    return 3*n if n % 3 == 0 else 3*(n-1)

def Hn(n): return n*(comb(n, 2)+1)

def C3(x): return comb(x, 3) if x >= 3 else 0

def run(a, joint=False, retain=False):
    F = comb(a+1, 3)
    pre = 0; surv = []; ntup = 0
    for r in (0, 1, 2):
        tf = (0, a, 2*a-1)[r]
        for l in range(0, 4-2*r+1):
            Sl = l*(a+2-l)
            for n0 in range(6-r, 7):
                q2 = n0+l
                e0 = l+r
                Bf = a-7-n0+l
                if a == 13: Bf = max(1, Bf)
                assert Bf >= 1
                Bh = a-7-n0-3*l-2*r
                B = 2*(13+n0+l+e0+C3(e0+2)+(n0+3*e0)*(a-3))-(a-1)-(a+3)*(n0+l)
                tmax = (F-(a+1)*q2+(a-3)*r-1)//4
                for t in range(tf, tmax+1):
                    D3 = 3*t-(a+2)*r
                    eps = t-tf
                    for R in range(0, a-3+1):
                        Fr = 15-5*a+Sl+D3
                        Fc = a-27+(a+3)*n0+Sl-2*n0*R-(a+2)*r
                        if retain:  # keep D3-3t0 >= 3(t-t0max)-(a+2)r; forced cubics avoid the pure-low face when n0=6
                            t0max = min(10, t-tf) if n0 == 6 else min(10, t)
                            Fc += 3*(t-t0max)
                        Fw = a-39+(a+3)*n0+Sl-2*n0*R+D3
                        K = max(Fr, Fc, Fw)
                        if K > -1: continue
                        b = 0
                        while K+b*Bf <= -1:
                            dmax = B-D3-b*Bh-1
                            if dmax >= 1:
                                pre += 1
                                ok = []
                                for delta in range(1, dmax+1):
                                    w = (delta+1)//2
                                    n = max(0, R-l-r)
                                    if n*(n-1) > 2*w-2+2*r*(r+1): continue
                                    ns = max(0, R-l-2*r); nw = max(0, R-r)
                                    if 2*(3*w-2) < 2*Hn(ns)-lam2(ns)*eps: continue
                                    if 2*(3*delta-2) < 2*Hn(nw)-lam2(nw)*eps: continue
                                    nc = max(0, R-l-r)
                                    if comb(nc+2, 3)-t > 3*w-2: continue
                                    if comb(R+2, 3)-t > 3*delta-2: continue
                                    if R*(R-1) > 2*delta-2+2*r*(r+1): continue
                                    if joint:  # JOINT-SP: 3 lows + R highs in [L,theta-2L), s=ceil(3delta/2)
                                        nj = max(0, 3+R-r); sj = (3*delta+1)//2
                                        if 2*(3*sj-2) < 2*Hn(nj)-lam2(nj)*eps: continue
                                    ok.append(delta)
                                if ok:
                                    surv.append((a, r, l, n0, t, R, b, min(ok), max(ok), len(ok)))
                                    ntup += len(ok)
                            b += 1
    return pre, surv, ntup

if __name__ == '__main__':
    amin, amax = int(sys.argv[1]), int(sys.argv[2]); joint = 'joint' in sys.argv[3:]; retain = 'retain' in sys.argv[3:]
    tot = []
    for a in range(amin, amax+1):
        pre, surv, ntup = run(a, joint, retain)
        tot += surv
        print(f"a={a} pre-packing profiles={pre} surviving profiles={len(surv)} expanded delta tuples={ntup} "
              f"max b={max((s[6] for s in surv), default=-1)}", flush=True)
    print("total surviving", len(tot), "expanded", sum(s[9] for s in tot))
    for s in tot[:10]: print("  ", s)
