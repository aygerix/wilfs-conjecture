/* Lead's independent re-implementation of codex P10 section 10 (placed-face certificate, support-two e=5 tiles),
 * written from the report text only.  For m in [mlo, mhi]:
 *   ordered edge tuple a_e (e over the 6 edges of K4) with sum C(a_e+1,2) <= m-5 (FACE-A; N1 >= 4),
 *   J subset of [4] containing every isolated vertex (b_i = max incident a_e = 0),
 *   l_i = b_i + [i in J] if b_i > 0 else 1;  N2 from sum C(a_e+1,2) up to m-1-sum l_i;  N1 = m-1-N2.
 *   R_lower = rank term of {a_e copies of a_e+5} u {4+l_i : i in J}; if J = [4], min over the 4 lists that add
 *   E = N1 - sum l_i to one axis weight.   H_* = max(0, ceil(3m - 15|J|/4 - 6t), D2(N2;f) + J12(3N1-N2-f)).
 *   Check 2[(m+1)H_* + R_lower] - 3m(m-1) > 0.
 * gcc -O3 -std=gnu11 s2fin_lead.c -o s2fin_lead ; ./s2fin_lead mlo mhi */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int64_t C2(int64_t a) { return a * (a - 1) / 2; }
static int64_t D2(int64_t n, int f) { int64_t s = 0, j = 0; while (n > 0) { int64_t cap = (int64_t)f * (j + 1), take = cap < n ? cap : n; s += take * j; n -= take; j++; } return s; }
static int64_t J12(int64_t S) { if (S < 0) return 0; int64_t u = S / 12, r = S % 12; return 12 * C2(u) + r * u; }
static int cmpd(const void *a, const void *b) { return (*(const int *)b) - (*(const int *)a); }
static int64_t rank_term(int *w, int n) { int t[128]; for (int i = 0; i < n; i++) t[i] = w[i]; qsort(t, n, sizeof(int), cmpd); int64_t R = 0; for (int i = 0; i < n; i++) R += (int64_t)i * t[i]; return R; }
static const int EU[6] = {0, 0, 0, 1, 1, 2}, EV[6] = {1, 2, 3, 2, 3, 3};
int main(int argc, char **argv) {
  int mlo = atoi(argv[1]), mhi = atoi(argv[2]);
  for (int m = mlo; m <= mhi; m++) {
    int cap = m - 5; long long tuples = 0, profiles = 0, fails = 0; int64_t minsl = INT64_MAX; char best[256] = "";
    int A = 0; while (C2(A + 2) <= cap) A++;   /* max a with C(a+1,2) <= cap */
    int a[6];
    for (a[0] = 0; a[0] <= A; a[0]++) for (a[1] = 0; a[1] <= A; a[1]++) for (a[2] = 0; a[2] <= A; a[2]++)
    for (a[3] = 0; a[3] <= A; a[3]++) for (a[4] = 0; a[4] <= A; a[4]++) for (a[5] = 0; a[5] <= A; a[5]++) {
      int64_t cost = 0; for (int e = 0; e < 6; e++) cost += C2(a[e] + 1);
      if (cost > cap) continue;
      tuples++;
      int b[4] = {0, 0, 0, 0}, f = 0, t = 0;
      for (int e = 0; e < 6; e++) { if (a[e] > b[EU[e]]) b[EU[e]] = a[e]; if (a[e] > b[EV[e]]) b[EV[e]] = a[e]; if (a[e] > 0) f++; t += a[e]; }
      int base[128], nb = 0;
      for (int e = 0; e < 6; e++) for (int k = 0; k < a[e]; k++) base[nb++] = a[e] + 5;
      int iso = 0; for (int i = 0; i < 4; i++) if (b[i] == 0) iso |= 1 << i;
      for (int Jm = 0; Jm < 16; Jm++) {
        if ((Jm & iso) != iso) continue;
        int l[4], sl = 0, t1 = 0;
        for (int i = 0; i < 4; i++) { int inJ = (Jm >> i) & 1; t1 += inJ; l[i] = b[i] > 0 ? b[i] + inJ : 1; sl += l[i]; }
        int w[128], nw = nb; for (int k = 0; k < nb; k++) w[k] = base[k];
        int ax[4], na = 0; for (int i = 0; i < 4; i++) if ((Jm >> i) & 1) { ax[na] = i; w[nw + na] = 4 + l[i]; na++; }
        int64_t Rfix = rank_term(w, nw + na);
        for (int64_t N2 = cost; N2 <= m - 1 - sl; N2++) {
          if (f == 0 && N2 > 0) break;   /* no positive face => no support-two cells */
          int64_t N1 = m - 1 - N2, E = N1 - sl;
          int64_t R = Rfix;
          if (Jm == 15 && E > 0) {
            R = INT64_MAX;
            for (int k = 0; k < 4; k++) { int w2[128]; for (int z = 0; z < nw + na; z++) w2[z] = w[z]; w2[nw + k] += (int)E;
              int64_t r2 = rank_term(w2, nw + na); if (r2 < R) R = r2; }
          }
          int64_t hb4 = 12 * m - 15 * t1 - 24 * t;  /* 4 * (3m - 15 t1/4 - 6t) */
          int64_t hb = hb4 > 0 ? (hb4 + 3) / 4 : 0;
          int64_t hf = D2(N2, f) + J12(3 * N1 - N2 - f);
          int64_t H = hb > hf ? hb : hf; if (H < 0) H = 0;
          int64_t sl2 = 2 * ((int64_t)(m + 1) * H + R) - 3LL * m * (m - 1);
          profiles++;
          if (sl2 < minsl) { minsl = sl2; snprintf(best, 256, "a=(%d,%d,%d,%d,%d,%d) J=%d N2=%lld H=%lld R=%lld", a[0], a[1], a[2], a[3], a[4], a[5], Jm, (long long)N2, (long long)H, (long long)R); }
          if (sl2 <= 0) fails++;
        }
      }
    }
    printf("m=%d tuples=%lld profiles=%lld failures=%lld min_slack=%lld/2 at %s\n", m, tuples, profiles, fails, (long long)minsl, best);
    fflush(stdout);
  }
  return 0;
}
