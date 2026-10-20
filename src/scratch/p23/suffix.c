/* SUFFIX test (lead, 2026-10-20): for every numerical semigroup S of genus <= G (e >= 2), and every s in S n [0,c):
 *   SUF(s): e*|S n [s,c)| >= c - s.   s = 0 is Wilf; s = (q-1)m is TOPBAND.
 * Report: failures for s in mZ, failures for general s in S, smallest failing examples.
 * usage: ./suffix G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, totS, failM, failS; static long long mnM = 1LL << 40, mnS = 1LL << 40; static int shown;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(u128 gm, int m, int e, int c){
  tot++; int cnt = 0;
  for (int s = c - 1; s >= 0; s--){ if (gapq(gm, s)) continue; cnt++;
    long long d = (long long)e * cnt - (c - s); totS++;
    if (s % m == 0){ if (d < mnM) mnM = d; if (d < 0) failM++; }
    if (d < mnS){ mnS = d; }
    if (d < 0){ failS++; if (shown < 12){ shown++; printf("FAIL m=%d c=%d e=%d s=%d cnt=%d d=%lld S<c:", m, c, e, s, cnt, d);
        for (int z = 0; z < c; z++) if (!gapq(gm, z)) printf(" %d", z); printf("\n"); } } }
}
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  if (F >= 1 && m >= 2) check(gm, m, e, F + 1);
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
  printf("G<=%d: S %llu, (S,s) pairs %llu; failures s in mZ %llu (min %lld); failures general s %llu (min %lld)\n", G,
    (unsigned long long)tot, (unsigned long long)totS, (unsigned long long)failM, mnM, (unsigned long long)failS, mnS);
}
