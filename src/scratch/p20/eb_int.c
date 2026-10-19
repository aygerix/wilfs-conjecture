/* Chain deficit vs trade compensation on interval semigroups <m, km+a..km+a+L-1> (lead, 2026-10-19).
 * ./eb_int mlo mhi KMAX : per m, CHAIN failures, CHAIN-TRADE failures, min (Bc+Ebeta)/need, and the minimum coverage
 * Ebeta/(need - Bc) over CHAIN failures (coverage >= 1 means the trade bound alone pays the whole chain deficit). */
#include <stdio.h>
#include <stdlib.h>
#include "ebeta_core.h"
static int m; static int64_t w[1024];
static void apery(int64_t *g, int k) {
  int done[1024]; for (int i = 0; i < m; i++) { w[i] = INT64_MAX; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++) { int u = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] != INT64_MAX && (u < 0 || w[i] < w[u])) u = i;
    if (u < 0) break; done[u] = 1;
    for (int j = 0; j < k; j++) { int v = (int)((u + g[j]) % m); if (w[u] + g[j] < w[v]) w[v] = w[u] + g[j]; } }
}
int main(int argc, char **argv) {
  int mlo = atoi(argv[1]), mhi = atoi(argv[2]), KMAX = atoi(argv[3]);
  long idf = 0;
  for (m = mlo; m <= mhi; m++) {
    long chf = 0, ctf = 0, cuf = 0; double ctmin = 1e18, cov = 1e18, cumin = 1e18, covu = 1e18; char uex[220] = ""; char ex[200] = "", cex[220] = "";
    for (int k = 1; k <= KMAX; k++) for (int a = 1; a < m; a++) for (int L = 2; a + L - 1 < m; L++) {
      int64_t g[1024]; for (int i = 0; i < L; i++) g[i] = (int64_t)k * m + a + i;
      apery(g, L); int bad = 0; for (int i = 0; i < m; i++) if (w[i] == INT64_MAX) bad = 1; if (bad) continue;
      int64_t n[1024]; int d = 0;
      for (int j = 0; j < L; j++) { int r = (int)(g[j] % m); if (w[r] != g[j]) continue; int dec = 0;
        for (int i = 1; i < m && !dec; i++) { int r2 = (r - i + m) % m; if (r2 && w[i] + w[r2] == g[j]) dec = 1; }
        if (!dec) n[d++] = g[j]; }
      if (d < 2) continue;
      EB r; if (!eb_compute(m, w, n, d, &r)) continue;
      if (r.E != r.B - r.Bc) idf++;
      double ct = (double)(r.Bc + r.Eb) / r.need;
      if (ct < ctmin) { ctmin = ct; snprintf(ex, 200, "k=%d a=%d L=%d e=%d", k, a, L, d + 1); }
      if (r.Bc + r.Eb < r.need) { ctf++; if (0) printf("CTFAIL m=%d k=%d a=%d L=%d e=%d Bc/need=%.4f Eb/need=%.4f E/need=%.4f\n", m, k, a, L, d + 1, (double)r.Bc / r.need, (double)r.Eb / r.need, (double)r.E / r.need); }
      { double cu = (double)(r.Bc + r.Eu) / r.need; if (cu < cumin) cumin = cu; if (r.Bc + r.Eu < r.need) { cuf++; if (cuf <= 3) printf("CUFAIL m=%d k=%d a=%d L=%d e=%d Bc/need=%.4f Eu/need=%.4f E/need=%.4f\n", m, k, a, L, d + 1, (double)r.Bc / r.need, (double)r.Eu / r.need, (double)r.E / r.need); }
        if (r.Bc < r.need) { double c = (double)r.Eu / (double)(r.need - r.Bc); if (c < covu) { covu = c; snprintf(uex, 220, "k=%d a=%d L=%d e=%d Bc/need=%.4f Eu/need=%.4f E/need=%.4f", k, a, L, d + 1, (double)r.Bc / r.need, (double)r.Eu / r.need, (double)r.E / r.need); } } }
      if (r.Bc < r.need) { chf++; double c = (double)r.Eb / (double)(r.need - r.Bc);
        if (c < cov) { cov = c; snprintf(cex, 220, "k=%d a=%d L=%d e=%d Bc/need=%.4f Eb/need=%.4f E/need=%.4f ntmin=%d bmin=%lld M=%lld", k, a, L, d + 1, (double)r.Bc / r.need, (double)r.Eb / r.need, (double)r.E / r.need, r.ntmin, (long long)r.bmin, (long long)r.M); } }
    }
    printf("m=%d CHAINfail=%ld TRADEfail=%ld UNIONfail=%ld min(Bc+Eb)/need=%.4f min(Bc+Eu)/need=%.4f | min Eu-coverage %.3f at %s\n", m, chf, ctf, cuf, ctmin, cumin, covu, uex); fflush(stdout);
  }
  printf("identity failures %ld\n", idf);
  return 0;
}
