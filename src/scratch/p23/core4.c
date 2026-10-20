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
/* Dense-core construction (lead, 2026-10-20): fixed B_3 A-core C = ceil(h/2) + D, B-class fillers F in [h, m) (P18).
   Hard constraint: c = 3m + h exactly.  Objective: maximize ex = |Y| - Lam - Z (WIN excess), then |Y|.
   usage: ./core4 m h seed iters D1,D2,...   (D = offsets of the core relative to ceil(h/2)) */
int main(int argc, char **argv){
  m = atoi(argv[1]); int h = atoi(argv[2]); srand(atoi(argv[3])); long iters = atol(argv[4]);
  long long D[32]; int nd = 0; { char *p = argv[5]; while (*p){ D[nd++] = strtol(p, &p, 10); if (*p == ',') p++; } }
  static long long G[MM]; static int inF[MM]; int ng;
  long long base = (h + 1) / 2;
  #define BUILD() { ng = 0; G[ng++] = m; for (int i = 0; i < nd; i++) G[ng++] = m + base + D[i]; for (int f = h; f < m; f++) if (inF[f]) G[ng++] = m + f; }
  /* start: all fillers in [h, m) that are needed: greedily add uncovered residues */
  for (int f = 0; f < m; f++) inF[f] = 0;
  res_t cur; BUILD(); cur = evalS(ng, G);
  for (int pass = 0; pass < 3 * m && !(cur.ok && cur.h == h); pass++){
    /* find residues >= h with height >= 4 (w > 3m + r) and add the smallest such as a filler */
    int added = 0;
    for (int r = h; r < m && !added; r++) if (w[r] < 0 || w[r] > 3LL * m + r){ inF[r] = 1; added = 1; }
    if (!added) break;
    BUILD(); cur = evalS(ng, G);
  }
  if (!(cur.ok && cur.h == h)){ printf("no feasible start (c=%lld)\n", cur.c); return 0; }
  double sc = (cur.RAhi - cur.Lam - cur.Z) * 10.0 + cur.RAhi;
  long long bestex = -(1LL << 60);
  for (long it = 0; it < iters; it++){
    int f = h + rand() % (m - h); int g2 = h + rand() % (m - h); int mv = rand() % 3;
    int sf = inF[f], sg = inF[g2];
    if (mv == 0) inF[f] = !inF[f]; else if (mv == 1){ inF[f] = 0; inF[g2] = 1; } else { inF[f] = !inF[f]; inF[g2] = !inF[g2]; }
    BUILD(); res_t nr = evalS(ng, G);
    double ns = (nr.ok && nr.h == h) ? (nr.RAhi - nr.Lam - nr.Z) * 10.0 + nr.RAhi : -1e18;
    if (ns > -1e17 && (ns >= sc || urand() < 0.02)){ cur = nr; sc = ns;
      long long ex = nr.RAhi - nr.Lam - nr.Z;
      if (ex > bestex || ex > 0 || nr.W < 0 || nr.mdef > 0){ if (ex > bestex) bestex = ex;
        printf("%s ex=%lld mdef=%lld W=%lld m=%d c=%lld h=%lld e=%d Lam=%lld Z=%lld Nlo=%lld |Y|=%lld F=", nr.W < 0 ? "WILFFAIL" : (ex > 0 ? "WINFAIL" : (nr.mdef > 0 ? "MATCHFAIL" : "rec")), ex, nr.mdef, nr.W, m, nr.c, nr.h, d + 1, nr.Lam, nr.Z, nr.Nlo, nr.RAhi);
        for (int x = h; x < m; x++) if (inF[x]) printf("%d,", x); printf("\n"); fflush(stdout); } }
    else { inF[f] = sf; inF[g2] = sg; }
  }
  printf("DONE bestex=%lld\n", bestex);
}
