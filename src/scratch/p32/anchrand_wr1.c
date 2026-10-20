/* ANCHOR and ID-q on RANDOM numerical semigroups with generators at several levels (lead, 2026-10-20).
 * S = <m, g_1..g_k>, g_i random in (m, LMAX*m); Apery set by Dijkstra; c = max Ap - m + 1; minimal generators =
 * Apery elements not a sum of two nonzero Apery elements (plus m); left primitives (< c) give the offsets b = g - m.
 * Same canonical-rep computation as anchgen.c. Asserts ID-q and p = #right primitives.
 * gcc -O3 -o anchrand anchrand.c ; ./anchrand MLO MHI KMIN KMAX LMAX NS SEED
 *   small-e exhaustive: ./anchrand E3 MLO MHI GMAXMULT   (all <m, a, b>, m < a < b < GMAXMULT*m, gcd 1)
 *                        ./anchrand E4 MLO MHI GMAXMULT NS SEED (random <m, a, b, c>)
 *   explicit:           ./anchrand S g1 g2 ... */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
#define MM 256
#define KM 64
static int M, RHO, K, Q, B[KM], lam[MM], deg[MM], al[MM][KM], fin[MM];
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long xr(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int better(int l, int t, const int *a, int u) {
  if (l != lam[u]) return l < lam[u]; if (t != deg[u]) return t < deg[u];
  for (int k = K - 1; k >= 0; k--) if (a[k] != al[u][k]) return a[k] < al[u][k];
  return 0;
}
static void canon(void) {
  for (int u = 0; u < M; u++) { lam[u] = 1 << 28; deg[u] = 0; fin[u] = 0; memset(al[u], 0, sizeof(int) * KM); }
  lam[RHO] = 0;
  for (;;) {
    int u = -1;
    for (int x = 0; x < M; x++) if (!fin[x] && lam[x] < (1 << 28)) { if (u < 0 || better(lam[x], deg[x], al[x], u)) u = x; }
    if (u < 0) break;
    fin[u] = 1;
    if (lam[u] > Q) continue;
    for (int i = 0; i < K; i++) {
      int v = u + B[i], kap = v / M, u2 = v % M;
      if (fin[u2]) continue;
      int l2 = lam[u] + 1 + kap, t2 = deg[u] + 1; int a2[KM]; memcpy(a2, al[u], sizeof(int) * KM); a2[i]++;
      if (better(l2, t2, a2, u2)) { lam[u2] = l2; deg[u2] = t2; memcpy(al[u2], a2, sizeof(int) * KM); }
    }
  }
}
static ll n = 0, mis = 0, failA = 0, failC = 0, cnt[64], minA[64], minC[64];
static void eval_gens(int m, int k, int *g) {
    /* Apery set */
    static ll w[MM]; for (int r = 0; r < m; r++) w[r] = 1LL << 60; w[0] = 0;
    static int done[MM]; memset(done, 0, sizeof(done));
    for (;;) {
      int r = -1; for (int x = 0; x < m; x++) if (!done[x] && w[x] < (1LL << 60) && (r < 0 || w[x] < w[r])) r = x;
      if (r < 0) break; done[r] = 1;
      for (int i = 0; i < k; i++) { ll v = w[r] + g[i]; int s = v % m; if (v < w[s]) w[s] = v; }
    }
    int ok = 1; for (int r = 0; r < m; r++) if (w[r] >= (1LL << 60)) ok = 0;
    if (!ok) return; /* gcd > 1 */
    ll mx = 0; for (int r = 0; r < m; r++) if (w[r] > mx) mx = w[r];
    ll c = mx - m + 1; if (c <= m) return;
    /* minimal generators among Apery elements */
    int gens[MM], e = 0;
    for (int r = 1; r < m; r++) {
      int dec = 0;
      for (int a = 1; a < m && !dec; a++) { int b2 = (r - a + m) % m; if (b2 == 0) continue; if (w[a] + w[b2] == w[r]) dec = 1; }
      if (!dec) gens[e++] = (int)w[r];
    }
    if (e > KM) return;
    M = m; Q = (int)((c + m - 1) / m); RHO = (int)(Q * m - c); K = 0;
    int rp = 0; for (int i = 0; i < e; i++) { if (gens[i] < c) B[K++] = gens[i] - m; else rp++; }
    for (int i = 0; i < K; i++) for (int j = i + 1; j < K; j++) if (B[j] < B[i]) { int t = B[i]; B[i] = B[j]; B[j] = t; }
    canon();
    ll ell = 0, d = 0, POOL = 0, Utop = 0, EXC = 0, DEF = 0;
    for (int x = 0; x < M; x++) {
      if (lam[x] > Q) continue;
      d++; if (lam[x] < Q) ell += Q - lam[x];
      int jx = lam[x] - deg[x];
      for (int i = 0; i < K; i++) {
        int wt = al[x][i] + 1, v = x + B[i], kap = v / M, y = v % M, used = 0;
        if (lam[y] <= Q && lam[y] == lam[x] + 1 + kap) { int okk = 1; for (int kk = 0; kk < K; kk++) if (al[y][kk] != al[x][kk] + (kk == i)) { okk = 0; break; } used = okk; }
        if (!used) { POOL += (ll)(Q - lam[x]) * wt; if (jx > 0) Utop += (ll)(Q - lam[x]) * wt; }
      }
      int cy = 0;
      for (int i = 0; i < K; i++) if (al[x][i] > 0) { int px = ((x - B[i]) % M + M) % M; cy += ((px + B[i]) / M) * al[x][i]; }
      if (cy > jx) EXC += cy - jx; else DEF += jx - cy;
    }
    ll p = M - d, W0 = (ll)(K + 1) * ell - (ll)Q * d + RHO;
    if (W0 != RHO + POOL + EXC - DEF || p != rp) { mis++; if (mis < 5) fprintf(stderr, "MISMATCH m=%d c=%lld\n", m, c); }
    n++; int qq = Q < 63 ? Q : 63; cnt[qq]++;
    ll A = RHO + EXC + Utop + p - DEF, C1 = W0 + p;
    if (A < minA[qq]) minA[qq] = A; if (C1 < minC[qq]) minC[qq] = C1;
    if (A < 0) { failA++; if (failA <= 5) { printf("WR1 FAIL m=%d c=%lld gens=", m, c); for (int i = 0; i < e; i++) printf("%d,", gens[i]); printf(" DEF=%lld EXC=%lld Utop=%lld p=%lld rho=%d W0=%lld POOL=%lld\n", DEF, EXC, Utop, p, RHO, W0, POOL); fflush(stdout); } }
    if (C1 < 0) { failC++; if (failC <= 5) { printf("CORE1 FAIL m=%d c=%lld gens=", m, c); for (int i = 0; i < e; i++) printf("%d,", gens[i]); printf(" W0=%lld p=%lld\n", W0, p); fflush(stdout); } }
  
}
int main(int argc, char **argv) {
  for (int i = 0; i < 64; i++) { minA[i] = minC[i] = 1LL << 60; cnt[i] = 0; }
  if (!strcmp(argv[1], "S")) {
    int g[KM], k = 0, m = atoi(argv[2]);
    for (int i = 3; i < argc; i++) g[k++] = atoi(argv[i]);
    eval_gens(m, k, g);
  } else if (!strcmp(argv[1], "E3")) {
    int MLO = atoi(argv[2]), MHI = atoi(argv[3]), GM = atoi(argv[4]);
    for (int m = MLO; m <= MHI; m++) for (int a = m + 1; a < GM * m; a++) for (int b = a + 1; b < GM * m; b++) {
      int g[2] = {a, b}; eval_gens(m, 2, g);
    }
  } else if (!strcmp(argv[1], "E4")) {
    int MLO = atoi(argv[2]), MHI = atoi(argv[3]), GM = atoi(argv[4]); ll NS = atoll(argv[5]); rs ^= (unsigned long long)atoll(argv[6]) * 2654435761ULL;
    for (ll it = 0; it < NS; it++) {
      int m = MLO + xr() % (MHI - MLO + 1); int g[3];
      for (int i = 0; i < 3; i++) g[i] = m + 1 + xr() % ((GM - 1) * m - 1);
      eval_gens(m, 3, g);
    }
  } else {
    int MLO = atoi(argv[1]), MHI = atoi(argv[2]), KMIN = atoi(argv[3]), KMAX = atoi(argv[4]), LMAX = atoi(argv[5]);
    ll NS = atoll(argv[6]); rs ^= (unsigned long long)atoll(argv[7]) * 2654435761ULL;
    for (ll it = 0; it < NS; it++) {
      int m = MLO + xr() % (MHI - MLO + 1), k = KMIN + xr() % (KMAX - KMIN + 1);
      int g[KM]; for (int i = 0; i < k; i++) g[i] = m + 1 + xr() % ((LMAX - 1) * m - 1);
      eval_gens(m, k, g);
    }
  }
  printf("random S: %lld (with c > m), ID-q/p mismatches %lld, WR1 fails %lld, CORE1 fails %lld\n", n, mis, failA, failC);
  for (int q = 2; q < 64; q++) if (cnt[q]) printf("  q=%d: %lld S, min WR1 slack %lld, min CORE1 %lld\n", q, cnt[q], minA[q], minC[q]);
  return 0;
}
