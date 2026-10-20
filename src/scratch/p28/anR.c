/* anR: annealer for Conjecture R3 (|R| <= Z, third regime). Derived from anJ.c. mode 0: min Z-R over 3h<=m; 1: all; 2: 2h<=m.
 * Annealer for Conjecture J (lead, 2026-10-20). P18 depth four: S = <m, m+B>, B c [1,m-1], 3m < c = 3m+h <= 4m.
 * Apery orders o(w) (max #generators), levels x(w) = w/m.  H_j = #{o = j}.
 * J = E2 + (e-1) y - 4 H4 - q - 3 qQ - p, with E2 = e(e-1) - 2 H2, y = #{r < h : x <= 3}, H4 = #{o = 4},
 * q = #{x = 4, o = 3}, qQ = #{those with a summand w - m - b that is a carried pair (x = 3, o = 2)}, p = #{x = 3, o = 2}.
 * W = J + sigma, sigma = E3 - (e-1) p + 3 qQ >= 0 (RTCM on gr(R/t^m)).
 * mode 10/11/12: min CL = U2+U3+U4-p-q (carry lemma) over h > e / all / uncovered.
 * mode 4/5: min C4/C3 over h > e; 6/7: C4/C3 over uncovered S; 8/9: C4/C3 over all S.
 * C4 = (e-1) y0 - 4 H4 - q ; C3 = E3 + chi3 - e p (chi3 = carried-parent rep tokens of carried triples, best rep).
 * mode 0: min J; mode 1: min J over h > e; mode 2: min J over S not covered by known criteria; mode 3: min W (sanity).
 * usage: ./anJ mode seed mlo mhi kmin kmax iters restarts */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define MX 1200
static int mode;
static double urand(void){ return rand() / (RAND_MAX + 1.0); }
typedef struct { int m, k, B[64]; } St;
static long long info[20];
static int cmpw(const void *a, const void *b){ long long x = *(const long long *)a, y = *(const long long *)b; return (x > y) - (x < y); }
static double evalS(St *s){
  int m = s->m, k = s->k; if (m < 3 || m > MX) return 1e9;
  int B[64]; for (int i = 0; i < k; i++) B[i] = s->B[i];
  for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) if (B[j] < B[i]){ int t = B[i]; B[i] = B[j]; B[j] = t; }
  for (int i = 0; i < k; i++){ if (B[i] < 1 || B[i] >= m) return 1e9; if (i && B[i] == B[i-1]) return 1e9; }
  static long long w[MX]; static char done[MX];
  for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return 1e9; done[b] = 1;
    for (int a = 0; a < k; a++){ int j = (b + B[a]) % m; long long v = w[b] + m + B[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
  long long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long long c = M - m + 1; if (!(3 * m < c && c <= 4 * m)) return 1e9;
  int h = (int)(c - 3 * m), e = k + 1;
  static long long sw[MX]; static int ord[MX], par[MX];
  for (int i = 0; i < m; i++) sw[i] = w[i];
  qsort(sw, m, sizeof(long long), cmpw);
  ord[0] = 0; par[0] = -1;
  for (int t = 1; t < m; t++){ long long v = sw[t]; int r = (int)(v % m), best = -1, bp = -1;
    for (int a = 0; a < k; a++){ long long u = v - m - B[a]; if (u < 0) continue; int ru = (int)(u % m); if (w[ru] == u && ord[ru] + 1 > best){ best = ord[ru] + 1; bp = a; } }
    ord[r] = best; par[r] = bp; }
  /* R: carried triples (level 4, order 3) whose chosen rep b1<=b2<=b3 has b1+b2 >= h */
  long long R = 0;
  for (int r = 0; r < m; r++){ if (!(w[r] / m == 4 && ord[r] == 3)) continue;
    int idx[3], n = 0; long long x = w[r]; while (x != 0){ int rr = (int)(x % m); int a = par[rr]; idx[n++] = a; x -= m + B[a]; if (n > 3) return 1e9; }
    int b0 = B[idx[0]], b1 = B[idx[1]], b2 = B[idx[2]]; int lo = b0 < b1 ? b0 : b1; lo = lo < b2 ? lo : b2;
    int hi = b0 > b1 ? b0 : b1; hi = hi > b2 ? hi : b2; int mid = b0 + b1 + b2 - lo - hi;
    if (lo + mid >= h) R++; }
  /* Z: unused zero tokens (0, x, kk), kk = 2,3,4: {x^kk} is not the chosen rep of an Apery element of order kk */
  long long Z = 0;
  for (int a = 0; a < k; a++) for (int kk = 2; kk <= 4; kk++){
    long long v = (long long)kk * (m + B[a]); int rr = (int)(v % m); int alive = 0;
    if (w[rr] == v && ord[rr] == kk){ alive = 1; long long x = v; while (x != 0){ int r2 = (int)(x % m); if (par[r2] != a){ alive = 0; break; } x -= m + B[a]; } }
    if (!alive) Z++; }
  long long W = (long long)e * (c - g) - c;
  info[0] = h; info[1] = e; info[2] = W; info[3] = R; info[4] = Z;
  int reg3 = (3 * h <= m);
  switch (mode){ case 0: return reg3 ? (double)(Z - R) : 1e9; case 1: return (double)(Z - R); case 2: return (2 * h <= m) ? (double)(Z - R) : 1e9; default: return W; }
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
        printf("mode %d best %.0f m=%d e=%lld h=%lld W=%lld R=%lld Z=%lld B=", mode, best, s.m, info[1], info[0], info[2], info[3], info[4]);
        int tmp[64]; memcpy(tmp, s.B, sizeof(int) * s.k); for (int a = 0; a < s.k; a++) for (int b2 = a + 1; b2 < s.k; b2++) if (tmp[b2] < tmp[a]){ int x = tmp[a]; tmp[a] = tmp[b2]; tmp[b2] = x; }
        for (int a = 0; a < s.k; a++) printf("%d,", tmp[a]); printf("\n"); fflush(stdout); }
      T *= 0.99995; if (T < 0.05) T = 0.05;
    }
  }
}
