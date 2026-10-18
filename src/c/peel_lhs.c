/* peel_lhs.c [M wM wT wU wO kappa [x]]: weights per cell type (max, tripod, unit-notch Q', other Q'), currency kappa;
 * W = sum of weights; peeling inequality PI_c = (face-c weight) - 4 (C(D) - C(D'_c)); weight 2 for h = 0, 1 for Q'.
 * Exhaustive enumeration of the cone class: D = Cyl(A1,A2,A3) \ (q + N^3), q in Cyl with q >= (1,1,1), plus q = none,
 * over all faces with |A1 u A2 u A3| <= M; keeps |D| <= M.  (Every 3-D lattice tile has this form.)
 * [cone_split.c: per-size maxima of candidate split inequalities; qU = unit-notch Q cells, qO = other Q cells]
 * Per size: min delta, min CHT slack (m+1-(2t+2Tri+Q')), max(t - C), max(2Tri+Q' - 2C), max(LHS - 4C), max C^2/m.
 * Separate statistics for q = none (class C) and q present.   usage: cone_class M */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 40
static int SMAXV = 3;
static int WM = 2, WT = 2, WU = 1, WO = 1, KAP = 4;
static int M, L1, L2, L3, h[N], F[N], G[N];
static unsigned char cyl[N+1][N+1][N+1], in[N+1][N+1][N+1];
static int ht[N+1][N+1][N+1], T1[N+1][N+1][N+1], T2[N+1][N+1][N+1], T3[N+1][N+1][N+1];
#define NS 12
static const char *SN[NS] = {"W-KC", "min_c PI_c", "PI_3", "lev(nontop)", "lev(top)", "", "", "", "", "", "", ""};
typedef struct { long long cnt, nfail, nvfail, nunit, nmixed, ndouble; char exm[200], exd[200]; int mx[NS], maxfailslack; char ex[NS][200]; } St;
static St st[2][N+1];
static int pc[2][3*N+3][4], pcn[2][3*N+3]; static char pcex[2][3*N+3][4][200]; /* per-C maxima: 2tri+q, LHS, tri, q */
static void fmt(char *b, int q1, int q2, int q3) {
    int p = sprintf(b, "h=");
    for (int i = 0; i < L1; i++) p += sprintf(b + p, "%d%s", h[i], i + 1 < L1 ? "," : "");
    p += sprintf(b + p, " F="); for (int i = 0; i < L1; i++) p += sprintf(b + p, "%d%s", F[i], i + 1 < L1 ? "," : "");
    p += sprintf(b + p, " G="); for (int j = 0; j < L2; j++) p += sprintf(b + p, "%d%s", G[j], j + 1 < L2 ? "," : "");
    if (q1 >= 0) sprintf(b + p, " q=(%d,%d,%d)", q1, q2, q3);
}
static void evalD(int n, int hasq, int q1, int q2, int q3) {
    for (int i = L1 - 1; i >= 0; i--) for (int j = L2 - 1; j >= 0; j--) for (int k = L3 - 1; k >= 0; k--) {
        if (!in[i][j][k]) continue;
        int v = 0;
        if (in[i+1][j][k] && ht[i+1][j][k] + 1 > v) v = ht[i+1][j][k] + 1;
        if (in[i][j+1][k] && ht[i][j+1][k] + 1 > v) v = ht[i][j+1][k] + 1;
        if (in[i][j][k+1] && ht[i][j][k+1] + 1 > v) v = ht[i][j][k+1] + 1;
        ht[i][j][k] = v;
        T1[i][j][k] = in[i+1][j][k] ? T1[i+1][j][k] : v;
        T2[i][j][k] = in[i][j+1][k] ? T2[i][j+1][k] : v;
        T3[i][j][k] = in[i][j][k+1] ? T3[i][j][k+1] : v;
    }
    static int wt[N+1][N+1][N+1];
    int lhs = 0, C = 0, Lx[3] = {0, 0, 0};
    for (int i = 0; i < L1; i++) for (int j = 0; j < L2; j++) for (int k = 0; k < L3; k++) {
        wt[i][j][k] = 0;
        if (!in[i][j][k]) continue;
        if (i + 1 > Lx[0]) Lx[0] = i + 1; if (j + 1 > Lx[1]) Lx[1] = j + 1; if (k + 1 > Lx[2]) Lx[2] = k + 1;
        int hh = T1[i][j][k] + T2[i][j][k] + T3[i][j][k];
        int nn = (T1[i][j][k] == 0) + (T2[i][j][k] == 0) + (T3[i][j][k] == 0);
        int w = 0;
        if (ht[i][j][k] == 0) w = WM; else if (nn == 3) w = WT; else if (nn == 2 && hh == 1) {
            int c = T1[i][j][k] ? 1 : T2[i][j][k] ? 2 : 3;
            int notch = c == 1 ? !in[i+1][j][k] : c == 2 ? !in[i][j+1][k] : !in[i][j][k+1];
            w = notch ? WU : WO;
        }
        wt[i][j][k] = w; lhs += w;
        if (k == 0 && !in[i+1][j][0] && !in[i][j+1][0]) C++;
        if (j == 0 && !in[i+1][0][k] && !in[i][0][k+1]) C++;
        if (i == 0 && !in[0][j+1][k] && !in[0][j][k+1]) C++;
    }
    int lvmax = -999, lvtop = 0;
    for (int k = 0; k < Lx[2]; k++) {
        int sm = 0;
        for (int i = 0; i < L1; i++) for (int j = 0; j < L2; j++) if (in[i][j][k]) sm += wt[i][j][k];
        if (k == Lx[2] - 1) lvtop = sm; else if (sm > lvmax) lvmax = sm;
    }
    /* peeling: D'_c = {x : x + e_c in D}; faces of D'_c are the slices x_a = 1 (a != c) shifted, and slice x_c = 1 */
    int best = 1 << 30, bestc = -1, allpi[3] = {99, 99, 99};
    for (int c = 0; c < 3; c++) {
        if (Lx[c] < 2) continue;
        int layer = 0, Cp = 0;
        for (int i = 0; i < L1; i++) for (int j = 0; j < L2; j++) for (int k = 0; k < L3; k++) {
            int x[3] = {i, j, k};
            if (!in[i][j][k]) continue;
            if (x[c] == 0) { layer += wt[i][j][k]; continue; }
            /* x in D, x_c >= 1: x - e_c in D'. corner of face b of D' at x - e_c if (x - e_c)_b == 0 */
            for (int b = 0; b < 3; b++) {
                int yb = x[b] - (b == c);
                if (yb != 0) continue;
                int ok = 1;
                for (int a = 0; a < 3; a++) if (a != b) {
                    int z[3] = {x[0], x[1], x[2]}; z[a]++;
                    if (in[z[0]][z[1]][z[2]]) ok = 0;
                }
                Cp += ok;
            }
        }
        int pi = layer - KAP * (C - Cp);
        allpi[c] = pi;
        if (pi < best) { best = pi; bestc = c; }
    }
    int vbest = 1 << 30, smax = SMAXV, gm = 0;
    for (int s1 = 0; s1 <= smax; s1++) for (int s2 = 0; s2 <= smax; s2++) for (int s3 = 0; s3 <= smax; s3++) {
        if (s1 + s2 + s3 == 0 || s1 + s2 + s3 > smax) continue;
        if (s1 >= Lx[0] || s2 >= Lx[1] || s3 >= Lx[2]) continue;
        if (!in[s1][s2][s3]) continue;
        int out = 0, Cs = 0;
        for (int i = 0; i < L1; i++) for (int j = 0; j < L2; j++) for (int k = 0; k < L3; k++) {
            if (!in[i][j][k]) continue;
            if (i < s1 || j < s2 || k < s3) { out += wt[i][j][k]; continue; }
            int y[3] = {i - s1, j - s2, k - s3};
            for (int b = 0; b < 3; b++) {
                if (y[b] != 0) continue;
                int ok = 1;
                for (int a = 0; a < 3; a++) if (a != b) { int z[3] = {i, j, k}; z[a]++; if (in[z[0]][z[1]][z[2]]) ok = 0; }
                Cs += ok;
            }
        }
        int pv = out - KAP * (C - Cs);
        if (pv < vbest) vbest = pv;
        if (pv <= 0) { int ss = s1 + s2 + s3; if (ss == 1) gm |= 1; else if (s1 == 2 || s2 == 2 || s3 == 2) gm |= 4; else gm |= 2; }
    }
    St *s = &st[hasq][n]; int first = s->cnt == 0; s->cnt++;
    if (vbest != (1 << 30) && vbest > 0) s->nvfail++;
    if (gm & 1) s->nunit++; else if (gm & 2) { if (!s->nmixed) fmt(s->exm, q1, q2, q3); s->nmixed++; } else if (gm & 4) { if (!s->ndouble) fmt(s->exd, q1, q2, q3); s->ndouble++; }
    if (best != (1 << 30) && best > 0) { if (!s->nfail || lhs - KAP*C > s->maxfailslack) s->maxfailslack = lhs - KAP*C; s->nfail++; }
    int mn = allpi[0]; for (int c = 1; c < 3; c++) if (allpi[c] < mn) mn = allpi[c];
    int v[NS] = {lhs - KAP*C, best == (1 << 30) ? -99 : best, allpi[2] == 99 ? -99 : allpi[2], lvmax, lvtop, 0, 0, 0, 0, 0, 0, 0, 0};
    for (int a = 0; a < 5; a++) if (first || v[a] > s->mx[a]) { s->mx[a] = v[a]; fmt(s->ex[a], q1, q2, q3); }
}
static void process(void) {
    memset(cyl, 0, sizeof cyl);
    int cs = 0;
    for (int i = 0; i < L1; i++) for (int j = 0; j < h[i]; j++) {
        int l = F[i] < G[j] ? F[i] : G[j];
        for (int k = 0; k < l; k++) { cyl[i][j][k] = 1; cs++; }
    }
    if (cs <= M) { memcpy(in, cyl, sizeof in); evalD(cs, 0, -1, -1, -1); }
    for (int q1 = 1; q1 < L1; q1++) for (int q2 = 1; q2 < L2; q2++) for (int q3 = 1; q3 < L3; q3++) {
        if (!cyl[q1][q2][q3]) continue;
        int n = 0;
        for (int i = 0; i <= L1; i++) for (int j = 0; j <= L2; j++) for (int k = 0; k <= L3; k++) {
            in[i][j][k] = cyl[i][j][k] && !(i >= q1 && j >= q2 && k >= q3); n += in[i][j][k];
        }
        if (n <= M) evalD(n, 1, q1, q2, q3);
    }
}
static int unionsize(int upto_i, int upto_j) { /* lower bound with unfilled entries = 1 */
    int s = 0;
    for (int i = 0; i < L1; i++) s += h[i] + (i < upto_i ? F[i] : 1);
    for (int j = 0; j < L2; j++) s += (j < upto_j ? G[j] : 1);
    return s - L1 - L2 - L3 + 1;
}
static void recG(int j) {
    if (j == L2) { process(); return; }
    for (int v = G[j-1]; v >= 1; v--) { G[j] = v; if (unionsize(L1, j + 1) > M) continue; recG(j + 1); }
}
static void recF(int i) {
    if (i == L1) { G[0] = L3; if (L2 == 1) { process(); return; } recG(1); return; }
    for (int v = F[i-1]; v >= 1; v--) { F[i] = v; if (unionsize(i + 1, 1) > M) continue; recF(i + 1); }
}
static void recH(int i) {
    if (i == L1) { F[0] = L3; G[0] = L3; if (unionsize(1, 1) > M) return; recF(1); return; }
    for (int v = h[i-1]; v >= 1; v--) { h[i] = v; for (int ii = i + 1; ii < L1; ii++) h[ii] = 1; if (unionsize(1, 1) > M) continue; recH(i + 1); }
}
int main(int argc, char **argv) {
    M = atoi(argv[1]); if (argc > 6) { WM = atoi(argv[2]); WT = atoi(argv[3]); WU = atoi(argv[4]); WO = atoi(argv[5]); KAP = atoi(argv[6]); } if (getenv("SMAXV")) SMAXV = atoi(getenv("SMAXV"));
    for (L1 = 1; L1 <= M; L1++) for (L2 = 1; L1 + L2 - 1 <= M; L2++) for (L3 = 1; L1 + L2 + L3 - 2 <= M; L3++) {
        h[0] = L2; F[0] = L3; G[0] = L3; for (int i = 1; i < L1; i++) h[i] = 1; recH(1);
    }
    for (int q = 0; q < 2; q++) for (int n = 1; n <= M; n++) {
        St *s = &st[q][n]; if (!s->cnt) continue;
        printf("%s %d count %lld", q ? "CONE" : "CYL ", n, s->cnt);
        for (int a = 0; a < 5; a++) printf(" | %s %d", SN[a], s->mx[a]);
        printf(" | PIfail %lld maxW-KC among fails %d | vecPIfail(|s|<=3) %lld", s->nfail, s->nfail ? s->maxfailslack : 0, s->nvfail);
        printf(" | unit %lld mixedonly %lld [%s] doubleonly %lld [%s]", s->nunit, s->nmixed, s->exm, s->ndouble, s->exd);
        printf("\n");
    }
    if (0) for (int q = 0; q < 2; q++) for (int C = 0; C < 3*N+3; C++) if (pcn[q][C])
        printf("%s perC C=%d n=%d max(2tri+q) %d [%s] max(LHS) %d max(tri) %d max(q) %d\n", q ? "CONE" : "CYL", C, pcn[q][C], pc[q][C][0], pcex[q][C][0], pc[q][C][1], pc[q][C][2], pc[q][C][3]);
    if (argc > 7) for (int q = 0; q < 2; q++) { St *s = &st[q][M]; for (int a = 0; a < 5; a++) printf("%s ex %s: %s\n", q ? "CONE" : "CYL", SN[a], s->ex[a]); }
    return 0;
}
