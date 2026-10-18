/* Exhaustive enumeration of the cone class: D = Cyl(A1,A2,A3) \ (q + N^3), q in Cyl with q >= (1,1,1), plus q = none,
 * over all faces with |A1 u A2 u A3| <= M; keeps |D| <= M.  (Every 3-D lattice tile has this form.)
 * Per size: min delta, min CHT slack (m+1-(2t+2Tri+Q')), max(t - C), max(2Tri+Q' - 2C), max(LHS - 4C), max C^2/m.
 * Separate statistics for q = none (class C) and q present.   usage: cone_class M */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 40
static int M, L1, L2, L3, h[N], F[N], G[N];
static unsigned char cyl[N+1][N+1][N+1], in[N+1][N+1][N+1];
static int ht[N+1][N+1][N+1], T1[N+1][N+1][N+1], T2[N+1][N+1][N+1], T3[N+1][N+1][N+1];
typedef struct { long long cnt; int mindel, mincht, mtc, m2tq, ma4, mtq2t, mtri, mq; double mcr; char ex[200], ex2[200]; } St;
static St st[2][N+1];
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
    long long del = 1; int t = 0, tri = 0, qq = 0, C = 0;
    for (int i = 0; i < L1; i++) for (int j = 0; j < L2; j++) for (int k = 0; k < L3; k++) {
        if (!in[i][j][k]) continue;
        int hh = T1[i][j][k] + T2[i][j][k] + T3[i][j][k];
        int nn = (T1[i][j][k] == 0) + (T2[i][j][k] == 0) + (T3[i][j][k] == 0);
        del += hh - 1;
        if (ht[i][j][k] == 0) t++; else if (nn == 3) tri++; else if (nn == 2 && hh == 1) qq++;
        if (k == 0 && !in[i+1][j][0] && !in[i][j+1][0]) C++;
        if (j == 0 && !in[i+1][0][k] && !in[i][0][k+1]) C++;
        if (i == 0 && !in[0][j+1][k] && !in[0][j][k+1]) C++;
    }
    St *s = &st[hasq][n]; int first = s->cnt == 0; s->cnt++;
    int cht = n + 1 - (2*t + 2*tri + qq), lhs = 2*t + 2*tri + qq;
    if (first || del < s->mindel) s->mindel = del;
    if (first || cht < s->mincht) s->mincht = cht;
    if (first || t - C > s->mtc) s->mtc = t - C;
    if (first || 2*tri + qq - 2*C > s->m2tq) s->m2tq = 2*tri + qq - 2*C;
    if (first || lhs - 4*C > s->ma4) { s->ma4 = lhs - 4*C; fmt(s->ex, q1, q2, q3); }
    double cr = (double)C * C / n; if (first || cr > s->mcr) s->mcr = cr;
    if (first || 2*tri + qq - 2*t > s->mtq2t) { s->mtq2t = 2*tri + qq - 2*t; fmt(s->ex2, q1, q2, q3); }
    if (first || tri > s->mtri) s->mtri = tri;
    if (first || qq > s->mq) s->mq = qq;
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
    M = atoi(argv[1]);
    for (L1 = 1; L1 <= M; L1++) for (L2 = 1; L1 + L2 - 1 <= M; L2++) for (L3 = 1; L1 + L2 + L3 - 2 <= M; L3++) {
        h[0] = L2; F[0] = L3; G[0] = L3; for (int i = 1; i < L1; i++) h[i] = 1; recH(1);
    }
    for (int q = 0; q < 2; q++) for (int n = 1; n <= M; n++) {
        St *s = &st[q][n]; if (!s->cnt) continue;
        printf("%s %d count %lld minDelta %d minCHT %d max(t-C) %d max(2Tri+Q-2C) %d max(LHS-4C) %d maxC^2/n %.3f max(2Tri+Q-2t) %d [%s] maxTri %d maxQ %d\n",
               q ? "CONE" : "CYL ", n, s->cnt, s->mindel, s->mincht, s->mtc, s->m2tq, s->ma4, s->mcr, s->mtq2t, s->ex2, s->mtri, s->mq);
    }
    return 0;
}
