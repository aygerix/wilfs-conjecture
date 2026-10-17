"""Continuous analogue of Tile-CL for the polyomino D+[0,1)^d (numerical, Monte Carlo-free):
a(h) = sum_y B(h - N0(y)), B = density of <u,p> (u uniform in [0,1)^d).
Claim (cont-CL): mu(sigma) := sum_j h_j a(h_j), h_j = j m - sigma (j>=1)  >=  mean_sigma mu - m/2.
B computed exactly on a grid of step 1/K via convolution of uniform densities."""
import sys, itertools
import numpy as np
sys.path.insert(0,'src')
from exp_cl_tiling import downsets
K=60
def Bdens(p):
    # density of sum p_a u_a on grid of step 1/K
    f=np.array([1.0])
    for pa in p:
        if pa==0: continue
        box=np.ones(pa*K)/(pa*K)   # uniform on [0,pa)
        f=np.convolve(f,box)
    return f*K  # density values at grid points (approx)
worst=[]
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(3,M+1):
  for D in downsets(m,d):
    Dl=sorted(D)
    if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
    for p in itertools.product(range(m),repeat=d):
      N0=[sum(x*y for x,y in zip(n,p)) for n in Dl]
      if len({x%m for x in N0})!=m: continue
      B=Bdens(p); H=(max(N0)+sum(p))*K+len(B)+m*K
      a=np.zeros(H)
      for n0 in N0: a[n0*K:n0*K+len(B)]+=B
      mus=[]
      for sg in range(m*K):           # sigma = sg/K
        idx=np.arange(m*K-sg, H, m*K)
        h=idx/K
        mus.append(float(np.sum(h*a[idx])/K*1.0))
      mus=np.array(mus)
      # normalization: sum_j a(h_j) should be ~1 (density per unit h)... a is density in h; fiber weights a(h_j) sum to 1
      slack=mus.min()-(mus.mean()-m/2)
      worst.append((slack,m,Dl,p))
worst.sort()
print('d',d,'worst slacks:',[(round(w[0],3),w[1],w[3]) for w in worst[:5]])
