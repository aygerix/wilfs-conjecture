/* Exhaustive enumeration of the class C of q*-free cylindrical down-sets
 *   D = {(i,j,k) : j < h(i), k < min(F(i), G(j))},  h, F, G nonincreasing, entries >= 1, F(0) = G(0), h(0) = len(G),
 * with |D| <= M (two-face and degenerate sets included; C is closed under peeling D -> {x : x+e_c in D}).
 * For each D:  h(x) = sum_a ht(top_a x)   (ht = longest upward chain in D, top_a = end of the a-ray from x)
 *   delta(D) = H(D) - (|D|-1) = 1 + sum_x (h(x)-1),   Psi_c(D) = sum_{x in D, x_c = 0} (h(x) - 1).
 * Per size n reports: count, min delta, min max_c Psi_c, min Psi_{c*} for c* = direction of the largest face
 * (ties: best Psi), #sets with max_c Psi_c < 0; variant cyl_class3: MAXSUM slack 2n+1 - sum_{y max}(|y|+3).  usage: cyl_class M        (independent of the Python code) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 48
static int M;
static int L1, L2, L3, h[N], F[N], G[N];
static unsigned char in[N+1][N+1][N+1];
static int ht[N+1][N+1][N+1], T1[N+1][N+1][N+1], T2[N+1][N+1][N+1], T3[N+1][N+1][N+1];
static long long cnt[N+1];
static int mindel[N+1], minmax[N+1], minarg[N+1], negmax[N+1], minMS[N+1], negMS[N+1];
static char exMS[N+1][256];
static char exdel[N+1][256], exmax[N+1][256], exarg[N+1][256];
static void fmt(char *buf) {
    int p = 0; p += sprintf(buf + p, "h=");
    for (int i = 0; i < L1; i++) p += sprintf(buf + p, "%d%s", h[i], i + 1 < L1 ? "," : "");
    p += sprintf(buf + p, " F="); for (int i = 0; i < L1; i++) p += sprintf(buf + p, "%d%s", F[i], i + 1 < L1 ? "," : "");
    p += sprintf(buf + p, " G="); for (int j = 0; j < L2; j++) p += sprintf(buf + p, "%d%s", G[j], j + 1 < L2 ? "," : "");
}
static void eval(int n) {
    /* fill membership */
    for (int i = 0; i <= L1; i++) for (int j = 0; j <= L2; j++) for (int k = 0; k <= L3; k++) in[i][j][k] = 0;
    for (int i = 0; i < L1; i++) for (int j = 0; j < h[i]; j++) {
        int l = F[i] < G[j] ? F[i] : G[j];
        for (int k = 0; k < l; k++) in[i][j][k] = 1;
    }
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
    long long ms = 0;
    long long del = 1; long long ps[3] = {0, 0, 0}; int fs[3] = {0, 0, 0};
    for (int i = 0; i < L1; i++) for (int j = 0; j < L2; j++) for (int k = 0; k < L3; k++) {
        if (!in[i][j][k]) continue;
        int hx = T1[i][j][k] + T2[i][j][k] + T3[i][j][k] - 1;
        del += hx;
        if (ht[i][j][k] == 0) ms += i + j + k + 3;
        if (i == 0) { ps[0] += hx; fs[0]++; }
        if (j == 0) { ps[1] += hx; fs[1]++; }
        if (k == 0) { ps[2] += hx; fs[2]++; }
    }
    int mx = ps[0]; for (int c = 1; c < 3; c++) if (ps[c] > mx) mx = ps[c];
    int cs = 0; for (int c = 1; c < 3; c++) if (fs[c] > fs[cs] || (fs[c] == fs[cs] && ps[c] > ps[cs])) cs = c;
    int ar = ps[cs];
    cnt[n]++;
    if (cnt[n] == 1 || del < mindel[n]) { mindel[n] = del; fmt(exdel[n]); }
    if (cnt[n] == 1 || mx < minmax[n]) { minmax[n] = mx; fmt(exmax[n]); }
    if (cnt[n] == 1 || ar < minarg[n]) { minarg[n] = ar; fmt(exarg[n]); }
    if (mx < 0) negmax[n]++;
    int slack = 2*n + 1 - (int)ms; if (slack < 0) negMS[n]++;
    if (cnt[n] == 1 || slack < minMS[n]) { minMS[n] = slack; fmt(exMS[n]); }
}
/* recursion: choose L1, h (shape), then F, then G, pruning on size */
static int sizeD(void) {
    int s = 0;
    for (int i = 0; i < L1; i++) for (int j = 0; j < h[i]; j++) s += F[i] < G[j] ? F[i] : G[j];
    return s;
}
static void recG(int j) {
    if (j == L2) { int n = sizeD(); if (n <= M) eval(n); return; }
    for (int v = G[j-1]; v >= 1; v--) {
        G[j] = v;
        /* lower bound on size: remaining G entries >= 1 */
        int s = 0;
        for (int i = 0; i < L1; i++) for (int jj = 0; jj < h[i]; jj++) {
            int g = jj <= j ? G[jj] : 1; s += F[i] < g ? F[i] : g;
        }
        if (s > M) continue;
        recG(j + 1);
    }
}
static void recF(int i) {
    if (i == L1) { G[0] = L3; if (L2 == 1) { int n = sizeD(); if (n <= M) eval(n); return; } recG(1); return; }
    for (int v = F[i-1]; v >= 1; v--) {
        F[i] = v;
        int s = 0;   /* lower bound: columns with G >= 1 */
        for (int ii = 0; ii < L1; ii++) {
            int f = ii <= i ? F[ii] : 1;
            s += (h[ii] - 1) + f;     /* column j = 0 has height min(F, G0 = L3) = f; others >= 1 */
        }
        if (s > M) continue;
        recF(i + 1);
    }
}
static void recH(int i) {
    if (i == L1) {
        int area = 0; for (int ii = 0; ii < L1; ii++) area += h[ii];
        if (area + L3 - 1 > M) return;
        F[0] = L3; recF(1); return;
    }
    for (int v = h[i-1]; v >= 1; v--) {
        h[i] = v;
        int area = 0; for (int ii = 0; ii <= i; ii++) area += h[ii];
        area += L1 - 1 - i;
        if (area + L3 - 1 > M) continue;
        recH(i + 1);
    }
}
int main(int argc, char **argv) {
    M = atoi(argv[1]);
    if (M >= N) { fprintf(stderr, "M too large\n"); return 1; }
    for (L1 = 1; L1 <= M; L1++) for (L2 = 1; L1 + L2 - 1 <= M; L2++) for (L3 = 1; L1 + L2 + L3 - 2 <= M; L3++) {
        h[0] = L2; recH(1);
    }
    for (int n = 1; n <= M; n++)
        printf("%d count %lld minDelta %d minMaxsumSlack(2n+1-M3) %d [%s] #M3>2n+1 %d\n", n, cnt[n], mindel[n], minMS[n], exMS[n], negMS[n]);
    return 0;
}
