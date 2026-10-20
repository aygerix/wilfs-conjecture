/* Depth four (3m < c <= 4m), general S.  Window decomposition and the shift lemma (lead, 2026-10-20).
 * Positions: residue r of v; high window Hw = residues [h, 2h) mod m (size h).  W = Lam + Z + Nlo - RAhi (exact):
 *   Nlo = #{K <= 0, r not in Hw}, RAhi = #{K = 1, r in Hw} (short critical pure-A cubics).
 * c0 = least (n - m) over A-class factors n of short critical cubics.
 * SHIFT (proved on paper when c0 > h/2): with src = residues [2c0, 2h - c0),
 *   RAhi <= #{x in src : K(v_x) <= -1} + #{x in src : v_x + n_c0 not in Ap, lam(v_x) >= 1} + #{x in src : lam(v_x) = 0, K(v_x) >= 0}
 * Also tests: WIN  RAhi <= Lam + Z;  and records how often c0 <= h/2.
 * Sources: ./shift4 G  (all S of genus <= G);  ./shift4 P m k R seed (random P18 <m, m+B>, |B| = k) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, withR, c0low, failShift, failWin, badId;
static long long maxWinEx = -(1LL<<60), maxShiftEx = -(1LL<<60);
static uint64_t c0pos, c0posNlo; static long long maxMinC0 = -1;
static uint64_t noLopt, noLoptS, matchFail; static long long maxNoL = 0;
static uint64_t fV1, fV2; static long long maxV1 = -(1LL<<60), maxV2 = -(1LL<<60);
static uint64_t fWF, fCR, withC0, fWF2, fCNT, noTrans; static long long maxCNT = -(1LL<<60);
static long long minWF = 1LL<<60, maxCR = -(1LL<<60), minWF2 = 1LL<<60;
/* bipartite matching: cubes without a Lambda-option -> Z-sources (capacity -K) */
static int madj[4096][64], mdeg[4096], cap[4096], used[4096], owner[4096][8], nown[4096], seen_[4096];
static int aug(int y){ for (int j = 0; j < mdeg[y]; j++){ int x = madj[y][j]; if (seen_[x]) continue; seen_[x] = 1;
  if (nown[x] < cap[x]){ owner[x][nown[x]++] = y; return 1; }
  for (int u = 0; u < nown[x]; u++) if (aug(owner[x][u])){ owner[x][u] = y; return 1; } } return 0; }
static void check(int m, long long *w, long long *n, int d, int c) {
  int q = (c + m - 1) / m; if (q != 4) return;
  tot++;
  #define INAP(v) ((v) >= 0 && w[(v) % m] == (v))
  #define INS(v) ((v) >= 0 && w[(v) % m] <= (v))
  long long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  long long h = c - 3LL * m; int e = d + 1;
  static long long K[4096], lam[4096]; static int top[4096][64];
  long long Lam = 0, Z = 0, Nlo = 0, RAhi = 0, g = 0, tauB = 0, sumU = 0, a0 = 0;
  int c0 = 1 << 30;
  for (int i = 0; i < m; i++) { long long x = w[i]; lam[i] = (M - x) / m; K[i] = 4 - lam[i]; g += x / m;
    for (int a = 0; a < d; a++) { int j = 0; while (INS(x - (long long)(j + 1) * n[a])) j++;
      if (j) K[i] -= j * ((M - (x - n[a])) / m - lam[i]);
      top[i][a] = !INAP(x + n[a]); if (top[i][a]) Lam += (j + 1) * lam[i];
      if (top[i][a] && x < c) tauB++; }
    { int U = 0; for (int a = 0; a < d; a++) if (INS(x - n[a])) U++; long long cp = 4 - lam[i]; sumU += U < cp ? U : cp; if (lam[i] == 0) a0++; }
    int inw = ((i - h) % m + m) % m < h;  /* r in [h, 2h) mod m */
    if (K[i] < 0) Z -= K[i];
    if (K[i] <= 0 && !inw) Nlo++;
    if (K[i] == 1 && inw) { RAhi++;
      for (int a = 0; a < d; a++) if (INS(x - n[a]) && n[a] < m + h) { int t = (int)(n[a] - m); if (t < c0) c0 = t; } }
  }
  long long W = (long long)e * (c - g) - c;
  if (W != Lam + Z + Nlo - RAhi) badId++;
  { /* window-filling form: W1 = residues [h, h+ceil(h/2)) mod m, W2 = rest of Hw */
    long long hh = (h + 1) / 2; long long best = 1LL << 60, best2 = 1LL << 60;
    static int inW1[4096], inHw[4096], isgen[4096];
    for (int i = 0; i < m; i++){ inW1[i] = ((i - h) % m + m) % m < hh; inHw[i] = ((i - h) % m + m) % m < h; isgen[i] = 0; }
    for (int a = 0; a < d; a++) isgen[n[a] % m] = 1;
    long long Zc1 = 0, C0 = 0, C0E = 0, NW2 = 0, genOut = 0;
    for (int i = 0; i < m; i++){ if (inW1[i]){ if (K[i] <= -1) Zc1++; else if (K[i] == 0 && lam[i] == 0){ C0++; if (isgen[i]) C0E++; } }
      else if (inHw[i] && K[i] <= 0) NW2++;
      if (!inHw[i] && K[i] <= 0 && (i == 0 || isgen[i])) genOut++; }
    if (C0 > 0) withC0++;
    for (int a = 0; a < d; a++){ long long tau = n[a] % m; long long dt = tau < m - tau ? tau : m - tau; if (2 * dt < h) continue;
      long long IL = 0, I2 = 0, Il = 0;
      for (int i = 0; i < m; i++){ if (!inW1[i] || K[i] != 0 || lam[i] == 0) continue;
        if (top[i][a]) { IL++; continue; } int j = (int)((i + tau) % m); if (inHw[j]) { if (inW1[j]) { printf("WF LOGIC m=%d\n", m); exit(1); } I2++; } else Il++; }
      long long slack = (Lam - IL) + (Z - Zc1) + (Nlo - Il) + (NW2 - I2) + (hh - (h - hh)) - C0;
      if (slack < best) best = slack;
      long long slack2 = (Z - Zc1) + (Nlo - Il) + (NW2 - I2) + (hh - (h - hh)) - C0; if (slack2 < best2) best2 = slack2; }
    { /* CNT: C0(W1) <= #{v not in W1, K<=0, no predecessor in W1} + (Z - Zc1) + delta */
      long long np = 0;
      for (int i = 0; i < m; i++){ if (inW1[i] || K[i] > 0) continue; long long x = w[i]; int hasP = 0;
        for (int a = 0; a < d && !hasP; a++) if (INS(x - n[a])){ int j = (int)(((x - n[a]) % m)); if (inW1[j] && w[j] == x - n[a]) hasP = 1; }
        if (!hasP) np++; }
      long long cnt = C0 - np - (Z - Zc1) - (hh - (h - hh)); if (cnt > 0) fCNT++; if (cnt > maxCNT){ maxCNT = cnt; printf("CNTrec %lld C0=%lld np=%lld Zx=%lld W=%lld m=%d c=%d h=%lld gens=", cnt, C0, np, Z - Zc1, W, m, c, h); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf("\n"); fflush(stdout); } }
    if (best2 >= (1LL << 59)) noTrans++;
    if (best2 < (1LL << 59)){ if (best2 < 0){ fWF2++; static int pr2 = 0; if (pr2++ < 6){ printf("WF2neg %lld W=%lld Lam=%lld m=%d c=%d h=%lld C0=%lld gens=", best2, W, Lam, m, c, h, C0); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf("\n"); } } if (best2 < minWF2) minWF2 = best2; }
    if (best < (1LL << 59)){ if (best < 0) fWF++; if (best < minWF) minWF = best; }
    long long cr = (C0 - C0E) - genOut; if (cr > 0) fCR++; if (cr > maxCR){ maxCR = cr; printf("CRrec C0-E - (1+gensOut) = %lld C0=%lld C0E=%lld genOut=%lld W=%lld m=%d c=%d h=%lld gens=", cr, C0, C0E, genOut, W, m, c, h); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf("\n"); fflush(stdout); }
  }
  if (RAhi == 0) return;
  withR++;
  { long long L2 = (long long)d * (m - a0) - sumU; long long v1 = RAhi - L2, v2 = RAhi - tauB - Z;
    if (v1 > 0) fV1++; if (v2 > 0) fV2++;
    if (v1 >= 0 && fV1 + 1 > 0){ static int pr = 0; if (pr++ < 12){ printf("V1tight v1=%lld W=%lld m=%d c=%d h=%lld e=%d RAhi=%lld L2=%lld Lam=%lld Z=%lld gens=", v1, W, m, c, h, e, RAhi, L2, Lam, Z); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf("\n"); } } if (v1 > maxV1) maxV1 = v1; if (v2 > maxV2) maxV2 = v2; }
  long long wex = RAhi - Lam - Z; if (wex > 0) failWin++; if (wex > maxWinEx) { maxWinEx = wex;
    printf("WINrec ex=%lld W=%lld m=%d c=%d h=%lld e=%d Lam=%lld Z=%lld Nlo=%lld RAhi=%lld c0=%d gens=", wex, W, m, c, h, e, Lam, Z, Nlo, RAhi, c0); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf("\n"); fflush(stdout); }
  { long long best = 1LL << 60; int bt = -1;
    for (int a = 0; a < d; a++) { long long cz = 0;
      for (int y = 0; y < m; y++) { int inw = ((y - h) % m + m) % m < h; if (!(inw && K[y] == 1)) continue;
        int x = (int)(((y - n[a]) % m + m) % m);
        if (K[x] <= -1) continue; if (lam[x] >= 1 && top[x][a]) continue;
        if (lam[x] >= 1) { printf("LOGIC FAIL m=%d\n", m); exit(1); }
        cz++; }
      if (cz < best) { best = cz; bt = a; } }
    if (best > 0) { c0pos++; if (best > Nlo) c0posNlo++; }
    if (best > maxMinC0) { maxMinC0 = best; printf("minC0rec %lld (Nlo=%lld W=%lld) m=%d c=%d h=%lld RAhi=%lld gens=", best, Nlo, W, m, c, h, RAhi); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf("\n"); fflush(stdout); } }
  { int ny = 0; static int ylist[4096];
    for (int x = 0; x < m; x++){ cap[x] = K[x] < 0 ? (int)(-K[x] < 8 ? -K[x] : 8) : 0; nown[x] = 0; }
    for (int y = 0; y < m; y++){ int inw = ((y - h) % m + m) % m < h; if (!(inw && K[y] == 1)) continue;
      int hasL = 0; mdeg[y] = 0;
      for (int a = 0; a < d; a++){ int x = (int)(((y - n[a]) % m + m) % m);
        if (lam[x] >= 1 && top[x][a]) hasL = 1;
        if (K[x] <= -1){ int dup = 0; for (int j = 0; j < mdeg[y]; j++) if (madj[y][j] == x) dup = 1; if (!dup) madj[y][mdeg[y]++] = x; } }
      if (!hasL) ylist[ny++] = y; }
    if (ny){ noLoptS++; noLopt += ny; if (ny > maxNoL){ maxNoL = ny; printf("noLrec %d of RAhi=%lld m=%d c=%d h=%lld gens=", ny, RAhi, m, c, h); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf("\n"); fflush(stdout);} }
    int matched = 0; for (int i = 0; i < ny; i++){ for (int x = 0; x < m; x++) seen_[x] = 0; if (aug(ylist[i])) matched++; }
    if (matched < ny){ matchFail++; printf("MATCHFAIL %d/%d m=%d c=%d h=%lld W=%lld gens=", matched, ny, m, c, h, W); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf("\n"); fflush(stdout); } }
  if (2 * c0 <= h) { c0low++; return; }
  int ac = -1; for (int a = 0; a < d; a++) if (n[a] == m + c0) ac = a;
  long long cred = 0;
  for (long long r = 2 * c0; r < 2 * h - c0; r++) { int i = (int)(r % m);
    if (K[i] <= -1) cred++; else if (lam[i] >= 1 && top[i][ac]) cred++; else if (lam[i] == 0) cred++; }
  long long sex = RAhi - cred; if (sex > 0) { failShift++; printf("SHIFTFAIL m=%d c=%d\n", m, c); }
  if (sex > maxShiftEx) maxShiftEx = sex;
}
static inline int gapq(u128 gm, int z) { return z < 128 && ((gm >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  if (F >= 1 && m >= 2 && e >= 3) {
    long long w[128]; for (int i = 0; i < m; i++) { int s = i; while (gapq(gm, s)) s += m; w[i] = s; }
    long long n[64]; int d = 0; for (int j = 0; j < e; j++) if (gens[j] != m) n[d++] = gens[j];
    check(m, w, n, d, F + 1);
  }
  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int nn = gens[j]; if (nn <= F) continue;
    u128 gm2 = gm | ((u128)1 << nn); int e2 = 0, m2;
    if (nn == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else { m2 = m; for (int k = 0; k < e; k++) if (gens[k] != nn) ng[e2++] = gens[k];
      int y = nn + m, dec = 0; for (int a = m; a <= y / 2 && !dec; a++) if (a != nn && !gapq(gm2, a) && (y - a) != nn && !gapq(gm2, y - a)) dec = 1;
      if (!dec) ng[e2++] = y; }
    visit(gm2, nn, m2, ng, e2, g + 1);
  }
}
static int gcd(int a, int b){ while(b){int t=a%b;a=b;b=t;} return a; }
int main(int argc, char **argv) {
  if (argv[1][0] == 'P') { int m = atoi(argv[2]), k = atoi(argv[3]); long R = atol(argv[4]); srand(atoi(argv[5]));
    static long long w[4096]; static int done[4096]; long long n[64]; int B[64];
    for (long t = 0; t < R; t++) {
      for (int a = 0; a < k; a++) { int ok; do { B[a] = 1 + rand() % (m - 1); ok = 1; for (int b = 0; b < a; b++) if (B[b] == B[a]) ok = 0; } while (!ok); }
      int g0 = m; for (int a = 0; a < k; a++) g0 = gcd(g0, B[a]); if (g0 != 1) continue;
      for (int i = 0; i < m; i++) { w[i] = -1; done[i] = 0; } w[0] = 0;
      for (int it = 0; it < m; it++) { int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
        done[b] = 1; for (int a = 0; a < k; a++) { int j = (b + m + B[a]) % m; long long v = w[b] + m + B[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
      long long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
      for (int a = 0; a < k; a++) n[a] = m + B[a];
      check(m, w, n, k, (int)(M - m + 1)); }
  } else { G = atoi(argv[1]); int gens[1] = {1}; visit(0, -1, 1, gens, 1, 0); }
  printf("q=4 S: %llu; identity failures %llu; with RAhi>0: %llu; c0<=h/2: %llu; WIN failures %llu (max ex %lld); SHIFT failures %llu (max ex %lld); minC0>0: %llu, minC0>Nlo: %llu, max minC0 %lld; S with cubes lacking Lambda-option %llu (cubes %llu), MATCH failures %llu; V1 (RAhi<=L2) fails %llu max %lld; V2 (RAhi<=tauB+Z) fails %llu max %lld; WF slack<0 (all translators bad or slack) %llu, min WF slack %lld; S with C0>0 %llu; crude C0'<=1+gensOut fails %llu max %lld; WF without Lam fails %llu min %lld; no valid translator %llu; CNT fails %llu max %lld\n",
    (unsigned long long)tot, (unsigned long long)badId, (unsigned long long)withR, (unsigned long long)c0low, (unsigned long long)failWin, maxWinEx, (unsigned long long)failShift, maxShiftEx, (unsigned long long)c0pos, (unsigned long long)c0posNlo, maxMinC0, (unsigned long long)noLoptS, (unsigned long long)noLopt, (unsigned long long)matchFail, (unsigned long long)fV1, maxV1, (unsigned long long)fV2, maxV2, (unsigned long long)fWF, minWF, (unsigned long long)withC0, (unsigned long long)fCR, maxCR, (unsigned long long)fWF2, minWF2, (unsigned long long)noTrans, (unsigned long long)fCNT, maxCNT);
  return 0;
}
