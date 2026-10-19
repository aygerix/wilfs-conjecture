/* Semigroup tree to genus G.  For each S with K = floor(maxAp/m) >= 1:
 * rho = K*m - c, class of generator n (n != m) = band j with n in [jm-rho,(j+1)m-rho).
 * Intrinsic face F_j = {w in Ap : w is a sum of generators of class <= j}.
 * W_j = (d_j+1)*sum_{F_j} lambda - K|F_j| + rho_*(F_j), lambda = floor((M-w)/m),
 * rho_*(F) = #{w in F : w mod m >= m-rho}.  W_K = e*ell - c (Wilf slack).
 * Reports per K: min W_j, #(W_j < 0), #(W_j < W_{j-1}).  Run on fejer only. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
#define KM 40
static int G; static uint64_t cnt, perK[KM], neg[KM][KM], nonmono[KM][KM], neg0[KM][KM], negG[KM][KM]; static long minW[KM][KM], minW0[KM][KM], minWG[KM][KM]; static int shown[KM][KM], shown0[KM][KM];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt++;
  int c = F + 1;
  if (c > 0 && m > 1) {
    int isS[512]; for (int z = 0; z < 512; z++) isS[z] = !gapq(gm, z);
    int ap[128], M = 0; for (int r = 0; r < m; r++) { int w = r; while (!isS[w]) w += m; ap[r] = w; if (w > M) M = w; }
    int K = M / m, rho = K * m - c;   /* = (K+1)m-1-M */
    if (K < KM) {
      perK[K]++;
      int cls[128], d = 0, ng[128];
      for (int i = 0; i < e; i++) if (gens[i] != m) { ng[d] = gens[i]; cls[d] = (gens[i] + rho) / m; d++; }
      long prev = -1000000;
      for (int j = 1; j <= K; j++) {
        static char R[512]; memset(R, 0, M + 1); R[0] = 1; int dj = 0;
        for (int a = 0; a < d; a++) if (cls[a] <= j) { dj++; for (int z = ng[a]; z <= M; z++) if (R[z - ng[a]]) R[z] = 1; }
        long L = 0, Fc = 0, Rs = 0;
        for (int r = 0; r < m; r++) if (R[ap[r]]) { L += (M - ap[r]) / m; Fc++; Rs += (ap[r] % m) >= m - rho; }
        long W = (long)(dj + 1) * L - (long)K * Fc + Rs;
        if (W < minW[K][j]) minW[K][j] = W;
        if (W < 0) { neg[K][j]++; if (shown[K][j]++ < 3) { printf("NEG K=%d j=%d W=%ld m=%d c=%d gens=", K, j, W, m, c); for (int i = 0; i < e; i++) printf("%d,", gens[i]); printf("\n"); } }
        if (W < prev) nonmono[K][j]++;
        long W0 = W - Rs, WG = W0 + rho;
        if (W0 < minW0[K][j]) minW0[K][j] = W0; if (W0 < 0) { neg0[K][j]++; if (K == 4 && shown0[K][j]++ < 4) { printf("NEG0 K=%d j=%d W0=%ld m=%d c=%d gens=", K, j, W0, m, c); for (int i = 0; i < e; i++) printf("%d,", gens[i]); printf("\n"); } }
        if (WG < minWG[K][j]) minWG[K][j] = WG; if (WG < 0) negG[K][j]++;
        prev = W;
      }
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
  for (int K = 0; K < KM; K++) for (int j = 0; j < KM; j++) minW[K][j] = minW0[K][j] = minWG[K][j] = 1 << 30;
  visit(0, -1, 1, gens, 1, 0);
  printf("genus<=%d semigroups=%llu\n", G, (unsigned long long)cnt);
  for (int K = 1; K < KM && K <= 8; K++) if (perK[K]) {
    printf("K=%d count=%llu :", K, (unsigned long long)perK[K]);
    for (int j = 1; j <= K; j++) printf("\n   j%d rho*:[min %ld neg %llu nonmono %llu] none:[min %ld neg %llu] global:[min %ld neg %llu]", j, minW[K][j], (unsigned long long)neg[K][j], (unsigned long long)nonmono[K][j], minW0[K][j], (unsigned long long)neg0[K][j], minWG[K][j], (unsigned long long)negG[K][j]);
    printf("\n");
  }
  return 0;
}
