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
static void check(int m, long long *w, long long *n, int d, int c) {
  int q = (c + m - 1) / m; if (q != 4) return;
  tot++;
  #define INAP(v) ((v) >= 0 && w[(v) % m] == (v))
  #define INS(v) ((v) >= 0 && w[(v) % m] <= (v))
  long long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  long long rho = 4LL * m - c, h = m - rho; int e = d + 1;
  long long Lam = 0, Z = 0, R = 0, a0 = 0, sumU = 0, g = 0;
  for (int i = 0; i < m; i++) { long long x = w[i], lam = (M - x) / m, K = 4 - lam; int U = 0; g += x / m;
    if (lam == 0) a0++;
    for (int a = 0; a < d; a++) { int j = 0; while (INS(x - (long long)(j + 1) * n[a])) j++;
      if (j) { U++; K -= j * ((M - (x - n[a])) / m - lam); }
      if (!INAP(x + n[a])) Lam += (j + 1) * lam; }
    if (K < 0) Z -= K; if (K == 1) R++;
    long long cap = 4 - lam; sumU += U < cap ? U : cap; }
  long long W = (long long)e * (c - g) - c;
  if (W != (e - h + Lam + Z) + (m - e - R)) bad++;
  long long L2 = (long long)d * (m - a0) - sumU;
  if (L2 > Lam + Z) bad++;
  long long lz = Lam + Z - (h - e), l2 = L2 - (h - e);
  if (lz < 0) { low4++; if (R > 0) lowR++; }
  if (l2 < 0) { l2low++; if (l2 + (m - e - R) < 0) { l2rlow++; } byE[e < 15 ? e : 15]++;
    if (l2low <= 40) { printf("L2FAIL e=%d m=%d c=%d h=%lld L2-(h-e)=%lld a0=%lld R=%lld m-e-R=%lld W=%lld gens=", e, m, c, h, l2, a0, R, m - e - R, W); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf("\n"); } }
  if (lz < minLZ) { minLZ = lz; int pp = snprintf(exLZ, 400, "m=%d c=%d e=%d h=%lld Lam=%lld Z=%lld R=%lld W=%lld gens=", m, c, e, h, Lam, Z, R, W); for (int a = 0; a < d && pp < 380; a++) pp += snprintf(exLZ + pp, 400 - pp, "%lld,", n[a]); }
  if (l2 < minL2) { minL2 = l2; int pp = snprintf(exL2, 400, "m=%d c=%d e=%d h=%lld L2=%lld a0=%lld Lam+Z=%lld W=%lld gens=", m, c, e, h, L2, a0, Lam + Z, W); for (int a = 0; a < d && pp < 380; a++) pp += snprintf(exL2 + pp, 400 - pp, "%lld,", n[a]); }
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
  printf("genus<=%d, q=4, e>=3: %llu S; identity/L2 failures %llu\n", G, (unsigned long long)tot, (unsigned long long)bad);
  printf("Lam+Z < h-e in %llu S (with R>0: %llu); min (Lam+Z)-(h-e) = %lld at %s\n", (unsigned long long)low4, (unsigned long long)lowR, minLZ, exLZ);
  printf("L2+(m-e-R) < h-e in %llu S; L2 failures by e:", (unsigned long long)l2rlow); for (int k = 3; k < 16; k++) printf(" e%d:%llu", k, (unsigned long long)byE[k]); printf("\n");
  printf("L2 < h-e in %llu S; min L2-(h-e) = %lld at %s\n", (unsigned long long)l2low, minL2, exL2);
  return 0;
}
