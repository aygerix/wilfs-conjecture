/* Top-half / bottom-half split of the Wilf defect (genus <= G).  Delta_k = |U_k| - d|L_k| (k = 1..K, d = e-1),
 * U_k = #{w in Ap : w >= km}, L_k = #{w in Ap : w <= M - km}.  i = floor((K+2)/2) (H_i reach).
 * TH = sum_{k>i} Delta_k (top half), BS = -sum_{k<=i} Delta_k (bottom slack), W = BS - TH = e*ell - c... (= d*ell - g).
 * Reports per K: #(TH>0), max TH, max TH/(something), and the PF bound PB = sum_{k>i} (t_{k-1}-d)^+ |L_k|.  fejer only. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
#define KM 40
static int G; static uint64_t cnt, perK[KM], thpos[KM], pbfail[KM]; static long maxTH[KM], minBSmTH[KM]; static int shown[KM];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  cnt++;
  int c = F + 1;
  if (c > 0 && m > 1) {
    int isS[512]; for (int z = 0; z < 512; z++) isS[z] = !gapq(gm, z);
    int ap[128], M = 0; for (int r = 0; r < m; r++) { int w = r; while (!isS[w]) w += m; ap[r] = w; if (w > M) M = w; }
    int K = M / m, d = e - 1, I = (K + 2) / 2;
    if (K < KM && K >= 3) {
      perK[K]++;
      int pf[128], t = 0;
      for (int z = 1; z <= F; z++) if (!isS[z]) { int ok = 1; for (int j = 0; j < e && ok; j++) if (!isS[z + gens[j]]) ok = 0; if (ok) pf[t++] = z; }
      long TH = 0, BS = 0, PB = 0;
      for (int k = 1; k <= K; k++) {
        long U = 0, L = 0; for (int r = 0; r < m; r++) { if (ap[r] >= k * m) U++; if (ap[r] <= M - k * m) L++; }
        long Dk = U - (long)d * L;
        if (k <= I) BS -= Dk; else { TH += Dk; int tk = 0; for (int q = 0; q < t; q++) if (pf[q] >= (k - 1) * m) tk++; if (tk > d) PB += (tk - d) * L; }
      }
      if (TH > 0) { thpos[K]++; if (shown[K]++ < 2) { printf("THPOS K=%d TH=%ld BS=%ld m=%d e=%d t=%d gens=", K, TH, BS, m, e, t); for (int q = 0; q < e; q++) printf("%d,", gens[q]); printf("\n"); } }
      if (TH > maxTH[K]) maxTH[K] = TH;
      if (TH > PB) pbfail[K]++;
      if (BS - TH < minBSmTH[K]) minBSmTH[K] = BS - TH;
    }
  }
  if (g == G) return;
  int ng[128];
  for (int j = 0; j < e; j++) {
    int n = gens[j]; if (n <= F) continue;
    u128 gm2 = gm | ((u128)1 << n); int e2 = 0, m2;
    if (n == m) { m2 = m + 1; for (int k = m2; k <= 2 * m2 - 1; k++) ng[e2++] = k; }
    else {
      m2 = m; for (int k = 0; k < e; k++) if (gens[k] != n) ng[e2++] = gens[k];
      int y = n + m, dec = 0;
      for (int a = m; a <= y / 2 && !dec; a++) if (a != n && !gapq(gm2, a) && (y - a) != n && !gapq(gm2, y - a)) dec = 1;
      if (!dec) ng[e2++] = y;
    }
    visit(gm2, n, m2, ng, e2, g + 1);
  }
}
int main(int argc, char **argv) {
  G = atoi(argv[1]); int gens[1] = {1};
  for (int k = 0; k < KM; k++) minBSmTH[k] = 1 << 30;
  visit(0, -1, 1, gens, 1, 0);
  printf("genus<=%d semigroups=%llu\n", G, (unsigned long long)cnt);
  for (int K = 3; K < KM; K++) if (perK[K]) printf("K=%d n=%llu TH>0: %llu  maxTH=%ld  TH>PFbound: %llu  min W=%ld\n", K, (unsigned long long)perK[K], (unsigned long long)thpos[K], maxTH[K], (unsigned long long)pbfail[K], minBSmTH[K]);
  return 0;
}
