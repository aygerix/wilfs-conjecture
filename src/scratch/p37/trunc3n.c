/* trunc3n: TRUNC3 split by U = T versus U != T (lead, 2026-10-21).
 * Same objects as trunc3.c: A c [1, m-1], |A| = d, e = d + 1, sigma_s = min(3A' n (s + mZ)), U = {sigma_s} + mN, covering
 * hypothesis 3A' = Z/m.  T = <A, m>; its Apery set tau w.r.t. m is obtained from sigma by unbounded relaxation.  U != T iff
 * sigma != tau somewhere (then c(U) > 4 min A by LOW-AGREE).
 * mode R: ./trunc3n R d mlo mhi part np        exhaustive over all A with |A| = d, by depth-first search with the pruning
 *          |3A_j' mod m| + C(d+3,3) - C(j+3,3) < m  (A_j = first j chosen elements; the others add at most that many
 *          residues); work split round-robin over the pairs (a_1, a_2)
 * mode N: ./trunc3n N d mlo mhi restarts steps seed   hill climbing on e*l/c restricted to U != T
 * mode P: as N, restricted to U != T and c(U) > m (the residue-descent residual's regime, c = m + r + 1)
 * Per m: #covering, #U!=T, failures, min ratio (all, and U != T) with minimizers; mode R also buckets min ratio by
 * t = ceil(c / mu) for all and for U != T. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXM 256
#define INF (1 << 29)
static int m, d, e;
static long binom3(int n){ return (long)n * (n - 1) * (n - 2) / 6; }
/* returns 0 if not covering; else fills c, l, *ne (1 if U != T) */
static int eval(const int *a, long *c, long *l, int *ne){
  static int sig[MAXM], nw[MAXM], tau[MAXM];
  for (int s = 0; s < m; s++) sig[s] = INF; sig[0] = 0;
  for (int round = 0; round < 3; round++){
    memcpy(nw, sig, sizeof(int) * m);
    for (int s = 0; s < m; s++) if (sig[s] < INF) for (int i = 0; i < d; i++){ int v = sig[s] + a[i], t = v % m; if (v < nw[t]) nw[t] = v; }
    memcpy(sig, nw, sizeof(int) * m);
  }
  int M = 0; long g = 0;
  for (int s = 0; s < m; s++){ if (sig[s] >= INF) return 0; if (sig[s] > M) M = sig[s]; g += sig[s] / m; }
  long cc = M - m + 1; if (cc < 0) cc = 0;
  *c = cc; *l = cc - g;
  memcpy(tau, sig, sizeof(int) * m); int ch = 1;
  while (ch){ ch = 0; for (int s = 0; s < m; s++) for (int i = 0; i < d; i++){ int v = tau[s] + a[i], t = v % m; if (v < tau[t]){ tau[t] = v; ch = 1; } } }
  *ne = 0; for (int s = 0; s < m; s++) if (tau[s] != sig[s]){ *ne = 1; break; }
  return 1;
}
typedef struct { double r; long c, l; int A[64], mm; } rec;
static void upd(rec *b, double r, long c, long l, const int *a){ if (r < b->r){ b->r = r; b->c = c; b->l = l; b->mm = m; memcpy(b->A, a, sizeof(int) * d); } }
static void prt(const char *tag, const rec *b){ if (b->r > 1e17){ printf(" %s=none", tag); return; }
  printf(" %s=%.4f (m=%d c=%ld l=%ld) A={", tag, b->r, b->mm, b->c, b->l); for (int i = 0; i < d; i++) printf("%s%d", i ? "," : "", b->A[i]); printf("}"); }
static rec ball, bne, bkt[64], bktne[64];
static long ncov, nne, fails, failsne;
static void leaf(const int *a){
  long c, l; int ne;
  if (!eval(a, &c, &l, &ne)) return;
  ncov++; if (ne) nne++;
  if (c == 0) return;
  double rt = (double)e * l / c; if ((long)e * l < c){ fails++; if (ne) failsne++; }
  int mu = a[0]; for (int i = 1; i < d; i++) if (a[i] < mu) mu = a[i];
  int t = (int)((c + mu - 1) / mu); if (t > 63) t = 63;
  upd(&ball, rt, c, l, a); upd(&bkt[t], rt, c, l, a);
  if (ne){ upd(&bne, rt, c, l, a); upd(&bktne[t], rt, c, l, a); }
}
/* depth-first search with residue-coverage pruning; S1, S2, S3 = residues of 1-, 2-, 3-sums of A_k' */
static int part, np; static long nsplit;
static void dfs(int k, int *a, char *S1, char *S2, char *S3, int cnt3){
  if (k == 2 && k < d && (nsplit++ % np != part)) return;   /* work split: round-robin over the first two elements */
  if (k == d){ if (cnt3 == m && (d > 2 || (nsplit++ % np == part))) leaf(a); return; }
  for (int x = (k ? a[k - 1] + 1 : 1); x <= m - 1 - (d - 1 - k); x++){
    char T1[MAXM], T2[MAXM], T3[MAXM];
    memcpy(T1, S1, m); memcpy(T2, S2, m); memcpy(T3, S3, m);
    T1[x] = 1;
    for (int s = 0; s < m; s++) if (T1[s]) T2[(s + x) % m] = 1;
    int c3 = 0;
    for (int s = 0; s < m; s++) if (T2[s]) T3[(s + x) % m] = 1;
    for (int s = 0; s < m; s++) c3 += T3[s];
    if (c3 + binom3(d + 3) - binom3(k + 4) < m) continue;
    a[k] = x; dfs(k + 1, a, T1, T2, T3, c3);
  }
}
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int cmpint(const void *x, const void *y){ return *(const int *)x - *(const int *)y; }
static void reset(rec *b){ b->r = 1e18; }
int main(int argc, char **argv){
  char mode = argv[1][0]; d = atoi(argv[2]); int mlo = atoi(argv[3]), mhi = atoi(argv[4]); e = d + 1;
  for (int t = 0; t < 64; t++){ reset(&bkt[t]); reset(&bktne[t]); }
  rec gall, gne; reset(&gall); reset(&gne);
  for (m = mlo; m <= mhi; m++){
    if (d > m - 1) continue;
    reset(&ball); reset(&bne); ncov = nne = fails = failsne = 0; nsplit = 0;
    int a[64];
    if (mode == 'R'){
      part = atoi(argv[5]); np = atoi(argv[6]);
      char S1[MAXM] = {0}, S2[MAXM] = {0}, S3[MAXM] = {0}; S1[0] = S2[0] = S3[0] = 1;
      dfs(0, a, S1, S2, S3, 1);
    } else {
      int restarts = atoi(argv[5]), steps = atoi(argv[6]); rs ^= (unsigned long long)atoi(argv[7]) * 2654435761ULL + m;
      for (int rr = 0; rr < restarts; rr++){
        long c = 0, l = 0; int ne = 0, tries = 0, ok = 0;
        while (tries++ < 4000){
          char used[MAXM] = {0}; for (int i = 0; i < d; i++){ int x; do x = 1 + rnd() % (m - 1); while (used[x]); used[x] = 1; a[i] = x; }
          if (eval(a, &c, &l, &ne) && c > 0 && ne && (mode != 'P' || c > m)){ ok = 1; break; }
        }
        if (!ok) continue;
        double cur = (double)e * l / c;
        for (int st = 0; st < steps; st++){
          int b[64]; memcpy(b, a, sizeof b); int i = rnd() % d, x, tries2 = 0;
          do { x = (rnd() & 1) ? 1 + rnd() % (m - 1) : b[i] + (int)(rnd() % 7) - 3; tries2++; } while ((x < 1 || x > m - 1) && tries2 < 50);
          if (x < 1 || x > m - 1) continue;
          int dup = 0; for (int j = 0; j < d; j++) if (j != i && b[j] == x) dup = 1; if (dup) continue;
          b[i] = x; long c2, l2; int ne2;
          if (!eval(b, &c2, &l2, &ne2) || c2 == 0 || !ne2 || (mode == 'P' && c2 <= m)) continue;
          double nr = (double)e * l2 / c2;
          if (nr <= cur){ memcpy(a, b, sizeof a); cur = nr; c = c2; l = l2; }
        }
        int srt[64]; memcpy(srt, a, sizeof srt); qsort(srt, d, sizeof(int), cmpint);
        leaf(srt);
      }
    }
    if (ncov == 0) continue;
    printf("%c d=%d e=%d m=%d covering=%ld UneT=%ld FAILS=%ld FAILSne=%ld", mode, d, e, m, ncov, nne, fails, failsne);
    prt("minratio", &ball); prt("minratioNE", &bne); printf("\n"); fflush(stdout);
    if (ball.r < gall.r) gall = ball; if (bne.r < gne.r) gne = bne;
  }
  printf("GLOBAL"); prt("minratio", &gall); prt("minratioNE", &gne); printf("\n");
  if (mode == 'R') for (int t = 1; t < 64; t++) if (bkt[t].r < 1e17){ printf("BUCKET t=%d", t); prt("all", &bkt[t]); prt("NE", &bktne[t]); printf("\n"); }
  return 0;
}
