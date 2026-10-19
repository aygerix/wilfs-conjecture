/* Window-Wilf on the tree of numerical semigroups (genus <= G).
 * P_i:  #(gaps < i*m)  <=  (e-1) * #(S cap [c - i*m, c))     for all i >= 1  (i*m >= c is Wilf).
 * Gaps as a 128-bit mask (F < 128).  Children: remove a minimal generator n > F; new generator candidate only n+m.
 * gcc -O3 -std=gnu11 win_tree.c -o win_tree */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G;
static uint64_t cnt[80], fail[80], wilffail, tight1[80], tightmid[80];
static int64_t minslack[80];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static inline int pc(u128 x) { return __builtin_popcountll((uint64_t)x) + __builtin_popcountll((uint64_t)(x >> 64)); }
static inline u128 below(int k) { return k >= 128 ? ~(u128)0 : (((u128)1 << k) - 1); }   /* bits 0..k-1 */
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt[g]++;
  int c = F + 1;
  if (c > 0) {
    int q = (c + m - 1) / m; int64_t best = INT64_MAX; int t1 = 0, tm = 0;
    for (int i = 1; i <= q; i++) {
      int N = i * m; int lo = c - N; if (lo < 0) lo = 0;
      int Gb = pc(gm & below(N < c ? N : c));                     /* gaps < N */
      int gaps_win = pc(gm & below(c) & ~below(lo));               /* gaps in [lo, c) */
      int Lt = (c - lo) - gaps_win;
      int64_t sl = (int64_t)(e - 1) * Lt - Gb;
      if (sl < best) best = sl;
      if (sl == 0 && i == 1) t1 = 1;
      if (sl == 0 && i > 1 && i < q) tm = 1;
      if (sl < 0) { if (i == q) wilffail++; fail[g]++;
        if (fail[g] <= 3) { fprintf(stderr, "FAIL g=%d i=%d m=%d c=%d e=%d gens:", g, i, m, c, e); for (int j = 0; j < e; j++) fprintf(stderr, " %d", gens[j]); fprintf(stderr, "\n"); }
        break; }
    }
    if (best < minslack[g]) minslack[g] = best;
    tight1[g] += t1; tightmid[g] += tm;
  }
  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int n = gens[j]; if (n <= F) continue;
    u128 gm2 = gm | ((u128)1 << n);
    int e2 = 0, m2;
    if (n == m) {                                   /* ordinary semigroup {0, m, m+1, ...} -> {0, m+1, ...} */
      m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k;
    } else {
      m2 = m;
      for (int k = 0; k < e; k++) if (gens[k] != n) ng[e2++] = gens[k];
      int y = n + m, dec = 0;                         /* is n+m decomposable in S' = S \ {n}? */
      for (int a = m; a <= y / 2 && !dec; a++) if (a != n && !gapq(gm2, a) && (y - a) != n && !gapq(gm2, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, n, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); if (G > 60) return 1;
  for (int g = 0; g <= G; g++) minslack[g] = INT64_MAX;
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("g,count,fail,wilf_fail,tight_at_i1,tight_strictly_inside,min_slack\n");
  for (int g = 0; g <= G; g++) printf("%d,%llu,%llu,%llu,%llu,%llu,%lld\n", g, (unsigned long long)cnt[g], (unsigned long long)fail[g], g == G ? (unsigned long long)wilffail : 0ULL, (unsigned long long)tight1[g], (unsigned long long)tightmid[g], (long long)minslack[g]);
  return 0;
}
