/* Kunz-coordinate annealing for CHAIN-WILF and RC (lead).
   State: Apery set w[0..m-1] (w[0]=0, w[i] = i mod m, w[i] >= m+? ), Kunz-valid:
     w[j] + w[k] >= w[(j+k) % m] for all j,k != 0 with j+k != 0 mod m.
   Objective: ratio_chain = B_chain/need, need = (d-1) m (m-1)/2, d = e-1 (e >= 3), restricted to c > (QMIN-1) m.
   B_chain = sum_a sum_w (M - top_a(w)), R = sum_a sum_w ((M-w) mod n_a).
   Also tracks W = e*ell - c (asserts the identity B = dmM-(d+1)sum Ap = mW + need).
   usage: ./chain_kunz seed m steps chains QMIN start EMAX  (start: 0=T_{m,q}, 1=random descent, 2=mixed)  */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
static uint64_t rs;
static uint64_t rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static double urand(void){ return (rnd() >> 11) * (1.0/9007199254740992.0); }
static int m, QMIN, EMAX, OBJ = 0; static double PEN = 0.15;
static int64_t w[256];
static int kunz_ok_at(int i){ /* check all inequalities involving index i */
  for (int j = 1; j < m; j++) {
    if (j == i) { int k = (2*i) % m; if (k && w[i] + w[i] < w[k]) return 0; continue; }
    int k = (i + j) % m; if (k && w[i] + w[j] < w[k]) return 0;          /* i as summand */
    int jj = (i - j + m) % m; if (jj && w[j] + w[jj] < w[i]) return 0;   /* i as target */
  }
  return 1;
}
typedef struct { double rc, ch, f, pw; int e, q; int64_t W, c, M; } Res;
static int eval(Res *r){
  int64_t M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  int64_t c = M - m + 1; int q = (int)((c + m - 1) / m);
  if (q < QMIN) return 0;
  int gen[256], d = 0;
  for (int i = 1; i < m; i++) {
    int ok = 1;
    for (int j = 1; j < m && ok; j++) { int k = (i - j + m) % m; if (k && w[j] + w[k] == w[i]) ok = 0; }
    if (ok) gen[d++] = i;
  }
  if (d < 2) return 0;
  int64_t sumAp = 0, ell = 0;
  for (int i = 0; i < m; i++) { sumAp += w[i]; if (w[i] < c) ell += (c - 1 - w[i]) / m + 1; }
  int64_t W = (int64_t)(d + 1) * ell - c;
  int64_t need = (int64_t)(d - 1) * m * (m - 1) / 2;
  int64_t B = (int64_t)d * m * M - (int64_t)(d + 1) * sumAp;
  if (B != (int64_t)m * W + need) { fprintf(stderr, "IDENTITY FAIL\n"); exit(1); }
  int64_t Bc = 0, R = 0, cw[256] = {0}, PW = 0;
  for (int a = 0; a < d; a++) { int64_t n = w[gen[a]];
    for (int i = 0; i < m; i++) {
      int64_t t = w[i];
      for (;;) { int64_t t2 = t + n; if (t2 > M) break; if (w[t2 % m] != t2) break; t = t2; }
      Bc += M - t; R += (M - w[i]) % n; cw[i] += (M - w[i]) % m - (M - t);
    }
  }
  for (int i = 0; i < m; i++) if (cw[i] > 0) PW += cw[i];
  if (!(B >= Bc && Bc >= R)) { fprintf(stderr, "ORDER FAIL\n"); exit(1); }
  r->rc = (double)R / need; r->ch = (double)Bc / need; r->pw = (double)PW / ((double)m * (m - 1) / 2); r->f = (OBJ ? -r->pw : r->ch) + PEN * (d + 1 > EMAX ? d + 1 - EMAX : 0); r->e = d + 1; r->q = q; r->W = W; r->c = c; r->M = M;
  return 1;
}
int main(int argc, char **argv){
  rs = 0x9E3779B97F4A7C15ULL ^ (uint64_t)atoll(argv[1]) * 2654435761ULL; if (!rs) rs = 1;
  m = atoi(argv[2]); long steps = atol(argv[3]); int chains = atoi(argv[4]); QMIN = atoi(argv[5]);
  int start = atoi(argv[6]); EMAX = atoi(argv[7]); if (argc > 8) OBJ = atoi(argv[8]);
  double gbest = 1e9; int64_t gw[256]; Res gr;
  double ebest[257]; for (int i = 0; i < 257; i++) ebest[i] = 1e9;
  double pwmax[257]; for (int i = 0; i < 257; i++) pwmax[i] = -1; long pwfail = 0;
  long fails = 0;
  for (int ch = 0; ch < chains; ch++) {
    int qs = QMIN + (int)(rnd() % 3);
    w[0] = 0;
    for (int i = 1; i < m; i++) w[i] = (int64_t)qs * m + i;      /* T_{m,qs} */
    int len = (start == 0) ? 2 * m : (start == 1 ? 20 * m : (int)(rnd() % (20 * m)) + m);
    Res cur; int okst = 0;
    for (int it = 0; it < 200 * m && !okst; it++) {            /* random descent from T until e <= EMAX */
      int i = 1 + rnd() % (m - 1); int64_t old = w[i];
      w[i] -= m; if (w[i] < m + i || !kunz_ok_at(i)) { w[i] = old; continue; }
      int64_t MM = 0; for (int k = 0; k < m; k++) if (w[k] > MM) MM = w[k];
      if (MM < (int64_t)QMIN * m) { w[i] = old; continue; }
      if (it >= len && eval(&cur)) okst = 1;
      if (it < len) okst = 0;
    }
    if (getenv("DBG")) { int64_t MM = 0; for (int k = 0; k < m; k++) if (w[k] > MM) MM = w[k];
      int gg = 0; for (int i2 = 1; i2 < m; i2++) { int ok = 1;
        for (int j = 1; j < m && ok; j++) { int k = (i2 - j + m) % m; if (k && w[j] + w[k] == w[i2]) ok = 0; } gg += ok; }
      fprintf(stderr, "ch %d okst %d MM %lld e %d\n", ch, okst, (long long)MM, gg + 1); }
    if (!okst && !eval(&cur)) continue;
    double T = 0.05;
    for (long it = 0; it < steps; it++) {
      int i = 1 + rnd() % (m - 1); int64_t old = w[i];
      int dlt = (urand() < 0.5) ? -1 : 1; if (urand() < 0.2) dlt *= 2;
      w[i] += (int64_t)dlt * m;
      if (w[i] < i + m || w[i] > (int64_t)(QMIN + 3) * m + m || !kunz_ok_at(i)) { w[i] = old; continue; }
      Res r; if (!eval(&r)) { w[i] = old; continue; }
      if (r.ch < ebest[r.e]) ebest[r.e] = r.ch;
      if (r.pw > pwmax[r.e]) pwmax[r.e] = r.pw;
      if (r.pw > 1.0 + 1e-12) { pwfail++; if (pwfail <= 10) { printf("PWFAIL pw=%.5f ch=%.4f e=%d q=%d W=%lld c=%lld w=", r.pw, r.ch, r.e, r.q, (long long)r.W, (long long)r.c); for (int k = 0; k < m; k++) printf("%lld,", (long long)w[k]); printf("\n"); } }
      if (r.ch < 1.0) { fails++; if (fails <= 20) { printf("FAIL ch=%.5f rc=%.4f e=%d q=%d W=%lld c=%lld w=", r.ch, r.rc, r.e, r.q, (long long)r.W, (long long)r.c); for (int k = 0; k < m; k++) printf("%lld,", (long long)w[k]); printf("\n"); } }
      if (r.f < cur.f || urand() < exp(-(r.f - cur.f) / T)) cur = r; else w[i] = old;
      if (r.e <= EMAX && r.ch < gbest) { gbest = r.ch; memcpy(gw, w, sizeof(int64_t) * m); gr = r; }
      T *= 0.9997; if (T < 1e-4) T = 1e-4;
    }
  }
  printf("EMAX=%d m=%d QMIN=%d start=%d best_chain=%.5f rc=%.4f e=%d q=%d W=%lld c=%lld fails=%ld\n  w=", EMAX, m, QMIN, start, gbest, gr.rc, gr.e, gr.q, (long long)gr.W, (long long)gr.c, fails);
  for (int k = 0; k < m; k++) printf("%lld,", (long long)gw[k]); printf("\n  min chain ratio by e:");
  for (int e = 3; e <= m; e++) if (ebest[e] < 1e8) printf(" %d:%.3f", e, ebest[e]);
  printf("\n  max PW/C2 by e:");
  for (int e = 3; e <= m; e++) if (pwmax[e] >= 0) printf(" %d:%.3f", e, pwmax[e]);
  printf("\n  pwfails=%ld\n", pwfail);
  return 0;
}
