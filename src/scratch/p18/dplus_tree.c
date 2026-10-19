/* Chain deficit packing (lead, 2026-10-19), exhaustive over the semigroup tree (genus <= G).
 * Ap = Ap(S,m), M = max Ap, n_1..n_d minimal generators other than m, s_w = (M-w) mod m,
 * y_{w,a} = M - top_a(w) (top of the n_a-chain of Ap through w).
 *   Delta  = sum_{w,a} (s_w - y_{w,a})          CHAIN-WILF  <=>  Delta <= C(m,2)
 *   Delta+ = sum_{w,a} max(0, s_w - y_{w,a})    candidate PACK: Delta+ <= C(m,2)  (implies CHAIN-WILF; FALSE, m=5 <8,12>)
 *   PW = sum_w max(0, sum_a (s_w - y_{w,a}))     candidate PACK-W: PW <= C(m,2)
 *   PA = sum_a max(0, sum_w (s_w - y_{w,a}))     candidate PACK-A: PA <= C(m,2)  [= sum_a (C2 - B_a)^+]
 * (B_chain = d C(m,2) - Delta holds by definition.)
 * gcc -O3 -std=gnu11 dplus_tree.c -o dplus_tree ; ./dplus_tree G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G;
static uint64_t cnt[80], tq[3][64], fD[3][64], fP[3][64], fW[3][64], fA[3][64], idfail; static int nsh, nshw, nsha;
static double minP[3][64]; static int minP_set[3][64]; static char exP[3][64][200];
static double minW[3][64]; static int minW_set[3][64]; static char exW[3][64][200];
static uint64_t fW1[4][64], tq3[4][64]; static int nsh1;
static double laymax[4][8]; static char layex[4][8][200]; static int layset[4][8]; static uint64_t laypos[4][8];  /* max layer-sum/C2 over w!=0 by co-level (1..6, 7 = >=7), by q class */  /* PW0': some w != 0 with positive contribution; by q class 0:q<=2 1:q=3 2:q=4 3:q>=5 */
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt[g]++;
  if (F >= 1 && m >= 2 && e >= 3) {
    int w[128]; int64_t M = 0;
    for (int i = 0; i < m; i++) { int s = i; while (gapq(gm, s)) s += m; w[i] = s; if (s > M) M = s; }
    int d = e - 1, n[64], dd = 0;
    for (int j = 0; j < e; j++) if (gens[j] != m) n[dd++] = gens[j];
    int64_t c = F + 1, ell = c - g;
    int64_t D = 0, Dp = 0, Bc = 0, PA = 0, PW = 0, cw[128] = {0};
    int64_t lsum[8] = {0};
    for (int a = 0; a < d; a++) { int64_t da = 0;
      for (int i = 0; i < m; i++) {
        int64_t t = w[i];
        for (;;) { int64_t t2 = t + n[a]; if (t2 > M) break; if (w[t2 % m] != t2) break; t = t2; }
        int64_t y = M - t, s = (M - w[i]) % m, df = s - y;
        D += df; if (df > 0) Dp += df; Bc += y; da += df; cw[i] += df;
      }
      if (da > 0) PA += da; }
    for (int i = 0; i < m; i++) if (cw[i] > 0) PW += cw[i];
    for (int i = 1; i < m; i++) { int lam = (int)((M - w[i]) / m); if (lam > 7) lam = 7; lsum[lam] += cw[i]; }
    { int q0 = (int)((F + 1 + m - 1) / m), k4 = q0 <= 2 ? 0 : (q0 == 3 ? 1 : (q0 == 4 ? 2 : 3)); double C2d = (double)m * (m - 1) / 2;
      for (int L = 1; L < 8; L++) { double v = lsum[L] / C2d; if (lsum[L] > 0) laypos[k4][L]++;
        if (!layset[k4][L] || v > laymax[k4][L]) { layset[k4][L] = 1; laymax[k4][L] = v;
          int p = snprintf(layex[k4][L], 200, "m=%d c=%d e=%d gens=", m, F + 1, e); for (int a = 0; a < d && p < 180; a++) p += snprintf(layex[k4][L] + p, 200 - p, "%d,", n[a]); } } }
    { int q0 = (int)((F + 1 + m - 1) / m), k4 = q0 <= 2 ? 0 : (q0 == 3 ? 1 : (q0 == 4 ? 2 : 3)); tq3[k4][e]++;
      int bad = 0, ib = -1; int64_t cmax = 0; for (int i = 1; i < m; i++) if (cw[i] > 0) { bad = 1; if (cw[i] > cmax) { cmax = cw[i]; ib = i; } }
      if (bad) { fW1[k4][e]++; if (k4 >= 2 && nsh1 < 40) { nsh1++;
        printf("PW0FAIL g=%d m=%d c=%d q=%d e=%d w=%d s_w=%lld contrib=%lld cw0=%lld gens=", g, m, F + 1, q0, e, w[ib], (long long)((M - w[ib]) % m), (long long)cmax, (long long)cw[0]);
        for (int a = 0; a < d; a++) printf("%d,", n[a]); printf("\n"); } } }
    int64_t C2 = (int64_t)m * (m - 1) / 2;
    if (Bc != (int64_t)d * C2 - D) idfail++;
    (void)ell;
    int q = (int)((c + m - 1) / m), cls = q <= 3 ? 0 : (q == 4 ? 1 : 2);
    tq[cls][e]++;
    if (D > C2) fD[cls][e]++;
    if (PW > C2) { fW[cls][e]++; if (cls > 0 && nshw < 15) { nshw++; printf("PACKWFAIL g=%d m=%d c=%lld q=%d e=%d D=%lld PW=%lld C2=%lld gens=", g, m, (long long)c, q, e, (long long)D, (long long)PW, (long long)C2); for (int a = 0; a < d; a++) printf("%d,", n[a]); printf("\n"); } }
    if (PA > C2) { fA[cls][e]++; if (cls > 0 && nsha < 15) { nsha++; printf("PACKAFAIL g=%d m=%d c=%lld q=%d e=%d D=%lld PA=%lld C2=%lld gens=", g, m, (long long)c, q, e, (long long)D, (long long)PA, (long long)C2); for (int a = 0; a < d; a++) printf("%d,", n[a]); printf("\n"); } }
    if (Dp > C2) { fP[cls][e]++;
      if (cls > 0 && nsh < 0) { nsh++; printf("PACKFAIL g=%d m=%d c=%lld q=%d e=%d D=%lld D+=%lld C2=%lld gens=", g, m, (long long)c, q, e, (long long)D, (long long)Dp, (long long)C2);
        for (int a = 0; a < d; a++) printf("%d,", n[a]); printf("\n"); } }
    if (PW > 0) { double r = (double)C2 / (double)PW;
      if (!minW_set[cls][e] || r < minW[cls][e]) { minW[cls][e] = r; minW_set[cls][e] = 1;
        int p = snprintf(exW[cls][e], 200, "m=%d c=%lld D=%lld PW=%lld gens=", m, (long long)c, (long long)D, (long long)PW);
        for (int a = 0; a < d && p < 180; a++) p += snprintf(exW[cls][e] + p, 200 - p, "%d,", n[a]); } }
    if (Dp > 0) { double r = (double)C2 / (double)Dp;
      if (!minP_set[cls][e] || r < minP[cls][e]) { minP[cls][e] = r; minP_set[cls][e] = 1;
        int p = snprintf(exP[cls][e], 200, "m=%d c=%lld D=%lld D+=%lld gens=", m, (long long)c, (long long)D, (long long)Dp);
        for (int a = 0; a < d && p < 180; a++) p += snprintf(exP[cls][e] + p, 200 - p, "%d,", n[a]); } }
  }
  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int nn = gens[j]; if (nn <= F) continue;
    u128 gm2 = gm | ((u128)1 << nn);
    int e2 = 0, m2;
    if (nn == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else {
      m2 = m;
      for (int k = 0; k < e; k++) if (gens[k] != nn) ng[e2++] = gens[k];
      int y = nn + m, dec = 0;
      for (int a = m; a <= y / 2 && !dec; a++) if (a != nn && !gapq(gm2, a) && (y - a) != nn && !gapq(gm2, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, nn, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); if (G > 60) return 1;
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  uint64_t tot = 0; for (int g = 0; g <= G; g++) tot += cnt[g];
  printf("genus<=%d semigroups: %llu  identity failures: %llu\n", G, (unsigned long long)tot, (unsigned long long)idfail);
  for (int k = 0; k < 4; k++) for (int L = 1; L < 8; L++) if (layset[k][L]) printf("LAYER class %s lambda=%d%s: max sum/C2 = %.4f  (#S with positive sum: %llu) at %s\n", k == 0 ? "q<=2" : (k == 1 ? "q=3" : (k == 2 ? "q=4" : "q>=5")), L, L == 7 ? "+" : "", laymax[k][L], (unsigned long long)laypos[k][L], layex[k][L]);
  for (int k = 0; k < 4; k++) { printf("PW0' (w!=0) failures, class %s:", k == 0 ? "q<=2" : (k == 1 ? "q=3" : (k == 2 ? "q=4" : "q>=5")));
    for (int e = 3; e < 64; e++) if (tq3[k][e]) printf(" e%d:%llu/%llu", e, (unsigned long long)fW1[k][e], (unsigned long long)tq3[k][e]); printf("\n"); }
  for (int k = 0; k < 3; k++) {
    printf("class %s: (e: total / CHAIN fails / PACK fails / PACK-W fails / PACK-A fails)\n", k == 0 ? "q<=3" : (k == 1 ? "q=4" : "q>=5"));
    for (int e = 3; e < 64; e++) if (tq[k][e]) printf("  e%d: %llu / %llu / %llu / %llu / %llu  min C2/D+ = %.4f at %s\n", e, (unsigned long long)tq[k][e],
      (unsigned long long)fD[k][e], (unsigned long long)fP[k][e], (unsigned long long)fW[k][e], (unsigned long long)fA[k][e], minP_set[k][e] ? minP[k][e] : -1.0, minP_set[k][e] ? exP[k][e] : "-");
    for (int e = 3; e < 64; e++) if (minW_set[k][e]) printf("    PACK-W e%d min C2/PW = %.4f at %s\n", e, minW[k][e], exW[k][e]);
  }
  return 0;
}
