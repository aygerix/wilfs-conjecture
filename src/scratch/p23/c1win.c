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
  long long Lam = 0, Z = 0, Nlo = 0, RAhi = 0, g = 0;
  int c0 = 1 << 30;
  for (int i = 0; i < m; i++) { long long x = w[i]; lam[i] = (M - x) / m; K[i] = 4 - lam[i]; g += x / m;
    for (int a = 0; a < d; a++) { int j = 0; while (INS(x - (long long)(j + 1) * n[a])) j++;
      if (j) K[i] -= j * ((M - (x - n[a])) / m - lam[i]);
      top[i][a] = !INAP(x + n[a]); if (top[i][a]) Lam += (j + 1) * lam[i]; }
    int inw = ((i - h) % m + m) % m < h;  /* r in [h, 2h) mod m */
    if (K[i] < 0) Z -= K[i];
    if (K[i] <= 0 && !inw) Nlo++;
    if (K[i] == 1 && inw) { RAhi++;
      for (int a = 0; a < d; a++) if (INS(x - n[a]) && n[a] < m + h) { int t = (int)(n[a] - m); if (t < c0) c0 = t; } }
  }
  long long W = (long long)e * (c - g) - c;
  if (W != Lam + Z + Nlo - RAhi) badId++;
  if (RAhi == 0) return;
  withR++;
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

static int mm_, kk, BB[16], cur_[16]; static long long w0[4096];
static void apery0(void){
  static int done[4096]; for (int i = 0; i < mm_; i++){ w0[i] = -1; done[i] = 0; } w0[0] = 0;
  for (int it = 0; it < mm_; it++){ int b = -1; for (int i = 0; i < mm_; i++) if (!done[i] && w0[i] >= 0 && (b < 0 || w0[i] < w0[b])) b = i;
    if (b < 0) return; done[b] = 1;
    for (int a = 0; a < kk; a++){ int j = (b + mm_ + BB[a]) % mm_; long long v = w0[b] + mm_ + BB[a]; if (w0[j] < 0 || v < w0[j]) w0[j] = v; } }
}
static void evalt(int t){
  int m = mm_; static long long w[4096]; for (int i = 0; i < m; i++){ long long tail = t + ((i - t) % m + m) % m; w[i] = (w0[i] >= 0 && w0[i] < tail) ? w0[i] : tail; }
  long long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  int c = (int)(M - m + 1); if (!(3 * m < c && c <= 4 * m)) return;
  static long long n[4096]; int d = 0;
  for (int i = 1; i < m; i++){ long long x = w[i]; int dec = 0;
    for (int j = 1; j < m && !dec; j++){ long long y = w[j]; if (y < x){ long long z = x - y; if (w[z % m] <= z) dec = 1; } }
    if (!dec) n[d++] = x; }
  if (d > 60) return;
  check(m, w, n, d, c);
}
static void rec(int pos, int start){
  if (pos == kk){ for (int a = 0; a < kk; a++) BB[a] = cur_[a]; apery0();
    for (int i = 0; i < mm_; i++) if (w0[i] < 0) return;
    for (int t = 3 * mm_ + 1; t <= 4 * mm_; t++) evalt(t); return; }
  for (int b = start; b < mm_; b++){ cur_[pos] = b; rec(pos + 1, b + 1); }
}
int main(int argc, char **argv){
  int mlo = atoi(argv[1]), mhi = atoi(argv[2]); kk = atoi(argv[3]);
  for (mm_ = mlo; mm_ <= mhi; mm_++){ rec(0, 1);
    printf("m=%d: q=4 S %llu; identity failures %llu; RAhi>0 %llu; WIN failures %llu (max ex %lld); SHIFT(c0>h/2) failures %llu; minC0>Nlo %llu; MATCH failures %llu\n",
      mm_, (unsigned long long)tot, (unsigned long long)badId, (unsigned long long)withR, (unsigned long long)failWin, maxWinEx, (unsigned long long)failShift, (unsigned long long)c0posNlo, (unsigned long long)matchFail); fflush(stdout); }
}
