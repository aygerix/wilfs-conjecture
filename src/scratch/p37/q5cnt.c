/* q5cnt: exhaustive test of the q = 5 counting decomposition (lead, 2026-10-21).
 * Domain: multiplicity m; d = e-1 generator residues (all subsets with dmin <= d <= dmax) with levels k_b in [1, L];
 * every chosen generator minimal; q = 5 (5m <= max Ap < 6m); every Apery element has all factorizations of length <= 3.
 * For a chosen factorization of each w_s (predecessor chain in increasing w): K_s = sum of generator levels,
 * sigma_s = w_s - m K_s (integer residue sum).  Identity (LEVEL1-THRESHOLD, level-weighted):
 *     l = 5m - sum K - N,   N = sum_s #{j >= 0 : sigma_s > jm + r}            (asserted on every S)
 * With K additive (K-graded: every factorization has the same level sum; asserted Kmax == Kmin), K* = max K and
 *     Delta = (e-1) m K* - e sum K  >= 0   (CH', asserted),   E = e N - (5 - K*)(e-1) m - rho,   W = Delta - E  (asserted).
 * For level-1 generators K = h, K* <= 3; the advisor's form uses K* := 3: Delta3 = 3(e-1)m - eH, E3 = eN - 2(e-1)m - rho.
 * Reports: counts (all / K-graded / level-1), failures of E3 <= 0 (level-1) and of E <= 0 (all K-graded), the worst cases
 * by E and by margin W among failures, with threshold-band counts of generator / pair / cubic cells
 * (band 0: sigma <= r, band 1: r < sigma <= m + r, band 2: sigma > m + r).
 * usage: ./q5cnt m L dmin dmax part nparts */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXM 40
#define TOP 6
typedef struct { long E, D, W, Nr, Nmr, SK; int m, d, r, rho, Ks, lev1, G[24], band[3][3]; } Rec;
static Rec topE[TOP], topW[TOP]; static int nE = 0, nW = 0;
static void push(Rec *arr, int *n, Rec *x, int byE){
  /* keep TOP records: byE: largest E; else smallest W */
  int pos = *n;
  for (int i = 0; i < *n; i++){ int better = byE ? (x->E > arr[i].E) : (x->W < arr[i].W); if (better){ pos = i; break; } }
  if (pos >= TOP) return;
  int last = (*n < TOP) ? *n : TOP - 1;
  for (int i = last; i > pos; i--) arr[i] = arr[i - 1];
  arr[pos] = *x; if (*n < TOP) (*n)++;
}
static void prec(const char *tag, Rec *x){
  printf("%s E=%ld Delta=%ld W=%ld | m=%d e=%d r=%d rho=%d K*=%d level1=%d | N(r)=%ld N(m+r)=%ld sumK=%ld | <%d", tag, x->E, x->D, x->W,
         x->m, x->d + 1, x->r, x->rho, x->Ks, x->lev1, x->Nr, x->Nmr, x->SK, x->m);
  for (int b = 0; b < x->d; b++) printf(",%d", x->G[b]);
  printf("> | bands (sigma<=r, r<sigma<=m+r, sigma>m+r): gens %d/%d/%d pairs %d/%d/%d cubics %d/%d/%d\n",
         x->band[0][0], x->band[0][1], x->band[0][2], x->band[1][0], x->band[1][1], x->band[1][2], x->band[2][0], x->band[2][1], x->band[2][2]);
}
int main(int argc, char **argv){
  if (argc < 7){ fprintf(stderr, "usage: ./q5cnt m L dmin dmax part nparts\n"); return 1; }
  int m = atoi(argv[1]), L = atoi(argv[2]), dmin = atoi(argv[3]), dmax = atoi(argv[4]), part = atoi(argv[5]), np = atoi(argv[6]);
  if (m > MAXM || dmax > 23 || dmax > m - 1) { fprintf(stderr, "bad parameters\n"); return 1; }
  long nS = 0, nG = 0, nL1 = 0, fE3 = 0, fE = 0, minW = 1L << 60; long ncomb = 0; int minWG[24] = {0}, minWd = 0; long perd[24] = {0};
  int lim = 6 * m;
  for (int d = dmin; d <= dmax; d++){
    int s[24], kk[24];
    for (int i = 0; i < d; i++) s[i] = i + 1;
    while (1){
      if (ncomb++ % np == part){
        for (int i = 0; i < d; i++) kk[i] = 1;
        while (1){
          int w[MAXM], done[MAXM], G[24]; for (int x = 0; x < m; x++){ w[x] = 1 << 29; done[x] = 0; } w[0] = 0;
          for (int b = 0; b < d; b++) G[b] = m * kk[b] + s[b];
          int ok = 1, order[MAXM];
          for (int it = 0; it < m; it++){
            int u = -1; for (int x = 0; x < m; x++) if (!done[x] && (u < 0 || w[x] < w[u])) u = x;
            if (w[u] >= lim){ ok = 0; break; }
            done[u] = 1; order[it] = u;
            for (int b = 0; b < d; b++){ int v = w[u] + G[b], t = v % m; if (v < w[t]) w[t] = v; }
          }
          for (int b = 0; b < d && ok; b++) if (w[s[b]] != G[b]) ok = 0;
          int r = 0; if (ok){ for (int x = 1; x < m; x++) if (w[x] > w[r]) r = x; if (w[r] < 5 * m) ok = 0; }
          if (ok){
            int hmx[MAXM], hmn[MAXM], Kmx[MAXM], Kmn[MAXM], Kc[MAXM], sg[MAXM], isg[MAXM] = {0};
            for (int b = 0; b < d; b++) isg[s[b]] = 1;
            hmx[0] = hmn[0] = Kmx[0] = Kmn[0] = Kc[0] = 0; sg[0] = 0;
            for (int it = 1; it < m && ok; it++){
              int x = order[it]; int f = 0; hmx[x] = -1; hmn[x] = 99; Kmx[x] = -1; Kmn[x] = 99;
              for (int b = 0; b < d; b++){
                int t = ((x - s[b]) % m + m) % m;
                if (w[t] == w[x] - G[b] && (t == 0 || w[t] > 0)){
                  if (t != 0 && isg[x]){ ok = 0; break; }   /* chosen generator decomposable */
                  if (hmx[t] + 1 > hmx[x]) hmx[x] = hmx[t] + 1; if (hmn[t] + 1 < hmn[x]) hmn[x] = hmn[t] + 1;
                  if (Kmx[t] + kk[b] > Kmx[x]) Kmx[x] = Kmx[t] + kk[b]; if (Kmn[t] + kk[b] < Kmn[x]) Kmn[x] = Kmn[t] + kk[b];
                  if (!f){ Kc[x] = Kc[t] + kk[b]; sg[x] = sg[t] + s[b]; f = 1; }
                }
              }
              if (!f) ok = 0;
              if (ok && hmx[x] > 3) ok = 0;
            }
            if (ok){
              int e = d + 1; long c = w[r] - m + 1; int rho = 5 * m - (int)c;
              long g = 0; for (int x = 1; x < m; x++) g += w[x] / m;
              long W = (long)e * (c - g) - c, SKc = 0, N = 0, Nr = 0, Nmr = 0;
              for (int x = 1; x < m; x++){ SKc += Kc[x]; int cnt = 0; for (int j = 0; sg[x] > j * m + r; j++) cnt++; N += cnt;
                if (sg[x] > r) Nr++; if (sg[x] > m + r) Nmr++; if (sg[x] > 2 * m + r){ fprintf(stderr, "third threshold!\n"); return 5; } }
              if ((long)e * (5L * m - SKc - N) - c != W){ fprintf(stderr, "IDENTITY FAILS\n"); return 6; }
              nS++; perd[d]++; int lev1 = 1; for (int b = 0; b < d; b++) if (kk[b] != 1) lev1 = 0; nL1 += lev1;
              if (W < minW){ minW = W; minWd = d; memcpy(minWG, G, sizeof G); }
              int Kgraded = 1; for (int x = 1; x < m; x++) if (Kmx[x] != Kmn[x]) Kgraded = 0;
              if (Kgraded){
                nG++; int Ks = 0; long SK = 0; for (int x = 1; x < m; x++){ SK += Kmx[x]; if (Kmx[x] > Ks) Ks = Kmx[x]; }
                long D = (long)(e - 1) * m * Ks - (long)e * SK; long E = (long)e * N - (long)(5 - Ks) * (e - 1) * m - rho;
                if (D < 0){ fprintf(stderr, "CH' FAILS\n"); return 7; }
                if (D - E != W){ fprintf(stderr, "W != Delta - E\n"); return 8; }
                Rec R; memset(&R, 0, sizeof R); R.m = m; R.d = d; R.r = r; R.rho = rho; R.Ks = Ks; R.lev1 = lev1; R.Nr = Nr; R.Nmr = Nmr; R.SK = SK;
                memcpy(R.G, G, sizeof G);
                for (int x = 1; x < m; x++){ int cl = hmx[x] - 1; int bd = sg[x] <= r ? 0 : (sg[x] <= m + r ? 1 : 2); if (cl >= 0 && cl < 3) R.band[cl][bd]++; }
                if (lev1){ long D3 = 3L * (e - 1) * m - (long)e * SK, E3 = (long)e * N - 2L * (e - 1) * m - rho;
                  if (E3 > 0){ fE3++; R.E = E3; R.D = D3; R.W = W; push(topE, &nE, &R, 1); push(topW, &nW, &R, 0); } }
                else if (E > 0){ fE++; R.E = E; R.D = D; R.W = W; push(topE, &nE, &R, 1); push(topW, &nW, &R, 0); }
              }
            }
          }
          int i = d - 1; while (i >= 0 && kk[i] == L){ kk[i] = 1; i--; } if (i < 0) break; kk[i]++;
        }
      }
      int i = d - 1; while (i >= 0 && s[i] == m - d + i) i--; if (i < 0) break; s[i]++; for (int j = i + 1; j < d; j++) s[j] = s[j - 1] + 1;
    }
  }
  printf("SUMMARY m=%d L=%d d=%d..%d part=%d/%d S=%ld Kgraded=%ld level1=%ld E3>0(level1)=%ld E>0(mixed)=%ld minW=%ld <%d", m, L, dmin, dmax, part, np,
         nS, nG, nL1, fE3, fE, minW, m);
  for (int b = 0; b < minWd; b++) printf(",%d", minWG[b]); printf(">  per-d:");
  for (int x = dmin; x <= dmax; x++) if (perd[x]) printf(" d%d:%ld", x, perd[x]); printf("\n");
  for (int i = 0; i < nE; i++) prec("topE", &topE[i]);
  for (int i = 0; i < nW; i++) prec("topW", &topW[i]);
  return 0;
}
