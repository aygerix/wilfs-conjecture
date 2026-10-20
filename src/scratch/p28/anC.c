/* anC: annealer for (**): |R| + p <= (a+1)|B >= h/3| + #{(b,x): b + 2x >= m + h}  (derived from anM.c).
 * mode 0: all S; 1: 3h <= m; 2: h > e; 3: 2h > m.  Prints slack2.
 * anM: annealer for the Hall condition of the residual class R at P18 depth four, X = R (lead, 2026-10-20).
 * R = carried triples (level 4, order 3) whose chosen rep b1<=b2<=b3 has b1+b2 >= h.
 * N(R) = unused power tokens not in im(pi) u im(rho) whose first coordinate is an uncarried sub-sum of some v in R
 *        (0, its generators, its sub-pairs), plus spare capacity of carried sub-pairs.  slack = |N(R)| - |R|.
 * pi(pair {b<=b'}) = (g_b, b', 3) if b' >= h else (g_b, b', 4); rho(triple b1+b2<h) = (u12, b3, 4).
 * mode 0: min slack; 1: min slack over 3h <= m; 2: min slack over h > e.   usage: ./anM mode seed mlo mhi kmin kmax iters restarts */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define MX 400
static int mode;
static double urand(void){ return rand() / (RAND_MAX + 1.0); }
typedef struct { int m, k, B[40]; } St;
static long long info[10];
static int cmpw(const void *a, const void *b){ long long x = *(const long long *)a, y = *(const long long *)b; return (x > y) - (x < y); }
/* token index: (r, a, kk) -> (r*40 + a)*5 + kk */
static unsigned char pool[MX * 40 * 5], used[MX * 40 * 5], taken[MX * 40 * 5];
#define TI(r, a, kk) (((r) * 40 + (a)) * 5 + (kk))
static double evalS(St *s){
  int m = s->m, k = s->k; if (m < 3 || m > MX || k > 39) return 1e9;
  int B[40]; for (int i = 0; i < k; i++) B[i] = s->B[i];
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
  static long long sw[MX]; static int ord[MX], par[MX], car[MX];
  for (int i = 0; i < m; i++) sw[i] = w[i];
  qsort(sw, m, sizeof(long long), cmpw);
  ord[0] = 0; par[0] = -1;
  for (int t = 1; t < m; t++){ long long v = sw[t]; int r = (int)(v % m), best = -1, bp = -1;
    for (int a = 0; a < k; a++){ long long u = v - m - B[a]; if (u < 0) continue; int ru = (int)(u % m); if (w[ru] == u && ord[ru] + 1 > best){ best = ord[ru] + 1; bp = a; } }
    ord[r] = best; par[r] = bp; }
  for (int r = 0; r < m; r++) car[r] = (int)(w[r] / m) - ord[r];
  int NT = m * 40 * 5; memset(pool, 0, NT); memset(used, 0, NT); memset(taken, 0, NT);
  for (int r = 0; r < m; r++){ int top = (r < h) ? 4 : 3; for (int a = 0; a < k; a++) for (int kk = (ord[r] + 1 > 2 ? ord[r] + 1 : 2); kk <= top; kk++) pool[TI(r, a, kk)] = 1; }
  /* used tokens: element v of order kk >= 2 uses (v - j g_a, a, kk), j = 1..mult_a, along its chosen rep */
  int rep[MX][4], nrep[MX];
  for (int r = 0; r < m; r++){ nrep[r] = 0; long long x = w[r]; while (x != 0){ int rr = (int)(x % m); int a = par[rr]; if (nrep[r] >= 4){ nrep[r] = 99; break; } rep[r][nrep[r]++] = a; x -= m + B[a]; } }
  for (int r = 0; r < m; r++){ int kk = ord[r]; if (kk < 2 || nrep[r] > 4) continue;
    for (int a = 0; a < k; a++){ int mult = 0; for (int i = 0; i < nrep[r]; i++) if (rep[r][i] == a) mult++;
      for (int j = 1; j <= mult; j++){ long long u = w[r] - (long long)j * (m + B[a]); int ru = (int)(u % m); used[TI(ru, a, kk)] = 1; } } }
  /* pi and rho */
  int R = 0, Rlist[MX];
  for (int r = 0; r < m; r++){ if (car[r] <= 0) continue;
    if (nrep[r] == 2){ int a0 = rep[r][0], a1 = rep[r][1]; int lo = B[a0] <= B[a1] ? a0 : a1, hi = (lo == a0) ? a1 : a0;
      int rg = B[lo] % m; int kk = (B[hi] >= h) ? 3 : 4; taken[TI(rg, hi, kk)] = 1; }
    else if (nrep[r] == 3){ int id[3] = {rep[r][0], rep[r][1], rep[r][2]};
      for (int i = 0; i < 3; i++) for (int j = i + 1; j < 3; j++) if (B[id[j]] < B[id[i]]){ int t = id[i]; id[i] = id[j]; id[j] = t; }
      if (B[id[0]] + B[id[1]] < h){ long long u = w[r] - (m + B[id[2]]); int ru = (int)(u % m); taken[TI(ru, id[2], 4)] = 1; }
      else Rlist[R++] = r; } }
  /* first coordinates F: sub-sums of R elements */
  static char F[MX]; memset(F, 0, m);
  for (int i = 0; i < R; i++){ int r = Rlist[i]; F[0] = 1;
    for (int j = 0; j < 3; j++){ int rg = B[rep[r][j]] % m; F[rg] = 1; long long u = w[r] - (m + B[rep[r][j]]); F[(int)(u % m)] = 1; } }
  long long N = 0;
  for (int r = 0; r < m; r++){ if (!F[r]) continue; long long un = 0;
    for (int a = 0; a < k; a++) for (int kk = 2; kk <= 4; kk++){ int t = TI(r, a, kk); if (pool[t] && !used[t] && !taken[t]) un++; }
    if (car[r] == 0) N += un; else { long long sp = un - (long long)(e - 1) * car[r]; if (sp > 0) N += sp; } }
  long long W = (long long)e * (c - g) - c;
  info[0] = h; info[1] = e; info[2] = W; info[3] = R; info[4] = N;
  long long p = 0; for (int r = 0; r < m; r++) if (car[r] > 0 && nrep[r] == 2) p++;
  int a = 0; for (int i = 0; i < k; i++) if (B[i] < h) a++;
  long long n3 = 0; for (int i = 0; i < k; i++) if (3 * B[i] >= h) n3++;
  long long D3 = 0; for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) if (B[i] + 2 * B[j] >= m + h) D3++;
  long long slack2 = (long long)(a + 1) * n3 + D3 - p - R;
  info[5] = p; info[6] = slack2; info[7] = a;
  double slack = (double)slack2;
  if (R < 3 || h <= e) return 1e9;
  if (mode == 3) return (2 * h > m) ? slack : 1e9;
  switch (mode){ case 0: return slack; case 1: return (3 * h <= m) ? slack : 1e9; case 2: return (h > e) ? slack : 1e9; default: return W; }
}
int main(int argc, char **argv){
  mode = atoi(argv[1]); srand(atoi(argv[2])); int mlo = atoi(argv[3]), mhi = atoi(argv[4]), kmin = atoi(argv[5]), kmax = atoi(argv[6]); long iters = atol(argv[7]); int RR = atoi(argv[8]);
  double best = 1e18;
  for (int rs = 0; rs < RR; rs++){
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
        printf("mode %d best %.0f m=%d e=%lld h=%lld a=%lld W=%lld R=%lld p=%lld slack2=%lld B=", mode, best, s.m, info[1], info[0], info[7], info[2], info[3], info[5], info[6]);
        int tmp[40]; memcpy(tmp, s.B, sizeof(int) * s.k); for (int a = 0; a < s.k; a++) for (int b2 = a + 1; b2 < s.k; b2++) if (tmp[b2] < tmp[a]){ int x = tmp[a]; tmp[a] = tmp[b2]; tmp[b2] = x; }
        for (int a = 0; a < s.k; a++) printf("%d,", tmp[a]); printf("\n"); fflush(stdout); }
      T *= 0.99995; if (T < 0.05) T = 0.05;
    }
  }
}
