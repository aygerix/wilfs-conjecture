/* Scaling test of CORE1 (E + r >= 0) on collision-free h-regular S with n = 2 (left generators m, g1, g1 + D):
 * dense lattice packings of the triangle Delta_h(2) could make r = m - s small while E ~ E0 ~ -s (Bacher Thm 3.3).
 * For h in [HLO,HHI], m in [s, MF*s], c in ((h-1)m, (h+X)m], g1 with h*g1 >= c, D >= 1 with h*(g1+D) < c+m:
 *   CF  <=> the s residues of t*g1 + j*D (0 <= j <= t <= h) are distinct mod m;
 *   c is the conductor <=> (c-1) mod m is not the residue of an element of degree < h.
 * Then k = sum_{deg<h} ceil((c - v)/m), r = m - s, E = 3k - q s + rho, W = (3+r)k - c, CORE1 = E + r.
 * gcc -O2 -o cfn2 cfn2.c ; ./cfn2 HLO HHI MF X */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
int main(int argc, char **argv) {
  int HLO = atoi(argv[1]), HHI = atoi(argv[2]); double MF = atof(argv[3]); int XX = atoi(argv[4]);
  static int seen[200000]; int stamp = 0; memset(seen, 0, sizeof(seen));
  ll tot = 0, fails = 0, wf = 0;
  for (int h = HLO; h <= HHI; h++) {
    int s = (h + 1) * (h + 2) / 2; ll best = 1LL << 60; int bm = 0, bc = 0, bg = 0, bD = 0; ll bE = 0, br = 0, cnt = 0;
    double bestden = 0;
    for (int m = s; m <= (int)(MF * s); m++) {
      for (int D = 1; D * h < m; D++) {
        /* CF depends on (g1 mod m, D): precheck over residues g1r */
        for (int g1r = 1; g1r < m; g1r++) {
          stamp++; int ok = 1;
          for (int t = 0; t <= h && ok; t++) for (int j = 0; j <= t; j++) {
            int v = (int)(((ll)t * g1r + (ll)j * D) % m);
            if (seen[v] == stamp) { ok = 0; break; } seen[v] = stamp;
          }
          if (!ok) continue;
          /* realize: g1 = g1r + a m > m, window: c <= h g1, h (g1 + D) < c + m, c > (h-1)m, c <= (h+XX)m */
          for (ll g1 = g1r + m; g1 * h <= (ll)(h + XX) * m + m; g1 += m) {
            ll clo = h * (g1 + D) - m + 1, chi = h * g1;
            if (clo < (ll)(h - 1) * m + 1) clo = (ll)(h - 1) * m + 1;
            for (ll c = clo; c <= chi; c++) {
              /* conductor check */
              int res = (int)((c - 1) % m), bad = 0;
              for (int t = 0; t < h && !bad; t++) for (int j = 0; j <= t; j++) if ((int)(((ll)t * g1 + (ll)j * D) % m) == res) { bad = 1; break; }
              if (bad) continue;
              ll q = (c + m - 1) / m, rho = q * m - c, k = 0;
              for (int t = 0; t < h; t++) for (int j = 0; j <= t; j++) { ll v = t * g1 + (ll)j * D; k += (c - v + m - 1) / m; }
              ll r = m - s, E = 3 * k - q * s + rho, W = (3 + r) * k - c, C1 = E + r;
              tot++; cnt++;
              if (W < 0) { wf++; printf("WILF FAIL h=%d m=%d c=%lld g=%lld,%lld\n", h, m, c, g1, g1 + D); }
              if (C1 < 0) { fails++; if (fails <= 20) printf("CORE1 FAIL h=%d m=%d c=%lld gens=%d,%lld,%lld r=%lld E=%lld W=%lld\n", h, m, c, m, g1, g1 + D, r, E, W); }
              if (C1 < best) { best = C1; bm = m; bc = (int)c; bg = (int)g1; bD = D; bE = E; br = r; }
              if ((double)s / m > bestden) bestden = (double)s / m;
            }
          }
        }
      }
    }
    printf("h=%d s=%d: %lld CF S; max density s/m %.3f; min CORE1 %lld at <%d,%d,%d>_%d (r=%lld, E=%lld)\n", h, s, cnt, bestden, best, bm, bg, bg + bD, bc, br, bE);
    fflush(stdout);
  }
  printf("total %lld, CORE1 fails %lld, Wilf fails %lld\n", tot, fails, wf);
  return 0;
}
