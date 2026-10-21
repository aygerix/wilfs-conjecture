/* q5d5: PAY2 gate on the Q5 residual with the pruned enumeration of trunc3n (lead, 2026-10-21).
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
static long nQ5, nRes, fail2, sliceN[3]; static long minD3all = 1L << 40, minD3eq = 1L << 40; static int mdA[16], mdeA[16]; static long min2, slice[3]; static int min2A[16], sliceA[3][16];
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
  if (D3 < minD3all){ minD3all = D3; memcpy(mdA, a, sizeof(int) * d); }
  if (UeqT){ if (D3 < minD3eq){ minD3eq = D3; memcpy(mdeA, a, sizeof(int) * d); } return; }
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
    if (nQ5){ printf(" minD3(U=T)=%ld at ", minD3eq); pr(mdeA); } minD3all = minD3eq = 1L << 40;
    if (nRes){ printf(" minPAY2=%ld at ", min2); pr(min2A);
      const char *nm[3] = { "h>=2", "dc=0", "D3<=3e" };
      for (int k = 0; k < 3; k++){ printf(" | %s: n=%ld", nm[k], sliceN[k]); if (sliceN[k]){ printf(" min=%ld at ", slice[k]); pr(sliceA[k]); } } }
    printf("\n"); fflush(stdout);
  }
  return 0;
}
