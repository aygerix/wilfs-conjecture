/* G(a,L) window growth test (lead, 2026-10-20). For every S (genus <= G), every a in [0, c+m] and L in [1,m] with
 * [a+L, a+m) subset S:   |S n [a+m, a+m+L)| <= (e-1) |S n [a, a+L)| + 1.
 * TB2 = (a=(q-1)m, L=h); D1 = (a=c-m, L=m); RC' = (a=(l-1)m).  Reports failures split by a mod m == 0 / a in S / other.
 * usage: ./gwin G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, inst, fM, fS, fO, fL; static int shown;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(u128 gm, int m, int *gens, int e, int c){
  tot++;
  for (int a = 0; a <= c + m; a++){
    int full = 1; /* [a+L, a+m) subset S: find smallest valid L */
    int Lmin = m; for (int z = a + m - 1; z >= a; z--){ if (gapq(gm, z)) break; Lmin = z - a; }
    if (Lmin < 1) Lmin = 1;
    for (int L = Lmin; L <= m; L++){ int lo = 0, hi = 0;
      for (int z = a; z < a + L; z++) if (!gapq(gm, z)) lo++;
      for (int z = a + m; z < a + m + L; z++) if (!gapq(gm, z)) hi++;
      inst++;
      if ((long)hi > (long)(e - 1) * lo + 1){
        if (a % m == 0) fM++; else if (!gapq(gm, a)) fS++; else fO++; if (L == m) fL++;
        if (shown < 12){ shown++; printf("FAIL a=%d L=%d m=%d c=%d e=%d lo=%d hi=%d a%%m=%d a_in_S=%d gens:", a, L, m, c, e, lo, hi, a % m, !gapq(gm, a)); for (int t = 0; t < e; t++) printf(" %d", gens[t]); printf("\n"); } } }
    (void)full; }
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
  printf("G<=%d: S %llu, instances %llu; failures: a in mZ %llu, a in S (not mZ) %llu, a gap %llu; with L=m %llu\n", G, (unsigned long long)tot, (unsigned long long)inst, (unsigned long long)fM, (unsigned long long)fS, (unsigned long long)fO, (unsigned long long)fL);
}
