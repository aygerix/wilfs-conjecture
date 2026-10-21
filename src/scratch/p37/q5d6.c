/* q5d6: local structure of Delta3 on the Q5 residual (lead, 2026-10-21); q5d5 + the tile analysis below.
 * D = lex-largest max-length factorizations x_s (a down-set; x_s = max_lex over valid predecessors of x_t + e_b).
 * Column-top form (asserted): Delta3 = sum_s sum_{i : x_s + e_i not in D} ((x_s)_i + 1)(3 - |x_s|) =: sum_s P_s.
 * j_s = (sigma_s - tau_s)/m.  Classes: NE2 = {j >= 1, h = 2}, NE3 = {j >= 1, h = 3}, EQ = {j = 0}.
 * Reports: violations of H1 (every NE2 element is a top in every direction), H2 (sum_{NE2} P >= e |NE2|), H3 (the rest
 * pays NE3: sum_{EQ} P + (sum_{NE2} P - e|NE2|) + (e-1) dc >= e sum_{NE3} j), minima, and h-profiles of NE classes.
 * Base: q5d5: PAY2 gate on the Q5 residual with the pruned enumeration of trunc3n.
 * Q5: S = <m, m + a_1, ..., m + a_d> (A = {a_i} c [1, m-1]), every generator minimal, q = ceil(c(S)/m) = 5, every
 * factorization of every Apery element (w.r.t. m) of length <= 3.  Then the residues of {0} u A u 2A u 3A cover Z/m,
 * so the DFS of trunc3n (pruning |3A_j' mod m| + C(d+3,3) - C(j+3,3) < m) enumerates a superset of Q5 exactly once.
 * Per S (same computations as q5d4 mode 1): Apery set w by Dijkstra, max/min factorization lengths along the Dijkstra
 * order, sigma_s = w_s - m h_s (h = max length), T = <m, A> by Dijkstra (tau), U = T or not.
 * Asserted: l = 5m - H - N; W = Delta3 - E3; max sigma = 2m + r; on the residual, W(S) - W(T) = PAY2 + (e - e(T)) l(T)
 * with PAY2 := Delta3 + (e-1) dc - e h, h = |T \ U| = sum (sigma_s - tau_s)/m, dc = c(U) - c(T).
 * Reports per m: #Q5, #residual, PAY2 failures and minimum (with S), and the minimum of PAY2 over the adversarial
 * slices h >= 2, dc = 0, and Delta3 <= 3e.
 * usage: ./q5d5 d mlo mhi part np */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXM 160
static int m, d, e, part, np; static long nsplit;
static double maxCTr = 0, maxCr = 0; static int cTrA[16], cRA[16]; static long nCT = 0, minCT = 1L << 40, minCTx = 1L << 40, nDESCfail = 0, minDESC = 1L << 40; static int cTA[16], cTxA[16], dA[16]; static int hardflag; static long nTgtFail, nTgtNEclasses, nTgtSfail, minTgtSlack = 1L << 40, nTgtA1fail; static int tgA[16]; static long nMult, nRay, nRayA1min = 1L << 40, nNotMultA1min = 1L << 40; static int rayflag;
static long nNE2only, nH1only, nHard, minHardA1 = 1L << 40, minHardC = 1L << 40; static int hA1[16], hC[16];
static long nC, minC = 1L << 40, nj2any; static int cA[16];
static long nB1, nB2, nIDNE, nNE3above, nNE3all, minB1 = 1L << 40, minB2 = 1L << 40; static int b1A[16], b2A[16];
static long nA1, nA2, nlo0, minA1 = 1L << 40, minA2 = 1L << 40; static int a1A[16], a2A[16];
static long nQ5, nRes, fail2, sliceN[3], vH1, vH2, vH3, minH2 = 1L << 40, minH3 = 1L << 40, nNE2tot, nNE3tot, nj2; static int h2A[16], h3A[16]; static long min2, slice[3]; static int min2A[16], sliceA[3][16];
static long binom3(int n){ return (long)n * (n - 1) * (n - 2) / 6; }
static void pr(const int *a){ printf("<%d", m); for (int b = 0; b < d; b++) printf(",%d", m + a[b]); printf(">"); }
static void body(const int *a){
  int w[MAXM], done[MAXM], order[MAXM], G[16], ok = 1, lim = 6 * m;
  for (int x = 0; x < m; x++){ w[x] = 1 << 29; done[x] = 0; } w[0] = 0;
  for (int b = 0; b < d; b++) G[b] = m + a[b];
  for (int it = 0; it < m; it++){
    int u = -1; for (int x = 0; x < m; x++) if (!done[x] && (u < 0 || w[x] < w[u])) u = x;
    if (w[u] >= lim) return;
    done[u] = 1; order[it] = u;
    for (int b = 0; b < d; b++){ int v = w[u] + G[b], t = v % m; if (v < w[t]) w[t] = v; }
  }
  for (int b = 0; b < d; b++) if (w[a[b]] != G[b]) return;              /* every generator minimal */
  int r = 0; for (int x = 1; x < m; x++) if (w[x] > w[r]) r = x;
  if (w[r] < 5 * m) return;                                              /* q = 5 (q <= 5 is forced by height <= 3) */
  int hmx[MAXM], hmn[MAXM]; hmx[0] = hmn[0] = 0;
  for (int it = 1; it < m && ok; it++){
    int x = order[it]; hmx[x] = -1; hmn[x] = 99;
    for (int b = 0; b < d; b++){
      int t = ((x - a[b]) % m + m) % m;
      if (w[t] == w[x] - G[b]){
        if (t != 0 && hmx[t] < 0){ ok = 0; break; }
        if (hmx[t] + 1 > hmx[x]) hmx[x] = hmx[t] + 1; if (hmn[t] + 1 < hmn[x]) hmn[x] = hmn[t] + 1;
      }
    }
    if (hmx[x] < 0 || hmx[x] > 3) ok = 0;
  }
  if (!ok) return;
  nQ5++;
  long c = w[r] - m + 1, g = 0; for (int x = 1; x < m; x++) g += w[x] / m;
  long W = (long)e * (c - g) - c; int H = 0, N = 0;
  int sg[MAXM], mxs = 0;
  for (int x = 0; x < m; x++){ sg[x] = w[x] - m * hmx[x]; H += hmx[x]; if (sg[x] > mxs) mxs = sg[x];
    if (sg[x] > r) N++; if (sg[x] > m + r) N++; if (sg[x] > 2 * m + r){ fprintf(stderr, "third threshold\n"); exit(5); } }
  if ((long)e * (5L * m - H - N) - c != W){ fprintf(stderr, "IDENTITY FAILS\n"); exit(6); }
  long D3 = 3L * (e - 1) * m - (long)e * H, rho = 5L * m - c, E3 = (long)e * N - 2L * (e - 1) * m - rho;
  if (D3 < 0){ fprintf(stderr, "CH' FAILS\n"); exit(7); }
  if (D3 - E3 != W){ fprintf(stderr, "W != D3 - E3\n"); exit(8); }
  if (mxs != 2 * m + r){ fprintf(stderr, "c_U != m+r+1\n"); exit(12); }
  if (W < 0){ printf("WILF FAILS "); pr(a); printf("\n"); }
  int tau[MAXM], dn[MAXM];
  for (int x = 0; x < m; x++){ tau[x] = 1 << 29; dn[x] = 0; } tau[0] = 0;
  for (int it = 0; it < m; it++){ int u = -1; for (int x = 0; x < m; x++) if (!dn[x] && (u < 0 || tau[x] < tau[u])) u = x;
    dn[u] = 1; for (int b = 0; b < d; b++){ int v = tau[u] + a[b], t = v % m; if (v < tau[t]) tau[t] = v; } }
  long h = 0; int UeqT = 1;
  for (int x = 0; x < m; x++){ if (tau[x] > sg[x]){ fprintf(stderr, "T > U ?\n"); exit(14); } if (tau[x] < sg[x]){ UeqT = 0; h += (sg[x] - tau[x]) / m; } }
  if (UeqT) return;
  nRes++;
  /* Wilf data of T by membership on [0, 3m] */
  static char inT[4 * MAXM]; int Nn = 3 * m + 2, cT = 0, ellT = 0, eT = 0;
  for (int z = 0; z <= Nn; z++) inT[z] = 0;
  for (int x = 0; x < m; x++) for (int z = tau[x]; z <= Nn; z += m) inT[z] = 1;
  { int lastgap = -1; for (int z = 0; z <= Nn; z++) if (!inT[z]) lastgap = z; cT = lastgap + 1; }
  for (int z = 0; z < cT; z++) ellT += inT[z];
  for (int z = 1; z <= Nn; z++) if (inT[z]){ int dec = 0; for (int y = 1; y < z && !dec; y++) if (inT[y] && inT[z - y]) dec = 1; if (!dec) eT++; }
  long WT = (cT > 0) ? (long)eT * ellT - cT : 0, dc = (m + r + 1) - cT;
  long p2 = D3 + (long)(e - 1) * dc - (long)e * h;
  if (W - WT != p2 + (long)(e - eT) * ellT){ fprintf(stderr, "combined identity FAILS m=%d\n", m); exit(16); }
  hardflag = 0;
  { /* shape of T \ U: all NE tau multiples of mu = min A?  exactly the ray {4mu, ..., K mu}? */
    int mu = a[0]; for (int b = 1; b < d; b++) if (a[b] < mu) mu = a[b];
    int allmult = 1, K = 0, cnt = 0;
    for (int x = 0; x < m; x++) if (tau[x] < sg[x]){ cnt++; if (tau[x] % mu) allmult = 0; else if (tau[x] / mu > K) K = tau[x] / mu; }
    rayflag = 0; if (allmult){ nMult++; if (K >= 4 && cnt == K - 3) { int ok2 = 1; for (int k = 4; k <= K; k++){ int x = (k * mu) % m; if (!(tau[x] == k * mu && tau[x] < sg[x])) ok2 = 0; } if (ok2){ nRay++; rayflag = 1; if (getenv("RAYK") && K >= atoi(getenv("RAYK"))){ printf("RAYEX K=%d mu=%d ", K, mu); pr(a); printf("\n"); } } } }
    else rayflag = -1; }
  { /* tile analysis */
    static int X[MAXM][16]; for (int b = 0; b < d; b++) X[0][b] = 0;
    for (int it = 1; it < m; it++){ int x = order[it], have = 0; int best[16];
      for (int b = 0; b < d; b++){ int t = ((x - a[b]) % m + m) % m;
        if (w[t] == w[x] - G[b] && hmx[t] + 1 == hmx[x]){ int cand[16]; memcpy(cand, X[t], sizeof(int) * d); cand[b]++;
          int bigger = !have; if (have){ for (int q = 0; q < d; q++){ if (cand[q] != best[q]){ bigger = cand[q] > best[q]; break; } } }
          if (bigger){ memcpy(best, cand, sizeof(int) * d); have = 1; } } }
      if (!have){ fprintf(stderr, "no max pred\n"); exit(20); }
      memcpy(X[x], best, sizeof(int) * d); }
    long P[MAXM], D3c = 0, Pne2 = 0, Peq = 0, Jne3 = 0; int nNE2 = 0, nNE3 = 0, h1 = 0;
    for (int s2 = 0; s2 < m; s2++){ P[s2] = 0; int js = (sg[s2] - tau[s2]) / m;
      for (int i = 0; i < d; i++){ int t = (sg[s2] + a[i]) % m; int intop = 1;
        if (hmx[s2] + 1 == hmx[t] && sg[t] == sg[s2] + a[i]){ int same = 1; for (int q = 0; q < d; q++) if (X[t][q] != X[s2][q] + (q == i)) same = 0; if (same) intop = 0; }
        if (intop) P[s2] += (long)(X[s2][i] + 1) * (3 - hmx[s2]);
        else if (js >= 1 && hmx[s2] == 2) h1 = 1; }
      D3c += P[s2];
      if (js >= 1 && hmx[s2] == 2){ nNE2++; Pne2 += P[s2]; if (js != 1){ fprintf(stderr, "NE2 with j != 1\n"); exit(21); } }
      else if (js >= 1 && hmx[s2] == 3){ nNE3++; Jne3 += js; if (js == 2) nj2++; }
      else if (js >= 1){ fprintf(stderr, "NE class with h < 2\n"); exit(22); }
      else Peq += P[s2]; }
    if (D3c != D3){ fprintf(stderr, "column-top form FAILS m=%d (%ld vs %ld)\n", m, D3c, D3); exit(23); }
    nNE2tot += nNE2; nNE3tot += nNE3; if (h1) vH1++; if (nNE3 == 0) nNE2only++; if (h == 1) nH1only++;
    long H2 = Pne2 - (long)e * nNE2, H3 = Peq + H2 + (long)(e - 1) * dc - (long)e * Jne3;
    if (H2 < 0) vH2++; if (H3 < 0) vH3++;
    if (H2 < minH2){ minH2 = H2; memcpy(h2A, a, sizeof(int) * d); } if (H3 < minH3){ minH3 = H3; memcpy(h3A, a, sizeof(int) * d); }
    if (H3 != p2){ fprintf(stderr, "H3 != PAY2 ?\n"); exit(24); }
    { /* TARGET charging: assign each column top (x, i) to the class of sigma(x) + a_i; R(t) = total P assigned to t.
         Test: every NE class t has R(t) >= cost(t), cost = e if tau_t < c_T (low), 1 if high (j = 1 assumed; j >= 2 -> cost e*j). */
      static long R[MAXM]; for (int t = 0; t < m; t++) R[t] = 0;
      long Rsum = 0;
      for (int s2 = 0; s2 < m; s2++) for (int i = 0; i < d; i++){
        int t = (sg[s2] + a[i]) % m; int same = 1; for (int q = 0; q < d; q++) if (X[t][q] != X[s2][q] + (q == i)) same = 0;
        if (!same && hmx[s2] < 3){ long c0 = (long)(X[s2][i] + 1) * (3 - hmx[s2]); R[t] += c0; Rsum += c0; } }
      if (Rsum != D3){ fprintf(stderr, "target sum != Delta3\n"); exit(27); }
      int bad = 0; long slackS = 0;
      for (int t = 0; t < m; t++){ int jt = (sg[t] - tau[t]) / m; if (jt < 1) continue; nTgtNEclasses++;
        long cost = 0; for (int q = 0; q < jt; q++) cost += (tau[t] + q * m < cT) ? e : 1;
        if (R[t] < cost){ nTgtFail++; bad = 1; } slackS += R[t] - cost; }
      if (bad) nTgtSfail++;
      if (slackS < minTgtSlack){ minTgtSlack = slackS; memcpy(tgA, a, sizeof(int) * d); }
    }
    { /* ID-NE: PAY2 = Peq + |NE2| + (e-1) dc - sum_{y in NE3} (e j_y + pi(y)), pi(y) = sum_{i: y - e_i in NE2} y_i.
         B1: dc >= sum_{NE3} j;  B2: Peq + |NE2| >= sum_{NE3} (j_y + pi(y)).  (B1 & B2 => PAY2.) */
      static int cls[MAXM * 4]; long cost = 0, pisum = 0, jsum3 = 0, cstar = 0; int maxtau = 0, nbelow = 0;
      for (int s2 = 0; s2 < m; s2++) if (tau[s2] > maxtau) maxtau = tau[s2];
      for (int s2 = 0; s2 < m; s2++){ int js = (sg[s2] - tau[s2]) / m; if (!(js >= 1 && hmx[s2] == 3)) continue;
        long pi = 0;
        for (int i = 0; i < d; i++) if (X[s2][i] >= 1){ int t = ((sg[s2] - a[i]) % m + m) % m; int jt = (sg[t] - tau[t]) / m;
          int same = 1; for (int q = 0; q < d; q++) if (X[t][q] != X[s2][q] - (q == i)) same = 0;
          if (same && jt >= 1 && hmx[t] == 2) pi += X[s2][i]; }
        cost += (long)e * js + pi; pisum += pi; jsum3 += js; nNE3all++; if (sg[s2] > maxtau) nNE3above++;
        cstar += (sg[s2] > maxtau) ? (long)e * (js - 1) + 1 + pi : (long)e * js + pi; if (js >= 2) nj2any++;
        if (sg[s2] <= maxtau) nbelow++; }
      (void)cls;
      if (Peq + nNE2 + (long)(e - 1) * dc - cost != p2) nIDNE++;
      long B1 = dc - jsum3, B2 = Peq + nNE2 - (jsum3 + pisum);
      if (B1 < 0) nB1++; if (B2 < 0) nB2++;
      { /* C*-eT: Peq + |NE2| >= sum_{NE3 below}(e_T j + pi) + sum_{NE3 above}(e_T (j-1) + 1 + pi); implies DESC = W(S) - W(T) >= 0 */
        long cT2 = 0; for (int s2 = 0; s2 < m; s2++){ int js = (sg[s2] - tau[s2]) / m; if (!(js >= 1 && hmx[s2] == 3)) continue;
          long pi = 0; for (int i = 0; i < d; i++) if (X[s2][i] >= 1){ int t = ((sg[s2] - a[i]) % m + m) % m; int jt = (sg[t] - tau[t]) / m;
            int same = 1; for (int q = 0; q < d; q++) if (X[t][q] != X[s2][q] - (q == i)) same = 0; if (same && jt >= 1 && hmx[t] == 2) pi += X[s2][i]; }
          cT2 += (sg[s2] > maxtau) ? (long)eT * (js - 1) + 1 + pi : (long)eT * js + pi; }
        long CT = Peq + nNE2 - cT2; if (CT < 0) nCT++; if (CT < minCT){ minCT = CT; memcpy(cTA, a, sizeof(int) * d); }
        if (Peq + nNE2 > 0){ double rt = (double)cT2 / (Peq + nNE2), rc = (double)cstar / (Peq + nNE2);
          if (rt > maxCTr){ maxCTr = rt; memcpy(cTrA, a, sizeof(int) * d); } if (rc > maxCr){ maxCr = rc; memcpy(cRA, a, sizeof(int) * d); } }
        long desc = W - WT; if (desc < 0) nDESCfail++; if (desc < minDESC){ minDESC = desc; memcpy(dA, a, sizeof(int) * d); } }
      { long C = Peq + nNE2 - cstar; if (C < 0) nC++; if (C < minC){ minC = C; memcpy(cA, a, sizeof(int) * d); }   /* C*: Peq + |NE2| >= cstar */
        if (nbelow >= 2){ nHard++; if (C < minHardC){ minHardC = C; memcpy(hC, a, sizeof(int) * d); } hardflag = 1; } }
      if (B1 < minB1){ minB1 = B1; memcpy(b1A, a, sizeof(int) * d); } if (B2 < minB2){ minB2 = B2; memcpy(b2A, a, sizeof(int) * d); } }
    { /* split T \ U at c(T): h_lo below, h_hi in [c_T, c_U); u' = |U n [c_T, c_U)|; dc = h_hi + u' */
      long hlo = 0, hhi = 0, up = 0; int cU = m + r + 1;
      for (int z = 0; z < cU; z++){ int inU = (z >= sg[z % m]); if (inT[z] && !inU){ if (z < cT) hlo++; else hhi++; } if (z >= cT && inU) up++; }
      if (hlo + hhi != h || hhi + up != dc){ fprintf(stderr, "split FAILS m=%d\n", m); exit(25); }
      if (D3 + (long)(e - 1) * up - hhi - (long)e * hlo != p2){ fprintf(stderr, "split PAY2 FAILS\n"); exit(26); }
      long A1 = D3 - hhi - (long)e * hlo, A2 = D3 - (long)e * hlo;          /* A1: Delta3 >= h_hi + e h_lo;  A2: Delta3 >= e h_lo */
      if (A1 < 0) nA1++; if (A2 < 0) nA2++; if (hlo == 0) nlo0++;
      if (A1 < minA1){ minA1 = A1; memcpy(a1A, a, sizeof(int) * d); } if (A2 < minA2){ minA2 = A2; memcpy(a2A, a, sizeof(int) * d); }
      if (hardflag && A1 < minHardA1){ minHardA1 = A1; memcpy(hA1, a, sizeof(int) * d); }
      if (rayflag == 1 && A1 < nRayA1min) nRayA1min = A1; if (rayflag == -1 && A1 < nNotMultA1min) nNotMultA1min = A1;
      if (getenv("Q5VERB")) printf("SPLIT hlo=%ld hhi=%ld u'=%ld\n", hlo, hhi, up);
      if (getenv("Q5DUMP")){ int n2eq = 0, n3eq = 0; for (int s2 = 0; s2 < m; s2++) if (sg[s2] == tau[s2]){ if (hmx[s2] == 2) n2eq++; if (hmx[s2] == 3) n3eq++; }
        long DEQ = 2L * d * (d + 1) + (long)(d - 2) * n2eq - 3L * n3eq;
        if (DEQ != D3 - (long)(d - 2) * nNE2 + 3L * nNE3){ fprintf(stderr, "DEQ identity FAILS\n"); exit(28); }
        printf("DUMP %d %d %ld %ld %ld %ld %ld %d %d %ld %d %d %d %d", m, e, D3, DEQ, h, hlo, hhi, nNE2, nNE3, dc, n2eq, n3eq, cT, r);
        for (int b = 0; b < d; b++) printf(" %d", a[b]); printf("\n"); } }
    if (getenv("Q5VERB")){ long outc = 0, nout = 0; for (int s2 = 0; s2 < m; s2++){ int js = (sg[s2] - tau[s2]) / m; if (js >= 1 && hmx[s2] == 2)
          for (int i = 0; i < d; i++){ int t = (sg[s2] + a[i]) % m; int same = 1; for (int q = 0; q < d; q++) if (X[t][q] != X[s2][q] + (q == i)) same = 0; if (same){ nout++; outc += X[s2][i] + 1; } } }
      printf("RES "); pr(a); printf(" e=%d r=%d NE2=%d NE3=%d out=%ld outcost=%ld Peq=%ld Pne2=%ld dc=%ld (e-1)dc=%ld D3=%ld PAY2=%ld cT=%d maxtau=%d\n", e, r, nNE2, nNE3, nout, outc, Peq, Pne2, dc, (long)(e - 1) * dc, D3, p2, cT, cT + m - 1); }
  }
  if (p2 < 0){ fail2++; printf("PAY2 FAILS %ld at ", p2); pr(a); printf(" h=%ld dc=%ld D3=%ld W=%ld WT=%ld\n", h, dc, D3, W, WT); }
  if (nRes == 1 || p2 < min2){ min2 = p2; memcpy(min2A, a, sizeof(int) * d); }
  int sl[3] = { h >= 2, dc == 0, D3 <= 3L * e };
  for (int k = 0; k < 3; k++) if (sl[k]){ if (sliceN[k] == 0 || p2 < slice[k]){ slice[k] = p2; memcpy(sliceA[k], a, sizeof(int) * d); } sliceN[k]++; }
}
static void dfs(int k, int *a, char *S1, char *S2, char *S3, int cnt3){
  if (k == 2 && k < d && (nsplit++ % np != part)) return;
  if (k == d){ if (cnt3 == m && (d > 2 || (nsplit++ % np == part))) body(a); return; }
  for (int x = (k ? a[k - 1] + 1 : 1); x <= m - 1 - (d - 1 - k); x++){
    char T1[MAXM], T2[MAXM], T3[MAXM];
    memcpy(T1, S1, m); memcpy(T2, S2, m); memcpy(T3, S3, m);
    T1[x] = 1;
    for (int s = 0; s < m; s++) if (T1[s]) T2[(s + x) % m] = 1;
    int c3 = 0;
    for (int s = 0; s < m; s++) if (T2[s]) T3[(s + x) % m] = 1;
    for (int s = 0; s < m; s++) c3 += T3[s];
    if (c3 + binom3(d + 3) - binom3(k + 4) < m) continue;
    a[k] = x; dfs(k + 1, a, T1, T2, T3, c3);
  }
}
int main(int argc, char **argv){
  if (argc < 6){ fprintf(stderr, "usage: ./q5d5 d mlo mhi part np\n"); return 1; }
  d = atoi(argv[1]); int mlo = atoi(argv[2]), mhi = atoi(argv[3]); part = atoi(argv[4]); np = atoi(argv[5]); e = d + 1;
  if (mhi >= MAXM || d > 15 || d < 2){ fprintf(stderr, "bad parameters\n"); return 1; }
  for (m = mlo; m <= mhi; m++){
    if (m - 1 < d) continue;
    nQ5 = nRes = fail2 = 0; nsplit = 0; for (int k = 0; k < 3; k++) sliceN[k] = 0;
    int a[16]; char S1[MAXM] = {0}, S2[MAXM] = {0}, S3[MAXM] = {0}; S1[0] = S2[0] = S3[0] = 1;
    dfs(0, a, S1, S2, S3, 1);
    printf("SUMMARY d=%d e=%d m=%d part=%d/%d Q5=%ld residual=%ld PAY2fail=%ld", d, e, m, part, np, nQ5, nRes, fail2);
    if (nRes){ printf(" minPAY2=%ld at ", min2); pr(min2A);
      const char *nm[3] = { "h>=2", "dc=0", "D3<=3e" };
      for (int k = 0; k < 3; k++){ printf(" | %s: n=%ld", nm[k], sliceN[k]); if (sliceN[k]){ printf(" min=%ld at ", slice[k]); pr(sliceA[k]); } } }
    printf(" | NE2=%ld NE3=%ld (j=2: %ld) H1viol=%ld H2viol=%ld minH2=%ld at ", nNE2tot, nNE3tot, nj2, vH1, vH2, minH2); pr(h2A);
    printf(" H3viol=%ld | A1fail=%ld minA1=%ld at ", vH3, nA1, minA1); pr(a1A); printf(" A2fail=%ld minA2=%ld hlo0=%ld", nA2, minA2, nlo0);
    nA1 = nA2 = nlo0 = 0; minA1 = minA2 = 1L << 40;
    printf(" | IDNEfail=%ld B1fail=%ld minB1=%ld at ", nIDNE, nB1, minB1); pr(b1A); printf(" B2fail=%ld minB2=%ld at ", nB2, minB2); pr(b2A);
    printf(" NE3above=%ld/%ld Cfail=%ld minC=%ld at ", nNE3above, nNE3all, nC, minC); pr(cA); printf(" j2any=%ld", nj2any);
    printf(" NE2only=%ld h1=%ld hard(>=2 NE3 below max tau)=%ld", nNE2only, nH1only, nHard);
    printf(" CstarT: fail=%ld min=%ld at ", nCT, minCT); pr(cTA); printf(" DESC: fail=%ld min=%ld at ", nDESCfail, minDESC); pr(dA);
    printf(" ratio cost/(Peq+|NE2|): C* max=%.4f at ", maxCr); pr(cRA); printf(" CstarT max=%.4f at ", maxCTr); pr(cTrA);
    nCT = nDESCfail = 0; minCT = minDESC = 1L << 40; maxCTr = maxCr = 0;
    printf(" TGT: NEclasses=%ld classfail=%ld Sfail=%ld minNEslack=%ld at ", nTgtNEclasses, nTgtFail, nTgtSfail, minTgtSlack); pr(tgA);
    nTgtNEclasses = nTgtFail = nTgtSfail = 0; minTgtSlack = 1L << 40;
    if (nHard){ printf(" hardminA1=%ld at ", minHardA1); pr(hA1); printf(" hardminC=%ld at ", minHardC); pr(hC); }
    nHard = 0; minHardA1 = minHardC = 1L << 40;
    printf(" allNEmultofmu=%ld ray=%ld rayminA1=%ld notmultminA1=%ld", nMult, nRay, nRayA1min, nNotMultA1min); nMult = nRay = 0; nRayA1min = nNotMultA1min = 1L << 40;
    nC = nj2any = 0; minC = 1L << 40; nNE2only = nH1only = 0;
    nIDNE = nB1 = nB2 = nNE3above = nNE3all = 0; minB1 = minB2 = 1L << 40;
    printf("\n"); fflush(stdout); nNE2tot = nNE3tot = nj2 = vH1 = vH2 = vH3 = 0; minH2 = minH3 = 1L << 40;
  }
  return 0;
}
