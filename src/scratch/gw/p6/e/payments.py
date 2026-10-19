"""Exact P6e payment predicates. Execution only on fejer."""
from collections import Counter
from math import comb


def cubic_data(m, U, Q, T, rho):
    kp = {z:(sum(U[i] for i in z)-rho)//m for z in Q}
    kt = {y:(sum(U[i] for i in y)-2*rho)//m for y in T}
    rt = {y:(sum(U[i] for i in y)-2*rho)%m for y in T}
    bad = []
    gain = 0
    types = Counter()
    for y in T:
        ks = [kp[y[:j]+y[j+1:]] for j in range(3)]
        v = int(rt[y] >= m-rho)
        b = 2*kt[y]-sum(ks)+v
        gain += max(0, b)
        if b != -1:
            continue
        bad.append(y)
        if kt[y] == 1 and v == 0 and ks == [1, 1, 1]:
            types['A'] += 1
        elif kt[y] == -1 and v == 1 and ks == [0, 0, 0]:
            types['D'] += 1
        else:
            raise AssertionError(('BAD-TWO', m, U, y, rho, kt[y], ks, v))
        assert all(U[i]>rho for i in y) if kt[y]==1 else all(U[i]<rho for i in y)
    return kp, kt, rt, bad, gain, types


def origin(m, U, Q, T, ans):
    k = len(U)
    rp = {z:sum(U[i] for i in z)%m for z in Q}
    kp, kt, rt, bad, gain, types = cubic_data(m, U, Q, T, 0)
    assert types['A'] == len(bad)
    assert all(2*rt[y] > m and sum(2*U[i] > m for i in y) >= 2 for y in bad)
    H = sum(2*u > m for u in U)
    l = k-H
    q0 = sum(kp[z] == 0 for z in Q)
    q0L = sum(kp[z] == 0 and 2*rp[z] <= m for z in Q)
    qpH = sum(kp[z] == 1 and 2*rp[z] > m for z in Q)
    bs = set(bad)
    nu = n0H = gH = E = 0
    pure_low = one_high = 0
    for y in T:
        kap = 2*kt[y]-sum(kp[y[:j]+y[j+1:]] for j in range(3))
        if y in bs:
            continue
        if kap == 0:
            if 2*rt[y] <= m:
                nu += 1
                if kt[y] == 0:
                    assert sum(U[i] for i in y) <= m//2
                    assert all(2*U[i] <= m for i in y)
                    pure_low += 1
                else:
                    assert kt[y] == 1
                    assert sum(2*U[i] > m for i in y) == 1
                    assert sum(kp[y[:j]+y[j+1:]] for j in range(3)) == 2
                    one_high += 1
            else:
                n0H += 1
        else:
            assert kap > 0
            gH += 2*rt[y] > m
            E += kap-1
    used = {0, *U, *rp.values(), *rt.values()}
    sH = sum(2*r > m for r in range(1, m) if r not in used)
    h = (m-1)//2
    pi = m-1-2*h
    half = (pi+H-l+q0-ans['s']-nu+2*sH-2*q0L+2*qpH+n0H+2*gH+E)
    assert ans['S'] == ans['Lplus']+m*half
    assert nu == pure_low+one_high
    if H <= 1:
        assert len(bad) <= ans['Pplus']
        assert ans['HC'] >= 0
    if len(bad) <= 3:
        assert len(bad) <= ans['Pplus']
        assert ans['HC'] >= 0
    if l == 0 and k >= 2:
        assert 2*ans['S'] >= m*(2*(ans['e']+k+pi)+(k-2)*ans['s'])
        assert ans['S'] >= 0
        if len(bad)<=5 or k>=2*len(T):
            assert ans['HC']>=0
    if l <= 1:
        assert ans['S'] >= 0
    if l==1 and H>=2:
        v=next(u for u in U if 2*u<=m)
        j=sum(u+v>m for u in U if 2*u>m)
        if 4*v>m:
            c=H-1+int(nu>0)-nu
            assert 2*ans['S']>=2*m*c+ans['s']*(H*m+2*v-2*m)
        else:
            assert 4*ans['S']>=m*(6*H-12+3*j*(j-1))+4*ans['s']*(sum(U)-m)
    if l and H >= 2 and all(4*u <= m or 2*u > m for u in U):
        low = [u for u in U if 2*u <= m]
        j = sum(u+max(low) > m for u in U if 2*u > m)
        Ql, Ul = comb(l+1, 2), comb(l+2, 3)
        p4 = 2*(l+2)*H-4*(l+Ql+Ul)+3*j*j-(2*l*l+4*l-3)*j
        assert 4*ans['S'] >= m*p4
        if p4 >= 0:
            assert ans['S'] >= 0
    return dict(H=H,l=l,nu=nu,pure_low=pure_low,one_high=one_high,
                q0=q0,q0L=q0L,qpH=qpH,sH=sH,n0H=n0H,gH=gH,E=E,pi=pi)


def defect(m, U, Q, ans):
    k = len(U)
    deg = Counter(i for z in Q for i in z)
    D = [i for i in range(k) if deg[i] < k+1]
    v = len(D)
    e = comb(k+1,2)-len(Q)
    A = sum((k+1-deg[i])*U[i] for i in range(k))
    assert 18*A >= v*(v+1)*(v-3)
    assert 10*A >= v*(v+1)*(v-3)
    if v:
        assert 8*(5*v+4)*A>=4*v**4-16*v*v-12*v-1
    t = ans['t']
    if t >= 2 and k >= 40*t+8:
        assert ans['HC'] >= 0
    return v


def few_cutoff(k,t):
    C = comb(k,2)
    if C <= t:
        return None
    M0 = comb(k+2,2)
    smax = (t*(M0+t)-1)//(C-t)
    mmax = M0+t+smax
    vmin = max(0,k+1-(mmax-1)//k)
    closes = vmin >= 3 and vmin*(vmin+1)*(vmin-3) >= 18*mmax*t
    return dict(smax=smax,mmax=mmax,vmin=vmin,closes=closes)


def few_cutoff_linked(k,t):
    a=few_cutoff(k,t)
    if a is None:return None
    v=a['vmin']
    N=4*v**4-16*v*v-12*v-1
    a['closes']=v>=1 and N>=8*(5*v+4)*a['mmax']*t
    return a
