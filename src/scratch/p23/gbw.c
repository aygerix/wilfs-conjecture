/* GBW (lead, 2026-10-20): for every S (genus <= G) and every N in [1, c):
 *   GBW(N):  m*e*|S n [0,N)| >= N*|S n [N, N+m)|      (N = c is Wilf; N = Jm is BANDWILF(J), the Macaulay prefix sum)
 * Also the prefix Macaulay sums Phi_J = e*sum_{j<J} H_j - J*H_J for J = 1..q-1, and individual slacks M_J.
 * usage: ./gbw G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, instN, fN, fNm, fPhi, fM, instPhi; static int shown; static double minrat = 1e9; static char exs[300];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(u128 gm, int m, int *gens, int e, int c){
  tot++; int pre = 0;
  for (int N = 1; N < c; N++){ if (!gapq(gm, N - 1)) pre++; int up = 0; for (int z = N; z < N + m; z++) if (!gapq(gm, z)) up++;
    instN++; long lhs = (long)m * e * pre, rhs = (long)N * up;
    if (lhs < rhs){ fN++; if (N % m == 0) fNm++; if (shown < 12){ shown++; printf("GBWFAIL N=%d m=%d c=%d e=%d pre=%d up=%d gens:", N, m, c, e, pre, up); for (int t = 0; t < e; t++) printf(" %d", gens[t]); printf("\n"); } }
    else { double r = (double)lhs / rhs; if (r < minrat && N % m){ minrat = r; int o = snprintf(exs, 300, "ratio %.4f N=%d m=%d c=%d e=%d gens:", r, N, m, c, e); for (int t = 0; t < e && o < 280; t++) o += snprintf(exs + o, 300 - o, " %d", gens[t]); } } }
  int q = (c + m - 1) / m; long H[64]; for (int j = 0; j <= q; j++){ H[j] = 0; for (int z = j * m; z < (j + 1) * m; z++) if (!gapq(gm, z)) H[j]++; }
  long S = 0; for (int J = 1; J <= q - 1; J++){ S += H[J - 1]; long phi = (long)e * S - (long)J * H[J]; instPhi++; if (phi < 0) fPhi++;
    long MJ = (long)(e - 1) * H[J - 1] - (long)J * (H[J] - H[J - 1]); if (MJ < 0) fM++; }
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
  printf("G<=%d: S %llu; GBW instances %llu, failures %llu (N in mZ: %llu); min ratio (N not in mZ) %s\n  Phi_J (BANDWILF) instances %llu failures %llu; single M_J < 0: %llu\n", G, (unsigned long long)tot,
    (unsigned long long)instN, (unsigned long long)fN, (unsigned long long)fNm, exs, (unsigned long long)instPhi, (unsigned long long)fPhi, (unsigned long long)fM);
}
