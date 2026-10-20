/* genM: Conjecture M (inside matching of the carry deficit) for GENERAL numerical semigroups (lead, 2026-10-20).
 * S = <m, n_1..n_k> (n_i in (m, Gm)), minimal generators extracted.  Ap(S,m), orders (max # minimal generators), levels,
 * carry t = level - order.  Power tokens (u, a, kk), 2 <= kk <= top(u) (top = q if r(u) < h else q-1), kk > ord(u);
 * used tokens from chosen reps (parent pointers: first generator index attaining max order).
 * Flow: source -> carried v (cap t(v)) -> inside supply -> sink.  Inside supply of v: unused tokens whose first coordinate is an
 * UNCARRIED proper sub-sum of rep(v) (cap 1), and spare(u) = #unused(u) - (e-1) t(u) for CARRIED proper sub-sums u and u = v.
 * deficit = sum t(v) - maxflow.  (M <=> deficit = 0; M implies Wilf.)
 * usage: ./genM rnd seed mlo mhi kmin kmax G N Qmax      (random sampling, reports any deficit)
 *        ./genM ann seed mlo mhi kmin kmax G iters restarts Qmax   (anneal min W/(T_c+1) - 1000*deficit, e >= 3) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define MXM 160
#define MXQ 14
#define MXK 16
static double urand(void){ return rand() / (RAND_MAX + 1.0); }
/* ---- Dinic ---- */
#define MAXN 200000
#define MAXE 4000000
static int head[MAXN], nxt[MAXE], to[MAXE], cap_[MAXE], ecnt, lvl[MAXN], itr[MAXN], qq[MAXN], NN;
static void addE(int a, int b, int c){ to[ecnt] = b; cap_[ecnt] = c; nxt[ecnt] = head[a]; head[a] = ecnt++; to[ecnt] = a; cap_[ecnt] = 0; nxt[ecnt] = head[b]; head[b] = ecnt++; }
static int bfs(int s, int t){ for (int i = 0; i < NN; i++) lvl[i] = -1; int h0 = 0, t0 = 0; qq[t0++] = s; lvl[s] = 0;
  while (h0 < t0){ int x = qq[h0++]; for (int e = head[x]; e >= 0; e = nxt[e]) if (cap_[e] > 0 && lvl[to[e]] < 0){ lvl[to[e]] = lvl[x] + 1; qq[t0++] = to[e]; } } return lvl[t] >= 0; }
static int dfs(int x, int t, int f){ if (x == t) return f; for (int *e = &itr[x]; *e >= 0; *e = nxt[*e]){ int y = to[*e];
    if (cap_[*e] > 0 && lvl[y] == lvl[x] + 1){ int d = dfs(y, t, f < cap_[*e] ? f : cap_[*e]); if (d > 0){ cap_[*e] -= d; cap_[*e ^ 1] += d; return d; } } } return 0; }
static long long maxflow(int s, int t){ long long fl = 0; while (bfs(s, t)){ for (int i = 0; i < NN; i++) itr[i] = head[i]; int f; while ((f = dfs(s, t, 1 << 30)) > 0) fl += f; } return fl; }
/* ---- semigroup ---- */
static long long info[8];
static int cmpw(const void *a, const void *b){ long long x = *(const long long *)a, y = *(const long long *)b; return (x > y) - (x < y); }
static int Qmax;
/* returns deficit, or -1 if invalid */
static long long evalS(int m, int k0, int *N0){
  if (m < 2 || m > MXM) return -1;
  long long w[MXM]; char done[MXM];
  int gens[MXK], k = 0;
  for (int i = 0; i < k0; i++){ if (N0[i] <= m) return -1; gens[k++] = N0[i]; }
  for (int i = 0; i < m; i++){ w[i] = -1; done[i] = 0; } w[0] = 0;
  for (int it = 0; it < m; it++){ int b = -1; for (int i = 0; i < m; i++) if (!done[i] && w[i] >= 0 && (b < 0 || w[i] < w[b])) b = i;
    if (b < 0) return -1; done[b] = 1;
    for (int a = 0; a < k; a++){ int j = (b + gens[a]) % m; long long v = w[b] + gens[a]; if (w[j] < 0 || v < w[j]) w[j] = v; } }
  long long M = 0, g = 0; for (int i = 0; i < m; i++){ if (w[i] > M) M = w[i]; g += w[i] / m; }
  long long c = M - m + 1; if (c <= m) return -1;
  int q = (int)((c + m - 1) / m); if (q > Qmax || q > MXQ) return -1;
  int h = (int)(c - (long long)(q - 1) * m);
  /* minimal generators among gens: n is minimal iff it is in Ap (n - m not in S) and not a sum of two nonzero Ap elements */
  int mg[MXK], km = 0;
  for (int a = 0; a < k; a++){ int r = gens[a] % m; if (w[r] != gens[a]) continue; int dec = 0;
    for (int r2 = 1; r2 < m && !dec; r2++){ long long u = w[r2]; if (u >= gens[a]) continue; long long d = gens[a] - u; int r3 = (int)(d % m); if (w[r3] == d) dec = 1; }
    if (!dec){ int dup = 0; for (int j = 0; j < km; j++) if (mg[j] == gens[a]) dup = 1; if (!dup) mg[km++] = gens[a]; } }
  for (int i = 0; i < km; i++) for (int j = i + 1; j < km; j++) if (mg[j] < mg[i]){ int t = mg[i]; mg[i] = mg[j]; mg[j] = t; }
  int e = km + 1;
  long long sw[MXM]; int ord[MXM], par[MXM], car[MXM];
  for (int i = 0; i < m; i++) sw[i] = w[i];
  qsort(sw, m, sizeof(long long), cmpw);
  ord[0] = 0; par[0] = -1;
  for (int t = 1; t < m; t++){ long long v = sw[t]; int r = (int)(v % m), best = -1, bp = -1;
    for (int a = 0; a < km; a++){ long long u = v - mg[a]; if (u < 0) continue; int ru = (int)(u % m); if (w[ru] == u && ord[ru] + 1 > best){ best = ord[ru] + 1; bp = a; } }
    if (best < 0) return -1; ord[r] = best; par[r] = bp; }
  for (int r = 0; r < m; r++) car[r] = (int)(w[r] / m) - ord[r];
  /* tokens */
  static unsigned char pool[MXM][MXK][MXQ + 2], used[MXM][MXK][MXQ + 2];
  memset(pool, 0, sizeof(pool)); memset(used, 0, sizeof(used));
  for (int r = 0; r < m; r++){ int top = (r < h) ? q : q - 1; for (int a = 0; a < km; a++) for (int kk = (ord[r] + 1 > 2 ? ord[r] + 1 : 2); kk <= top; kk++) pool[r][a][kk] = 1; }
  static int rep[MXM][MXQ + 2], nrep[MXM];
  for (int r = 0; r < m; r++){ nrep[r] = 0; long long x = w[r]; while (x != 0){ int rr = (int)(x % m); int a = par[rr]; if (nrep[r] > MXQ) return -1; rep[r][nrep[r]++] = a; x -= mg[a]; } }
  for (int r = 0; r < m; r++){ int kk = ord[r]; if (kk < 2) continue;
    int mult[MXK]; memset(mult, 0, sizeof(mult)); for (int i = 0; i < nrep[r]; i++) mult[rep[r][i]]++;
    for (int a = 0; a < km; a++) for (int j = 1; j <= mult[a]; j++){ long long u = w[r] - (long long)j * mg[a]; int ru = (int)(u % m); if (kk <= MXQ + 1) used[ru][a][kk] = 1; } }
  long long un[MXM]; for (int r = 0; r < m; r++){ un[r] = 0; for (int a = 0; a < km; a++) for (int kk = 2; kk <= q; kk++) if (pool[r][a][kk] && !used[r][a][kk]) un[r]++; }
  long long Tc = 0; for (int r = 0; r < m; r++) if (car[r] > 0){ Tc += car[r]; if (un[r] - (long long)(e - 1) * car[r] < 0){ fprintf(stderr, "own bound fails\n"); exit(1); } }
  long long W = (long long)e * (c - g) - c;
  { long long sup = 0; for (int r = 0; r < m; r++) sup += (car[r] == 0) ? un[r] : (un[r] - (long long)(e - 1) * car[r]);
    if (sup - Tc != W){ fprintf(stderr, "IDENTITY FAIL m=%d W=%lld sup=%lld Tc=%lld\n", m, W, sup, Tc); exit(1); } }
  info[0] = h; info[1] = e; info[2] = W; info[3] = Tc; info[4] = q;
  if (Tc == 0) return 0;
  /* graph: node 0 = source, 1 = sink, carried v nodes, uncarried-token nodes (per (r,a,kk) unused), spare nodes per carried u */
  NN = 2; ecnt = 0;
  static int vnode[MXM], spnode[MXM]; static int tnode[MXM][MXK][MXQ + 2];
  for (int r = 0; r < m; r++){ vnode[r] = -1; spnode[r] = -1; }
  for (int r = 0; r < m; r++) if (car[r] > 0){ vnode[r] = NN++; long long sp = un[r] - (long long)(e - 1) * car[r]; if (sp > 0) spnode[r] = NN++; }
  for (int r = 0; r < m; r++) for (int a = 0; a < km; a++) for (int kk = 0; kk <= MXQ + 1; kk++) tnode[r][a][kk] = -1;
  for (int r = 0; r < m; r++) if (car[r] == 0) for (int a = 0; a < km; a++) for (int kk = 2; kk <= q; kk++) if (pool[r][a][kk] && !used[r][a][kk]) tnode[r][a][kk] = NN++;
  if (NN > MAXN - 10) return -1;
  for (int i = 0; i < NN; i++) head[i] = -1;
  for (int r = 0; r < m; r++) if (car[r] > 0){ addE(0, vnode[r], car[r]); if (spnode[r] >= 0){ addE(spnode[r], 1, (int)(un[r] - (long long)(e - 1) * car[r])); } }
  for (int r = 0; r < m; r++) for (int a = 0; a < km; a++) for (int kk = 2; kk <= q; kk++) if (tnode[r][a][kk] >= 0) addE(tnode[r][a][kk], 1, 1);
  static char seen[MXM];
  for (int r = 0; r < m; r++){ if (car[r] <= 0) continue;
    /* enumerate proper sub-multisets of rep(r): use bitmask over positions (nrep <= MXQ) */
    memset(seen, 0, m); int n = nrep[r];
    for (long mask = 0; mask < (1L << n) - 1; mask++){ long long s = 0; for (int i = 0; i < n; i++) if (mask >> i & 1) s += mg[rep[r][i]];
      int ru = (int)(s % m); if (w[ru] != s || seen[ru]) continue; seen[ru] = 1;
      if (car[ru] == 0){ for (int a = 0; a < km; a++) for (int kk = 2; kk <= q; kk++) if (tnode[ru][a][kk] >= 0){ addE(vnode[r], tnode[ru][a][kk], 1); if (ecnt > MAXE - 10) return -1; } }
      else if (spnode[ru] >= 0) addE(vnode[r], spnode[ru], 1 << 20); }
    if (spnode[r] >= 0) addE(vnode[r], spnode[r], 1 << 20); }
  long long fl = maxflow(0, 1);
  return Tc - fl;
}
int main(int argc, char **argv){
  int ann = !strcmp(argv[1], "ann"); srand(atoi(argv[2])); int mlo = atoi(argv[3]), mhi = atoi(argv[4]), kmin = atoi(argv[5]), kmax = atoi(argv[6]); int G = atoi(argv[7]);
  if (!ann){ long N = atol(argv[8]); Qmax = atoi(argv[9]); long cnt = 0, bad = 0; long byq[MXQ + 2] = {0};
    for (long it = 0; it < N; it++){ int m = mlo + rand() % (mhi - mlo + 1), k = kmin + rand() % (kmax - kmin + 1); int Nn[MXK];
      for (int i = 0; i < k; i++) Nn[i] = m + 1 + rand() % ((G - 1) * m - 1);
      long long d = evalS(m, k, Nn); if (d < 0) continue; cnt++; byq[info[4]]++;
      if (d > 0){ bad++; printf("DEFICIT %lld m=%d e=%lld q=%lld h=%lld W=%lld Tc=%lld gens=", d, m, info[1], info[4], info[0], info[2], info[3]); for (int i = 0; i < k; i++) printf("%d,", Nn[i]); printf("\n"); fflush(stdout); } }
    printf("rnd S %ld deficits %ld; by depth:", cnt, bad); for (int q = 2; q <= MXQ; q++) if (byq[q]) printf(" %d:%ld", q, byq[q]); printf("\n"); return 0; }
  long iters = atol(argv[8]); int R = atoi(argv[9]); Qmax = atoi(argv[10]); double best = 1e18;
  for (int rs = 0; rs < R; rs++){
    int m, k, Nn[MXK]; double f; int tries = 0; long long d;
    do { m = mlo + rand() % (mhi - mlo + 1); k = kmin + rand() % (kmax - kmin + 1); for (int i = 0; i < k; i++) Nn[i] = m + 1 + rand() % ((G - 1) * m - 1);
      d = evalS(m, k, Nn); tries++; } while (d < 0 && tries < 100000);
    if (d < 0 || info[1] < 3) continue; f = (double)info[2] / ((double)info[3] + 1.0) - 1000.0 * d;
    double T = 0.5;
    for (long it = 0; it < iters; it++){
      int m2 = m, k2 = k, N2[MXK]; memcpy(N2, Nn, sizeof(Nn)); int mv = rand() % 5, i = rand() % k2;
      if (mv == 0) N2[i] = m2 + 1 + rand() % ((G - 1) * m2 - 1);
      else if (mv == 1) N2[i] += (rand() % 2) ? 1 : -1;
      else if (mv == 2) m2 += (rand() % 2) ? 1 : -1;
      else if (mv == 3 && k2 < kmax) N2[k2++] = m2 + 1 + rand() % ((G - 1) * m2 - 1);
      else if (mv == 4 && k2 > kmin) N2[i] = N2[--k2];
      if (m2 < mlo || m2 > mhi) continue;
      long long d2 = evalS(m2, k2, N2); if (d2 < 0 || info[1] < 3) continue;
      double g2 = (double)info[2] / ((double)info[3] + 1.0) - 1000.0 * d2;
      if (g2 <= f || urand() < exp((f - g2) / T)){ m = m2; k = k2; memcpy(Nn, N2, sizeof(Nn)); f = g2; d = d2; }
      if (d2 > 0){ printf("DEFICIT %lld m=%d e=%lld q=%lld W=%lld gens=", d2, m2, info[1], info[4], info[2]); for (int j = 0; j < k2; j++) printf("%d,", N2[j]); printf("\n"); fflush(stdout); }
      if (f < best){ best = f; evalS(m, k, Nn); printf("best %.4f m=%d e=%lld q=%lld h=%lld W=%lld Tc=%lld deficit=%lld gens=", best, m, info[1], info[4], info[0], info[2], info[3], d); for (int j = 0; j < k; j++) printf("%d,", Nn[j]); printf("\n"); fflush(stdout); }
      T *= 0.9999; if (T < 0.01) T = 0.01;
    }
  }
}
