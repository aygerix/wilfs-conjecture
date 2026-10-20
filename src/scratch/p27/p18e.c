/* Complete enumeration of P18 depth-four semigroups with fixed embedding dimension e (lead, 2026-10-20).
 * S = <m, m+B>, |B| = e-1, B subset [1,m-1], gcd 1, 3m < c <= 4m.  Depth four forces m <= |4A| <= C(e+3,4)
 * (every residue mod m is the residue of a 4-fold sum of A = {0} u B), so m <= C(e+3,4) is exhaustive.
 * Reports per m: number of depth-four S, min W, and the minimizer.  usage: ./p18e e mlo mhi */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int e, k, m, B[16]; static long long cnt, minW; static int best[16], besth;
static long long w[400]; static int bucketnext[400];
static void eval(void){
  { static unsigned char cov[400]; memset(cov, 0, m); int A[17]; A[0] = 0; for (int i = 0; i < k; i++) A[i+1] = B[i];
    int n = k + 1, got = 0;
    for (int a1 = 0; a1 < n; a1++) for (int a2 = a1; a2 < n; a2++){ int s2 = A[a1] + A[a2];
      for (int a3 = a2; a3 < n; a3++){ int s3 = s2 + A[a3]; for (int a4 = a3; a4 < n; a4++){ int r = (s3 + A[a4]) % m; if (!cov[r]){ cov[r] = 1; got++; } } } }
    if (got < m) return; }
  int g0 = m; for (int i = 0; i < k; i++){ int x = B[i], y = g0; while (y){ int t = x % y; x = y; y = t; } g0 = x; } if (g0 != 1) return;
  /* Apery set by Dijkstra over residues; values < 5m, use simple O(m^2) selection with early exit */
  static char done[400]; for (int i = 0; i < m; i++){ w[i] = 1LL << 40; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int u = -1; long long bv = 1LL << 41; for (int i = 0; i < m; i++) if (!done[i] && w[i] < bv){ bv = w[i]; u = i; }
    if (u < 0 || bv >= (1LL << 40)) return; done[u] = 1; if (bv >= 5LL * m) return; /* depth > 4 */
    for (int a = 0; a < k; a++){ long long v = bv + m + B[a]; int r = v % m; if (v < w[r]) w[r] = v; } }
  long long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long long c = M - m + 1; if (!(3LL * m < c && c <= 4LL * m)) return;
  long long W = (long long)e * (c - g) - c; cnt++;
  if (W < minW){ minW = W; memcpy(best, B, sizeof(int) * k); besth = (int)(c - 3 * m); }
}
static void rec(int i, int lo){ if (i == k){ eval(); return; } for (int x = lo; x <= m - 1 - (k - 1 - i); x++){ B[i] = x; rec(i + 1, x + 1); } }
int main(int argc, char **argv){ e = atoi(argv[1]); k = e - 1; int mlo = atoi(argv[2]), mhi = atoi(argv[3]);
  long long tot = 0, gmin = 1LL << 60;
  for (m = mlo; m <= mhi; m++){ cnt = 0; minW = 1LL << 60; rec(0, 1); tot += cnt; if (cnt && minW < gmin) gmin = minW;
    printf("e=%d m=%d depth-four S: %lld min W %lld", e, m, cnt, cnt ? minW : 0);
    if (cnt){ printf(" at h=%d B=", besth); for (int i = 0; i < k; i++) printf("%d,", best[i]); } printf("\n"); fflush(stdout); }
  printf("TOTAL e=%d m in [%d,%d]: %lld depth-four S, min W %lld\n", e, mlo, mhi, tot, gmin); }
