/* SUF2 (lead, 2026-10-20): which start points s make e*|S n [s,c)| >= c-s hold for all S of genus <= G?
 * For each S and each s in [0,c): classify by k = floor((c-s-1)/m)+... we record failures for
 *   (A) s = c - k*m (k >= 1, Eliahou alignment),  (B) s = j*m,  (C) s = c - k*m - 1 ... and
 *   (D) the TB2 analogue (e-1)*|S n [s,c)| + 1 >= c - s for s = c-m and s = (q-1)m.
 * usage: ./suf2 G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, fA, fB, fD1, fD2, fA1; static long long mnA = 1LL << 40, mnD1 = 1LL << 40; static int shown;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(u128 gm, int m, int *gens, int e, int c){
  tot++; int cnt[256]; int run = 0; for (int s = c - 1; s >= 0; s--){ if (!gapq(gm, s)) run++; cnt[s] = run; }
  for (int k = 1; c - k * m >= 0; k++){ int s = c - k * m; long long d = (long long)e * cnt[s] - (c - s);
    if (d < mnA) mnA = d; if (d < 0){ fA++; if (k == 1) fA1++; if (shown < 8){ shown++; printf("AFAIL k=%d m=%d c=%d e=%d cnt=%d gens:", k, m, c, e, cnt[s]); for (int a = 0; a < e; a++) printf(" %d", gens[a]); printf("\n"); } } }
  for (int j = 0; j * m < c; j++){ int s = j * m; if ((long long)e * cnt[s] < c - s) fB++; }
  if (c - m >= 0){ long long d = (long long)(e - 1) * cnt[c - m] + 1 - m; if (d < mnD1) mnD1 = d; if (d < 0) fD1++; }
  { int q = (c + m - 1) / m; int s = (q - 1) * m; if ((long long)(e - 1) * cnt[s] + 1 < c - s) fD2++; }
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
  printf("G<=%d: S %llu; (A) s=c-km fails %llu (k=1: %llu, min %lld); (B) s=jm fails %llu; (D1) (e-1)|S n[c-m,c)|+1>=m fails %llu (min %lld); (D2) TB2 fails %llu\n", G,
    (unsigned long long)tot, (unsigned long long)fA, (unsigned long long)fA1, mnA, (unsigned long long)fB, (unsigned long long)fD1, mnD1, (unsigned long long)fD2);
}
