/* Semigroups of genus <= G not covered by GW-20 (#PF >= 3m <= e-1).  Profile: K = floor(maxAp/m), e, m, t,
 * #PF >= im for i = 3..6, Wilf slack; and coverage of the conjectural ladder criteria "#PF >= im <= e-1".  fejer only. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t cnt, core, coverI[12], histK[64], histE[64], shown, resid, residK[64]; static int shownR;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt++;
  int c = F + 1;
  if (c > 0) {
    int isS[512]; for (int z = 0; z < 512; z++) isS[z] = !gapq(gm, z);
    int pf[128], t = 0;
    for (int z = 1; z <= F; z++) if (!isS[z]) { int ok = 1; for (int j = 0; j < e && ok; j++) if (!isS[z + gens[j]]) ok = 0; if (ok) pf[t++] = z; }
    int cI[12] = {0}; for (int i = 0; i < t; i++) for (int k = 0; k < 12; k++) if (pf[i] >= k * m) cI[k]++;
    { int M = F + m, K = M / m, ie = (K + 2) / 2; if (ie < 3) ie = 3; int cnt2 = 0; for (int i = 0; i < t; i++) if (pf[i] >= ie * m) cnt2++;
      if (K > 3 && cnt2 > e - 1) { resid++; residK[K < 63 ? K : 63]++; if (shownR++ < 8) { int ell = 0; for (int z = 0; z < c; z++) ell += isS[z]; printf("RESID K=%d i=%d m=%d e=%d t=%d c=%d W=%d #PF>=im=%d gens=", K, ie, m, e, t, c, e*ell-c, cnt2); for (int i = 0; i < e; i++) printf("%d,", gens[i]); printf("\n"); } } }
    if (cI[3] > e - 1) {
      core++;
      int M = F + m, K = M / m; histK[K < 63 ? K : 63]++; histE[e < 63 ? e : 63]++;
      for (int k = 3; k < 12; k++) if (cI[k] <= e - 1) { coverI[k]++; break; }
      int ell = 0; for (int z = 0; z < c; z++) ell += isS[z];
      if (0) { shown++; printf("CORE m=%d e=%d t=%d c=%d K=%d W=%d PF>=3m:%d PF>=4m:%d PF>=5m:%d gens=", m, e, t, c, K, e*ell-c, cI[3], cI[4], cI[5]); for (int i = 0; i < e; i++) printf("%d,", gens[i]); printf("\n"); }
    }
  }
  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int n = gens[j]; if (n <= F) continue;
    u128 gm2 = gm | ((u128)1 << n); int e2 = 0, m2;
    if (n == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else {
      m2 = m; for (int k = 0; k < e; k++) if (gens[k] != n) ng[e2++] = gens[k];
      int y = n + m, dec = 0;
      for (int a = m; a <= y / 2 && !dec; a++) if (a != n && !gapq(gm2, a) && (y - a) != n && !gapq(gm2, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, n, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("genus<=%d semigroups=%llu core(not GW-20)=%llu\n", G, (unsigned long long)cnt, (unsigned long long)core);
  printf("first ladder rung i covering a core S (#PF>=im <= e-1):"); for (int k = 3; k < 12; k++) printf(" i=%d:%llu", k, (unsigned long long)coverI[k]); printf("\n");
  printf("RESIDUAL (uniform ladder, i=max(3,floor((K+2)/2))): %llu  by K:", (unsigned long long)resid); for (int k = 0; k < 64; k++) if (residK[k]) printf(" %d:%llu", k, (unsigned long long)residK[k]); printf("\n");
  printf("K histogram:"); for (int k = 0; k < 64; k++) if (histK[k]) printf(" %d:%llu", k, (unsigned long long)histK[k]); printf("\n");
  printf("e histogram:"); for (int k = 0; k < 64; k++) if (histE[k]) printf(" %d:%llu", k, (unsigned long long)histE[k]); printf("\n");
  return 0;
}
