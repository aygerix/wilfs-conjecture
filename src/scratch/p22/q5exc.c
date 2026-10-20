/* Depth-four Lambda study (lead, 2026-10-20).  At q = 4 (3m < c <= 4m):
 *   W = (e - h + Lam + Z) + (m - e - R)      (DEC-ID; R = #{K = 1}, Z = sum (-K)^+)
 *   L2 := d(m - a0) - sum_v min(|U(v)|, 4 - lam(v)) <= Lam + Z   (PROVED; a0 = #Ap in [c, M], U(v) = {a : v - n_a in S})
 * Reports min over S of (Lam + Z) - (h - e), of L2 - (h - e), counts, and checks DEC-ID and L2 <= Lam + Z.  ./d4lam G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, low4, l2low, bad, lowR, l2rlow, byE[16];
static long long minLZ = 1LL << 60, minL2 = 1LL << 60, minL2m = 1LL << 60; static char exLZ[400], exL2[400];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static uint64_t nexc; static double minratio = 1e18; static long long minLx = 1LL << 60; static char rex[400];
static uint64_t k2cnt, k2bad, faceBad, relayFail, s5, pseudoOK, pseudoFail; static char kex[300];
static void check(int m, long long *w, long long *n, int d, int c) {
  int q = (c + m - 1) / m; if (q != 5) return;
  s5++;
  #define INAP(v) ((v) >= 0 && w[(v) % m] == (v))
  #define INS(v) ((v) >= 0 && w[(v) % m] <= (v))
  long long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  long long h = c - 4LL * m; int e = d + 1;
  long long Lam = 0, credit = 0, RB = 0;
  static long long Kv[128];
  for (int i = 0; i < m; i++) { long long x = w[i], lam = (M - x) / m, K = 5 - lam; int nu1 = 0, alld1 = 1, U = 0;
    for (int a = 0; a < d; a++) { int jj = 0; while (INS(x - (long long)(jj + 1) * n[a])) jj++;
      if (jj) { U++; long long dr = (M - (x - n[a])) / m - lam; K -= jj * dr; nu1 += jj; if (dr != 1) alld1 = 0; }
      if (!INAP(x + n[a])) Lam += (jj + 1) * lam; }
    Kv[i] = K;
    int isgen = 0; for (int a = 0; a < d; a++) if (x == n[a]) isgen = 1;
    if (x != 0 && !isgen && K <= 0) credit += 1 - K;
    if (K >= 3) k2bad++;
    if (K == 2) { k2cnt++; RB++;
      int ok = (lam == 0 && nu1 == 3 && alld1);
      for (int a = 0; a < d; a++) if (INS(x - n[a]) && !(n[a] >= m + h && n[a] < 2 * m)) ok = 0;
      if (!ok) { k2bad++; snprintf(kex, 300, "m=%d c=%d v=%lld lam=%lld nu=%d", m, c, x, lam, nu1); } } }
  /* faces of K=2 values: v - n_a for a in U(v) must have K = 0 and co-level 1 */
  for (int i = 0; i < m; i++) if (Kv[i] == 2) for (int a = 0; a < d; a++) { long long y = w[i] - n[a];
    if (INS(y)) { if (!INAP(y) || Kv[y % m] != 0 || (M - y) / m != 1) faceBad++; } }
  if (RB > credit + Lam) relayFail++;
  { /* distinct faces */ static char isface[128]; memset(isface, 0, sizeof isface); long long p5 = 0;
    for (int i = 0; i < m; i++) if (Kv[i] == 2) for (int a = 0; a < d; a++) { long long y = w[i] - n[a]; if (INS(y) && !isface[y % m]) { isface[y % m] = 1; p5++; } }
    if (RB > p5) { nexc++; double r = (double)Lam / (RB - p5);
      if (r < minratio || Lam - (RB - p5) < minLx) { if (r < minratio) minratio = r; if (Lam - (RB - p5) < minLx) minLx = Lam - (RB - p5);
        int pp = snprintf(rex, 400, "m=%d c=%d e=%d beta=%lld p5=%lld Lam=%lld gens=", m, c, e, RB, p5, Lam); for (int a = 0; a < d && pp < 380; a++) pp += snprintf(rex + pp, 400 - pp, "%lld,", n[a]);
        printf("EXC %s\n", rex); } } }
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
  printf("genus<=%d: %llu S at q=5 (e>=3); K=2 values %llu; classification violations %llu (%s); face violations %llu; GEN-EH relay (R_B <= credits + Lam) failures %llu\n",
    G, (unsigned long long)s5, (unsigned long long)k2cnt, (unsigned long long)k2bad, kex, (unsigned long long)faceBad, (unsigned long long)relayFail);
  printf("S with beta > p5: %llu; min Lam/(beta-p5) = %.2f; min Lam-(beta-p5) = %lld\n", (unsigned long long)nexc, minratio, minLx);
  return 0;
}
