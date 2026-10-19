/* For each S (genus <= G): K = floor(maxAp/m), Ntop = #{w in Ap : w >= K m}.  Tests Ntop <= e-1, and the
 * reduction GW <= P_{K-1} + (Ntop - d <= slack of P_{K-1}).  Also W of example family.  fejer only. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
#define KM 40
static int G; static uint64_t cnt, perK[KM], ntopfail[KM], pfail[KM]; static int maxexc[KM]; static int shown[KM];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt++;
  int c = F + 1;
  if (c > 0 && m > 1) {
    int isS[512]; for (int z = 0; z < 512; z++) isS[z] = !gapq(gm, z);
    int ap[128], M = 0; for (int r = 0; r < m; r++) { int w = r; while (!isS[w]) w += m; ap[r] = w; if (w > M) M = w; }
    int K = M / m, d = e - 1, Nt = 0; long A = 0, B = 0;
    for (int r = 0; r < m; r++) { if (ap[r] >= K * m) Nt++; int k = ap[r] / m, l = (M - ap[r]) / m; A += k < K - 1 ? k : K - 1; B += l < K - 1 ? l : K - 1; }
    if (K < KM) { perK[K]++;
      if (Nt > d) { ntopfail[K]++; if (Nt - d > maxexc[K]) maxexc[K] = Nt - d; if (shown[K]++ < 2) { printf("NTOP K=%d Nt=%d d=%d m=%d c=%d gens=", K, Nt, d, m, c); for (int i = 0; i < e; i++) printf("%d,", gens[i]); printf("\n"); } }
      if (A > (long)d * B) pfail[K]++; }
  }
  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int n = gens[j]; if (n <= F) continue;
    u128 gm2 = gm | ((u128)1 << n); int e2 = 0, m2;
    if (n == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else {
      m2 = m; for (int k = 0; k < e; k++) if (gens[k] != n) ng[e2++] = gens[k];
      int y = n + m, dec = 0;
      for (int a = m; a <= y / 2 && !dec; a++) if (a != n && !gapq(gm2, a) && (y - a) != n && !gapq(gm2, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, n, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("genus<=%d semigroups=%llu\n", G, (unsigned long long)cnt);
  for (int K = 1; K < KM; K++) if (perK[K]) printf("K=%d count=%llu Ntop>d: %llu (max excess %d)  P_{K-1} fails: %llu\n", K, (unsigned long long)perK[K], (unsigned long long)ntopfail[K], maxexc[K], (unsigned long long)pfail[K]);
  return 0;
}
