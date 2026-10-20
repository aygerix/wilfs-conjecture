/* SP0 as a pure statement about the small set (lead, 2026-10-20): A_s = {0} u U, U subset [1,h), |U| = a, h-1 not in 3A_s.
 * SP0_s = (a+1)*|3A_s n [0,h)| - 3|(4A_s\3A_s) n [0,h)| - |3A_s n [h,2h)| + E1_s, E1_s = (a+1)(a+2) - 2|2A_s|.
 * Exhaustive over U for each h <= H.  usage: ./sp0 a H */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int a, H, best = 1 << 30, bh, bU[16];
static int U[16];
static void eval(int h){
  static char s2[512], s3[512], s4[512]; int L = 4 * h + 4; memset(s2, 0, L); memset(s3, 0, L); memset(s4, 0, L);
  int A[17]; A[0] = 0; for (int i = 0; i < a; i++) A[i + 1] = U[i]; int n = a + 1;
  for (int i = 0; i < n; i++) for (int j = i; j < n; j++) s2[A[i] + A[j]] = 1;
  for (int x = 0; x < L; x++) if (s2[x]) for (int i = 0; i < n; i++) if (x + A[i] < L) s3[x + A[i]] = 1;
  if (s3[h - 1]) return;
  for (int x = 0; x < L; x++) if (s3[x]) for (int i = 0; i < n; i++) if (x + A[i] < L) s4[x + A[i]] = 1;
  int n2 = 0, y0 = 0, N4 = 0, t = 0; for (int x = 0; x < L; x++) n2 += s2[x];
  for (int x = 0; x < h; x++){ y0 += s3[x]; N4 += s4[x] && !s3[x]; }
  for (int x = h; x < 2 * h; x++) t += s3[x];
  int v = (a + 1) * y0 - 3 * N4 - t + (a + 1) * (a + 2) - 2 * n2;
  if (v < best){ best = v; bh = h; memcpy(bU, U, sizeof(int) * a); }
}
static void rec(int i, int lo, int h){ if (i == a){ eval(h); return; } for (int x = lo; x < h; x++){ U[i] = x; rec(i + 1, x + 1, h); } }
int main(int argc, char **argv){ a = atoi(argv[1]); H = atoi(argv[2]);
  for (int h = a + 1; h <= H; h++){ int old = best; rec(0, 1, h); if (best < old || h == H){ printf("a=%d up to h=%d: min SP0_s = %d at h=%d U=", a, h, best, bh); for (int i = 0; i < a; i++) printf("%d,", bU[i]); printf("\n"); fflush(stdout);} } }
