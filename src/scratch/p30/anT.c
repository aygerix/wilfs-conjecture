/* anT: annealer against STAR at P18 depth four (lead, 2026-10-20).  S = <m, m+B>, layers S_1 = {0} u B,
 * S_2 = (S_1 + S_1) n [0,m), S_3 = S_2 u (S_2 + B)_{<m} u ((S_1 + B)_{>=m} - m), D4 = [0,m) - S_3 (must be covered by
 * (S_3 + B)_{<m} u ((S_2 + B)_{>=m} - m)), h = 1 + max D4.  U2 = S_2 - S_1, N3 = S_3 - S_2.
 * STAR = P_w + J_ge + k h - (k+4) d4,  J_ge = #{(s,b) in U2 x B : s + b >= m},  P_w = #{x <= y in B : x + y >= m}.
 * W = 2k^2 + 2k + (k-2) d2 + k L3 - 3 d3 - 4 d4 (identity).  mode 0: min STAR; 1: min STAR/k; 2: min W; 3: min W/k;
 * 4: min STAR/(k h) over h >= 10; 5: min STAR/d4 over d4 >= 10;
 * 6: min Q4/(k h) over h > e, 3e < m (Q4 = k L3 - 4 d4; LAYER3-W covers Q4 >= 0); 7: min W over Q4 < 0, h > e, 3e < m.
 * usage: ./anT mode seed mlo mhi kmin kmax iters restarts */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define MX 6000
static int mode;
static double urand(void){ return rand() / (RAND_MAX + 1.0); }
typedef struct { int m, k, B[200]; } St;
static long long info[16];
static char in1[MX], s2[2 * MX], s3[MX], s4[MX];
static double evalS(St *s){
  int m = s->m, k = s->k, *B = s->B; if (m < 4 || m >= MX || k < 2 || k > 199) return 1e18;
  memset(in1, 0, m); for (int i = 0; i < k; i++){ if (B[i] < 1 || B[i] >= m || in1[B[i]]) return 1e18; in1[B[i]] = 1; }
  memset(s2, 0, 2 * m); s2[0] = 1; for (int i = 0; i < k; i++){ s2[B[i]] = 1; for (int j = i; j < k; j++) s2[B[i] + B[j]] = 1; }
  /* S_3 */
  memset(s3, 0, m);
  for (int r = 0; r < m; r++) if (s2[r]){ s3[r] = 1; for (int i = 0; i < k; i++){ int t = r + B[i]; if (t < m) s3[t] = 1; } }
  long long Pw = 0;
  for (int i = 0; i < k; i++) for (int j = i; j < k; j++) if (B[i] + B[j] >= m){ s3[B[i] + B[j] - m] = 1; Pw++; }
  /* S_4 coverage */
  memcpy(s4, s3, m);
  for (int r = 0; r < m; r++) if (s3[r]) for (int i = 0; i < k; i++){ int t = r + B[i]; if (t < m) s4[t] = 1; }
  for (int r = 0; r < m; r++) if (s2[r]) for (int i = 0; i < k; i++){ int t = r + B[i]; if (t >= m) s4[t - m] = 1; }
  int h = 0; for (int r = 0; r < m; r++){ if (!s4[r]) return 1e18; if (!s3[r]) h = r + 1; }
  if (h == 0) return 1e18;
  long long d2 = 0, d3 = 0, d4 = 0, L3 = 0, Jge = 0;
  for (int r = 0; r < m; r++){
    int u2 = s2[r] && !in1[r] && r; if (u2){ d2++; for (int i = 0; i < k; i++) if (r + B[i] >= m) Jge++; }
    if (s3[r] && !s2[r]) d3++; if (!s3[r]) d4++; if (s3[r] && r < h) L3++; }
  long long kk = k, STAR = Pw + Jge + kk * h - (kk + 4) * d4;
  long long W = 2 * kk * kk + 2 * kk + (kk - 2) * d2 + kk * L3 - 3 * d3 - 4 * d4;
  info[0] = h; info[1] = W; info[2] = STAR; info[3] = d2; info[4] = d3; info[5] = d4; info[6] = L3; info[7] = Jge; info[8] = Pw;
  switch (mode){ case 0: return STAR; case 1: return (double)STAR / k; case 2: return W; case 3: return (double)W / k;
    case 4: return (h >= 10) ? (double)STAR / ((double)k * h) : 1e18;
    case 5: return (d4 >= 10) ? (double)STAR / d4 : 1e18;
    case 6: return (h > k + 1 && 3 * (k + 1) < m) ? (double)(kk * L3 - 4 * d4) / ((double)k * h) : 1e18;
    default: return (h > k + 1 && 3 * (k + 1) < m && kk * L3 - 4 * d4 < 0) ? (double)W : 1e18; }
}
int main(int argc, char **argv){
  mode = atoi(argv[1]); srand(atoi(argv[2])); int mlo = atoi(argv[3]), mhi = atoi(argv[4]), kmin = atoi(argv[5]), kmax = atoi(argv[6]);
  long iters = atol(argv[7]); int RR = atoi(argv[8]); double best = 1e18;
  for (int rs = 0; rs < RR; rs++){
    St s; double f; int tries = 0;
    do { s.m = mlo + rand() % (mhi - mlo + 1); s.k = kmin + rand() % (kmax - kmin + 1);
      for (int i = 0; i < s.k; i++){ int ok; do { s.B[i] = 1 + rand() % (s.m - 1); ok = 1; for (int j = 0; j < i; j++) if (s.B[j] == s.B[i]) ok = 0; } while (!ok); }
      f = evalS(&s); tries++; } while (f >= 1e17 && tries < 2000000);
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
        printf("mode %d best %.3f m=%d k=%d h=%lld W=%lld STAR=%lld d2=%lld d3=%lld d4=%lld L3=%lld Jge=%lld Pw=%lld B=", mode, best, s.m, s.k, info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8]);
        int tmp[200]; memcpy(tmp, s.B, sizeof(int) * s.k); for (int a = 0; a < s.k; a++) for (int b2 = a + 1; b2 < s.k; b2++) if (tmp[b2] < tmp[a]){ int x = tmp[a]; tmp[a] = tmp[b2]; tmp[b2] = x; }
        for (int a = 0; a < s.k; a++) printf("%d,", tmp[a]); printf("\n"); fflush(stdout); }
      T *= 0.99995; if (T < 0.05) T = 0.05;
    }
  }
}
