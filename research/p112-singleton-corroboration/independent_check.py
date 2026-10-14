#!/usr/bin/env python3
"""Algorithmically separate exact cross-check; same ChatGPT author, not formal review.

Rebuilds geometry and all complex-support flats without using verify.py or the
published representatives. Uses a nine-bit label model with an explicitly
inverted binary pairing matrix, low-bit elimination, and adjugate rational
inversion for the fixture matrices. Standard library only, Python 3.12+.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import platform

ROOT = Path(__file__).resolve().parent


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def members(mask):
    return [j for j in range(mask.bit_length()) if (mask >> j) & 1]


def basis(vectors):
    # Lowest-pivot elimination, distinct from the primary high-pivot algorithm.
    piv = {}
    for vector in vectors:
        while vector:
            low = vector & -vector
            if low in piv:
                vector ^= piv[low]
            else:
                piv[low] = vector
                break
    return [piv[k] for k in sorted(piv)]


def rank(vectors):
    return len(basis(vectors))


def parity(x):
    return x.bit_count() % 2


def histogram(values):
    return {str(k): v for k, v in sorted(Counter(values).items())}


def geometry():
    roots = set()
    for i in range(8):
        for j in range(i + 1, 8):
            for minus in (False, True):
                vector = tuple(2 if k == i else (-2 if minus else 2) if k == j else 0
                               for k in range(8))
                # These are precisely the eight frame root lines.
                if i // 2 != j // 2:
                    roots.add(vector)
    for code in range(128):
        if parity(code) == 0:
            roots.add((1,) + tuple(1 - 2 * ((code >> k) & 1) for k in range(7)))
    roots = sorted(roots)
    check(len(roots) == 112, "independent live-root census")
    X = [[(r[2 * p] + sign * r[2 * p + 1]) // 2
          for p in range(4) for sign in (1, -1)] for r in roots]
    gram = [[sum(x * y for x, y in zip(a, b)) // 4 for b in roots] for a in roots]
    B = [sum(((g + 1) % 2) << j for j, g in enumerate(row)) for row in gram]
    digest = sha256(json.dumps({"roots": roots, "X": X, "B": B},
                              sort_keys=True).encode()).hexdigest()
    return roots, X, B, gram, digest


def binary_inverse(rows, n):
    aug = [r | (1 << (n + i)) for i, r in enumerate(rows)]
    for col in range(n):
        k = next((i for i in range(col, n) if (aug[i] >> col) & 1), None)
        check(k is not None, "singular binary pairing matrix")
        aug[k], aug[col] = aug[col], aug[k]
        for i in range(n):
            if i != col and (aug[i] >> col) & 1:
                aug[i] ^= aug[col]
    check(all((v & ((1 << n) - 1)) == 1 << i for i, v in enumerate(aug)),
          "binary inverse elimination")
    return [v >> n for v in aug]


def compress(B):
    selected, rows = [], []
    for i, row in enumerate(B):
        if rank(rows + [row]) > len(rows):
            selected.append(i)
            rows.append(row)
    check(len(selected) == 9, "independent binary rank is nine")
    labels = [sum(((row >> p) & 1) << j for j, p in enumerate(selected)) for row in B]
    H = [labels[p] for p in selected]
    invH = binary_inverse(H, 9)

    def dual(x):
        result = 0
        for k in members(x):
            result ^= invH[k]
        return result

    check(all(parity(dual(labels[i]) & labels[j]) == ((B[i] >> j) & 1)
              for i in range(112) for j in range(112)), "all 12544 binary pairings")
    return labels, dual, selected, H, invH


def all_supports(Y):
    directions = sorted({tuple((1 if next(x for x in y if x) > 0 else -1) * x for x in y)
                         for y in Y if any(y)})
    check(len(directions) == 13, "independent direction census")
    zero_sets = {frozenset()}
    zero_sets |= {frozenset([i]) for i in range(13)}
    for p, q in combinations(range(13), 2):
        a, b = directions[p], directions[q]
        normal = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
                  a[0] * b[1] - a[1] * b[0])
        zero_sets.add(frozenset(i for i, d in enumerate(directions)
                               if sum(x * y for x, y in zip(d, normal)) == 0))
    check(len(zero_sets) == 39, "independent proper-flat census")
    row_direction = []
    for y in Y:
        if not any(y):
            row_direction.append(None)
        else:
            sign = 1 if next(x for x in y if x) > 0 else -1
            row_direction.append(directions.index(tuple(sign * x for x in y)))
    return sorted(sum(1 << i for i, d in enumerate(row_direction) if d is not None and d not in z)
                  for z in zero_sets)


def determinant(A):
    n = len(A)
    answer = Fraction(0)
    for p in permutations(range(n)):
        sign = -1 if sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n)) % 2 else 1
        value = Fraction(sign)
        for i in range(n):
            value *= A[i][p[i]]
        answer += value
    return answer


def adjugate_inverse(A):
    n, det = len(A), determinant(A)
    check(det != 0, "fixture M invertible by determinant")
    return [[((-1) ** (i + j)) * determinant(
        [[A[r][c] for c in range(n) if c != i] for r in range(n) if r != j]) / det
        for j in range(n)] for i in range(n)]


def main():
    certificate = json.loads((ROOT / "certificate.json").read_text())
    roots, X, B, G, digest = geometry()
    check(digest == certificate["geometry_sha256"] ==
          "384dd5b48cfd306667deafa09f58255f39a8099e609122dc695fe4ce416b2115", "geometry digest")
    Y = [[r[k] for k in (2, 4, 5)] for r in X]
    labels, dual, selected, H, invH = compress(B)
    masks = all_supports(Y)
    span_cache = {}

    def label_basis(mask):
        if mask not in span_cache:
            span_cache[mask] = basis(labels[i] for i in members(mask))
        return span_cache[mask]

    def pair_rank(left, right):
        aa, bb = label_basis(left), label_basis(right)
        return rank(sum(parity(dual(a) & b) << j for j, b in enumerate(bb)) for a in aa)

    finite = certificate["finite"]
    strata = {int(s["support"], 16): s for s in finite["strata"]}
    check(set(strata) == set(masks), "independently generated support patterns")
    check(histogram(pair_rank(s, t) for s in masks for t in masks) ==
          finite["unmodified_pairing_histogram"], "unmodified pairing histogram")
    words = sorted(sum(parity(label & h) << i for i, label in enumerate(labels)) for h in range(512))
    check(len(set(words)) == 512, "all dual functionals of nine-bit label space")
    total_cuts, total_anchor_spans, total_pairings = Counter(), Counter(), Counter()
    deletion_count = 0
    for s in masks:
        item = strata[s]
        check(len(label_basis(s)) == item["span"], "independent stratum span")
        cuts = Counter(len(label_basis(s & w)) for w in words if s & w)
        check(min(cuts) >= 7, "independent cut span floor")
        check({str(k): v for k, v in sorted(cuts.items())} == item["nonempty_cut_span_histogram"],
              "per-stratum cut histogram")
        check(min((s & w).bit_count() for w in words if s & w) == item["minimum_nonempty_cut_size"],
              "per-stratum minimum cut size")
        total_cuts.update(cuts)
        anchors, pairs = Counter(), Counter()
        for beta in range(112):
            check(len(label_basis(s & ~(1 << beta))) == len(label_basis(s)), "single deletion span")
            deletion_count += 1
            cut = s & B[beta]
            check(cut != 0, "nonempty live-anchor cut")
            anchors[len(label_basis(cut))] += 1
            for t in masks:
                cost = pair_rank(cut, t)
                check(cost >= 7, "independent mandatory pairing floor")
                pairs[cost] += 1
        check({str(k): v for k, v in sorted(anchors.items())} == item["mandatory_span_histogram"],
              "per-stratum mandatory span histogram")
        check({str(k): v for k, v in sorted(pairs.items())} == item["mandatory_pairing_histogram"],
              "per-stratum mandatory pairing histogram")
        total_anchor_spans.update(anchors)
        total_pairings.update(pairs)
    check(deletion_count == finite["one_point_span_preservation_checks"], "deletion census")
    results = []
    for f, target in zip(certificate["fixture_inputs"], certificate["fixture_results"]):
        beta, lam = f["beta"], Fraction(f["lambda"])
        u = [Fraction(0)] * 112
        for i, x in f["u"]:
            u[i] = Fraction(x)
        U = sum(1 << i for i, x in enumerate(u) if x)
        check(U.bit_count() >= 2 and not U & B[beta] and lam != 0, "fixture scope")
        M = [[Fraction(x) for x in r] for r in f["M"]]
        N = list(zip(*adjugate_inverse(M)))
        D = [[sum(x * M[k][j] for k, x in enumerate(Y[i] + [u[i]])) for j in range(4)]
             for i in range(112)]
        T = [[sum(x * N[k][j] for k, x in enumerate(Y[i] + [lam * (i == beta)])) for j in range(4)]
             for i in range(112)]
        check(all(sum(D[i][k] * T[j][k] for k in range(4)) ==
                  sum(Y[i][k] * Y[j][k] for k in range(3)) + u[i] * lam * (j == beta)
                  for i in range(112) for j in range(112)), "independent exact fixture identity")
        ds = [sum(1 << i for i in range(112) if D[i][j]) for j in range(4)]
        ts = [sum(1 << i for i in range(112) if T[i][j]) for j in range(4)]
        costs = [pair_rank(a, b) for a, b in zip(ds, ts)]
        check(costs == f["expected_ranks"] == target["mixed_ranks"], "independent fixture ranks")
        check([hex(s) for s in ds] == target["D_supports"] and
              [hex(s) for s in ts] == target["T_supports"], "independent actual supports")
        check(40 + sum(costs) == f["expected_complete_copy"] == target["complete_copy"],
              "independent complete billing")
        results.append({"name": f["name"], "mixed_ranks": costs, "complete_copy": 40 + sum(costs)})
    print(json.dumps({"status": "PASS_ALGORITHMIC_CROSS_CHECK", "python": platform.python_version(),
                      "geometry_sha256": digest, "label_basis_indices": selected,
                      "pairing_matrix_rows": H, "inverse_pairing_matrix_rows": invH,
                      "proper_support_patterns": len(masks), "one_point_deletion_checks": deletion_count,
                      "mandatory_pairing_histogram": {str(k): v for k, v in sorted(total_pairings.items())},
                      "nonempty_cut_span_histogram": {str(k): v for k, v in sorted(total_cuts.items())},
                      "fixtures": results}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
