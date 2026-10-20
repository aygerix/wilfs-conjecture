/* LASTWIN on the tree (lead, 2026-10-20): for depth q = ceil(c/m) >= 2, h = c - (q-1)m,
 * LASTWIN: h <= e * |S n [(q-1)m, c)|.  Also LASTWIN' with e replaced by e - 1 (i.e. (q-1)m... ) and a full-window check
 * FULLWIN(j): m <= e * |S n [jm, (j+1)m)| for 1 <= j <= q-2.  Per depth: count, fails, min slack.
 * gcc -O3 -std=gnu11 lastwin.c -o lastwin */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G;
static uint64_t cnt[64], fl[64], flm1[64]; static int64_t mn[64]; static int nshow;
static inline int inS(u128 g, int F, int x) { return x >= 0 && (x > F || !((g >> x) & 1)); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  int c = F + 1;
  if (m >= 2 && c > m) {
    int q = (c + m - 1) / m, h = c - (q - 1) * m, L = 0;
    for (int x = (q - 1) * m; x < c; x++) L += inS(gm, F, x);
    int64_t sl = (int64_t)e * L - h, sl1 = (int64_t)(e - 1) * L - (h - L);
    if (q < 64) { cnt[q]++; if (sl < 0) { fl[q]++; if (nshow++ < 10) { fprintf(stderr, "FAIL q=%d g=%d m=%d c=%d e=%d L=%d gens=", q, g, m, c, e, L); for (int b = 0; b < e; b++) fprintf(stderr, "%d,", gens[b]); fprintf(stderr, "\n"); } }
      if (sl < mn[q]) mn[q] = sl; if (sl1 < 0) flm1[q]++; }
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
  for (int i = 0; i < 64; i++) mn[i] = INT64_MAX;
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  for (int q = 2; q < 64; q++) if (cnt[q]) printf("depth %d: S %llu LASTWIN fails %llu min slack %lld\n", q, (unsigned long long)cnt[q], (unsigned long long)fl[q], (long long)mn[q]);
  return 0;
}
