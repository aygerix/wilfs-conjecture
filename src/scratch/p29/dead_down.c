/* Conjecture DEAD on the tree of numerical semigroups (genus <= G) (lead, 2026-10-20).
 * For w in Ap(S,m): o(w) = max length of a factorisation into non-m minimal generators, mu_b(w) = max{j: w - j g_b in S}.
 * Lambda = sum mu_b(w), O = sum o(w), T_c = g - O.  DEAD: W - (Lambda - O) >= 0, i.e. (e-1) ell >= Lambda + T_c.
 * Prints per genus: count, failures, min D over e >= 3, #(D == 0, e >= 3); first few failures / tight cases to stderr.
 * gcc -O3 -std=gnu11 dead_tree.c -o dead_tree */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G;
static uint64_t cnt[80], fail[80], zero3[80]; static int64_t mind[80];
static int nshow; static uint64_t downfail[80]; static int64_t mindown[80]; static int nshowd; static int64_t minDnu = INT64_MAX; static char bestnu[512];
static inline int inS(u128 g, int F, int x) { return x >= 0 && (x > F || !((g >> x) & 1)); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt[g]++;
  int c = F + 1;
  if (m >= 2) {
    int w[128], o[128];
    for (int r = 0; r < m; r++) { int x = r; while (!inS(gm, F, x)) x += m; w[r] = x; }
    /* orders: process residues by increasing w */
    int idx[128]; for (int r = 0; r < m; r++) idx[r] = r;
    for (int i = 1; i < m; i++) { int t = idx[i], j = i; while (j > 0 && w[idx[j - 1]] > w[t]) { idx[j] = idx[j - 1]; j--; } idx[j] = t; }
    int64_t O = 0, Lam = 0, gg = 0;
    for (int ii = 0; ii < m; ii++) { int r = idx[ii], v = w[r]; gg += v / m;
      if (v == 0) { o[r] = 0; continue; }
      int best = -1;
      for (int b = 0; b < e; b++) { int gb = gens[b]; if (gb == m) continue; int u = v - gb; if (u >= 0 && inS(gm, F, u)) { int ou = o[u % m]; if (ou + 1 > best) best = ou + 1; } }
      o[r] = best; O += best;
      for (int b = 0; b < e; b++) { int gb = gens[b]; if (gb == m) continue; int j = 0; while (inS(gm, F, v - (j + 1) * gb)) j++; Lam += j; } }
    int64_t W = (int64_t)e * (c - gg) - c, D = W - (Lam - O);
    { int q = (c + m - 1) / m, h = c - (q - 1) * m; int64_t sl[160]; for (int k = 0; k < 160; k++) sl[k] = 0;
      for (int r = 0; r < m; r++) { int v = w[r], x = v / m, tp = (r < h) ? q : q - 1, Lu = tp - x, t = x - o[r];
        for (int b = 0; b < e; b++) { int gb = gens[b]; if (gb == m) continue; int lam = 0; while (lam < 200 && v + (lam + 1) * gb < 128 + 2 * F + 4 * m && inS(gm, F, v + (lam + 1) * gb) && !inS(gm, F, v + (lam + 1) * gb - m)) lam++;
          for (int j = lam + 1; j <= Lu; j++) sl[o[r] + j]++; }
        for (int j = Lu + 1; j <= Lu + t; j++) sl[o[r] + j]--; }
      int64_t run = 0, mn = 0; for (int k = 0; k < 160; k++) { run += sl[k]; if (run < mn) mn = run; }
      if (run != D) { fprintf(stderr, "DOWN total mismatch g=%d m=%d run=%lld D=%lld\n", g, m, (long long)run, (long long)D); exit(1); }
      if (mn < 0) { downfail[g]++; if (nshowd++ < 10) { fprintf(stderr, "DOWN FAIL g=%d m=%d c=%d e=%d min=%lld gens=", g, m, c, e, (long long)mn); for (int b = 0; b < e; b++) fprintf(stderr, "%d,", gens[b]); fprintf(stderr, "\n"); } }
      if (mn < mindown[g]) mindown[g] = mn; }
    if (D < 0) { fail[g]++; if (nshow++ < 20) { fprintf(stderr, "FAIL g=%d m=%d c=%d e=%d W=%lld Lam=%lld O=%lld gens=", g, m, c, e, (long long)W, (long long)Lam, (long long)O); for (int b = 0; b < e; b++) fprintf(stderr, "%d,", gens[b]); fprintf(stderr, "\n"); } }
    if (e >= 3) { if (D < mind[g]) mind[g] = D; if (D == 0) zero3[g]++; }
    if (Lam > O && D < minDnu) { minDnu = D; int p = sprintf(bestnu, "minD with Lam>O: D=%lld W=%lld Lam-O=%lld g=%d m=%d c=%d e=%d gens=", (long long)D, (long long)W, (long long)(Lam - O), g, m, c, e);
      for (int b = 0; b < e && p < 480; b++) p += sprintf(bestnu + p, "%d,", gens[b]); }
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
  for (int i = 0; i < 80; i++) { mind[i] = INT64_MAX; mindown[i] = 0; }
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  for (int g = 0; g <= G; g++) printf("g=%d DOWNfail=%llu\n", g, (unsigned long long)downfail[g]);
  printf("g,count,DEADfail,minD(e>=3),#D=0(e>=3)\n");
  for (int g = 0; g <= G; g++) printf("%d,%llu,%llu,%lld,%llu\n", g, (unsigned long long)cnt[g], (unsigned long long)fail[g], (long long)(mind[g] == INT64_MAX ? -999 : mind[g]), (unsigned long long)zero3[g]);
  printf("%s\n", bestnu);
  return 0;
}
