/* Exhaustive (genus <= G): per genus, min W/c over all S, over the hard class H (#PF>=3m > e-1), and #H;
   also checks MC_i (top e-1 PF numbers, all i <= K) on every S with t > e-1.  fejer only. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t cnt, nH[64], nAll[64], mcfail, mctest; static double minAll[64], minH[64]; static int shownH=0;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static int cmpd(const void*a,const void*b){ int x=*(int*)a,y=*(int*)b; return x>y?-1:x<y; }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt++;
  int c = F + 1;
  if (c > 0 && m > 1) {
    int isS[512]; for (int z = 0; z < 512; z++) isS[z] = !gapq(gm, z);
    int ap[128], M = 0; for (int r = 0; r < m; r++) { int w = r; while (!isS[w]) w += m; ap[r] = w; if (w > M) M = w; }
    int K = M / m, d = e - 1;
    int pf[128], t = 0, h3 = 0;
    for (int z = 1; z <= F; z++) if (!isS[z]) { int ok = 1; for (int j = 0; j < e && ok; j++) if (!isS[z + gens[j]]) ok = 0; if (ok) { pf[t++] = z; if (z >= 3*m) h3++; } }
    int l = c - g; double r = (double)((long)e*l - c)/c;
    nAll[g]++; if (r < minAll[g]) minAll[g] = r;
    if (h3 > d) { nH[g]++; if (r < minH[g]) minH[g] = r; if (r < 0.105 && shownH++ < 12) { printf("hardtight g=%d W/c=%.4f m=%d e=%d t=%d K=%d gens:", g, r, m, e, t, K); for (int q=0;q<e;q++) printf(" %d",gens[q]); printf("\n"); } }
    if (t > d) {
      qsort(pf, t, sizeof(int), cmpd); mctest++;
      for (int i = 1; i <= K; i++) { long L = 0, R = 0;
        for (int q = 0; q < m; q++) { int k1 = ap[q]/m; L += k1 < i ? k1 : i; for (int k = 0; k < d; k++) { int wf = pf[k] + m; int l1 = wf >= ap[q] ? (wf - ap[q])/m : 0; R += l1 < i ? l1 : i; } }
        if (L > R) { mcfail++; if (mcfail <= 5) { printf("MC FAIL i=%d g=%d m=%d e=%d gens:", i, g, m, e); for (int q=0;q<e;q++) printf(" %d",gens[q]); printf("\n"); } break; } }
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
  for (int k = 0; k < 64; k++) { minAll[k] = 1e9; minH[k] = 1e9; }
  visit(0, -1, 1, gens, 1, 0);
  printf("genus<=%d semigroups=%llu | MC tested (t>e-1): %llu, MC fails: %llu\n", G, (unsigned long long)cnt, (unsigned long long)mctest, (unsigned long long)mcfail);
  for (int g = 1; g <= G; g++) printf("g=%d n=%llu minW/c=%.4f | hard n=%llu minW/c=%.4f\n", g, (unsigned long long)nAll[g], minAll[g], (unsigned long long)nH[g], nH[g]?minH[g]:-1.0);
  return 0;
}
