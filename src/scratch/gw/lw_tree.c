/* Semigroup tree to genus G.  For each S: PF numbers, type t, e, m, c, Wilf slack.
 * Checks the per-depth PF reflection |U_j| <= #{f in PF : f >= (j-1)m} * |L_j| for every j, and counts:
 *   H0: t <= e-1 (classical FGH);  H1: #{PF >= m} <= e-1;  H2: #{PF >= 2m} <= e-1;  H3: #{PF >= 3m} <= e-1 (needs P_3).
 * Every S with H1 or H2 must satisfy Wilf (corollaries of GW-14 / GW-16 + reflection). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static uint64_t lw_fail, lwp_fail, lw_tight; static int64_t lw_min = 1<<30;
static int G; static uint64_t cnt, h0, h1, h2, h3, refl_fail, wilf_fail_h, wilf_fail;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt++;
  int c = F + 1;
  if (c > 0) {
    int isS[256]; for (int z = 0; z < 256; z++) isS[z] = !gapq(gm, z);
    int pf[128], t = 0;
    for (int z = 1; z <= F; z++) if (!isS[z]) { int ok = 1; for (int j = 0; j < e && ok; j++) if (!isS[z + gens[j]]) ok = 0; if (ok) pf[t++] = z; }
    int c1 = 0, c2 = 0, c3 = 0; for (int i = 0; i < t; i++) { if (pf[i] >= m) c1++; if (pf[i] >= 2 * m) c2++; if (pf[i] >= 3 * m) c3++; }
    /* Kunz kappa_r and lambda_r per class */
    int K = (c + m - 1) / m + 2;
    for (int j = 1; j <= K; j++) {
      int U = 0, L = 0, tj = 0;
      for (int r = 0; r < m; r++) {
        int w = r; while (!isS[w]) w += m;              /* Apery element of class r */
        if (w / m >= j) U++;
        int lam = 0; for (int s = w; s < c; s += m) lam++;
        if (lam >= j) L++;
      }
      for (int i = 0; i < t; i++) if (pf[i] >= (j - 1) * m) tj++;
      if (U > (int64_t)tj * L) refl_fail++;
    }
    int ell = 0; for (int z = 0; z < c; z++) ell += isS[z];
    { int ap[128]; for (int r = 0; r < m; r++) { int w = r; while (!isS[w]) w += m; ap[r] = w; }
      int inAp[512] = {0}; for (int r = 0; r < m; r++) inAp[ap[r]] = 1;
      int H[128]; for (int r = 0; r < m; r++) { H[r] = 0; for (int q = 0; q < m; q++) { int y = ap[r] + ap[q]; if (y < 512 && inAp[y] && ap[q] > H[r]) H[r] = ap[q]; } }
      int gg = 0; for (int r = 0; r < m; r++) gg += ap[r] / m;
      int64_t rhs = 0; for (int r = 0; r < m; r++) rhs += H[r] / m;
      int64_t sl = (int64_t)(e - 1) * rhs - gg; if (sl < 0) lw_fail++; if (sl < lw_min) lw_min = sl; if (sl == 0) lw_tight++;
      int top = 0; for (int r = 0; r < m; r++) { if (ap[r]/m > top) top = ap[r]/m; }
      for (int i = 1; i <= top; i++) { int64_t L = 0, R = 0; for (int r = 0; r < m; r++) { int k = ap[r]/m; L += k < i ? k : i; int h = H[r]/m; R += h < i ? h : i; }
        if (L > (int64_t)(e - 1) * R) { lwp_fail++; break; } } }
    int wilf = e * ell - c;
    if (t <= e - 1) h0++;
    if (c1 <= e - 1) h1++;
    if (c2 <= e - 1) h2++;
    if (c3 <= e - 1) h3++;
    if (wilf < 0) wilf_fail++;
    if (wilf < 0 && (c1 <= e - 1 || c2 <= e - 1)) wilf_fail_h++;
  } else { h0++; h1++; h2++; h3++; }
  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int n = gens[j]; if (n <= F) continue;
    u128 gm2 = gm | ((u128)1 << n); int e2 = 0, m2;
    if (n == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else {
      m2 = m; for (int k = 0; k < e; k++) if (gens[k] != n) ng[e2++] = gens[k];
      int y = n + m, dec = 0;
      for (int a = m; a <= y / 2 && !dec; a++) if (a != n && !gapq(gm2, a) && (y - a) != n && !gapq(gm2, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, n, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("genus<=%d semigroups=%llu  t<=e-1: %llu (%.2f%%)  #PF>=m <=e-1: %llu (%.2f%%)  #PF>=2m <=e-1: %llu (%.2f%%)  #PF>=3m <=e-1: %llu (%.2f%%)\n",
    G, (unsigned long long)cnt, (unsigned long long)h0, 100.0*h0/cnt, (unsigned long long)h1, 100.0*h1/cnt, (unsigned long long)h2, 100.0*h2/cnt, (unsigned long long)h3, 100.0*h3/cnt);
  printf("LOCAL Wilf failures: %llu  local-prefix failures: %llu  min local slack %lld  tight %llu\n", (unsigned long long)lw_fail, (unsigned long long)lwp_fail, (long long)lw_min, (unsigned long long)lw_tight);
  printf("per-depth PF reflection failures: %llu ; Wilf failures: %llu ; Wilf failures under H1 or H2: %llu\n",
    (unsigned long long)refl_fail, (unsigned long long)wilf_fail, (unsigned long long)wilf_fail_h);
  return 0;
}
