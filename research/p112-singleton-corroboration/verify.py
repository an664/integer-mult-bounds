#!/usr/bin/env python3
"""Exact, offline checker for the fixed P112 three-mode singleton obstruction.

Python 3.12+; standard library only. No randomness, network, package installation,
or source-checkout changes. Default: recompute and compare certificate.json.
Use --emit PATH to write the fully recomputed certificate instead.

This program checks the finite premises and exact rational fixtures. The universal
complex-amplitude argument and the continuum of power exponents are in proof.md.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import platform
from typing import Iterable

BASE = Path(__file__).resolve().parent
GEOMETRY_SHA256 = "384dd5b48cfd306667deafa09f58255f39a8099e609122dc695fe4ce416b2115"
J = (2, 4, 5)


class VerificationError(Exception):
    """A finite premise, fixture, or supplied certificate failed verification."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def bits(mask: int):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def support(values) -> int:
    return sum(1 << i for i, x in enumerate(values) if x != 0)


def f2_basis(vectors: Iterable[int]) -> list[int]:
    pivots: dict[int, int] = {}
    for x in vectors:
        while x:
            p = x.bit_length() - 1
            if p not in pivots:
                pivots[p] = x
                break
            x ^= pivots[p]
    return [pivots[p] for p in sorted(pivots, reverse=True)]


def f2_rank(vectors: Iterable[int]) -> int:
    return len(f2_basis(vectors))


def label_span(B: list[int], mask: int) -> int:
    return f2_rank(B[i] for i in bits(mask))


def rho(B: list[int], left: int, right: int) -> int:
    return f2_rank(B[i] & right for i in bits(left))


def histogram(values) -> dict[str, int]:
    return {str(k): v for k, v in sorted(Counter(values).items())}


def transpose(A):
    return [list(c) for c in zip(*A)]


def multiply(A, C):
    return [[dot(r, c) for c in zip(*C)] for r in A]


def identity(n: int):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def inverse(A):
    n = len(A)
    require(n > 0 and all(len(r) == n for r in A), "matrix must be square")
    aug = [[Q(x) for x in r] + identity(n)[i] for i, r in enumerate(A)]
    for j in range(n):
        p = next((i for i in range(j, n) if aug[i][j]), None)
        require(p is not None, "singular mixing matrix")
        aug[j], aug[p] = aug[p], aug[j]
        pivot = aug[j][j]
        aug[j] = [x / pivot for x in aug[j]]
        for i in range(n):
            if i != j:
                multiplier = aug[i][j]
                aug[i] = [x - multiplier * y for x, y in zip(aug[i], aug[j])]
    return [r[n:] for r in aug]


def rational_rank(A) -> int:
    if not A:
        return 0
    rows = [[Q(x) for x in r] for r in A]
    k = 0
    for j in range(len(rows[0])):
        p = next((i for i in range(k, len(rows)) if rows[i][j]), None)
        if p is None:
            continue
        rows[k], rows[p] = rows[p], rows[k]
        pivot = rows[k][j]
        rows[k] = [x / pivot for x in rows[k]]
        for i in range(k + 1, len(rows)):
            v = rows[i][j]
            rows[i] = [x - v * y for x, y in zip(rows[i], rows[k])]
        k += 1
    return k


def build_geometry():
    roots = []
    for i, j in combinations(range(8), 2):
        for sign in (-1, 1):
            r = [0] * 8
            r[i], r[j] = 2, 2 * sign
            roots.append(tuple(r))
    for signs in product((-1, 1), repeat=7):
        if signs.count(-1) % 2 == 0:
            roots.append((1,) + signs)
    frame = []
    for p in range(4):
        for sign in (1, -1):
            r = [0] * 8
            r[2 * p], r[2 * p + 1] = 2, 2 * sign
            frame.append(tuple(r))
    require(len(roots) == len(set(roots)) == 120, "120 root representatives")
    require(set(frame) <= set(roots), "deleted frame membership")
    roots = sorted(set(roots) - set(frame))
    require(len(roots) == 112, "112 live roots")
    require(all(dot(r, f) % 4 == 0 for r in roots for f in frame), "integral X")
    require(all(dot(r, s) % 4 == 0 for r in roots for s in roots), "integral G")
    X = [[dot(r, f) // 4 for f in frame] for r in roots]
    G = [[dot(r, s) // 4 for s in roots] for r in roots]
    B = [sum(((1 + g) % 2) << j for j, g in enumerate(row)) for row in G]
    require(all(x in (-1, 0, 1) for row in X for x in row), "X entry alphabet")
    require(all(dot(X[i], X[j]) == 2 * G[i][j]
                for i in range(112) for j in range(112)), "XX^T = 2G")
    require(rational_rank(X) == 8, "rational/complex rank X = 8")
    require(all(((B[i] >> j) & 1) == ((B[j] >> i) & 1)
                for i in range(112) for j in range(112)), "B symmetric")
    require(f2_rank(B) == 9, "binary rank B = 9")
    require(all(rho(B, support(r[k] for r in X), support(r[k] for r in X)) == 8
                for k in range(8)), "all eight original costs equal 8")
    digest = sha256(json.dumps({"roots": roots, "X": X, "B": B},
                              sort_keys=True).encode()).hexdigest()
    require(digest == GEOMETRY_SHA256, "pinned geometry digest mismatch")
    return roots, X, B, G, digest


def canonical_direction(v):
    nonzero = next((x for x in v if x), None)
    if nonzero is None:
        return None
    return tuple(Q(x, nonzero) for x in v)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def enumerate_flats(Y):
    directions = sorted({canonical_direction(y) for y in Y if any(y)})
    require(len(directions) == 13, "13 nonzero projective directions")
    flat_rank = {0: 0}
    flat_rank.update({1 << i: 1 for i in range(13)})
    for a, b in combinations(directions, 2):
        normal = cross(a, b)
        require(any(normal), "distinct directions must be independent")
        flat = sum(1 << i for i, d in enumerate(directions) if dot(d, normal) == 0)
        flat_rank[flat] = 2
    require(histogram(flat_rank.values()) == {"0": 1, "1": 13, "2": 25},
            "proper flat census")
    index = {d: i for i, d in enumerate(directions)}
    support_to_flat = {}
    for flat, rank in flat_rank.items():
        mask = sum(1 << i for i, y in enumerate(Y)
                   if any(y) and not ((flat >> index[canonical_direction(y)]) & 1))
        require(mask not in support_to_flat, "distinct flats must give distinct supports")
        support_to_flat[mask] = (flat, rank)
    return directions, support_to_flat


def check_published_strata(Y, B, support_to_flat, rows):
    require(len(rows) == 39, "39 published stratum records")
    result = []
    seen = set()
    for a, hexa, size, span in rows:
        require(len(a) == 3 and any(a), "nonzero triple representative")
        mask = support(dot(y, a) for y in Y)
        require(mask == int(hexa, 16), f"copied support mask mismatch at {a}")
        require(mask.bit_count() == size, f"copied support size mismatch at {a}")
        require(label_span(B, mask) == span, f"copied label span mismatch at {a}")
        require(mask in support_to_flat and mask not in seen, "stratum flat match")
        seen.add(mask)
        flat, flat_rank = support_to_flat[mask]
        result.append({"a": a, "support": hex(mask), "size": size,
                       "span": span, "zero_flat": hex(flat), "flat_rank": flat_rank})
    require(seen == set(support_to_flat), "published representatives cover every proper flat")
    return result


def finite_certificate(Y, B, rows, flats):
    strata = check_published_strata(Y, B, flats, rows)
    masks = [int(s["support"], 16) for s in strata]
    original = histogram(rho(B, s, t) for s in masks for t in masks)
    require(min(map(int, original)) >= 8, "unmodified pairing floor 8")
    deletion_checks = 0
    for s in masks:
        before = label_span(B, s)
        for beta in range(112):
            require(label_span(B, s & ~(1 << beta)) == before,
                    "one-point deletion must preserve the coordinate-combination span")
            deletion_checks += 1
    words = [0]
    for b in f2_basis(B):
        words += [w ^ b for w in words]
    words.sort()
    require(len(set(words)) == 512, "all 512 row-space words")
    total_cuts, total_anchor_spans, total_anchor_pairings = Counter(), Counter(), Counter()
    weight_min, cut_rank_min, witness = 112, 9, None
    for item, s in zip(strata, masks):
        cuts, weights = Counter(), Counter()
        for w in words:
            e = s & w
            if not e:
                continue
            erank = label_span(B, e)
            cuts[erank] += 1
            weights[e.bit_count()] += 1
            require(erank >= 7, "nonempty row-space cut span floor 7")
            if witness is None or erank < cut_rank_min:
                witness = {"a": item["a"], "word": hex(w), "cut": hex(e), "span": erank}
            cut_rank_min = min(cut_rank_min, erank)
            weight_min = min(weight_min, e.bit_count())
        total_cuts.update(cuts)
        anchor_spans, anchor_pairs = Counter(), Counter()
        anchors_by_span = {}
        for beta in range(112):
            mandatory = s & B[beta]
            require(mandatory != 0, "every live anchor meets every nonzero stratum")
            r = label_span(B, mandatory)
            anchor_spans[r] += 1
            anchors_by_span.setdefault(str(r), []).append(beta)
            for t in masks:
                cost = rho(B, mandatory, t)
                require(cost >= 7, "mandatory singleton-anchor pairing floor 7")
                anchor_pairs[cost] += 1
        total_anchor_spans.update(anchor_spans)
        total_anchor_pairings.update(anchor_pairs)
        item["nonempty_cut_span_histogram"] = {str(k): v for k, v in sorted(cuts.items())}
        item["minimum_nonempty_cut_size"] = min(weights)
        item["mandatory_span_histogram"] = {str(k): v for k, v in sorted(anchor_spans.items())}
        item["anchors_by_mandatory_span"] = {
            k: ("all 112" if len(v) == 112 else v) for k, v in sorted(anchors_by_span.items())}
        item["mandatory_pairing_histogram"] = {str(k): v for k, v in sorted(anchor_pairs.items())}
    return {
        "strata": strata,
        "unmodified_pairing_histogram": original,
        "one_point_span_preservation_checks": deletion_checks,
        "row_space_word_count": len(words),
        "row_space_weight_histogram": histogram(w.bit_count() for w in words),
        "nonempty_cut_span_histogram": {str(k): v for k, v in sorted(total_cuts.items())},
        "minimum_nonempty_cut_size": weight_min,
        "minimum_nonempty_cut_span": cut_rank_min,
        "cut_span_seven_witness": witness,
        "mandatory_span_histogram": {str(k): v for k, v in sorted(total_anchor_spans.items())},
        "mandatory_pairing_histogram": {str(k): v for k, v in sorted(total_anchor_pairings.items())},
    }


def assess_fixture(f, Y, X, B, G):
    beta, lam = f["beta"], Q(f["lambda"])
    require(type(beta) is int and 0 <= beta < 112, "beta outside live indices")
    require(lam != 0, "lambda must be nonzero")
    u = [Q(0)] * 112
    for i, val in f["u"]:
        require(type(i) is int and 0 <= i < 112, "u index outside live indices")
        require(u[i] == 0 and Q(val) != 0, "u entries must be distinct and nonzero")
        u[i] = Q(val)
    U = support(u)
    require(U.bit_count() >= 2, "actual U support must have size at least two")
    require((U & B[beta]) == 0, "u correction touches a constrained entry")
    M = [[Q(x) for x in r] for r in f["M"]]
    require(len(M) == 4 and all(len(r) == 4 for r in M), "M must be 4 by 4")
    N = transpose(inverse(M))
    if "provided_N" in f:
        supplied = [[Q(x) for x in r] for r in f["provided_N"]]
        require(supplied == N, "supplied N is not M^(-T)")
    require(multiply(transpose(M), N) == identity(4), "dual-column identity")
    v = [lam * (i == beta) for i in range(112)]
    D = multiply([list(y) + [ui] for y, ui in zip(Y, u)], M)
    T = multiply([list(y) + [vi] for y, vi in zip(Y, v)], N)
    mixed = multiply(D, transpose(T))
    others = [[row[k] for k in range(8) if k not in J] for row in X]
    for i in range(112):
        for j in range(112):
            desired = dot(Y[i], Y[j]) + u[i] * v[j]
            require(mixed[i][j] == desired, "four-term algebraic identity")
            whole = mixed[i][j] + dot(others[i], others[j])
            require(whole == 2 * G[i][j] + u[i] * v[j], "complete nine-term identity")
            if (B[i] >> j) & 1:
                require(whole == 2 * G[i][j], "constrained-entry agreement")
    ds, ts = [support(c) for c in zip(*D)], [support(c) for c in zip(*T)]
    ranks = [rho(B, a, b) for a, b in zip(ds, ts)]
    bill = 40 + sum(ranks)
    require(ranks == f["expected_ranks"], "actual four-term ranks disagree with invoice")
    require(bill == f["expected_complete_copy"], "complete invoice drops or misprices a term")
    return {"name": f["name"], "beta": beta, "U": hex(U),
            "U_size": U.bit_count(), "U_span": label_span(B, U),
            "D_supports": [hex(s) for s in ds], "T_supports": [hex(s) for s in ts],
            "D_support_sizes": [s.bit_count() for s in ds],
            "T_support_sizes": [s.bit_count() for s in ts],
            "mixed_ranks": ranks, "complete_copy": bill,
            "a_zero_columns": [j for j in range(4) if not any(M[i][j] for i in range(3))],
            "b_zero_columns": [j for j in range(4) if not any(N[i][j] for i in range(3))]}


def fixture_inputs(Y, B):
    beta = 0
    free = [i for i in range(112) if not ((B[i] >> beta) & 1)]
    require(free[:2] == [1, 2], "fixture indexing")
    small = [[i, 1] for i in free[:2]]
    boundary = [[i, -Y[i][0]] for i in free if Y[i][0] != 0]
    I = [[int(i == j) for j in range(4)] for i in range(4)]
    lower = deepcopy(I)
    lower[3][0] = 1
    upper = deepcopy(I)
    upper[0][3] = 1
    dense = [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1], [1, 2, 3, 1]]
    rows = [
        ("baseline", small, I, [8, 8, 8, 0]),
        ("left_pure_u_without_saving", small, lower, [8, 8, 8, 2]),
        ("boundary_cancellation_compensation_paid", boundary, lower, [7, 8, 8, 7]),
        ("right_pure_target", small, upper, [8, 8, 8, 1]),
        ("four_nonzero_coordinate_pairs", small, dense, [9, 8, 8, 9]),
    ]
    return [{"name": name, "beta": beta, "lambda": 1, "u": u, "M": M,
             "expected_ranks": costs, "expected_complete_copy": 40 + sum(costs)}
            for name, u, M, costs in rows]


def rejection_controls(fixtures, Y, X, B, G, flats, published):
    passed = []

    def reject(name, action):
        try:
            action()
        except VerificationError:
            passed.append(name)
        else:
            raise VerificationError(f"rejection control accepted: {name}")

    def check(f):
        assess_fixture(f, Y, X, B, G)

    bad = deepcopy(fixtures[0]); bad["M"][3] = bad["M"][2][:]
    reject("singular_M", lambda: check(bad))
    bad = deepcopy(fixtures[0]); bad["u"] = [[0, 1], [1, 1]]
    reject("nonfree_u_entry", lambda: check(bad))
    bad = deepcopy(fixtures[0]); bad["u"] = [[1, 1]]
    reject("out_of_scope_singleton_U", lambda: check(bad))
    bad = deepcopy(fixtures[0]); bad["lambda"] = 0
    reject("zero_lambda", lambda: check(bad))
    bad = deepcopy(fixtures[2]); bad["expected_complete_copy"] = 63
    reject("boundary_invoice_omits_compensation", lambda: check(bad))
    bad = deepcopy(fixtures[2]); bad["provided_N"] = inverse(bad["M"])
    reject("inverse_used_without_transpose", lambda: check(bad))
    bad_data = deepcopy(published); bad_data[0][1] = hex(int(bad_data[0][1], 16) ^ 1)
    reject("corrupted_copied_support", lambda: check_published_strata(Y, B, flats, bad_data))
    # These last two deliberately false stronger claims have actual counter-witnesses.
    s = support(y[0] for y in Y)
    reject("false_anchor_floor_eight", lambda: require(label_span(B, s & B[0]) >= 8,
                                                        "observed anchor span is seven"))
    e = support(dict(fixtures[2]["u"]).get(i, 0) for i in range(112))
    reject("false_free_compensation", lambda: require(rho(B, e, s) == 0,
                                                       "compensation rank is seven"))
    return passed


def run():
    roots, X, B, G, digest = build_geometry()
    Y = [[r[k] for k in J] for r in X]
    directions, flats = enumerate_flats(Y)
    published = json.loads((BASE / "published_strata.json").read_text())
    finite = finite_certificate(Y, B, published, flats)
    fixtures = fixture_inputs(Y, B)
    checked = [assess_fixture(f, Y, X, B, G) for f in fixtures]
    controls = rejection_controls(fixtures, Y, X, B, G, flats, published)
    return {"schema": 1, "geometry_sha256": digest, "J": list(J),
            "direction_count": len(directions), "flat_count": len(flats),
            "finite": finite, "fixture_inputs": fixtures,
            "fixture_results": checked, "rejection_controls_passed": controls}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", type=Path, help="write recomputed certificate to this path")
    args = parser.parse_args()
    result = run()
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.emit:
        args.emit.write_text(serialized)
        status = "RECOMPUTED_AND_EMITTED"
    else:
        expected = json.loads((BASE / "certificate.json").read_text())
        require(result == expected, "recomputed certificate differs from supplied certificate")
        status = "PASS_RECOMPUTED_AND_MATCHED"
    print(json.dumps({"status": status, "python": platform.python_version(),
                      "geometry_sha256": result["geometry_sha256"],
                      "proper_flats": result["flat_count"],
                      "mandatory_pairing_histogram": result["finite"]["mandatory_pairing_histogram"],
                      "nonempty_cut_span_histogram": result["finite"]["nonempty_cut_span_histogram"],
                      "fixture_complete_copy": {f["name"]: f["complete_copy"]
                                                for f in result["fixture_results"]},
                      "rejection_controls_passed": result["rejection_controls_passed"]},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
