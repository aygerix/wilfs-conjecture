/* LASTWIN on the tree (lead, 2026-10-20): for depth q = ceil(c/m) >= 2, h = c - (q-1)m,
 * LASTWIN: h <= e * |S n [(q-1)m, c)|.  Also LASTWIN' with e replaced by e - 1 (i.e. (q-1)m... ) and a full-window check
 * FULLWIN(j): m <= e * |S n [jm, (j+1)m)| for 1 <= j <= q-2.  Per depth: count, fails, min slack.
 * gcc -O3 -std=gnu11 lastwin.c -o lastwin */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G;
static uint64_t cnt[64], fl[64], flm1[64], hg[64], hgw[64], ss[64]; static int nss; static uint64_t ss2[64]; static int nss2; static int64_t hgmin[64]; static int64_t mn[64]; static int nshow;
static inline int inS(u128 g, int F, int x) { return x >= 0 && (x > F || !((g >> x) & 1)); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  int c = F + 1;
  if (m >= 2 && c > m) {
    int q = (c + m - 1) / m, h = c - (q - 1) * m, L = 0;
    for (int x = (q - 1) * m; x < c; x++) L += inS(gm, F, x);
    int64_t sl = (int64_t)e * L - h, sl1 = (int64_t)(e - 1) * L - (h - L);
    if (q >= 3 && q < 64) {
      int lv[128]; for (int r = 0; r < m; r++) { int x = r; while (!inS(gm, F, x)) x += m; lv[r] = x / m; }
      int hard = 0, easy = 0, low = 0;
      for (int r = 0; r < h; r++) { if (lv[r] <= q - 3) low++;
        if (lv[r] != q) continue;
        int w = q * m + r, ok = 0;
        for (int b = 0; b < e && !ok; b++) { int gg = gens[b]; if (gg == m) continue; int u = w - gg; if (u >= 0 && inS(gm, F, u) && !inS(gm, F, u - m) && gg % m <= r) ok = 1; }
        if (ok) easy++; else hard++; }
      int64_t s1 = (int64_t)(e - 1) * low - hard, s2 = (int64_t)(e - 1) * L - easy - hard;
      { char in[128] = {0}; int sz = 0;
        for (int u = 0; u < h; u++) if (lv[u] <= q - 1) for (int b = 0; b < e; b++) { int gr = gens[b] % m; if (!gr) continue; int t = (u + gr) % m; if (!in[t]) { in[t] = 1; sz++; } }
        int d = 0; for (int r = 0; r < h; r++) d += lv[r] == q;
        int sz2 = sz; for (int u = 0; u < h; u++) if (lv[u] <= q - 1 && !in[u]) { in[u] = 1; sz2++; }
        if (sz2 < h) { ss2[q]++; if (nss2++ < 8) { fprintf(stderr, "SS2FAIL q=%d g=%d m=%d c=%d h=%d e=%d sz2=%d gens=", q, g, m, c, h, e, sz2); for (int b = 0; b < e; b++) fprintf(stderr, "%d,", gens[b]); fprintf(stderr, "\n"); } }
        if (sz < d) { ss[q]++; if (nss++ < 8) { fprintf(stderr, "SSFAIL q=%d g=%d m=%d c=%d e=%d d=%d sz=%d gens=", q, g, m, c, e, d, sz); for (int b = 0; b < e; b++) fprintf(stderr, "%d,", gens[b]); fprintf(stderr, "\n"); } } }
      if (s1 < 0) hg[q]++; if (s1 < hgmin[q]) hgmin[q] = s1; if (s2 < 0) hgw[q]++;
    }
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
  for (int i = 0; i < 64; i++) { mn[i] = INT64_MAX; hgmin[i] = INT64_MAX; }
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  for (int q = 2; q < 64; q++) if (cnt[q]) printf("depth %d: S %llu LASTWIN fails %llu min slack %lld | HG1 (hard <= (e-1)|S_{q-3} n [0,h)|) fails %llu min %lld | check %llu | SUMSET fails %llu | |X+A*| >= h fails %llu\n", q, (unsigned long long)cnt[q], (unsigned long long)fl[q], (long long)mn[q], (unsigned long long)hg[q], (long long)(hgmin[q] == INT64_MAX ? 0 : hgmin[q]), (unsigned long long)hgw[q], (unsigned long long)ss[q], (unsigned long long)ss2[q]);
  return 0;
}
