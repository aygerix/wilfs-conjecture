/* enumlp: exhaustive RT2 / UA2 minimization over the exact-MILP domain of kunz_cert_milp.py --open --h4 (lead, 2026-10-21).
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
 * usage: LD_LIBRARY_PATH=$HOME/gurobi1303/linux64/lib ./enumlp m e K part nparts */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "gurobi_c.h"
#define MAXM 24
typedef struct { uint64_t b[4]; uint8_t r, q; } Key;
typedef struct { Key k; long gen; double rt2; } Ent;
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
static double solve(int ntp, const int *ti, const int *tj, const int *ts, int q, int r, const double *fixed){
  int rho = m - r - 1; double obj[MAXM], lb[MAXM], ub[MAXM];
  for (int x = 0; x < m - 1; x++){ obj[x] = e; lb[x] = 0; ub[x] = GRB_INFINITY; if (fixed && fixed[x + 1] >= 0) lb[x] = ub[x] = fixed[x + 1]; }
  GRBmodel *M = NULL; if (GRBnewmodel(env, &M, "lp", m - 1, obj, lb, ub, NULL, NULL)){ fprintf(stderr, "newmodel failed\n"); exit(2); }
  for (int p = 0; p < ntp; p++){
    int ind[3], n = 0; double val[3]; int a[3] = {ti[p], tj[p], ts[p]}; double c[3] = {1, 1, -1};
    for (int z = 0; z < 3; z++){ int f = -1; for (int y = 0; y < n; y++) if (ind[y] == a[z] - 1) f = y;
      if (f >= 0) val[f] += c[z]; else { ind[n] = a[z] - 1; val[n] = c[z]; n++; } }
    int rs = ((ts[p] - r - 1) % m + m) % m; int lo = rs >= m - rho, up = rs <= m - rho - 2;
    if (!lo && !up) GRBaddconstr(M, n, ind, val, GRB_EQUAL, q, NULL);
    else { GRBaddconstr(M, n, ind, val, GRB_GREATER_EQUAL, q - lo, NULL); GRBaddconstr(M, n, ind, val, GRB_LESS_EQUAL, q + up, NULL); }
  }
  GRBoptimize(M); int st; GRBgetintattr(M, "Status", &st); double v = 1e30;
  if (st == GRB_OPTIMAL) GRBgetdblattr(M, "ObjVal", &v); else { fprintf(stderr, "LP status %d\n", st); exit(3); }
  GRBfreemodel(M);
  return v + (double)e * q - (double)q * m + rho;
}
int main(int argc, char **argv){
  if (argc < 6){ fprintf(stderr, "usage: ./enumlp m e K part nparts\n"); return 1; }
  m = atoi(argv[1]); e = atoi(argv[2]); int K = atoi(argv[3]), part = atoi(argv[4]), np = atoi(argv[5]); d = e - 1;
  if (m > MAXM || d < 1 || d > 7 || 3 * e >= m) { fprintf(stderr, "bad parameters\n"); return 1; }
  if (GRBloadenv(&env, NULL)){ fprintf(stderr, "no Gurobi env\n"); return 2; }
  GRBsetintparam(env, "OutputFlag", 0); GRBsetintparam(env, "Threads", 1);
  int pid[MAXM][MAXM]; int npairs = 0;
  for (int i = 1; i < m; i++) for (int j = i; j < m; j++) pid[i][j] = ((i + j) % m) ? npairs++ : -1;
  double bRT2[MAXM], bUA2[MAXM]; long bW[MAXM]; int gRT2[MAXM][8], gUA2[MAXM][8], gW[MAXM][8];
  for (int x = 0; x < MAXM; x++){ bRT2[x] = bUA2[x] = 1e30; bW[x] = 1L << 60; }
  double bestUA2 = 1e30, bestRT2W = 1e30, bestUA2W = 1e30; int gRT2W[8], gUA2W[8]; long nS = 0, nUA = 0, nneg = 0, nWneg = 0;
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
          if (c >= 4L * m + 1 && h4){
            long g = 0; for (int x = 1; x < m; x++) g += w[x] / m;
            long W = (long)e * (c - g) - c; nS++; int q = w[r] / m;
            if (W <= 0){ nWneg++; printf("WILF COUNTEREXAMPLE? W=%ld <%d", W, m); for (int b = 0; b < d; b++) printf(",%d", G[b]); printf(">\n"); fflush(stdout); }
            if (W < bW[r]){ bW[r] = W; memcpy(gW[r], G, sizeof G); }
            key.r = (uint8_t)r; key.q = (uint8_t)q; int isnew; Ent *E = find(&key, &isnew);
            if (isnew) E->rt2 = solve(ntp, ti, tj, ts, q, r, NULL);
            double R2 = E->rt2;
            if (R2 < -1e-7){ nneg++; printf("NEGATIVE RT2=%.6f <%d", R2, m); for (int b = 0; b < d; b++) printf(",%d", G[b]); printf(">\n"); fflush(stdout); }
            if (R2 < bRT2[r]){ bRT2[r] = R2; memcpy(gRT2[r], G, sizeof G); }
            if (W > 0 && R2 / W < bestRT2W){ bestRT2W = R2 / W; memcpy(gRT2W, G, sizeof G); }
            if (R2 < bestUA2 - 1e-9 || (W > 0 && R2 / W < bestUA2W - 1e-12) || R2 < bUA2[r] - 1e-9){
              double fx[MAXM]; for (int x = 0; x < m; x++) fx[x] = -1;
              for (int b = 0; b < d; b++){ int gs = s[b]; fx[gs] = q - kk[b] - (gs > r ? 1 : 0); }
              double U2 = solve(ntp, ti, tj, ts, q, r, fx); nUA++;
              if (U2 < bUA2[r]){ bUA2[r] = U2; memcpy(gUA2[r], G, sizeof G); }
              if (U2 < bestUA2) bestUA2 = U2;
              if (W > 0 && U2 / W < bestUA2W){ bestUA2W = U2 / W; memcpy(gUA2W, G, sizeof G); }
            }
          }
        }
        int i = d - 1; while (i >= 0 && kk[i] == K){ kk[i] = 1; i--; } if (i < 0) break; kk[i]++;
      }
    }
    int i = d - 1; while (i >= 0 && s[i] == m - d + i) i--; if (i < 0) break; s[i]++; for (int j = i + 1; j < d; j++) s[j] = s[j - 1] + 1;
  }
#define PG(arr) do { printf(" <%d", m); for (int b = 0; b < d; b++) printf(",%d", (arr)[b]); printf(">"); } while (0)
  printf("SUMMARY m=%d e=%d K=%d part=%d/%d S=%ld keys=%ld UA2solves=%ld negRT2=%ld W<=0:%ld\n", m, e, K, part, np, nS, tn, nUA, nneg, nWneg);
  for (int r = 1; r < m; r++) if (bW[r] < (1L << 60)){
    printf("r=%d minRT2=%.4f", r, bRT2[r]); PG(gRT2[r]); printf(" minUA2=%.4f", bUA2[r]); PG(gUA2[r]); printf(" minW=%ld", bW[r]); PG(gW[r]); printf("\n"); }
  printf("minRT2/W=%.4f", bestRT2W); PG(gRT2W); printf(" minUA2/W=%.4f", bestUA2W); PG(gUA2W); printf("\n");
  return 0;
}
