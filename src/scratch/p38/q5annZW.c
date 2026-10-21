/* q5annZW (p38, 2026-10-21): q5annCU + Conjecture ZW (Delta3 + e z >= c_U, z = #{s : sigma_s < m}).
 * Extra env OBJZ=1: maximize (c_U - e z)/Delta3 over residual states (OBJZ=2: over all Q5 states). Prints ZW FAILS, MAXZW.
 * q5annCU (p38, 2026-10-21): q5annMU + Conjecture CU (Delta3 >= c(U) - 3mu) on ALL Q5 states (residual or U = T).
 * Extra env OBJC=1: maximize (c_U - 3mu)/Delta3 over every Q5 state.  Prints CU FAILS and MAXCU (all / residual).
 * q5annMU (p38, 2026-10-21): q5annA1 + the mu-split terms (Identity W-mu): hlo_mu, U_mu, U', u', Qa, Qb, MU-LO.
 * Extra env: OBJM=1 maximize (mu*hlo_mu + h_hi)/Delta3 (mu <= e states only count as residual); OBJQ=1 minimize Qa.
 * q5annA1 (from q5ann): objective = A1 slack D3 - e*h_lo - h_hi (h_lo: T\U below c(T)); optional fixed a_1 = MU (env MU, never moved).
 * q5ann: adversarial search for PAY2 failures on the Q5 residual at larger e (lead, 2026-10-21).
 * Same membership test and invariants as q5d5 (Q5: S = <m, m + A>, all generators minimal, q = 5, every factorization
 * of every Apery element of length <= 3; residual: U != T).  Objective (minimized):
 *   residual S:      PAY2 = Delta3 + (e-1) dc - e h           (h = |T \ U|, dc = c(U) - c(T))
 *   Q5 with U = T:   BIG + Delta3                            (stepping stone)
 *   not in Q5:       rejected
 * Moves: replace one residue (uniform, or +-1..3); simulated annealing with temperature T0 -> 0.
 * usage: ./q5ann d mlo mhi restarts steps seed [T0]
 * Prints per m: tries, Q5 starts, residual states visited, PAY2 failures, min PAY2 with S and (h, dc, Delta3).
 * Hard stop: any class with j_s = (sigma_s - tau_s)/m >= 2 is printed ("J2 FOUND") and the program exits with code 30. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define MAXM 400
#define BIG 1000000L
static int m, d, e;
typedef struct { int inQ5, res; long p2, h, dc, D3, W, a1, hlo, hhi, eT, lT, aeT, desc, mu, hlomu, Umu, Up, up, Qa, Qb, mulo, cU, z; } Ev;
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
  int maxtau = 0; for (int x = 0; x < m; x++){ if (tau[x] < sg[x]){ v.res = 1; v.h += (sg[x] - tau[x]) / m;
      if ((sg[x] - tau[x]) / m >= 2){ printf("J2 FOUND class %d sigma=%d tau=%d h=%d at <%d", x, sg[x], tau[x], hmx[x], m); for (int q = 0; q < d; q++) printf(",%d", m + a[q]); printf(">\n"); fflush(stdout); exit(30); } }
    if (tau[x] > maxtau) maxtau = tau[x]; }
  v.dc = (long)mxs - maxtau;
  v.p2 = v.D3 + (long)(e - 1) * v.dc - (long)e * v.h;
  { int cT = maxtau - m + 1; v.hlo = v.hhi = 0;
    for (int x = 0; x < m; x++) for (int z = tau[x]; z < sg[x]; z += m){ if (z < cT) v.hlo++; else v.hhi++; }
    v.a1 = v.D3 - (long)e * v.hlo - v.hhi;
    /* e(T), l(T), |U n [0, c_T)|, A1-eT slack, DESC = W(S) - W(T) = PAY2 + (e - e_T) l_T */
    static char inT[3 * MAXM + 8]; int N = 3 * m + 2; long lT = 0, lUlo = 0, eT = 0;
    for (int z = 0; z <= N; z++) inT[z] = (z >= tau[z % m]);
    for (int z = 0; z < cT; z++){ if (inT[z]) lT++; if (z >= sg[z % m]) lUlo++; }
    for (int q = 0; q <= d; q++){ int g = q < d ? a[q] : m, dec = 0; for (int y = 1; y < g && !dec; y++) if (inT[y] && inT[g - y]) dec = 1; if (!dec) eT++; }
    v.eT = eT; v.lT = lT; v.aeT = v.D3 + (long)(e - eT) * lUlo - eT * v.hlo - v.hhi; v.desc = v.p2 + (long)(e - eT) * lT;
    int mu = a[0]; for (int q = 1; q < d; q++) if (a[q] < mu) mu = a[q]; v.mu = mu;
    long hm = 0, Um = 0, Upr = 0, upr = 0; int cU = mxs - m + 1;
    for (int z = 0; z < cT; z++){ int inU = z >= sg[z % m]; if (z % mu == 0){ if (inU) Um++; else hm++; } else if (inU) Upr++; }
    for (int z = cT; z < cU; z++) if (z >= sg[z % m]) upr++;
    v.cU = cU; { long zz = 0; for (int x = 0; x < m; x++) if (sg[x] < m) zz++; v.z = zz; } v.hlomu = hm; v.Umu = Um; v.Up = Upr; v.up = upr;
    v.Qa = (long)(e - mu) * Um + (long)e * Upr - (long)mu * hm; v.Qb = v.D3 + (long)(e - 1) * upr - v.hhi; v.mulo = v.D3 - (long)mu * hm - v.hhi;
    { long theta = (long)mu * ((cT + mu - 1) / mu) - cT; if (v.W != v.Qa + v.Qb + theta){ fprintf(stderr, "W-mu identity mismatch\n"); exit(13); } } }
  return v;
}
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static double urand(void){ return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static int cmpint(const void *x, const void *y){ return *(const int *)x - *(const int *)y; }
static int OBJR;   /* env OBJR=1: maximize the A1 ratio (e h_lo + h_hi)/Delta3 instead of minimizing the slack */
static int OBJE;   /* env OBJE=1: minimize the A1-eT slack (A1 slack otherwise) */
static int OBJW;   /* env OBJW=1: minimize W(S) itself on residual states */
static int OBJH; static int OBJM; static int OBJQ; static int OBJC; static int OBJZ;   /* env OBJH=1: minimize Delta3 / |T\\U| (candidate D6: Delta3 >= 6|T\\U|) */
static double obj(const Ev *v){ if (OBJZ && (v->res || OBJZ == 2)) return v->D3 > 0 ? -1000.0 * (double)(v->cU - (long)e * v->z) / (double)v->D3 : -1e9;
  if (OBJZ) return (double)(BIG + v->D3);
  if (OBJC) return v->D3 > 0 ? -1000.0 * (double)(v->cU - 3 * v->mu) / (double)v->D3 : -1e9;
  if (!v->res || ((OBJM || OBJQ) && v->mu > e)) return (double)(BIG + v->D3);
  if (OBJM) return -1000.0 * (double)(v->D3 - v->mulo) / (double)(v->D3 > 0 ? v->D3 : 1);
  if (OBJQ) return (double)v->Qa;
  if (OBJR) return -1000.0 * (double)(OBJE ? v->D3 - v->aeT : v->D3 - v->a1) / (double)(v->D3 > 0 ? v->D3 : 1);
  if (OBJW) return (double)v->W;
  if (OBJH) return 1000.0 * (double)v->D3 / (double)(v->h > 0 ? v->h : 1);
  return OBJE ? (double)v->aeT : (double)v->a1; }
int main(int argc, char **argv){
  if (argc < 7){ fprintf(stderr, "usage: ./q5ann d mlo mhi restarts steps seed [T0]\n"); return 1; }
  d = atoi(argv[1]); int mlo = atoi(argv[2]), mhi = atoi(argv[3]), restarts = atoi(argv[4]), steps = atoi(argv[5]);
  rs ^= (unsigned long long)atoll(argv[6]) * 2654435761ULL; double T0 = argc > 7 ? atof(argv[7]) : 8.0; e = d + 1;
  if (mhi >= MAXM || d > 30){ fprintf(stderr, "bad parameters\n"); return 1; }
  long gfail = 0; long gmin = 1L << 40; int gA[32] = {0}, gm = 0; int MU = getenv("MU") ? atoi(getenv("MU")) : 0; OBJR = getenv("OBJR") != NULL; OBJE = getenv("OBJE") != NULL; OBJW = getenv("OBJW") != NULL; OBJH = getenv("OBJH") != NULL; OBJM = getenv("OBJM") != NULL; OBJQ = getenv("OBJQ") != NULL; OBJC = getenv("OBJC") != NULL; OBJZ = getenv("OBJZ") ? atoi(getenv("OBJZ")) : 0; double maxzw[2] = {-1e9, -1e9}; int zwA[2][32] = {{0}}, zwm[2] = {0, 0}; long zwD3[2] = {0, 0}, zwz[2] = {0, 0}, zwcU[2] = {0, 0}; double maxcu[2] = {0, 0}; int cuA[2][32] = {{0}}, cum[2] = {0, 0}; long cuD3[2] = {0, 0}, cucU[2] = {0, 0}, cumu[2] = {0, 0}; double maxmr = 0; int mrA[32] = {0}, mrm = 0; long mrD3 = 0, mrhm = 0, mrhh = 0; long minQa = 1L << 40; int qaA[32] = {0}, qam = 0; double minDh = 1e18; int dhA[32] = {0}, dhm = 0; long dhD3 = 0, dhh = 0; int BLO = getenv("BLO") ? atoi(getenv("BLO")) : 0; long minW = 1L << 40; int wA[32] = {0}, wm = 0; long minaeT = 1L << 40, mindesc = 1L << 40; int aeA[32] = {0}, aem = 0; double maxrat = 0; int ratA[32] = {0}, ratm = 0; long ratD3 = 0, rathlo = 0, rathhi = 0;
  for (m = mlo; m <= mhi; m++){
    if (m - 1 < d) continue;
    long tries = 0, starts = 0, resvisits = 0, fails = 0, minp = 1L << 40; int minA[32] = {0}; Ev minv; memset(&minv, 0, sizeof minv);
    for (int rr = 0; rr < restarts; rr++){
      int a[32]; Ev cur; int ok = 0;
      for (int t = 0; t < 20000 && !ok; t++){ tries++;
        char used[MAXM] = {0}; for (int i = 0; i < d; i++){ int x; if (i == 0 && MU){ x = MU; } else { do x = (MU ? MU + 1 + rnd() % (m - 1 - MU) : 1 + rnd() % (m - 1)); while (used[x] || (MU && x * 100 < BLO * m)); } used[x] = 1; a[i] = x; }
        cur = eval(a); if (cur.inQ5) ok = 1; }
      if (!ok) continue;
      starts++;
      for (int st = 0; st < steps; st++){
        double Tt = T0 * (1.0 - (double)st / steps);
        int b[32]; memcpy(b, a, sizeof b); int i = MU ? 1 + rnd() % (d - 1) : rnd() % d, x, tr = 0;
        do { x = (rnd() & 1) ? 1 + rnd() % (m - 1) : b[i] + (int)(rnd() % 7) - 3; tr++; } while ((x < 1 || x > m - 1) && tr < 50);
        if (x < 1 || x > m - 1 || (MU && x <= MU) || (MU && x * 100 < BLO * m)) continue;
        int dup = 0; for (int j = 0; j < d; j++) if (j != i && b[j] == x) dup = 1; if (dup) continue;
        b[i] = x; Ev nv = eval(b); if (!nv.inQ5) continue;
        { int R = nv.res ? 1 : 0; double cr = nv.D3 > 0 ? (double)(nv.cU - 3 * nv.mu) / nv.D3 : 1e9;
          if (cr > maxcu[R]){ maxcu[R] = cr; memcpy(cuA[R], b, sizeof cuA[R]); qsort(cuA[R], d, sizeof(int), cmpint); cum[R] = m; cuD3[R] = nv.D3; cucU[R] = nv.cU; cumu[R] = nv.mu; }
          { double zr = nv.D3 > 0 ? (double)(nv.cU - (long)e * nv.z) / nv.D3 : 1e9;
            if (zr > maxzw[R]){ maxzw[R] = zr; memcpy(zwA[R], b, sizeof zwA[R]); qsort(zwA[R], d, sizeof(int), cmpint); zwm[R] = m; zwD3[R] = nv.D3; zwz[R] = nv.z; zwcU[R] = nv.cU; }
            if (nv.D3 + (long)e * nv.z < nv.cU){ int s9[32]; memcpy(s9, b, sizeof s9); qsort(s9, d, sizeof(int), cmpint); printf("ZW FAILS res=%d D3=%ld z=%ld cU=%ld W=%ld at <%d", R, nv.D3, nv.z, nv.cU, nv.W, m); for (int q = 0; q < d; q++) printf(",%d", m + s9[q]); printf(">\n"); fflush(stdout); } }
          if (nv.D3 < nv.cU - 3 * nv.mu){ int s8[32]; memcpy(s8, b, sizeof s8); qsort(s8, d, sizeof(int), cmpint); printf("CU FAILS res=%d D3=%ld cU=%ld mu=%ld W=%ld at <%d", R, nv.D3, nv.cU, nv.mu, nv.W, m); for (int q = 0; q < d; q++) printf(",%d", m + s8[q]); printf(">\n"); fflush(stdout); } }
        if (nv.res){ resvisits++; if (nv.a1 < 0){ int s3[32]; memcpy(s3, b, sizeof s3); qsort(s3, d, sizeof(int), cmpint);
            printf("A1 FAILS %ld at <%d", nv.a1, m); for (int q = 0; q < d; q++) printf(",%d", m + s3[q]); printf("> hlo=%ld hhi=%ld D3=%ld PAY2=%ld dc=%ld\n", nv.hlo, nv.hhi, nv.D3, nv.p2, nv.dc); fflush(stdout); }
          if (nv.p2 < 0){ fails++; int s2[32]; memcpy(s2, b, sizeof s2); qsort(s2, d, sizeof(int), cmpint);
            printf("PAY2 FAILS %ld at <%d", nv.p2, m); for (int q = 0; q < d; q++) printf(",%d", m + s2[q]); printf("> h=%ld dc=%ld D3=%ld W=%ld\n", nv.h, nv.dc, nv.D3, nv.W); }
          if (nv.D3 > 0 && (double)(nv.D3 - nv.a1) / nv.D3 > maxrat){ maxrat = (double)(nv.D3 - nv.a1) / nv.D3; memcpy(ratA, b, sizeof ratA); qsort(ratA, d, sizeof(int), cmpint); ratm = m; ratD3 = nv.D3; rathlo = nv.hlo; rathhi = nv.hhi; }
          if (nv.aeT < 0 || nv.desc < 0){ int s4[32]; memcpy(s4, b, sizeof s4); qsort(s4, d, sizeof(int), cmpint);
            printf("%s FAILS aeT=%ld desc=%ld at <%d", nv.desc < 0 ? "DESC" : "A1eT", nv.aeT, nv.desc, m); for (int q = 0; q < d; q++) printf(",%d", m + s4[q]); printf(">\n"); fflush(stdout); }
          if (nv.h > 0 && (double)nv.D3 / nv.h < minDh){ minDh = (double)nv.D3 / nv.h; memcpy(dhA, b, sizeof dhA); qsort(dhA, d, sizeof(int), cmpint); dhm = m; dhD3 = nv.D3; dhh = nv.h; }
          if (nv.D3 < 6 * nv.h){ int s6[32]; memcpy(s6, b, sizeof s6); qsort(s6, d, sizeof(int), cmpint); printf("D6 FAILS D3=%ld h=%ld at <%d", nv.D3, nv.h, m); for (int q = 0; q < d; q++) printf(",%d", m + s6[q]); printf(">\n"); fflush(stdout); }
          if (nv.mu <= e){ if (nv.D3 > 0 && (double)(nv.D3 - nv.mulo) / nv.D3 > maxmr){ maxmr = (double)(nv.D3 - nv.mulo) / nv.D3; memcpy(mrA, b, sizeof mrA); qsort(mrA, d, sizeof(int), cmpint); mrm = m; mrD3 = nv.D3; mrhm = nv.hlomu; mrhh = nv.hhi; }
            if (nv.Qa < minQa){ minQa = nv.Qa; memcpy(qaA, b, sizeof qaA); qsort(qaA, d, sizeof(int), cmpint); qam = m; }
            if (nv.mulo < 0 || nv.Qa < 0){ int s7[32]; memcpy(s7, b, sizeof s7); qsort(s7, d, sizeof(int), cmpint); printf("%s FAILS mulo=%ld Qa=%ld Qb=%ld W=%ld at <%d", nv.mulo < 0 ? "MULO" : "QA", nv.mulo, nv.Qa, nv.Qb, nv.W, m); for (int q = 0; q < d; q++) printf(",%d", m + s7[q]); printf(">\n"); fflush(stdout); } }
          if (nv.W < minW){ minW = nv.W; memcpy(wA, b, sizeof wA); qsort(wA, d, sizeof(int), cmpint); wm = m; }
          if (nv.W < 0){ int s5[32]; memcpy(s5, b, sizeof s5); qsort(s5, d, sizeof(int), cmpint); printf("WILF FAILS W=%ld at <%d", nv.W, m); for (int q = 0; q < d; q++) printf(",%d", m + s5[q]); printf(">\n"); fflush(stdout); }
          if (nv.aeT < minaeT){ minaeT = nv.aeT; memcpy(aeA, b, sizeof aeA); qsort(aeA, d, sizeof(int), cmpint); aem = m; } if (nv.desc < mindesc) mindesc = nv.desc;
          if (nv.a1 < minp){ minp = nv.a1; memcpy(minA, b, sizeof minA); qsort(minA, d, sizeof(int), cmpint); minv = nv; } }
        double dlt = obj(&nv) - obj(&cur);
        if (dlt <= 0 || (Tt > 1e-9 && urand() < exp(-dlt / Tt))){ memcpy(a, b, sizeof a); cur = nv; }
      }
    }
    printf("m=%d d=%d e=%d tries=%ld Q5starts=%ld residual_visits=%ld PAY2fail=%ld", m, d, e, tries, starts, resvisits, fails);
    if (resvisits){ printf(" minA1=%ld at <%d", minp, m); for (int q = 0; q < d; q++) printf(",%d", m + minA[q]); printf("> hlo=%ld hhi=%ld dc=%ld D3=%ld PAY2=%ld W=%ld", minv.hlo, minv.hhi, minv.dc, minv.D3, minv.p2, minv.W);
      if (minp < gmin){ gmin = minp; memcpy(gA, minA, sizeof gA); gm = m; } }
    gfail += fails; printf("\n"); fflush(stdout);
  }
  printf("MAXRATIO d=%d ratio=%.4f D3=%ld hlo=%ld hhi=%ld at <%d", d, maxrat, ratD3, rathlo, rathhi, ratm); for (int q = 0; q < d; q++) printf(",%d", ratm + ratA[q]); printf(">\n");
  printf("MINDH d=%d min D3/h=%.4f (D3=%ld h=%ld) at <%d", d, minDh, dhD3, dhh, dhm); for (int q = 0; q < d; q++) printf(",%d", dhm + dhA[q]); printf(">\n");
  printf("MINW d=%d minW(residual)=%ld at <%d", d, minW, wm); for (int q = 0; q < d; q++) printf(",%d", wm + wA[q]); printf(">\n");
  printf("MINAET d=%d minA1eT=%ld minDESC=%ld at <%d", d, minaeT, mindesc, aem); for (int q = 0; q < d; q++) printf(",%d", aem + aeA[q]); printf(">\n");
  printf("MAXMULO d=%d ratio=%.4f D3=%ld hlo_mu=%ld hhi=%ld at <%d", d, maxmr, mrD3, mrhm, mrhh, mrm); for (int q = 0; q < d; q++) printf(",%d", mrm + mrA[q]); printf(">\n");
  printf("MINQA d=%d minQa=%ld at <%d", d, minQa, qam); for (int q = 0; q < d; q++) printf(",%d", qam + qaA[q]); printf(">\n");
  for (int R = 0; R < 2; R++){ printf("MAXZW %s d=%d ratio=%.4f D3=%ld z=%ld cU=%ld at <%d", R ? "residual" : "U=T", d, maxzw[R], zwD3[R], zwz[R], zwcU[R], zwm[R]); for (int q = 0; q < d; q++) printf(",%d", zwm[R] + zwA[R][q]); printf(">\n"); }
  for (int R = 0; R < 2; R++){ printf("MAXCU %s d=%d ratio=%.4f D3=%ld cU=%ld mu=%ld at <%d", R ? "residual" : "U=T", d, maxcu[R], cuD3[R], cucU[R], cumu[R], cum[R]); for (int q = 0; q < d; q++) printf(",%d", cum[R] + cuA[R][q]); printf(">\n"); }
  printf("GLOBAL d=%d PAY2fail=%ld minA1=%ld at <%d", d, gfail, gmin, gm); for (int q = 0; q < d; q++) printf(",%d", gm + gA[q]); printf(">\n");
  return 0;
}
