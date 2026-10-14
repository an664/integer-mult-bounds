# Supplement: equality and the nonisolated penalty

The following is the separate GPT-6 Pro review's Sections 5-7, transcribed from chat transport. ChatGPT transport markers and the following-part separator were removed; the mathematical text is unchanged. This is not a byte-authenticated download of the reviewer's original file. It is retained as Pro-authored written mathematics, not as new Codex derivation or a novelty claim relative to PR1613.

All definitions and finite premises F1-F5 are in [proof.md](proof.md), for fixed J=(2,4,5), actual left support at least two and a nonzero singleton right correction. References to the review's (2.1), (3.2), (3.3) and (4.1) correspond respectively to (9), (4), (5) and (6) of that producer proof. This supplies the preceding context without reproducing the full review.

The quoted references to “the checker” describe the reviewer's separately reported reconstruction; that program was not downloaded or replayed locally. The package's [review_examples.py](review_examples.py) instead mechanically replays the explicit 672 support cases and three specified rational matrices using the unchanged producer API. Its local receipts are separate. The two original producer checkers were separately source-audited and replayed by Codex; the reviewer did not audit them.

---

## 5. Exhaustive four-case review

The top three rows of either invertible matrix `M` or `N` have rank 3. Four top column vectors therefore have at most one zero in each list. A zero `a_p` forces `c_p != 0`; a zero `b_k` forces `d_k != 0`, because no column of an invertible matrix is zero.

If these zeros occurred at different positions, (2.1) would give `c_p*d_k=0`, a contradiction. Thus there are exactly the following four possibilities. Permuting the displayed price coordinates is harmless.

| Case | Top-vector zeros | Proven componentwise price floor | Complete COPY floor |
|---|---|---|---:|
| A | Neither list has a zero | `(7,7,7,7)` | 68 |
| B | Only `b_p=0` | `(8,8,8,1)` | 65 |
| C, no saving | Only `a_p=0`; other three prices at least 8 | `(8,8,8,1)` | 65 |
| C, saving | Only `a_p=0`; at least one other price below 8 | `(7,7,7,6)` | 67 |
| D | `a_p=b_p=0` | `(8,8,8,0)` | 64 |

### A. No top-vector zeros

Every term has both `a_j` and `b_j` nonzero, so (4.1) applies to all four. There is no omitted low-price compensation column.

### B. A zero only on the right

Here `b_p=0`, `a_p != 0`, and `d_p != 0`. Equation (2.1) with right index `p` forces `c_j=0` for every `j != p`. The other three left factors are exactly `Ya_j`, with all `a_j,b_j` nonzero. Their right factors retain `S(b_j)\setminus{beta}`. Equations (3.3) and F2 give price at least 8 each.

The remaining right factor is the nonzero singleton `d_p*lambda*e_beta`. F4 implies `S(a_p) intersect H_beta` is nonempty; the left factor agrees with `Ya_p` there. Therefore the corresponding one-column binary matrix has a nonzero entry and rank exactly 1.

This does not claim that all possible unmodified three-mode pairs have price exactly 8: some may have price 9. Only the lower bound is needed.

### C. A zero only on the left

Here `a_p=0`, `b_p != 0`, and `c_p != 0`. There is no zero in the `b` list. Equation (2.1) with left index `p` forces `d_j=0` for all `j != p`. Thus the other three right factors are exactly `Yb_j`, and each other price is at least 7 by (4.1).

The compensation left factor has actual support `U`. Its right support can differ from `S(b_p)` only at `beta`. Since the entire binary column `B[U,{beta}]` is zero,

\[
r_p=\rho\bigl(U,\operatorname{supp}(Yb_p+d_p\lambda e_\beta)\bigr)
=\rho(U,S(b_p)). \tag{5.1}
\]

This equality is valid whether or not `beta` belongs to `S(b_p)` and whether or not the complex anchor entry cancels.

If the other three prices are all at least 8, then `r_p>=1`. Choose any `i in U`. F4 with anchor `i` implies `S(b_p) intersect H_i` is nonempty. By symmetry this supplies a nonzero entry in row `i` of `B[U,S(b_p)]`. The proof only uses that `U` is nonempty at this step; it certainly covers the requested `|U|>=2`. No broader domain is claimed in this review.

Otherwise some `j != p` has price below 8. Since its right factor is exactly `Yb_j`, the hypothesis of the compensation cut applies directly. Hence `s(U)>=7`. Equations (3.2) and (5.1) give `r_p>=6`. All other three prices remain at least 7. This proves the saving-case floor without assuming a false universal span-eight anchor bound.

### D. A common top-vector zero

Now (2.1) gives `c_p*d_p=1` and, for `j != p`, both `c_j=0` and `d_j=0`. The exceptional outer product is exactly `uv^T`, with binary price zero. The other three terms have nonzero top vectors on both sides and no correction coefficients, so F2 gives price at least 8 each.

Let `P` be the common permutation matrix moving column `p` to the last position. In the original factor basis `(Y_0,Y_1,Y_2,u)` and its right-side analogue,

\[
MP=\begin{pmatrix} A&0\\0&c\end{pmatrix},\qquad
NP=\begin{pmatrix} A^{-T}&0\\0&c^{-1}\end{pmatrix},
\quad A\in\mathrm{GL}(3,\mathbb C),\ c\ne0. \tag{5.2}
\]

No row operation or factor-basis change was made. Scaling the last left column by `c^{-1}` and the last right column by `c` normalizes the isolated pair. Applying the same, rather than reciprocal, scaling to the two factors would generally be incorrect; paired scaling here has the reciprocal meaning.

### 5.1 Zero-amplitude and zero-factor corners

Zero `c_j` and `d_j` are already allowed throughout. So are complex values that exactly cancel the anchor or entries of the left combination. However, a nonzero top vector cannot hide an identically zero whole factor: for the left side, F4 supplies an uncancelable entry in `S(a_j) intersect H_beta`; for the right side, F3 and F2 leave a support after anchor deletion whose label span is at least 8. If the top vector is zero, invertibility supplies a nonzero fourth coefficient, and the hypotheses supply nonzero `u` or `v`.

Thus all factor columns are actual nonzero complex vectors, although the isolated correction has binary **price** zero. The proof does not conflate price zero with an identically zero outer product.

## 6. Equality and the full power interval

The case table immediately proves the COPY lower bound and excludes equality outside case D. In D, all three remaining prices are at least 8, so COPY equality is equivalent to all three being exactly 8.

For powers, monotonicity applies to the **componentwise floors**, not merely to their sum. Although actual prices can be 9, the comparison values used below are at most 8. For `0<=x<=8` and `0<q<=1`, concavity gives

\[
x^q\ge 8^{q-1}x.
\]

Therefore A has mixed power at least `4*7^q >= (28/8)*8^q > 3*8^q`, and saving C has at least `3*7^q+6^q >= (27/8)*8^q > 3*8^q`. B and nonsaving C have at least `3*8^q+1`. D has at least `3*8^q`, with equality exactly when its three positive prices are 8, because `x -> x^q` is strictly increasing for every allowed `q`.

Adding the five unchanged prices proves the stated continuum result. It requires no numerical sampling of `q`. The endpoint `q=1` is included; `q=0` is excluded and no convention for `0^0` is used. The proposed warning about `(9,9,6)` correctly illustrates why a sum-only argument would not suffice for concave powers.

For `M=I`, the four mixed prices are `(8,8,8,0)`: the first three are the designated original coordinate prices, and the last is `rank B[U,{beta}]=0`. This proves attainment for every admissible correction and establishes both exact minima.

### Equality boundary controls

The checker gives a nonmonomial equality example with

\[
M=\begin{pmatrix}1&1&0&0\\0&1&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix},
\quad u=e_1+e_2,\quad \beta=0,\quad\lambda=1.
\]

Its prices are `(8,8,8,0)`, so an inference that equality forces a monomial or identity three-mode block would be false.

Conversely, the isolated matrix

\[
M=\begin{pmatrix}1&1&1&0\\1&2&3&0\\1&4&9&0\\0&0&0&1\end{pmatrix}
\]

with the same correction has prices `(9,9,9,0)` and complete COPY 67. A common zero alone is not sufficient for equality. The submitted extra condition “other three prices 8” is essential.

A further exact control moves the isolated column to position 1 and scales its left coefficient by 2, with the inverse-transpose partner computed rather than guessed. It gives `(8,0,8,8)` and complete COPY 64.

## 7. Optional refinement: the exact nonisolated penalty is one

This section is a reviewer-derived sharpening inside the same fixed model, not a repair or a broader frontier claim.

For `1<=x<=8`, the chord between 1 and 8 gives the stronger comparison

\[
x^q\ge\frac{8-x}{7}+\frac{x-1}{7}\,8^q.
\]

Writing `z=8^q>1`, the A floor satisfies

\[
4\,7^q\ge\frac47+\frac{24}{7}z
=1+3z+\frac37(z-1)>1+3z.
\]

The saving-C floor similarly satisfies

\[
3\,7^q+6^q\ge\frac57+\frac{23}{7}z
=1+3z+\frac27(z-1)>1+3z.
\]

Cases B and nonsaving C already have power at least `1+3z`. Thus every matrix without a common top-vector zero has complete power at least `8*8^q+1`.

This bound is attained for **every fixed admissible** `u`, `lambda`, and `beta`. Write `y_0=X[:,2]` and choose

\[
M=I+E_{0,3},\qquad N=I-E_{3,0}.
\]

The factors are

\[
D=[y_0,y_1,y_2,y_0+u],\qquad
T=[y_0-v,y_1,y_2,v].
\]

There is a zero top vector only on the right, so this is case B. The last price is exactly 1 by the uncancelable `S(y_0) intersect H_beta` argument. For the first term, F3 gives a lower bound 8 even if the anchor is deleted, while `s(S(y_0))=8` gives an upper bound 8 even if an anchor outside that support is added. Hence its price is exactly 8 for every nonzero complex `lambda`. The second and third terms are unchanged coordinate terms, also of price 8.

Thus the four prices are `(8,8,8,1)` universally for this unipotent choice. The nonisolated minima are exactly COPY 65 and power `8*8^q+1`. The script additionally checks all 672 combinations of designated coordinate, anchor, and forced-in/forced-out anchor support that underlie the first-term rank statement. Arbitrary complex amplitudes are covered by the two possible support states, not sampled.
