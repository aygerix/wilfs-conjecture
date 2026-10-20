/* GTB (lead, 2026-10-20): Kunz-level growth bounds on residue prefixes.
 * k_i = Kunz coordinate (w_i = k_i m + i). n_l(L) = #{i in [0,L) : k_i <= l}.
 *  GTB:  n_l(L) <= (e-1) n_{l-1}(L) + 1      for all 1 <= l <= q, 1 <= L <= m   (l = q, L = h is TB2)
 *  TCMK: l (n_l(L) - n_{l-1}(L)) <= (e-1) n_{l-1}(L)   (Macaulay-type, expected to fail)
 * usage: ./gtb G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, fG, fT, fGq; static int shown, shownT;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(u128 gm, int m, int *gens, int e, int c){
  tot++; int k[128]; int q = 0;
  for (int i = 0; i < m; i++){ int w = i; while (gapq(gm, w)) w += m; k[i] = w / m; if (k[i] > q) q = k[i]; }
  for (int l = 1; l <= q; l++){ int a = 0, b = 0; /* a = n_l(L), b = n_{l-1}(L) */
    for (int L = 1; L <= m; L++){ int i = L - 1; if (k[i] <= l) a++; if (k[i] <= l - 1) b++;
      if ((long)a > (long)(e - 1) * b + 1){ fG++; if (l == q) fGq++; if (shown < 10){ shown++; printf("GTBFAIL l=%d q=%d L=%d m=%d c=%d e=%d n_l=%d n_l-1=%d gens:", l, q, L, m, c, e, a, b); for (int t = 0; t < e; t++) printf(" %d", gens[t]); printf("\n"); } }
      if ((long)l * (a - b) > (long)(e - 1) * b){ fT++; if (shownT < 3){ shownT++; printf("TCMKFAIL l=%d L=%d m=%d e=%d gens:", l, L, m, e); for (int t = 0; t < e; t++) printf(" %d", gens[t]); printf("\n"); } } } }
}
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  if (F >= 1 && m >= 2) check(gm, m, gens, e, F + 1);
  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int nn = gens[j]; if (nn <= F) continue;
    u128 gm2 = gm | ((u128)1 << nn); int e2 = 0, m2;
    if (nn == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else { m2 = m; for (int k = 0; k < e; k++) if (gens[k] != nn) ng[e2++] = gens[k];
      int y = nn + m, dec = 0; for (int a = m; a <= y / 2 && !dec; a++) if (a != nn && !gapq(gm2, a) && (y - a) != nn && !gapq(gm2, y - a)) dec = 1;
      if (!dec) ng[e2++] = y; }
    visit(gm2, nn, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); int gens[1] = {1}; visit(0, -1, 1, gens, 1, 0);
  printf("G<=%d: S %llu; GTB fails %llu (at l=q: %llu); TCMK fails %llu\n", G, (unsigned long long)tot, (unsigned long long)fG, (unsigned long long)fGq, (unsigned long long)fT);
}
