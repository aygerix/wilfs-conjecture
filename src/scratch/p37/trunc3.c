/* trunc3: adversarial test of unrestricted TRUNC3 (lead, 2026-10-21).
 * A c [1, m-1], A' = A u {0}, e = |A| + 1, sigma_s = min(3A' n (s + mZ)) (3A' = sums of at most 3 elements of A, as
 * integers), U = {sigma_s} + mN.  Hypothesis: 3A' covers Z/m.  TRUNC3: e*l(U) >= c(U), c(U) = max sigma - m + 1 (0 if
 * max sigma < m), l(U) = c(U) - sum floor(sigma_s / m).
 * mode E: ./trunc3 E d mlo mhi part np           exhaustive over all A with |A| = d
 * mode H: ./trunc3 H d mlo mhi restarts steps seed   hill climbing on the ratio e*l/c (moves: replace one element)
 * mode O: as H, restricted to the open regime c(U) > 4 min A (proposals leaving the regime are rejected)
 * Reports per m: #covering A, failures, min slack e*l - c, min ratio e*l/c, with the minimizing A.
 * Mode E also buckets the min ratio by t = ceil(c / mu), mu = min(A u {m}) (Kaplan regime t <= 2), printed at the end. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXM 512
static int m, d; static double brat[64]; static int bA[64][64], bm[64]; static long bcc[64], bll[64];
/* returns 0 if not covering; else fills c, l */
static int eval(const int *a, long *c, long *l){
  static int sig[MAXM], nw[MAXM];
  for (int s = 0; s < m; s++) sig[s] = 1 << 29; sig[0] = 0;
  for (int round = 0; round < 3; round++){
    memcpy(nw, sig, sizeof(int) * m);
    for (int s = 0; s < m; s++) if (sig[s] < (1 << 29)) for (int i = 0; i < d; i++){ int v = sig[s] + a[i], t = v % m; if (v < nw[t]) nw[t] = v; }
    memcpy(sig, nw, sizeof(int) * m);
  }
  int M = 0; long g = 0;
  for (int s = 0; s < m; s++){ if (sig[s] >= (1 << 29)) return 0; if (sig[s] > M) M = sig[s]; g += sig[s] / m; }
  long cc = M - m + 1; if (cc < 0) cc = 0;
  *c = cc; *l = cc - g; return 1;
}
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int cmpint(const void *x, const void *y){ return *(const int *)x - *(const int *)y; }
int main(int argc, char **argv){
  char mode = argv[1][0]; d = atoi(argv[2]); int mlo = atoi(argv[3]), mhi = atoi(argv[4]);
  int e = d + 1; for (int t = 0; t < 64; t++) brat[t] = 1e18;
  for (m = mlo; m <= mhi; m++){
    if (d > m - 1) continue;
    long ncov = 0, fails = 0, minsl = 1L << 40; double minrat = 1e18; int bestA[64] = {0}, ratA[64] = {0}; long bc = 0, bl = 0, rc = 0, rl = 0;
    int a[64];
    if (mode == 'E'){
      int part = atoi(argv[5]), np = atoi(argv[6]); long ncomb = 0;
      for (int i = 0; i < d; i++) a[i] = i + 1;
      while (1){
        if (ncomb++ % np == part){
          long c, l;
          if (eval(a, &c, &l)){ ncov++;
            if (c > 0){ long sl = (long)e * l - c; double rt = (double)e * l / c;
              { int mu = a[0] < m ? a[0] : m; int t = (int)((c + mu - 1) / mu); if (t > 63) t = 63;
                if (rt < brat[t]){ brat[t] = rt; memcpy(bA[t], a, sizeof(int) * d); bm[t] = m; bcc[t] = c; bll[t] = l; } }
              if (sl < 0) fails++;
              if (sl < minsl){ minsl = sl; memcpy(bestA, a, sizeof a); bc = c; bl = l; }
              if (rt < minrat){ minrat = rt; memcpy(ratA, a, sizeof a); rc = c; rl = l; } } }
        }
        int i = d - 1; while (i >= 0 && a[i] == m - d + i) i--; if (i < 0) break; a[i]++; for (int j = i + 1; j < d; j++) a[j] = a[j - 1] + 1;
      }
    } else {
      int restarts = atoi(argv[5]), steps = atoi(argv[6]); rs ^= (unsigned long long)atoi(argv[7]) * 2654435761ULL + m;
      for (int rr = 0; rr < restarts; rr++){
        /* random covering start */
        long c, l; int tries = 0, ok = 0;
        while (tries++ < 2000){
          char used[MAXM] = {0}; for (int i = 0; i < d; i++){ int x; do x = 1 + rnd() % (m - 1); while (used[x]); used[x] = 1; a[i] = x; }
          if (eval(a, &c, &l) && c > 0){ int mu0 = m; for (int j = 0; j < d; j++) if (a[j] < mu0) mu0 = a[j];
            if (mode == 'O' && c <= 4L * mu0) continue; ok = 1; break; }
        }
        if (!ok) continue;
        ncov++;
        double cur = (double)e * l / c;
        for (int st = 0; st < steps; st++){
          int b[64]; memcpy(b, a, sizeof b); int i = rnd() % d, x;
          int tries2 = 0; do { x = (rnd() & 1) ? 1 + rnd() % (m - 1) : b[i] + (int)(rnd() % 7) - 3; tries2++; } while ((x < 1 || x > m - 1) && tries2 < 50);
          if (x < 1 || x > m - 1) continue;
          int dup = 0; for (int j = 0; j < d; j++) if (j != i && b[j] == x) dup = 1; if (dup) continue;
          b[i] = x; long c2, l2;
          if (!eval(b, &c2, &l2) || c2 == 0) continue;
          if (mode == 'O'){ int mu1 = m; for (int j = 0; j < d; j++) if (b[j] < mu1) mu1 = b[j]; if (c2 <= 4L * mu1) continue; }
          double nr = (double)e * l2 / c2;
          if (nr <= cur){ memcpy(a, b, sizeof a); cur = nr; c = c2; l = l2; }
        }
        long sl = (long)e * l - c; if (sl < 0) fails++;
        int srt[64]; memcpy(srt, a, sizeof srt); qsort(srt, d, sizeof(int), cmpint);
        if (sl < minsl){ minsl = sl; memcpy(bestA, srt, sizeof srt); bc = c; bl = l; }
        if (cur < minrat){ minrat = cur; memcpy(ratA, srt, sizeof srt); rc = c; rl = l; }
      }
    }
    if (ncov == 0) continue;
    printf("%c d=%d e=%d m=%d covering=%ld FAILS=%ld minslack=%ld (c=%ld l=%ld) A={", mode, d, e, m, ncov, fails, minsl, bc, bl);
    for (int i = 0; i < d; i++) printf("%s%d", i ? "," : "", bestA[i]);
    printf("} minratio=%.4f (c=%ld l=%ld) A={", minrat, rc, rl);
    for (int i = 0; i < d; i++) printf("%s%d", i ? "," : "", ratA[i]); printf("}\n"); fflush(stdout);
  }
  if (mode == 'E') for (int t = 1; t < 64; t++) if (brat[t] < 1e17){ printf("BUCKET ceil(c/mu)=%d min ratio %.4f at m=%d c=%ld l=%ld A={", t, brat[t], bm[t], bcc[t], bll[t]);
      for (int i = 0; i < d; i++) printf("%s%d", i ? "," : "", bA[t][i]); printf("}\n"); }
  return 0;
}
