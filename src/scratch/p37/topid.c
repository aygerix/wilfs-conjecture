/* topid: window accounting for TRUNC3 (lead, 2026-10-21).
 * A c [1, m-1], |A| = d, e = d + 1, U = 3A' + mN with 3A' covering Z/m, c = c(U), L = U n [0, c), l = |L|.
 * Window W = [c, c + m).  TypeM = {y in W : y - m in U}; Top = W \ TypeM (then y = sigma_{y mod m} in 3A').
 * Top1 = Top n (A + L); Top2 = Top \ Top1 (then every decomposition y = a + v, v in 2A', has v >= c).
 * Pi = {(a, x) in A x L : a + x in W}; PiM = pairs of Pi landing in TypeM; Ov = |Pi \ PiM| - |Top1| (multiplicity);
 * Nlt = #{(a, x) in A x L : a + x < c}; G0 = gaps of U in [0, c - m) (empty if c <= m).
 * Identity ID-TOP:  e*l - c = Nlt + |PiM| + Ov + |L n [0, c-m)| + (m - c) - |Top2|.
 * Checks the identity on every covering A and reports per (U = T / U != T): min of e*l - c, failures and minimum slack
 * of the crude sufficient condition CR: |Top2| + |G0| <= Nlt + max(m - c, 0), the largest |Top2|, and minimizers.
 * mode R: ./topid R d mlo mhi part np   (exhaustive, same pruned DFS as trunc3n) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXM 256
#define MAXV (4 * MAXM)
#define INF (1 << 29)
static int m, d, e;
static long binom3(int n){ return (long)n * (n - 1) * (n - 2) / 6; }
typedef struct { long v; int A[64], mm; long c, l, t2, nlt, pim, ov, g0; } rec;
static rec best[2][7]; static double rbest[2] = {1e18, 1e18}; /* [ne][0] = min W_e(U), [1] = min CR slack, [2] = max Top2 */
static long cnt[2], crfail[2], idfail, k1fail[2], k2fail[2], ncgm[2]; static long k1min[2] = {1L << 40, 1L << 40}, k2min[2] = {1L << 40, 1L << 40};
static void stash(rec *r, long v, const int *a, long c, long l, long t2, long nlt, long pim, long ov, long g0){
  r->v = v; memcpy(r->A, a, sizeof(int) * d); r->mm = m; r->c = c; r->l = l; r->t2 = t2; r->nlt = nlt; r->pim = pim; r->ov = ov; r->g0 = g0; }
static void leaf(const int *a){
  static int sig[MAXM], nw[MAXM], tau[MAXM]; static char inU[MAXV], in2[MAXV], top1[MAXV];
  for (int s = 0; s < m; s++) sig[s] = INF; sig[0] = 0;
  for (int round = 0; round < 3; round++){
    memcpy(nw, sig, sizeof(int) * m);
    for (int s = 0; s < m; s++) if (sig[s] < INF) for (int i = 0; i < d; i++){ int v = sig[s] + a[i], t = v % m; if (v < nw[t]) nw[t] = v; }
    memcpy(sig, nw, sizeof(int) * m);
  }
  int M = 0; for (int s = 0; s < m; s++){ if (sig[s] >= INF) return; if (sig[s] > M) M = sig[s]; }
  long c = M - m + 1; if (c <= 0) return;
  int top = c + m; /* integers 0..top-1 */
  memset(inU, 0, top); memset(in2, 0, top); memset(top1, 0, top);
  for (int x = 0; x < top; x++) inU[x] = (x >= sig[x % m]);
  /* 2A' as integers: 0, a_i, a_i + a_j */
  in2[0] = 1; for (int i = 0; i < d; i++){ if (a[i] < top) in2[a[i]] = 1; for (int j = i; j < d; j++) if (a[i] + a[j] < top) in2[a[i] + a[j]] = 1; }
  long l = 0; for (int x = 0; x < c; x++) l += inU[x];
  long nlt = 0, pim = 0, npi = 0;
  for (int i = 0; i < d; i++) for (int x = 0; x < c; x++) if (inU[x]){
    int y = a[i] + x;
    if (y < c) nlt++;
    else if (y < c + m){ npi++; if (y - m >= 0 && inU[y - m]) pim++; }
  }
  long ntop = 0, nt1 = 0;
  for (int y = c; y < c + m; y++){
    if (y - m >= 0 && inU[y - m]) continue;
    ntop++;
    int ok = 0; for (int i = 0; i < d && !ok; i++){ int v = y - a[i]; if (v >= 0 && v < c && inU[v]) ok = 1; }
    if (ok){ nt1++; top1[y] = 1; }
  }
  long t2 = ntop - nt1, ov = (npi - pim) - nt1;
  long lcm = 0, g0 = 0; for (int x = 0; x < c - m; x++){ if (inU[x]) lcm++; else g0++; }
  long W = (long)e * l - c;
  if (W != nlt + pim + ov + lcm + (m - c) - t2){ idfail++; if (idfail < 5){ printf("IDFAIL m=%d A=", m); for (int i = 0; i < d; i++) printf("%d,", a[i]); printf("\n"); } }
  memcpy(tau, sig, sizeof(int) * m); int ch = 1;
  while (ch){ ch = 0; for (int s = 0; s < m; s++) for (int i = 0; i < d; i++){ int v = tau[s] + a[i], t = v % m; if (v < tau[t]){ tau[t] = v; ch = 1; } } }
  int ne = 0; for (int s = 0; s < m; s++) if (tau[s] != sig[s]){ ne = 1; break; }
  long crs = nlt + (m > c ? m - c : 0) - t2 - g0;
  cnt[ne]++; if (crs < 0) crfail[ne]++;
  if (c > m){ ncgm[ne]++; long k1 = pim - g0, k2 = nlt + ov - t2;   /* K1: |G0| <= |PiM|;  K2: |Top2| <= Nlt + Ov */
    if (k1 < 0) k1fail[ne]++; if (k2 < 0) k2fail[ne]++; if (k1 < k1min[ne]){ k1min[ne] = k1; stash(&best[ne][3], k1, a, c, l, t2, nlt, pim, ov, g0); }
    if (k2 < k2min[ne]){ k2min[ne] = k2; stash(&best[ne][4], k2, a, c, l, t2, nlt, pim, ov, g0); }
    if (ncgm[ne] == 1 || W < best[ne][5].v) stash(&best[ne][5], W, a, c, l, t2, nlt, pim, ov, g0);          /* c > m: min W */
    double rt = (double)e * l / c; if (rt < rbest[ne]){ rbest[ne] = rt; stash(&best[ne][6], W, a, c, l, t2, nlt, pim, ov, g0); } }  /* c > m: min ratio */
  if (cnt[ne] == 1 || W < best[ne][0].v) stash(&best[ne][0], W, a, c, l, t2, nlt, pim, ov, g0);
  if (cnt[ne] == 1 || crs < best[ne][1].v) stash(&best[ne][1], crs, a, c, l, t2, nlt, pim, ov, g0);
  if (cnt[ne] == 1 || t2 > best[ne][2].v) stash(&best[ne][2], t2, a, c, l, t2, nlt, pim, ov, g0);
}
static int part, np; static long nsplit;
static void dfs(int k, int *a, char *S1, char *S2, char *S3, int cnt3){
  if (k == 2 && k < d && (nsplit++ % np != part)) return;
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
static void prec(const char *tag, const rec *r){
  printf(" %s=%ld [m=%d c=%ld l=%ld Top2=%ld Nlt=%ld PiM=%ld Ov=%ld G0=%ld A={", tag, r->v, r->mm, r->c, r->l, r->t2, r->nlt, r->pim, r->ov, r->g0);
  for (int i = 0; i < d; i++) printf("%s%d", i ? "," : "", r->A[i]); printf("}]"); }
int main(int argc, char **argv){
  d = atoi(argv[2]); int mlo = atoi(argv[3]), mhi = atoi(argv[4]); e = d + 1; part = atoi(argv[5]); np = atoi(argv[6]);
  for (m = mlo; m <= mhi; m++){
    if (d > m - 1) continue; nsplit = 0;
    int a[64]; char S1[MAXM] = {0}, S2[MAXM] = {0}, S3[MAXM] = {0}; S1[0] = S2[0] = S3[0] = 1;
    dfs(0, a, S1, S2, S3, 1);
  }
  printf("topid d=%d m=%d..%d part %d/%d: idfail=%ld\n", d, mlo, mhi, part, np, idfail);
  for (int ne = 0; ne < 2; ne++){
    printf("%s count=%ld CRfail=%ld [c>m: %ld; K1 fail %ld min %ld; K2 fail %ld min %ld]", ne ? "U!=T" : "U==T", cnt[ne], crfail[ne], ncgm[ne], k1fail[ne], k1min[ne], k2fail[ne], k2min[ne]);
    if (cnt[ne]){ prec("minW", &best[ne][0]); prec("minCR", &best[ne][1]); prec("maxTop2", &best[ne][2]); if (ncgm[ne]){ prec("minK1", &best[ne][3]); prec("minK2", &best[ne][4]); prec("c>m minW", &best[ne][5]); printf(" c>m minratio=%.4f", rbest[ne]); prec("at", &best[ne][6]); } }
    printf("\n");
  }
  return 0;
}
