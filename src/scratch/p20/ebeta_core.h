/* Shared core (lead, 2026-10-19): chain deficit vs factorization-overlap compensation.
 * Input: m, Apery set w[0..m-1] (w[0] = 0), M = max, minimal generators n[0..d-1] (all != m).
 * Computes
 *   B      = d m M - (d+1) sum Ap          (= mW + need, CH')
 *   Bc     = sum_{w,a} (M - top_a(w))      (Apery chains)
 *   E      = sum_w (sum_a n_a depth_a(w) - w)   = n.(join Z(w)) - w summed; identity E == B - Bc is asserted
 *   Ebeta  = sum_w max{ b in Tmin : b <=_S w }, Tmin = <=_S-minimal Apery elements with >= 2 factorizations
 *   Eu     = sum_w max(0, sum_{a : w - n_a in S} n_a - w)   (support-union / lower-cover bound; Eu <= E)
 *   need   = (d-1) m(m-1)/2
 *   Link form: Delta = sum_v P(v) - m Ltop, P(v) = sum_a depth_a(v)(s_{v-n_a} - s_v), Ltop = sum_{w,a} lam(top_a(w));
 *   L1(v) = sum_a depth_a(v)(lam(v-n_a) - lam(v)); local balance P(v) - E(v) = v - m L1(v) (asserted).
 *   Wp = sum_v max(0, v - m L1(v)) (WILF+: Wp - m Ltop <= C2);  Ppoor = sum_{v: m L1(v) < v} P(v) (CHAIN-POOR: Ppoor - m Ltop <= C2).
 * Factorization counts capped at 2 by coin-change DP over Apery values (partial sums of a factorization of an
 * Apery element are Apery elements). */
#include <stdint.h>
#include <string.h>
typedef struct { int64_t B, Bc, E, Eb, Eu, need, M, Wp, Ppoor, Ltop, Delta; int ntmin, idlink; int64_t bmin; } EB;
static unsigned char eb_cnt[1 << 16]; static unsigned char eb_tmin[1 << 16];
static int eb_compute(int m, const int64_t *w, const int64_t *n, int d, EB *r) {
  int64_t M = 0, sum = 0; for (int i = 0; i < m; i++) { if (w[i] > M) M = w[i]; sum += w[i]; }
  if (M >= (1 << 16)) return 0;
  #define INAP(v) ((v) >= 0 && (v) <= M && w[(v) % m] == (v))
  r->M = M; r->B = (int64_t)d * m * M - (int64_t)(d + 1) * sum; r->need = (int64_t)(d - 1) * m * (m - 1) / 2;
  r->Bc = 0; r->E = 0;
  for (int a = 0; a < d; a++) for (int i = 0; i < m; i++) {
    int64_t t = w[i]; while (INAP(t + n[a])) t += n[a]; r->Bc += M - t;
    int64_t s = w[i]; int64_t dep = 0; while (INAP(s - n[a])) { s -= n[a]; dep++; } r->E += n[a] * dep;
  }
  r->E -= sum;
  { int64_t Ltop = 0, Delta = 0, SP = 0, Wp = 0, Pp = 0; int bad = 0;
    for (int a = 0; a < d; a++) for (int i = 0; i < m; i++) { int64_t t = w[i]; while (INAP(t + n[a])) t += n[a]; Ltop += (M - t) / m; Delta += (M - w[i]) % m - (M - t); }
    for (int i = 0; i < m; i++) { int64_t v = w[i], P = 0, Ev = -v, L1 = 0;
      for (int a = 0; a < d; a++) { int64_t y = v, dep = 0; while (INAP(y - n[a])) { y -= n[a]; dep++; }
        if (dep) { P += dep * (((M - v + n[a]) % m) - ((M - v) % m)); L1 += dep * ((M - v + n[a]) / m - (M - v) / m); }
        Ev += n[a] * dep; }
      if (P - Ev != v - (int64_t)m * L1) bad = 1;
      SP += P; if (v > (int64_t)m * L1) { Wp += v - (int64_t)m * L1; Pp += P; } }
    if (Delta != SP - (int64_t)m * Ltop) bad = 1;
    r->Ltop = Ltop; r->Delta = Delta; r->Wp = Wp; r->Ppoor = Pp; r->idlink = bad; }
  r->Eu = 0; for (int i = 0; i < m; i++) { int64_t s2 = 0; for (int a = 0; a < d; a++) if (INAP(w[i] - n[a])) s2 += n[a]; if (s2 > w[i]) r->Eu += s2 - w[i]; }
  memset(eb_cnt, 0, M + 1); eb_cnt[0] = 1;
  for (int a = 0; a < d; a++) for (int64_t v = n[a]; v <= M; v++) if (INAP(v) && INAP(v - n[a])) { int c = eb_cnt[v] + eb_cnt[v - n[a]]; eb_cnt[v] = c > 2 ? 2 : c; }
  int64_t tlist[1024]; int nt = 0; r->bmin = -1;
  for (int i = 0; i < m; i++) { int64_t v = w[i]; eb_tmin[v] = 0; if (eb_cnt[v] < 2) continue; int mn = 1;
    for (int a = 0; a < d && mn; a++) if (INAP(v - n[a]) && eb_cnt[v - n[a]] >= 2) mn = 0;
    if (mn) { tlist[nt++] = v; if (r->bmin < 0 || v < r->bmin) r->bmin = v; } }
  r->ntmin = nt; r->Eb = 0;
  for (int i = 0; i < m; i++) { int64_t best = 0; for (int k = 0; k < nt; k++) { int64_t b = tlist[k]; if (b > best && INAP(w[i] - b)) best = b; } r->Eb += best; }
  #undef INAP
  return 1;
}
