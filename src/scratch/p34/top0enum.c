/* TOP0 census (lead, 2026-10-21). Enumerate all numerical semigroups of genus <= GMAX by the Frobenius tree
 * (children remove a minimal generator > F). Leaves of the tree are exactly the S with no right primitive (r = 0).
 * For each leaf with n = e - 1 >= 2, compute the lex-least factorizations (compare the last coordinate first) of the
 * Apery elements w.r.t. m and test
 *     TOP0:  sum_{y in Ap, y >= c} (|y| + n) (y - c)  <=  (n+1) m (m-1)/2          (i.e. Lambda <= G when r = 0)
 * Also re-checks Wilf. Reports per depth class (c <= 4m vs c > 4m).
 * gcc -O2 -o top0enum top0enum.c ; ./top0enum GMAX */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define L 160
#define EMAX 64
static int GMAX;
static long long leaves[2], fails[2], wfail = 0; static long long minsl[2] = {1LL << 60, 1LL << 60};
static int fac[L][EMAX];
static long long cntg[64];
static void leaf(const char *S, int F) {
  int m = 1; while (!S[m]) m++;
  int c = F + 1;
  int gens[EMAX], e = 0;
  for (int x = m + 1; x <= F + m; x++) if (S[x]) {
    int dec = 0; for (int a = m; a <= x / 2 && !dec; a++) if (S[a] && S[x - a]) dec = 1;
    if (!dec) gens[e++] = x;
  }
  int n = e; /* left generators (r = 0 so all are < c) */
  if (n < 2) return;
  for (int i = 0; i < n; i++) if (gens[i] >= c) { fprintf(stderr, "not a leaf?\n"); exit(1); }
  /* Apery set and lex factorizations */
  static int isAp[L]; memset(isAp, 0, sizeof(isAp));
  for (int x = 0; x <= F + m; x++) if (S[x] && (x < m || !S[x - m])) isAp[x] = 1;
  memset(fac[0], 0, sizeof(int) * n);
  long long g = 0, top = 0;
  for (int x = 1; x <= F + m; x++) if (isAp[x]) {
    int best = -1, bv[EMAX];
    for (int i = 0; i < n; i++) if (gens[i] <= x && isAp[x - gens[i]]) {
      int v[EMAX]; memcpy(v, fac[x - gens[i]], sizeof(int) * n); v[i]++;
      int better = 0;
      if (best < 0) better = 1; else { for (int t = n - 1; t >= 0; t--) if (v[t] != bv[t]) { better = v[t] < bv[t]; break; } }
      if (better) { best = i; memcpy(bv, v, sizeof(int) * n); }
    }
    if (best < 0) { fprintf(stderr, "no factorization\n"); exit(1); }
    memcpy(fac[x], bv, sizeof(int) * n);
    if (x >= c) { int deg = 0; for (int t = 0; t < n; t++) deg += bv[t]; top += (long long)(deg + n) * (x - c); }
  }
  for (int x = 1; x < c; x++) if (!S[x]) g++;
  long long W = (long long)(n + 1) * (c - g) - c;
  if (W < 0) { wfail++; printf("WILF FAIL m=%d c=%d\n", m, c); }
  long long sl = (long long)(n + 1) * m * (m - 1) / 2 - top;   /* (n+1)m(m-1)/2 even-safe: m(m-1) even */
  int deep = c > 4 * m;
  leaves[deep]++;
  if (sl < minsl[deep]) { minsl[deep] = sl; printf("  new min slack[%s] %lld at m=%d c=%d g=%lld W=%lld gens=", deep ? "deep" : "shallow", sl, m, c, g, W); for (int i = 0; i < n; i++) printf("%d,", gens[i]); printf("\n"); fflush(stdout); }
  if (sl < 0) { fails[deep]++; if (fails[deep] <= 10) { printf("TOP0 FAIL m=%d c=%d slack=%lld gens=", m, c, sl); for (int i = 0; i < n; i++) printf("%d,", gens[i]); printf("\n"); fflush(stdout); } }
}
static void rec(char *S, int *d, int F, int genus) {
  int m = 1; while (!S[m]) m++;
  int nchild = 0; cntg[genus]++;
  if (genus < GMAX) {
    for (int x = (F + 1 > 1 ? F + 1 : 1); x <= (F + m > 1 ? F + m : 1); x++) if (S[x] && d[x] == 1) {
      nchild++;
      char S2[L]; int d2[L]; memcpy(S2, S, L); memcpy(d2, d, sizeof(int) * L);
      for (int y = x; y < L; y++) if (S[y - x]) d2[y]--;
      S2[x] = 0;
      rec(S2, d2, x, genus + 1);
    }
  } else {
    for (int x = (F + 1 > 1 ? F + 1 : 1); x <= (F + m > 1 ? F + m : 1); x++) if (S[x] && d[x] == 1) nchild++;
  }
  if (nchild == 0 && genus >= 1) leaf(S, F);
}
int main(int argc, char **argv) {
  GMAX = atoi(argv[1]);
  if (3 * GMAX + 5 >= L) { fprintf(stderr, "increase L\n"); return 1; }
  char S[L]; int d[L];
  for (int x = 0; x < L; x++) S[x] = 1;
  for (int y = 0; y < L; y++) { d[y] = 0; for (int a = 0; a <= y / 2; a++) if (S[a] && S[y - a]) d[y]++; }
  rec(S, d, -1, 0);
  printf("counts by genus:"); for (int g = 0; g <= GMAX; g++) printf(" %lld", cntg[g]); printf("\n");
  printf("genus <= %d: leaves (r = 0, n >= 2): shallow %lld, deep (c > 4m) %lld; TOP0 failures shallow %lld deep %lld; min slack shallow %lld deep %lld; Wilf failures %lld\n",
         GMAX, leaves[0], leaves[1], fails[0], fails[1], minsl[0], minsl[1], wfail);
  return 0;
}
