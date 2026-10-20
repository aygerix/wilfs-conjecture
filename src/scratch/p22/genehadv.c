/* Depth-four LOW search (lead, 2026-10-20). q = 4: W = rho + Lam - sum K + ... ; DEPTH4-EH: W >= e - h + Lam + Z.
   Residual for Wilf at q = 4: LOW4 := Lam + Z < h - e.  Annealing maximizes F = (h - e) - (Lam + Z) - 1000|q - 4|
   (F > 0 means LOW4).  Prints the class counts a, b, gamma, eta (generators in (m,m+h), [m+h,2m+h), [2m+h,3m+h),
   [3m+h,4m+h)), level counts n_k = #{x in Ap : lambda(x) = k}, R = #{K = 1}, Z, W.
   usage: ./lowd4 seed mlo mhi dlo dhi iters */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MM 600
#define DD 40
static int m, d, gen[DD], w[MM], nu[DD][MM], minimal[DD], ord[MM];
static unsigned long long rs;
static unsigned rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static int apery(void){
  static int done[MM]; for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){
    int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return 0; done[b] = 1;
    for (int a = 0; a < d; a++){ int j = (b + gen[a]) % m, v = w[b] + gen[a]; if (w[j] < 0 || v < w[j]) w[j] = v; }
  }
  return 1;
}
static int cmpw(const void *x, const void *y){ return w[*(int*)x] - w[*(int*)y]; }
typedef struct { long F, W, Lam, Z, R, L2, a0; int e, q, h, rho, a, b, g, eta, n[5]; } Res;
static int eval(Res *r){
  if (!apery()) return 0;
  int e = 1;
  for (int a = 0; a < d; a++){
    int rr = gen[a] % m; minimal[a] = (rr != 0 && w[rr] == gen[a]);
    if (minimal[a]) for (int i = 1; i < m; i++){ int j = (rr - i + m) % m; if (j && w[i] + w[j] == gen[a]){ minimal[a] = 0; break; } }
    for (int b = 0; b < a; b++) if (minimal[b] && gen[b] == gen[a]) minimal[a] = 0;
    e += minimal[a];
  }
  long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long c = M - m + 1; int q = (int)((c + m - 1) / m); int h = (int)(c - (long)(q - 1) * m), rho = m - h;
  r->e = e; r->q = q; r->h = h; r->rho = rho;
  r->W = (long)e * (c - g) - c;
  for (int i = 0; i < m; i++) ord[i] = i;
  qsort(ord, m, sizeof(int), cmpw);
  for (int a = 0; a < d; a++) if (minimal[a]){
    int rr = gen[a] % m;
    for (int t = 0; t < m; t++){ int i = ord[t], j = (i - rr + m) % m; nu[a][i] = (w[j] + gen[a] == w[i]) ? nu[a][j] + 1 : 0; }
  }
  long Lam = 0, Z = 0, R = 0, sumU = 0, a0 = 0;
  for (int k = 0; k < 5; k++) r->n[k] = 0;
  for (int i = 0; i < m; i++){
    long x = w[i], lam = (M - x) / m; if (lam < 5) r->n[lam]++;
    long K = q - lam;
    for (int a = 0; a < d; a++) if (minimal[a]){
      if (nu[a][i] > 0) K -= nu[a][i] * ((M - (x - gen[a])) / m - lam);
      int j = (i + gen[a]) % m; if (w[j] != x + gen[a]) Lam += (nu[a][i] + 1) * lam;
    }
    if (K < 0) Z -= K; if (K == 1) R++;
    { int U = 0; for (int a = 0; a < d; a++) if (minimal[a] && nu[a][i] > 0) U++; long cap = 4 - lam; if (cap < 0) cap = 0; sumU += U < cap ? U : cap; if (lam == 0) a0++; }
  }
  r->a = r->b = r->g = r->eta = 0;
  for (int a = 0; a < d; a++) if (minimal[a]){ long t = gen[a] - m;
    if (t < h) r->a++; else if (t < m + h) r->b++; else if (t < 2 * m + h) r->g++; else r->eta++; }
  r->Lam = Lam; r->Z = Z; r->R = R; r->a0 = a0;
  r->L2 = (long)(e - 1) * (m - a0) - sumU;
  { long ell = 0; for (int i = 0; i < m; i++) ell += (M - w[i]) / m; r->F = (long)(q - 1) * m - (long)e * (ell - 1) - (q < 2 ? 1000000L : 0) - (e < 3 ? 1000000L : 0); }
  return 1;
}
static void pr(const char *tag, Res *r){
  printf("%s L2=%ld a0=%ld F=%ld m=%d e=%d q=%d h=%d rho=%d W=%ld Lam=%ld Z=%ld R=%ld abge=%d,%d,%d,%d n0..4=%d,%d,%d,%d,%d gens=", tag, r->L2, r->a0, r->F, m, r->e, r->q, r->h, r->rho, r->W, r->Lam, r->Z, r->R, r->a, r->b, r->g, r->eta, r->n[0], r->n[1], r->n[2], r->n[3], r->n[4]);
  for (int a = 0; a < d; a++) if (minimal[a]) printf("%d,", gen[a]); printf("\n"); fflush(stdout);
}
static int KM = 4;
static int randgen(void){ int x; do { x = m + 1 + rnd() % (KM * m); } while (x % m == 0); return x; }
int main(int argc, char **argv){
  rs = 88172645463325252ULL ^ (unsigned long long)atoi(argv[1]) * 2654435761ULL;
  int mlo = atoi(argv[2]), mhi = atoi(argv[3]), dlo = atoi(argv[4]), dhi = atoi(argv[5]); long iters = atol(argv[6]);
  long bestF = -1000000000L, lowcount = 0; long minWlow = 1L << 40;
  for (int restart = 0; ; restart++){
    m = mlo + rnd() % (mhi - mlo + 1); d = dlo + rnd() % (dhi - dlo + 1);
    for (int a = 0; a < d; a++) gen[a] = randgen();
    Res cur; if (!eval(&cur)) continue;
    for (long it = 0; it < iters; it++){
      int save[DD]; memcpy(save, gen, sizeof gen);
      int a = rnd() % d, kind = rnd() % 3;
      if (kind == 0) gen[a] = randgen();
      else { int dl = 1 + rnd() % (kind == 1 ? 3 : m); gen[a] += (rnd() & 1) ? dl : -dl; if (gen[a] <= m || gen[a] % m == 0) gen[a] = randgen(); }
      Res nr; if (!eval(&nr)){ memcpy(gen, save, sizeof gen); continue; }
      if (nr.F > bestF){ bestF = nr.F; pr("best", &nr); }
      if (nr.F > 0){ lowcount++; pr("GENEHFAIL", &nr); }
      if (nr.W < 0) pr("WILFFAIL", &nr);
      if (nr.q == 4 && nr.L2 > nr.Lam + nr.Z) pr("L2BUG", &nr);
      if (nr.F >= cur.F || (rnd() % 1000) < 20) cur = nr; else memcpy(gen, save, sizeof gen);
    }
    if (restart % 50 == 0){ printf("restart %d bestF %ld low4 %ld minWlow %ld\n", restart, bestF, lowcount, minWlow); fflush(stdout); }
  }
}
