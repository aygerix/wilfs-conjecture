/* P18 at depth four (S = <m, m+B>, B in [1,m-1], 3m < c <= 4m): window decomposition
     W = Lam + Z + Nlo - RAhi        (exact; asserted)
   Nlo  = #{v in Ap : K(v) <= 0, residue r(v) not in [h, 2h) mod m}
   RAhi = #{v in Ap : K(v) = 1, r(v) in [h, 2h) mod m}  (critical pure-A cubics only, by the short arc)
   Also: W1 = [h, ceil(3h/2)) holds no critical value (asserted).
   Reports the max of RAhi - Z - Lam ("excess") and the min W, with pieces.
   usage: ./p18arc mlo mhi k  (exhaustive k-subsets)  |  ./p18arc m m k R seed (R random k-subsets) */
#include <stdio.h>
#include <stdlib.h>
#define MM 512
static int m, k, B[32], w[MM], ord[MM], gen[MM], ng, nu[40][MM];
static long tot, maxex = -(1L<<40), minW = 1L<<40;
static int cmpw(const void *x, const void *y){ return w[*(int*)x] - w[*(int*)y]; }
static int gcd(int a, int b){ while(b){int t=a%b;a=b;b=t;} return a; }
static void eval(void){
  int g0 = m; for (int i = 0; i < k; i++) g0 = gcd(g0, B[i]); if (g0 != 1) return;
  static int done[MM]; for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    done[b] = 1; for (int a = 0; a < k; a++){ int j = (b + m + B[a]) % m, v = w[b] + m + B[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
  int M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  int c = M - m + 1; if (!(3 * m < c && c <= 4 * m)) return;
  int h = c - 3 * m; ng = k; for (int a = 0; a < k; a++) gen[a] = m + B[a];
  int e = k + 1; long gg = 0; for (int i = 0; i < m; i++) gg += w[i] / m;
  long W = (long)e * (c - gg) - c;
  for (int i = 0; i < m; i++) ord[i] = i; qsort(ord, m, sizeof(int), cmpw);
  for (int a = 0; a < ng; a++){ int r = gen[a] % m;
    for (int s = 0; s < m; s++){ int i = ord[s], j = (i - r + m) % m; nu[a][i] = (w[j] + gen[a] == w[i]) ? nu[a][j] + 1 : 0; } }
  long Lam = 0, Z = 0, Nlo = 0, RAhi = 0, R = 0, nW1 = 0, faces = 0;
  for (int i = 0; i < m; i++){ long x = w[i], lam = (M - x) / m, K = 4 - lam;
    for (int a = 0; a < ng; a++){ if (nu[a][i]) K -= nu[a][i] * ((M - (x - gen[a])) / m - lam);
      int j = (int)((x + gen[a]) % m); if (w[j] != x + gen[a]) Lam += (nu[a][i] + 1) * lam; }
    int inwin = (i >= h && i < 2 * h) || (i + m >= h && i + m < 2 * h);
    int inW1 = (i >= h && 2 * i < 3 * h);
    if (K < 0) Z -= K; if (K == 1) R++;
    if (K <= 0 && !inwin) Nlo++;
    if (K == 1 && inwin) RAhi++;
    if (K == 1 && inW1){ printf("W1 CRITICAL m=%d\n", m); exit(1); }
    if (K > 1){ printf("K>1 m=%d\n", m); exit(1); }
  }
  tot++;
  if (W != Lam + Z + Nlo - RAhi){ printf("IDENT FAIL m=%d W=%ld Lam=%ld Z=%ld Nlo=%ld RAhi=%ld\n", m, W, Lam, Z, Nlo, RAhi); exit(1); }
  long ex = RAhi - Z - Lam;
  if (ex > maxex || W < minW){
    if (ex > maxex) maxex = ex; if (W < minW) minW = W;
    printf("rec ex=%ld W=%ld m=%d c=%d h=%d e=%d Lam=%ld Z=%ld Nlo=%ld RAhi=%ld R=%ld B=", ex, W, m, c, h, e, Lam, Z, Nlo, RAhi, R);
    for (int a = 0; a < k; a++) printf("%d,", B[a]); printf("\n"); fflush(stdout); }
}
static void rec(int pos, int start){ if (pos == k){ eval(); return; } for (int b = start; b < m; b++){ B[pos] = b; rec(pos + 1, b + 1); } }
int main(int argc, char **argv){
  int mlo = atoi(argv[1]), mhi = atoi(argv[2]); k = atoi(argv[3]);
  if (argc > 5){ long Rn = atol(argv[4]); srand(atoi(argv[5])); m = mlo;
    for (long t = 0; t < Rn; t++){ for (int a = 0; a < k; a++){ int ok; do { B[a] = 1 + rand() % (m - 1); ok = 1; for (int b = 0; b < a; b++) if (B[b] == B[a]) ok = 0; } while (!ok); } eval(); } }
  else for (m = mlo; m <= mhi; m++) rec(0, 1);
  printf("DONE k=%d m=%d..%d depth4=%ld maxex=%ld minW=%ld\n", k, mlo, mhi, tot, maxex, minW);
}
