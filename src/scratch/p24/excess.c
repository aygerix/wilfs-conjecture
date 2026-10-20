/* Order vs Kunz level on Ap(S,m) (lead, 2026-10-20).  L(w) = max factorization length, k(w) = floor(w/m), eps = k - L.
 * Checks: (i) h(n) = #{w in Ap : L(w) = n} satisfies condensed Macaulay n h(n) <= (e-1) sum_{j<n} h(j) (theory: O-sequence);
 * (ii) LEN: (e-1) ell >= sum L(w); records Sigma eps, LENslack = (e-1)ell - sum L, W = LENslack - Sigma eps;
 * (iii) EXC: Sigma eps <= (1-1/e)(c - (D+1)m) + MacSlack, MacSlack = (1-1/e)(D+1)m - sum L  (this is Wilf; we record which side carries it);
 * (iv) eps monotone along Ap poset (w <=_S w' => eps(w) <= eps(w')).
 * usage: ./excess G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, fMac, fLEN, mono, wneg; static double maxr = 0; static char exr[300];
static long long minLS = 1LL<<40;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(u128 gm, int m, int *gens, int e, int c){
  tot++; int top = c + m; if (top > 127) return;
  int L[260]; L[0] = 0;
  for (int s = 1; s < top; s++){ L[s] = -1; if (gapq(gm, s)) continue; for (int a = 0; a < e; a++){ int t = s - gens[a]; if (t >= 0 && L[t] >= 0 && L[t] + 1 > L[s]) L[s] = L[t] + 1; } }
  int w[128], h[64] = {0}, D = 0; long sumL = 0, sumK = 0;
  for (int i = 0; i < m; i++){ int x = i; while (gapq(gm, x)) x += m; w[i] = x; h[L[x]]++; if (L[x] > D) D = L[x]; sumL += L[x]; sumK += x / m; }
  long A = 0; for (int n = 1; n <= D; n++){ A += h[n - 1]; if ((long)n * h[n] > (long)(e - 1) * A) fMac++; }
  long ell = c - sumK; long LS = (long)(e - 1) * ell - sumL; long se = sumK - sumL; long W = (long)e * ell - c;
  if (LS < 0) fLEN++; if (LS < minLS) minLS = LS; if (W != LS - se) wneg++;
  if (LS > 0){ double r = (double)se / LS; if (r > maxr){ maxr = r; int o = snprintf(exr, 300, "Sigma_eps/LENslack=%.4f eps=%ld LS=%ld W=%ld m=%d c=%d e=%d D=%d gens:", r, se, LS, W, m, c, e, D); for (int a = 0; a < e && o < 280; a++) o += snprintf(exr + o, 300 - o, " %d", gens[a]); } }
  int ok = 1; for (int i = 1; i < m && ok; i++) for (int a = 0; a < e && ok; a++){ int y = w[i] + gens[a]; int j = y % m; if (w[j] == y && (y / m - L[y]) < (w[i] / m - L[w[i]])) ok = 0; }
  mono += ok;
}
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  if (F >= 1 && m >= 2) check(gm, m, gens, e, F + 1);
  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int nn = gens[j]; if (nn <= F) continue;
    u128 gm2 = gm | ((u128)1 << nn); int e2 = 0, m2;
    if (nn == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else { m2 = m; for (int k = 0; k < e; k++) if (gens[k] != nn) ng[e2++] = gens[k];
      int y = nn + m, dec = 0; for (int a = m; a <= y / 2 && !dec; a++) if (a != nn && !gapq(gm2, a) && (y - a) != nn && !gapq(gm2, y - a)) dec = 1;
      if (!dec) ng[e2++] = y; }
    visit(gm2, nn, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); int gens[1] = {1}; visit(0, -1, 1, gens, 1, 0);
  printf("G<=%d: S %llu; Macaulay(order) violations %llu; LEN violations %llu (min LENslack %lld); identity mismatches %llu; eps-monotone S %llu\n  max Sigma_eps/LENslack: %s\n", G,
    (unsigned long long)tot, (unsigned long long)fMac, (unsigned long long)fLEN, minLS, (unsigned long long)wneg, (unsigned long long)mono, exr);
}
