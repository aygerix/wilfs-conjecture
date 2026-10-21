/* enumlp3 (= enumlp + RT3/UA3, optional height filter, top-K extremizers; lead 2026-10-21).
 * enumlp: exhaustive RT2 / UA2 minimization over the exact-MILP domain of kunz_cert_milp.py --open --h4 (lead, 2026-10-21).
 * Domain (as enumh4.c): multiplicity m, embedding dimension e, every Kunz coordinate in [1, K], c >= 4m+1, 3e < m,
 * Apery height >= 4.  Every S is generated exactly once (d = e-1 residues, levels in [1, K], all chosen generators minimal).
 * RT2(S) = min e(q + sum y) - qm + rho over y >= 0 with q - lo_s <= y_i + y_j - y_s <= q + up_s on tight pairs,
 *   lo_s = [r_s >= m - rho], up_s = [r_s <= m - rho - 2], r_x = (x - r - 1) mod m, rho = m - r - 1, q = k_r   (kunz_face.py),
 * depends only on the key (r, q, tight pairs): one LP per distinct key (Gurobi C API, no bounds on y other than y >= 0).
 * UA2(S) = RT2 with y_g = mu_g = q - k_g - [g > r] on generators; UA2 >= RT2(key), so UA2(S) is solved only when
 * RT2(key) < best UA2 so far or RT2(key)/W(S) < best UA2/W so far (exact pruning: skipped S cannot improve either minimum).
 * W(S) exact; W <= 0 is reported as a counterexample.  Output: per conductor residue r the minima of RT2, UA2, W with
 * representatives, global minima of RT2/W and UA2/W, counts.
 * build: gcc -O2 enumlp.c -I$HOME/gurobi1303/linux64/include -L$HOME/gurobi1303/linux64/lib -lgurobi130 -lm
 * RT3/UA3: RT2/UA2 with the part-type rule (lower allowance only if both parts LOW (> r), upper only if both HIGH (<= r)).
 * usage: LD_LIBRARY_PATH=$HOME/gurobi1303/linux64/lib ./enumlp3 m e K part nparts h4only */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "gurobi_c.h"
#define MAXM 24
typedef struct { uint64_t b[4]; uint8_t r, q; } Key;
typedef struct { Key k; long gen; double rt2, rt3; } Ent;
/* the tight-pair set determines the generator residues, so keys never repeat across residue combinations: the table is
   reset per combination by a generation stamp (an entry is live iff gen == current combination number) */
static Ent *tab; static long tsz, curgen;
static uint64_t hk(const Key *k){ uint64_t h = 1469598103934665603ULL; const uint8_t *p = (const uint8_t *)k;
  for (size_t i = 0; i < sizeof(Key); i++){ h ^= p[i]; h *= 1099511628211ULL; } return h; }
static long tn;
static Ent *find(const Key *k, int *isnew){
  uint64_t h = hk(k) & (tsz - 1);
  while (tab[h].gen == curgen){ if (!memcmp(&tab[h].k, k, sizeof(Key))){ *isnew = 0; return &tab[h]; } h = (h + 1) & (tsz - 1); }
  tab[h].gen = curgen; tab[h].k = *k; tn++; *isnew = 1; return &tab[h]; }
static GRBenv *env;
static int m, e, d;
/* LP: tight pairs (ti, tj, ts); fixed[x] >= 0 fixes y_x */
static double solve(int ntp, const int *ti, const int *tj, const int *ts, int q, int r, const double *fixed, int typed){
  int rho = m - r - 1; double obj[MAXM], lb[MAXM], ub[MAXM];
  for (int x = 0; x < m - 1; x++){ obj[x] = e; lb[x] = 0; ub[x] = GRB_INFINITY; if (fixed && fixed[x + 1] >= 0) lb[x] = ub[x] = fixed[x + 1]; }
  GRBmodel *M = NULL; if (GRBnewmodel(env, &M, "lp", m - 1, obj, lb, ub, NULL, NULL)){ fprintf(stderr, "newmodel failed\n"); exit(2); }
  for (int p = 0; p < ntp; p++){
    int ind[3], n = 0; double val[3]; int a[3] = {ti[p], tj[p], ts[p]}; double c[3] = {1, 1, -1};
    for (int z = 0; z < 3; z++){ int f = -1; for (int y = 0; y < n; y++) if (ind[y] == a[z] - 1) f = y;
      if (f >= 0) val[f] += c[z]; else { ind[n] = a[z] - 1; val[n] = c[z]; n++; } }
    int rs = ((ts[p] - r - 1) % m + m) % m; int lo = rs >= m - rho, up = rs <= m - rho - 2;
    if (typed){ lo = lo && ti[p] > r && tj[p] > r; up = up && ti[p] <= r && tj[p] <= r; }
    if (!lo && !up) GRBaddconstr(M, n, ind, val, GRB_EQUAL, q, NULL);
    else { GRBaddconstr(M, n, ind, val, GRB_GREATER_EQUAL, q - lo, NULL); GRBaddconstr(M, n, ind, val, GRB_LESS_EQUAL, q + up, NULL); }
  }
  GRBoptimize(M); int st; GRBgetintattr(M, "Status", &st); double v = 1e30;
  if (st == GRB_OPTIMAL) GRBgetdblattr(M, "ObjVal", &v); else { fprintf(stderr, "LP status %d\n", st); exit(3); }
  GRBfreemodel(M);
  return v + (double)e * q - (double)q * m + rho;
}
#define TK 5
typedef struct { double v; int G[8]; double W; } TRec;
static TRec tk[8][TK]; static int ntk[8];   /* 0 RT2, 1 RT3, 2 UA2, 3 UA3, 4 RT2/W, 5 RT3/W, 6 UA2/W, 7 UA3/W */
static double kth(int c){ return ntk[c] < TK ? 1e30 : tk[c][TK - 1].v; }
static void tpush(int c, double v, const int *G, double W){
  int pos = ntk[c]; for (int i = 0; i < ntk[c]; i++) if (v < tk[c][i].v - 1e-12){ pos = i; break; }
  if (pos >= TK) return; int last = ntk[c] < TK ? ntk[c] : TK - 1;
  for (int i = last; i > pos; i--) tk[c][i] = tk[c][i - 1];
  tk[c][pos].v = v; memcpy(tk[c][pos].G, G, 8 * sizeof(int)); tk[c][pos].W = W; if (ntk[c] < TK) ntk[c]++; }
int main(int argc, char **argv){
  if (argc < 7){ fprintf(stderr, "usage: ./enumlp3 m e K part nparts h4only\n"); return 1; }
  m = atoi(argv[1]); e = atoi(argv[2]); int K = atoi(argv[3]), part = atoi(argv[4]), np = atoi(argv[5]), h4only = atoi(argv[6]); d = e - 1;
  if (m > MAXM || d < 1 || d > 7 || 3 * e >= m) { fprintf(stderr, "bad parameters\n"); return 1; }
  if (GRBloadenv(&env, NULL)){ fprintf(stderr, "no Gurobi env\n"); return 2; }
  GRBsetintparam(env, "OutputFlag", 0); GRBsetintparam(env, "Threads", 1);
  int pid[MAXM][MAXM]; int npairs = 0;
  for (int i = 1; i < m; i++) for (int j = i; j < m; j++) pid[i][j] = ((i + j) % m) ? npairs++ : -1;
  double bRT2[MAXM], bUA2[MAXM]; long bW[MAXM]; int gRT2[MAXM][8], gUA2[MAXM][8], gW[MAXM][8];
  for (int x = 0; x < MAXM; x++){ bRT2[x] = bUA2[x] = 1e30; bW[x] = 1L << 60; }
  double bestUA2 = 1e30, bestRT2W = 1e30, bestUA2W = 1e30; int gRT2W[8], gUA2W[8]; long nS = 0, nUA = 0, nneg = 0, nWneg = 0, nH4 = 0;
  int s[8], kk[8]; long ncomb = 0; int lim = (K + 1) * m;
  long per = 1; for (int b = 0; b < d; b++) per *= K; tsz = 1; while (tsz < 4 * per) tsz <<= 1;
  tab = calloc(tsz, sizeof(Ent)); if (!tab){ fprintf(stderr, "no memory\n"); return 4; } for (long x = 0; x < tsz; x++) tab[x].gen = -1;
  for (int i = 0; i < d; i++) s[i] = i + 1;
  while (1){
    if (ncomb++ % np == part){
      curgen = ncomb;
      for (int i = 0; i < d; i++) kk[i] = 1;
      while (1){
        int w[MAXM], done[MAXM], G[8]; for (int x = 0; x < m; x++){ w[x] = 1 << 29; done[x] = 0; } w[0] = 0;
        for (int b = 0; b < d; b++) G[b] = m * kk[b] + s[b];
        int ok = 1;
        for (int it = 0; it < m; it++){
          int u = -1; for (int x = 0; x < m; x++) if (!done[x] && (u < 0 || w[x] < w[u])) u = x;
          if (w[u] >= lim){ ok = 0; break; }
          done[u] = 1;
          for (int b = 0; b < d; b++){ int v = w[u] + G[b], t = v % m; if (v < w[t]) w[t] = v; }
        }
        for (int b = 0; b < d && ok; b++) if (w[s[b]] != G[b]) ok = 0;
        int isgen[MAXM] = {0}; for (int b = 0; b < d; b++) isgen[s[b]] = 1;
        Key key; memset(&key, 0, sizeof key); int h4 = 0, ntp = 0; int ti[300], tj[300], ts[300];
        if (ok) for (int i = 1; i < m && ok; i++) for (int j = i; j < m; j++){
          int t = (i + j) % m; if (!t) continue;
          if (w[i] + w[j] == w[t]){ if (isgen[t]){ ok = 0; break; }
            int p = pid[i][j]; key.b[p >> 6] |= 1ULL << (p & 63); if (!isgen[i] && !isgen[j]) h4 = 1;
            ti[ntp] = i; tj[ntp] = j; ts[ntp] = t; ntp++; }
        }
        if (ok){
          int r = 0; for (int x = 1; x < m; x++) if (w[x] > w[r]) r = x;
          long c = w[r] - m + 1;
          if (c >= 4L * m + 1 && (h4 || !h4only)){
            long g = 0; for (int x = 1; x < m; x++) g += w[x] / m;
            long W = (long)e * (c - g) - c; nS++; int q = w[r] / m;
            if (W <= 0){ nWneg++; printf("WILF COUNTEREXAMPLE? W=%ld <%d", W, m); for (int b = 0; b < d; b++) printf(",%d", G[b]); printf(">\n"); fflush(stdout); }
            if (W < bW[r]){ bW[r] = W; memcpy(gW[r], G, sizeof G); }
            key.r = (uint8_t)r; key.q = (uint8_t)q; int isnew; Ent *E = find(&key, &isnew);
            if (isnew){ E->rt2 = solve(ntp, ti, tj, ts, q, r, NULL, 0); E->rt3 = solve(ntp, ti, tj, ts, q, r, NULL, 1); }
            double R2 = E->rt2, R3 = E->rt3; nH4 += h4;
            if (R2 < -1e-7 || R3 < -1e-7){ nneg++; printf("NEGATIVE RT2=%.6f RT3=%.6f <%d", R2, R3, m); for (int b = 0; b < d; b++) printf(",%d", G[b]); printf(">\n"); fflush(stdout); }
            if (R2 < bRT2[r]){ bRT2[r] = R2; memcpy(gRT2[r], G, sizeof G); }
            if (W > 0){
              if (R2 < kth(0)) tpush(0, R2, G, W); if (R3 < kth(1)) tpush(1, R3, G, W);
              if (R2 / W < kth(4)) tpush(4, R2 / W, G, W); if (R3 / W < kth(5)) tpush(5, R3 / W, G, W);
              double fx[MAXM]; int fxset = 0;
              for (int typed = 0; typed <= 1; typed++){
                double lb = typed ? R3 : R2; int cu = typed ? 3 : 2, cr = typed ? 7 : 6;
                if (lb < kth(cu) - 1e-9 || lb / W < kth(cr) - 1e-12 || (!typed && lb < bUA2[r] - 1e-9)){
                  if (!fxset){ for (int x = 0; x < m; x++) fx[x] = -1; for (int b = 0; b < d; b++){ int gs = s[b]; fx[gs] = q - kk[b] - (gs > r ? 1 : 0); } fxset = 1; }
                  double U = solve(ntp, ti, tj, ts, q, r, fx, typed); nUA++;
                  if (U < kth(cu)) tpush(cu, U, G, W); if (U / W < kth(cr)) tpush(cr, U / W, G, W);
                  if (!typed && U < bUA2[r]){ bUA2[r] = U; memcpy(gUA2[r], G, sizeof G); }
                  if (U < -1e-7){ printf("NEGATIVE %s=%.6f\n", typed ? "UA3" : "UA2", U); fflush(stdout); }
                }
              }
            }
          }
        }
        int i = d - 1; while (i >= 0 && kk[i] == K){ kk[i] = 1; i--; } if (i < 0) break; kk[i]++;
      }
    }
    int i = d - 1; while (i >= 0 && s[i] == m - d + i) i--; if (i < 0) break; s[i]++; for (int j = i + 1; j < d; j++) s[j] = s[j - 1] + 1;
  }
#define PG(arr) do { printf(" <%d", m); for (int b = 0; b < d; b++) printf(",%d", (arr)[b]); printf(">"); } while (0)
  printf("SUMMARY m=%d e=%d K=%d part=%d/%d h4only=%d S=%ld height>=4:%ld keys=%ld UAsolves=%ld negRT=%ld W<=0:%ld\n", m, e, K, part, np, h4only, nS, nH4, tn, nUA, nneg, nWneg);
  for (int r = 1; r < m; r++) if (bW[r] < (1L << 60)){
    printf("r=%d minRT2=%.4f", r, bRT2[r]); PG(gRT2[r]); printf(" minUA2=%.4f", bUA2[r]); PG(gUA2[r]); printf(" minW=%ld", bW[r]); PG(gW[r]); printf("\n"); }
  const char *nm[8] = {"RT2", "RT3", "UA2", "UA3", "RT2/W", "RT3/W", "UA2/W", "UA3/W"};
  for (int c = 0; c < 8; c++) for (int i = 0; i < ntk[c]; i++){ printf("TOP %s %d %.6f W=%.0f", nm[c], i, tk[c][i].v, tk[c][i].W); PG(tk[c][i].G); printf("\n"); }
  return 0;
}
