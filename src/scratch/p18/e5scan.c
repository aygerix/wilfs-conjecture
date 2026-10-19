/* CHAIN-H3 for e = 5 at larger m (lead, 2026-10-19), derived from e4scan.c.
 * Exhaustive over S = <m, n1..n4> with m < n1 < .. < n4 < K*m, gcd = 1, all four minimal (e = 5),
 * for m in [mlo, mhi].  Apery set by Dijkstra mod m; B_chain by walking chains; height = max least factorization length.
 * Reports CHAIN failures (B_chain < need) split by height, and min ratio among height >= 3, by depth class.
 * gcc -O3 -std=gnu11 e4scan.c -o e4scan ; ./e4scan mlo mhi K */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int m; static int64_t w[512];
static void apery(int *g, int k) {   /* Dijkstra on residues, O(m^2) simple version */
  int done[512]; for (int i = 0; i < m; i++) { w[i] = INT64_MAX; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++) { int u = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] != INT64_MAX && (u < 0 || w[i] < w[u])) u = i;
    if (u < 0) break; done[u] = 1;
    for (int j = 0; j < k; j++) { int v = (int)((u + g[j]) % m); if (w[u] + g[j] < w[v]) w[v] = w[u] + g[j]; } }
}
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
int main(int argc, char **argv) {
  int mlo = atoi(argv[1]), mhi = atoi(argv[2]), K = atoi(argv[3]);
  uint64_t tot = 0, f2 = 0, f3 = 0, n3 = 0; double min3[3] = {1e9, 1e9, 1e9}; char ex3[3][200] = {"", "", ""};
  for (m = mlo; m <= mhi; m++) {
    for (int a = m + 1; a < K * m; a++) for (int b = a + 1; b < K * m; b++) for (int c = b + 1; c < K * m; c++) for (int dd = c + 1; dd < K * m; dd++) {
      if (gcd(gcd(m, a), gcd(gcd(b, c), dd)) != 1) continue;
      int g[4] = {a, b, c, dd}; apery(g, 4);
      int bad = 0; for (int i = 0; i < m; i++) if (w[i] == INT64_MAX) bad = 1; if (bad) continue;
      /* minimality: each generator must be its own Apery element and not a sum of two Apery elements */
      int ok = 1;
      for (int j = 0; j < 4 && ok; j++) { int r = g[j] % m; if (w[r] != g[j]) { ok = 0; break; }
        for (int i = 1; i < m && ok; i++) { int r2 = (r - i + m) % m; if (r2 && w[i] + w[r2] == g[j]) ok = 0; } }
      if (!ok) continue;
      int64_t M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
      int64_t cc = M - m + 1; int q = (int)((cc + m - 1) / m), cls = q <= 3 ? 0 : (q == 4 ? 1 : 2);
      int64_t Bc = 0;
      for (int j = 0; j < 4; j++) for (int i = 0; i < m; i++) { int64_t t = w[i];
        for (;;) { int64_t t2 = t + g[j]; if (t2 > M) break; if (w[t2 % m] != t2) break; t = t2; } Bc += M - t; }
      int64_t need = (int64_t)3 * m * (m - 1) / 2;   /* (d-1) m(m-1)/2 with d = 4 */
      /* height */
      int ord[512]; for (int i = 0; i < m; i++) ord[i] = i;
      for (int i = 1; i < m; i++) { int v = ord[i], jj = i - 1; while (jj >= 0 && w[ord[jj]] > w[v]) { ord[jj + 1] = ord[jj]; jj--; } ord[jj + 1] = v; }
      int ml[512]; ml[0] = 0; int H = 0;
      for (int t = 1; t < m; t++) { int i = ord[t], best = 1 << 20;
        for (int j = 0; j < 4; j++) { int64_t y = w[i] - g[j]; if (y >= 0 && w[y % m] == y) { int v = 1 + ml[y % m]; if (v < best) best = v; } }
        ml[i] = best; if (best > H) H = best; }
      tot++;
      double r = (double)Bc / (double)need;
      if (H >= 3) { n3++; if (r < min3[cls]) { min3[cls] = r; snprintf(ex3[cls], 200, "m=%d gens=%d,%d,%d,%d c=%lld q=%d H=%d", m, a, b, c, dd, (long long)cc, q, H); } }
      if (Bc < need) { if (H >= 3) { f3++; printf("H3FAIL m=%d gens=%d,%d,%d,%d c=%lld q=%d H=%d ratio=%.4f\n", m, a, b, c, dd, (long long)cc, q, H, r); } else f2++; }
    }
    fprintf(stderr, "m=%d done tot=%llu\n", m, (unsigned long long)tot);
  }
  printf("e=5 semigroups m in [%d,%d], gens < %dm: %llu; height>=3: %llu; CHAIN failures height<=2: %llu, height>=3: %llu\n", mlo, mhi, K, (unsigned long long)tot, (unsigned long long)n3, (unsigned long long)f2, (unsigned long long)f3);
  for (int k = 0; k < 3; k++) printf("  min ratio height>=3, %s: %.4f at %s\n", k == 0 ? "q<=3" : (k == 1 ? "q=4" : "q>=5"), min3[k], ex3[k]);
  return 0;
}
