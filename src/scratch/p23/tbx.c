/* TOPBAND by x (lead, 2026-10-20): min over S (genus <= G, q >= 2) of e*x - h, and of e*(x-1)+1 - h... grouped by x = |S n [(q-1)m,c)|.
 * usage: ./tbx G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static long long mn[64], mn2[64]; static uint64_t cnt[64]; static char ex[64][300];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(u128 gm, int m, int *gens, int e, int c){
  int q = (c + m - 1) / m; if (q < 2) return;
  int lo = (q - 1) * m, h = c - lo, x = 0;
  for (int i = 0; i < h; i++) if (!gapq(gm, lo + i)) x++;
  long long d = (long long)e * x - h, d2 = (long long)(e - 1) * x + 1 - h; /* d2: (e-1)x >= h-1 ? */
  if (!cnt[x] || d < mn[x]){ mn[x] = d; int o = snprintf(ex[x], 300, "m=%d c=%d q=%d h=%d e=%d gens:", m, c, q, h, e);
    for (int a = 0; a < e && o < 280; a++) o += snprintf(ex[x] + o, 300 - o, " %d", gens[a]); }
  if (!cnt[x] || d2 < mn2[x]) mn2[x] = d2; cnt[x]++;
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
  for (int x = 1; x < 64; x++) if (cnt[x]) printf("x=%d: S %llu, min e*x-h %lld (%s), min (e-1)x+1-h %lld\n", x, (unsigned long long)cnt[x], mn[x], ex[x], mn2[x]);
}
