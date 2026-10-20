/* TOPBAND Hall test (lead, 2026-10-20). q = ceil(c/m), h = c-(q-1)m, T' = {i in [0,h): (q-1)m+i in S}, x = |T'|,
 * D = [0,h) \ T' (residues whose Apery element is qm+i). G_i = {minimal generators p != m : p <=_S qm+i}.
 * H1: x*|U_{i in D} G_i| >= |D|.  HALL: D can be matched into G with each p used <= x times.
 * usage: ./tbhall G */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
static int G; static uint64_t tot, fH1, fHall, fTB; static int shown;
static inline int gapq(u128 g, int z) { return z < 128 && ((g >> z) & 1); }
static int nD, nG, adj[64][64], cap, use[64], who[64][64], nwho[64], vis[64];
static int aug(int i){ for (int a = 0; a < nG; a++) if (adj[i][a] && !vis[a]){ vis[a] = 1;
    if (nwho[a] < cap){ who[a][nwho[a]++] = i; return 1; }
    for (int k = 0; k < nwho[a]; k++){ int i2 = who[a][k]; if (aug(i2)){ who[a][k] = i; return 1; } } }
  return 0; }
static void check(u128 gm, int m, int *gens, int e, int c){ { int q0=(c+m-1)/m; if(q0>=2){ int lo0=(q0-1)*m,h0=c-lo0,x0=0; for(int i=0;i<h0;i++) if(!gapq(gm,lo0+i)) x0++; if((long)e*x0==h0 && x0>=2 && shown<40){ shown++; printf("TIGHT m=%d c=%d q=%d h=%d x=%d e=%d gens:",m,c,q0,h0,x0,e); for(int a=0;a<e;a++) printf(" %d",gens[a]); printf("\n"); } } }
  int q = (c + m - 1) / m; if (q < 2) return; tot++;
  int lo = (q - 1) * m, h = c - lo, x = 0, Dl[64]; nD = 0;
  for (int i = 0; i < h; i++){ if (!gapq(gm, lo + i)) x++; else Dl[nD++] = i; }
  int gl[64]; nG = 0; for (int a = 0; a < e; a++) if (gens[a] != m) gl[nG++] = gens[a];
  int any[64]; memset(any, 0, sizeof any);
  for (int d = 0; d < nD; d++){ int w = q * m + Dl[d]; for (int a = 0; a < nG; a++){ int z = w - gl[a]; adj[d][a] = (z >= 0 && !gapq(gm, z)); if (adj[d][a]) any[a] = 1; } }
  int U = 0; for (int a = 0; a < nG; a++) U += any[a];
  if ((long)e * x < h) fTB++;
  int h1 = ((long)x * U >= nD); if (!h1) fH1++;
  cap = x; for (int a = 0; a < nG; a++) nwho[a] = 0; int matched = 0;
  for (int d = 0; d < nD; d++){ memset(vis, 0, sizeof vis); if (aug(d)) matched++; }
  if (matched < nD){ fHall++; if (0){ shown++; printf("HALLFAIL m=%d c=%d q=%d h=%d x=%d e=%d |D|=%d U=%d matched=%d gens:", m, c, q, h, x, e, nD, U, matched);
      for (int a = 0; a < e; a++) printf(" %d", gens[a]); printf("\n"); } }
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
  printf("G<=%d: S(q>=2) %llu; TOPBAND fails %llu; H1 fails %llu; HALL fails %llu\n", G, (unsigned long long)tot,
    (unsigned long long)fTB, (unsigned long long)fH1, (unsigned long long)fHall);
}
