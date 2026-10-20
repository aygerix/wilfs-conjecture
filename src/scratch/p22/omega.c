/* OMEGA test (lead, 2026-10-20). T1 at every shift implies W >= e - h + Lambda + Omega, where
 * Omega = max_p S_p - S_{p*},  S_p = sum_{x in Ap, 0 < x mod m < p} J(x),  p* = (M mod m) + 1.
 * If B* := e - h + Lambda + Omega >= 0 for all S, then T1-ALL alone implies Wilf.  ./omega G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, bneg, low, lowcov; static long long bmin = 1LL << 60; static char ex[400];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(int m, long long *w, long long *n, int d, int c) {
  tot++;
  #define INAP(v) ((v) >= 0 && w[(v) % m] == (v))
  #define INS(v) ((v) >= 0 && w[(v) % m] <= (v))
  long long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  int q = (c + m - 1) / m; long long rho = (long long)q * m - c, h = m - rho;
  long long J[128], Lam = 0;
  for (int i = 0; i < m; i++) { long long x = w[i], s = 0;
    for (int a = 0; a < d; a++) { if (!INAP(x + n[a])) { int j = 0; while (INS(x - (long long)(j + 1) * n[a])) j++; s += j + 1; }
      long long t = x; while (INAP(t + n[a])) t += n[a]; Lam += (M - t) / m; }
    J[i] = s - (d + 1); }
  int ps = (int)(M % m) + 1; long long S = 0, Smax = 0, Sps = 0; /* S_1 = 0 */
  for (int p = 1; p <= m; p++) { if (p == ps) Sps = S; if (S > Smax) Smax = S; if (p < m) S += J[p]; }
  long long Om = Smax - Sps, B = (d + 1) - h + Lam + Om;
  if (rho + Lam < m - (d + 1)) { low++; if (B >= 0) lowcov++; }
  if (B < 0) bneg++;
  if (B < bmin) { bmin = B; int pp = snprintf(ex, 400, "m=%d c=%d e=%d h=%lld Lam=%lld Om=%lld gens=", m, c, d + 1, h, Lam, Om); for (int a = 0; a < d && pp < 380; a++) pp += snprintf(ex + pp, 400 - pp, "%lld,", n[a]); }
}
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  if (F >= 1 && m >= 2 && e >= 3) {
    long long w[128]; for (int i = 0; i < m; i++) { int s = i; while (gapq(gm, s)) s += m; w[i] = s; }
    long long n[64]; int d = 0; for (int j = 0; j < e; j++) if (gens[j] != m) n[d++] = gens[j];
    check(m, w, n, d, F + 1);
  }
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
  printf("genus<=%d: %llu S; B* = e-h+Lam+Omega < 0 in %llu S; min B* %lld (%s); LOW %llu, of which B*>=0: %llu\n", G, (unsigned long long)tot, (unsigned long long)bneg, bmin, ex, (unsigned long long)low, (unsigned long long)lowcov);
  return 0;
}
