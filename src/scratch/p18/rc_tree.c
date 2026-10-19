/* Criterion RC (lead, 2026-10-19), exhaustive over the semigroup tree (genus <= G).
 * Ap = Ap(S,m), M = max Ap = F + m, n_1..n_d the minimal generators other than m (d = e - 1).
 * R = sum_{w in Ap} sum_a ((M - w) mod n_a).  RC: 2R >= (d-1) m (m-1)  ==> W >= 0  (since mW + (d-1)m(m-1)/2 >= R).
 * Also asserts the identity  d m M - (d+1) sum Ap = m W + (d-1) m (m-1)/2  (tile-free CH').
 * Reports RC failures by e and genus, and min 2R/((d-1)m(m-1)) by e.
 * gcc -O3 -std=gnu11 rc_tree.c -o rc_tree */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G;
static uint64_t cnt[80], fail[80][64], tot[80][64], idfail, fq[3][64], tq[3][64], cfq[3][64]; static int nshow, nshowc; static double minc[3][64]; static int minc_set[3][64]; static char exc[3][64][256];
static double minr[64] = {0}; static int minr_set[64];
static char ex[64][256];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt[g]++;
  if (F >= 1 && m >= 2 && e >= 3) {
    int w[128]; int64_t sw = 0, M = 0;
    for (int i = 0; i < m; i++) { int s = i; while (gapq(gm, s)) s += m; w[i] = s; sw += s; if (s > M) M = s; }
    int d = e - 1, n[64], dd = 0;
    for (int j = 0; j < e; j++) if (gens[j] != m) n[dd++] = gens[j];
    int64_t c = F + 1, ell = c - g, W = (int64_t)e * ell - c;
    int64_t lhs = 2 * ((int64_t)d * m * M - (int64_t)(d + 1) * sw), rhs = 2 * m * W + (int64_t)(d - 1) * m * (m - 1);
    if (lhs != rhs) idfail++;
    int64_t R = 0;
    for (int i = 0; i < m; i++) for (int a = 0; a < d; a++) R += (M - w[i]) % n[a];
    int64_t need = (int64_t)(d - 1) * m * (m - 1);
    tot[g][e]++;
    double r = (double)(2 * R) / (double)need;
    if (!minr_set[e] || r < minr[e]) {
      minr[e] = r; minr_set[e] = 1;
      int p = snprintf(ex[e], 256, "m=%d c=%lld W=%lld gens=", m, (long long)c, (long long)W);
      for (int a = 0; a < d && p < 230; a++) p += snprintf(ex[e] + p, 256 - p, "%d,", n[a]);
    }
    int q = (int)((c + m - 1) / m), cls = q <= 3 ? 0 : (q == 4 ? 1 : 2);
    /* B_chain = sum_a sum_w (M - top_a(w)), Apery chains along n_a */
    int64_t Bc = 0;
    for (int a = 0; a < d; a++) for (int i = 0; i < m; i++) {
      int64_t t = w[i];
      for (;;) { int64_t t2 = t + n[a]; if (t2 > M) break; if (w[t2 % m] != t2) break; t = t2; }
      Bc += M - t;
    }
    double rc = (double)(2 * Bc) / (double)need;
    if (!minc_set[cls][e] || rc < minc[cls][e]) { minc[cls][e] = rc; minc_set[cls][e] = 1;
      int p2 = snprintf(exc[cls][e], 256, "m=%d c=%lld W=%lld gens=", m, (long long)c, (long long)W);
      for (int a = 0; a < d && p2 < 230; a++) p2 += snprintf(exc[cls][e] + p2, 256 - p2, "%d,", n[a]); }
    if (2 * Bc < need) { cfq[cls][e]++; if (nshowc < 30) { nshowc++; printf("CHAINFAIL g=%d m=%d c=%lld q=%d e=%d W=%lld ratio=%.4f gens=", g, m, (long long)c, q, e, (long long)W, rc); for (int a = 0; a < d; a++) printf("%d,", n[a]); printf("\n"); } }
    tq[cls][e]++;
    if (2 * R < need) {
      fail[g][e]++; fq[cls][e]++;
      if (cls == 1 && 3 * e < m) { static int n4 = 0; if (n4++ < 60) { printf("FAILq4_3e<m g=%d m=%d c=%lld e=%d W=%lld 2R/need=%.4f gens=", g, m, (long long)c, e, (long long)W, r); for (int a = 0; a < d; a++) printf("%d,", n[a]); printf("\n"); } }
      if (cls == 2 && nshow < 40) { nshow++; printf("FAILq5 g=%d m=%d c=%lld q=%d e=%d W=%lld 2R/need=%.4f gens=", g, m, (long long)c, q, e, (long long)W, r);
        for (int a = 0; a < d; a++) printf("%d,", n[a]); printf("\n"); }
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
      int y = nn + m, dec = 0;
      for (int a = m; a <= y / 2 && !dec; a++) if (a != nn && !gapq(gm2, a) && (y - a) != nn && !gapq(gm2, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, nn, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); if (G > 60) return 1;
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("identity failures: %llu\n", (unsigned long long)idfail);
  printf("g: RC failures by e (e=3..)\n");
  for (int g = 0; g <= G; g++) {
    printf("%d %llu:", g, (unsigned long long)cnt[g]);
    for (int e = 3; e < 64; e++) if (tot[g][e]) printf(" e%d:%llu/%llu", e, (unsigned long long)fail[g][e], (unsigned long long)tot[g][e]);
    printf("\n");
  }
  for (int k = 0; k < 3; k++) { printf("depth class %s:", k == 0 ? "q<=3" : (k == 1 ? "q=4" : "q>=5"));
    for (int e = 3; e < 64; e++) if (tq[k][e]) printf(" e%d:%llu/%llu", e, (unsigned long long)fq[k][e], (unsigned long long)tq[k][e]); printf("\n"); }
  for (int k = 0; k < 3; k++) { printf("CHAIN depth class %s failures:", k == 0 ? "q<=3" : (k == 1 ? "q=4" : "q>=5"));
    for (int e = 3; e < 64; e++) if (tq[k][e]) printf(" e%d:%llu", e, (unsigned long long)cfq[k][e]); printf("\n");
    for (int e = 3; e < 64; e++) if (minc_set[k][e]) printf("   e=%d min 2Bc/need=%.4f at %s\n", e, minc[k][e], exc[k][e]); }
  for (int e = 3; e < 64; e++) if (minr_set[e]) printf("e=%d min 2R/need = %.4f at %s\n", e, minr[e], ex[e]);
  return 0;
}
