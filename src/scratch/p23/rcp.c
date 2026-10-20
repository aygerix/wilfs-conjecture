/* RC' (lead, 2026-10-20): for every S (genus <= G), level l >= 1 and L in [1,m] such that every residue in [L,m) has
 * Kunz level <= l-1:  #{i < L : k_i = l} <= (e-2) #{i < L : k_i <= l-1} + 1.   (l = q, L = h is TB2.)
 * Also record tightness and the D_dec form: #{i < L : k_i = l, w_i decomposable} <= (e_low - 2) x + 1 where
 * e_low = e - #{generators at level l with residue < L}.
 * usage: ./rcp G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, inst, f1, f2, instlq; static int shown;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(u128 gm, int m, int *gens, int e, int c){
  tot++; int k[128], isg[128] = {0}; int q = 0;
  for (int i = 0; i < m; i++){ int w = i; while (gapq(gm, w)) w += m; k[i] = w / m; if (k[i] > q) q = k[i]; }
  for (int t = 0; t < e; t++) if (gens[t] != m) isg[gens[t] % m] = 1;
  for (int l = 1; l <= q; l++){
    int mx = 0; /* smallest L with all residues >= L at level <= l-1 */
    for (int i = m - 1; i >= 0; i--) if (k[i] > l - 1){ mx = i + 1; break; }
    for (int L = mx; L <= m; L++){ if (L < 1) continue; int Q = 0, x = 0, Qg = 0;
      for (int i = 0; i < L; i++){ if (k[i] == l){ Q++; if (isg[i]) Qg++; } else if (k[i] < l) x++; }
      inst++; if (l < q) instlq++;
      if ((long)Q > (long)(e - 2) * x + 1){ f1++; if (shown < 10){ shown++; printf("RCFAIL l=%d q=%d L=%d m=%d c=%d e=%d Q=%d x=%d gens:", l, q, L, m, c, e, Q, x); for (int t = 0; t < e; t++) printf(" %d", gens[t]); printf("\n"); } }
      if ((long)(Q - Qg) > (long)(e - Qg - 2) * x + 1) f2++; } }
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
  printf("G<=%d: S %llu; instances %llu (l<q: %llu); RC' fails %llu; D_dec form fails %llu\n", G, (unsigned long long)tot, (unsigned long long)inst, (unsigned long long)instlq, (unsigned long long)f1, (unsigned long long)f2);
}
