/* Per-column inequality PCI for the uniform residue-free window theorem H_i.
 * Dominant b-column with base z (all weights of supp z <= n_b), u = v(z), beta = sum_a F(z_a n_a), F(t)=min(i,floor(t/q)).
 * PCI:  sum_{j=1..J} F(u + j n_b) <= J*beta + sum_{j=0..J} F(M - u - j n_b),   for M >= max(u + J n_b, (2i-2)q - 1).
 * The worst M is the smallest admissible one.  z is enumerated as a multiset of components (n_a, z_a), n_a in (q, n_b],
 * z_a >= 1, up to NC components.  fejer only.   Usage: pci i qmax NC [thr_num thr_den]  (threshold = thr*q - 1)  */
#include <stdio.h>
#include <stdlib.h>
static int I, Q, NC, NODOM, SHOWT; static long fails, tests, tight; static double THR;
static int F(long t, int q) { long f = t / q; return f < I ? (int)f : I; }
static int q, nb; static long comp_u[8], comp_b[8];
static void check(long u, long beta, int ncomp) {
  if (ncomp == 0) return;
  long thr = (long)(THR * q) - 1;
  for (int J = 1; ; J++) {
    long top = u + (long)J * nb; long M = top > thr ? top : thr;
    if (top > (long)(4 * I + 4) * q + 4 * nb) break;
    long L = 0, R = (long)J * beta;
    for (int j = 1; j <= J; j++) L += F(u + (long)j * nb, q);
    for (int j = 0; j <= J; j++) R += F(M - u - (long)j * nb, q);
    tests++;
    if (L == R && SHOWT && tight++ < 25 && ncomp >= 1) { printf("TIGHT i=%d q=%d nb=%d J=%d u=%ld beta=%ld M=%ld L=%ld comps:", I, q, nb, J, u, beta, M, L); for (int c = 0; c < ncomp; c++) printf(" (%ld,%ld)", comp_u[c], comp_b[c]); printf("\n"); }
    if (L > R) { fails++; if (fails <= 8) { printf("FAIL i=%d q=%d nb=%d J=%d u=%ld beta=%ld M=%ld L=%ld R=%ld comps:", I, q, nb, J, u, beta, M, L, R); for (int c = 0; c < ncomp; c++) printf(" (%ld,%ld)", comp_u[c], comp_b[c]); printf("\n"); } }
  }
}
/* enumerate components: value c = z_a*n_a with q < n_a <= nb, z_a >= 1, nondecreasing order of (n_a, z_a) to limit dupes */
static void rec(int k, long u, long beta, int minn, int minz) {
  check(u, beta, k);
  if (k == NC) return;
  for (int na = minn; na <= (NODOM ? 3 * q : nb); na++)
    for (int za = (na == minn ? minz : 1); ; za++) {
      long cv = (long)za * na; if (u + cv > (long)(2 * I + 2) * q) break;
      comp_u[k] = cv; comp_b[k] = F(cv, q);
      rec(k + 1, u + cv, beta + F(cv, q), na, za);
    }
}
int main(int argc, char **argv) {
  NODOM = getenv("NODOM") != 0; SHOWT = getenv("SHOWT") != 0;
  I = atoi(argv[1]); Q = atoi(argv[2]); NC = atoi(argv[3]); THR = argc > 5 ? (double)atoi(argv[4]) / atoi(argv[5]) : 2 * I - 2;
  for (q = 2; q <= Q; q++) for (nb = q + 1; nb <= 3 * q; nb++) rec(0, 0, 0, q + 1, 1);
  printf("i=%d q<=%d NC=%d thr=%.3fq-1: tests=%ld fails=%ld\n", I, Q, NC, THR, tests, fails);
  return 0;
}
