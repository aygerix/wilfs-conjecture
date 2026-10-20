/* LAYER(j) on the tree of numerical semigroups (genus <= G) (lead, 2026-10-20).
 * s_j = |S n [jm, (j+1)m)| = #{r : x_r <= j} (x_r = Kunz level).  LAYER(j): j s_j <= e (s_0 + ... + s_{j-1}).
 * Prints, for j = 1..8: number of S (with q >= j) and failures; min slack of LAYER(3); depth-four count and how many
 * satisfy (e+3) d4 <= (e-1) h (then LAYER(3) gives Wilf).  gcc -O3 -std=gnu11 layer_tree.c -o layer_tree */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G;
static uint64_t tot[10], lf[10], d4n, d4cov; static int64_t min3 = INT64_MAX; static char best3[512]; static int nshow;
static inline int inS(u128 g, int F, int x) { return x >= 0 && (x > F || !((g >> x) & 1)); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  int c = F + 1;
  if (m >= 2) {
    int lv[128], q = 0;
    for (int r = 0; r < m; r++) { int x = r; while (!inS(gm, F, x)) x += m; lv[r] = x / m; if (lv[r] > q) q = lv[r]; }
    int64_t s[130], pre = 0;
    for (int j = 0; j <= q; j++) { s[j] = 0; for (int r = 0; r < m; r++) s[j] += lv[r] <= j; }
    for (int j = 1; j <= q && j < 10; j++) {
      pre += s[j - 1]; tot[j]++;
      int64_t sl = (int64_t)e * pre - (int64_t)j * s[j];
      if (sl < 0) { lf[j]++; if (j == 3 && nshow++ < 10) { fprintf(stderr, "L3 FAIL g=%d m=%d c=%d e=%d gens=", g, m, c, e); for (int b = 0; b < e; b++) fprintf(stderr, "%d,", gens[b]); fprintf(stderr, "\n"); } }
      if (j == 3 && sl < min3 && e >= 3) { min3 = sl; int p = sprintf(best3, "min L3 slack (e>=3) %lld g=%d m=%d c=%d e=%d gens=", (long long)sl, g, m, c, e); for (int b = 0; b < e && p < 480; b++) p += sprintf(best3 + p, "%d,", gens[b]); }
    }
    if (q == 4) { int h = c - 3 * m, d4 = 0; for (int r = 0; r < m; r++) d4 += lv[r] == 4; d4n++; if ((int64_t)(e + 3) * d4 <= (int64_t)(e - 1) * h) d4cov++; }
  }
  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int n = gens[j]; if (n <= F) continue;
    u128 gm2 = gm | ((u128)1 << n);
    int e2 = 0, m2;
    if (n == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else {
      m2 = m;
      for (int k = 0; k < e; k++) if (gens[k] != n) ng[e2++] = gens[k];
      int y = n + m, dec = 0;
      for (int a = m; a <= y / 2 && !dec; a++) if (a != n && inS(gm2, n, a) && (y - a) != n && inS(gm2, n, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, n, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); if (G > 60) return 1;
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  for (int j = 1; j < 10; j++) printf("LAYER(%d): S %llu fails %llu\n", j, (unsigned long long)tot[j], (unsigned long long)lf[j]);
  printf("%s\ndepth four: %llu S, (e+3)d4 <= (e-1)h for %llu\n", best3, (unsigned long long)d4n, (unsigned long long)d4cov);
  return 0;
}
