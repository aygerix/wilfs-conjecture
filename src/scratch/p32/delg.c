/* CORE1 = E + r on Delgado-type truncations T = <mu, gamma, gamma+1> u [p mu, inf) (lead, 2026-10-20).
 * Apery set of S = <mu, gamma, gamma+1>; c = p*mu must be the conductor of T (c - 1 not in S); then
 *   ell = |S n [0,c)|, d = |S n [c, c+mu)|, r = mu - d, E = 3 ell - p d (q = p, rho = 0), CORE1 = E + r.
 * Reports min CORE1 among E < 0 per p, and the most negative E/r.  gcc -O3 -o delg delg.c ; ./delg PMAX MUMAX */
#include <stdio.h>
#include <stdlib.h>
typedef long long ll;
int main(int argc, char **argv) {
  int PMAX = atoi(argv[1]), MUMAX = atoi(argv[2]);
  static ll w[4096]; static int done[4096];
  ll tot = 0, neg = 0;
  for (int p = 3; p <= PMAX; p++) {
    ll best = 1LL << 60; int bm = 0, bg = 0; ll bE = 0, br = 0, minE = 0; int em = 0, eg = 0; ll er = 0;
    for (int mu = 3; mu <= MUMAX; mu++) for (int g = mu + 1; g < 2 * mu - 1; g++) {
      for (int r = 0; r < mu; r++) { w[r] = 1LL << 60; done[r] = 0; } w[0] = 0;
      int gs[2] = {g, g + 1};
      for (;;) {
        int r = -1; for (int x = 0; x < mu; x++) if (!done[x] && w[x] < (1LL << 60) && (r < 0 || w[x] < w[r])) r = x;
        if (r < 0) break; done[r] = 1;
        for (int i = 0; i < 2; i++) { ll v = w[r] + gs[i]; int s = v % mu; if (v < w[s]) w[s] = v; }
      }
      ll c = (ll)p * mu;
      if (w[(c - 1) % mu] <= c - 1) continue; /* c-1 in S: conductor of T below c */
      ll ell = 0, d = 0;
      for (int r = 0; r < mu; r++) {
        if (w[r] < c) ell += (c - 1 - w[r]) / mu + 1;
        ll x = c + ((r - c % mu) % mu + mu) % mu; /* element of [c, c+mu) congruent to r */
        if (x >= w[r]) d++;
      }
      ll rr = mu - d, E = 3 * ell - (ll)p * d;
      tot++;
      if (E < 0) { neg++; if (E + rr < best) { best = E + rr; bm = mu; bg = g; bE = E; br = rr; } }
      if (E < minE) { minE = E; em = mu; eg = g; er = rr; }
    }
    if (best < (1LL << 60)) printf("p=%d: min CORE1 among E<0: %lld (mu=%d gamma=%d E=%lld r=%lld); most negative E %lld (mu=%d gamma=%d r=%lld)\n", p, best, bm, bg, bE, br, minE, em, eg, er);
    else printf("p=%d: no E<0 (most negative E %lld)\n", p, minE);
    fflush(stdout);
  }
  printf("total %lld truncations, %lld with E < 0\n", tot, neg);
  return 0;
}
