/* Break C1 near B_3 simplices (lead, 2026-10-20; advisor's suggested experiment).
 * For every k-subset B of [1, m-1] and every truncation t in (3m, 4m]: S_t = <m, m+B> u [t, oo). If q(S_t) = 4, check
 *   C1: R <= rho + L2,  L2 = sum_{y in Ap, y < c} tau(y) + sum_v (lam(v) + |U(v)| - 4)^+
 *   C2: R <= rho + sum_{y<c} tau(y) + Z,   and Wilf.
 * usage: ./c1near mlo mhi k [tstep] */
#include <stdio.h>
#include <stdlib.h>
#define MM 200
static int m, k, B[16], w0[MM], w[MM], ord[MM], gen[MM], ng, nu[MM][MM];
static long tot, f1, f2, f3, min1 = 1L << 40, min2 = 1L << 40;
static int cmpw(const void *x, const void *y){ return w[*(int*)x] - w[*(int*)y]; }
static void apery0(void){
  static int done[MM]; for (int i = 0; i < m; i++){ w0[i] = -1; done[i] = 0; } w0[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w0[i] >= 0 && (b < 0 || w0[i] < w0[b])) b = i;
    if (b < 0) return; done[b] = 1;
    for (int a = 0; a < k; a++){ int j = (b + m + B[a]) % m, v = w0[b] + m + B[a]; if (w0[j] < 0 || v < w0[j]) w0[j] = v; } }
}
static void eval(int t){
  for (int i = 0; i < m; i++){ int tail = t + ((i - t) % m + m) % m; w[i] = (w0[i] >= 0 && w0[i] < tail) ? w0[i] : tail; }
  int M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  int c = M - m + 1; if (!(3 * m < c && c <= 4 * m)) return;
  /* minimal generators among Ap \ 0 */
  ng = 0;
  for (int i = 1; i < m; i++){ int x = w[i], dec = 0;
    for (int j = 1; j < m && !dec; j++){ int y = w[j]; if (y < x){ int z = x - y; if (w[z % m] == z) dec = 1; } }
    if (!dec) gen[ng++] = x; }
  int e = ng + 1; long g = 0; for (int i = 0; i < m; i++) g += w[i] / m;
  long W = (long)e * (c - g) - c, rho = 4L * m - c;
  for (int i = 0; i < m; i++) ord[i] = i; qsort(ord, m, sizeof(int), cmpw);
  for (int a = 0; a < ng; a++){ int r = gen[a] % m;
    for (int s = 0; s < m; s++){ int i = ord[s], j = (i - r + m) % m; nu[a][i] = (w[j] + gen[a] == w[i]) ? nu[a][j] + 1 : 0; } }
  long tau = 0, ex = 0, Z = 0, R = 0;
  for (int i = 0; i < m; i++){ long x = w[i], lam = (M - x) / m, K = 4 - lam; int U = 0, tb = 0;
    for (int a = 0; a < ng; a++){ if (nu[a][i]){ U++; K -= nu[a][i] * ((M - (x - gen[a])) / m - lam); }
      int j = (int)((x + gen[a]) % m); if (w[j] != x + gen[a]) tb++; }
    if (x < c) tau += tb; if (lam + U - 4 > 0) ex += lam + U - 4; if (K < 0) Z -= K; if (K == 1) R++; }
  tot++;
  long s1 = rho + tau + ex - R, s2 = rho + tau + Z - R;
  if (s1 < 0){ f1++; if (f1 <= 8){ printf("C1FAIL slack=%ld C2slack=%ld m=%d t=%d c=%d e=%d rho=%ld R=%ld tau=%ld ex=%ld Z=%ld W=%ld B=", s1, s2, m, t, c, e, rho, R, tau, ex, Z, W); for (int a = 0; a < k; a++) printf("%d,", B[a]); printf("\n"); fflush(stdout); } }
  if (s2 < 0){ f2++; printf("C2FAIL slack=%ld m=%d t=%d c=%d e=%d W=%ld B=", s2, m, t, c, e, W); for (int a = 0; a < k; a++) printf("%d,", B[a]); printf("\n"); fflush(stdout); }
  if (W < 0){ f3++; printf("WILFFAIL m=%d t=%d\n", m, t); }
  if (s1 < min1){ min1 = s1; printf("minC1 slack=%ld m=%d t=%d c=%d e=%d rho=%ld R=%ld tau=%ld ex=%ld Z=%ld W=%ld B=", s1, m, t, c, e, rho, R, tau, ex, Z, W); for (int a = 0; a < k; a++) printf("%d,", B[a]); printf("\n"); fflush(stdout); }
  if (s2 < min2) min2 = s2;
}
static int cur[16];
static int B3ONLY = 0;
static int b3ok(int pos){ /* check sums of <= 3 elements of {0} u cur[0..pos] distinct mod m */
  static int seen[MM]; for (int i = 0; i < m; i++) seen[i] = 0; int x[17]; x[0] = 0; for (int a = 0; a <= pos; a++) x[a + 1] = cur[a];
  int n = pos + 2;
  for (int i = 0; i < n; i++) for (int j = i; j < n; j++) for (int l = j; l < n; l++){ int r = (x[i] + x[j] + x[l]) % m; if (seen[r]) return 0; seen[r] = 1; }
  return 1; }
static void rec(int pos, int start){
  if (pos == k){ for (int a = 0; a < k; a++) B[a] = cur[a]; apery0();
    int ok = 1; for (int i = 0; i < m; i++) if (w0[i] < 0) ok = 0; if (!ok) return;
    for (int t = 3 * m + 1; t <= 4 * m; t++) eval(t); return; }
  for (int b = start; b < m; b++){ cur[pos] = b; if (B3ONLY && !b3ok(pos)) continue; rec(pos + 1, b + 1); }
}
int main(int argc, char **argv){
  int mlo = atoi(argv[1]), mhi = atoi(argv[2]); k = atoi(argv[3]); if (argc > 4) B3ONLY = atoi(argv[4]);
  for (m = mlo; m <= mhi; m++){ rec(0, 1); printf("m=%d done: tested %ld, C1 fails %ld, C2 fails %ld, Wilf fails %ld, min C1 slack %ld, min C2 slack %ld\n", m, tot, f1, f2, f3, min1, min2); fflush(stdout); }
}
