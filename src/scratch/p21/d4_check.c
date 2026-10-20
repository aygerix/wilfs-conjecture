/* Independent lead check of codex P13 (depth four, 3m < c <= 4m), over the semigroup tree: ./d4_check G
 * Checks, for every S with q = 4 and e >= 3:
 *   K-ID   W = rho + Lambda - sum_v K(v),  K(v) = 4 - lambda(v) - L1(v)
 *   K(0) = 0, K(v) <= 1 for v != 0, MF => K <= -1, primitives K = 0
 *   K = 1 => UF and type BB(co-level 1) | BC | cubic co-level 0 with all pair divisors co-level 1 (A/B factors)
 *   short arc: critical and not pure-A cubic => s(v) < rho;  every critical => s(v) <= m-1-ceil(h/2)
 *   COUNT-PAY W >= Lambda + C_U - R_A, SHADOW-3 inequalities.
 * Reports how many S fail A-OVERLAP (R_A > Lambda + C_U) and the extreme ratios. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, bad[16]; static long long minslackB = 1LL << 60, maxRA = 0; static char exB[300], exRA[300];
static uint64_t aoverlap_fail, shadow_fail, arcfail, lamEfail; static long long minNlow = 1LL << 60; static char exN[300]; static uint64_t ehfail, ehcls, ehneg; static long long mineh = 1LL << 60; static char exEH[300];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static int cls(long long n, int m, int h) { if (n < m + h) return 0; if (n < 2 * m + h) return 1; if (n < 3 * m + h) return 2; return 3; } /* A,B,C,E */
static void check(int m, long long *w, long long *n, int d, int g, int c) {
  long long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  if (c <= 3 * m || c > 4 * m) return;
  int h = c - 3 * m, rho = m - h; tot++;
  /* index Apery by residue; membership test for Apery values */
  #define INAP(v) ((v) >= 0 && w[(v) % m] == (v))
  #define INS(v) ((v) >= 0 && w[(v) % m] <= (v))
  #define LAM(v) ((int)((M - (v)) / m))
  #define SS(v) ((int)((M - (v)) % m))
  /* factorization counts (capped at 2) by generator-ordered DP over Apery values in increasing order */
  int ord[256]; for (int i = 0; i < m; i++) ord[i] = i;
  for (int i = 1; i < m; i++) { int v = ord[i], j = i - 1; while (j >= 0 && w[ord[j]] > w[v]) { ord[j + 1] = ord[j]; j--; } ord[j + 1] = v; }
  static int cnt[256][256]; /* cnt[k][res]: #factorizations using generators 0..k-1 */
  for (int k = 0; k <= d; k++) for (int i = 0; i < m; i++) cnt[k][i] = 0;
  for (int k = 0; k <= d; k++) cnt[k][0] = 1;
  for (int t = 1; t < m; t++) { int i = ord[t]; long long v = w[i];
    for (int k = 1; k <= d; k++) { int x = cnt[k - 1][i]; long long u = v - n[k - 1]; if (INAP(u)) x += cnt[k][u % m]; cnt[k][i] = x > 2 ? 2 : x; } }
  long long Lam = 0, sumK = 0; static long long LamDir[256]; for (int a = 0; a < d; a++) LamDir[a] = 0; int R = 0, RA = 0, Rout = 0, FM = 0; long long Z = 0, CU = 0;
  static int Kv[256], dep[256][256];
  for (int i = 0; i < m; i++) { long long v = w[i]; int L1 = 0, J = 0, U = 0;
    for (int a = 0; a < d; a++) { int j = 0; while (INS(v - (long long)(j + 1) * n[a])) j++; dep[i][a] = j;
      if (j > 0) { L1 += j * (LAM(v - n[a]) - LAM(v)); J += j; U++; }
      long long t = v; while (INAP(t + n[a])) t += n[a]; Lam += LAM(t); LamDir[a] += LAM(t); }
    int K = 4 - LAM(v) - L1; Kv[i] = K; sumK += K;
    int mf = cnt[d][i] >= 2;
    if (v == 0 && K != 0) bad[1]++;
    if (v != 0 && K > 1) bad[2]++;
    if (mf) { FM++; if (K > -1) bad[3]++; int cu = LAM(v) + U - 4; CU += cu > 1 ? cu : 1; }
    if (K < 0) Z += -K;
    if (v != 0 && J == 1 && K != 0) bad[4]++;
    if (K == 1) { R++;
      if (mf) bad[5]++;
      /* type */
      int fa[8], nf = 0; for (int a = 0; a < d; a++) for (int j = 0; j < dep[i][a] && nf < 8; j++) fa[nf++] = a;
      int pureA = 0;
      if (J == 2) { int c1 = cls(n[fa[0]], m, h), c2 = cls(n[fa[1]], m, h); if (c1 > c2) { int tt = c1; c1 = c2; c2 = tt; }
        if (!((c1 == 1 && c2 == 1 && LAM(v) == 1) || (c1 == 1 && c2 == 2))) bad[6]++; }
      else if (J == 3) { int okc = LAM(v) == 0; pureA = 1;
        for (int x = 0; x < 3; x++) { int cc = cls(n[fa[x]], m, h); if (cc > 1) okc = 0; if (cc != 0) pureA = 0; long long p = v - n[fa[x]]; if (LAM(p) != 1) okc = 0; }
        if (!okc) bad[6]++; }
      else bad[6]++;
      if (pureA) RA++; else { Rout++; if (SS(v) >= rho) bad[7]++; }
      if (SS(v) > m - 1 - (h + 1) / 2) bad[8]++; } }
  long long ell = 0; for (int i = 0; i < m; i++) ell += LAM(w[i]);
  long long W = (long long)(d + 1) * ell - c;
  if (W != rho + Lam - sumK) bad[9]++;
  { int Nlow = 0; for (int i = 0; i < m; i++) if (Kv[i] <= 0 && SS(w[i]) <= m - 1 - (h + 1) / 2) Nlow++;
    if (W != Lam + Z + Nlow - h / 2) arcfail++;
    long long nl = (long long)Nlow - h / 2; if (nl < minNlow) { minNlow = nl; snprintf(exN, 300, "m=%d c=%d e=%d W=%lld Nlow=%d h=%d Lam=%lld Z=%lld", m, c, d + 1, W, Nlow, h, Lam, Z); }
    for (int a = 0; a < d; a++) if (cls(n[a], m, h) == 3 && LamDir[a] != ell - 4) lamEfail++;
    if (W < (d + 1) - h + Lam + Z) ehfail++;
    long long eh = W - ((d + 1) - h); if (eh < mineh) { mineh = eh; snprintf(exEH, 300, "m=%d c=%d e=%d W=%lld h=%d Lam=%lld Z=%lld", m, c, d + 1, W, h, Lam, Z); }
    if (d + 1 >= h) { ehcls++; if (W < 0) ehneg++; } }
  if (W != rho + Lam - R + Z) bad[10]++;
  if (Rout > rho) bad[11]++;
  if (W < Lam + CU - RA) bad[12]++;
  /* SHADOW-3: P_A pairs dividing critical pure-A cubics */
  static char inPA[256]; memset(inPA, 0, m); int pA = 0;
  for (int i = 0; i < m; i++) if (Kv[i] == 1) { long long v = w[i]; int J = 0, allA = 1; for (int a = 0; a < d; a++) { J += dep[i][a]; if (dep[i][a] && cls(n[a], m, h) != 0) allA = 0; }
      if (J == 3 && allA) for (int a = 0; a < d; a++) if (dep[i][a]) { long long p = v - n[a]; if (!inPA[p % m]) { inPA[p % m] = 1; pA++; if (Kv[p % m] != -1) bad[13]++; } } }
  int aA = 0; for (int a = 0; a < d; a++) if (cls(n[a], m, h) == 0) aA++;
  if (3LL * RA > (long long)(aA + 2) * pA) bad[14]++;
  if (FM + RA + pA > m - 1 - d) bad[15]++;
  if (W < Lam + CU + pA - RA) shadow_fail++;
  if (RA > Lam + CU) aoverlap_fail++;
  long long sl = Lam + CU - RA; if (sl < minslackB) { minslackB = sl; int p = snprintf(exB, 300, "m=%d c=%d e=%d W=%lld R_A=%d Lam=%lld C_U=%lld gens=", m, c, d + 1, W, RA, Lam, CU); for (int a = 0; a < d && p < 280; a++) p += snprintf(exB + p, 300 - p, "%lld,", n[a]); }
  if (RA > maxRA) { maxRA = RA; int p = snprintf(exRA, 300, "m=%d c=%d e=%d W=%lld R_A=%d Lam=%lld Z=%lld rho-Rout=%d gens=", m, c, d + 1, W, RA, Lam, Z, rho - Rout); for (int a = 0; a < d && p < 280; a++) p += snprintf(exRA + p, 300 - p, "%lld,", n[a]); }
}
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  if (F >= 1 && m >= 2 && e >= 3) {
    long long w[128]; for (int i = 0; i < m; i++) { int s = i; while (gapq(gm, s)) s += m; w[i] = s; }
    long long n[64]; int d = 0; for (int j = 0; j < e; j++) if (gens[j] != m) n[d++] = gens[j];
    check(m, w, n, d, g, F + 1);
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
static long long wbuf[4096];
static int apery_gens(int m, long long *gl, int k) { /* Dijkstra O(m^2) */
  static char done[4096]; for (int i = 0; i < m; i++) { wbuf[i] = -1; done[i] = 0; } wbuf[0] = 0;
  for (int it = 0; it < m; it++) { int u = -1; for (int i = 0; i < m; i++) if (!done[i] && wbuf[i] >= 0 && (u < 0 || wbuf[i] < wbuf[u])) u = i;
    if (u < 0) return 0; done[u] = 1; for (int j = 0; j < k; j++) { int v = (int)((u + gl[j]) % m); long long y = wbuf[u] + gl[j]; if (wbuf[v] < 0 || y < wbuf[v]) wbuf[v] = y; } }
  return 1; }
int main(int argc, char **argv) {
  if (argc > 1 && strcmp(argv[1], "-g") == 0) { char line[20000];
    while (fgets(line, sizeof line, stdin)) { long long gl[256]; int k = 0; char *p = line; long long x; int off;
      while (k < 256 && sscanf(p, "%lld%n", &x, &off) == 1) { gl[k++] = x; p += off; }
      if (k < 2) continue; int m = (int)gl[0]; if (m > 255) continue;
      if (!apery_gens(m, gl + 1, k - 1)) continue;
      long long M = 0; for (int i = 0; i < m; i++) if (wbuf[i] > M) M = wbuf[i];
      /* minimal generators other than m: Apery elements not sums of two nonzero Apery elements */
      long long n[256]; int d = 0;
      for (int i = 1; i < m; i++) { long long v = wbuf[i]; int dec = 0; for (int j = 1; j < m && !dec; j++) { long long u = wbuf[j]; if (u < v && wbuf[(int)((v - u) % m)] == v - u) dec = 1; } if (!dec) n[d++] = v; }
      for (int i = 1; i < d; i++) { long long v = n[i]; int j = i - 1; while (j >= 0 && n[j] > v) { n[j + 1] = n[j]; j--; } n[j + 1] = v; }
      long long g = 0; for (int i = 0; i < m; i++) g += wbuf[i] / m;
      if (d >= 2) check(m, wbuf, n, d, (int)g, (int)(M - m + 1)); }
  } else {
  G = atoi(argv[1]); int gens[1] = {1}; visit(0, -1, 1, gens, 1, 0); }
  const char *nm[16] = {"", "K(0)!=0", "K>1", "MF with K>-1", "primitive K!=0", "critical MF", "critical type", "short arc (non-A critical, s>=rho)", "critical s > m-1-ceil(h/2)", "K-ID", "W=rho+Lam-R+Z", "R_out>rho", "COUNT-PAY", "P_A pair K!=-1", "3R_A>(a+2)p_A", "F_M+R_A+p_A>D_dec"};
  printf("genus<=%d, depth four (3m<c<=4m), e>=3: %llu S\n", G, (unsigned long long)tot);
  for (int k = 1; k < 16; k++) printf("  check %-38s failures %llu\n", nm[k], (unsigned long long)bad[k]);
  printf("  SHADOW-3 (W >= Lam+C_U+p_A-R_A) failures %llu; A-OVERLAP (R_A<=Lam+C_U) fails on %llu S\n", (unsigned long long)shadow_fail, (unsigned long long)aoverlap_fail);
  printf("  ARC identity W = Lam+Z+N_low-floor(h/2) failures %llu; Lambda_E = ell-4 failures %llu\n  min (N_low - floor(h/2)) = %lld at %s\n", (unsigned long long)arcfail, (unsigned long long)lamEfail, minNlow, exN);
  printf("  E-H bound W >= e-h+Lam+Z failures %llu; S with e >= h: %llu (W<0: %llu); min W-(e-h) = %lld at %s\n", (unsigned long long)ehfail, (unsigned long long)ehcls, (unsigned long long)ehneg, mineh, exEH);
  printf("  min (Lam+C_U-R_A) = %lld at %s\n  max R_A = %lld at %s\n", minslackB, exB, maxRA, exRA);
  return 0;
}
