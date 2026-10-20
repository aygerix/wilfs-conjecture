/* P18 tightness landscape (lead, 2026-10-19).
 * S = <m, m+b_1..m+b_k>, B* random k-subset of [1,m-1] (or exhaustive for small m), gcd(m,B)=1.
 * Apery by Dijkstra on residues; W = e*ell - c; ratio = e*ell/c.  Record min ratio per (k, q), q = ceil(c/m).
 * usage: p18_ratio mode(0=random,1=exhaustive k-subsets) k mlo mhi samples seed */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int m; static long long w[4096]; static int gens[64], ng;
static void apery(void) {
  static char done[4096];
  for (int i = 0; i < m; i++) { w[i] = LLONG_MAX; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++) { int u = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] != LLONG_MAX && (u < 0 || w[i] < w[u])) u = i;
    if (u < 0) break; done[u] = 1;
    for (int j = 0; j < ng; j++) { int v = (int)((u + gens[j]) % m); if (w[u] + gens[j] < w[v]) w[v] = w[u] + gens[j]; } }
}
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static double best[64][64]; static char ex[64][64][256];
static uint64_t rs = 88172645463325252ULL; static uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static void eval(int k, int *B) {
  int g = m; for (int i = 0; i < k; i++) g = gcd(g, B[i]); if (g != 1) return;
  ng = k; for (int i = 0; i < k; i++) gens[i] = m + B[i];
  apery();
  long long M = 0, sum = 0; for (int i = 0; i < m; i++) { if (w[i] > M) M = w[i]; sum += w[i] / m; }
  long long c = M - m + 1, gg = sum, ell = c - gg; int e = k + 1;   /* all m+b in (m,2m) are minimal */
  int q = (int)((c + m - 1) / m); if (q > 63) q = 63;
  double r = (double)(e * ell) / (double)c;
  if (r < best[k][q]) { best[k][q] = r; int p = snprintf(ex[k][q], 256, "m=%d B*={", m); for (int i = 0; i < k; i++) p += snprintf(ex[k][q] + p, 256 - p, "%d%s", B[i], i + 1 < k ? "," : "}"); snprintf(ex[k][q] + p, 256 - p, " c=%lld ell=%lld W=%lld", c, ell, e * ell - c); }
}
int main(int argc, char **argv) {
  int mode = atoi(argv[1]), k = atoi(argv[2]), mlo = atoi(argv[3]), mhi = atoi(argv[4]); long long samples = atoll(argv[5]); rs ^= (uint64_t)atoll(argv[6]) * 2654435761ULL;
  for (int a = 0; a < 64; a++) for (int b = 0; b < 64; b++) best[a][b] = 1e18;
  int B[64];
  for (m = mlo; m <= mhi; m++) {
    if (mode == 1) { for (int i = 0; i < k; i++) B[i] = i + 1;
      for (;;) { eval(k, B); int i = k - 1; while (i >= 0 && B[i] == m - k + i) i--; if (i < 0) break; B[i]++; for (int j = i + 1; j < k; j++) B[j] = B[j - 1] + 1; } }
    else { for (long long s = 0; s < samples; s++) { int n = 0; while (n < k) { int x = 1 + (int)(rnd() % (uint64_t)(m - 1)), dup = 0; for (int j = 0; j < n; j++) if (B[j] == x) dup = 1; if (!dup) B[n++] = x; }
        for (int i = 1; i < k; i++) { int v = B[i], j = i - 1; while (j >= 0 && B[j] > v) { B[j + 1] = B[j]; j--; } B[j + 1] = v; } eval(k, B); } }
  }
  for (int q = 1; q < 64; q++) if (best[k][q] < 1e17) printf("k=%d q=%d min e*ell/c = %.5f  at %s\n", k, q, best[k][q], ex[k][q]);
  return 0;
}
