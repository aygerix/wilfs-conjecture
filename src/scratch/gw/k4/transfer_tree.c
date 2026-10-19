/* Uniform-in-K transfer test on semigroups (genus <= G).  K = floor(maxAp/m), rho = K*m - c,
 * A = generators n != m with n < 2m - rho, F = Ap ∩ <A> (intrinsic A-face), WA = (a+1)*sum_F lambda - K|F|,
 * W = e*ell - c, miss = m - |F|.  Reports per K: min (W - WA), min (W - WA - rho), #(WA < 0),
 * max (-WA)/miss over deficient faces, min (W - WA)/miss over miss > 0.  fejer only. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
#define KM 24
static int G; static uint64_t cnt, perK[KM], defK[KM], trfail[KM]; static long mintr[KM], mintr2[KM]; static double maxdef[KM], minben[KM];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt++;
  int c = F + 1;
  if (c > 0 && m > 1) {
    int isS[512]; for (int z = 0; z < 512; z++) isS[z] = !gapq(gm, z);
    int ap[128], M = 0; for (int r = 0; r < m; r++) { int w = r; while (!isS[w]) w += m; ap[r] = w; if (w > M) M = w; }
    int K = M / m, rho = K * m - c;
    if (K < KM) {
      perK[K]++;
      static char R[512]; memset(R, 0, M + 1); R[0] = 1; int a = 0;
      for (int i = 0; i < e; i++) { int n = gens[i]; if (n == m || n >= 2 * m - rho) continue; a++; for (int z = n; z <= M; z++) if (R[z - n]) R[z] = 1; }
      long L = 0, Fc = 0; for (int r = 0; r < m; r++) if (R[ap[r]]) { L += (M - ap[r]) / m; Fc++; }
      long WA = (long)(a + 1) * L - (long)K * Fc;
      int ell = 0; for (int z = 0; z < c; z++) ell += isS[z];
      long W = (long)e * ell - c, miss = m - Fc;
      if (W - WA < mintr[K]) mintr[K] = W - WA;
      if (W - WA - rho < mintr2[K]) mintr2[K] = W - WA - rho;
      if (W < WA) { trfail[K]++; if (trfail[K] < 3) { printf("TRFAIL K=%d W=%ld WA=%ld m=%d c=%d gens=", K, W, WA, m, c); for (int i = 0; i < e; i++) printf("%d,", gens[i]); printf("\n"); } }
      if (WA < 0) { defK[K]++; double r = (double)(-WA) / (miss > 0 ? miss : 1); if (r > maxdef[K]) maxdef[K] = r; }
      if (miss > 0) { double b = (double)(W - WA) / miss; if (b < minben[K]) minben[K] = b; }
    }
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
  for (int k = 0; k < KM; k++) { mintr[k] = mintr2[k] = 1 << 30; minben[k] = 1e9; }
  visit(0, -1, 1, gens, 1, 0);
  printf("genus<=%d semigroups=%llu\n", G, (unsigned long long)cnt);
  for (int K = 1; K < KM; K++) if (perK[K]) printf("K=%d n=%llu  min(W-WA)=%ld  min(W-WA-rho)=%ld  W<WA:%llu  WA<0:%llu  max(-WA/miss)=%.3f  min((W-WA)/miss)=%.3f\n",
    K, (unsigned long long)perK[K], mintr[K], mintr2[K], (unsigned long long)trfail[K], (unsigned long long)defK[K], maxdef[K], minben[K]);
  return 0;
}
