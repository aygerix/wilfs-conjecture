/* theta_flow: theta_tree plus a local flow test: each deficient v sends (c - m Theta(v)) / |LC(v)| to each lower cover
 * u = v - n_a in Ap; FLOW holds if every u has m Theta(u) - c >= received (exact rational test).  Also FLOW2: send to lower
 * covers in proportion to their surplus is always feasible iff the total cover surplus >= deficit (per v, overlaps ignored).
 * Local form of Wilf (lead, 2026-10-19): Theta(v) = lam(v) + L1(v) + sum_a lam(top_a(v)), L1(v) = sum_a depth_a(v)(lam(v-n_a) - lam(v)).
 * Identity: sum_{v in Ap} Theta(v) = (d+1) ell, so Wilf <=> sum_v (m Theta(v) - c) >= 0.  Local Wilf: m Theta(v) >= c for all v.
 * Reports: identity failures; fraction of S with a local deficit; the worst per-element deficit (c - m Theta)/m;
 * (L0) whether 0's surplus alone covers all deficits: sum_{v != 0} (c - m Theta(v))^+ <= m Theta(0) - c;
 * which elements are deficient (layer, generator or not).   ./theta_tree G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static uint64_t flowf, flow2f; static double flw = -1e9; static char exf[300];
static int G; static uint64_t tot, idf, ndef, l0f, defgen, defdec, deflay[8]; static double worst = -1e9, l0w = -1e9; static char exw[300], exl[300];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  if (F >= 1 && m >= 2 && e >= 3) {
    int64_t w[128], M = 0; for (int i = 0; i < m; i++) { int s = i; while (gapq(gm, s)) s += m; w[i] = s; if (s > M) M = s; }
    int64_t n[64]; int d = 0; for (int j = 0; j < e; j++) if (gens[j] != m) n[d++] = gens[j];
    #define INAP(v) ((v) >= 0 && (v) <= M && w[(v) % m] == (v))
    int64_t c = M - m + 1, ell = 0, sumT = 0, th0 = 0, defsum = 0; int anydef = 0; double wv = -1e9; int64_t wvv = 0; int64_t TH[128]; double recv[128] = {0};
    for (int i = 0; i < m; i++) if (w[i] < c) ell += (c - 1 - w[i]) / m + 1;
    for (int i = 0; i < m; i++) { int64_t v = w[i], th = (M - v) / m; int isgen = 0;
      for (int a = 0; a < d; a++) { if (n[a] == v) isgen = 1;
        int64_t y = v, dep = 0; while (INAP(y - n[a])) { y -= n[a]; dep++; } if (dep) th += dep * ((M - v + n[a]) / m - (M - v) / m);
        int64_t t = v; while (INAP(t + n[a])) t += n[a]; th += (M - t) / m; }
      sumT += th; if (v == 0) th0 = th; TH[i] = th;
      int64_t df = c - (int64_t)m * th;
      if (df > 0 && v != 0) { anydef = 1; defsum += df; int L = (int)((M - v) / m); if (L > 7) L = 7; deflay[L]++; if (isgen) defgen++; else defdec++;
        double q = (double)df / m; if (q > wv) { wv = q; wvv = v; } } }
    { int bad2 = 0;
      for (int i = 0; i < m; i++) { int64_t v = w[i], df = c - (int64_t)m * TH[i]; if (df <= 0 || v == 0) continue;
        int nlc = 0; int64_t sur = 0; for (int a = 0; a < d; a++) if (INAP(v - n[a])) { nlc++; int r = (int)((v - n[a]) % m); int64_t su = (int64_t)m * TH[r] - c; if (su > 0) sur += su; }
        if (sur < df) bad2 = 1;
        for (int a = 0; a < d; a++) if (INAP(v - n[a])) recv[(v - n[a]) % m] += (double)df / nlc; }
      int badf = 0; double wf = -1e9; for (int i = 0; i < m; i++) { double ex = recv[i] - (double)((int64_t)m * TH[i] - c); if (ex > 1e-9) { badf = 1; if (ex / m > wf) wf = ex / m; } }
      if (badf) { flowf++; if (wf > flw) { flw = wf; int p = snprintf(exf, 300, "g=%d m=%d c=%lld e=%d over/m=%.3f gens=", g, m, (long long)c, e, wf); for (int a = 0; a < d && p < 280; a++) p += snprintf(exf + p, 300 - p, "%d,", (int)n[a]); } }
      if (bad2) flow2f++; }
    #undef INAP
    tot++; if (sumT != (int64_t)(d + 1) * ell) idf++;
    if (anydef) { ndef++; if (wv > worst) { worst = wv; int p = snprintf(exw, 300, "g=%d m=%d c=%lld e=%d v=%lld deficit/m=%.3f gens=", g, m, (long long)c, e, (long long)wvv, wv); for (int a = 0; a < d && p < 280; a++) p += snprintf(exw + p, 300 - p, "%d,", (int)n[a]); } }
    int64_t sur0 = (int64_t)m * th0 - c; if (defsum > sur0) { l0f++; double q = (double)(defsum - sur0) / ((double)m * m); if (q > l0w) { l0w = q; int p = snprintf(exl, 300, "g=%d m=%d c=%lld e=%d gens=", g, m, (long long)c, e); for (int a = 0; a < d && p < 280; a++) p += snprintf(exl + p, 300 - p, "%d,", (int)n[a]); } }
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
  printf("genus<=%d e>=3: %llu S; identity sum Theta = (d+1) ell failures: %llu\n", G, (unsigned long long)tot, (unsigned long long)idf);
  printf("S with a local deficit (some v != 0 with m Theta(v) < c): %llu; worst deficit/m %.3f at %s\n", (unsigned long long)ndef, worst, exw);
  printf("deficient elements: generators %llu, decomposable %llu; by layer:", (unsigned long long)defgen, (unsigned long long)defdec);
  for (int L = 0; L < 8; L++) printf(" %d:%llu", L, (unsigned long long)deflay[L]); printf("\n");
  printf("(L0) 0's surplus covers all deficits fails in %llu S; worst (deficit - surplus)/m^2 %.4f at %s\n", (unsigned long long)l0f, l0w, exl);
  printf("FLOW (equal split to lower covers) fails in %llu S; worst overload/m %.3f at %s\n", (unsigned long long)flowf, flw, exf);
  printf("FLOW2 (per v: total positive surplus of its lower covers >= its deficit) fails in %llu S\n", (unsigned long long)flow2f);
  return 0;
}
