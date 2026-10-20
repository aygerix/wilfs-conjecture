/* Coverage of Corollary LAYER3-W at every depth q >= 4 (lead, 2026-10-20):
 * Wilf holds if  G + 3*D4 <= (e-1)*L,  G = #gaps in [3m, c), D4 = #{r : Kunz x_r >= 4}, L = |S n [3m, c)|.
 * Also verifies W >= Q3 + (e-1)L - G - 3*D4 (exact derivation: W = Q3 + (e-1)L - G - 3 D4 identically? printed check).
 * Per depth: count, covered, uncovered with 3e < m.  gcc -O3 -std=gnu11 l3w.c -o l3w */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G_;
static uint64_t cnt[64], cov[64], unc3[64], idfail; static int nshow;
static inline int inS(u128 g, int F, int x) { return x >= 0 && (x > F || !((g >> x) & 1)); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  int c = F + 1;
  if (m >= 2 && c > 3 * m) {
    int q = (c + m - 1) / m;
    int lv[128]; for (int r = 0; r < m; r++) { int x = r; while (!inS(gm, F, x)) x += m; lv[r] = x / m; }
    int64_t s[4] = {0,0,0,0}; for (int j = 0; j < 4; j++) for (int r = 0; r < m; r++) s[j] += lv[r] <= j;
    int64_t Q3 = (int64_t)e * (s[0] + s[1] + s[2]) - 3 * s[3];
    int64_t Gp = 0, L = 0, D4 = 0; for (int x = 3 * m; x < c; x++) { if (inS(gm, F, x)) L++; else Gp++; }
    for (int r = 0; r < m; r++) D4 += lv[r] >= 4;
    int64_t ell = 0; for (int x = 0; x < c; x++) ell += inS(gm, F, x);
    int64_t W = (int64_t)e * ell - c;
    if (W != Q3 + (int64_t)(e - 1) * L - Gp - 3 * D4) { idfail++; if (nshow++ < 5) fprintf(stderr, "IDFAIL g=%d m=%d c=%d e=%d\n", g, m, c, e); }
    if (q < 64) { cnt[q]++; if (Gp + 3 * D4 <= (int64_t)(e - 1) * L) cov[q]++; else if (3 * e < m) { unc3[q]++; if (nshow++ < 40) { fprintf(stderr, "UNC q=%d g=%d m=%d c=%d e=%d G=%lld D4=%lld L=%lld W=%lld gens=", q, g, m, c, e, (long long)Gp, (long long)D4, (long long)L, (long long)W); for (int b = 0; b < e; b++) fprintf(stderr, "%d,", gens[b]); fprintf(stderr, "\n"); } } }
  }
  if (g == G_) return;
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
      for (int a = m; a <= y / 2 && !dec; a++) if (a != n && inS(gm2, n, a) && (y - a) != n && inS(gm2, n, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, n, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G_ = atoi(argv[1]); if (G_ > 60) return 1;
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("identity W = Q3 + (e-1)L - G - 3 D4 failures: %llu\n", (unsigned long long)idfail);
  for (int q = 4; q < 64; q++) if (cnt[q]) printf("depth %d: S %llu covered %llu uncovered-with-3e<m %llu\n", q, (unsigned long long)cnt[q], (unsigned long long)cov[q], (unsigned long long)unc3[q]);
  return 0;
}
