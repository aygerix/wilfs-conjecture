/* Adversarial search for BANDWILF / GBW'' (lead, 2026-10-20).
 * BANDWILF(J): Phi_J = e*sum_{j<J} H_j - J*H_J >= 0, H_j = #{i : k_i <= j} (Kunz), 1 <= J <= q.
 * GBW''(N):    e*|S n [0,N)| - sum_{z in S n [N,N+m)} floor(z/m) >= 0, 0 <= N <= c   (tested only when e >= emin).
 * Objective (mode 0): minimize min_J Phi_J/(J*H_J);  (mode 1): minimize min_N GBW''(N)/(rhs).  Prints any failure.
 * usage: ./bwanneal mode seed mlo mhi dlo dhi kmax iters emin */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MM 400
#define DD 40
static int m, d, gen[DD], w[MM], kmax;
static unsigned long long rs;
static unsigned rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static int apery(void){
  static int done[MM]; for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){
    int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return 0; done[b] = 1;
    for (int a = 0; a < d; a++){ int j = (b + gen[a]) % m, v = w[b] + gen[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
  return 1; }
static int mode, emin;
static double eval(int pr, int *eo, int *qo){
  if (!apery()) return 1e9;
  int e = 1; for (int i = 1; i < m; i++){ int x = w[i], dec = 0; for (int j = 1; j < m && !dec; j++){ int y = w[j]; if (y < x){ int z = x - y; if (w[z % m] <= z) dec = 1; } } if (!dec) e++; }
  long M = 0; for (int i = 0; i < m; i++) if (w[i] > M) M = w[i];
  long c = M - m + 1; int q = (int)((c + m - 1) / m); *eo = e; *qo = q;
  double best = 1e9;
  if (mode == 0){ if (e < emin) return 1e9; long H[200]; for (int J = 0; J <= q; J++){ H[J] = 0; for (int i = 0; i < m; i++) if (w[i] / m <= J) H[J]++; }
    long s = 0; for (int J = 1; J <= q; J++){ s += H[J - 1]; long phi = (long)e * s - (long)J * H[J]; double r = (double)phi / ((double)J * H[J]);
      if (phi < 0 && pr) printf("BANDWILF FAIL J=%d q=%d phi=%ld\n", J, q, phi); if (r < best) best = r; } }
  else { if (e < emin) return 1e9; long pre = 0; /* count S below N via residues */
    for (long N = 0; N <= c; N++){ if (N > 0){ long z = N - 1; if (w[z % m] <= z) pre++; } long rhs = 0;
      for (long z = N; z < N + m; z++) if (w[z % m] <= z) rhs += z / m;
      if (rhs == 0) continue; long dd = (long)e * pre - rhs; double r = (double)dd / rhs; if (dd < 0 && pr) printf("GBW'' FAIL N=%ld c=%ld\n", N, c); if (r < best) best = r; } }
  return best; }
int main(int argc, char **argv){
  mode = atoi(argv[1]); rs = 88172645463325252ULL ^ (unsigned long long)atoi(argv[2]) * 2654435761ULL;
  int mlo = atoi(argv[3]), mhi = atoi(argv[4]), dlo = atoi(argv[5]), dhi = atoi(argv[6]); kmax = atoi(argv[7]); long iters = atol(argv[8]); emin = atoi(argv[9]);
  double gbest = 1e9; long fails = 0;
  for (long restart = 0; ; restart++){
    m = mlo + rnd() % (mhi - mlo + 1); d = dlo + rnd() % (dhi - dlo + 1); if (d > DD) d = DD;
    for (int a = 0; a < d; a++) gen[a] = m + 1 + rnd() % ((kmax - 1) * m);
    int e, q; double cur = eval(0, &e, &q); double T = 0.05;
    for (long it = 0; it < iters; it++){
      int a = rnd() % d, old = gen[a]; int mv = rnd() % 3;
      if (mv == 0) gen[a] = m + 1 + rnd() % ((kmax - 1) * m); else if (mv == 1){ int dl = (int)(rnd() % 7) - 3; gen[a] += dl; if (gen[a] <= m) gen[a] = m + 1; if (gen[a] > kmax * m) gen[a] = kmax * m; } else { gen[a] += (rnd() % 2 ? m : -m); if (gen[a] <= m || gen[a] > kmax * m) gen[a] = old; }
      int e2, q2; double v = eval(0, &e2, &q2);
      if (v <= cur || (double)(rnd() % 100000) / 100000.0 < __builtin_exp((cur - v) / T)) cur = v; else gen[a] = old;
      T *= 0.9995; if (T < 1e-4) T = 1e-4;
      if (cur < gbest){ gbest = cur; eval(0, &e2, &q2); printf("best %.5f m=%d e=%d q=%d gens:", cur, m, e2, q2); for (int t = 0; t < d; t++) printf(" %d", gen[t]); printf("\n"); fflush(stdout); }
      if (cur < 0){ fails++; eval(1, &e2, &q2); }
    }
    if (restart % 20 == 0){ printf("restart %ld done (m=%d), global best %.5f, fails %ld\n", restart, m, gbest, fails); fflush(stdout); }
  }
}
