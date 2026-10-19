/* Monotonicity of the chain slack along the semigroup tree (lead, 2026-10-19).
 * For each child S (parent P = S u {F(S)}, same multiplicity), slack(S) = B_chain(S) - need(S), need = (d-1)m(m-1)/2.
 * Reports, by height class of S and P, the counts of edges with slack(S) < slack(P), and the min of slack(S) - slack(P).
 * Also the normalized version slack/C2.  gcc -O3 -std=gnu11 chain_mono.c -o chain_mono ; ./chain_mono G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G;
static uint64_t cnt[4][4], dec[4][4]; static int64_t mind[4][4]; static int minset[4][4]; static char ex[4][4][256];
static uint64_t negS3;  /* height>=3 nodes with negative slack (CHAIN-H3 failures) */
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void stats(u128 gm, int m, int *gens, int e, int64_t *slack, int *H) {
  int w[128]; int64_t M = 0;
  for (int i = 0; i < m; i++) { int s = i; while (gapq(gm, s)) s += m; w[i] = s; if (s > M) M = s; }
  int d = 0, n[64]; for (int j = 0; j < e; j++) if (gens[j] != m) n[d++] = gens[j];
  int64_t Bc = 0;
  for (int a = 0; a < d; a++) for (int i = 0; i < m; i++) { int64_t t = w[i];
    for (;;) { int64_t t2 = t + n[a]; if (t2 > M) break; if (w[t2 % m] != t2) break; t = t2; } Bc += M - t; }
  *slack = Bc - (int64_t)(d - 1) * m * (m - 1) / 2;
  int ord[128]; for (int i = 0; i < m; i++) ord[i] = i;
  for (int i = 1; i < m; i++) { int v = ord[i], j = i - 1; while (j >= 0 && w[ord[j]] > w[v]) { ord[j + 1] = ord[j]; j--; } ord[j + 1] = v; }
  int ml[128]; ml[0] = 0; int Hh = 0;
  for (int t = 1; t < m; t++) { int i = ord[t], best = 1 << 20;
    for (int a = 0; a < d; a++) { int y = w[i] - n[a]; if (y >= 0 && w[y % m] == y) { int v = 1 + ml[y % m]; if (v < best) best = v; } }
    ml[i] = best; if (best > Hh) Hh = best; }
  *H = Hh;
}
static void visit(u128 gm, int F, int m, int *gens, int e, int g, int64_t pslack, int pH, int pm) {
  int64_t sl = 0; int H = 0;
  if (m >= 2 && e >= 3) {
    stats(gm, m, gens, e, &sl, &H);
    if (H >= 3 && sl < 0) negS3++;
    if (pm == m && pH > 0) {
      int cs = H >= 3 ? 2 : 1, cp = pH >= 3 ? 2 : 1;
      cnt[cs][cp]++; int64_t dd = sl - pslack;
      if (dd < 0) dec[cs][cp]++;
      if (!minset[cs][cp] || dd < mind[cs][cp]) { minset[cs][cp] = 1; mind[cs][cp] = dd;
        int p = snprintf(ex[cs][cp], 256, "g=%d m=%d F=%d e=%d slack %lld -> %lld gens=", g, m, F, e, (long long)pslack, (long long)sl);
        for (int j = 0; j < e && p < 230; j++) p += snprintf(ex[cs][cp] + p, 256 - p, "%d,", gens[j]); }
    }
  }
  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int nn = gens[j]; if (nn <= F) continue;
    u128 gm2 = gm | ((u128)1 << nn);
    int e2 = 0, m2;
    if (nn == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else {
      m2 = m;
      for (int k = 0; k < e; k++) if (gens[k] != nn) ng[e2++] = gens[k];
      int y = nn + m, decmp = 0;
      for (int a = m; a <= y / 2 && !decmp; a++) if (a != nn && !gapq(gm2, a) && (y - a) != nn && !gapq(gm2, y - a)) decmp = 1;
      if (!decmp) ng[e2++] = y;
    }
    visit(gm2, nn, m2, ng, e2, g + 1, (m >= 2 && e >= 3) ? sl : 0, (m >= 2 && e >= 3) ? (H > 0 ? H : 1) : 0, m);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0, 0, 0, 0);
  const char *nm[4] = {"h0", "h1", "h>=3", "?"};
  printf("CHAIN-H3 failures (height>=3, slack<0): %llu\n", (unsigned long long)negS3);
  for (int cs = 1; cs <= 2; cs++) for (int cp = 1; cp <= 2; cp++) if (cnt[cs][cp] || cs == 2)
    printf("child %s <- parent %s: edges %llu, slack decreases %llu, min change %lld at %s\n", cs == 2 ? "h>=3" : "h<=2", cp == 2 ? "h>=3" : "h<=2",
      (unsigned long long)cnt[cs][cp], (unsigned long long)dec[cs][cp], (long long)mind[cs][cp], minset[cs][cp] ? ex[cs][cp] : "-");
  return 0;
}
