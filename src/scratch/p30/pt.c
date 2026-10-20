/* Prefix/tail split W = P + T for c > 3m (lead, 2026-10-20): P = e|S n [0,3m)| - 3m, T = e|S n [3m,c)| - (c - 3m).
 * Reports per depth: #(P<0), min T/(-P) over P<0; #(T<0), min P/(-T) over T<0 (e >= 3). gcc -O3 -std=gnu11 pt.c -o pt */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G_;
static uint64_t cnt[64], pn[64], tn[64]; static double rp[64], rt[64]; static char bp[64][300], bt[64][300];
static inline int inS(u128 g, int F, int x) { return x >= 0 && (x > F || !((g >> x) & 1)); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  int c = F + 1;
  if (m >= 2 && c > 3 * m && e >= 3) {
    int q = (c + m - 1) / m; if (q > 63) q = 63;
    int64_t sig = 0, L = 0; for (int x = 0; x < 3 * m; x++) sig += inS(gm, F, x); for (int x = 3 * m; x < c; x++) L += inS(gm, F, x);
    int64_t P = (int64_t)e * sig - 3 * m, T = (int64_t)e * L - (c - 3 * m);
    cnt[q]++;
    if (P < 0) { pn[q]++; double r = (double)T / (double)(-P); if (pn[q] == 1 || r < rp[q]) { rp[q] = r; int p = sprintf(bp[q], "P=%lld T=%lld m=%d c=%d e=%d gens=", (long long)P, (long long)T, m, c, e); for (int b = 0; b < e && p < 280; b++) p += sprintf(bp[q] + p, "%d,", gens[b]); } }
    if (T < 0) { tn[q]++; double r = (double)P / (double)(-T); if (tn[q] == 1 || r < rt[q]) { rt[q] = r; int p = sprintf(bt[q], "P=%lld T=%lld m=%d c=%d e=%d gens=", (long long)P, (long long)T, m, c, e); for (int b = 0; b < e && p < 280; b++) p += sprintf(bt[q] + p, "%d,", gens[b]); } }
  }
  if (g == G_) return;
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
  G_ = atoi(argv[1]); if (G_ > 60) return 1;
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  for (int q = 4; q < 64; q++) if (cnt[q]) { printf("depth %d: S %llu | P<0: %llu, min T/(-P) %.3f [%s] | T<0: %llu, min P/(-T) %.3f [%s]\n", q, (unsigned long long)cnt[q], (unsigned long long)pn[q], pn[q] ? rp[q] : 0.0, pn[q] ? bp[q] : "", (unsigned long long)tn[q], tn[q] ? rt[q] : 0.0, tn[q] ? bt[q] : ""); }
  return 0;
}
