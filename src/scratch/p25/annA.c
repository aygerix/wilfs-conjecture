/* Annealer for P18 depth four, all-A (B c [1,h)), lead 2026-10-20.
 * Minimizes: mode 0: Z (non-core only), 1: D = 3tau + 3omega - e*delta, 2: W - (e-2), 3: Z + 2E1 + E3f, 4: D restricted to delta >= 1
 *   5: Z + D (non-core), 6: Z + D + 2E1 (non-core), 7: Z + D over all all-A (core included)
 *   8: F = e*y0 - e*delta + 3*omega - 3*N4 - h (FREE-A), 9: Z + D + 2E1, 10: Z + D + E1 (all all-A)
 *   Z = e(y0-e) + 2(|2A_<h|-e) + e - 2|(3A\2A) n W1| - 3N4 - 2e'' + 3[h odd], W1 = [h, 3h'), e'' = |W1 n (m + 4A_<h) \ 3A|.
 * usage: ./annA mode seed mlo mhi kmin kmax iters restarts */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define MX 1200
static int mode;
static double urand(void){ return rand() / (RAND_MAX + 1.0); }
typedef struct { int m, k, B[64]; } St;
static long long lastW; static int lastinfo[16];
static double evalS(St *s){
  int m = s->m, k = s->k, *B = s->B; if (m < 3 || m > MX / 5) return 1e9;
  static char in[MX]; memset(in, 0, m);
  for (int i = 0; i < k; i++){ if (B[i] < 1 || B[i] >= m || in[B[i]]) return 1e9; in[B[i]] = 1; }
  static long long w[MX]; static char done[MX];
  for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return 1e9; done[b] = 1;
    for (int a = 0; a < k; a++){ int j = (b + B[a]) % m; long long v = w[b] + m + B[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
  long long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long long c = M - m + 1; if (!(3 * m < c && c <= 4 * m)) return 1e9;
  int h = (int)(c - 3 * m), e = k + 1, mx = 0, mn = m; for (int i = 0; i < k; i++){ if (B[i] > mx) mx = B[i]; if (B[i] < mn) mn = B[i]; }
  if (mx >= h) return 1e9;
  int hp = (h + 1) / 2; if ((mode == 0 || mode == 3 || mode == 5 || mode == 6) && mn >= hp) return 1e9;
  static char X1[MX], X2[MX], X3[MX], X4[MX]; int L = 4 * h;
  memset(X1, 0, L); memset(X2, 0, L); memset(X3, 0, L); memset(X4, 0, L);
  X1[0] = 1; for (int i = 0; i < k; i++) X1[B[i]] = 1;
  for (int x = 0; x < L; x++) if (X1[x]) for (int y = 0; y < L; y++) if (X1[y] && x + y < L) X2[x + y] = 1;
  for (int x = 0; x < L; x++) if (X2[x]) for (int y = 0; y < h; y++) if (X1[y] && x + y < L) X3[x + y] = 1;
  for (int x = 0; x < L; x++) if (X3[x]) for (int y = 0; y < h; y++) if (X1[y] && x + y < L) X4[x + y] = 1;
  int n2 = 0, n3 = 0; for (int x = 0; x < L; x++){ n2 += X2[x]; n3 += X3[x]; }
  long long E1 = (long long)e * (e + 1) - 2 * n2, E3f = (long long)(e + 2) * n2 - 3LL * n3;
  int y0 = 0, x2h = 0, N4 = 0; for (int x = 0; x < h; x++){ y0 += X3[x]; x2h += X2[x]; N4 += (X4[x] && !X3[x]); }
  int t3w = 0, epp = 0; for (int v = h; v < 3 * hp; v++){ t3w += (X3[v] && !X2[v]); if (v >= m && v - m < h && X4[v - m] && !X3[v]) epp++; }
  int delta = 0, tau = 0, omega = 0;
  for (int s = m; s < m + h; s++){ if (X2[s] && X3[s - m]) delta++; if (X3[s] && X4[s - m]) omega++; }
  for (int s = m + h; s < L; s++) tau += X3[s];
  long long Z = (long long)e * (y0 - e) + 2 * (x2h - e) + e - 2 * t3w - 3 * N4 - 2 * epp + 3 * (h % 2);
  long long D = 3LL * tau + 3LL * omega - (long long)e * delta;
  long long W = (long long)e * (c - g) - c; lastW = W;
  lastinfo[0] = h; lastinfo[1] = e; lastinfo[2] = y0; lastinfo[3] = N4; lastinfo[4] = t3w; lastinfo[5] = delta; lastinfo[6] = tau; lastinfo[7] = omega; lastinfo[8] = (int)Z; lastinfo[9] = (int)D; lastinfo[10] = (int)E1; lastinfo[11] = (int)E3f;
  if (mode == 4 && delta < 1) return 1e9;
  switch (mode){ case 0: return Z; case 1: case 4: return D; case 2: return W - (e - 2); case 3: return Z + 2 * E1 + E3f;
    case 5: case 7: return Z + D; case 6: return Z + D + 2 * E1;
    case 8: return (double)e * y0 - (double)e * delta + 3.0 * omega - 3.0 * N4 - h; case 9: return Z + D + 2 * E1; default: return Z + D + E1; }
}
int main(int argc, char **argv){
  mode = atoi(argv[1]); srand(atoi(argv[2])); int mlo = atoi(argv[3]), mhi = atoi(argv[4]), kmin = atoi(argv[5]), kmax = atoi(argv[6]); long iters = atol(argv[7]); int R = atoi(argv[8]);
  double best = 1e18;
  for (int r = 0; r < R; r++){
    St s; double f;
    do { s.m = mlo + rand() % (mhi - mlo + 1); s.k = kmin + rand() % (kmax - kmin + 1); int h0 = s.m / 2 + rand() % (s.m / 2 + 1);
      for (int i = 0; i < s.k; i++){ int ok; do { s.B[i] = 1 + rand() % (h0 > 2 ? h0 - 1 : 1); ok = 1; for (int j = 0; j < i; j++) if (s.B[j] == s.B[i]) ok = 0; } while (!ok); }
      f = evalS(&s); } while (f >= 1e9);
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
        printf("mode %d best %.0f m=%d e=%d h=%d W=%lld y0=%d N4=%d t3w=%d delta=%d tau=%d omega=%d Z=%d D=%d E1=%d E3f=%d B=", mode, best, s.m, s.k + 1, lastinfo[0], lastW, lastinfo[2], lastinfo[3], lastinfo[4], lastinfo[5], lastinfo[6], lastinfo[7], lastinfo[8], lastinfo[9], lastinfo[10], lastinfo[11]);
        int tmp[64]; memcpy(tmp, s.B, sizeof(int) * s.k); for (int a = 0; a < s.k; a++) for (int b2 = a + 1; b2 < s.k; b2++) if (tmp[b2] < tmp[a]){ int x = tmp[a]; tmp[a] = tmp[b2]; tmp[b2] = x; }
        for (int a = 0; a < s.k; a++) printf("%d,", tmp[a]); printf("\n"); fflush(stdout); }
      T *= 0.99995; if (T < 0.05) T = 0.05;
    }
  }
}
