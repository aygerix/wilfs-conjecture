/* anD: annealer against Conjecture DEAD, W >= Lambda - O (lead, 2026-10-20).
 * State: m and a set G of generators in (m, HI*m); S = <m, G>.  Computes Ap(S,m), the minimal generators, orders o(w),
 * mu_b(w) = max{j: w - j g_b in S}, Lambda = sum mu, O = sum o, W = e(c-g) - c.
 * mode 0: minimise W/(Lambda-O) over Lambda - O >= 5 (failure iff < 1);  mode 1: minimise D = W - (Lambda - O) over
 * Lambda - O >= 5;  mode 2: mode 0 restricted to P18 (all minimal generators < 2m).
 * usage: ./anD mode seed mlo mhi kmin kmax HI iters restarts */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define MX 260
#define KX 80
static int mode, HI;
static double urand(void){ return rand() / (RAND_MAX + 1.0); }
typedef struct { int m, k, G[KX]; } St;
static long long info[8]; static int mg[KX], nmg;
static double evalS(St *s){
  int m = s->m, k = s->k; if (m < 3 || m >= MX) return 1e18;
  for (int i = 0; i < k; i++) if (s->G[i] <= m || s->G[i] >= HI * m) return 1e18;
  static long long w[MX]; static char done[MX];
  for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return 1e18; done[b] = 1;
    for (int a = 0; a < k; a++){ int j = (int)((b + s->G[a]) % m); long long v = w[b] + s->G[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
  long long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long long c = M - m + 1; if (c <= m) return 1e18;
  /* membership: x in S iff x >= w[x % m] */
  #define INS(x) ((x) >= 0 && (x) >= w[(x) % m])
  /* minimal generators among Ap \ {0}: w not a sum of two nonzero Ap elements */
  nmg = 0;
  for (int r = 1; r < m; r++){ int dec = 0; for (int r2 = 1; r2 < m && !dec; r2++){ long long u = w[r] - w[r2]; if (u > 0 && u >= w[u % m] && (u % m) != 0) dec = 1; }
    if (!dec){ if (nmg >= KX - 1) return 1e18; mg[nmg++] = (int)w[r]; } }
  int e = nmg + 1;
  if (mode == 2) for (int i = 0; i < nmg; i++) if (mg[i] >= 2 * m) return 1e18;
  /* orders by increasing w */
  static int idx[MX], o[MX];
  for (int i = 0; i < m; i++) idx[i] = i;
  for (int i = 1; i < m; i++){ int t = idx[i], j = i; while (j > 0 && w[idx[j - 1]] > w[t]){ idx[j] = idx[j - 1]; j--; } idx[j] = t; }
  long long O = 0, Lam = 0;
  for (int ii = 0; ii < m; ii++){ int r = idx[ii]; long long v = w[r]; if (v == 0){ o[r] = 0; continue; }
    int best = -1; for (int b = 0; b < nmg; b++){ long long u = v - mg[b]; if (u >= 0 && INS(u) && o[u % m] + 1 > best) best = o[u % m] + 1; }
    o[r] = best; O += best;
    for (int b = 0; b < nmg; b++){ int j = 0; while (INS(v - (long long)(j + 1) * mg[b])) j++; Lam += j; } }
  long long W = (long long)e * (c - g) - c, nu = Lam - O;
  info[0] = e; info[1] = c; info[2] = g; info[3] = W; info[4] = nu; info[5] = W - nu;
  if (nu < 5) return 1e18;
  if (mode == 1) return (double)(W - nu);
  return (double)W / (double)nu;
}
int main(int argc, char **argv){
  mode = atoi(argv[1]); srand(atoi(argv[2])); int mlo = atoi(argv[3]), mhi = atoi(argv[4]), kmin = atoi(argv[5]), kmax = atoi(argv[6]);
  HI = atoi(argv[7]); long iters = atol(argv[8]); int R = atoi(argv[9]);
  double best = 1e18;
  for (int rs = 0; rs < R; rs++){
    St s; double f; int tries = 0;
    do { s.m = mlo + rand() % (mhi - mlo + 1); s.k = kmin + rand() % (kmax - kmin + 1);
      if (rand() % 2){ int a = s.m + 1 + rand() % s.m; for (int i = 0; i < s.k; i++) s.G[i] = a + i; }
      else for (int i = 0; i < s.k; i++) s.G[i] = s.m + 1 + rand() % ((HI - 1) * s.m - 1);
      f = evalS(&s); tries++; } while (f >= 1e17 && tries < 100000);
    if (f >= 1e17) continue;
    double T = 0.05;
    for (long it = 0; it < iters; it++){
      St t = s; int mv = rand() % 6, i = rand() % t.k;
      if (mv == 0) t.G[i] = t.m + 1 + rand() % ((HI - 1) * t.m - 1);
      else if (mv == 1) t.G[i] += (rand() % 2) ? 1 : -1;
      else if (mv == 2){ int d = (rand() % 2) ? 1 : -1; t.m += d; for (int j = 0; j < t.k; j++) t.G[j] += d; }
      else if (mv == 3 && t.k < kmax) t.G[t.k++] = t.m + 1 + rand() % ((HI - 1) * t.m - 1);
      else if (mv == 4 && t.k > kmin) t.G[i] = t.G[--t.k];
      else { t.G[i] += (rand() % 7) - 3; }
      if (t.m < mlo || t.m > mhi) continue;
      double g2 = evalS(&t); if (g2 >= 1e17) continue;
      if (g2 <= f || urand() < exp((f - g2) / T)){ s = t; f = g2; }
      if (f < best){ best = f; evalS(&s);
        printf("mode %d best %.5f m=%d e=%lld c=%lld g=%lld W=%lld nu=%lld D=%lld mingens=", mode, best, s.m, info[0], info[1], info[2], info[3], info[4], info[5]);
        int tmp[KX]; memcpy(tmp, mg, sizeof(int) * nmg); for (int a = 0; a < nmg; a++) for (int b = a + 1; b < nmg; b++) if (tmp[b] < tmp[a]){ int x = tmp[a]; tmp[a] = tmp[b]; tmp[b] = x; }
        for (int a = 0; a < nmg; a++) printf("%d,", tmp[a]); printf("\n"); fflush(stdout); }
      T *= 0.99997; if (T < 0.002) T = 0.002;
    }
  }
}
