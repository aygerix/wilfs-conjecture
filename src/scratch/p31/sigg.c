/* General-S form of SIG at depth four (lead, 2026-10-20).
 * LAYER3 proof: Q3 = e(s0+s1+s2) - 3 s3 >= sigT := k1*u2 + 2*Pu - 3|T_U| >= 0, where k1 = |G_1|, U2 = N_2 \ G_2,
 * Pu = #{multisets {x,y} in G_1, x + y < m}, T_U = ((G_1 + U2)_{<m}) \ (S_2 u (G_1 + G_2)_{<m}).
 * Depth four (3m < c <= 4m): W = Q3 + Q4, Q4 = (e-1) L3 - 4 d4.  Test SIG: Q4 + sigT >= 0 on the genus tree.
 * Also records min (Q3 - sigT) (must be >= 0) and min sigT/(-Q4) over Q4 < 0.
 * gcc -O3 -o sigg sigg.c ; ./sigg G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static long long nS, nD4, nneg, fail, shown; static long long minSig = 1LL << 60, minRest = 1LL << 60;
static double minRatio = 1e18; static int rgens[64], re, rm, rc;
static inline int inS(u128 g, int F, int x) { return x >= 0 && (x > F || !((g >> x) & 1)); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  nS++;
  int c = F + 1;
  if (c > 3 * m && c <= 4 * m) {
    nD4++;
    static int lev[256], isgen[1024];
    for (int x = 0; x < 4 * m + 2 && x < 1024; x++) isgen[x] = 0;
    for (int i = 0; i < e; i++) if (gens[i] < 1024) isgen[gens[i]] = 1;
    for (int r = 0; r < m; r++) { int j = 0; while (!inS(gm, F, j * m + r)) j++; lev[r] = j; }
    int G1[256], k1 = 0, G2[256], k2 = 0;
    for (int r = 1; r < m; r++) { if (isgen[m + r]) G1[k1++] = r; if (isgen[2 * m + r]) G2[k2++] = r; }
    static char inU2[256], inS2[256], inTG[256], inTU[256];
    for (int r = 0; r < m; r++) { inS2[r] = lev[r] <= 2; inU2[r] = (lev[r] == 2 && !isgen[2 * m + r]); inTG[r] = 0; inTU[r] = 0; }
    int u2 = 0; for (int r = 0; r < m; r++) u2 += inU2[r];
    long long Pu = 0;
    for (int i = 0; i < k1; i++) for (int j = i; j < k1; j++) if (G1[i] + G1[j] < m) Pu++;
    for (int i = 0; i < k1; i++) for (int j = 0; j < k2; j++) if (G1[i] + G2[j] < m) inTG[G1[i] + G2[j]] = 1;
    int tu = 0;
    for (int i = 0; i < k1; i++) for (int r = 0; r < m; r++) if (inU2[r]) { int v = G1[i] + r; if (v < m && !inS2[v] && !inTG[v] && !inTU[v]) { inTU[v] = 1; tu++; } }
    long long sigT = (long long)k1 * u2 + 2 * Pu - 3LL * tu;
    long long s012 = 0; for (int r = 0; r < m; r++) s012 += (lev[r] <= 2 ? 3 - lev[r] : 0);
    long long s3 = 0; for (int r = 0; r < m; r++) s3 += (lev[r] <= 3);
    long long Q3 = (long long)e * s012 - 3 * s3;
    int h = c - 3 * m; long long L3 = 0; for (int r = 0; r < h; r++) L3 += (lev[r] <= 3);
    long long d4 = h - L3;
    long long Q4 = (long long)(e - 1) * L3 - 4 * d4;
    long long gsum = 0; for (int r = 0; r < m; r++) gsum += lev[r];
    long long W = (long long)e * (c - g) - c;
    if (W != Q3 + Q4 || gsum != g) { fprintf(stderr, "IDENTITY MISMATCH m=%d c=%d\n", m, c); exit(1); }
    if (sigT < 0 || Q3 - sigT < 0) { fprintf(stderr, "PROOF BOUND VIOLATED m=%d sigT=%lld Q3=%lld\n", m, sigT, Q3); exit(1); }
    if (Q3 - sigT < minRest) minRest = Q3 - sigT;
    long long sig = Q4 + sigT;
    if (sig < minSig) { minSig = sig; re = e; rm = m; rc = c; for (int i = 0; i < e; i++) rgens[i] = gens[i]; }
    if (Q4 < 0) { nneg++; double rr = (double)sigT / (double)(-Q4); if (rr < minRatio) minRatio = rr; }
    if (sig < 0) { fail++; if (shown < 20) { shown++; fprintf(stderr, "SIG FAIL sig=%lld W=%lld Q3=%lld sigT=%lld Q4=%lld m=%d c=%d e=%d gens=", sig, W, Q3, sigT, Q4, m, c, e);
        for (int i = 0; i < e; i++) fprintf(stderr, "%d,", gens[i]); fprintf(stderr, "\n"); } }
  }
  if (g == G) return;
  int ng[128];
  for (int jj = 0; jj < e; jj++) {
    int nn = gens[jj]; if (nn <= F) continue;
    u128 gm2 = gm | ((u128)1 << nn);
    int e2 = 0, m2;
    if (nn == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else {
      m2 = m;
      for (int k = 0; k < e; k++) if (gens[k] != nn) ng[e2++] = gens[k];
      int y = nn + m, dec = 0;
      for (int a = m; a <= y / 2 && !dec; a++) if (a != nn && inS(gm2, nn, a) && (y - a) != nn && inS(gm2, nn, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, nn, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); if (G > 60) return 1;
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("genus <= %d: %lld semigroups, depth four %lld, Q4<0: %lld, SIG failures %lld, min SIG %lld (m=%d c=%d e=%d gens=", G, nS, nD4, nneg, fail, minSig, rm, rc, re);
  for (int i = 0; i < re; i++) printf("%d,", rgens[i]);
  printf("), min (Q3 - sigT) %lld, min sigT/(-Q4) on Q4<0: %.3f\n", minRest, minRatio);
  return 0;
}
