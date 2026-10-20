/* ID-q and ANCHOR for EVERY numerical semigroup (lead, 2026-10-20). For each S of genus <= G (tree), with c > m:
 *   q = ceil(c/m), rho = q m - c, generators g_1..g_K = left primitives other than m, offsets b_i = g_i - m (any size);
 *   positions u = (v + rho) mod m, level floor((v + rho)/m); canonical reps by (level, degree, lex code);
 *   adding g_i to position x: kappa = floor((x + b_i)/m) crossings, level + 1 + kappa.
 *   c_y = sum_i kappa_i(y) beta_y(i) (kappa of the parent edge), j_y = lambda_y - t_y.
 *   Asserts ID-q: W0 = (K+1) ell - q d + rho = rho + POOL + sum (c_y - j_y), with d = #{lambda <= q}, p = m - d
 *   (= number of right primitives). Reports T1 = rho + EXC + p - DEF (variant anchgen_t1) and CORE1 = W0 + p, per depth.
 * gcc -O3 -o anchgen anchgen.c ; ./anchgen G */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128; typedef long long ll;
#define MM 128
#define KM 64
static int G; static ll nS, nM, mis, failA[64], failC[64], cnt[64], minA[64], minC[64]; static int exA[64][KM + 3], exC[64][KM + 3];
static inline int inS(u128 g, int F, int x) { return x >= 0 && (x > F || !((g >> x) & 1)); }
static int M, RHO, K, Q, B[KM], lam[MM], deg[MM], al[MM][KM], fin[MM];
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
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  nS++;
  int c = F + 1;
  if (c > m && m < MM) {
    M = m; Q = (c + m - 1) / m; RHO = Q * m - c; K = 0;
    for (int i = 0; i < e; i++) if (gens[i] != m && gens[i] < c) B[K++] = gens[i] - m;
    /* sort B */
    for (int i = 0; i < K; i++) for (int j = i + 1; j < K; j++) if (B[j] < B[i]) { int t = B[i]; B[i] = B[j]; B[j] = t; }
    canon();
    ll ell = 0, d = 0, POOL = 0, Utop = 0, EXC = 0, DEF = 0;
    for (int x = 0; x < M; x++) {
      if (lam[x] > Q) continue;
      d++; if (lam[x] < Q) ell += Q - lam[x];
      int jx = lam[x] - deg[x];
      for (int i = 0; i < K; i++) {
        int w = al[x][i] + 1, v = x + B[i], kap = v / M, y = v % M, used = 0;
        if (lam[y] <= Q && lam[y] == lam[x] + 1 + kap) { int ok = 1; for (int k = 0; k < K; k++) if (al[y][k] != al[x][k] + (k == i)) { ok = 0; break; } used = ok; }
        if (!used) { POOL += (ll)(Q - lam[x]) * w; if (lam[x] == Q - 1) Utop += w; }
      }
      int cy = 0;
      for (int i = 0; i < K; i++) if (al[x][i] > 0) { int px = ((x - B[i]) % M + M) % M; cy += ((px + B[i]) / M) * al[x][i]; }
      if (cy > jx) EXC += cy - jx; else DEF += jx - cy;
    }
    ll p = M - d, W0 = (ll)(K + 1) * ell - (ll)Q * d + RHO;
    /* cross-check p against the right primitives of S */
    int rp = 0; for (int i = 0; i < e; i++) if (gens[i] >= c) rp++;
    if (W0 != RHO + POOL + EXC - DEF || p != rp) { mis++; if (mis < 5) fprintf(stderr, "MISMATCH m=%d c=%d W0=%lld rhs=%lld p=%lld rp=%d\n", m, c, W0, RHO + POOL + EXC - DEF, p, rp); }
    nM++;
    int qq = Q < 63 ? Q : 63; cnt[qq]++;
    ll A = RHO + EXC + p - DEF, C1 = W0 + p; (void)Utop;
    if (A < 0) failA[qq]++;
    if (C1 < 0) failC[qq]++;
    if (cnt[qq] == 1 || A < minA[qq]) { minA[qq] = A; exA[qq][0] = m; exA[qq][1] = c; exA[qq][2] = e; for (int i = 0; i < e && i < KM; i++) exA[qq][3 + i] = gens[i]; }
    if (cnt[qq] == 1 || C1 < minC[qq]) { minC[qq] = C1; exC[qq][0] = m; exC[qq][1] = c; exC[qq][2] = e; for (int i = 0; i < e && i < KM; i++) exC[qq][3 + i] = gens[i]; }
  }
  if (g == G) return;
  int ng[128];
  for (int jj = 0; jj < e; jj++) {
    int nn = gens[jj]; if (nn <= F) continue;
    u128 gm2 = gm | ((u128)1 << nn);
    int e2 = 0, m2;
    if (nn == m) { m2 = m + 1; for (int kk = m2; kk <= 2 * m2 - 1; kk++) ng[e2++] = kk; }
    else {
      m2 = m;
      for (int kk = 0; kk < e; kk++) if (gens[kk] != nn) ng[e2++] = gens[kk];
      int y = nn + m, dec = 0;
      for (int a = m; a <= y / 2 && !dec; a++) if (a != nn && inS(gm2, nn, a) && (y - a) != nn && inS(gm2, nn, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, nn, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); if (G > 60) return 1;
  int gens[1] = {1};
  visit(0, -1, 1, gens, 1, 0);
  printf("genus <= %d: %lld S, %lld with c > m; ID-q/p mismatches %lld\n", G, nS, nM, mis);
  for (int q = 2; q < 64; q++) if (cnt[q]) {
    printf("q=%d: %lld S; T1 fails %lld (min %lld at m=%d c=%d gens=", q, cnt[q], failA[q], minA[q], exA[q][0], exA[q][1]);
    for (int i = 0; i < exA[q][2]; i++) printf("%d,", exA[q][3 + i]);
    printf("); CORE1 fails %lld (min %lld at m=%d c=%d gens=", failC[q], minC[q], exC[q][0], exC[q][1]);
    for (int i = 0; i < exC[q][2]; i++) printf("%d,", exC[q][3 + i]);
    printf(")\n");
  }
  return 0;
}
