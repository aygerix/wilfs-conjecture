/* GBW'' (lead, 2026-10-20): for all N in [0, c]:  e*|S n [0,N)| >= sum_{z in S n [N, N+m)} floor(z/m).
 * Kunz form: sum_{i in R(N)} k_i <= (1-1/e) sum_{i in R(N)} lambda_i, R(N) = residues present in the window, lambda_i = floor(z_i/m).
 * N = c: Wilf. N = Jm: BANDWILF.  Reports failures by e and the min slack for N not in mZ.
 * usage: ./gbw3 G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, inst, f[8]; static long long mn = 1LL<<40; static int shown; static char ex[300];
static double mr = 1e9; static char exr[300];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(u128 gm, int m, int *gens, int e, int c){
  tot++; int pre = 0; int ei = e < 7 ? e : 7;
  for (int N = 0; N <= c; N++){ if (N > 0 && !gapq(gm, N - 1)) pre++; long long rhs = 0;
    for (int z = N; z < N + m; z++) if (!gapq(gm, z)) rhs += z / m;
    inst++; long long d = (long long)e * pre - rhs;
    if (d < 0){ f[ei]++; if (shown < 10){ shown++; printf("GBW''FAIL N=%d m=%d c=%d e=%d pre=%d rhs=%lld gens:", N, m, c, e, pre, rhs); for (int t = 0; t < e; t++) printf(" %d", gens[t]); printf("\n"); } }
    if (N % m && N != c){ if (d < mn){ mn = d; int o = snprintf(ex, 300, "d=%lld N=%d m=%d c=%d e=%d gens:", d, N, m, c, e); for (int t = 0; t < e && o < 280; t++) o += snprintf(ex + o, 300 - o, " %d", gens[t]); }
      if (rhs > 0){ double r = (double)e * pre / rhs; if (r < mr){ mr = r; int o = snprintf(exr, 300, "ratio=%.4f N=%d m=%d c=%d e=%d gens:", r, N, m, c, e); for (int t = 0; t < e && o < 280; t++) o += snprintf(exr + o, 300 - o, " %d", gens[t]); } } } }
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
  printf("G<=%d: S %llu, (S,N) %llu\n  min slack (N not in mZ, N<c): %s\n  min ratio: %s\n", G, (unsigned long long)tot, (unsigned long long)inst, ex, exr);
  for (int e = 2; e < 8; e++) printf("  e=%d%s: fails %llu\n", e, e == 7 ? "+" : "", (unsigned long long)f[e]);
}
