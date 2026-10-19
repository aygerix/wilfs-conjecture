"""VOL-MINK constants: beta_d = 2^d / C(2d,d); sigma*_d = least root in (0,1) of sigma + (beta_d (1 - sigma^d))^(1/d) = 1;
g(s) = 1/sum_{j=1..d} s^-j;  K_d = (d-1)/(2 g(sigma*_d)).  Theorem: Lambda := c + m - 1 + N >= K_d (N + m - 1)  ==>  W >= 0.
Also the data-free bound mu = m/V <= mu*_d = 1 - sigma*^d."""
from mpmath import mp, mpf, binomial, findroot
mp.dps = 30
def g(s, d): return 1/sum(s**(-j) for j in range(1, d+1))
for d in range(2, 13):
    beta = mpf(2)**d / binomial(2*d, d)
    f = lambda s: s + (beta*(1 - s**d))**(mpf(1)/d) - 1
    # bracket the least root: f(0) = beta^(1/d) - 1 < 0; scan
    lo = mpf('1e-9'); x = lo; step = mpf('0.001')
    while f(x + step) < 0: x += step
    s = findroot(f, (x, x + step), solver='bisect') if f(x) < 0 < f(x+step) else findroot(f, x)
    K = (d - 1)/(2*g(s, d))
    print('d=%2d e=%2d beta=%.5f sigma*=%.5f mu*=%.5f g=%.6f K_d=%.2f  K_d/((d-1)2^d)=%.3f' % (d, d+1, beta, s, 1 - s**d, g(s, d), K, K/((d-1)*2**d)))
