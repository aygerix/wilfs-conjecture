/* q5ann: adversarial search for PAY2 failures on the Q5 residual at larger e (lead, 2026-10-21).
 * Same membership test and invariants as q5d5 (Q5: S = <m, m + A>, all generators minimal, q = 5, every factorization
 * of every Apery element of length <= 3; residual: U != T).  Objective (minimized):
 *   residual S:      PAY2 = Delta3 + (e-1) dc - e h           (h = |T \ U|, dc = c(U) - c(T))
 *   Q5 with U = T:   BIG + Delta3                            (stepping stone)
 *   not in Q5:       rejected
 * Moves: replace one residue (uniform, or +-1..3); simulated annealing with temperature T0 -> 0.
 * usage: ./q5ann d mlo mhi restarts steps seed [T0]
 * Prints per m: tries, Q5 starts, residual states visited, PAY2 failures, min PAY2 with S and (h, dc, Delta3). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define MAXM 400
#define BIG 1000000L
static int m, d, e;
typedef struct { int inQ5, res; long p2, h, dc, D3, W; } Ev;
static Ev eval(const int *a){
  Ev v; memset(&v, 0, sizeof v);
  static int w[MAXM], done[MAXM], order[MAXM], hmx[MAXM], sg[MAXM], tau[MAXM], dn[MAXM]; int G[32], lim = 6 * m;
  for (int x = 0; x < m; x++){ w[x] = 1 << 29; done[x] = 0; } w[0] = 0;
  for (int b = 0; b < d; b++) G[b] = m + a[b];
  for (int it = 0; it < m; it++){
    int u = -1; for (int x = 0; x < m; x++) if (!done[x] && (u < 0 || w[x] < w[u])) u = x;
    if (w[u] >= lim) return v;
    done[u] = 1; order[it] = u;
    for (int b = 0; b < d; b++){ int vv = w[u] + G[b], t = vv % m; if (vv < w[t]) w[t] = vv; }
  }
  for (int b = 0; b < d; b++) if (w[a[b]] != G[b]) return v;
  int r = 0; for (int x = 1; x < m; x++) if (w[x] > w[r]) r = x;
  if (w[r] < 5 * m) return v;
  hmx[0] = 0;
  for (int it = 1; it < m; it++){
    int x = order[it]; hmx[x] = -1;
    for (int b = 0; b < d; b++){ int t = ((x - a[b]) % m + m) % m;
      if (w[t] == w[x] - G[b]){ if (t != 0 && hmx[t] < 0) return v; if (hmx[t] + 1 > hmx[x]) hmx[x] = hmx[t] + 1; } }
    if (hmx[x] < 0 || hmx[x] > 3) return v;
  }
  v.inQ5 = 1;
  long c = w[r] - m + 1, g = 0; for (int x = 1; x < m; x++) g += w[x] / m;
  v.W = (long)e * (c - g) - c; long H = 0; int mxs = 0;
  for (int x = 0; x < m; x++){ sg[x] = w[x] - m * hmx[x]; H += hmx[x]; if (sg[x] > mxs) mxs = sg[x]; }
  v.D3 = 3L * (e - 1) * m - (long)e * H;
  if (mxs != 2 * m + r){ fprintf(stderr, "max sigma != 2m + r\n"); exit(12); }
  for (int x = 0; x < m; x++){ tau[x] = 1 << 29; dn[x] = 0; } tau[0] = 0;
  for (int it = 0; it < m; it++){ int u = -1; for (int x = 0; x < m; x++) if (!dn[x] && (u < 0 || tau[x] < tau[u])) u = x;
    dn[u] = 1; for (int b = 0; b < d; b++){ int vv = tau[u] + a[b], t = vv % m; if (vv < tau[t]) tau[t] = vv; } }
  int maxtau = 0; for (int x = 0; x < m; x++){ if (tau[x] < sg[x]){ v.res = 1; v.h += (sg[x] - tau[x]) / m; } if (tau[x] > maxtau) maxtau = tau[x]; }
  v.dc = (long)mxs - maxtau;
  v.p2 = v.D3 + (long)(e - 1) * v.dc - (long)e * v.h;
  return v;
}
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static double urand(void){ return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static int cmpint(const void *x, const void *y){ return *(const int *)x - *(const int *)y; }
static double obj(const Ev *v){ return v->res ? (double)v->p2 : (double)(BIG + v->D3); }
int main(int argc, char **argv){
  if (argc < 7){ fprintf(stderr, "usage: ./q5ann d mlo mhi restarts steps seed [T0]\n"); return 1; }
  d = atoi(argv[1]); int mlo = atoi(argv[2]), mhi = atoi(argv[3]), restarts = atoi(argv[4]), steps = atoi(argv[5]);
  rs ^= (unsigned long long)atoll(argv[6]) * 2654435761ULL; double T0 = argc > 7 ? atof(argv[7]) : 8.0; e = d + 1;
  if (mhi >= MAXM || d > 30){ fprintf(stderr, "bad parameters\n"); return 1; }
  long gfail = 0; long gmin = 1L << 40; int gA[32] = {0}, gm = 0;
  for (m = mlo; m <= mhi; m++){
    if (m - 1 < d) continue;
    long tries = 0, starts = 0, resvisits = 0, fails = 0, minp = 1L << 40; int minA[32] = {0}; Ev minv; memset(&minv, 0, sizeof minv);
    for (int rr = 0; rr < restarts; rr++){
      int a[32]; Ev cur; int ok = 0;
      for (int t = 0; t < 20000 && !ok; t++){ tries++;
        char used[MAXM] = {0}; for (int i = 0; i < d; i++){ int x; do x = 1 + rnd() % (m - 1); while (used[x]); used[x] = 1; a[i] = x; }
        cur = eval(a); if (cur.inQ5) ok = 1; }
      if (!ok) continue;
      starts++;
      for (int st = 0; st < steps; st++){
        double Tt = T0 * (1.0 - (double)st / steps);
        int b[32]; memcpy(b, a, sizeof b); int i = rnd() % d, x, tr = 0;
        do { x = (rnd() & 1) ? 1 + rnd() % (m - 1) : b[i] + (int)(rnd() % 7) - 3; tr++; } while ((x < 1 || x > m - 1) && tr < 50);
        if (x < 1 || x > m - 1) continue;
        int dup = 0; for (int j = 0; j < d; j++) if (j != i && b[j] == x) dup = 1; if (dup) continue;
        b[i] = x; Ev nv = eval(b); if (!nv.inQ5) continue;
        if (nv.res){ resvisits++; if (nv.p2 < 0){ fails++; int s2[32]; memcpy(s2, b, sizeof s2); qsort(s2, d, sizeof(int), cmpint);
            printf("PAY2 FAILS %ld at <%d", nv.p2, m); for (int q = 0; q < d; q++) printf(",%d", m + s2[q]); printf("> h=%ld dc=%ld D3=%ld W=%ld\n", nv.h, nv.dc, nv.D3, nv.W); }
          if (nv.p2 < minp){ minp = nv.p2; memcpy(minA, b, sizeof minA); qsort(minA, d, sizeof(int), cmpint); minv = nv; } }
        double dlt = obj(&nv) - obj(&cur);
        if (dlt <= 0 || (Tt > 1e-9 && urand() < exp(-dlt / Tt))){ memcpy(a, b, sizeof a); cur = nv; }
      }
    }
    printf("m=%d d=%d e=%d tries=%ld Q5starts=%ld residual_visits=%ld PAY2fail=%ld", m, d, e, tries, starts, resvisits, fails);
    if (resvisits){ printf(" minPAY2=%ld at <%d", minp, m); for (int q = 0; q < d; q++) printf(",%d", m + minA[q]); printf("> h=%ld dc=%ld D3=%ld W=%ld", minv.h, minv.dc, minv.D3, minv.W);
      if (minp < gmin){ gmin = minp; memcpy(gA, minA, sizeof gA); gm = m; } }
    gfail += fails; printf("\n"); fflush(stdout);
  }
  printf("GLOBAL d=%d PAY2fail=%ld minPAY2=%ld at <%d", d, gfail, gmin, gm); for (int q = 0; q < d; q++) printf(",%d", gm + gA[q]); printf(">\n");
  return 0;
}
