/* C1 test on <m, m+B>, B subset of [1, m-1] (lead, 2026-10-20). At q = 4 checks
 *   (C1) R <= rho + L2,  L2 = sum_{y in Ap, y < c} tau(y) + sum_v (lam(v) + |U(v)| - 4)^+,
 *   (C2) R <= rho + sum_{y<c} tau(y) + Z,   and Wilf (C3).  mode 0: random B of size k (seeded); mode 1: all k-subsets.
 *   usage: ./c1fam mode mlo mhi klo khi samples seed */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MM 1200
static int m, d, gen[64], w[MM], nu[64][MM], minimal[64], ord[MM];
static unsigned long long rs; static unsigned rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static int cmpw(const void *x, const void *y){ return w[*(int*)x] - w[*(int*)y]; }
static long tot, f1, f2, f3; static long min1 = 1L << 40, min2 = 1L << 40;
static int apery(void){
  static int done[MM]; for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return 0; done[b] = 1;
    for (int a = 0; a < d; a++){ int j = (b + gen[a]) % m, v = w[b] + gen[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
  return 1;
}
static void eval(void){
  if (!apery()) return;
  int e = 1;
  for (int a = 0; a < d; a++){ int rr = gen[a] % m; minimal[a] = (w[rr] == gen[a]);
    if (minimal[a]) for (int i = 1; i < m; i++){ int j = (rr - i + m) % m; if (j && w[i] + w[j] == gen[a]){ minimal[a] = 0; break; } }
    e += minimal[a]; }
  long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long c = M - m + 1; int q = (int)((c + m - 1) / m); if (q != 4) return;
  long rho = 4L * m - c, W = (long)e * (c - g) - c;
  for (int i = 0; i < m; i++) ord[i] = i; qsort(ord, m, sizeof(int), cmpw);
  for (int a = 0; a < d; a++) if (minimal[a]){ int rr = gen[a] % m;
    for (int t = 0; t < m; t++){ int i = ord[t], j = (i - rr + m) % m; nu[a][i] = (w[j] + gen[a] == w[i]) ? nu[a][j] + 1 : 0; } }
  long tau = 0, ex = 0, Z = 0, R = 0, Lam = 0;
  for (int i = 0; i < m; i++){ long x = w[i], lam = (M - x) / m, K = 4 - lam; int U = 0, t = 0;
    for (int a = 0; a < d; a++) if (minimal[a]){
      if (nu[a][i]){ U++; K -= nu[a][i] * ((M - (x - gen[a])) / m - lam); }
      int j = (i + gen[a]) % m; if (w[j] != x + gen[a]){ t++; Lam += (nu[a][i] + 1) * lam; } }
    if (x < c) tau += t; if (lam + U - 4 > 0) ex += lam + U - 4; if (K < 0) Z -= K; if (K == 1) R++; }
  tot++;
  long s1 = rho + tau + ex - R, s2 = rho + tau + Z - R;
  if (s1 < 0){ f1++; if (f1 <= 5){ printf("C1FAIL slack=%ld m=%d e=%d rho=%ld R=%ld tau=%ld ex=%ld Z=%ld Lam=%ld W=%ld B=", s1, m, e, rho, R, tau, ex, Z, Lam, W); for (int a = 0; a < d; a++) printf("%d,", gen[a] - m); printf("\n"); } }
  if (s2 < 0) f2++; if (W < 0) f3++;
  if (s1 < min1){ min1 = s1; printf("minC1 slack=%ld m=%d e=%d rho=%ld R=%ld tau=%ld ex=%ld Z=%ld Lam=%ld W=%ld B=", s1, m, e, rho, R, tau, ex, Z, Lam, W); for (int a = 0; a < d; a++) printf("%d,", gen[a] - m); printf("\n"); fflush(stdout); }
}
static int cur[64];
static void rec(int pos, int start, int k){
  if (pos == k){ d = k; for (int a = 0; a < k; a++) gen[a] = m + cur[a]; eval(); return; }
  for (int b = start; b < m; b++){ cur[pos] = b; rec(pos + 1, b + 1, k); }
}
int main(int argc, char **argv){
  int mode = atoi(argv[1]), mlo = atoi(argv[2]), mhi = atoi(argv[3]), klo = atoi(argv[4]), khi = atoi(argv[5]); long samples = atol(argv[6]);
  rs = 88172645463325252ULL ^ (unsigned long long)atoi(argv[7]) * 2654435761ULL;
  for (m = mlo; m <= mhi; m++) for (int k = klo; k <= khi && k < m; k++){
    if (mode == 1) rec(0, 1, k);
    else for (long s = 0; s < samples; s++){ d = k; for (int a = 0; a < k; a++){ int b, ok; do { b = 1 + rnd() % (m - 1); ok = 1; for (int j = 0; j < a; j++) if (gen[j] == m + b) ok = 0; } while (!ok); gen[a] = m + b; } eval(); }
  }
  printf("q=4 S tested %ld; C1 fails %ld, C2 fails %ld, Wilf fails %ld; min C1 slack %ld\n", tot, f1, f2, f3, min1);
}
