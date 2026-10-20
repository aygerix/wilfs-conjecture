/* Exhaustive test of ANCHOR-q and ID-q (lead, 2026-10-20). For every m in [MLO,MHI], rho in [0,m-2], every
 * B subset of [1,HI) (HI = m - rho strip-free, or m with STRIP=1) with KMIN <= |B| <= KMAX, depth q:
 *   canonical reps by Dijkstra on (level, degree, code), code base q+3;
 *   W0 = (K+1) ell - q d + rho must equal rho + POOL + EXC - DEF (ID-q, asserted);
 *   ANCHOR-q slack = rho + EXC + Utop + p - DEF; only models of TRUE depth (lambda(m-1) >= q) are counted.
 * gcc -O3 -o anchqx anchqx.c ; ./anchqx q MLO MHI KMIN KMAX STRIP
 *   random mode: ./anchqx q MLO MHI KMIN KMAX STRIP NSAMPLES SEED  (B drawn from a random sub-interval of [1,HI))
 *   single model: ./anchqx q m rho b1,b2,... (prints the parts) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
static int q, M, RHO, K, B[64];
static int lam[512], deg[512], al[512][64], fin[512]; static ll code[512];
static ll powb[64];
/* order: level, degree, then the code sum a_i (q+3)^i, i.e. lexicographic on (a_{K-1}, ..., a_0) (digits < q+3) */
static int better(int l, int t, const int *a, int u) {
  if (l != lam[u]) return l < lam[u]; if (t != deg[u]) return t < deg[u];
  for (int k = K - 1; k >= 0; k--) if (a[k] != al[u][k]) return a[k] < al[u][k];
  return 0;
}
static void canon(void) {
  for (int u = 0; u < M; u++) { lam[u] = 1 << 28; deg[u] = 0; code[u] = 0; fin[u] = 0; memset(al[u], 0, sizeof(int) * 64); }
  lam[RHO] = 0;
  for (;;) {
    int u = -1;
    for (int x = 0; x < M; x++) if (!fin[x] && lam[x] < (1 << 28)) { if (u < 0 || better(lam[x], deg[x], al[x], u)) u = x; }
    if (u < 0) break;
    fin[u] = 1;
    if (lam[u] > q) continue;
    for (int i = 0; i < K; i++) {
      int v = u + B[i], cr = v >= M, u2 = v % M;
      if (fin[u2]) continue;
      int l2 = lam[u] + 1 + cr, t2 = deg[u] + 1; int a2[64]; memcpy(a2, al[u], sizeof(int) * 64); a2[i]++;
      if (better(l2, t2, a2, u2)) { lam[u2] = l2; deg[u2] = t2; memcpy(al[u2], a2, sizeof(int) * 64); }
    }
  }
}
static ll nmod, nfail, nmis; static ll minsl = 1LL << 60; static double minratio = 1e18; static int ex[64], exK, exm, exr; static ll exr_def, exr_sl;
static int rex[64], rexK, rexm, rexr; static ll rdef, rsl;
static void eval(void) {
  canon();
  if (lam[M - 1] < q) return; /* not true depth */
  ll ell = 0, d = 0, POOL = 0, Utop = 0, EXC = 0, DEF = 0;
  for (int x = 0; x < M; x++) {
    if (lam[x] > q) continue;
    d++; if (lam[x] < q) ell += q - lam[x];
    int jx = lam[x] - deg[x];
    for (int i = 0; i < K; i++) {
      int w = al[x][i] + 1, v = x + B[i], cr = v >= M, y = v % M, used = 0;
      if (lam[y] <= q && lam[y] == lam[x] + 1 + cr) {
        int ok = 1;
        for (int k = 0; k < K; k++) if (al[y][k] != al[x][k] + (k == i)) { ok = 0; break; }
        used = ok;
      }
      if (!used) { POOL += (ll)(q - lam[x]) * w; if (lam[x] == q - 1) Utop += w; }
    }
    int cy = 0; for (int i = 0; i < K; i++) if (al[x][i] > 0 && B[i] > x) cy += al[x][i];
    if (cy > jx) EXC += cy - jx; else DEF += jx - cy;
  }
  ll p = M - d, W0 = (ll)(K + 1) * ell - (ll)q * d + RHO;
  if (W0 != RHO + POOL + EXC - DEF) { nmis++; if (nmis < 4) fprintf(stderr, "ID-q MISMATCH m=%d rho=%d\n", M, RHO); }
  nmod++;
  ll sl = RHO + EXC + Utop + p - DEF;
  if (sl < 0) { nfail++; if (nfail <= 10) { printf("FAIL m=%d rho=%d B=", M, RHO); for (int i = 0; i < K; i++) printf("%d,", B[i]); printf(" W0=%lld POOL=%lld Utop=%lld EXC=%lld DEF=%lld p=%lld slack=%lld\n", W0, POOL, Utop, EXC, DEF, p, sl); fflush(stdout); } }
  if (sl < minsl) { minsl = sl; exK = K; exm = M; exr = RHO; exr_def = DEF; exr_sl = sl; memcpy(ex, B, sizeof(int) * K); }
  if (DEF >= 4) { double r = (double)sl / DEF; if (r < minratio) { minratio = r; rexK = K; rexm = M; rexr = RHO; rdef = DEF; rsl = sl; memcpy(rex, B, sizeof(int) * K); } }
}
static int HI, KMIN, KMAX;
static void rec(int start, int k) {
  if (k >= KMIN) { K = k; eval(); }
  if (k == KMAX) return;
  for (int b = start; b < HI; b++) { B[k] = b; rec(b + 1, k + 1); }
}
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long xr(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int cmpi(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }
int main(int argc, char **argv) {
  q = atoi(argv[1]);
  powb[0] = 1; for (int i = 1; i < 64; i++) powb[i] = powb[i - 1] * (q + 3);
  if (argc == 5) { /* single model */
    M = atoi(argv[2]); RHO = atoi(argv[3]); K = 0; char *s = argv[4];
    while (*s) { B[K++] = atoi(s); while (*s && *s != ',') s++; if (*s == ',') s++; }
    eval(); printf("models %lld failures %lld minslack %lld DEF %lld\n", nmod, nfail, minsl, exr_def); return 0;
  }
  int MLO = atoi(argv[2]), MHI = atoi(argv[3]); KMIN = atoi(argv[4]); KMAX = atoi(argv[5]); int STRIP = atoi(argv[6]);
  if (argc > 8) {
    long long NS = atoll(argv[7]); rs ^= (unsigned long long)atoll(argv[8]) * 2654435761ULL;
    for (long long it = 0; it < NS; it++) {
      M = MLO + xr() % (MHI - MLO + 1); RHO = xr() % (M - 1); HI = STRIP ? M : M - RHO;
      if (HI < 4) continue;
      int lo = 1 + xr() % (HI - 2), hi2 = lo + 1 + xr() % (HI - lo);
      if (hi2 > HI) hi2 = HI;
      int span = hi2 - lo; if (span < 2) continue;
      int k = KMIN + xr() % (KMAX - KMIN + 1); if (k > span) k = span;
      int n = 0, tries = 0;
      while (n < k && tries < 10000) { tries++; int b = lo + xr() % span, dup = 0; for (int i = 0; i < n; i++) if (B[i] == b) dup = 1; if (!dup) B[n++] = b; }
      qsort(B, n, sizeof(int), cmpi); K = n; if (K < 1) continue;
      eval();
    }
  } else
  for (M = MLO; M <= MHI; M++) for (RHO = 0; RHO <= M - 2; RHO++) { HI = STRIP ? M : M - RHO; rec(1, 0); }
  printf("q=%d m=%d..%d K=%d..%d strip=%d: true-depth models %lld, ID-q mismatches %lld, ANCHOR-q failures %lld\n", q, MLO, MHI, KMIN, KMAX, STRIP, nmod, nmis, nfail);
  printf("min slack %lld at m=%d rho=%d B=", minsl, exm, exr); for (int i = 0; i < exK; i++) printf("%d,", ex[i]); printf(" (DEF=%lld)\n", exr_def);
  printf("min slack/DEF (DEF>=4) %.4f at m=%d rho=%d B=", minratio, rexm, rexr); for (int i = 0; i < rexK; i++) printf("%d,", rex[i]); printf(" DEF=%lld slack=%lld\n", rdef, rsl);
  return 0;
}
