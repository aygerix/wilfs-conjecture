/* List S with K = floor(maxAp/m) = 4 and Wilf slack W <= WMAX (genus <= G).  fejer only. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G, WMAX, KK; static uint64_t cnt, hist[64];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt++;
  int c = F + 1;
  if (c > 0 && m > 1) {
    int isS[512]; for (int z = 0; z < 512; z++) isS[z] = !gapq(gm, z);
    int ap[128], M = 0; for (int r = 0; r < m; r++) { int w = r; while (!isS[w]) w += m; ap[r] = w; if (w > M) M = w; }
    int K = M / m;
    if (K == KK) {
      int ell = 0; for (int z = 0; z < c; z++) ell += isS[z];
      int W = e * ell - c; if (W < 64) hist[W]++;
      if (W <= WMAX && m >= 6) { printf("W=%d m=%d c=%d rho=%d e=%d g=%d gens=", W, m, c, K*m-c, e, g); for (int i = 0; i < e; i++) printf("%d,", gens[i]); printf("\n"); }
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
  G = atoi(argv[1]); WMAX = atoi(argv[2]); KK = atoi(argv[3]); int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("hist W:"); for (int w = 0; w < 20; w++) printf(" %d:%llu", w, (unsigned long long)hist[w]); printf("\n");
  return 0;
}
