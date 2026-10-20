/* Does the generalized-core reduction of the conjectures.io depth-four proof extend to other depths? (lead, 2026-10-20)
 * For S with c > 2m: A = generators of S in [m, 2m), T = <A> u [c, inf) (the "generalized core"; c_T <= c).
 * Report per depth q = ceil(c/m):
 *   (1) failures of W(S) >= W(T)  (plain transfer; would reduce Wilf to cores at that depth);
 *   (2) failures of 23(d_S - d_T) <= 13(W0(S) - W0(T)) among S with W0(S) < 0 (c_T = c always: c-1 is a gap of S), with W0 = n*l - q*d + rho,
 *       rho = q*m - c, n = #primitives < c, l = |X n [0,c)|, d = #decomposables in [c, c+m)  (their Theorem A form);
 *   (3) the least lambda making lambda*(d_S - d_T) <= W0(S) - W0(T) hold on all S with d_S > d_T (max ratio).
 * W(T) = e_T * l_T - c_T with T's own conductor and primitives.
 * gcc -O3 -o coretr coretr.c ; ./coretr G */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned __int128 u128;
#define QM 40
static int G; static long long nS, nq[QM], f1[QM], f2[QM], nc[QM], nneg[QM]; static long long w1[QM]; static int w1m[QM], w1c[QM], w1e[QM], w1g[QM][64];
static double lam[QM]; static int lm[QM], lc[QM], le[QM], lg[QM][64];
static inline int inS(u128 g, int F, int x) { return x >= 0 && (x > F || !((g >> x) & 1)); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  nS++;
  int c = F + 1;
  if (c > 2 * m) {
    int q = (c + m - 1) / m; if (q >= QM) q = QM - 1;
    nq[q]++;
    static char T[400];
    int A[64], k = 0;
    for (int i = 0; i < e; i++) if (gens[i] < 2 * m) A[k++] = gens[i];
    int top = c + 2 * m + 2;
    for (int x = 0; x < top; x++) {
      if (x >= c) { T[x] = 1; continue; }
      T[x] = (x == 0);
      for (int i = 0; i < k && !T[x]; i++) if (A[i] <= x && T[x - A[i]]) T[x] = 1;
    }
    int cT = 0; for (int x = c - 1; x >= 0; x--) if (!T[x]) { cT = x + 1; break; }
    long long lT = 0; for (int x = 0; x < cT; x++) lT += T[x];
    long long eT = k;
    for (int x = cT; x < cT + m; x++) {
      if (x < 2 * m) continue; /* x in [m,2m) members of T below c are in A or decomposable; x >= cT here */
      int dec = 0;
      for (int y = m; y <= x - m && !dec; y++) if (T[y] && T[x - y]) dec = 1;
      if (!dec) eT++;
    }
    /* members of [cT, 2m) that are not in A and not decomposable would also be primitive */
    for (int x = cT; x < 2 * m && x < cT + m; x++) {
      int inA = 0; for (int i = 0; i < k; i++) if (A[i] == x) inA = 1;
      if (inA) continue;
      int dec = 0; for (int y = m; y <= x - m && !dec; y++) if (T[y] && T[x - y]) dec = 1;
      if (!dec) eT++;
    }
    long long lS = 0; for (int x = 0; x < c; x++) lS += inS(gm, F, x);
    long long WS = (long long)e * lS - c, WT = eT * lT - cT;
    long long d1 = WS - WT;
    if (d1 < 0) { f1[q]++; if (d1 < w1[q]) { w1[q] = d1; w1m[q] = m; w1c[q] = c; w1e[q] = e; for (int i = 0; i < e; i++) w1g[q][i] = gens[i]; } }
    if (cT == c) {
      nc[q]++;
      int rho = q * m - c;
      long long nS_ = 0, nT_ = 0, dS = 0, dT = 0;
      for (int i = 0; i < e; i++) if (gens[i] < c) nS_++;
      nT_ = k; /* all of A is below c (A < 2m < c) */
      for (int x = c; x < c + m; x++) {
        int decS = 0, decT = 0;
        for (int y = m; y <= x - m && !(decS && decT); y++) {
          if (!decS && inS(gm, F, y) && inS(gm, F, x - y)) decS = 1;
          if (!decT && T[y] && T[x - y]) decT = 1;
        }
        dS += decS; dT += decT;
      }
      long long W0S = nS_ * lS - (long long)q * dS + rho, W0T = nT_ * lT - (long long)q * dT + rho;
      if (W0S >= 0) goto done; /* Theorem A is only claimed when W0(S) < 0 */
      nneg[q]++;
      if (23 * (dS - dT) > 13 * (W0S - W0T)) f2[q]++;
      if (dS > dT) {
        double r = (double)(dS - dT) > 0 ? (double)(W0S - W0T) / (double)(dS - dT) : 0;
        /* need lambda <= r for all; record the minimum r (the best possible lambda) */
        if (lam[q] == 0 || r < lam[q]) { lam[q] = r; lm[q] = m; lc[q] = c; le[q] = e; for (int i = 0; i < e; i++) lg[q][i] = gens[i]; }
      }
    }
  }
  done:
  if (g == G) return;
  int ng[128];
  for (int jj = 0; jj < e; jj++) {
    int nn = gens[jj]; if (nn <= F) continue;
    u128 gm2 = gm | ((u128)1 << nn);
    int e2 = 0, m2;
    if (nn == m) { m2 = m + 1; for (int kk = m2; kk <= 2 * m2 - 1; kk++) ng[e2++] = kk; }
    else {
      m2 = m;
      for (int kk = 0; kk < e; kk++) if (gens[kk] != nn) ng[e2++] = gens[kk];
      int y = nn + m, dec = 0;
      for (int a = m; a <= y / 2 && !dec; a++) if (a != nn && inS(gm2, nn, a) && (y - a) != nn && inS(gm2, nn, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, nn, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); if (G > 60) return 1;
  for (int q = 0; q < QM; q++) { w1[q] = 0; lam[q] = 0; }
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("genus <= %d: %lld semigroups\n", G, nS);
  for (int q = 3; q < QM; q++) if (nq[q]) {
    printf("q=%d: %lld S; (1) W(S)<W(T): %lld", q, nq[q], f1[q]);
    if (f1[q]) { printf(" worst %lld at m=%d c=%d gens=", w1[q], w1m[q], w1c[q]); for (int i = 0; i < w1e[q]; i++) printf("%d,", w1g[q][i]); }
    printf("; W0(S)<0: %lld, (2) 23/13 fails among them: %lld; (3) min ratio (W0S-W0T)/(dS-dT) = %.4f", nneg[q], f2[q], lam[q]);
    if (lam[q] != 0) { printf(" at m=%d c=%d gens=", lm[q], lc[q]); for (int i = 0; i < le[q]; i++) printf("%d,", lg[q][i]); }
    printf("\n");
  }
  return 0;
}
