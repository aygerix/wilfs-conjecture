/* LAYER_j(n) for general window length n (lead, 2026-10-20).
 * LAYER_j(n): j * |S n [jn, (j+1)n)| <= e * |S n [0, jn)|.  n = m, j = 3 is Theorem LAYER3; n = c/j is Wilf.
 * Tree of numerical semigroups to genus G; for j = 1, 2, 3 and every n in [1, ceil(c/j)], count failures and
 * record the minimal slack, split by n < m, n = m, m < n.  Prints first failures to stderr.
 * gcc -O3 -o layn layn.c ; ./layn G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static long long nS, fail[4][3], mins[4][3]; static int shown;
static inline int inS(u128 g, int F, int x) { return x >= 0 && (x > F || !((g >> x) & 1)); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  nS++;
  int c = F + 1;
  if (c > 0) {
    static int pre[400]; pre[0] = 0;
    for (int x = 0; x < 4 * c + 8 && x < 399; x++) pre[x + 1] = pre[x] + inS(gm, F, x);
    for (int j = 1; j <= 3; j++) {
      int nmax = (c + j - 1) / j;
      for (int n = 1; n <= nmax; n++) {
        int hi = (j + 1) * n; if (hi > 398) break;
        long long lhs = (long long)j * (pre[hi] - pre[j * n]), rhs = (long long)e * pre[j * n];
        long long sl = rhs - lhs; int cl = n < m ? 0 : (n == m ? 1 : 2);
        if (sl < mins[j][cl]) mins[j][cl] = sl;
        if (sl < 0) { fail[j][cl]++;
          if (shown < 30) { shown++; fprintf(stderr, "FAIL j=%d n=%d m=%d c=%d e=%d g=%d slack=%lld gens=", j, n, m, c, e, g, sl);
            for (int b = 0; b < e; b++) fprintf(stderr, "%d,", gens[b]); fprintf(stderr, "\n"); } }
      }
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
  for (int j = 0; j < 4; j++) for (int k = 0; k < 3; k++) mins[j][k] = 1LL << 60;
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("genus <= %d: %lld semigroups\n", G, nS);
  const char *nm[3] = {"n<m", "n=m", "n>m"};
  for (int j = 1; j <= 3; j++) for (int k = 0; k < 3; k++)
    printf("LAYER_%d(n), %s: failures %lld, min slack %lld\n", j, nm[k], fail[j][k], mins[j][k]);
  return 0;
}
