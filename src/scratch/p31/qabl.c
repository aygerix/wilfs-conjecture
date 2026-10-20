/* Necessity audit of the LAYER3 surplus at depth four, every numerical semigroup (lead, 2026-10-20).
 * Exact split from the LAYER3 proof (k1, k2, k3 = generator counts in layers 1,2,3; k4p = in layers >= 4):
 *   N3 = G3 + A_G + T_U + A_R (disjoint; asserted), A_G = N3 n (G1+G2)_{<m}, T_U = ((G1+U2)_{<m}) \ (S2 u T_G),
 *   A_R = rest of N3 (inside R = (G1+G1)_{>=m} - m; asserted).
 *   Q3 = sigT + Pwp3 + Puu2 + Pw + Gam23 + Gam4 with
 *     sigT = k1 u2 + 2 Pu - 3|T_U|, Pwp3 = 3(Pw - |A_R|), Puu2 = 2(Pu - u2), Pw,
 *     Gam4 = k4p (3 + 2k1 + k2 + u2), Gam23 = (1+k1)k2 + (k2+k3)(3+2k1+k2+u2) - 3k2 - 3k3 - 3|A_G|.
 * W = Q3 + Q4, Q4 = (e-1)L3 - 4 d4.  For each nonempty subset X of the 6 components report #(W - sum X < 0).
 * gcc -O3 -o qabl qabl.c ; ./qabl G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G, DMIN = 4, DMAX = 4, EMIN = 1; static long long nS, nD4, fails[64], worst[64]; static int wg[64][64], we[64], wm[64], wc[64];
static const char *NM[6] = {"sigT", "Pwp3", "Puu2", "Pw", "Gam23", "Gam4"};
static inline int inS(u128 g, int F, int x) { return x >= 0 && (x > F || !((g >> x) & 1)); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  nS++;
  int c = F + 1;
  int depth = (c + m - 1) / m;
  if (c > 3 * m && depth >= DMIN && depth <= DMAX && e >= EMIN) {
    nD4++;
    static int lev[256], isgen[1200];
    for (int x = 0; x < 4 * m + 2 && x < 1200; x++) isgen[x] = 0;
    for (int i = 0; i < e; i++) if (gens[i] < 1200) isgen[gens[i]] = 1;
    for (int r = 0; r < m; r++) { int j = 0; while (!inS(gm, F, j * m + r)) j++; lev[r] = j; }
    int G1[256], k1 = 0, G2[256], k2 = 0, k3 = 0, k4p = 0;
    for (int i = 0; i < e; i++) { int lay = gens[i] / m; if (gens[i] == m) continue; if (lay == 1) G1[k1++] = gens[i] - m; else if (lay == 2) G2[k2++] = gens[i] - 2 * m; else if (lay == 3) k3++; else k4p++; }
    static char inU2[256], inS2[256], inTG[256], inTU[256], inR[256];
    for (int r = 0; r < m; r++) { inS2[r] = lev[r] <= 2; inU2[r] = (lev[r] == 2 && !isgen[2 * m + r]); inTG[r] = inTU[r] = inR[r] = 0; }
    long long u2 = 0; for (int r = 0; r < m; r++) u2 += inU2[r];
    long long Pu = 0, Pw = 0;
    for (int i = 0; i < k1; i++) for (int j = i; j < k1; j++) { int s = G1[i] + G1[j]; if (s < m) Pu++; else { Pw++; inR[s - m] = 1; } }
    for (int i = 0; i < k1; i++) for (int j = 0; j < k2; j++) if (G1[i] + G2[j] < m) inTG[G1[i] + G2[j]] = 1;
    long long tu = 0;
    for (int i = 0; i < k1; i++) for (int r = 0; r < m; r++) if (inU2[r]) { int v = G1[i] + r; if (v < m && !inS2[v] && !inTG[v] && !inTU[v]) { inTU[v] = 1; tu++; } }
    long long aG = 0, aR = 0, n3 = 0, g3 = 0;
    for (int r = 0; r < m; r++) if (lev[r] == 3) {
      n3++;
      if (isgen[3 * m + r]) { g3++; continue; }
      if (inTG[r]) { aG++; continue; }
      if (inTU[r]) continue;
      if (!inR[r]) { fprintf(stderr, "N3 COVER FAIL m=%d r=%d\n", m, r); exit(1); }
      aR++;
    }
    for (int r = 0; r < m; r++) if (inTU[r] && lev[r] != 3) { fprintf(stderr, "TU not in N3 m=%d r=%d\n", m, r); exit(1); }
    if (g3 != k3) { fprintf(stderr, "G3 mismatch\n"); exit(1); }
    long long s012 = 3 + 2LL * k1 + k2 + u2;
    long long C[6];
    C[0] = (long long)k1 * u2 + 2 * Pu - 3 * tu;
    C[1] = 3 * (Pw - aR); C[2] = 2 * (Pu - u2); C[3] = Pw;
    C[5] = (long long)k4p * s012;
    C[4] = (long long)(1 + k1) * k2 + (long long)(k2 + k3) * s012 - 3LL * k2 - 3LL * k3 - 3 * aG;
    long long s3 = 0, s012b = 0; for (int r = 0; r < m; r++) { s3 += (lev[r] <= 3); s012b += (lev[r] <= 2 ? 3 - lev[r] : 0); }
    long long Q3 = (long long)e * s012b - 3 * s3;
    if (s012 != s012b) { fprintf(stderr, "s012 mismatch m=%d %lld %lld\n", m, s012, s012b); exit(1); }
    long long sumC = 0; for (int i = 0; i < 6; i++) { sumC += C[i]; if (C[i] < 0) { fprintf(stderr, "NEG component %s=%lld m=%d\n", NM[i], C[i], m); exit(1); } }
    if (sumC != Q3) { fprintf(stderr, "Q3 SPLIT MISMATCH m=%d Q3=%lld sum=%lld\n", m, Q3, sumC); exit(1); }
    long long L = 0, Gp = 0, D4 = 0;
    for (int x = 3 * m; x < c; x++) { if (inS(gm, F, x)) L++; else Gp++; }
    for (int r = 0; r < m; r++) D4 += (lev[r] >= 4);
    long long Q4 = (long long)(e - 1) * L - Gp - 3 * D4, W = (long long)e * (c - g) - c;
    if (W != Q3 + Q4) { fprintf(stderr, "W mismatch\n"); exit(1); }
    for (int X = 1; X < 64; X++) {
      long long v = W; for (int i = 0; i < 6; i++) if (X >> i & 1) v -= C[i];
      if (v < 0) { fails[X]++; if (v < worst[X]) { worst[X] = v; we[X] = e; wm[X] = m; wc[X] = c; for (int i = 0; i < e; i++) wg[X][i] = gens[i]; } }
    }
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
  if (argc > 3) { DMIN = atoi(argv[2]); DMAX = atoi(argv[3]); } if (argc > 4) EMIN = atoi(argv[4]);
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("genus <= %d: %lld semigroups, depth %d..%d: %lld (Q3 split and W = Q3 + (e-1)L - G - 3D4 asserted on all)\n", G, nS, DMIN, DMAX, nD4);
  for (int X = 1; X < 64; X++) {
    printf("drop {"); for (int i = 0; i < 6; i++) if (X >> i & 1) printf(" %s", NM[i]);
    printf(" }: failures %lld", fails[X]);
    if (fails[X]) { printf(", worst %lld at m=%d c=%d gens=", worst[X], wm[X], wc[X]); for (int i = 0; i < we[X]; i++) printf("%d,", wg[X][i]); }
    printf("\n");
  }
  return 0;
}
