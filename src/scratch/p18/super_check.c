/* LK-SUPER: for every band j >= 1, G_{H+j+1} - R_j subset G_H (mod m), R_j = {r : jm + r in S}, u_j = |R_j|.
 * Step: if gcd(m, R_j) = 1 and u_j >= 2: g_{t-j-1} >= g_t + delta_j for j+1 <= t <= q-1, delta_j = u_j - 1 (m prime) or ceil(u_j/2).
 * Bound (prime m, any j): Theta_t >= floor((t+1)/(j+1)) * Theta_j (t <= q-1); ell >= q + sum_{t=1}^{q-2} Theta_t + Theta_{q-1} - rho.
 * Coverage (k = |S cap (m,2m)| = 0, outside LIT): SUPER = e * [q + sum_t max_j floor((t+1)/(j+1)) Theta_j_lower + max(0, ...)] >= c,
 *   using only Theta_j for j <= J0 (structural: first nonempty band).
 * gcc -O3 -std=gnu11 super_check.c -o super_check */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G;
static uint64_t cnt[80], stepfail, stepchk, k0[80], k0deep[80], cov_super[80], open_[80];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int isprime(int n) { if (n < 2) return 0; for (int p = 2; p * p <= n; p++) if (n % p == 0) return 0; return 1; }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt[g]++;
  int c = F + 1;
  if (c > m && m >= 2) {
    int q = (c + m - 1) / m, rho = q * m - c, pr = isprime(m);
    int gh[64], uj[64], gj[64];
    for (int H = 0; H <= q; H++) { int t = 0, gg = m; for (int r = 0; r < m; r++) { if (gapq(gm, H * m + r)) t++; else if (r > 0) gg = gcd(gg, r); } gh[H] = t; uj[H] = m - t; gj[H] = gg; }
    for (int j = 1; j <= q - 2; j++) {
      if (uj[j] < 2 || gcd(gj[j], m) != 1) continue;
      int delta = pr ? uj[j] - 1 : (uj[j] + 1) / 2;
      for (int t = j + 1; t <= q - 1; t++) { stepchk++; if (gh[t - j - 1] < gh[t] + delta) { stepfail++; if (stepfail <= 3) fprintf(stderr, "STEP FAIL m=%d c=%d j=%d t=%d\n", m, c, j, t); } }
    }
    int k = uj[1] - 1;
    int lit = (c <= 3 * m) || (3 * e >= m) || (m <= 18);
    if (k == 0 && pr) {
      k0[g]++;
      /* structural bound from the first nonempty band j0 only */
      int j0 = 0; for (int j = 1; j <= q - 1; j++) if (uj[j] >= 2) { j0 = j; break; }
      if (j0 && j0 <= q - 2) {
        int64_t Th = uj[j0] - 1, L = q;
        for (int t = 1; t <= q - 2; t++) L += (int64_t)((t + 1) / (j0 + 1)) * Th;
        int64_t last = (int64_t)((q) / (j0 + 1)) * Th - rho; if (last > 0) L += last;
        if (L > c - g) fprintf(stderr, "BOUND FAIL m=%d c=%d\n", m, c);
        if (!lit) { open_[g]++; if ((int64_t)e * L >= c) cov_super[g]++; }
        if (q >= 4) k0deep[g]++;
      }
    }
  }

  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int n = gens[j]; if (n <= F) continue;
    u128 gm2 = gm | ((u128)1 << n);
    int e2 = 0, m2;
    if (n == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else {
      m2 = m;
      for (int k = 0; k < e; k++) if (gens[k] != n) ng[e2++] = gens[k];
      int y = n + m, dec = 0;
      for (int a = m; a <= y / 2 && !dec; a++) if (a != n && !gapq(gm2, a) && (y - a) != n && !gapq(gm2, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, n, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); if (G > 60) return 1;
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("g,count,k0_prime_m,k0_q>=4,k0_outside_LIT,SUPER_covers\n");
  for (int g = 0; g <= G; g++) printf("%d,%llu,%llu,%llu,%llu,%llu\n", g, (unsigned long long)cnt[g], (unsigned long long)k0[g], (unsigned long long)k0deep[g], (unsigned long long)open_[g], (unsigned long long)cov_super[g]);
  printf("step_checks=%llu step_failures=%llu\n", (unsigned long long)stepchk, (unsigned long long)stepfail);
  return 0;
}
