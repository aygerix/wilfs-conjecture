/* Coverage of pure-P18 depth-four semigroups S = <m, m+A*> by proved criteria (lead, 2026-10-20).
 * Criteria: (1) c <= 3m+e [Lean DepthFour]; (2) 3e >= m [Eliahou]; (3) e(eta+2) >= 2m [YZ Cor 4.2, eta = k];
 * (4) 3 n_1 >= c + m [Lean LargeSecondGen]; (5) 12 a <= e s_2 [P9 PAIR-SPAN12, a = beta/gcd(A*)]; (6) NO-WRAP [Lean];
 * (7) Lam + Z >= h - e [DEPTH4-EH]; (8) genus <= 100 or m <= 18 [computation].
 * mode 1: all k-subsets A* of [1, m-1]; mode 0: random.  usage: ./p18cov mode mlo mhi klo khi samples seed */
#include <stdio.h>
#include <stdlib.h>
#define MM 1200
static int m, k, A[64], w[MM], lev[MM], nu[64][MM], ord[MM];
static unsigned long long rs; static unsigned rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static int cmpw(const void *x, const void *y){ return w[*(int*)x] - w[*(int*)y]; }
static int USEFIN = 0; static long tot, unc, cnt[9]; static double minratio = 1e9;
static int gcd(int a, int b){ while (b){ int t = a % b; a = b; b = t; } return a; }
static void eval(void){
  /* Dijkstra on residues with weights m + A[i]; also track number of generators used (for NO-WRAP) */
  static int done[MM]; for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; lev[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return; done[b] = 1;
    for (int a = 0; a < k; a++){ int j = (b + m + A[a]) % m, v = w[b] + m + A[a]; if (w[j] < 0 || v < w[j]){ w[j] = v; lev[j] = lev[b] + 1; } } }
  int g0 = 0; for (int a = 0; a < k; a++) g0 = gcd(g0, A[a]); if (gcd(g0, m) != 1) return;
  /* minimal generators: all m + A[a] are minimal (they are < 2m); e = k + 1 */
  int e = k + 1; long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long c = M - m + 1; int q = (int)((c + m - 1) / m); if (q != 4) return;
  long h = c - 3L * m, rho = m - h, ell = c - g, W = (long)e * ell - c;
  tot++;
  int ok[9] = {0};
  ok[1] = (c <= 3L * m + e); ok[2] = (3 * e >= m); ok[3] = ((long)e * (k + 2) >= 2L * m);
  int amin = A[0], amax = A[0]; for (int a = 0; a < k; a++){ if (A[a] < amin) amin = A[a]; if (A[a] > amax) amax = A[a]; }
  ok[4] = (3L * (m + amin) >= c + m);
  { static char in2[2 * MM]; for (int t = 0; t < 2 * m; t++) in2[t] = 0; in2[0] = 1;
    for (int a = 0; a < k; a++){ in2[A[a]] = 1; for (int b = a; b < k; b++) in2[A[a] + A[b]] = 1; }
    int s2 = 0; for (int t = 0; t < m; t++) s2 += in2[t];
    long aa = amax / g0; ok[5] = (12 * aa <= (long)e * s2); }
  { int nw = 1; for (int i = 0; i < m; i++) if (w[i] - lev[i] * m != i) { nw = 0; break; } ok[6] = nw; }
  { for (int i = 0; i < m; i++) ord[i] = i; qsort(ord, m, sizeof(int), cmpw);
    for (int a = 0; a < k; a++){ int r = (m + A[a]) % m; for (int t = 0; t < m; t++){ int i = ord[t], j = (i - r + m) % m; nu[a][i] = (w[j] + m + A[a] == w[i]) ? nu[a][j] + 1 : 0; } }
    long Lam = 0, Z = 0;
    for (int i = 0; i < m; i++){ long x = w[i], lam = (M - x) / m, K = 4 - lam;
      for (int a = 0; a < k; a++){ long n = m + A[a]; if (nu[a][i]) K -= nu[a][i] * ((M - (x - n)) / m - lam);
        int j = (i + (int)(n % m)) % m; if (w[j] != x + n) Lam += (nu[a][i] + 1) * lam; }
      if (K < 0) Z -= K; }
    ok[7] = (Lam + Z >= h - e); }
  ok[8] = USEFIN && (g <= 100 || m <= 18);
  int any = 0; for (int t = 1; t <= 8; t++) if (ok[t]){ any = 1; cnt[t]++; }
  if (W < 0) printf("WILF FAIL m=%d\n", m);
  if (!any){ unc++; double ratio = (double)e * ell / c; if (ratio < minratio) minratio = ratio;
    if (unc <= 12 || ratio <= minratio){ printf("UNCOVERED m=%d k=%d c=%ld h=%ld g=%ld ell=%ld W=%ld ratio=%.4f A*=", m, k, c, h, g, ell, W, ratio); for (int a = 0; a < k; a++) printf("%d,", A[a]); printf("\n"); fflush(stdout); } }
}
static int cur[64];
static void rec(int pos, int start){ if (pos == k){ for (int a = 0; a < k; a++) A[a] = cur[a]; eval(); return; } for (int b = start; b < m; b++){ cur[pos] = b; rec(pos + 1, b + 1); } }
int main(int argc, char **argv){
  int mode = atoi(argv[1]), mlo = atoi(argv[2]), mhi = atoi(argv[3]), klo = atoi(argv[4]), khi = atoi(argv[5]); long samples = atol(argv[6]);
  rs = 88172645463325252ULL ^ (unsigned long long)atoi(argv[7]) * 2654435761ULL; if (argc > 8) USEFIN = atoi(argv[8]);
  for (m = mlo; m <= mhi; m++) for (k = klo; k <= khi && k < m; k++){
    if (mode == 1) rec(0, 1);
    else for (long s = 0; s < samples; s++){ for (int a = 0; a < k; a++){ int b, okb; do { b = 1 + rnd() % (m - 1); okb = 1; for (int j = 0; j < a; j++) if (A[j] == b) okb = 0; } while (!okb); A[a] = b; } eval(); }
  }
  printf("P18 depth-four S: %ld; uncovered: %ld (min ratio %.4f); covered by: c<=3m+e %ld, 3e>=m %ld, YZ %ld, LSG %ld, PS12 %ld, NOWRAP %ld, D4EH %ld, finite %ld\n",
    tot, unc, minratio, cnt[1], cnt[2], cnt[3], cnt[4], cnt[5], cnt[6], cnt[7], cnt[8]);
}
