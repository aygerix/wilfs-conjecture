/* Chain deficit vs trade compensation over the semigroup tree (lead, 2026-10-19): ./eb_tree G
 * Tests CHAIN-TRADE: Bc + Ebeta >= need, and reports how much of the chain deficit Ebeta covers. */
#include <stdio.h>
#include <stdlib.h>
#include "ebeta_core.h"
typedef unsigned __int128 u128;
static uint64_t cuf, wpf, ppf, idl; static double cumin = 1e18, wpmax = -1e18, ppmax = -1e18; static char cuex[300], wpex[300], ppex[300];
static int G; static uint64_t tot, idf, chf, ctf; static double ctmin = 1e18, covmin = 1e18; static char ctex[300], covex[300];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  if (F >= 1 && m >= 2 && e >= 3) {
    int64_t w[128]; for (int i = 0; i < m; i++) { int s = i; while (gapq(gm, s)) s += m; w[i] = s; }
    int64_t n[64]; int d = 0; for (int j = 0; j < e; j++) if (gens[j] != m) n[d++] = gens[j];
    EB r; if (eb_compute(m, w, n, d, &r)) { tot++;
      if (r.E != r.B - r.Bc) idf++;
      double ct = (double)(r.Bc + r.Eb) / (double)r.need;
      if (ct < ctmin) { ctmin = ct; int p = snprintf(ctex, 300, "g=%d m=%d c=%d e=%d gens=", g, m, F + 1, e); for (int a = 0; a < d && p < 280; a++) p += snprintf(ctex + p, 300 - p, "%d,", (int)n[a]); }
      { double cu = (double)(r.Bc + r.Eu) / r.need; if (cu < cumin) { cumin = cu; int p = snprintf(cuex, 300, "g=%d m=%d c=%d e=%d gens=", g, m, F + 1, e); for (int a = 0; a < d && p < 280; a++) p += snprintf(cuex + p, 300 - p, "%d,", (int)n[a]); } if (r.Bc + r.Eu < r.need) cuf++; }
      { int64_t C2 = (int64_t)m * (m - 1) / 2; if (r.idlink) idl++;
        double wp = (double)(r.Wp - (int64_t)m * r.Ltop) / C2, pp = (double)(r.Ppoor - (int64_t)m * r.Ltop) / C2;
        if (wp > 1.0 + 1e-12) { wpf++; if (wpf <= 10) printf("WPFAIL g=%d m=%d c=%d e=%d wplus=%.4f\n", g, m, F + 1, e, wp); }
        if (pp > 1.0 + 1e-12) ppf++;
        if (wp > wpmax) { wpmax = wp; int p = snprintf(wpex, 300, "g=%d m=%d c=%d e=%d chain=%.4f gens=", g, m, F + 1, e, (double)r.Bc / r.need); for (int a = 0; a < d && p < 280; a++) p += snprintf(wpex + p, 300 - p, "%d,", (int)n[a]); }
        if (pp > ppmax) { ppmax = pp; int p = snprintf(ppex, 300, "g=%d m=%d c=%d e=%d gens=", g, m, F + 1, e); for (int a = 0; a < d && p < 280; a++) p += snprintf(ppex + p, 300 - p, "%d,", (int)n[a]); } }
      if (r.Bc + r.Eb < r.need) { ctf++; if (ctf <= 10) printf("CTFAIL %s\n", ctex); }
      if (r.Bc < r.need) { chf++; double cov = (double)r.Eb / (double)(r.need - r.Bc);
        if (cov < covmin) { covmin = cov; int p = snprintf(covex, 300, "g=%d m=%d c=%d e=%d Bc/need=%.4f Eb/need=%.4f E/need=%.4f gens=", g, m, F + 1, e, (double)r.Bc / r.need, (double)r.Eb / r.need, (double)r.E / r.need); for (int a = 0; a < d && p < 280; a++) p += snprintf(covex + p, 300 - p, "%d,", (int)n[a]); } } }
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
  printf("genus<=%d, e>=3: %llu S; identity E=B-Bc failures %llu; CHAIN failures %llu; CHAIN-TRADE (Bc+Ebeta>=need) failures %llu\n", G,
    (unsigned long long)tot, (unsigned long long)idf, (unsigned long long)chf, (unsigned long long)ctf);
  printf("  link-identity failures %llu; WILF+ failures %llu (max %.5f at %s); CHAIN-POOR failures %llu (max %.5f at %s)\n", (unsigned long long)idl, (unsigned long long)wpf, wpmax, wpex, (unsigned long long)ppf, ppmax, ppex);
  printf("  UNION (Bc+Eu>=need) failures %llu, min (Bc+Eu)/need = %.5f at %s\n", (unsigned long long)cuf, cumin, cuex);
  printf("  min (Bc+Ebeta)/need = %.5f at %s\n  min Ebeta/(need-Bc) over CHAIN failures = %.4f at %s\n", ctmin, ctex, covmin, covex);
  return 0;
}
