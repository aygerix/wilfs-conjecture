/* a = 0 at depth four for P18 (lead, 2026-10-20): enumerate every B subset [lo, m) with lo = floor(m/3)+1 (all subsets
 * whose elements exceed m/3), compute the semigroup S = <m, m+B> (Apery set by shortest paths), keep depth four with
 * h = c - 3m <= min B (a = 0) and 3h > m.  Report count, min W, and how many have 3e < m (Eliahou's criterion fails).
 * usage: ./a0mid mlo mhi */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
  int mlo = atoi(argv[1]), mhi = atoi(argv[2]);
  for (int m = mlo; m <= mhi; m++) {
    int lo = m / 3 + 1, nb = m - lo; long long cnt = 0, small_e = 0, minW = 1LL << 60; int exB[64], exn = 0, exh = 0;
    long long cnt_half = 0;
    for (long long mask = 1; mask < (1LL << nb); mask++) {
      int B[64], k = 0, g = 0;
      for (int i = 0; i < nb; i++) if (mask >> i & 1) B[k++] = lo + i;
      for (int i = 0; i < k; i++) { int x = B[i], y = m; while (y) { int t = x % y; x = y; y = t; } g = (i == 0) ? x : g; }
      int gg = m; for (int i = 0; i < k; i++) { int x = B[i], y = gg; while (y) { int t = x % y; x = y; y = t; } gg = x; }
      if (gg != 1) continue;
      /* Apery set: w[r] minimal element = r mod m; Bellman-Ford style relaxation (Dijkstra on residues) */
      long long w[200]; for (int r = 0; r < m; r++) w[r] = 1LL << 50; w[0] = 0;
      int done[200]; memset(done, 0, sizeof done);
      for (int it = 0; it < m; it++) {
        int u = -1; for (int r = 0; r < m; r++) if (!done[r] && (u < 0 || w[r] < w[u])) u = r;
        done[u] = 1;
        for (int i = 0; i < k; i++) { long long v = w[u] + m + B[i]; int rr = v % m; if (v < w[rr]) w[rr] = v; }
      }
      long long mx = 0, gsum = 0; for (int r = 0; r < m; r++) { if (w[r] > mx) mx = w[r]; gsum += w[r] / m; }
      long long c = mx - m + 1; if (!(3LL * m < c && c <= 4LL * m)) continue;
      int h = c - 3 * m; if (B[0] < h) continue; if (3 * h <= m) continue;
      int e = k + 1; long long W = e * (c - gsum) - c;
      cnt++; if (2 * h >= m) cnt_half++;
      if (3 * e < m) small_e++;
      if (W < minW) { minW = W; exn = k; exh = h; memcpy(exB, B, sizeof(int) * k); }
    }
    printf("m=%d  a=0 & 3h>m depth-four S: %lld (h>=m/2: %lld)  3e<m: %lld  minW %lld", m, cnt, cnt_half, small_e, cnt ? minW : 0);
    if (cnt) { printf(" at h=%d B=", exh); for (int i = 0; i < exn; i++) printf("%d,", exB[i]); }
    printf("\n"); fflush(stdout);
  }
}
