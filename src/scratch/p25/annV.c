/* Annealer for the residual V of P18 depth four (lead, 2026-10-20). S = <m, m+B>, B c [1, m-1], 3m < c <= 4m, h = c - 3m.
 * V = E1 + T + 2 delta - P_hi + 3 delta_hi + 3 extra,  T = e*y0 - 3N4 - h,  extra = tau + omega - |Q + A|,
 * Q = Dset u Pset_hi.  mode 0: min V; mode 1: min V over S not covered by (h<=e, e(e+1)>=2m, (e-1)^2>=2m, 3e>=m);
 * mode 2: min (V - E1) ; mode 3: min T + 3 delta_hi - P_hi ; mode 4: min W (sanity).
 * usage: ./annV mode seed mlo mhi kmin kmax iters restarts */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define MX 1400
static int mode;
static double urand(void){ return rand() / (RAND_MAX + 1.0); }
typedef struct { int m, k, B[64]; } St;
static long long info[20];
static double evalS(St *s){
  int m = s->m, k = s->k, *B = s->B; if (m < 3 || 4 * m + 4 > MX) return 1e9;
  static char in[MX]; memset(in, 0, m);
  for (int i = 0; i < k; i++){ if (B[i] < 1 || B[i] >= m || in[B[i]]) return 1e9; in[B[i]] = 1; }
  static long long w[MX]; static char done[MX];
  for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return 1e9; done[b] = 1;
    for (int a = 0; a < k; a++){ int j = (b + B[a]) % m; long long v = w[b] + m + B[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
  long long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long long c = M - m + 1; if (!(3 * m < c && c <= 4 * m)) return 1e9;
  int h = (int)(c - 3 * m), e = k + 1, L = 4 * m;
  static char X1[MX], X2[MX], X3[MX], X4[MX], QA[MX];
  memset(X1, 0, L); memset(X2, 0, L); memset(X3, 0, L); memset(X4, 0, L); memset(QA, 0, L);
  int Al[65]; Al[0] = 0; for (int i = 0; i < k; i++) Al[i + 1] = B[i];
  for (int i = 0; i < e; i++) X1[Al[i]] = 1;
  for (int x = 0; x < L; x++) if (X1[x]) for (int i = 0; i < e; i++) if (x + Al[i] < L) X2[x + Al[i]] = 1;
  for (int x = 0; x < L; x++) if (X2[x]) for (int i = 0; i < e; i++) if (x + Al[i] < L) X3[x + Al[i]] = 1;
  for (int x = 0; x < L; x++) if (X3[x]) for (int i = 0; i < e; i++) if (x + Al[i] < L) X4[x + Al[i]] = 1;
  int n2 = 0; for (int x = 0; x < L; x++) n2 += X2[x];
  long long E1 = (long long)e * (e + 1) - 2 * n2;
  int y0 = 0, N4 = 0; for (int x = 0; x < h; x++){ y0 += X3[x]; N4 += (X4[x] && !X3[x]); }
  int tau = 0, omega = 0, delta = 0, Phi = 0, dhi = 0, nQA = 0;
  for (int s = m; s < m + h; s++){ if (X3[s] && X4[s - m]) omega++; if (X2[s] && X3[s - m]){ delta++; for (int i = 0; i < e; i++) QA[s + Al[i]] = 1; } }
  for (int s = m + h; s < 2 * m; s++) if (X2[s]){ Phi++; if (X3[s - m]) dhi++; for (int i = 0; i < e; i++) QA[s + Al[i]] = 1; }
  for (int s = m + h; s < L; s++) tau += X3[s];
  for (int s = 0; s < L; s++) nQA += QA[s];
  long long extra = tau + omega - nQA, T = (long long)e * y0 - 3 * N4 - h;
  long long V = E1 + T + 2 * delta - Phi + 3 * dhi + 3 * extra, W = (long long)e * (c - g) - c;
  int known = (h <= e) || ((long long)e * (e + 1) >= 2 * m) || ((long long)(e - 1) * (e - 1) >= 2 * m) || (3 * e >= m);
  info[0] = h; info[1] = e; info[2] = W; info[3] = V; info[4] = T; info[5] = delta; info[6] = Phi; info[7] = dhi; info[8] = extra; info[9] = E1; info[10] = y0; info[11] = N4; info[12] = known;
  switch (mode){ case 0: return V; case 1: return known ? 1e9 : V; case 2: return V - E1; case 3: return T + 3 * dhi - Phi; default: return W; }
}
int main(int argc, char **argv){
  mode = atoi(argv[1]); srand(atoi(argv[2])); int mlo = atoi(argv[3]), mhi = atoi(argv[4]), kmin = atoi(argv[5]), kmax = atoi(argv[6]); long iters = atol(argv[7]); int R = atoi(argv[8]);
  double best = 1e18;
  for (int r = 0; r < R; r++){
    St s; double f; int tries = 0;
    do { s.m = mlo + rand() % (mhi - mlo + 1); s.k = kmin + rand() % (kmax - kmin + 1);
      for (int i = 0; i < s.k; i++){ int ok; do { s.B[i] = 1 + rand() % (s.m - 1); ok = 1; for (int j = 0; j < i; j++) if (s.B[j] == s.B[i]) ok = 0; } while (!ok); }
      f = evalS(&s); tries++; } while (f >= 1e9 && tries < 1000000);
    if (f >= 1e9) continue;
    double T = 4.0;
    for (long it = 0; it < iters; it++){
      St t = s; int mv = rand() % 6, i = rand() % t.k;
      if (mv == 0) t.B[i] = 1 + rand() % (t.m - 1);
      else if (mv == 1) t.B[i] += (rand() % 2) ? 1 : -1;
      else if (mv == 2) t.m += (rand() % 2) ? 1 : -1;
      else if (mv == 3 && t.k < kmax) t.B[t.k++] = 1 + rand() % (t.m - 1);
      else if (mv == 4 && t.k > kmin){ t.B[i] = t.B[--t.k]; }
      else { t.B[i] += (rand() % 7) - 3; t.m += (rand() % 3) - 1; }
      if (t.m < mlo || t.m > mhi) continue;
      double g2 = evalS(&t); if (g2 >= 1e9) continue;
      if (g2 <= f || urand() < exp((f - g2) / T)){ s = t; f = g2; }
      if (f < best){ best = f; evalS(&s);
        printf("mode %d best %.0f m=%d e=%lld h=%lld W=%lld V=%lld T=%lld delta=%lld Phi=%lld dhi=%lld extra=%lld E1=%lld y0=%lld N4=%lld known=%lld B=", mode, best, s.m, info[1], info[0], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10], info[11], info[12]);
        int tmp[64]; memcpy(tmp, s.B, sizeof(int) * s.k); for (int a = 0; a < s.k; a++) for (int b2 = a + 1; b2 < s.k; b2++) if (tmp[b2] < tmp[a]){ int x = tmp[a]; tmp[a] = tmp[b2]; tmp[b2] = x; }
        for (int a = 0; a < s.k; a++) printf("%d,", tmp[a]); printf("\n"); fflush(stdout); }
      T *= 0.99995; if (T < 0.05) T = 0.05;
    }
  }
}
