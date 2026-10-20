/* Depth-four Lambda study (lead, 2026-10-20).  At q = 4 (3m < c <= 4m):
 *   W = (e - h + Lam + Z) + (m - e - R)      (DEC-ID; R = #{K = 1}, Z = sum (-K)^+)
 *   L2 := d(m - a0) - sum_v min(|U(v)|, 4 - lam(v)) <= Lam + Z   (PROVED; a0 = #Ap in [c, M], U(v) = {a : v - n_a in S})
 * Reports min over S of (Lam + Z) - (h - e), of L2 - (h - e), counts, and checks DEC-ID and L2 <= Lam + Z.  ./d4lam G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, low4, l2low, bad, lowR, l2rlow, byE[16];
static long long minLZ = 1LL << 60, minL2 = 1LL << 60, minL2m = 1LL << 60; static char exLZ[400], exL2[400];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static long long best[40][4]; static char bex[40][4][300];
static void check(int m, long long *w, long long *n, int d, int c) {
  int q = (c + m - 1) / m; if (q < 2 || q >= 40) return;
  tot++;
  long long M = 0, ell = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  for (int i = 0; i < m; i++) ell += (M - w[i]) / m;
  int e = d + 1; long long slack = (long long)e * (ell - q) - (long long)(q - 1) * (m - e);
  if (slack < 0) bad++;
  if (m == e) return;
  int cls = 3 * e >= m ? 0 : (4 * e >= m ? 1 : (6 * e >= m ? 2 : 3));  /* 0: 3e>=m, 1: m/4<=e<m/3, 2: m/6<=e<m/4, 3: e<m/6 */
  if (best[q][cls] == 0 || slack * 1000 / (m - e) < best[q][cls] - 1) {
    best[q][cls] = slack * 1000 / (m - e) + 1;
    int pp = snprintf(bex[q][cls], 300, "slack=%lld m=%d e=%d c=%d ell=%lld gens=", slack, m, e, c, ell);
    for (int a = 0; a < d && pp < 280; a++) pp += snprintf(bex[q][cls] + pp, 300 - pp, "%lld,", n[a]); }
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
  printf("genus<=%d: %llu S with q>=2, e>=3; GEN-EH failures %llu\n", G, (unsigned long long)tot, (unsigned long long)bad);
  for (int q = 2; q < 40; q++) for (int k = 0; k < 4; k++) if (best[q][k]) printf("q=%d cls=%d min slack/(m-e)=%.3f %s\n", q, k, (best[q][k] - 1) / 1000.0, bex[q][k]);
  return 0;
}
