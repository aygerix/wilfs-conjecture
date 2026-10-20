/* Annealer for Conjecture J (lead, 2026-10-20). P18 depth four: S = <m, m+B>, B c [1,m-1], 3m < c = 3m+h <= 4m.
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
  int m = s->m, k = s->k, *B = s->B; if (m < 3 || m > MX) return 1e9;
  static char in[MX]; memset(in, 0, m);
  for (int i = 0; i < k; i++){ if (B[i] < 1 || B[i] >= m || in[B[i]]) return 1e9; in[B[i]] = 1; }
  static long long w[MX]; static char done[MX];
  for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return 1e9; done[b] = 1;
    for (int a = 0; a < k; a++){ int j = (b + B[a]) % m; long long v = w[b] + m + B[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
  long long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long long c = M - m + 1; if (!(3 * m < c && c <= 4 * m)) return 1e9;
  int h = (int)(c - 3 * m), e = k + 1;
  static long long sw[MX]; static int ord[MX], car[MX];
  for (int i = 0; i < m; i++) sw[i] = w[i];
  qsort(sw, m, sizeof(long long), cmpw);
  ord[0] = 0;
  for (int t = 1; t < m; t++){ long long v = sw[t]; int r = (int)(v % m), best = -1;
    for (int a = 0; a < k; a++){ long long u = v - m - B[a]; if (u < 0) continue; int ru = (int)(u % m); if (w[ru] == u && ord[ru] + 1 > best) best = ord[ru] + 1; }
    ord[r] = best; }
  long long H[6] = {0}; long long p = 0, q = 0, qQ = 0, H4 = 0, y = 0;
  for (int r = 0; r < m; r++){ int x = (int)(w[r] / m), o = ord[r]; if (o < 0 || o > 5) return 1e9; H[o]++;
    car[r] = (x == 3 && o == 2); if (car[r]) p++; if (x == 4 && o == 4) H4++; if (r < h && x <= 3) y++; }
  for (int r = 0; r < m; r++){ int x = (int)(w[r] / m), o = ord[r]; if (x == 4 && o == 3){ q++; int f = 0;
      for (int a = 0; a < k && !f; a++){ long long u = w[r] - m - B[a]; if (u < 0) continue; int ru = (int)(u % m); if (w[ru] == u && car[ru]) f = 1; }
      qQ += f; } }
  long long E2 = (long long)e * (e - 1) - 2 * H[2], E3 = (long long)(e - 1) * (e + H[2]) - 3 * H[3];
  /* C4 = (e-1) y0 - 4 H4 - q, y0 = uncarried residues < h ; C3 = E3 + chi3 - e p, chi3 = max over reps of carried-parent tokens */
  long long plo = 0; for (int r = 0; r < h; r++) if (car[r]) plo++;
  long long y0 = y - plo, C4 = (long long)(e - 1) * y0 - 4 * H4 - q, chi3 = 0;
  int SB[64]; for (int i = 0; i < k; i++) SB[i] = B[i];
  for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) if (SB[j] < SB[i]){ int t = SB[i]; SB[i] = SB[j]; SB[j] = t; }
  for (int r = 0; r < m; r++){ int x = (int)(w[r] / m), o = ord[r]; if (!(x == 4 && o == 3)) continue;
    long long s3 = w[r] - 3LL * m; int bestc = 0;
    for (int i = 0; i < k; i++) for (int j = i; j < k; j++){ long long z = s3 - SB[i] - SB[j]; if (z < SB[j] || z >= m) continue;
        int kk = -1; for (int t = j; t < k; t++) if (SB[t] == z){ kk = t; break; } if (kk < 0) continue;
        int idx[3] = {i, j, kk}, cc = 0;
        /* tokens: for each distinct value with multiplicity a: (v - jj*g, b) jj = 1..a ; carried iff that element is a carried pair */
        for (int t = 0; t < 3; t++){ int dup = 0; for (int t2 = 0; t2 < t; t2++) if (idx[t2] == idx[t]) dup = 1; if (dup) continue;
          int a = 0; for (int t2 = 0; t2 < 3; t2++) if (idx[t2] == idx[t]) a++;
          for (int jj = 1; jj <= a; jj++){ long long u = w[r] - (long long)jj * (m + SB[idx[t]]); if (u <= 0) continue; int ru = (int)(u % m); if (w[ru] == u && car[ru]) cc++; } }
        if (cc > bestc) bestc = cc; }
    chi3 += bestc; }
  long long C3 = E3 + chi3 - (long long)e * p;
  long long CL = E2 + (E3 - (long long)(e - 1) * p + chi3) + C4 - p;  /* = U2 + U3 + U4 - p - q */
  long long J = E2 + (long long)(e - 1) * y - 4 * H4 - q - 3 * qQ - p, W = (long long)e * (c - g) - c;
  long long sigma = E3 - (long long)(e - 1) * p + 3 * qQ;
  if (W != J + sigma){ fprintf(stderr, "IDENTITY FAIL m=%d\n", m); exit(1); }
  int known = (h <= e) || ((long long)e * (e + 1) >= 2 * m) || ((long long)(e - 1) * (e - 1) >= 2 * m) || (3 * e >= m);
  info[0] = h; info[1] = e; info[2] = W; info[3] = J; info[4] = E2; info[5] = y; info[6] = H4; info[7] = q; info[8] = qQ; info[9] = p; info[10] = sigma; info[11] = known; info[12] = H[2]; info[13] = H[3];
  info[14] = C3; info[15] = C4; info[16] = CL;
  switch (mode){ case 0: return J; case 1: return h > e ? J : 1e9; case 2: return known ? 1e9 : J;
    case 4: return h > e ? C4 : 1e9; case 5: return h > e ? C3 : 1e9; case 6: return known ? 1e9 : C4; case 7: return known ? 1e9 : C3;
    case 8: return C4; case 9: return C3; case 10: return h > e ? CL : 1e9; case 11: return CL; case 12: return known ? 1e9 : CL;
    default: return W; }
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
        printf("mode %d best %.0f m=%d e=%lld h=%lld W=%lld J=%lld E2=%lld y=%lld H4=%lld q=%lld qQ=%lld p=%lld sigma=%lld known=%lld H2=%lld H3=%lld C3=%lld C4=%lld CL=%lld B=", mode, best, s.m, info[1], info[0], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10], info[11], info[12], info[13], info[14], info[15], info[16]);
        int tmp[64]; memcpy(tmp, s.B, sizeof(int) * s.k); for (int a = 0; a < s.k; a++) for (int b2 = a + 1; b2 < s.k; b2++) if (tmp[b2] < tmp[a]){ int x = tmp[a]; tmp[a] = tmp[b2]; tmp[b2] = x; }
        for (int a = 0; a < s.k; a++) printf("%d,", tmp[a]); printf("\n"); fflush(stdout); }
      T *= 0.99995; if (T < 0.05) T = 0.05;
    }
  }
}
