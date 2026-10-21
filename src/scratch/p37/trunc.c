/* trunc: test TRUNC (lead, 2026-10-21).  A c [1, m-1], A' = A u {0}, U_k = kA' + mN (kA' = sums of at most k elements
 * of A, as integers).  For every k >= h(A) (least k with kA' covering Z/m): e = |A| + 1, test e*l(U_k) >= c(U_k),
 * c(U_k) = max_s sigma_s - m + 1 (sigma_s = least element of kA' in class s), l = c - sum floor(sigma_s/m).
 * Exhaustive over all A with |A| = d for m in [mlo, mhi], k = h .. h + kextra.  usage: ./trunc d mlo mhi kextra part np
 * Also MONO: W_e(U_k) >= W_e(T) for T = <m, A> = U_infinity (e = |A| + 1), for every tested k. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXM 128
int main(int argc, char **argv){
  int d = atoi(argv[1]), mlo = atoi(argv[2]), mhi = atoi(argv[3]), kx = atoi(argv[4]), part = atoi(argv[5]), np = atoi(argv[6]);
  for (int m = mlo; m <= mhi; m++){
    long tested = 0, fails = 0, ncomb = 0, minsl = 1L << 40, monofail = 0, minmono = 1L << 40, nstrict = 0; int bestA[16] = {0}, bestk = 0;
    int a[16]; for (int i = 0; i < d; i++) a[i] = i + 1;
    if (d > m - 1) continue;
    while (1){
      if (ncomb++ % np == part){
        /* sig[s] after k rounds: least element of kA' in class s (INF if none) */
        int sig[MAXM], nw[MAXM]; for (int s = 0; s < m; s++) sig[s] = 1 << 29; sig[0] = 0;
        int k = 0, covered = 1, h = -1;
        for (k = 1; k <= 3 * m && h < 0; k++){
          memcpy(nw, sig, sizeof(int) * m);
          for (int s = 0; s < m; s++) if (sig[s] < (1 << 29)) for (int i = 0; i < d; i++){ int v = sig[s] + a[i], t = v % m; if (v < nw[t]) nw[t] = v; }
          memcpy(sig, nw, sizeof(int) * m);
          covered = 1; for (int s = 0; s < m; s++) if (sig[s] >= (1 << 29)) covered = 0;
          if (covered) h = k;
          if (k > m) break;
        }
        if (h > 0){
          /* T = U_infinity: Dijkstra over residues */
          long WeT; { int tau[MAXM], dn[MAXM]; for (int x = 0; x < m; x++){ tau[x] = 1 << 29; dn[x] = 0; } tau[0] = 0;
            for (int it = 0; it < m; it++){ int u = -1; for (int x = 0; x < m; x++) if (!dn[x] && (u < 0 || tau[x] < tau[u])) u = x; dn[u] = 1;
              for (int i = 0; i < d; i++){ int v = tau[u] + a[i], t = v % m; if (v < tau[t]) tau[t] = v; } }
            int MT = 0; long gT = 0; for (int x = 0; x < m; x++){ if (tau[x] > MT) MT = tau[x]; gT += tau[x] / m; }
            long cT = MT - m + 1; if (cT < 0) cT = 0; WeT = (long)(d + 1) * (cT - gT) - cT; }
          for (int kk = h; kk <= h + kx; kk++){
            if (kk > h){ memcpy(nw, sig, sizeof(int) * m);
              for (int s = 0; s < m; s++) for (int i = 0; i < d; i++){ int v = sig[s] + a[i], t = v % m; if (v < nw[t]) nw[t] = v; }
              memcpy(sig, nw, sizeof(int) * m); }
            int M = 0; long g = 0; for (int s = 0; s < m; s++){ if (sig[s] > M) M = sig[s]; g += sig[s] / m; }
            long c = M - m + 1; if (c < 0) c = 0; long l = c - g; long sl = (long)(d + 1) * l - c;
            tested++; if (sl < 0){ fails++; if (fails <= 3){ printf("TRUNC FAIL m=%d k=%d h=%d slack=%ld c=%ld l=%ld A={", m, kk, h, sl, c, l); for (int i = 0; i < d; i++) printf("%s%d", i ? "," : "", a[i]); printf("}\n"); } }
            if (sl < minsl){ minsl = sl; memcpy(bestA, a, sizeof a); bestk = kk; }
            { long dm = sl - WeT; if (dm < minmono) minmono = dm; if (dm < 0){ monofail++; if (monofail <= 3){ printf("MONO FAIL m=%d k=%d h=%d We(U)=%ld We(T)=%ld A={", m, kk, h, sl, WeT); for (int i = 0; i < d; i++) printf("%s%d", i ? "," : "", a[i]); printf("}\n"); } } else if (dm > 0) nstrict++; }
          }
        }
      }
      int i = d - 1; while (i >= 0 && a[i] == m - d + i) i--; if (i < 0) break; a[i]++; for (int j = i + 1; j < d; j++) a[j] = a[j - 1] + 1;
    }
    printf("d=%d m=%d tested=%ld fails=%ld MONOfail=%ld minMONO=%ld strict=%ld minslack=%ld at k=%d A={", d, m, tested, fails, monofail, minmono, nstrict, minsl, bestk);
    for (int i = 0; i < d; i++) printf("%s%d", i ? "," : "", bestA[i]); printf("}\n"); fflush(stdout);
  }
  return 0;
}
