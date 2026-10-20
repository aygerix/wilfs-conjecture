/* Multiplier-keeping targets on Delgado-type truncations T = <mu, g, g+1> u [p mu, inf) (E338 family, E < 0 rich):
 *   E = 3 k - p d (rho = 0), r = mu - d, a = #{w in Ap : 0 < w < c}, W = E + r (k - p).
 *   DEF : E + 3a >= 0           (would give Wilf whenever r >= 3 = number of left generators)
 *   P1  : r >= 1  =>  E + (k - p) >= 0
 *   COREa: E + a r >= 0         (between CORE1 and Wilf)
 * Reports failures and minima over E < 0.  gcc -O3 -o delgdef delgdef.c ; ./delgdef PMAX MUMAX */
#include <stdio.h>
#include <stdlib.h>
typedef long long ll;
int main(int argc, char **argv) {
  int PMAX = atoi(argv[1]), MUMAX = atoi(argv[2]);
  static ll w[8192]; static int done[8192];
  ll tot = 0, neg = 0, fD = 0, fP = 0, fA = 0; double worstD = 1e9, worstP = 1e9;
  for (int p = 3; p <= PMAX; p++) {
    for (int mu = 3; mu <= MUMAX; mu++) for (int g = mu + 1; g < 2 * mu - 1; g++) {
      for (int r = 0; r < mu; r++) { w[r] = 1LL << 60; done[r] = 0; } w[0] = 0;
      int gs[2] = {g, g + 1};
      for (;;) {
        int r = -1; for (int x = 0; x < mu; x++) if (!done[x] && w[x] < (1LL << 60) && (r < 0 || w[x] < w[r])) r = x;
        if (r < 0) break; done[r] = 1;
        for (int i = 0; i < 2; i++) { ll v = w[r] + gs[i]; int s = v % mu; if (v < w[s]) w[s] = v; }
      }
      ll c = (ll)p * mu;
      if (w[(c - 1) % mu] <= c - 1) continue;
      if (g + 1 >= c) continue;
      ll k = 0, d = 0, a = 0;
      for (int r = 0; r < mu; r++) {
        if (w[r] < c) { k += (c - w[r] + mu - 1) / mu; d++; if (r) a++; }
        else if (w[r] < c + mu) d++;
      }
      ll r = mu - d, E = 3 * k - (ll)p * d, W = E + r * (k - p);
      tot++;
      if (W < 0) printf("WILF FAIL mu=%d g=%d p=%d\n", mu, g, p);
      if (E >= 0) continue;
      neg++;
      ll D = E + 3 * a, P = E + (k - p), A = E + a * r;
      if (D < 0) { fD++; if (fD <= 5) printf("DEF fail mu=%d g=%d p=%d E=%lld a=%lld r=%lld k-p=%lld\n", mu, g, p, E, a, r, k - p); }
      if (r >= 1 && P < 0) { fP++; if (fP <= 5) printf("P1 fail mu=%d g=%d p=%d E=%lld r=%lld k-p=%lld\n", mu, g, p, E, r, k - p); }
      if (A < 0) { fA++; if (fA <= 5) printf("COREa fail mu=%d g=%d p=%d E=%lld a=%lld r=%lld\n", mu, g, p, E, a, r); }
      double rd = (double)E / (3.0 * a), rp = (double)E / (double)(k - p);
      if (rd < worstD) worstD = rd; if (rp < worstP) worstP = rp;
    }
  }
  printf("total %lld truncations, %lld with E < 0; DEF fails %lld (min E/(3a) %.3f), P1 fails %lld (min E/(k-p) %.3f), COREa fails %lld\n", tot, neg, fD, worstD, fP, worstP, fA);
  return 0;
}
