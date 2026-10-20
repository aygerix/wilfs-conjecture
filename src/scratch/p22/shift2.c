/* T1 at every window shift (lead, 2026-10-20).  T1(mu'):  sum_{a in P'} sum_{x in Ap} delta(top_a(x)) >= e * sum_{x in Ap*} delta(x),
 * delta(x) = floor((x - mu' - 1)/m), mu' in [0, m-1].  The true shift is mu = M - qm = (c-1) mod m, where T1 <=> sum_x K(x) <= m - e.
 * Reports failures at the true shift and at other shifts.  ./shift G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tightTrue, tightOther, nprint; static uint64_t tot, failTrue, failAny, failShifts; static long long minTrue = 1LL << 60, minAny = 1LL << 60; static char exTrue[400], exAny[400];
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static long long fl(long long a, long long m) { return a >= 0 ? a / m : -((-a + m - 1) / m); }
static void check(int m, long long *w, long long *n, int d, int c) {
  long long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  int q = (c + m - 1) / m; long long mu = M - (long long)q * m; tot++;
  #define INAP(v) ((v) >= 0 && w[(v) % m] == (v))
  static long long top[64][128];
  for (int a = 0; a < d; a++) for (int i = 0; i < m; i++) { long long t = w[i]; while (INAP(t + n[a])) t += n[a]; top[a][i] = t; }
  int anyfail = 0;
  for (long long s = 0; s < m; s++) {
    long long L = 0, R = 0;
    for (int i = 0; i < m; i++) { for (int a = 0; a < d; a++) L += fl(top[a][i] - s - 1, m); if (i) R += fl(w[i] - s - 1, m); }
    long long sl = L - (long long)(d + 1) * R;
    if (sl == 0) { if (s == mu) tightTrue++; else tightOther++;
      if (m >= 6 && q >= 3 && nprint < 60) { nprint++; printf("TIGHT m=%d c=%d q=%d e=%d p=%lld (true p=%lld) gens=", m, c, q, d + 1, s + 1, mu + 1); for (int a = 0; a < d; a++) printf("%lld,", n[a]); printf(" Ap="); for (int i = 0; i < m; i++) printf("%lld,", w[i]); printf("\n"); } }
    if (s == mu) { if (sl < 0) failTrue++; if (sl < minTrue) { minTrue = sl; int p = snprintf(exTrue, 400, "m=%d c=%d e=%d slack=%lld gens=", m, c, d + 1, sl); for (int a = 0; a < d && p < 380; a++) p += snprintf(exTrue + p, 400 - p, "%lld,", n[a]); } }
    else { if (sl < 0) { failShifts++; anyfail = 1; } if (sl < minAny) { minAny = sl; int p = snprintf(exAny, 400, "m=%d c=%d e=%d shift=%lld (true %lld) slack=%lld gens=", m, c, d + 1, s, mu, sl); for (int a = 0; a < d && p < 380; a++) p += snprintf(exAny + p, 400 - p, "%lld,", n[a]); } }
  }
  if (anyfail) failAny++;
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
  printf("tight pairs: true %llu other %llu\n", (unsigned long long)tightTrue, (unsigned long long)tightOther); printf("genus<=%d: %llu S (e>=3). True shift: fails %llu, min slack %lld (%s)\nOther shifts: S with a failing shift %llu, failing (S,shift) %llu, min slack %lld (%s)\n",
    G, (unsigned long long)tot, (unsigned long long)failTrue, minTrue, exTrue, (unsigned long long)failAny, (unsigned long long)failShifts, minAny, exAny);
  return 0;
}
