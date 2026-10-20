/* TAIL test (lead, 2026-10-20). Q(z) = -sum_{x in Ap, x >= z} J(x), J(x) = sum_{a: x+n_a not in Ap}(nu_a(x)+1) - e.
 * T1(p) <=> sum_{z = p mod m, z > m} Q(z) <= 0.  TAIL(p, y): sum_{z = p mod m, z >= y} Q(z) <= 0 for every y > m.
 * Also checks the down-set version is not needed here. ./tail G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, t1fail, tailfail, monofail, monofail2; static int nex2; static char ex[400]; static int nex;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(int m, long long *w, long long *n, int d, int c) {
  tot++;
  #define INAP(v) ((v) >= 0 && w[(v) % m] == (v))
  #define INS(v) ((v) >= 0 && w[(v) % m] <= (v))
  long long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  static long long J[128];
  for (int i = 0; i < m; i++) { long long x = w[i], s = 0;
    for (int a = 0; a < d; a++) if (!INAP(x + n[a])) { int j = 0; while (INS(x - (long long)(j + 1) * n[a])) j++; s += j + 1; }
    J[i] = s - (d + 1); }
  int bad1 = 0, badt = 0;
  for (long long p = 1; p <= m; p++) {
    /* marks z = p + k m, k >= 1, z <= M; Q(z) = -sum_{x >= z} J */
    long long suffix = 0;
    for (long long z = p + m * ((M - p) / m); z > m; z -= m) {
      long long Q = 0; for (int i = 0; i < m; i++) if (w[i] >= z) Q -= J[i];
      suffix += Q;
      if (suffix > 0) { badt = 1; if (z - m <= m) bad1 = 1; }
    }
  }
  /* MONO: window J-sums over [z, z+m) <= 0 for m < z, z + m <= M (window not reaching M) */
  int bm = 0, bm2 = 0;
  for (long long z = m + 1; z + m <= M; z++) { long long s = 0; for (int i = 0; i < m; i++) if (w[i] >= z && w[i] < z + m) s += J[i]; if (s > 0) bm = 1; }
  /* MONO2: same but windows ending at or before M (z + m - 1 <= M), i.e. allowing the window to contain M */
  for (long long z = m + 1; z + m - 1 <= M; z++) { long long s = 0; for (int i = 0; i < m; i++) if (w[i] >= z && w[i] < z + m) s += J[i]; if (s > 0) bm2 = 1; }
  if (bm) { monofail++; if (nex2 < 4) { nex2++; printf("MONOFAIL m=%d c=%d e=%d gens=", m, c, d + 1); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf("\n"); } }
  if (bm2) monofail2++;
  if (bad1) t1fail++;
  if (badt) { tailfail++; if (nex < 5) { nex++; printf("TAILFAIL m=%d c=%d e=%d gens=", m, c, d + 1); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf("\n"); } }
}
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
int main(int argc, char **argv) {
  G = atoi(argv[1]); int gens[1] = {1}; visit(0, -1, 1, gens, 1, 0);
  printf("genus<=%d: %llu S; T1 failures %llu; TAIL failures (some y > m) %llu; MONO failures %llu; MONO2 failures %llu\n", G, (unsigned long long)tot, (unsigned long long)t1fail, (unsigned long long)tailfail, (unsigned long long)monofail, (unsigned long long)monofail2);
  return 0;
}
