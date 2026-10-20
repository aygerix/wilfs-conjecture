/* Split test (lead, 2026-10-20): c0 = max_w (L(w) m + r(w)) - m + 1 (virtual conductor of the order vector).
 *  (a) OW:   e * sum_w L(w) <= (e-1) * c0      (order-Wilf at the virtual conductor)
 *  (b) EXC2: e * Sigma eps   <= (e-1) * (c - c0)
 *  (a)+(b) => Wilf.  Count failures of each, and of both.
 * usage: ./exc2 G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, fa, fb, fab; static int sa, sb;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static void check(u128 gm, int m, int *gens, int e, int c){
  int top = c + m; if (top > 127) return; tot++;
  int L[260]; L[0] = 0;
  for (int s = 1; s < top; s++){ L[s] = -1; if (gapq(gm, s)) continue; for (int a = 0; a < e; a++){ int t = s - gens[a]; if (t >= 0 && L[t] >= 0 && L[t] + 1 > L[s]) L[s] = L[t] + 1; } }
  long sumL = 0, sumK = 0, mx0 = 0;
  for (int i = 0; i < m; i++){ int x = i; while (gapq(gm, x)) x += m; sumL += L[x]; sumK += x / m; long v = (long)L[x] * m + i; if (v > mx0) mx0 = v; }
  long c0 = mx0 - m + 1; long se = sumK - sumL;
  int A = ((long)e * sumL > (long)(e - 1) * c0), B = ((long)e * se > (long)(e - 1) * (c - c0));
  fa += A; fb += B; fab += (A && B);
  if (A && sa < 4){ sa++; printf("OWFAIL m=%d c=%d c0=%ld e=%d sumL=%ld gens:", m, c, c0, e, sumL); for (int a = 0; a < e; a++) printf(" %d", gens[a]); printf("\n"); }
  if (B && sb < 4){ sb++; printf("EXC2FAIL m=%d c=%d c0=%ld e=%d eps=%ld gens:", m, c, c0, e, se); for (int a = 0; a < e; a++) printf(" %d", gens[a]); printf("\n"); }
}
static void visit(u128 gm, int F, int m, int *gens, int e, int g) {
  if (F >= 1 && m >= 2) check(gm, m, gens, e, F + 1);
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
  printf("G<=%d: S %llu; OW fails %llu; EXC2 fails %llu; both %llu\n", G, (unsigned long long)tot, (unsigned long long)fa, (unsigned long long)fb, (unsigned long long)fab);
}
