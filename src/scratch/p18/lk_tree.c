/* LAYER-KNESER on the tree of numerical semigroups (genus <= G).  For S with c > m, D = ceil(c/m),
 * k = |S cap (m,2m)|, B = {0} u (S cap (m,2m)) - m.  If k >= 1 and gcd(m, B) = 1, with delta = k (m prime) or
 * ceil((k+1)/2):  (step) g_H >= g_{H+2} + delta for H+2 <= D-1;  (LB) ell >= D + (D-2)k + delta*floor((D-3)^2/4)
 * (sharpened form; the earlier D + k floor((D-1)/2) + delta floor((D-2)^2/4) is also counted for comparison).
 * Coverage: LK = e*LB >= c; DKM = D > 2 and k^2 (D-2) >= D m; LIT = c <= 3m or 3e >= m or m <= 18.
 * gcc -O3 -std=gnu11 lk_tree.c -o lk_tree */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G;
static uint64_t cnt[80], hyp[80], stepfail, lbfail, lk[80], dkm[80], lkonly[80], lkonly_nolit[80], open_[80], lknew[80];
static int64_t minsl = INT64_MAX; static uint64_t lb0better;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int isprime(int n) { if (n < 2) return 0; for (int p = 2; p * p <= n; p++) if (n % p == 0) return 0; return 1; }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt[g]++;
  int c = F + 1;
  if (c > m && m >= 2) {
    int D = (c + m - 1) / m, k = 0, gb = m;
    for (int s = m + 1; s < 2 * m; s++) if (!gapq(gm, s)) { k++; gb = gcd(gb, s - m); }
    int lit = (c <= 3 * m) || (3 * e >= m) || (m <= 18);
    int dk = D > 2 && (int64_t)k * k * (D - 2) >= (int64_t)D * m;
    if (k >= 1 && gb == 1) {
      hyp[g]++;
      int delta = isprime(m) ? k : (k + 2) / 2;
      int gh[64];
      for (int H = 0; H < D; H++) { int t = 0; for (int r = 0; r < m; r++) if (gapq(gm, H * m + r)) t++; gh[H] = t; }
      for (int H = 0; H + 2 <= D - 1; H++) if (gh[H] < gh[H + 2] + delta) { stepfail++;
        if (stepfail <= 3) fprintf(stderr, "STEP FAIL m=%d c=%d H=%d\n", m, c, H); break; }
      int64_t LB = D + (int64_t)k * (D - 2) + (int64_t)delta * (((D - 3) * (D - 3)) / 4);
      int64_t LB0 = D + (int64_t)k * ((D - 1) / 2) + (int64_t)delta * (((D - 2) * (D - 2)) / 4);
      if (LB0 > LB) lb0better++;
      int64_t ell = c - g;
      if (ell < LB) { lbfail++; if (lbfail <= 3) fprintf(stderr, "LB FAIL m=%d c=%d\n", m, c); }
      if (ell - LB < minsl) minsl = ell - LB;
      int l = (int64_t)e * LB >= c;
      lk[g] += l; lkonly[g] += l && !dk; lkonly_nolit[g] += l && !dk && !lit;
    }
    dkm[g] += dk;
    open_[g] += !lit && !dk;
  }
  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int n = gens[j]; if (n <= F) continue;
    u128 gm2 = gm | ((u128)1 << n);
    int e2 = 0, m2;
    if (n == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else {
      m2 = m;
      for (int k = 0; k < e; k++) if (gens[k] != n) ng[e2++] = gens[k];
      int y = n + m, dec = 0;
      for (int a = m; a <= y / 2 && !dec; a++) if (a != n && !gapq(gm2, a) && (y - a) != n && !gapq(gm2, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, n, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); if (G > 60) return 1;
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("g,count,hyp(k>=1,gcd=1),LK,DKM,LK_not_DKM,LK_not_DKM_not_LIT,outside_LIT_and_DKM\n");
  for (int g = 0; g <= G; g++) printf("%d,%llu,%llu,%llu,%llu,%llu,%llu,%llu\n", g, (unsigned long long)cnt[g], (unsigned long long)hyp[g],
     (unsigned long long)lk[g], (unsigned long long)dkm[g], (unsigned long long)lkonly[g], (unsigned long long)lkonly_nolit[g], (unsigned long long)open_[g]);
  printf("step_failures=%llu LB_failures=%llu min(ell-LB)=%lld old_bound_better=%llu\n", (unsigned long long)stepfail, (unsigned long long)lbfail, (long long)minsl, (unsigned long long)lb0better);
  return 0;
}
