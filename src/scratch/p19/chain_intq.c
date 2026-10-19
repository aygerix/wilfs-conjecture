/* CHAIN on level-k interval semigroups by depth q (lead, 2026-10-19): S = <m, km+a..km+a+L-1>.
 * For each q: min B_chain/need and the e/m of the minimizer, over m in [mlo, mhi], k in [1, KMAX]. Do CHAIN failures
 * persist at small e/m (large q)?  gcc -O3 -std=gnu11 chain_intq.c -o chain_intq ; ./chain_intq mlo mhi KMAX */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int m; static int64_t w[1024];
static void apery(int64_t *g, int k) {
  int done[1024]; for (int i = 0; i < m; i++) { w[i] = INT64_MAX; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++) { int u = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] != INT64_MAX && (u < 0 || w[i] < w[u])) u = i;
    if (u < 0) break; done[u] = 1;
    for (int j = 0; j < k; j++) { int v = (int)((u + g[j]) % m); if (w[u] + g[j] < w[v]) w[v] = w[u] + g[j]; } }
}
int main(int argc, char **argv) {
  int mlo = atoi(argv[1]), mhi = atoi(argv[2]), KMAX = atoi(argv[3]);
  double qmin[40]; char qex[40][160]; long qf[40]; for (int q = 0; q < 40; q++) { qmin[q] = 1e18; qf[q] = 0; qex[q][0] = 0; }
  for (m = mlo; m <= mhi; m++) for (int k = 1; k <= KMAX; k++) for (int a = 1; a < m; a++) for (int L = 2; a + L - 1 < m; L++) {
    int64_t g[1024]; for (int i = 0; i < L; i++) g[i] = (int64_t)k * m + a + i;
    apery(g, L);
    int bad = 0; for (int i = 0; i < m; i++) if (w[i] == INT64_MAX) bad = 1; if (bad) continue;
    int64_t n[1024]; int d = 0;
    for (int j = 0; j < L; j++) { int r = (int)(g[j] % m); if (w[r] != g[j]) continue; int dec = 0;
      for (int i = 1; i < m && !dec; i++) { int r2 = (r - i + m) % m; if (r2 && w[i] + w[r2] == g[j]) dec = 1; }
      if (!dec) n[d++] = g[j]; }
    if (d < 2) continue;
    int64_t M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
    int q = (int)((M - m + 1 + m - 1) / m); if (q >= 40) q = 39;
    int64_t Bc = 0;
    for (int aa = 0; aa < d; aa++) for (int i = 0; i < m; i++) { int64_t t = w[i];
      for (;;) { int64_t t2 = t + n[aa]; if (t2 > M) break; if (w[t2 % m] != t2) break; t = t2; } Bc += M - t; }
    double cr = (double)Bc / ((double)(d - 1) * m * (m - 1) / 2);
    if (cr < 1) qf[q]++;
    if (cr < qmin[q]) { qmin[q] = cr; snprintf(qex[q], 160, "m=%d k=%d a=%d L=%d e=%d e/m=%.3f M>=3n1:%d", m, k, a, L, d + 1, (double)(d + 1) / m, M >= 3 * n[0]); }
  }
  for (int q = 2; q < 40; q++) if (qmin[q] < 1e17) printf("q=%d: min ratio %.4f at %s; failures %ld\n", q, qmin[q], qex[q], qf[q]);
  return 0;
}
