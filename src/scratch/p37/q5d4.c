/* q5d: the dense regime of the level-1 q = 5 class at fixed d (lead, 2026-10-21).
 * Domain: multiplicity m in [mlo, mhi]; generator residues A = {a_1 < ... < a_d} c [1, m-1], all generators m + a
 * minimal; q = 5; every factorization of every Apery element has length <= 3.  Non-graded S are INCLUDED: h_s is the
 * minimum factorization length (the grlex-least factorization, so CH' applies) and sigma_s = w_s - m h_s.
 * Checks on every S: l = 5m - H - N (LEVEL1-THRESHOLD), W = Delta3 - E3 with Delta3 = 3(e-1)m - eH >= 0 (CH'),
 * E3 <= 0 <=> e(|X|+|Y|) >= m+r+1, X = {s : sigma_s <= m+r}, Y = {s : sigma_s <= r}.
 * Reports: counts (all / graded), failures of E3 <= 0 and of WINDOW e|X| >= m+r+1, smallest slacks with full data.
 * mode 1 (q5d d mlo mhi part nparts 1): h_s = MAX factorization length (down-set of max-length factorizations, CH' holds);
 *   then U := {sigma_s} + mN = (A'+A'+A') + mN and E3 <= 0 <=> e |U n [0,c_U)| >= c_U, c_U = m + r + 1 (asserted).  Compares U
 *   with T = <m, A> (Apery of T w.r.t. m by Dijkstra over A), tests U + U c U, and when U = T records Wilf data of T.
 *   On the residual U != T it reports MONO*: min of W_e(U) - W(T) (W_e(U) = e l_U - c_U = -E3, W(T) with e(T)),
 *   and RESID-PAY: Delta3 >= e |T \ U| (|T \ U| = sum_s (sigma_s - tau_s)/m).
 *   q5d4 adds, on the residual: the combined identity W(S) - W(T) = Delta3 - e h + (e-1) dc + (e - e(T)) l(T) (asserted;
 *   h = |T \ U|, dc = c_U - c_T), PAY2 := Delta3 + (e-1) dc - e h >= 0 (the residual through W(T) >= 0 alone, without
 *   T's padding term), and PAY3 := PAY2 + (e - e(T)) l(T) = W(S) - W(T) (RD on the residual).
 * usage: ./q5d d mlo mhi part nparts [mode] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXM 128
#define TOP 5
typedef struct { long v; int m, r, X, Y, H, N, graded, UeqT, eT, ellT, cT; long W, E3, D3; int A[16]; } Rec;
static void push(Rec *arr, int *n, Rec *x){
  int pos = *n; for (int i = 0; i < *n; i++) if (x->v < arr[i].v){ pos = i; break; }
  if (pos >= TOP) return; int last = (*n < TOP) ? *n : TOP - 1;
  for (int i = last; i > pos; i--) arr[i] = arr[i - 1]; arr[pos] = *x; if (*n < TOP) (*n)++;
}
static void prec(const char *tag, Rec *x, int d){
  printf("%s %ld | m=%d e=%d r=%d |X|=%d |Y|=%d H=%d N=%d W=%ld E3=%ld Delta3=%ld graded=%d U=T:%d T: e=%d l=%d c=%d | <%d", tag, x->v, x->m, d + 1, x->r,
         x->X, x->Y, x->H, x->N, x->W, x->E3, x->D3, x->graded, x->UeqT, x->eT, x->ellT, x->cT, x->m);
  for (int b = 0; b < d; b++) printf(",%d", x->m + x->A[b]); printf(">\n");
}
int main(int argc, char **argv){
  if (argc < 6){ fprintf(stderr, "usage: ./q5d d mlo mhi part nparts\n"); return 1; }
  int d = atoi(argv[1]), mlo = atoi(argv[2]), mhi = atoi(argv[3]), part = atoi(argv[4]), np = atoi(argv[5]);
  if (mhi >= MAXM || d > 15 || d < 1) { fprintf(stderr, "bad parameters\n"); return 1; }
  int e = d + 1, mode = argc > 6 ? atoi(argv[6]) : 0; long nUT = 0, nUclosed = 0, nTwilffail = 0, nUTE3 = 0, nRes = 0, minMS = 1L << 40, minPay = 1L << 40, failPay = 0, minP2 = 1L << 40, failP2 = 0, minP3 = 1L << 40, failP3 = 0; int p2A[16] = {0}, p2m = 0, p3A[16] = {0}, p3m = 0; int msA[16] = {0}, msm = 0, mseT = 0, payA[16] = {0}, paym = 0;
  for (int m = mlo; m <= mhi; m++){
    if (m - 1 < d) continue;
    long nS = 0, nGr = 0, fE3 = 0, fX = 0, ncomb = 0, nfilt = 0; long minW = 1L << 60; int minWA[16] = {0};
    Rec tX[TOP], tE[TOP]; int nX = 0, nE = 0;
    int a[16]; for (int i = 0; i < d; i++) a[i] = i + 1;
    while (1){
      if (ncomb++ % np == part){
        /* filter: residues of {0} u A u 2A u 3A must cover Z/m */
        static char cv[MAXM]; memset(cv, 0, m); cv[0] = 1; int ncv = 1;
        for (int i = 0; i < d; i++){ int x = a[i] % m; if (!cv[x]){ cv[x] = 1; ncv++; }
          for (int j = i; j < d; j++){ int y = (a[i] + a[j]) % m; if (!cv[y]){ cv[y] = 1; ncv++; }
            for (int k = j; k < d; k++){ int z = (a[i] + a[j] + a[k]) % m; if (!cv[z]){ cv[z] = 1; ncv++; } } } }
        if (ncv == m){
          nfilt++;
          int w[MAXM], done[MAXM], order[MAXM], G[16], ok = 1, lim = 6 * m;
          for (int x = 0; x < m; x++){ w[x] = 1 << 29; done[x] = 0; } w[0] = 0;
          for (int b = 0; b < d; b++) G[b] = m + a[b];
          for (int it = 0; it < m; it++){
            int u = -1; for (int x = 0; x < m; x++) if (!done[x] && (u < 0 || w[x] < w[u])) u = x;
            if (w[u] >= lim){ ok = 0; break; }
            done[u] = 1; order[it] = u;
            for (int b = 0; b < d; b++){ int v = w[u] + G[b], t = v % m; if (v < w[t]) w[t] = v; }
          }
          for (int b = 0; b < d && ok; b++) if (w[a[b]] != G[b]) ok = 0;
          int r = 0; if (ok){ for (int x = 1; x < m; x++) if (w[x] > w[r]) r = x; if (w[r] < 5 * m) ok = 0; }
          int hmx[MAXM], hmn[MAXM];
          if (ok){
            hmx[0] = hmn[0] = 0;
            for (int it = 1; it < m && ok; it++){
              int x = order[it]; hmx[x] = -1; hmn[x] = 99;
              for (int b = 0; b < d; b++){
                int t = ((x - a[b]) % m + m) % m;
                if (w[t] == w[x] - G[b]){
                  if (t != 0 && hmx[t] < 0){ ok = 0; break; }
                  if (hmx[t] + 1 > hmx[x]) hmx[x] = hmx[t] + 1; if (hmn[t] + 1 < hmn[x]) hmn[x] = hmn[t] + 1;
                }
              }
              if (hmx[x] < 0) ok = 0;
              if (ok && hmx[x] > 3) ok = 0;
            }
          }
          if (ok){
            long c = w[r] - m + 1; int rho = 5 * m - (int)c; long g = 0; int graded = 1;
            for (int x = 1; x < m; x++){ g += w[x] / m; if (hmx[x] != hmn[x]) graded = 0; }
            long W = (long)e * (c - g) - c; int H = 0, N = 0, X = 0, Y = 0;
            int *hh = mode ? hmx : hmn;
            for (int x = 0; x < m; x++){ int sg = w[x] - m * hh[x]; H += hh[x];
              if (sg > r) N++; if (sg > m + r) N++; if (sg > 2 * m + r){ fprintf(stderr, "third threshold\n"); return 5; }
              if (sg <= m + r) X++; if (sg <= r) Y++; }
            if ((long)e * (5L * m - H - N) - c != W){ fprintf(stderr, "IDENTITY FAILS\n"); return 6; }
            long D3 = 3L * (e - 1) * m - (long)e * H, E3 = (long)e * N - 2L * (e - 1) * m - rho;
            if (D3 < 0){ fprintf(stderr, "CH' FAILS\n"); return 7; }
            if (D3 - E3 != W){ fprintf(stderr, "W != D3 - E3\n"); return 8; }
            if (((long)e * (X + Y) >= m + r + 1) != (E3 <= 0)){ fprintf(stderr, "window reformulation FAILS\n"); return 9; }
            if (W < 0){ fprintf(stderr, "WILF FAILS m=%d\n", m); }
            int UeqT = 0, eT = 0, ellT = 0, cT = 0;
            if (mode){
              int sgm[MAXM], tau[MAXM], dn[MAXM]; int mxs = 0;
              for (int x = 0; x < m; x++){ sgm[x] = w[x] - m * hmx[x]; if (sgm[x] > mxs) mxs = sgm[x]; tau[x] = 1 << 29; dn[x] = 0; }
              if (mxs != 2 * m + r){ fprintf(stderr, "c_U != m+r+1\n"); return 12; }
              { int ell = 0; for (int x = 0; x < m; x++) for (int k = 0; sgm[x] + k * m <= m + r; k++) ell++;
                if (ell != X + Y){ fprintf(stderr, "l_U != X+Y\n"); return 13; } }
              tau[0] = 0;
              for (int it = 0; it < m; it++){ int u = -1; for (int x = 0; x < m; x++) if (!dn[x] && (u < 0 || tau[x] < tau[u])) u = x;
                dn[u] = 1; for (int b = 0; b < d; b++){ int v = tau[u] + a[b], t = v % m; if (v < tau[t]) tau[t] = v; } }
              UeqT = 1; for (int x = 0; x < m; x++){ if (tau[x] > sgm[x]){ fprintf(stderr, "T > U ?\n"); return 14; } if (tau[x] < sgm[x]) UeqT = 0; }
              int clos = 1; for (int x = 0; x < m && clos; x++) for (int y = x; y < m; y++) if (sgm[(x + y) % m] > sgm[x] + sgm[y]){ clos = 0; break; }
              nUclosed += clos; nUT += UeqT;
              { /* Wilf data of T = <m, A> by membership on [0, 3m] */
                static char inT[4 * MAXM]; int Nn = 3 * m + 2; for (int z = 0; z <= Nn; z++) inT[z] = 0;
                for (int x = 0; x < m; x++) for (int z = tau[x]; z <= Nn; z += m) inT[z] = 1;
                int lastgap = -1; for (int z = 0; z <= Nn; z++) if (!inT[z]) lastgap = z; cT = lastgap + 1;
                for (int z = 0; z < cT; z++) ellT += inT[z];
                for (int z = 1; z <= Nn; z++) if (inT[z]){ int dec = 0; for (int y = 1; y < z && !dec; y++) if (inT[y] && inT[z - y]) dec = 1; if (!dec) eT++; }
                if (UeqT && (cT != m + r + 1 || ellT != X + Y)){ fprintf(stderr, "T/U mismatch\n"); return 15; }
                if ((long)eT * ellT < cT) nTwilffail++;
                if (UeqT && E3 > 0) nUTE3++;
                if (!UeqT){ /* MONO*: W_e(U) - W(T) on the residual */
                  long WeU = (long)e * (X + Y) - (m + r + 1), WT = (cT > 0) ? (long)eT * ellT - cT : 0; nRes++;
                  if (WeU - WT < minMS){ minMS = WeU - WT; memcpy(msA, a, sizeof a); msm = m; mseT = eT; }
                  /* RESID-PAY: Delta3 >= e |T \ U|, |T \ U| = sum (sigma - tau)/m */
                  long TU = 0; for (int x = 0; x < m; x++) TU += (sgm[x] - tau[x]) / m;
                  long pay = D3 - (long)e * TU; if (pay < 0) failPay++; if (pay < minPay){ minPay = pay; memcpy(payA, a, sizeof a); paym = m; }
                  long dc = (m + r + 1) - cT, p2 = D3 + (long)(e - 1) * dc - (long)e * TU, p3 = p2 + (long)(e - eT) * ellT;
                  if (W - WT != p3){ fprintf(stderr, "combined identity FAILS m=%d\n", m); return 16; }
                  if (p2 < 0) failP2++; if (p2 < minP2){ minP2 = p2; memcpy(p2A, a, sizeof a); p2m = m; }
                  if (p3 < 0) failP3++; if (p3 < minP3){ minP3 = p3; memcpy(p3A, a, sizeof a); p3m = m; } } }
            }
            nS++; nGr += graded; if (E3 > 0) fE3++;
            long sx = (long)e * X - (m + r + 1); if (sx < 0) fX++;
            if (W < minW){ minW = W; memcpy(minWA, a, sizeof a); }
            Rec R; memset(&R, 0, sizeof R); R.m = m; R.r = r; R.X = X; R.Y = Y; R.H = H; R.N = N; R.graded = graded; R.W = W;
            R.E3 = E3; R.D3 = D3; memcpy(R.A, a, sizeof a); R.UeqT = UeqT; R.eT = eT; R.ellT = ellT; R.cT = cT;
            R.v = sx; push(tX, &nX, &R); R.v = -E3; push(tE, &nE, &R);
          }
        }
      }
      int i = d - 1; while (i >= 0 && a[i] == m - d + i) i--; if (i < 0) break; a[i]++; for (int j = i + 1; j < d; j++) a[j] = a[j - 1] + 1;
    }
    printf("SUMMARY d=%d m=%d part=%d/%d subsets=%ld covering=%ld S=%ld graded=%ld E3>0=%ld WINDOWfail=%ld minW=%ld", d, m, part, np,
           ncomb, nfilt, nS, nGr, fE3, fX, nS ? minW : 0);
    if (nS){ printf(" <%d", m); for (int b = 0; b < d; b++) printf(",%d", m + minWA[b]); printf(">"); }
    if (mode){ printf(" | U=T:%ld Uclosed:%ld Twilffail:%ld E3>0withU=T:%ld residual:%ld", nUT, nUclosed, nTwilffail, nUTE3, nRes);
      if (nRes){ printf(" minMONO*=%ld (eT=%d) at <%d", minMS, mseT, msm); for (int b = 0; b < d; b++) printf(",%d", msm + msA[b]); printf(">");
        printf(" RESID-PAY fail %ld min %ld at <%d", failPay, minPay, paym); for (int b = 0; b < d; b++) printf(",%d", paym + payA[b]); printf(">");
        printf(" PAY2 fail %ld min %ld at <%d", failP2, minP2, p2m); for (int b = 0; b < d; b++) printf(",%d", p2m + p2A[b]); printf(">");
        printf(" PAY3 fail %ld min %ld at <%d", failP3, minP3, p3m); for (int b = 0; b < d; b++) printf(",%d", p3m + p3A[b]); printf(">"); } }
    printf("\n"); nUT = nUclosed = nTwilffail = nUTE3 = nRes = 0; minMS = 1L << 40; minPay = 1L << 40; failPay = 0; minP2 = minP3 = 1L << 40; failP2 = failP3 = 0;
    for (int i = 0; i < nX; i++) prec(" minWINDOWslack", &tX[i], d);
    for (int i = 0; i < nE; i++) prec(" min(-E3)", &tE[i], d);
    fflush(stdout);
  }
  return 0;
}
