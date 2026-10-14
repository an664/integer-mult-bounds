# Independent P112 singleton corroboration and equality detail

This fork-only evidence package preserves the independently produced fixed-triple result from [Discussion1550](https://github.com/CrocSwap/integer-mult-bounds/discussions/1550). **Hanson Sun / @bbMisk's broader [PR1613](https://github.com/CrocSwap/integer-mult-bounds/pull/1613)**, head `a34723742801f877c9636ed72f176a7ffa7bf005`, presents a broader written proof of the common COPY 64 and power `8*8^q` floor for all 56 triples and additional support boundaries. It credits our earlier parallel claim. This artifact is a corroborating reconstruction and equality note; no duplicate upstream theorem PR or novelty claim is intended.

Our scope fixes `J=(2,4,5)`, actual left correction support `|U|>=2`, a free nonzero singleton right correction `v=lambda e_beta`, arbitrary complex `GL4` mixing of the three original modes plus correction, and five unchanged terms. Supports are actual complex nonzero entries; transpose is ordinary bilinear; every term is charged separately.

The producer [proof.md](proof.md) gives sharp complete COPY 64 and power `8*8^q` minima for every `0<q<=1`, attained by identity mixing for each admissible correction. A binary-functional-cut argument forces any saved coordinate price to pay for its compensation. The explicit rank vector `(7,8,8,7)` costs 70, not the subtotal 63 obtained by dropping its final term.

## Equality and nonisolated mixing

The separate Pro review's [supplement](equality-review.md) states that equality holds exactly when a common column of `M` and `M^(-T)` has zero top-three vectors and the other three prices are eight. After common column permutation, the three-mode block may be any invertible block whose resulting prices meet that condition; it need not be monomial. Isolation alone does not guarantee equality.

Inside the same fixed scope, that review derives exact nonisolated minima COPY 65 and power `8*8^q+1` for each fixed admissible correction. Its explicit `M=I+E_(0,3)` attains `(8,8,8,1)`. The supplement retains the four-case reasoning and the chord comparison that applies to componentwise lower bounds, including when actual ranks exceed eight. This is Pro-authored written reasoning, not a claim inferred from finite sampling or an independently established novelty over PR1613.

## Replay

From the fork repository root with Python 3.12 and the standard library:

```sh
python3.12 -B scripts/research_package.py --package research/p112-singleton-corroboration
```

Or run the three read-only commands directly from this directory:

```sh
python3.12 -I -O -B verify.py
python3.12 -I -O -B independent_check.py
python3.12 -I -O -B review_examples.py
```

The first two unchanged producer implementations rebuild the geometry and finite premises: 39 complex-support strata, 1,521 baseline pairings, 4,368 singleton deletions, 170,352 mandatory anchor pairings and 19,926 nonempty functional cuts. They check five exact rational fixtures; the primary also runs nine supplied rejection controls and compares its whole regenerated certificate. The second generates flats without the copied representative table, uses a compressed binary pairing model and adjugate rational inversion, and imports no primary code. Both were authored in one Pro session, so their distinction is algorithmic rather than independent authorship.

`review_examples.py` uses the pinned producer API to replay the review's explicit 672 coordinate/anchor/in-out checks (all rank 8), three full 112x112 rational fixture identities with ranks `(8,8,8,0)`, `(9,9,9,0)` and `(8,8,8,1)`, and two false-inference controls. It compares the recomputed result to `review_examples.json`. It is a mechanical transcription of Pro-provided examples, not another independent rank engine.

Original local CPython 3.12.14 normal and optimized executions passed for both producer checkers. The additional review-example replay also passed in both modes with identical JSON; input hashes stayed unchanged. [REPLAY.json](REPLAY.json) distinguishes these receipts from the producing session's Python 3.13.5 run and records the fork-package hook separately. Each registered command is capped at 120 seconds; no installation or runtime network access is needed.

## Source and review boundary

The 39-row `published_strata.json` is copied numerical data from Hanson Sun / PR1512, authenticated against the pinned Git certificate. Neither original checker imports predecessor code. [SOURCES.json](SOURCES.json) retains the exact historical main and external Git/blob/SHA pins; [SOURCES.md](SOURCES.md) gives attribution. Both producer programs, their certificate and table are unchanged; producer proof mathematics is unchanged. Only its research attribution and first runtime paragraph were updated to distinguish actual environments.

The separate GPT-6 Pro reviewer reconstructed the premises from the theorem transcription and reported no flaw. It did not audit the original producer programs or repository checkout. The supplemental text is a chat transfer, not an authenticated original reviewer download; its mathematical sections are retained with only transport markers removed. Reviewer-code execution is not claimed locally. The new local script checks only its explicitly supplied finite examples.

No PR1613 code, 56 transports or zero/single-entry boundaries are audited here. Completed [PR1591](https://github.com/CrocSwap/integer-mult-bounds/pull/1591) is a different single-entry/all-nine-factor result. Other triples, extra modes, multiple corrections, shared COPY, physical supplier admission, a formal/human proof review and a new frontier or kappa remain outside this artifact. Historical revision-2 selection is retained alongside the revision-3 checkpoint and the explicit overlap-driven scope change.

## Open next questions

Can the finite-premise-to-universal compensation and equality argument be checked in a proof assistant? Start with the binary restriction-rank identity and cut lemma under explicit F1-F5 premises, then formalize the dual-column cases and the real-power chord comparison. This would reduce trust in the written universal implication. Formal support/rank/power interfaces and binding of the finite certificate are the missing pieces; more amplitude samples do not supply them. See the structured question in TASK.json.

## Credit

Andrey Mas with substantial GPT-6 Pro research, proof and original checker assistance through ChatGPT, followed by a separate Pro adversarial review and its equality refinement. Codex coordinated sources, audited execution, mechanically replayed explicit checks and packaged the evidence. No new mathematical derivation by Codex is claimed.

Credit Hanson Sun / @bbMisk (PR1512 arrangement and question, PR1473 and broader PR1613), Gareth Davidson / @bitplane (PR1468), Arham Tahir (PR1591/1331), commdata2338 (PR1375), Cinna Davis (PR1373), Mihir Srivastava (PR845), DreamingOfClouds (PR717/446/595), themilkman216 (PR968), Joel Pulikkan / GamingPuzzled (PR620), and woklerx (PR1077). Their geometry, table, pricing model and COPY 64 benchmark are not claimed anew. Apache-2.0.
