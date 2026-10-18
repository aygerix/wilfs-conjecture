/* cone_pw.c: as cone_restricted.c, plus class PW = RCON sets passing the pairwise Groebner-vector relaxation
 * (every face inner corner w gives a lattice vector (w, -t e_c) with unknown t; q* in Lambda; for all such vectors and
 * their pairwise differences and sums v: NOT(v+ in D and v- in D)).  PW stats are updated lazily (feasibility is
 * tested only for sets that would raise a PW maximum).  Every 3-D lattice tile in the cone class is in PW.
 * Exhaustive enumeration of the cone class: D = Cyl(A1,A2,A3) \ (q + N^3), q in Cyl with q >= (1,1,1), plus q = none,
 * over all faces with |A1 u A2 u A3| <= M; keeps |D| <= M.  (Every 3-D lattice tile has this form.)
 * [cone_split.c: per-size maxima of candidate split inequalities; qU = unit-notch Q cells, qO = other Q cells]
 * Per size: min delta, min CHT slack (m+1-(2t+2Tri+Q')), max(t - C), max(2Tri+Q' - 2C), max(LHS - 4C), max C^2/m.
 * Separate statistics for q = none (class C) and q present.   usage: cone_class M */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 40
static int M, L1, L2, L3, h[N], F[N], G[N];
static unsigned char cyl[N+1][N+1][N+1], in[N+1][N+1][N+1];
static int ht[N+1][N+1][N+1], T1[N+1][N+1][N+1], T2[N+1][N+1][N+1], T3[N+1][N+1][N+1];
#define NS 12
static const char *SN[NS] = {"t-C", "qU+tri-t", "2tri+qO-C", "qU-t", "2tri-t", "qO-C", "2tri+q-2C", "LHS-4C", "qU3+tri-t", "qO3+tri-C", "qO-t", "tri"};
typedef struct { long long cnt; int mx[NS]; char ex[NS][200]; } St;
static St st[3][N+1];
static int exT[3][64], exO[3][64], exU[3][64], exL[3][64], nfl[3][64]; static char exTs[3][64][200];
static int pc[3][3*N+3][4], pcn[3][3*N+3]; static char pcex[3][3*N+3][4][200]; /* per-C maxima: 2tri+q, LHS, tri, q */
static void fmt(char *b, int q1, int q2, int q3) {
    int p = sprintf(b, "h=");
    for (int i = 0; i < L1; i++) p += sprintf(b + p, "%d%s", h[i], i + 1 < L1 ? "," : "");
    p += sprintf(b + p, " F="); for (int i = 0; i < L1; i++) p += sprintf(b + p, "%d%s", F[i], i + 1 < L1 ? "," : "");
    p += sprintf(b + p, " G="); for (int j = 0; j < L2; j++) p += sprintf(b + p, "%d%s", G[j], j + 1 < L2 ? "," : "");
    if (q1 >= 0) sprintf(b + p, " q=(%d,%d,%d)", q1, q2, q3);
}
static int IN(int a, int b, int c) { if (a < 0 || b < 0 || c < 0 || a > N || b > N || c > N) return 0; return in[a][b][c]; }
static int INv(int *x) { return IN(x[0], x[1], x[2]); }
/* proven tile constraints for the cone class: (W) face A_c has <= q_c inner corners in [q_a,inf)x[q_b,inf);
   (FL) slice x_c = q_c - 1 has <= 1 inner corner in [q_a+1,inf)x[q_b+1,inf) */
static int tile_ok(int q1, int q2, int q3) {
    int q[3] = {q1, q2, q3}, Lm[3] = {L1, L2, L3};
    for (int c = 0; c < 3; c++) {
        int a = c == 0 ? 1 : 0, b = c == 2 ? 1 : 2;
        int nw = 0, nf = 0;
        for (int u = 1; u <= Lm[a]; u++) for (int v = 1; v <= Lm[b]; v++) {
            int w[3]; w[c] = 0; w[a] = u; w[b] = v;
            int wa[3] = {w[0], w[1], w[2]}, wb[3] = {w[0], w[1], w[2]}; wa[a]--; wb[b]--;
            if (u >= q[a] && v >= q[b] && !INv(w) && INv(wa) && INv(wb)) nw++;
            w[c] = q[c] - 1; wa[c] = w[c]; wb[c] = w[c];
            if (u >= q[a] + 1 && v >= q[b] + 1 && !INv(w) && INv(wa) && INv(wb)) nf++;
        }
        if ((!getenv("FLOORONLY") && nw > q[c]) || nf > 1) return 0;
        if (getenv("CP")) { /* column packing (assumes no wrap mod ord(e_c)): sum H_w - max H_w <= q_c - 1 */
            int sumH = 0, maxH = 0;
            for (int u = 1; u <= Lm[a]; u++) for (int v = 1; v <= Lm[b]; v++) {
                int w[3]; w[c] = 0; w[a] = u; w[b] = v;
                int wa[3] = {w[0], w[1], w[2]}, wb[3] = {w[0], w[1], w[2]}; wa[a]--; wb[b]--;
                if (!(u >= q[a] && v >= q[b] && !INv(w) && INv(wa) && INv(wb))) continue;
                int z[3] = {w[0], w[1], w[2]}; z[a] -= q[a]; z[b] -= q[b];
                int H = 0; while (INv(z)) { H++; z[c]++; }
                sumH += H; if (H > maxH) maxH = H;
            }
            if (sumH - maxH > q[c] - 1) return 0;
        }
    }
    return 1;
}

static int nit, itb[64][3], itd[64], itdom[64], val[64], fq[3], hasfq;
static int badv(int a, int b, int c) {
    if (!a && !b && !c) return 1;
    return IN(a > 0 ? a : 0, b > 0 ? b : 0, c > 0 ? c : 0) && IN(a < 0 ? -a : 0, b < 0 ? -b : 0, c < 0 ? -c : 0);
}
static void vec(int k, int *v) { v[0] = itb[k][0]; v[1] = itb[k][1]; v[2] = itb[k][2]; v[itd[k]] = -val[k]; }
static int okk(int k) {
    int v[3], w[3]; vec(k, v);
    if (badv(v[0], v[1], v[2])) return 0;
    if (hasfq && (badv(v[0]-fq[0], v[1]-fq[1], v[2]-fq[2]) || badv(v[0]+fq[0], v[1]+fq[1], v[2]+fq[2]))) return 0;
    for (int l = 0; l < k; l++) { vec(l, w);
        if (badv(v[0]-w[0], v[1]-w[1], v[2]-w[2]) || badv(v[0]+w[0], v[1]+w[1], v[2]+w[2])) return 0; }
    return 1;
}
static int rec_pw(int k) {
    if (k == nit) return 1;
    for (int x = 0; x < itdom[k]; x++) { val[k] = x; if (okk(k) && rec_pw(k + 1)) return 1; }
    return 0;
}
static int pw_ok(int q1, int q2, int q3) {
    nit = 0;
    for (int i = 1; i < L1; i++) if (h[i-1] > h[i] && h[i] >= 1) { itb[nit][0] = i; itb[nit][1] = h[i]; itb[nit][2] = 0; itd[nit] = 2; itdom[nit] = L3; nit++; }
    for (int i = 1; i < L1; i++) if (F[i-1] > F[i] && F[i] >= 1) { itb[nit][0] = i; itb[nit][1] = 0; itb[nit][2] = F[i]; itd[nit] = 1; itdom[nit] = L2; nit++; }
    for (int j = 1; j < L2; j++) if (G[j-1] > G[j] && G[j] >= 1) { itb[nit][0] = 0; itb[nit][1] = j; itb[nit][2] = G[j]; itd[nit] = 0; itdom[nit] = L1; nit++; }
    hasfq = q1 >= 0; fq[0] = q1; fq[1] = q2; fq[2] = q3;
    if (hasfq && badv(q1, q2, q3)) return 0;
    return rec_pw(0);
}
#define NP 9
static const char *PN[NP] = {"t-C", "2tri-t", "qO-t", "qU-t", "LHS-4C", "LHS-5C", "C", "tri", "Q'-t"};
static int pwmx[N+1][NP], pwn[N+1], pwall[NP]; static char pwex[N+1][NP][200], pwallex[NP][200]; static long long pwtested, pwpass;
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
    int t = 0, tri = 0, qU = 0, qO = 0, qU3 = 0, qO3 = 0, C = 0;
    for (int i = 0; i < L1; i++) for (int j = 0; j < L2; j++) for (int k = 0; k < L3; k++) {
        if (!in[i][j][k]) continue;
        int hh = T1[i][j][k] + T2[i][j][k] + T3[i][j][k];
        int nn = (T1[i][j][k] == 0) + (T2[i][j][k] == 0) + (T3[i][j][k] == 0);
        if (ht[i][j][k] == 0) t++; else if (nn == 3) tri++; else if (nn == 2 && hh == 1) {
            /* non-max top direction c; unit notch iff x + e_c not in D */
            int c = T1[i][j][k] ? 1 : T2[i][j][k] ? 2 : 3;
            int notch = c == 1 ? !in[i+1][j][k] : c == 2 ? !in[i][j+1][k] : !in[i][j][k+1];
            if (notch) { qU++; if (c == 3) qU3++; } else { qO++; if (c == 3) qO3++; }
        }
        if (k == 0 && !in[i+1][j][0] && !in[i][j+1][0]) C++;
        if (j == 0 && !in[i+1][0][k] && !in[i][0][k+1]) C++;
        if (i == 0 && !in[0][j+1][k] && !in[0][j][k+1]) C++;
    }
    if (hasq && tile_ok(q1, q2, q3)) hasq = 2;
    int Fl = 0;
    if (hasq) for (int i = 0; i < L1; i++) for (int j = 0; j < L2; j++) for (int k = 0; k < L3; k++) {
        if (!in[i][j][k] || ht[i][j][k]) continue;
        if ((i + 1 >= q1 && j >= q2 && k >= q3) || (i >= q1 && j + 1 >= q2 && k >= q3) || (i >= q1 && j >= q2 && k + 1 >= q3)) Fl++;
    }
    if (Fl > 63) Fl = 63;
    { int eT = 2*tri - t + 1, eO = qO - t + 1, eU = qU - t + 1, eL = 2*t + 2*tri + qU + qO - 5*C;
      if (!nfl[hasq][Fl] || eT > exT[hasq][Fl]) { exT[hasq][Fl] = eT; fmt(exTs[hasq][Fl], q1, q2, q3); }
      if (!nfl[hasq][Fl] || eO > exO[hasq][Fl]) exO[hasq][Fl] = eO;
      if (!nfl[hasq][Fl] || eU > exU[hasq][Fl]) exU[hasq][Fl] = eU;
      if (!nfl[hasq][Fl] || eL > exL[hasq][Fl]) exL[hasq][Fl] = eL;
      nfl[hasq][Fl]++;
      if (hasq == 2 && getenv("DUMP") && (eT > 0 || eO > 0 || eU > 0)) { char b[200]; fmt(b, q1, q2, q3); printf("DUMP eT %d eO %d eU %d Fl %d n %d t %d C %d | %s\n", eT, eO, eU, Fl, n, t, C, b); } }

    if (hasq == 2) {
        int lhs = 2*t + 2*tri + qU + qO;
        int pv[NP] = {t - C, 2*tri - t, qO - t, qU - t, lhs - 4*C, lhs - 5*C, C, tri, qU + qO - t};
        int need = 0;
        for (int a = 0; a < NP; a++) if (!pwn[n] || pv[a] > pwmx[n][a]) need = 1;
        if (getenv("PWDUMP") && tri >= atoi(getenv("PWDUMP"))) {
            if (pw_ok(q1, q2, q3)) { char b[200]; fmt(b, q1, q2, q3); printf("PWSET n %d t %d tri %d qU %d qO %d C %d | %s\n", n, t, tri, qU, qO, C, b); } }
        if (need) { pwtested++;
            if (pw_ok(q1, q2, q3)) { pwpass++;
                for (int a = 0; a < NP; a++) {
                    if (!pwn[n] || pv[a] > pwmx[n][a]) { pwmx[n][a] = pv[a]; fmt(pwex[n][a], q1, q2, q3); }
                    if (!pwtested || pv[a] > pwall[a] || pwpass == 1) { if (pwpass == 1 || pv[a] > pwall[a]) { pwall[a] = pv[a]; fmt(pwallex[a], q1, q2, q3); } }
                }
                pwn[n]++;
            } }
    }
    St *s = &st[hasq][n]; int first = s->cnt == 0; s->cnt++;
    int v[NS] = {t - C, qU + tri - t, 2*tri + qO - C, qU - t, 2*tri - t, qO - C, 2*tri + qU + qO - 2*C, 2*t + 2*tri + qU + qO - 4*C,
                 qU3 + tri - t, qO3 + tri - C, qO - t, tri};
    for (int a = 0; a < NS; a++) if (first || v[a] > s->mx[a]) { s->mx[a] = v[a]; fmt(s->ex[a], q1, q2, q3); }
    int w[4] = {2*tri + qU + qO, 2*t + 2*tri + qU + qO, tri, qU + qO};
    for (int a = 0; a < 4; a++) if (!pcn[hasq][C] || w[a] > pc[hasq][C][a]) { pc[hasq][C][a] = w[a]; fmt(pcex[hasq][C][a], q1, q2, q3); }
    pcn[hasq][C]++;
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
static void perfl(void) { for (int q = 1; q < 3; q++) for (int f = 0; f < 64; f++) if (nfl[q][f]) printf("%s Fl=%d n=%d max(2Tri-t+1) %d [%s] max(qO-t+1) %d max(qU-t+1) %d max(LHS-5C) %d\n", q == 2 ? "RCON" : "CONE", f, nfl[q][f], exT[q][f], exTs[q][f], exO[q][f], exU[q][f], exL[q][f]); }
int main(int argc, char **argv) {
    M = atoi(argv[1]);
    for (L1 = 1; L1 <= M; L1++) for (L2 = 1; L1 + L2 - 1 <= M; L2++) for (L3 = 1; L1 + L2 + L3 - 2 <= M; L3++) {
        h[0] = L2; F[0] = L3; G[0] = L3; for (int i = 1; i < L1; i++) h[i] = 1; recH(1);
    }
    for (int q = 0; q < 3; q++) for (int n = 1; n <= M; n++) {
        St *s = &st[q][n]; if (!s->cnt) continue;
        printf("%s %d count %lld", q == 2 ? "RCON" : q ? "CONE" : "CYL ", n, s->cnt);
        for (int a = 0; a < NS; a++) printf(" | %s %d", SN[a], s->mx[a]);
        printf("\n");
    }
    for (int q = 0; q < 2; q++) for (int C = 0; C < 3*N+3; C++) if (pcn[q][C])
        printf("%s perC C=%d n=%d max(2tri+q) %d [%s] max(LHS) %d max(tri) %d max(q) %d\n", q ? "CONE" : "CYL", C, pcn[q][C], pc[q][C][0], pcex[q][C][0], pc[q][C][1], pc[q][C][2], pc[q][C][3]);
    perfl();
    for (int n = 1; n <= M; n++) if (pwn[n]) { printf("PW %d", n); for (int a = 0; a < NP; a++) printf(" | %s %d", PN[a], pwmx[n][a]); printf("\n"); }
    for (int a = 0; a < NP; a++) printf("PW overall max %s %d [%s]\n", PN[a], pwall[a], pwallex[a]);
    printf("PW feasibility tests %lld, passed %lld\n", pwtested, pwpass);

    if (argc > 2) for (int q = 0; q < 3; q++) { St *s = &st[q][M]; for (int a = 0; a < NS; a++) printf("%s ex %s: %s\n", q == 2 ? "RCON" : q ? "CONE" : "CYL", SN[a], s->ex[a]); }
    return 0;
}
