/* Annealer against WIN / MATCH4 at depth four (lead, 2026-10-20).
 * S = <m, G>.  Score = WIN excess  ex = RAhi - Lam - Z  (WIN: ex <= 0), tie-break by RAhi and matching deficiency.
 * Also checks MATCH4 (cubes -> Lambda-options or distinct Z-sources) and Wilf.  Moves: add / delete / shift a generator.
 * usage: ./anneal4 m iters seed [mode]   mode 0: random start; 1: seeded A-core in [h/2, 2h/3) + fillers */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define MM 600
static int m; static long long w[MM]; static int done_[MM];
static long long K[MM], lam[MM]; static unsigned char top[MM][MM]; static long long P[MM]; static int d;
typedef struct { int ok; long long W, Lam, Z, Nlo, RAhi, mdef, c, h; } res_t;
static int madj[MM][MM], mdeg[MM], cap[MM], owner[MM][8], nown[MM], seen_[MM];
static int aug(int y){ for (int j = 0; j < mdeg[y]; j++){ int x = madj[y][j]; if (seen_[x]) continue; seen_[x] = 1;
  if (nown[x] < cap[x]){ owner[x][nown[x]++] = y; return 1; }
  for (int u = 0; u < nown[x]; u++) if (aug(owner[x][u])){ owner[x][u] = y; return 1; } } return 0; }
#define INAP(v) ((v) >= 0 && w[(v) % m] == (v))
#define INS(v) ((v) >= 0 && w[(v) % m] <= (v))
static long long CAP = 0; /* if > 0: S := <m,G> u [CAP, oo) */
static res_t evalS(int ng, long long *G){
  res_t R = {0};
  for (int i = 0; i < m; i++){ w[i] = -1; done_[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done_[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return R; done_[b] = 1;
    for (int a = 0; a < ng; a++){ int j = (int)((b + G[a]) % m); long long v = w[b] + G[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
  if (CAP > 0) for (int i = 0; i < m; i++){ long long tail = CAP + ((i - CAP) % m + m) % m; if (w[i] < 0 || w[i] > tail) w[i] = tail; }
  long long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  long long c = M - m + 1; if (!(c > 3LL * m && c <= 4LL * m)) { R.c = c; return R; }
  d = 0; for (int i = 1; i < m; i++){ long long x = w[i]; int dec = 0;
    for (int j = 1; j < m && !dec; j++){ long long y = w[j]; if (y < x && INS(x - y)) dec = 1; } if (!dec) P[d++] = x; }
  long long h = c - 3LL * m, g = 0, Lam = 0, Z = 0, Nlo = 0, RAhi = 0;
  for (int i = 0; i < m; i++){ long long x = w[i]; lam[i] = (M - x) / m; K[i] = 4 - lam[i]; g += x / m;
    for (int a = 0; a < d; a++){ int j = 0; while (INS(x - (long long)(j + 1) * P[a])) j++;
      if (j) K[i] -= j * ((M - (x - P[a])) / m - lam[i]);
      top[i][a] = !INAP(x + P[a]); if (top[i][a]) Lam += (j + 1) * lam[i]; }
    int inw = ((i - h) % m + m) % m < h;
    if (K[i] < 0) Z -= K[i]; if (K[i] <= 0 && !inw) Nlo++; if (K[i] == 1 && inw) RAhi++; }
  long long e = d + 1; R.W = e * (c - g) - c; R.Lam = Lam; R.Z = Z; R.Nlo = Nlo; R.RAhi = RAhi; R.c = c; R.h = h; R.ok = 1;
  if (R.W != Lam + Z + Nlo - RAhi){ printf("IDENTITY FAIL\n"); exit(1); }
  /* matching */
  int ny = 0; static int yl[MM];
  for (int x = 0; x < m; x++){ cap[x] = K[x] < 0 ? (int)(-K[x] < 8 ? -K[x] : 8) : 0; nown[x] = 0; }
  for (int y = 0; y < m; y++){ int inw = ((y - h) % m + m) % m < h; if (!(inw && K[y] == 1)) continue;
    int hasL = 0; mdeg[y] = 0;
    for (int a = 0; a < d; a++){ int x = (int)(((y - P[a]) % m + m) % m);
      if (lam[x] >= 1 && top[x][a]) hasL = 1;
      if (K[x] <= -1){ int dup = 0; for (int j = 0; j < mdeg[y]; j++) if (madj[y][j] == x) dup = 1; if (!dup) madj[y][mdeg[y]++] = x; } }
    if (!hasL) yl[ny++] = y; }
  int mt = 0; for (int i = 0; i < ny; i++){ for (int x = 0; x < m; x++) seen_[x] = 0; if (aug(yl[i])) mt++; }
  R.mdef = ny - mt;
  return R;
}

static double urand(void){ return rand() / (RAND_MAX + 1.0); }
/* P18 annealing: S = <m, m+B>, maximize WIN excess ex = RAhi - Lam - Z (then RAhi, then -W/m). */
static double score(res_t r){ if (!r.ok) return -1e9; return (double)(r.RAhi - r.Lam - r.Z) * 10.0 + r.RAhi * 1.0 + r.mdef * 50.0 - 0.01 * r.W; }
int main(int argc, char **argv){
  m = atoi(argv[1]); long iters = atol(argv[2]); srand(atoi(argv[3])); int kmax = argc > 4 ? atoi(argv[4]) : 12;
  static long long G[MM], G2[MM]; long long bestex = -(1LL << 60);
  while (iters > 0){
    int k = 3 + rand() % (kmax - 2); int ng = 0; G[ng++] = m;
    int hh = m / 3 + rand() % (2 * m / 3);
    for (int i = 0; i < k; i++) G[ng++] = m + ((rand() % 2) ? (hh / 2 + rand() % (hh / 6 + 1)) : (1 + rand() % (m - 1)));
    res_t cur = evalS(ng, G); double sc = score(cur); double T = 2.0;
    for (int it = 0; it < 20000 && iters > 0; it++, iters--){
      int ng2 = ng; for (int i = 0; i < ng; i++) G2[i] = G[i];
      double u = urand();
      if (u < 0.15 && ng2 < kmax + 1) G2[ng2++] = m + 1 + rand() % (m - 1);
      else if (u < 0.3 && ng2 > 4){ int i = 1 + rand() % (ng2 - 1); G2[i] = G2[--ng2]; }
      else if (u < 0.5){ int i = 1 + rand() % (ng2 - 1); G2[i] = m + 1 + rand() % (m - 1); }
      else { int i = 1 + rand() % (ng2 - 1); G2[i] += (rand() % 11) - 5; if (G2[i] <= m) G2[i] = m + 1; if (G2[i] >= 2 * m) G2[i] = 2 * m - 1; }
      res_t nr = evalS(ng2, G2); double ns = score(nr);
      if (ns >= sc || urand() < exp((ns - sc) / T)){ ng = ng2; for (int i = 0; i < ng; i++) G[i] = G2[i]; cur = nr; sc = ns; }
      T *= 0.9996;
      if (nr.ok){ long long ex = nr.RAhi - nr.Lam - nr.Z;
        if (nr.W < 0 || ex > 0 || nr.mdef > 0 || ex > bestex){ if (ex > bestex) bestex = ex;
          printf("%s ex=%lld mdef=%lld W=%lld m=%d c=%lld h=%lld e=%d Lam=%lld Z=%lld Nlo=%lld RAhi=%lld gens=", nr.W < 0 ? "WILFFAIL" : (ex > 0 ? "WINFAIL" : (nr.mdef > 0 ? "MATCHFAIL" : "rec")), ex, nr.mdef, nr.W, m, nr.c, nr.h, d + 1, nr.Lam, nr.Z, nr.Nlo, nr.RAhi);
          for (int a = 0; a < d; a++) printf("%lld,", P[a]); printf("\n"); fflush(stdout); } }
    }
  }
  printf("DONE m=%d bestex=%lld\n", m, bestex);
}
