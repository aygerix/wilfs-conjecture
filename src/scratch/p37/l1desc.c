/* l1desc: residue descent on the level-1 class (DKM Problem 1.8 class), all heights (lead, 2026-10-21).
 * S = <m, m + a : a in A>, A c [1, m-1], |A| = d (all subsets; S with gcd != 1 are skipped by the Apery check).
 * kappa = max factorization length (level 1), sigma_s = w_s - m kappa_s, U = {sigma} + mN, T = <m, A>.
 * Per (depth q, height K*) bucket: #S, #U=T, #U=T with Delta' >= 0 (descent applies), #U=T with Delta' < 0, and on the
 * rest the min of W(S) - W(T) (RD) with e(T).  Asserts ID-U: W = Delta' + W_e(U).  usage: ./l1desc d mlo mhi part np */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXM 100
#define QMAX 40
#define KMAX 40
static long cnt[QMAX][KMAX], cUT[QMAX][KMAX], cDesc[QMAX][KMAX], cNeg[QMAX][KMAX], minRD[QMAX][KMAX];
static int eT_of(int *tau, int m, int *cT, long *gT){
  int mx = 0; long gg = 0; for (int x = 0; x < m; x++){ if (tau[x] > mx) mx = tau[x]; gg += tau[x] / m; }
  *gT = gg; *cT = mx - m + 1; if (*cT < 0) *cT = 0; if (*cT == 0) return 1;
  static unsigned char in[8 * MAXM]; int N = mx + m + 1; for (int z = 0; z <= N; z++) in[z] = 0;
  for (int x = 0; x < m; x++) for (int z = tau[x]; z <= N; z += m) in[z] = 1;
  int e = 0; for (int z = 1; z <= N; z++) if (in[z]){ int dec = 0; for (int y = 1; y <= z / 2 && !dec; y++) if (in[y] && in[z - y]) dec = 1; if (!dec) e++; }
  return e;
}
int main(int argc, char **argv){
  int d = atoi(argv[1]), mlo = atoi(argv[2]), mhi = atoi(argv[3]), part = atoi(argv[4]), np = atoi(argv[5]);
  for (int q = 0; q < QMAX; q++) for (int k = 0; k < KMAX; k++) minRD[q][k] = 1L << 40;
  long ncomb = 0, tot = 0;
  for (int m = mlo; m <= mhi; m++){
    int a[32]; if (d > m - 1) continue; for (int i = 0; i < d; i++) a[i] = i + 1;
    while (1){
      if (ncomb++ % np == part){
        int w[MAXM], dn[MAXM], ord[MAXM], ok = 1;
        for (int x = 0; x < m; x++){ w[x] = 1 << 29; dn[x] = 0; } w[0] = 0;
        for (int it = 0; it < m; it++){ int u = -1; for (int x = 0; x < m; x++) if (!dn[x] && (u < 0 || w[x] < w[u])) u = x;
          if (w[u] >= (1 << 29)){ ok = 0; break; } dn[u] = 1; ord[it] = u;
          for (int b = 0; b < d; b++){ int v = w[u] + m + a[b], t = v % m; if (v < w[t]) w[t] = v; } }
        if (ok){
          int kap[MAXM]; kap[0] = 0; int Ks = 0, M = 0, r = 0; long H = 0, gS = 0;
          for (int it = 1; it < m; it++){ int x = ord[it]; kap[x] = -1;
            for (int b = 0; b < d; b++){ int g = m + a[b], t = ((x - g) % m + m) % m; if (w[t] == w[x] - g && kap[t] >= 0 && kap[t] + 1 > kap[x]) kap[x] = kap[t] + 1; }
            if (kap[x] > Ks) Ks = kap[x]; H += kap[x]; if (w[x] > M){ M = w[x]; r = x; } }
          for (int x = 0; x < m; x++) gS += w[x] / m;
          long c = M - m + 1, W = (long)(d + 1) * (c - gS) - c; int q = (int)((c + m - 1) / m);
          int sg[MAXM], Mu = 0; long gU = 0; for (int x = 0; x < m; x++){ sg[x] = w[x] - m * kap[x]; if (sg[x] > Mu) Mu = sg[x]; gU += sg[x] / m; }
          long cU = Mu - m + 1, WeU = (long)(d + 1) * (cU - gU) - cU, Dp = (long)d * (M - Mu) - (long)(d + 1) * H;
          if (W != Dp + WeU){ fprintf(stderr, "ID-U FAILS m=%d\n", m); return 3; }
          int tau[MAXM]; for (int x = 0; x < m; x++){ tau[x] = 1 << 29; dn[x] = 0; } tau[0] = 0;
          for (int it = 0; it < m; it++){ int u = -1; for (int x = 0; x < m; x++) if (!dn[x] && (u < 0 || tau[x] < tau[u])) u = x; dn[u] = 1;
            for (int b = 0; b < d; b++){ int v = tau[u] + a[b], t = v % m; if (v < tau[t]) tau[t] = v; } }
          int UT = 1; for (int x = 0; x < m; x++) if (sg[x] != tau[x]) UT = 0;
          if (q >= QMAX) q = QMAX - 1; int K = Ks >= KMAX ? KMAX - 1 : Ks;
          cnt[q][K]++; tot++;
          if (UT){ cUT[q][K]++; if (Dp >= 0) cDesc[q][K]++; else cNeg[q][K]++; }
          if (!UT || Dp < 0){ int cT; long gT; int eT = eT_of(tau, m, &cT, &gT); long WT = (cT == 0) ? 0 : (long)eT * (cT - gT) - cT;
            if (W - WT < minRD[q][K]) minRD[q][K] = W - WT; }
        }
      }
      int i = d - 1; while (i >= 0 && a[i] == m - d + i) i--; if (i < 0) break; a[i]++; for (int j = i + 1; j < d; j++) a[j] = a[j - 1] + 1;
    }
  }
  printf("d=%d m=%d..%d part %d/%d: total S=%ld\n", d, mlo, mhi, part, np, tot);
  for (int q = 0; q < QMAX; q++) for (int k = 0; k < KMAX; k++) if (cnt[q][k])
    printf("  q=%d K*=%d: S=%ld U=T %ld descent(D'>=0) %ld U=T&D'<0 %ld | rest: min W-W(T) %ld\n", q, k, cnt[q][k], cUT[q][k], cDesc[q][k], cNeg[q][k],
           (cnt[q][k] - cDesc[q][k]) ? minRD[q][k] : 0);
  return 0;
}
