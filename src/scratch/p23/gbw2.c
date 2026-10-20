/* GBW' (lead, 2026-10-20): N = Jm + r (0 <= r < m), all N in [1, c]:
 *   e*|S n [0,N)| >= J*|S n [N,N+m)| + |S n [N, N+r)|     (N = c: Wilf;  r = 0: BANDWILF)
 * plus variant V2: e*|S n [0,N)| >= J*|S n [N,N+m)| + r*|S n [N,N+m)|/m  (= GBW), split by e.
 * usage: ./gbw2 G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, inst, f1[8], f2[8]; static long long mn1 = 1LL<<40; static int shown; static char ex[300];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(u128 gm, int m, int *gens, int e, int c){
  tot++; int pre = 0; int ei = e < 7 ? e : 7;
  for (int N = 1; N <= c; N++){ if (!gapq(gm, N - 1)) pre++; int J = N / m, r = N % m, up = 0, upr = 0;
    for (int z = N; z < N + m; z++) if (!gapq(gm, z)){ up++; if (z < N + r) upr++; }
    inst++; long long d1 = (long long)e * pre - (long long)J * up - upr;
    if (d1 < 0){ f1[ei]++; if (shown < 10){ shown++; printf("GBW'FAIL N=%d m=%d c=%d e=%d pre=%d up=%d upr=%d gens:", N, m, c, e, pre, up, upr); for (int t = 0; t < e; t++) printf(" %d", gens[t]); printf("\n"); } }
    if (d1 < mn1 && r){ mn1 = d1; int o = snprintf(ex, 300, "d=%lld N=%d m=%d c=%d e=%d gens:", d1, N, m, c, e); for (int t = 0; t < e && o < 280; t++) o += snprintf(ex + o, 300 - o, " %d", gens[t]); }
    if ((long long)m * e * pre < (long long)N * up) f2[ei]++; }
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
  printf("G<=%d: S %llu, (S,N) %llu; min GBW' slack with r>0: %s\n", G, (unsigned long long)tot, (unsigned long long)inst, ex);
  for (int e = 2; e < 8; e++) printf("  e=%d%s: GBW' fails %llu, GBW fails %llu\n", e, e == 7 ? "+" : "", (unsigned long long)f1[e], (unsigned long long)f2[e]);
}
