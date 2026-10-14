#!/usr/bin/env python3
"""Mechanical replay of explicit P112 review Section6/7 checks, not a new proof.

Uses the unchanged producer geometry/rank/fixture API. Stdlib only. Reads only
adjacent verify.py and review_examples.json, prints JSON, and never writes files. No universal
complex or continuum-power argument is executed by this script.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

source = Path(__file__).with_name('verify.py')
if hashlib.sha256(source.read_bytes()).hexdigest() != '8a7fb4ebea94938c6c5ffbcb49b42c1dc0480d530502d1709dc50de9994a8ca9':
    raise RuntimeError('producer source SHA256 mismatch')
spec = importlib.util.spec_from_file_location('p112_producer', source)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
roots, X, B, G, digest = p.build_geometry()
Y = [[row[k] for k in p.J] for row in X]
anchor_checks = []
for coordinate in p.J:
    mask = p.support(row[coordinate] for row in X)
    for beta in range(112):
        for forced_in in (False, True):
            right = (mask | (1 << beta)) if forced_in else (mask & ~(1 << beta))
            rank = p.rho(B, mask, right)
            p.require(rank == 8, 'review Section7 anchor-in/out price must equal eight')
            anchor_checks.append({'coordinate': coordinate, 'beta': beta,
                                  'forced_anchor_in': forced_in, 'rank': rank})
p.require(len(anchor_checks) == 672, 'expected 3*112*2 anchor checks')
inputs = [
    {'name': 'review_nonmonomial_isolated_equality',
     'M': [[1,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
     'expected_ranks': [8,8,8,0], 'expected_complete_copy': 64},
    {'name': 'review_isolated_nonoptimal',
     'M': [[1,1,1,0],[1,2,3,0],[1,4,9,0],[0,0,0,1]],
     'expected_ranks': [9,9,9,0], 'expected_complete_copy': 67},
    {'name': 'review_unipotent_nonisolated_attainment',
     'M': [[1,0,0,1],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
     'expected_ranks': [8,8,8,1], 'expected_complete_copy': 65},
]
for fixture in inputs:
    fixture.update({'beta': 0, 'lambda': 1, 'u': [[1,1],[2,1]]})
results = [p.assess_fixture(f, Y, X, B, G) for f in inputs]
p.require(results[0]['a_zero_columns'] == results[0]['b_zero_columns'] == [3], 'equality fixture isolation')
p.require(results[1]['a_zero_columns'] == results[1]['b_zero_columns'] == [3], 'nonoptimal fixture isolation')
p.require(results[2]['a_zero_columns'] == [] and results[2]['b_zero_columns'] == [3], 'nonisolated fixture caseB')
controls = []
def reject(name, operation):
    try:
        operation()
    except p.VerificationError as exc:
        controls.append({'name': name, 'rejected': True, 'message': str(exc)})
    else:
        raise RuntimeError('false boundary claim accepted: ' + name)
reject('false_equality_requires_monomial_block', lambda: p.require(
    all(sum(value != 0 for value in row[:3]) == 1 for row in inputs[0]['M'][:3]),
    'the explicit equality block is nonmonomial'))
reject('false_isolation_alone_implies_copy64', lambda: p.require(
    results[1]['complete_copy'] == 64, 'the explicit isolated block costs 67'))
report = {'status': 'PASS_REVIEW_EXPLICIT_FINITE_CHECKS', 'geometry_sha256': digest,
          'anchor_support_checks': len(anchor_checks), 'all_anchor_ranks': [8],
          'fixture_inputs': inputs, 'fixture_results': results,
          'rejection_controls': controls,
          'scope': 'Explicit finite checks from Pro review Sections6/7 only; no arbitrary-amplitude or power-continuum execution.'}
expected = json.loads(Path(__file__).with_name('review_examples.json').read_text())
p.require(report == expected, 'recomputed review examples differ from saved report')
print(json.dumps(report, indent=2, sort_keys=True))
