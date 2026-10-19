/* Yang-Zhang (preprints.org 202604.0551) vs LAYER-KNESER, exhaustive over the semigroup tree (genus <= G).
 * c = qm - rho, Theta_t = #{1<=i<m : tm+i in S}, Theta_{t,rho} = same with i <= m-rho-1, eta = Theta_1, eta_rho = Theta_{1,rho}.
 * (YZ-EX)  ell = q + sum_{t=1}^{q-2} Theta_t + Theta_{q-1,rho}                       [YZ Prop 2.4 / 5.2]
 * (YZ-3.1) ell >= q + (q-2) eta + eta_rho                                           [YZ Prop 3.1]
 * (LAST)   Theta_{q-1,rho} = Theta_{q-1} - rho
 * (LKYZ)   if eta >= 1, gcd(m,B) = 1: ell >= q + (q-2)eta + delta*floor((q-3)^2/4) + max(eta_rho, eta + delta*floor((q-2)/2) - rho)
 * coverage outside LIT (c <= 3m or 3e >= m or m <= 18): YZ42 = e(eta+2) >= 2m (q >= 4), LK = e*LKbound >= c, LKYZ = e*LKYZ >= c.
 * gcc -O3 -std=gnu11 yz_check.c -o yz_check */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G;
static uint64_t cnt[80], exfail, yzfail, lastfail, lkyzfail, cov_yz[80], cov_lk[80], cov_lkyz[80], cov_any[80], open_[80], lkyz_only[80];
static int64_t minsl = INT64_MAX;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int isprime(int n) { if (n < 2) return 0; for (int p = 2; p * p <= n; p++) if (n % p == 0) return 0; return 1; }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt[g]++;
  int c = F + 1;
  if (c > m && m >= 2) {
    int q = (c + m - 1) / m, rho = q * m - c, k = 0, gb = m;
    for (int s = m + 1; s < 2 * m; s++) if (!gapq(gm, s)) { k++; gb = gcd(gb, s - m); }
    int64_t ell = c - g;
    int Th[64], Thr[64];
    for (int t = 0; t <= q; t++) { int a = 0, b = 0; for (int i = 1; i < m; i++) if (!gapq(gm, t * m + i)) { a++; if (i <= m - rho - 1) b++; } Th[t] = a; Thr[t] = b; }
    int64_t ex = q; for (int t = 1; t <= q - 2; t++) ex += Th[t]; ex += Thr[q - 1];
    if (ex != ell) { exfail++; if (exfail <= 3) fprintf(stderr, "EX FAIL m=%d c=%d\n", m, c); }
    int64_t yz = q + (int64_t)(q - 2) * k + Thr[1];
    if (q >= 2 && ell < yz) { yzfail++; if (yzfail <= 3) fprintf(stderr, "YZ FAIL m=%d c=%d\n", m, c); }
    if (Thr[q - 1] != Th[q - 1] - rho) { lastfail++; if (lastfail <= 3) fprintf(stderr, "LAST FAIL m=%d c=%d\n", m, c); }
    int lit = (c <= 3 * m) || (3 * e >= m) || (m <= 18);
    int cyz = q >= 4 && (int64_t)e * (k + 2) >= 2 * m;
    int clk = 0, clkyz = 0;
    if (k >= 1 && gb == 1) {
      int delta = isprime(m) ? k : (k + 2) / 2;
      int64_t LB = q + (int64_t)k * (q - 2) + (int64_t)delta * (((q - 3) * (q - 3)) / 4);
      int64_t last = Thr[1]; int64_t alt = k + (int64_t)delta * ((q - 2) / 2) - rho; if (alt > last) last = alt;
      int64_t LB2 = q + (int64_t)k * (q - 2) + (int64_t)delta * (((q - 3) * (q - 3)) / 4) + last;
      if (q >= 3 && ell < LB2) { lkyzfail++; if (lkyzfail <= 3) fprintf(stderr, "LKYZ FAIL m=%d c=%d\n", m, c); }
      if (q >= 3 && ell - LB2 < minsl) minsl = ell - LB2;
      clk = (int64_t)e * LB >= c; clkyz = q >= 3 && (int64_t)e * LB2 >= c;
    }
    if (!lit) { open_[g]++; cov_yz[g] += cyz; cov_lk[g] += clk; cov_lkyz[g] += clkyz; cov_any[g] += cyz || clkyz; lkyz_only[g] += clkyz && !cyz; }
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
  printf("g,count,outside_LIT,YZ4.2,LK,LKYZ,YZ_or_LKYZ,LKYZ_not_YZ\n");
  for (int g = 0; g <= G; g++) printf("%d,%llu,%llu,%llu,%llu,%llu,%llu,%llu\n", g, (unsigned long long)cnt[g], (unsigned long long)open_[g],
    (unsigned long long)cov_yz[g], (unsigned long long)cov_lk[g], (unsigned long long)cov_lkyz[g], (unsigned long long)cov_any[g], (unsigned long long)lkyz_only[g]);
  printf("YZ_exact_failures=%llu YZ31_failures=%llu last_identity_failures=%llu LKYZ_failures=%llu min(ell-LKYZ)=%lld\n",
    (unsigned long long)exfail, (unsigned long long)yzfail, (unsigned long long)lastfail, (unsigned long long)lkyzfail, (long long)minsl);
  return 0;
}
