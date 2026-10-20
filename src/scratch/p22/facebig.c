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
static uint64_t nS, bad1, bad2, bad3, bad4, nexc, nbig, bigfail; static char ex[300];
static void check(int m, long long *w, long long *n, int d, int c) {
  int q = (c + m - 1) / m; if (q != 4) return;
  nS++;
  #define INAP(v) ((v) >= 0 && w[(v) % m] == (v))
  #define INS(v) ((v) >= 0 && w[(v) % m] <= (v))
  long long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long long h = c - 3LL * m, rho = m - h; int e = d + 1;
  long long W = (long long)e * (c - g) - c;
  static long long K[128], nuS[128]; static int crit[128], isF[128], ncrit[128];
  long long R = 0, RA = 0;
  for (int i = 0; i < m; i++){ long long x = w[i], lam = (M - x) / m, k = 4 - lam, ns = 0; int allA = 1;
    for (int a = 0; a < d; a++){ int jj = 0; while (INS(x - (long long)(jj + 1) * n[a])) jj++;
      if (jj){ k -= jj * ((M - (x - n[a])) / m - lam); ns += jj; if (n[a] - m >= h) allA = 0; } }
    K[i] = k; nuS[i] = ns; if (k == 1) R++;
    crit[i] = (k == 1 && lam == 0 && ns == 3 && allA); if (crit[i]) RA++; isF[i] = 0; ncrit[i] = 0; }
  /* faces */
  long long nF = 0; double load[128];
  for (int i = 0; i < m; i++) load[i] = 0;
  for (int i = 0; i < m; i++) if (crit[i]){ int fi[8], nf = 0;
    for (int a = 0; a < d; a++){ long long y = w[i] - n[a]; if (INS(y)){ int r = (int)(y % m), dup = 0; for (int t = 0; t < nf; t++) if (fi[t] == r) dup = 1; if (!dup) fi[nf++] = r; } }
    for (int t = 0; t < nf; t++){ load[fi[t]] += 1.0 / nf; if (!isF[fi[t]]){ isF[fi[t]] = 1; nF++; }
      long long y = w[fi[t]]; if (K[fi[t]] != -1 || (M - y) / m != 1) bad1++; } }
  if (R - RA > rho) bad2++;
  long long sumtau = 0; double worst = 1e9;
  for (int i = 0; i < m; i++) if (isF[i]){ int tau = 0; for (int a = 0; a < d; a++) if (!INAP(w[i] + n[a])) tau++; sumtau += tau;
    double sl = 1 + tau - load[i]; if (sl < worst) worst = sl; }
  if (W < nF + sumtau - RA) bad3++;          /* W >= sum_F (1 + tau) - R_A */
  if (RA > nF) nexc++;
  int big = 0; for (int a = 0; a < d; a++) if (n[a] >= 2 * m) big++;
  if (3 * big >= d - 1){ nbig++; if (worst < 0) bigfail++; }
  if (worst < 0 && 3 * big >= d - 1 && bigfail < 3){ snprintf(ex, 300, "m=%d c=%d d=%d big=%d", m, c, d, big); }
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
  printf("genus<=%d q=4: %llu S; face K!=-1 or colevel!=1: %llu; R_out>rho: %llu; W < sum_F(1+tau)-R_A: %llu; R_A>|F|: %llu; FACE-BIG class: %llu, per-face condition failures in class: %llu %s\n",
    G, (unsigned long long)nS, (unsigned long long)bad1, (unsigned long long)bad2, (unsigned long long)bad3, (unsigned long long)nexc, (unsigned long long)nbig, (unsigned long long)bigfail, ex);
  return 0;
}
