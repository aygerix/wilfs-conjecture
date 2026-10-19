/* REST-M3 on interval semigroups (lead, 2026-10-19): S = <m, km+a, km+a+1, ..., km+a+L-1>, k in [1,KMAX].
 * For each m: max REST/C2 over members of class A = {M >= 3 n1}, the argmax, and any REST > 0 (printed).
 * gcc -O3 -std=gnu11 rest_int.c -o rest_int ; ./rest_int mlo mhi KMAX */
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
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
int main(int argc, char **argv) {
  int mlo = atoi(argv[1]), mhi = atoi(argv[2]), KMAX = atoi(argv[3]);
  for (m = mlo; m <= mhi; m++) {
    double best = -1e18; char bex[200] = ""; long npos = 0, nA = 0;
    for (int k = 1; k <= KMAX; k++) for (int a = 1; a < m; a++) for (int L = 2; a + L - 1 < m; L++) {
      int64_t g[1024]; int gg = m; for (int i = 0; i < L; i++) { g[i] = (int64_t)k * m + a + i; gg = gcd(gg, (int)(g[i] % m)); }
      if (gcd(gg, m) != 1 && L == 1) continue;
      apery(g, L);
      int bad = 0; for (int i = 0; i < m; i++) if (w[i] == INT64_MAX) bad = 1; if (bad) continue;
      int64_t n[1024]; int d = 0;
      for (int j = 0; j < L; j++) { int r = (int)(g[j] % m); if (w[r] != g[j]) continue; int dec = 0;
        for (int i = 1; i < m && !dec; i++) { int r2 = (r - i + m) % m; if (r2 && w[i] + w[r2] == g[j]) dec = 1; }
        if (!dec) n[d++] = g[j]; }
      if (d < 2) continue;
      int64_t M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
      if (M < 3 * n[0]) continue;
      nA++;
      int64_t rest = 0;
      for (int aa = 0; aa < d; aa++) for (int i = 1; i < m; i++) { int64_t t = w[i];
        for (;;) { int64_t t2 = t + n[aa]; if (t2 > M) break; if (w[t2 % m] != t2) break; t = t2; }
        rest += (M - w[i]) % m - (M - t); }
      double rr = (double)rest / ((double)m * (m - 1) / 2);
      if (rest > 0) { npos++; if (npos <= 5) printf("RESTPOS m=%d k=%d a=%d L=%d e=%d M=%lld REST/C2=%.4f\n", m, k, a, L, d + 1, (long long)M, rr); }
      if (rr > best) { best = rr; snprintf(bex, 200, "k=%d a=%d L=%d e=%d M=%lld q=%lld", k, a, L, d + 1, (long long)M, (long long)((M - m + 1 + m - 1) / m)); }
    }
    printf("m=%d classA=%ld REST>0: %ld  max REST/C2 = %.4f at %s\n", m, nA, npos, best, bex); fflush(stdout);
  }
  return 0;
}
