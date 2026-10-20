/* P18 depth-four Wilf margin (lead, 2026-10-20). S = <m, m+B>, B a k-subset of [1, m), gcd 1, 3m < c <= 4m.
 * Reports min W, min e*ell/c, min W/(e(e-1)), split by allA (max B < h) and by wrap (some 2- or 3-sum of A >= m lies below 4m... i.e. X_3 n [m, 3m) nonempty).
 * usage: ./p18margin k mlo mhi */
#include <stdio.h>
#include <stdlib.h>
#define MM 256
static int m, k, B[16], cur[16];
static long cnt[2][2]; static double mr[2][2] = {{9,9},{9,9}}, mq[2][2] = {{1e9,1e9},{1e9,1e9}}; static long mW[2][2] = {{1L<<40,1L<<40},{1L<<40,1L<<40}};
static char ex[2][2][3][200];
static int gcd(int a, int b){ while (b){ int t = a % b; a = b; b = t; } return a; }
static void eval(void){
  int g0 = m; for (int a = 0; a < k; a++) g0 = gcd(g0, B[a]); if (g0 != 1) return;
  static int w[MM]; for (int i = 0; i < m; i++) w[i] = -1; w[0] = 0;
  /* gens < 2m: relax in increasing order of value via repeated passes (Bellman-Ford style, small m) */
  int changed = 1; while (changed){ changed = 0; for (int i = 0; i < m; i++) if (w[i] >= 0) for (int a = 0; a < k; a++){ int v = w[i] + m + B[a], j = v % m; if (w[j] < 0 || v < w[j]){ w[j] = v; changed = 1; } } }
  int M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  int c = M - m + 1; if (!(3 * m < c && c <= 4 * m)) return;
  int h = c - 3 * m, e = k + 1; long g = 0; for (int i = 0; i < m; i++) g += w[i] / m; long ell = c - g, W = (long)e * ell - c;
  int allA = B[k - 1] < h;
  /* wrap: some residue's Apery element w has w = j*m + s with s >= m in its sumset form; P18 Kunz level k_r vs min j: detect if any w_i < c has floor(w/m) > number of summands... approximate: wrap iff some Apery element w < 4m+h has level > min summand count. compute summand count via BFS levels */
  static int lev[MM]; for (int i = 0; i < m; i++) lev[i] = -1; lev[0] = 0; int fr[MM], nf = 1; fr[0] = 0; int L = 0;
  while (nf){ int nx[MM], nn = 0; L++; for (int t = 0; t < nf; t++) for (int a = 0; a < k; a++){ int j = (fr[t] + B[a]) % m; if (lev[j] < 0){ lev[j] = L; nx[nn++] = j; } } for (int t = 0; t < nn; t++) fr[t] = nx[t]; nf = nn; }
  int wrap = 0; for (int i = 0; i < m; i++) if (w[i] / m != lev[i]) wrap = 1;
  double r = (double)e * ell / c, q = (double)W / ((double)e * (e - 1));
  cnt[allA][wrap]++;
  if (W < mW[allA][wrap]){ mW[allA][wrap] = W; int o = snprintf(ex[allA][wrap][0], 200, "W=%ld m=%d c=%d h=%d B=", W, m, c, h); for (int a = 0; a < k; a++) o += snprintf(ex[allA][wrap][0] + o, 200 - o, "%d,", B[a]); }
  if (r < mr[allA][wrap]){ mr[allA][wrap] = r; int o = snprintf(ex[allA][wrap][1], 200, "ratio=%.4f W=%ld m=%d c=%d h=%d B=", r, W, m, c, h); for (int a = 0; a < k; a++) o += snprintf(ex[allA][wrap][1] + o, 200 - o, "%d,", B[a]); }
  if (q < mq[allA][wrap]){ mq[allA][wrap] = q; int o = snprintf(ex[allA][wrap][2], 200, "W/e(e-1)=%.3f W=%ld m=%d c=%d h=%d B=", q, W, m, c, h); for (int a = 0; a < k; a++) o += snprintf(ex[allA][wrap][2] + o, 200 - o, "%d,", B[a]); }
}
static void rec(int pos, int start){ if (pos == k){ for (int a = 0; a < k; a++) B[a] = cur[a]; eval(); return; } for (int b = start; b < m; b++){ cur[pos] = b; rec(pos + 1, b + 1); } }
int main(int argc, char **argv){
  k = atoi(argv[1]); int mlo = atoi(argv[2]), mhi = atoi(argv[3]);
  for (m = mlo; m <= mhi; m++) rec(0, 1);
  for (int A = 0; A < 2; A++) for (int wr = 0; wr < 2; wr++) if (cnt[A][wr]) printf("k=%d m<=%d allA=%d wrap=%d: %ld S\n   %s\n   %s\n   %s\n", k, mhi, A, wr, cnt[A][wr], ex[A][wr][0], ex[A][wr][1], ex[A][wr][2]);
}
