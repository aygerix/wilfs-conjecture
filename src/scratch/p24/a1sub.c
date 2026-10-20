/* Subcase A1 of P18 depth four (lead, 2026-10-20): B subset (0,h), 2h <= m.  Exhaustive over k-subsets B of [1, m).
 * Reports min W, min W/e^2, and the extremal B with the profile (|2A|, y0 = |3A n [0,h)|, s = |A n [0,h/2)|).
 * usage: ./a1sub k mlo mhi */
#include <stdio.h>
#include <stdlib.h>
#define MM 256
static int m, k, B[16], cur[16]; static long cnt; static long mW = 1L << 40; static double mq = 1e9; static char ex[2][300];
static int gcd(int a, int b){ while (b){ int t = a % b; a = b; b = t; } return a; }
static void eval(void){
  int g0 = m; for (int a = 0; a < k; a++) g0 = gcd(g0, B[a]); if (g0 != 1) return;
  static int w[MM]; for (int i = 0; i < m; i++) w[i] = -1; w[0] = 0;
  int changed = 1; while (changed){ changed = 0; for (int i = 0; i < m; i++) if (w[i] >= 0) for (int a = 0; a < k; a++){ int v = w[i] + m + B[a], j = v % m; if (w[j] < 0 || v < w[j]){ w[j] = v; changed = 1; } } }
  int M = 0; for (int i = 0; i < m; i++){ if (w[i] < 0) return; if (w[i] > M) M = w[i]; }
  int c = M - m + 1; if (!(3 * m < c && c <= 4 * m)) return;
  int h = c - 3 * m, e = k + 1; if (B[k - 1] >= h || 2 * h > m) return;
  long g = 0; for (int i = 0; i < m; i++) g += w[i] / m; long W = (long)e * (c - g) - c; cnt++;
  /* profile */
  static char s2[3 * MM], s3[3 * MM]; for (int t = 0; t < 3 * m; t++){ s2[t] = 0; s3[t] = 0; }
  int A[17]; A[0] = 0; for (int a = 0; a < k; a++) A[a + 1] = B[a];
  for (int i = 0; i <= k; i++) for (int j = i; j <= k; j++){ s2[A[i] + A[j]] = 1; for (int l = j; l <= k; l++) s3[A[i] + A[j] + A[l]] = 1; }
  int n2 = 0, y0 = 0, sm = 0; for (int t = 0; t < 3 * m; t++){ n2 += s2[t]; if (t < h) y0 += s3[t]; } for (int i = 0; i <= k; i++) if (2 * A[i] < h) sm++;
  double q = (double)W / ((double)e * e);
  if (W < mW){ mW = W; int o = snprintf(ex[0], 300, "W=%ld m=%d h=%d c=%d |2A|=%d y0=%d small=%d B=", W, m, h, c, n2, y0, sm); for (int a = 0; a < k; a++) o += snprintf(ex[0] + o, 300 - o, "%d,", B[a]); }
  if (q < mq){ mq = q; int o = snprintf(ex[1], 300, "W/e^2=%.3f W=%ld m=%d h=%d |2A|=%d y0=%d small=%d B=", q, W, m, h, n2, y0, sm); for (int a = 0; a < k; a++) o += snprintf(ex[1] + o, 300 - o, "%d,", B[a]); }
}
static void rec(int pos, int start){ if (pos == k){ for (int a = 0; a < k; a++) B[a] = cur[a]; eval(); return; } for (int b = start; b < m / 2; b++){ cur[pos] = b; rec(pos + 1, b + 1); } }
int main(int argc, char **argv){ k = atoi(argv[1]); int mlo = atoi(argv[2]), mhi = atoi(argv[3]);
  for (m = mlo; m <= mhi; m++) rec(0, 1);
  printf("k=%d m in [%d,%d]: %ld S in subcase A1\n  %s\n  %s\n", k, mlo, mhi, cnt, ex[0], ex[1]); }
