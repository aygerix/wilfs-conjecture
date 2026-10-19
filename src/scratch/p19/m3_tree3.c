/* m3_tree3: m3_tree2 plus RCREST = d*sum_{w!=0} s_w - sum_{a,w!=0} ((M-w) mod n_a) (an upper bound for REST; RCREST<=0 => REST<=0).
 * m3_tree2: m3_tree plus REST = sum_{w != 0} con(w) (con(w) = sum_a (s_w - (M - top_a(w)))) and the SC weakening.
 * CHAIN-M3 over the semigroup tree (lead, 2026-10-19).  For every S of genus <= G with e >= 3:
 * B_chain = sum_{w in Ap, a} (M - top_a(w)), need = (d-1) m(m-1)/2, n1 = least generator > m, H = Apery height.
 * Class A: M >= 3 n1 (contains every S of height >= 3).  Reports CHAIN failures by (class, height) and minima.
 * gcc -O3 -std=gnu11 m3_tree.c -o m3_tree ; ./m3_tree G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static double rmax[2][2] = {{-9,-9},{-9,-9}}; static char rex[2][2][256]; static uint64_t rpos[2][2], scf[2][2];
static double c0max = -9; static char c0ex[256]; static uint64_t c0f, c0tie;
static uint64_t rcrpos[2][2]; static double rcrmax[2][2] = {{-9,-9},{-9,-9}}; static char rcrex[2][2][256];
static int G; static uint64_t cnt[80], tot[2][2], fl[2][2]; static double mn[2][2] = {{9,9},{9,9}}; static char ex[2][2][256];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt[g]++;
  if (F >= 1 && m >= 2 && e >= 3) {
    int w[128]; int64_t M = 0;
    for (int i = 0; i < m; i++) { int s = i; while (gapq(gm, s)) s += m; w[i] = s; if (s > M) M = s; }
    int d = e - 1, n[64], dd = 0, n1 = 1 << 30;
    for (int j = 0; j < e; j++) if (gens[j] != m) { n[dd++] = gens[j]; if (gens[j] < n1) n1 = gens[j]; }
    int64_t Bc = 0, rest = 0, Bsc = 0, rcr = 0; int64_t c0 = M - m + 1;
    for (int a = 0; a < d; a++) for (int i = 0; i < m; i++) { int64_t t = w[i];
      for (;;) { int64_t t2 = t + n[a]; if (t2 > M) break; if (w[t2 % m] != t2) break; t = t2; } Bc += M - t;
      if (i) { rest += (M - w[i]) % m - (M - t); rcr += (M - w[i]) % m - (M - w[i]) % n[a]; }
      Bsc += (t >= c0) ? (M - t) : m; }
    { int64_t con0 = 0, tops[64]; int tie = 0;
      for (int a = 0; a < d; a++) { int64_t t = 0; for (;;) { int64_t t2 = t + n[a]; if (t2 > M) break; if (w[t2 % m] != t2) break; t = t2; }
        tops[a] = t; con0 += M % m - (M - t); for (int b = 0; b < a; b++) if (tops[b] == t) tie = 1; }
      if (tie) c0tie++;
      double v = (double)con0 / ((double)m * (m - 1) / 2);
      if (v > 1.0 + 1e-12) { c0f++; if (c0f <= 10) { printf("CON0FAIL g=%d m=%d c=%d e=%d tie=%d con0/C2=%.4f gens=", g, m, F + 1, e, tie, v); for (int a = 0; a < d; a++) printf("%d,", n[a]); printf("\n"); } }
      if (v > c0max) { c0max = v; int p = snprintf(c0ex, 256, "g=%d m=%d c=%d e=%d tie=%d gens=", g, m, F + 1, e, tie); for (int a = 0; a < d && p < 230; a++) p += snprintf(c0ex + p, 256 - p, "%d,", n[a]); } }
    int64_t need = (int64_t)(d - 1) * m * (m - 1) / 2;
    int ord[128]; for (int i = 0; i < m; i++) ord[i] = i;
    for (int i = 1; i < m; i++) { int v = ord[i], j = i - 1; while (j >= 0 && w[ord[j]] > w[v]) { ord[j + 1] = ord[j]; j--; } ord[j + 1] = v; }
    int ml[128]; ml[0] = 0; int H = 0;
    for (int t = 1; t < m; t++) { int i = ord[t], best = 1 << 20;
      for (int a = 0; a < d; a++) { int y = w[i] - n[a]; if (y >= 0 && w[y % m] == y) { int v = 1 + ml[y % m]; if (v < best) best = v; } }
      ml[i] = best; if (best > H) H = best; }
    int A = M >= 3LL * n1, h3 = H >= 3;
    tot[A][h3]++;
    { int E3 = 3 * e < m; double rr = (double)rest / ((double)m * (m - 1) / 2);
      if (rest > 0) rpos[A][E3]++;
      { double v = (double)rcr / ((double)m * (m - 1) / 2); if (rcr > 0) rcrpos[A][E3]++;
        if (v > rcrmax[A][E3]) { rcrmax[A][E3] = v; int p = snprintf(rcrex[A][E3], 256, "g=%d m=%d c=%d e=%d REST/C2=%.4f gens=", g, m, F + 1, e, rr); for (int a = 0; a < d && p < 230; a++) p += snprintf(rcrex[A][E3] + p, 256 - p, "%d,", n[a]); } }
      if (rr > rmax[A][E3]) { rmax[A][E3] = rr; int p = snprintf(rex[A][E3], 256, "g=%d m=%d c=%d e=%d H=%d ratio=%.4f gens=", g, m, F + 1, e, H, (double)Bc / (double)((int64_t)(d - 1) * m * (m - 1) / 2));
        for (int a = 0; a < d && p < 230; a++) p += snprintf(rex[A][E3] + p, 256 - p, "%d,", n[a]); }
      if (Bsc < (int64_t)(d - 1) * m * (m - 1) / 2) scf[A][E3]++; }
    double r = (double)Bc / (double)need;
    if (r < mn[A][h3]) { mn[A][h3] = r; int p = snprintf(ex[A][h3], 256, "g=%d m=%d c=%d e=%d H=%d M=%lld n1=%d gens=", g, m, F + 1, e, H, (long long)M, n1);
      for (int a = 0; a < d && p < 230; a++) p += snprintf(ex[A][h3] + p, 256 - p, "%d,", n[a]); }
    if (Bc < need) { fl[A][h3]++; if (A) { printf("M3FAIL g=%d m=%d c=%d e=%d H=%d M=%lld n1=%d ratio=%.4f gens=", g, m, F + 1, e, H, (long long)M, n1, r); for (int a = 0; a < d; a++) printf("%d,", n[a]); printf("\n"); } }
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
  int gens[1] = {1}; visit(0, -1, 1, gens, 1, 0);
  for (int A = 0; A < 2; A++) for (int h = 0; h < 2; h++)
    printf("class M%s3n1, height%s: %llu semigroups, CHAIN failures %llu, min ratio %.5f at %s\n", A ? ">=" : "<", h ? ">=3" : "<=2",
      (unsigned long long)tot[A][h], (unsigned long long)fl[A][h], mn[A][h], ex[A][h]);
  printf("con(0)/C2: max %.5f at %s; con(0) > C2 failures %llu; semigroups with tied tops of 0: %llu\n", c0max, c0ex, (unsigned long long)c0f, (unsigned long long)c0tie);
  for (int A = 0; A < 2; A++) for (int E3 = 0; E3 < 2; E3++)
    printf("REST class M%s3n1, %s: max REST/C2 = %.4f (#REST>0: %llu; SC failures %llu) at %s\n", A ? ">=" : "<", E3 ? "3e<m" : "3e>=m",
      rmax[A][E3], (unsigned long long)rpos[A][E3], (unsigned long long)scf[A][E3], rex[A][E3]);
  for (int A = 0; A < 2; A++) for (int E3 = 0; E3 < 2; E3++)
    printf("RCREST class M%s3n1, %s: #RCREST>0 = %llu, max RCREST/C2 = %.4f at %s\n", A ? ">=" : "<", E3 ? "3e<m" : "3e>=m", (unsigned long long)rcrpos[A][E3], rcrmax[A][E3], rcrex[A][E3]);
  return 0;
}
