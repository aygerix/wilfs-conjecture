/* Adversarial search for T1 and Lemma U-FULL at large m (lead, 2026-10-20).
   T1(p): sum_{x in Ap} K_p(x) <= m - e, K_p(x) = C_p(x) - sum_a nu_a(x)(C_p(x) - C_p(x - n_a)).
   U-FULL(p): same with nu replaced by the lex-max factorization f(x) (>= K_p pointwise; f(Ap) is an order ideal with
   bijective residues).  Annealing over generator sets <m, n_1..n_d>, n_a in (m, kmax*m).
   Also checks the walk form of Wilf: W = rho + Lam + E/m + mean_p S_p - S_{p*} (asserted exactly via m*W).
   usage: ./t1adv seed mlo mhi dlo dhi kmax iters mode   (mode 0: maximize T1 violation, 1: U-FULL violation) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MM 512
#define DD 16
static int m, d, gen[DD], w[MM], nu[DD][MM], fx[DD][MM], minimal[DD];
static unsigned long long rs;
static unsigned rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static long Cp(long y, int p){ return y < p ? 0 : (y - p) / m + 1; }
static int apery(void){
  static int done[MM]; for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){
    int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return 0; done[b] = 1;
    for (int a = 0; a < d; a++){ int j = (b + gen[a]) % m, v = w[b] + gen[a]; if (w[j] < 0 || v < w[j]) w[j] = v; }
  }
  return 1;
}
static int ord[MM];
static int cmpw(const void *x, const void *y){ return w[*(int*)x] - w[*(int*)y]; }
/* returns e and fills best violation over p for T1 and U; computes Wilf walk identity check */
static int eval(int *vT, int *vU, int *pT, int *pU, long *Wout){
  if (!apery()) return -1;
  int e = 1;
  for (int a = 0; a < d; a++){
    int r = gen[a] % m; minimal[a] = (r != 0 && w[r] == gen[a]);
    if (minimal[a]) for (int i = 1; i < m; i++){ int j = (r - i + m) % m; if (j && w[i] + w[j] == gen[a]){ minimal[a] = 0; break; } }
    for (int b = 0; b < a; b++) if (minimal[b] && gen[b] == gen[a]) minimal[a] = 0;
    e += minimal[a];
  }
  for (int i = 0; i < m; i++) ord[i] = i;
  qsort(ord, m, sizeof(int), cmpw);
  for (int a = 0; a < d; a++) if (minimal[a]){
    int r = gen[a] % m;
    for (int t = 0; t < m; t++){ int i = ord[t], j = (i - r + m) % m; nu[a][i] = (w[j] + gen[a] == w[i]) ? nu[a][j] + 1 : 0; }
  }
  for (int t = 0; t < m; t++){ int i = ord[t]; int cur = i;
    for (int a = 0; a < d; a++){ if (!minimal[a]){ fx[a][i] = 0; continue; } int k = nu[a][cur]; fx[a][i] = k;
      cur = ((cur - (long)k * gen[a]) % m + m) % m; }
  }
  *vT = -1000000; *vU = -1000000;
  for (int p = 1; p <= m; p++){
    long sT = 0, sU = 0;
    for (int i = 0; i < m; i++){ long x = w[i], c0 = Cp(x, p); long kT = c0, kU = c0;
      for (int a = 0; a < d; a++) if (minimal[a]){ long dc = c0 - Cp(x - gen[a], p); kT -= nu[a][i] * dc; kU -= fx[a][i] * dc; }
      sT += kT; sU += kU; }
    if (sT - (m - e) > *vT){ *vT = sT - (m - e); *pT = p; }
    if (sU - (m - e) > *vU){ *vU = sU - (m - e); *pU = p; }
  }
  /* Wilf walk identity: m*W = m*(rho + Lam) + E + sum_p S_p - m*S_{p*} */
  long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long c = M - m + 1, q = (c + m - 1) / m, rho = q * m - c, pst = M % m + 1;
  long Wv = (long)e * (c - g) - c;
  long Lam = 0, E = 0; static long J[MM];
  for (int i = 0; i < m; i++){ J[i] = -e; long y = 0;
    for (int a = 0; a < d; a++) if (minimal[a]){ y += (long)nu[a][i] * gen[a]; int j = (i + gen[a]) % m;
      if (w[j] != w[i] + gen[a]){ J[i] += nu[a][i] + 1; Lam += (long)(nu[a][i] + 1) * ((M - w[i]) / m); } }
    E += y - w[i]; }
  long sumS = 0, Sp = 0, Spst = 0;
  for (int p = 1; p <= m; p++){ if (p == pst) Spst = Sp; sumS += Sp; if (p < m) Sp += J[p]; }
  if ((long)m * Wv != m * (rho + Lam) + E + sumS - m * Spst){ printf("WALK IDENTITY FAIL m=%d\n", m); fflush(stdout); }
  *Wout = Wv;
  return e;
}
static void pr(const char *tag, int v, int p, int e, long W){
  printf("%s viol=%d p=%d m=%d e=%d W=%ld gens=", tag, v, p, m, e, W);
  for (int a = 0; a < d; a++) if (minimal[a]) printf("%d,", gen[a]); printf("\n"); fflush(stdout);
}
static int randgen(int kmax){ int x; do { x = m + 1 + rnd() % ((kmax - 1) * m - 1); } while (x % m == 0); return x; }
int main(int argc, char **argv){
  rs = 88172645463325252ULL ^ (unsigned long long)atoi(argv[1]) * 2654435761ULL;
  int mlo = atoi(argv[2]), mhi = atoi(argv[3]), dlo = atoi(argv[4]), dhi = atoi(argv[5]), kmax = atoi(argv[6]);
  long iters = atol(argv[7]); int mode = atoi(argv[8]);
  int bestT = -1000000, bestU = -1000000; long evals = 0, fails = 0;
  for (int restart = 0; ; restart++){
    m = mlo + rnd() % (mhi - mlo + 1); d = dlo + rnd() % (dhi - dlo + 1);
    for (int a = 0; a < d; a++) gen[a] = randgen(kmax);
    int vT, vU, pT, pU, e; long W;
    e = eval(&vT, &vU, &pT, &pU, &W); if (e < 0) continue;
    int cur = mode ? vU : vT;
    for (long it = 0; it < iters; it++){
      int save[DD]; memcpy(save, gen, sizeof gen);
      int a = rnd() % d, kind = rnd() % 3;
      if (kind == 0) gen[a] = randgen(kmax);
      else { int dl = 1 + rnd() % (kind == 1 ? 3 : m); gen[a] += (rnd() & 1) ? dl : -dl; if (gen[a] <= m || gen[a] % m == 0) gen[a] = randgen(kmax); }
      int nT, nU, qT, qU; long W2; int e2 = eval(&nT, &nU, &qT, &qU, &W2); evals++;
      if (e2 < 0){ memcpy(gen, save, sizeof gen); continue; }
      int val = mode ? nU : nT;
      if (nT > bestT){ bestT = nT; pr("bestT", nT, qT, e2, W2); }
      if (nU > bestU){ bestU = nU; pr("bestU", nU, qU, e2, W2); }
      if (nT > 0){ fails++; pr("T1FAIL", nT, qT, e2, W2); }
      if (W2 < 0){ pr("WILFFAIL", (int)W2, 0, e2, W2); }
      if (val >= cur || (rnd() % 1000) < 20){ cur = val; } else memcpy(gen, save, sizeof gen);
    }
    if (restart % 20 == 0){ printf("restart %d evals %ld bestT %d bestU %d T1fails %ld\n", restart, evals, bestT, bestU, fails); fflush(stdout); }
  }
}
