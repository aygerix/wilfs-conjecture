/* anS: annealer against S2 (p + q <= G) and S3 (p + q <= Z + G) at P18 depth four (lead, 2026-10-20).
 * S = <m, m+B>, 3m < c <= 4m, h = c - 3m.  top(u) = 4 if r(u) < h else 3; L_u = top(u) - level(u);
 * lambda(u, x) = max{j : u + j g_x in Ap}.  Z = sum_x (L_0 - lambda(0,x)), G = sum_{b,x} (L_{g_b} - lambda(g_b, x)).
 * p = carried pairs (level 3, order 2), q = carried triples (level 4, order 3).
 * mode 0: min S2 slack; 1: min S3 slack; 2: S2 slack / e; 3: S2 over h > e only; 4: S2 over 2h > m;
 * mode 5: min G/(p+q) over p+q >= 10 (S2 fails iff < 1); 6: min (Z+G)/(p+q).
 * usage: ./anS mode seed mlo mhi kmin kmax iters restarts */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define MX 700
static int mode;
static double urand(void){ return rand() / (RAND_MAX + 1.0); }
typedef struct { int m, k, B[80]; } St;
static long long info[12];
static int cmpw(const void *a, const void *b){ long long x = *(const long long *)a, y = *(const long long *)b; return (x > y) - (x < y); }
static double evalS(St *s){
  int m = s->m, k = s->k; if (m < 3 || m >= MX || k > 79 || k < 1) return 1e18;
  int B[80]; for (int i = 0; i < k; i++) B[i] = s->B[i];
  for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) if (B[j] < B[i]){ int t = B[i]; B[i] = B[j]; B[j] = t; }
  for (int i = 0; i < k; i++){ if (B[i] < 1 || B[i] >= m) return 1e18; if (i && B[i] == B[i-1]) return 1e18; }
  static long long w[MX]; static char done[MX];
  for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return 1e18; done[b] = 1;
    for (int a = 0; a < k; a++){ int j = (b + B[a]) % m; long long v = w[b] + m + B[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
  long long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  long long c = M - m + 1; if (!(3 * m < c && c <= 4 * m)) return 1e18;
  int h = (int)(c - 3 * m), e = k + 1;
  /* all generators minimal? (m+b is always minimal in P18 unless b in B+B... m+b = (m+b1)+(m+b2) impossible) */
  static long long sw[MX]; static int ord[MX];
  for (int i = 0; i < m; i++) sw[i] = w[i];
  qsort(sw, m, sizeof(long long), cmpw);
  ord[0] = 0;
  for (int t = 1; t < m; t++){ long long v = sw[t]; int r = (int)(v % m), best = -1;
    for (int a = 0; a < k; a++){ long long u = v - m - B[a]; if (u < 0) continue; int ru = (int)(u % m); if (w[ru] == u && ord[ru] + 1 > best) best = ord[ru] + 1; }
    ord[r] = best; }
  long long p = 0, q = 0;
  for (int r = 0; r < m; r++){ int lv = (int)(w[r] / m); if (lv - ord[r] > 0){ if (ord[r] == 2) p++; else if (ord[r] == 3) q++; else if (lv - ord[r] >= 1) return 1e18; } }
  #define ISAP(v) ((v) >= 0 && w[(v) % m] == (v))
  long long Z = 0, G = 0;
  for (int x = 0; x < k; x++){ long long gx = m + B[x]; int j = 0; while (ISAP((j + 1) * gx)) j++; Z += 4 - j; }
  for (int b = 0; b < k; b++){ long long gb = m + B[b]; int Lb = (B[b] < h) ? 3 : 2;
    for (int x = 0; x < k; x++){ long long gx = m + B[x]; int j = 0; while (ISAP(gb + (j + 1) * gx)) j++; G += Lb - j; } }
  long long g = 0; for (int i = 0; i < m; i++) g += w[i] / m; long long W = (long long)e * (c - g) - c;
  long long S2 = G - p - q, S3 = Z + G - p - q;
  info[0] = h; info[1] = e; info[2] = W; info[3] = p; info[4] = q; info[5] = Z; info[6] = G; info[7] = S2; info[8] = S3;
  switch (mode){ case 0: return S2; case 1: return S3; case 2: return (double)S2 / e; case 3: return (h > e) ? S2 : 1e18;
    case 4: return (2 * h > m) ? S2 : 1e18;
    case 5: return (p + q >= 10) ? (double)G / (double)(p + q) : 1e18;
    case 6: return (p + q >= 10) ? (double)(Z + G) / (double)(p + q) : 1e18;
    default: return W; }
}
int main(int argc, char **argv){
  mode = atoi(argv[1]); srand(atoi(argv[2])); int mlo = atoi(argv[3]), mhi = atoi(argv[4]), kmin = atoi(argv[5]), kmax = atoi(argv[6]);
  long iters = atol(argv[7]); int RR = atoi(argv[8]); double best = 1e18;
  for (int rs = 0; rs < RR; rs++){
    St s; double f; int tries = 0;
    do { s.m = mlo + rand() % (mhi - mlo + 1); s.k = kmin + rand() % (kmax - kmin + 1);
      for (int i = 0; i < s.k; i++){ int ok; do { s.B[i] = 1 + rand() % (s.m - 1); ok = 1; for (int j = 0; j < i; j++) if (s.B[j] == s.B[i]) ok = 0; } while (!ok); }
      f = evalS(&s); tries++; } while (f >= 1e17 && tries < 1000000);
    if (f >= 1e17) continue;
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
      double g2 = evalS(&t); if (g2 >= 1e17) continue;
      if (g2 <= f || urand() < exp((f - g2) / T)){ s = t; f = g2; }
      if (f < best){ best = f; evalS(&s);
        printf("mode %d best %.3f m=%d e=%lld h=%lld W=%lld p=%lld q=%lld Z=%lld G=%lld S2=%lld S3=%lld B=", mode, best, s.m, info[1], info[0], info[2], info[3], info[4], info[5], info[6], info[7], info[8]);
        int tmp[80]; memcpy(tmp, s.B, sizeof(int) * s.k); for (int a = 0; a < s.k; a++) for (int b2 = a + 1; b2 < s.k; b2++) if (tmp[b2] < tmp[a]){ int x = tmp[a]; tmp[a] = tmp[b2]; tmp[b2] = x; }
        for (int a = 0; a < s.k; a++) printf("%d,", tmp[a]); printf("\n"); fflush(stdout); }
      T *= 0.99995; if (T < 0.05) T = 0.05;
    }
  }
}
