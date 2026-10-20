/* General-depth K-identity (lead, 2026-10-19): for every S (e >= 3) in the genus tree, q = ceil(c/m), rho = qm - c,
 *   K(v) = q - lambda(v) - L1(v),  W = rho + Lambda - sum_v K(v)   (K-ID, any depth)
 * Reports per depth q: max K, #S with some K >= 2, failures of W >= e - (c-(q-1)m) + Lambda + Z (true when K <= 1),
 * failures of W >= e - (c-(q-1)m) itself, MF values with K >= 0.  ./kq_check G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot[64], kid[64], k2[64], ehLZ[64], eh[64], mfpos[64]; static int maxK[64]; static uint64_t t1[64]; static char exT1[64][300]; static long long t1min[64]; static double genr[64]; static char exG[64][300]; static char exK[64][300], exEH[64][300];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(int m, long long *w, long long *n, int d, int c) {
  long long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  int q = (c + m - 1) / m, rho = q * m - c; if (q >= 64) return; tot[q]++;
  #define INAP(v) ((v) >= 0 && w[(v) % m] == (v))
  #define INS(v) ((v) >= 0 && w[(v) % m] <= (v))
  #define LAM(v) ((int)((M - (v)) / m))
  int ord[128]; for (int i = 0; i < m; i++) ord[i] = i;
  for (int i = 1; i < m; i++) { int v = ord[i], j = i - 1; while (j >= 0 && w[ord[j]] > w[v]) { ord[j + 1] = ord[j]; j--; } ord[j + 1] = v; }
  static int cnt[64][128];
  for (int k = 0; k <= d; k++) { for (int i = 0; i < m; i++) cnt[k][i] = 0; cnt[k][0] = 1; }
  for (int t = 1; t < m; t++) { int i = ord[t]; long long v = w[i];
    for (int k = 1; k <= d; k++) { int x = cnt[k - 1][i]; long long u = v - n[k - 1]; if (INAP(u)) x += cnt[k][u % m]; cnt[k][i] = x > 2 ? 2 : x; } }
  long long Lam = 0, sumK = 0, Z = 0, ell = 0; int mk = -1000, has2 = 0;
  for (int i = 0; i < m; i++) { long long v = w[i]; int L1 = 0; ell += LAM(v);
    for (int a = 0; a < d; a++) { int j = 0; while (INS(v - (long long)(j + 1) * n[a])) j++;
      if (j > 0) L1 += j * (LAM(v - n[a]) - LAM(v));
      long long t = v; while (INAP(t + n[a])) t += n[a]; Lam += LAM(t); }
    int K = q - LAM(v) - L1; sumK += K; if (K < 0) Z += -K; if (K > mk) mk = K; if (K >= 2) has2 = 1;
    if (cnt[d][i] >= 2 && K >= 0) mfpos[q]++; }
  long long W = (long long)(d + 1) * ell - c;
  if (W != rho + Lam - sumK) kid[q]++;
  if (has2) k2[q]++;
  long long bound = (d + 1) - (c - (long long)(q - 1) * m);
  if (W < bound + Lam + Z) ehLZ[q]++;
  if (W < bound) { eh[q]++; }
  long long sl = (m - (d + 1)) - sumK; /* T1 slack: m - e - sum K */
  if (sl < 0) { t1[q]++; }
  { static int np = 0; if (has2 && sl == 0 && np < 40 && 3 * (d + 1) <= 2 * m) { np++; printf("TIGHTK2 q=%d m=%d c=%d e=%d mk=%d gens=", q, m, c, d + 1, mk); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf("\n"); } }
  if (sl < t1min[q]) { t1min[q] = sl; int p = snprintf(exT1[q], 300, "m=%d c=%d e=%d W=%lld Lam=%lld sumK=%lld gens=", m, c, d + 1, W, Lam, sumK); for (int a = 0; a < d && p < 280; a++) p += snprintf(exT1[q] + p, 300 - p, "%lld,", n[a]); }
  if (has2) { double r = (double)(W - bound) / (double)(Lam > 0 ? Lam : 1); if (r < genr[q]) { genr[q] = r; int p = snprintf(exG[q], 300, "m=%d c=%d e=%d W=%lld Lam=%lld sumK=%lld gens=", m, c, d + 1, W, Lam, sumK); for (int a = 0; a < d && p < 280; a++) p += snprintf(exG[q] + p, 300 - p, "%lld,", n[a]); } }
  if (mk > maxK[q]) { maxK[q] = mk; int p = snprintf(exK[q], 300, "m=%d c=%d e=%d W=%lld gens=", m, c, d + 1, W); for (int a = 0; a < d && p < 280; a++) p += snprintf(exK[q] + p, 300 - p, "%lld,", n[a]); }
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
  G = atoi(argv[1]); for (int q = 0; q < 64; q++) { maxK[q] = -1000; t1min[q] = 1000000; genr[q] = 1e9; }
  int gens[1] = {1}; visit(0, -1, 1, gens, 1, 0);
  for (int q = 1; q < 64; q++) if (tot[q]) printf("q=%d: %llu S; K-ID fails %llu; max K %d (%s); S with K>=2: %llu; MF with K>=0: %llu; W < e-(c-(q-1)m)+Lam+Z: %llu; W < e-(c-(q-1)m): %llu\n",
    q, (unsigned long long)tot[q], (unsigned long long)kid[q], maxK[q], exK[q], (unsigned long long)k2[q], (unsigned long long)mfpos[q], (unsigned long long)ehLZ[q], (unsigned long long)eh[q]);
  for (int q = 1; q < 64; q++) if (tot[q]) printf("q=%d: T1 (sumK <= m-e) fails %llu; min slack %lld (%s); min (W-(e-h))/Lam among K>=2 S: %.4f (%s)\n", q, (unsigned long long)t1[q], t1min[q], exT1[q], genr[q], exG[q]);
  return 0;
}
