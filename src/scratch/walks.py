import sys
sys.path.insert(0,'src')
from exp_cl_tiling import Tvals
def show(Dl, p):
    d=len(p); m=len(Dl); D=set(Dl)
    T=Tvals(D,d)
    phi={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
    inv={v:k for k,v in phi.items()}
    # per-direction T_a
    Ta=[{n:(n[a]+1 if tuple(n[:a]+(n[a]+1,)+n[a+1:]) not in D else 0) for n in Dl} for a in range(d)]
    print('D',Dl,'p',p,'m',m)
    print(' res :', ' '.join(f'{r:3d}' for r in range(m)))
    print(' cell:', ' '.join(''.join(map(str,inv[r])).rjust(3) for r in range(m)))
    for a in range(d):
        print(f' T_{a+1} :', ' '.join(f'{Ta[a][inv[r]]:3d}' for r in range(m)))
    print(' T   :', ' '.join(f'{T[inv[r]]:3d}' for r in range(m)))
    f=[sum(T[inv[y]]*((s-y)%m) for y in range(m)) for s in range(m)]
    tgt=(d-1)*m*(m-1)//2
    print(' slack(s)=f(s)-target:', [x-tgt for x in f])
    for a in range(d):
        fa=[sum(Ta[a][inv[y]]*((s-y)%m) for y in range(m)) for s in range(m)]
        print(f'  f_{a+1}(s)-m(m-1)/2:', [x-m*(m-1)//2 for x in fa])
show([(0,0,0),(0,0,1),(0,0,2),(0,1,0),(1,0,0),(1,0,1)],(3,5,4))
show([(0,0),(0,1),(1,0),(1,1),(2,0),(2,1),(3,0),(4,0)],(1,5))
show([(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)],(1,4))
