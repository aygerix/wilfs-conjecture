/* TOPBAND test (lead, 2026-10-20): for every numerical semigroup S of genus <= G with e >= 2, depth q = ceil(c/m) >= 2:
 *   x = |S n [(q-1)m, c)|, h = c - (q-1)m.  Is e*x >= h ?  Report failures by depth, min (e*x - h), and also D1 = e*|S n [0,(q-1)m)| - (q-1)m.
 * usage: ./topband G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot[64], fail[64]; static long long mn[64]; static char ex[64][200];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(u128 gm, int m, int e, int c){
  int q = (c + m - 1) / m; if (q < 2 || q > 63) return;
  int lo = (q - 1) * m, h = c - lo, x = 0;
  for (int z = lo; z < c; z++) if (!gapq(gm, z)) x++;
  long long d2 = (long long)e * x - h;
  tot[q]++; if (d2 < 0){ fail[q]++; }
  if (tot[q] == 1 || d2 < mn[q]){ mn[q] = d2; snprintf(ex[q], 200, "m=%d c=%d e=%d h=%d x=%d", m, c, e, h, x); }
}
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  if (F >= 1 && m >= 2) check(gm, m, e, F + 1);
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
  for (int q = 2; q < 64; q++) if (tot[q]) printf("q=%d: S %llu, e*x<h failures %llu, min e*x-h %lld at %s\n", q, (unsigned long long)tot[q], (unsigned long long)fail[q], mn[q], ex[q]);
}
