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
static double score(res_t r){ if (!r.ok) return -1e9; return (double)(r.RAhi - r.Lam - r.Z) * 10.0 + r.RAhi * 0.5 + r.mdef * 50.0; }
static double urand(void){ return rand() / (RAND_MAX + 1.0); }
int main(int argc, char **argv){
  m = atoi(argv[1]); long iters = atol(argv[2]); srand(atoi(argv[3])); int mode = argc > 4 ? atoi(argv[4]) : 0;
  static long long G[MM], G2[MM]; int ng = 0;
  double best = -1e18; long long bestex = -(1LL << 60);
  if (mode >= 2){
    for (int restart = 0; iters > 0; restart++){
      int h = m / 3 + rand() % (2 * m / 3); int k = 3 + rand() % 6; long long T[16]; int nt = 0;
      for (int tries = 0; tries < 4000 && nt < k; tries++){ long long t = (h + 1) / 2 + rand() % ((2 * h) / 3 - (h + 1) / 2 + 1);
        int ok = 1; for (int i = 0; i < nt; i++) if (T[i] == t) ok = 0; if (!ok) continue;
        /* 3-sums of T u {t} distinct */
        long long X[17]; int nx = 0; for (int i = 0; i < nt; i++) X[nx++] = T[i]; X[nx++] = t;
        static char seen[4000]; for (int i = 0; i < 3 * h + 3; i++) seen[i] = 0;
        for (int i = 0; i < nx && ok; i++) for (int j = i; j < nx && ok; j++) for (int l = j; l < nx && ok; l++){ long long v = X[i] + X[j] + X[l]; if (seen[v]) ok = 0; seen[v] = 1; }
        if (ok) T[nt++] = t; }
      if (nt < 3) continue;
      CAP = (mode == 2) ? 3LL * m + h : 0;
      long long F[64]; int nf = rand() % 7;
      #define NEWF() ((mode == 3) ? (m + h + rand() % (m - h > 0 ? m - h : 1)) : ((rand() % 3 == 0) ? 2LL * m + h + rand() % m : m + h + rand() % m))
      if (mode == 3) nf = 2 + rand() % 12;
      for (int i = 0; i < nf; i++) F[i] = NEWF();
      #define BUILD(nf_, F_) { ng = 0; G[ng++] = m; for (int i = 0; i < nt; i++) G[ng++] = m + T[i]; for (int i = 0; i < nf_; i++) G[ng++] = F_[i]; }
      BUILD(nf, F); res_t cur = evalS(ng, G); double sc = score(cur);
      for (int it = 0; it < 3000 && iters > 0; it++, iters--){
        long long F2[64]; int nf2 = nf; for (int i = 0; i < nf; i++) F2[i] = F[i];
        int mv = rand() % 4;
        if (mv == 0 && nf2 > 0) F2[rand() % nf2] = F2[--nf2];
        else if (mv == 1 && nf2 < 60) F2[nf2++] = NEWF();
        else if (nf2 > 0){ int i = rand() % nf2; F2[i] += (rand() % 9) - 4; if (F2[i] <= m + h) F2[i] = m + h; }
        BUILD(nf2, F2); res_t nr = evalS(ng, G); double ns = score(nr);
        if (mode == 3 && nr.ok && nr.h != h) ns -= 1e6;
        if (ns >= sc || urand() < 0.03){ nf = nf2; for (int i = 0; i < nf; i++) F[i] = F2[i]; cur = nr; sc = ns; }
        if (nr.ok){ long long ex = nr.RAhi - nr.Lam - nr.Z;
          if (nr.W < 0 || ex > 0 || nr.mdef > 0 || ex > bestex){ if (ex > bestex) bestex = ex;
            printf("%s ex=%lld mdef=%lld W=%lld m=%d c=%lld h=%lld e=%d Lam=%lld Z=%lld Nlo=%lld RAhi=%lld core=", nr.W < 0 ? "WILFFAIL" : (ex > 0 ? "WINFAIL" : (nr.mdef > 0 ? "MATCHFAIL" : "rec")), ex, nr.mdef, nr.W, m, nr.c, nr.h, d + 1, nr.Lam, nr.Z, nr.Nlo, nr.RAhi);
            for (int i = 0; i < nt; i++) printf("%lld,", T[i]); printf(" gens="); for (int a = 0; a < d; a++) printf("%lld,", P[a]); printf("\n"); fflush(stdout); } }
      }
    }
    printf("DONE m=%d bestex=%lld\n", m, bestex); return 0;
  }
  for (int restart = 0; restart < 1000000 && iters > 0; restart++){
    /* initial state */
    ng = 0; G[ng++] = m;
    int h0 = m / 4 + rand() % (m / 2);
    if (mode == 1){ int a = 4 + rand() % 8; for (int i = 0; i < a; i++) G[ng++] = m + h0 / 2 + rand() % (h0 / 6 + 1); }
    int nf = 1 + rand() % 6; for (int i = 0; i < nf; i++) G[ng++] = m + 1 + rand() % (3 * m);
    G[ng++] = 4LL * m + h0 - 1 - rand() % 3; /* not needed in general; dropped if decomposable */
    res_t cur = evalS(ng, G); double sc = score(cur);
    double T = 3.0;
    for (long it = 0; it < 20000 && iters > 0; it++, iters--){
      int ng2 = ng; for (int i = 0; i < ng; i++) G2[i] = G[i];
      double u = urand();
      if (u < 0.35 && ng2 < 90){ G2[ng2++] = m + 1 + rand() % (3 * m + m / 2); }
      else if (u < 0.6 && ng2 > 2){ int i = 1 + rand() % (ng2 - 1); G2[i] = G2[--ng2]; }
      else if (ng2 > 1){ int i = 1 + rand() % (ng2 - 1); G2[i] += (rand() % 7) - 3; if (G2[i] <= m) G2[i] = m + 1; }
      res_t nr = evalS(ng2, G2); double ns = score(nr);
      if (ns >= sc || urand() < exp((ns - sc) / T)){ ng = ng2; for (int i = 0; i < ng; i++) G[i] = G2[i]; cur = nr; sc = ns; }
      T *= 0.9997;
      if (cur.ok){ long long ex = cur.RAhi - cur.Lam - cur.Z;
        if (cur.W < 0 || ex > 0 || cur.mdef > 0 || ex > bestex){
          if (ex > bestex) bestex = ex;
          evalS(ng, G);
          printf("%s ex=%lld mdef=%lld W=%lld m=%d c=%lld h=%lld e=%d Lam=%lld Z=%lld Nlo=%lld RAhi=%lld gens=",
                 cur.W < 0 ? "WILFFAIL" : (ex > 0 ? "WINFAIL" : (cur.mdef > 0 ? "MATCHFAIL" : "rec")), ex, cur.mdef, cur.W, m, cur.c, cur.h, d + 1, cur.Lam, cur.Z, cur.Nlo, cur.RAhi);
          for (int a = 0; a < d; a++) printf("%lld,", P[a]); printf("\n"); fflush(stdout);
          if (cur.W < 0 || ex > 0 || cur.mdef > 0) { if (bestex > 5) return 0; } } }
    }
  }
  printf("DONE m=%d bestex=%lld\n", m, bestex);
}
