/* REST-M3 on level-1 generator sets (lead, 2026-10-19): S = <m, m+b_1, ..., m+b_k>, 0 < b_1 < ... < b_k < m,
 * exhaustive for k = K (given), m in [mlo, mhi].  Near-perfect additive bases make the Apery set simplex-like, where
 * every con_a(w) >= 0; this is the natural place for REST > 0 inside the class A = {M >= 3 n_1}.
 * Reports max REST/C2 over A (split 3e<m / 3e>=m), REST>0 count in A, CHAIN failures in A, and the extremal S.
 * gcc -O3 -std=gnu11 rest_lev1.c -o rest_lev1 ; ./rest_lev1 K mlo mhi */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int m; static int64_t w[512];
static void apery(int64_t *g, int k) {
  int done[512]; for (int i = 0; i < m; i++) { w[i] = INT64_MAX; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++) { int u = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] != INT64_MAX && (u < 0 || w[i] < w[u])) u = i;
    if (u < 0) break; done[u] = 1;
    for (int j = 0; j < k; j++) { int v = (int)((u + g[j]) % m); if (w[u] + g[j] < w[v]) w[v] = w[u] + g[j]; } }
}
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int K, b[16]; static uint64_t tot, totA, posA, chfA; static double rmax[2] = {-1e9, -1e9}; static char rex[2][256];
static void eval_S(void) {
  int g0 = m; for (int i = 0; i < K; i++) g0 = gcd(g0, b[i]); if (g0 != 1) return;
  int64_t g[16]; for (int i = 0; i < K; i++) g[i] = m + b[i];
  apery(g, K);
  for (int i = 0; i < m; i++) if (w[i] == INT64_MAX) return;
  /* minimal generators among g (all are level 1 so each is its own Apery element; check decomposability) */
  int64_t n[16]; int d = 0;
  for (int j = 0; j < K; j++) { int r = (int)(g[j] % m); if (w[r] != g[j]) continue; int dec = 0;
    for (int i = 1; i < m && !dec; i++) { int r2 = (r - i + m) % m; if (r2 && w[i] + w[r2] == g[j]) dec = 1; }
    if (!dec) n[d++] = g[j]; }
  if (d < 2) return;
  int64_t M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  tot++;
  int64_t n1 = n[0]; for (int a = 1; a < d; a++) if (n[a] < n1) n1 = n[a];
  if (M < 3 * n1) return;
  totA++;
  int64_t rest = 0, Bc = 0;
  for (int a = 0; a < d; a++) for (int i = 0; i < m; i++) { int64_t t = w[i];
    for (;;) { int64_t t2 = t + n[a]; if (t2 > M) break; if (w[t2 % m] != t2) break; t = t2; }
    Bc += M - t; if (i) rest += (M - w[i]) % m - (M - t); }
  int64_t need = (int64_t)(d - 1) * m * (m - 1) / 2;
  if (Bc < need) { chfA++; printf("CHAINFAIL_A m=%d d=%d b=", m, d); for (int i = 0; i < K; i++) printf("%d,", b[i]); printf("\n"); }
  double rr = (double)rest / ((double)m * (m - 1) / 2); int E3 = 3 * (d + 1) < m;
  if (rest > 0) { posA++; if (posA <= 20) { printf("RESTPOS m=%d d=%d M=%lld REST/C2=%.4f chain=%.4f b=", m, d, (long long)M, rr, (double)Bc / need); for (int i = 0; i < K; i++) printf("%d,", b[i]); printf("\n"); } }
  if (rr > rmax[E3]) { rmax[E3] = rr; int p = snprintf(rex[E3], 256, "m=%d e=%d M=%lld c=%lld chain=%.4f b=", m, d + 1, (long long)M, (long long)(M - m + 1), (double)Bc / need); for (int i = 0; i < K && p < 230; i++) p += snprintf(rex[E3] + p, 256 - p, "%d,", b[i]); }
}
static void rec(int i, int lo) { if (i == K) { eval_S(); return; } for (int x = lo; x < m; x++) { b[i] = x; rec(i + 1, x + 1); } }
int main(int argc, char **argv) {
  K = atoi(argv[1]); int mlo = atoi(argv[2]), mhi = atoi(argv[3]);
  for (m = mlo; m <= mhi; m++) { rec(0, 1); fprintf(stderr, "m=%d tot=%llu A=%llu\n", m, (unsigned long long)tot, (unsigned long long)totA); }
  printf("K=%d m in [%d,%d]: %llu S, %llu in A (M >= 3 n1); REST>0 in A: %llu; CHAIN failures in A: %llu\n", K, mlo, mhi,
    (unsigned long long)tot, (unsigned long long)totA, (unsigned long long)posA, (unsigned long long)chfA);
  for (int E3 = 0; E3 < 2; E3++) printf("  max REST/C2 in A, %s: %.4f at %s\n", E3 ? "3e<m" : "3e>=m", rmax[E3], rex[E3]);
  return 0;
}
