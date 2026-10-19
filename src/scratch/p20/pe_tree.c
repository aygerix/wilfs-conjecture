/* Per-element structure of WILF+ (lead, 2026-10-19).  beta(v) = v - m L1(v) (local balance, = P(v) - E(v)).
 * Candidates: (B1) beta(v) <= m-1-s_v for every v;  (B2) sum_v beta(v)^+ <= C2 (WILF+ without the m*Ltop credit);
 * (B3) sum over v of beta^+ restricted to v in layer 0.  Reports failure counts and extremes over the genus tree.
 * gcc -O3 -std=gnu11 pe_tree.c -o pe_tree ; ./pe_tree G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, f1, f2, nposS; static double r2max = -1e9, b1max = -1e9; static char ex2[300], ex1[300];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  if (F >= 1 && m >= 2 && e >= 3) {
    int64_t w[128], M = 0; for (int i = 0; i < m; i++) { int s = i; while (gapq(gm, s)) s += m; w[i] = s; if (s > M) M = s; }
    int64_t n[64]; int d = 0; for (int j = 0; j < e; j++) if (gens[j] != m) n[d++] = gens[j];
    #define INAP(v) ((v) >= 0 && (v) <= M && w[(v) % m] == (v))
    int64_t C2 = (int64_t)m * (m - 1) / 2, sp = 0; int bad1 = 0; double worst1 = -1e9; int64_t vb = 0;
    for (int i = 0; i < m; i++) { int64_t v = w[i], L1 = 0;
      for (int a = 0; a < d; a++) { int64_t y = v, dep = 0; while (INAP(y - n[a])) { y -= n[a]; dep++; } if (dep) L1 += dep * ((M - v + n[a]) / m - (M - v) / m); }
      int64_t b = v - (int64_t)m * L1; if (b > 0) { sp += b; int64_t s = (M - v) % m; if (b > m - 1 - s) { bad1 = 1; double q = (double)(b - (m - 1 - s)) / m; if (q > worst1) { worst1 = q; vb = v; } } } }
    #undef INAP
    tot++; if (bad1) { f1++; if (worst1 > b1max) { b1max = worst1; int p = snprintf(ex1, 300, "g=%d m=%d c=%d e=%d v=%lld excess/m=%.3f gens=", g, m, F + 1, e, (long long)vb, worst1); for (int a = 0; a < d && p < 280; a++) p += snprintf(ex1 + p, 300 - p, "%d,", (int)n[a]); } }
    if (sp > 0) nposS++;
    double r = (double)sp / C2; if (sp > C2) f2++;
    if (r > r2max) { r2max = r; int p = snprintf(ex2, 300, "g=%d m=%d c=%d e=%d gens=", g, m, F + 1, e); for (int a = 0; a < d && p < 280; a++) p += snprintf(ex2 + p, 300 - p, "%d,", (int)n[a]); }
  }
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
  printf("genus<=%d e>=3: %llu S; S with some beta>0: %llu\n", G, (unsigned long long)tot, (unsigned long long)nposS);
  printf("(B1) beta(v) <= m-1-s_v fails in %llu S; worst excess/m %.3f at %s\n", (unsigned long long)f1, b1max, ex1);
  printf("(B2) sum beta^+ <= C2 fails in %llu S; max sum beta^+/C2 = %.5f at %s\n", (unsigned long long)f2, r2max, ex2);
  return 0;
}
