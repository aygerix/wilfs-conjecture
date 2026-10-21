/* rdexh: exhaustive residue-descent test over all numerical semigroups of genus <= G (lead, 2026-10-21).
 * Semigroup tree (children by removing minimal generators > Frobenius).  For each S (multiplicity m, minimal generators
 * g_1..g_d other than m) let T = <m, g_i mod m>; test RD: W(S) >= W(T) (W(N) := 0).  Reports failures with data and
 * the minimum of W(S) - W(T) per genus.  Also RD': (e-1)(c_S - c_T) - e(g_S - g_T) >= 0 (implies RD since e(T) <= e(S)).
 * Split: the semigroups of genus > 6 are divided by their genus-12 ancestor (round robin).  usage: ./rdexh G [part nparts] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MX 128
typedef struct { unsigned char in[MX]; int F, g, m; } SG;
static int kunzT[MX];  /* tau_s of the last Tdata call */   /* in[x] for x < MX; elements >= F+1 all in */
static long nUT[64], nAL[64], nBoth[64], nBothKnown[64], nTN[64], nDesc[64], nDescTN[64], nUTneg[64]; static long minDp2[64];
static long nRes[64], nResDneg[64], nResMono[64], minResD[64], minResMono[64];
static long nS[64], nF[64], minD[64], nFp[64], minDp[64], nTpos[64], minDpos[64]; static int bestG[64][40], bestn[64], bestW[64], bestWT[64]; static int G, Gsplit = 12, part = 0, np = 1; static long ctr = 0;
static void props(const unsigned char *in, int F, int *m, int *e, int *c, int *g, int *W, int *gens, int *ng){
  int cc = F + 1; *c = cc; int gg = 0, l = 0; for (int x = 0; x < cc; x++){ if (in[x]) l++; else gg++; } *g = gg;
  int mm = 0; for (int x = 1; x < MX; x++) if (in[x]){ mm = x; break; } *m = mm;
  int ee = 0; *ng = 0;
  for (int x = 1; x < cc + mm + 1 && x < MX; x++) if (in[x]){ int dec = 0; for (int y = 1; y <= x / 2 && !dec; y++) if (in[y] && in[x - y]) dec = 1;
      if (!dec){ ee++; gens[(*ng)++] = x; } }
  *e = ee; *W = (cc == 0) ? 0 : ee * l - cc;
}
static void Tdata(int m, int *gens, int ng, int *WT, int *cT, int *eT, long *gT){
  /* T = <m, gens mod m> via Apery of T w.r.t. m (Dijkstra over residues) */
  int w[MX], dn[MX], A[MX], na = 0; for (int i = 0; i < ng; i++){ int a = gens[i] % m; if (a){ int dup = 0; for (int j = 0; j < na; j++) if (A[j] == a) dup = 1; if (!dup) A[na++] = a; } }
  for (int x = 0; x < m; x++){ w[x] = 1 << 29; dn[x] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int u = -1; for (int x = 0; x < m; x++) if (!dn[x] && (u < 0 || w[x] < w[u])) u = x; dn[u] = 1;
    for (int j = 0; j < na; j++){ int v = w[u] + A[j], t = v % m; if (v < w[t]) w[t] = v; } }
  int mx = 0; long gg = 0; for (int x = 0; x < m; x++){ if (w[x] > mx) mx = w[x]; gg += w[x] / m; }
  int c = mx - m + 1; if (c < 0) c = 0; for (int x = 0; x < m; x++) kunzT[x] = w[x];
  /* membership up to c + m to count minimal generators */
  static unsigned char in[4 * MX]; int N = mx + m + 1; for (int z = 0; z <= N; z++) in[z] = 0;
  for (int x = 0; x < m; x++) for (int z = w[x]; z <= N; z += m) in[z] = 1;
  int e = 0; for (int z = 1; z <= N; z++) if (in[z]){ int dec = 0; for (int y = 1; y <= z / 2 && !dec; y++) if (in[y] && in[z - y]) dec = 1; if (!dec) e++; }
  *gT = gg; *cT = c; *eT = e; *WT = (c == 0) ? 0 : (int)(e * (c - gg) - c);
}
static void aligned(int m, int *gens, int ng, int W, int e, int g, int cT, int eT, long gT){
  /* Apery of S w.r.t. m, max level-weighted factorization length kappa_s by DP in increasing w */
  int w[MX], dn[MX], ord[MX], kap[MX];
  for (int x = 0; x < m; x++){ w[x] = 1 << 29; dn[x] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int u = -1; for (int x = 0; x < m; x++) if (!dn[x] && (u < 0 || w[x] < w[u])) u = x; dn[u] = 1; ord[it] = u;
    for (int j = 0; j < ng; j++){ if (gens[j] == m) continue; int v = w[u] + gens[j], t = v % m; if (v < w[t]) w[t] = v; } }
  kap[0] = 0; int Ks = 0, M = 0; long Hk = 0;
  for (int it = 1; it < m; it++){ int x = ord[it]; kap[x] = -1;
    for (int j = 0; j < ng; j++){ int G0 = gens[j]; if (G0 == m) continue; int t = ((x - G0) % m + m) % m;
      if (w[t] == w[x] - G0 && kap[t] >= 0){ int k = kap[t] + G0 / m; if (k > kap[x]) kap[x] = k; } }
    if (kap[x] > Ks) Ks = kap[x]; Hk += kap[x]; if (w[x] > M) M = w[x]; }
  int UT = 1, MT = 0; for (int x = 0; x < m; x++){ int sg = w[x] - m * kap[x]; if (sg != kunzT[x]) UT = 0; if (kunzT[x] > MT) MT = kunzT[x]; }
  int AL = (M == Ks * m + MT);
  if (!UT){ /* residual U != T: Delta' and MONO* (W_e(U) >= W(T)) */
    int MU = 0; long gU = 0; for (int x = 0; x < m; x++){ int sg = w[x] - m * kap[x]; if (sg > MU) MU = sg; gU += sg / m; }
    long cU = MU - m + 1; long WeU = (long)e * (cU - gU) - cU; long Dr = (long)(e - 1) * (M - MU) - (long)e * Hk;
    if ((long)W != Dr + WeU){ printf("ID-U FAILS g=%d\n", g); exit(5); }
    int ellT2 = (cT == 0) ? 0 : cT - (int)gT; long WT2 = (cT == 0) ? 0 : (long)eT * ellT2 - cT;
    nRes[g]++; if (Dr < 0) nResDneg[g]++; if (Dr < minResD[g]) minResD[g] = Dr;
    if (WeU < WT2){ nResMono[g]++; if (nResMono[g] <= 3){ printf("MONO* FAIL g=%d W=%d WeU=%ld W(T)=%ld Dr=%ld S=<", g, W, WeU, WT2, Dr); for (int j = 0; j < ng; j++) printf("%s%d", j ? "," : "", gens[j]); printf(">\n"); fflush(stdout); } } if (WeU - WT2 < minResMono[g]) minResMono[g] = WeU - WT2; }
  if (UT){ long Dp2 = (long)(e - 1) * (M - MT) - (long)e * Hk; int ellT = (cT == 0) ? 0 : cT - (int)gT;
    if ((long)W != Dp2 + (long)e * ellT - cT){ printf("DELTA' IDENTITY FAILS g=%d\n", g); exit(4); }
    if (Dp2 >= 0){ nDesc[g]++; if (cT == 0) nDescTN[g]++; } else { nUTneg[g]++; if (Dp2 < minDp2[g]) minDp2[g] = Dp2; } }
  nUT[g] += UT; nAL[g] += AL;
  if (UT && AL){ nBoth[g]++;
    long Delta = (long)(e - 1) * m * Ks - (long)e * Hk;
    int ellT = cT - (int)gT; if (cT == 0) ellT = 0;
    if (Delta < 0 || (long)W != Delta + (long)e * ellT - cT){ printf("ALIGNED DESCENT IDENTITY FAILS g=%d\n", g); exit(3); }
    int muT = 0; for (int x = 1; x < m; x++) ; /* multiplicity of T = least positive element */
    { int best = m; for (int x = 0; x < m; x++) if (kunzT[x] > 0 && kunzT[x] < best) best = kunzT[x]; muT = best; }
    if (cT == 0) nTN[g]++;
    else if (cT <= 4 * muT || 3 * eT >= muT || muT <= 18) nBothKnown[g]++; }
}
static void visit(unsigned char *in, int F, int g){
  int m, e, c, gg, W, gens[MX], ng; props(in, F, &m, &e, &c, &gg, &W, gens, &ng);
  if (g > 0){
    int WT, cT, eT; long gT; Tdata(m, gens, ng, &WT, &cT, &eT, &gT);
    aligned(m, gens, ng, W, e, gg, cT, eT, gT);
    nS[g]++; long D = W - WT; if (D < minD[g]) minD[g] = D;
    if (WT > 0){ nTpos[g]++; if (D < minDpos[g]){ minDpos[g] = D; bestn[g] = ng; bestW[g] = W; bestWT[g] = WT; for (int i = 0; i < ng && i < 40; i++) bestG[g][i] = gens[i]; } }
    long Dp = (long)(e - 1) * (c - cT) - (long)e * (gg - gT); if (Dp < minDp[g]) minDp[g] = Dp;
    if (Dp < 0){ nFp[g]++; if (nFp[g] <= 3){ printf("RD' FAIL g=%d Dp=%ld W=%d WT=%d c=%d cT=%d eT=%d S=<", g, Dp, W, WT, c, cT, eT); for (int i = 0; i < ng; i++) printf("%s%d", i ? "," : "", gens[i]); printf(">\n"); fflush(stdout); } }
    if (D < 0){ nF[g]++; if (nF[g] <= 5){ printf("FAIL g=%d W=%d WT=%d cT=%d eT=%d S=<", g, W, WT, cT, eT); for (int i = 0; i < ng; i++) printf("%s%d", i ? "," : "", gens[i]); printf(">\n"); fflush(stdout); } }
  }
  if (g == G) return;
  if (g == Gsplit){ if (ctr++ % np != part) return; }
  /* children: remove a minimal generator x > F */
  for (int i = 0; i < ng; i++){ int x = gens[i]; if (x <= F) continue; if (x + 1 >= MX - 2) continue;
    unsigned char ch[MX]; memcpy(ch, in, MX); ch[x] = 0; visit(ch, x, g + 1); }
}
int main(int argc, char **argv){
  G = atoi(argv[1]); if (argc > 3){ part = atoi(argv[2]); np = atoi(argv[3]); } for (int i = 0; i < 64; i++) minD[i] = minDp[i] = minDpos[i] = minResD[i] = minResMono[i] = 1L << 40;
  unsigned char in[MX]; for (int x = 0; x < MX; x++) in[x] = 1;
  visit(in, -1, 0);
  for (int g = 1; g <= G; g++) { printf("genus %d part %d/%d: S=%ld RDfail=%ld min(W(S)-W(T))=%ld RD'fail=%ld minRD'=%ld | W(T)>0: %ld, min diff %ld", g, part, np, nS[g], nF[g], minD[g], nFp[g], minDp[g], nTpos[g], nTpos[g] ? minDpos[g] : 0);
    printf(" | RESIDUAL U!=T %ld: D'<0 %ld (min %ld) MONO*fail %ld (min %ld)", nRes[g], nResDneg[g], nRes[g] ? minResD[g] : 0, nResMono[g], nRes[g] ? minResMono[g] : 0);
    printf(" | U=T %ld ALIGN %ld both %ld (T=N %ld, Wilf(T) known %ld) | descent U=T&D'>=0: %ld (T=N %ld), U=T&D'<0: %ld (min D' %ld)", nUT[g], nAL[g], nBoth[g], nTN[g], nBothKnown[g], nDesc[g], nDescTN[g], nUTneg[g], nUTneg[g] ? minDp2[g] : 0);
    if (nTpos[g]){ printf(" (W=%d W(T)=%d S=<", bestW[g], bestWT[g]); for (int i = 0; i < bestn[g] && i < 40; i++) printf("%s%d", i ? "," : "", bestG[g][i]); printf(">)"); } printf("\n"); }
  return 0;
}
