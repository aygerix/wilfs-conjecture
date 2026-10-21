/* f0ann (p38, 2026-10-21): family F0 = {S = <m, m+A> in Q5 : A = {mu} u B, B subset [c, m) \ mu*N, N subset B},
 * N = non-multiples of mu in [c, c+mu); c-1 not = 0 mod mu.  Then T = <m, A> = mu*N u [c, inf), c(T) = c,
 * U cap [0,c) = {0, mu, 2mu, 3mu} (c > 4mu), so P1 = e|U cap [0,c_T)| - c_T = 4(|B|+2) - c and 4mu lies in T \ U.
 * Annealing over B (fixed mu, c, m) minimizes |B| + PEN * (Q5 violations); reports min |B| among exact Q5 members
 * and flags P1 < 0.  Q5 check: Dijkstra for Ap(S, m); max factorization length <= 3 on every Apery element
 * (DP over Apery predecessors); max Apery element in [5m, 6m).  W(S) recomputed for every reported S.
 * usage: f0ann mu cmin cmax restarts steps seed   (m runs over [max(c+mu, 2c-2mu-6), min(3c, 2c+6mu)];
 * in F0 the window [m, m+c) minus 4 points lies in 3A', which forces c <= m/2 + mu + 2) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXM 1200
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int m, mu, c;
/* returns number of violations (0 = in Q5); fills W */
static long viol(const char *inB, long *Wout){
  static long w[MAXM]; static int hmx[MAXM], done[MAXM], ord[MAXM]; int A[MAXM], d = 0;
  A[d++] = mu; for (int x = c; x < m; x++) if (inB[x]) A[d++] = x;
  for (int i = 0; i < m; i++){ w[i] = 1L << 40; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){
    int u = -1; for (int x = 0; x < m; x++) if (!done[x] && (u < 0 || w[x] < w[u])) u = x;
    if (w[u] >= (1L << 40)) return 1000000; done[u] = 1; ord[it] = u;
    for (int i = 0; i < d; i++){ long v = w[u] + m + A[i]; int t = (int)(v % m); if (v < w[t]) w[t] = v; } }
  long bad = 0; hmx[0] = 0; long mx = 0;
  for (int it = 1; it < m; it++){ int x = ord[it]; int best = -1;
    for (int i = 0; i < d; i++){ int t = ((x - A[i]) % m + m) % m; if (w[t] == w[x] - m - A[i] && hmx[t] + 1 > best) best = hmx[t] + 1; }
    hmx[x] = best; if (best > 3) bad += best - 3; if (w[x] > mx) mx = w[x]; }
  if (mx < 5L * m) bad += (5L * m - mx + m - 1) / m * 3; if (mx >= 6L * m) bad += (mx - 6L * m) / m + 1;
  if (!bad){ long cc = mx - m + 1, g = 0; for (int x = 0; x < m; x++) g += w[x] / m; *Wout = (long)(d + 1) * (cc - g) - cc; }
  return bad; }
int main(int argc, char **argv){
  mu = atoi(argv[1]); int cmin = atoi(argv[2]), cmax = atoi(argv[3]), R = atoi(argv[4]), ST = atoi(argv[5]);
  rs ^= (unsigned long long)atoll(argv[6]) * 2654435761ULL; const long PEN = 4;
  for (c = cmin; c <= cmax; c++){ if ((c - 1) % mu == 0 || c <= 4 * mu) continue;
    int bestB = 1 << 30, bm = 0; long bW = 0; char bset[MAXM];
    int mlo = c + mu > 2 * c - 2 * mu - 6 ? c + mu : 2 * c - 2 * mu - 6, mhi = 3 * c < 2 * c + 6 * mu ? 3 * c : 2 * c + 6 * mu;
    for (m = mlo; m <= mhi && m < MAXM; m++){
      int cand[MAXM], nc = 0; for (int x = c + mu; x < m; x++) if (x % mu) cand[nc++] = x;
      for (int r = 0; r < R; r++){
        char in[MAXM] = {0}; int nb = 0; for (int x = c; x < c + mu && x < m; x++) if (x % mu){ in[x] = 1; nb++; }
        if (c + mu > m) break;
        for (int k = 0; k < nc; k++) if (rnd() % 3 == 0){ in[cand[k]] = 1; nb++; }
        long W, v = viol(in, &W); double cur = nb + PEN * v; double T = 2.0;
        for (int s = 0; s < ST && nc > 0; s++){
          int x = cand[rnd() % nc]; in[x] ^= 1; int nb2 = nb + (in[x] ? 1 : -1);
          int y = -1; if (rnd() % 2 && nc > 1){ y = cand[rnd() % nc]; if (y != x){ in[y] ^= 1; nb2 += in[y] ? 1 : -1; } else y = -1; }
          long W2, v2 = viol(in, &W2); double nw = nb2 + PEN * v2;
          if (nw <= cur || (double)(rnd() % 1000000) / 1e6 < __builtin_exp((cur - nw) / T)){ cur = nw; nb = nb2; v = v2; W = W2;
            if (v == 0 && nb < bestB){ bestB = nb; bm = m; bW = W; memcpy(bset, in, sizeof bset);
              int P1 = 4 * (nb + 2) - c; if (P1 < 0){ printf("P1<0 mu=%d c=%d m=%d e=%d P1=%d W=%ld A=<%d", mu, c, m, nb + 2, P1, W, mu); for (int z = c; z < m; z++) if (in[z]) printf(",%d", z); printf(">\n"); fflush(stdout); } } }
          else { in[x] ^= 1; if (y >= 0) in[y] ^= 1; }
          T *= 0.9995; if (T < 0.05) T = 0.05; } } }
    if (bestB < (1 << 30)){ printf("mu=%d c=%d minB=%d e=%d P1=%d (m=%d W=%ld) A=<%d", mu, c, bestB, bestB + 2, 4 * (bestB + 2) - c, bm, bW, mu);
      for (int z = c; z < bm; z++) if (bset[z]) printf(",%d", z); printf(">\n"); }
    else printf("mu=%d c=%d none\n", mu, c);
    fflush(stdout); }
  return 0; }
