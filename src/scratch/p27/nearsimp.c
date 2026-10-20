/* Near-B3-simplex test (lead, 2026-10-20).  Step 1: for k = |U|, search (random restarts + hill climbing) for U subset [0,D],
 * 0, D in U, with 3U = [0, 3D] (complete restricted 3-basis), maximizing D.  Step 2: for B = x + U (and B = x + U plus the
 * reflected variants), scan m in [3x - 3D, 3x + 3D] and x, compute the semigroup <m, m+B> exactly (Apery by Dijkstra) and
 * report the minimum of W and of W/(e*l) at depth >= 4.  usage: ./nearsimp k iters seed */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int full3(int *U, int k, int D){ static char s[4000]; if (3*D+1 > 4000) return 0; memset(s, 0, 3*D+1);
  for (int i = 0; i < k; i++) for (int j = i; j < k; j++) for (int l = j; l < k; l++) s[U[i]+U[j]+U[l]] = 1;
  for (int z = 0; z <= 3*D; z++) if (!s[z]) return 0; return 1; }
static long long Wof(int m, int *B, int k, int *depth, long long *ell, long long *cc){
  static long long w[20000]; static char done[20000]; if (m >= 20000) return 1LL<<60;
  for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return 1LL<<60; done[b] = 1;
    for (int a = 0; a < k; a++){ int j = (b + B[a]) % m; long long v = w[b] + m + B[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
  long long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long long c = M - m + 1; *depth = (int)((c + m - 1) / m); *ell = c - g; *cc = c; return (long long)(k + 1) * (c - g) - c; }
int main(int argc, char **argv){
  int k = atoi(argv[1]); long iters = atol(argv[2]); srand(atoi(argv[3]));
  int bestD = 0, bestU[64];
  for (int D = k - 1; D < 400; D++){ /* random search for a complete restricted 3-basis with diameter D */
    int found = 0;
    for (long t = 0; t < iters && !found; t++){
      int U[64]; U[0] = 0; U[k-1] = D; for (int i = 1; i < k-1; i++) U[i] = 1 + rand() % (D - 1);
      for (int i = 1; i < k; i++) for (int j = i; j > 0 && U[j] < U[j-1]; j--){ int x = U[j]; U[j] = U[j-1]; U[j-1] = x; }
      int dup = 0; for (int i = 1; i < k; i++) if (U[i] == U[i-1]) dup = 1; if (dup) continue;
      if (full3(U, k, D)){ found = 1; bestD = D; memcpy(bestU, U, sizeof(int)*k); }
    }
    if (!found && D > bestD + 6) break;
  }
  printf("k=%d best D=%d (3D+1=%d, C(k+2,3)=%d, efficiency %.3f) U=", k, bestD, 3*bestD+1, (k+2)*(k+1)*k/6, (3.0*bestD+1)/((k+2)*(k+1)*k/6.0));
  for (int i = 0; i < k; i++) printf("%d,", bestU[i]); printf("\n");
  /* Step 2 */
  long long minW = 1LL<<60; double minr = 1e9; int bm = 0, bx = 0, bq = 0;
  for (int x = 1; x <= 6 * bestD + 20; x++) for (int m = x + bestD + 1; m <= 3 * x + 3 * bestD + 2; m++){
    int B[64]; for (int i = 0; i < k; i++) B[i] = x + bestU[i];
    int depth; long long ell, cc; long long W = Wof(m, B, k, &depth, &ell, &cc);
    if (W >= (1LL<<59) || depth < 4) continue;
    double r = (double)(k + 1) * ell / cc;
    if (W < minW){ minW = W; bm = m; bx = x; bq = depth; }
    if (r < minr) minr = r;
  }
  printf("  depth>=4 scan: min W = %lld at m=%d x=%d (depth %d); min e*l/c = %.4f\n", minW, bm, bx, bq, minr);
}
