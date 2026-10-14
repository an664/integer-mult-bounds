# A complete singleton-target obstruction for the fixed three-mode P112 problem

**Research:** Andrey Mas with substantial GPT-6 Pro assistance through ChatGPT.

**Scope:** CrocSwap/integer-mult-bounds Discussion 1550; the first singleton-side question identified in the supplied PR1512 handoff.

**Result type:** A universal mathematical reduction with completely enumerated, exact finite geometry premises. Not a formal proof-assistant development and not an independent human review.

## 1. Claim

All coordinate and live-root indices are zero-based, and all dots and transposes are ordinary bilinear operations, without conjugation. Start with the 120 integer vectors consisting of the 56 vectors \(2e_i+2s e_j\), for \(0\le i<j<8\) and \(s\in\{-1,1\}\), and the 64 vectors \((1,s_1,\ldots,s_7)\) with an even number of minus signs. Define

\[
f_{2j}=2e_{2j}+2e_{2j+1},\qquad
f_{2j+1}=2e_{2j}-2e_{2j+1},\qquad 0\le j<4.
\]

Delete these eight frame vectors and lexicographically sort the remaining vectors as \(r_0,\ldots,r_{111}\). Set

\[
G_{ij}=\frac{r_i\cdot r_j}{4},\qquad
X_{ik}=\frac{r_i\cdot f_k}{4},\qquad
B_{ij}=(1+G_{ij})\bmod2\in\{0,1\}.
\]

Every support below means actual nonzero complex entries, not coefficient support modulo two. Let

\[
J=(2,4,5),\qquad Y=X[:,J],\qquad
v=\lambda e_\beta,\quad \lambda\in\mathbb C\setminus\{0\}.
\]

Let \(u\in\mathbb C^{112}\) have actual support \(U\), with \(|U|\ge2\) and \(B[U,\{\beta\}]=0\). For arbitrary \(M\in\mathrm{GL}_4(\mathbb C)\), put

\[
N=M^{-T},\qquad D=[Y,u]M,\qquad T=[Y,v]N.
\]

Since \(MN^T=I_4\), the four terms satisfy \(DT^T=YY^T+uv^T\). Adding the unchanged five coordinate terms gives \(2G+uv^T\). The correction is zero on every constrained entry with \(B_{ij}=1\), by its singleton right support and the condition \(B[U,\{\beta\}]=0\). Define the **four** mixed prices by

\[
r_j=\operatorname{rank}_{\mathbb F_2}
 B[\operatorname{supp}D[:,j],\operatorname{supp}T[:,j]],
\quad j=0,1,2,3.
\]

Then

\[
\boxed{40+\sum_{j=0}^3r_j\ge64}
\]

and, separately, for every real \(0<q\le1\),

\[
\boxed{5\,8^q+\sum_{j=0}^3r_j^q\ge8\,8^q.}
\]

Both lower bounds are attained by \(M=I_4\), for every admissible \(u,v\). Thus the exact minima in the stated algebraic relaxation are 64 and \(8\,8^q\), respectively.

There is also an equality restriction. Write the columns of \(M,N\) as

\[
m_j=\binom{a_j}{c_j},\qquad n_j=\binom{b_j}{d_j},
\quad a_j,b_j\in\mathbb C^3.
\]

Equality in either bill is possible only when some column \(p\) has **both** \(a_p=0\) and \(b_p=0\), and each of the other three term prices is 8. In that case the correction is isolated as a scalar-rescaled factor pair; after a common column permutation, the factor transformation is block diagonal between the three coordinate modes and the correction. If no such common zero column exists, the complete COPY bill is at least 65 and the complete power bill is strictly above baseline for every allowed \(q\).

No claim is made about other triples of modes, more than three modes, multiple corrections, all-nine-factor GL9 mixing, shared COPY billing, or physical supplier recurrences.

## 2. Binary labels and exact finite premises

For an index set \(A\), define

\[
L(A)=\operatorname{span}_{\mathbb F_2}\{B[i,:]:i\in A\},
\qquad s(A)=\dim L(A).
\]

Throughout, \(\rho(A,C)=\operatorname{rank}_{\mathbb F_2}B[A,C]\), with rank zero when either set is empty.

Let \(W=L(\{0,\ldots,111\})\). The rebuilt geometry has symmetric \(B\) and \(\dim W=9\). These 112-bit row vectors are an exact label model; they are not the complex coefficient vectors of a factor. For \(a\ne0\), write

\[
S(a)=\operatorname{supp}(Ya),\qquad
H_\beta=\{i:B_{i\beta}=1\}.
\]

The following finite statements are checked from the root construction, not assumed from a search failure.

**F1. Geometry and original prices.** The construction has 112 roots, \(X\) has entries in \(\{0,\pm1\}\), \(XX^T=2G\), rational and hence complex rank \(X=8\), binary rank \(B=9\), and every original coordinate term has price 8. The computed geometry digest equals the supplied digest:

```text
384dd5b48cfd306667deafa09f58255f39a8099e609122dc695fe4ce416b2115
```

The precise serialization is Python `json.dumps({"roots": roots, "X": X, "B": B}, sort_keys=True)`, with its default separators, UTF-8 encoded. Each entry of `B` is an integer row mask, with bit \(i\) corresponding to root \(r_i\).

**F2. All nonzero complex coordinate-combination supports.** There are exactly 39 possible sets \(S(a)\). Three have label span 8; the other 36 have label span 9. For all ordered pairs of these supports,

\[
\rho(S(a),S(b))\ge8.
\]

The 1,521 pairings comprise 225 ranks of 8 and 1,296 ranks of 9.

**F3. One-point deletion.** For every one of the 39 supports and every live index \(\beta\),

\[
L(S(a)\setminus\{\beta\})=L(S(a)).
\]

There are 4,368 checked instances, including the trivial instances where \(\beta\notin S(a)\).

**F4. Mandatory singleton-anchor pairing.** For every nonzero \(a,b\) and every live \(\beta\),

\[
\rho(S(a)\cap H_\beta,S(b))\ge7.
\tag{1}
\]

The 170,352 stratum/anchor/stratum instances comprise 19,464 ranks of 7 and 150,888 ranks of 8. In particular, every \(S(a)\cap H_\beta\) is nonempty.

**F5. Nonempty binary-functional cuts are large in label span.** For every one of the 39 supports \(S\), and every \(w\in W\),

\[
E=S\cap\operatorname{supp}(w)\ne\varnothing
\quad\Longrightarrow\quad s(E)\ge7.
\tag{2}
\]

The checker enumerates all 512 words of the nine-dimensional binary row space. Among the 39 times 512 pairs, there are 19,926 nonempty cuts: 1,563 have span 7, 18,327 have span 8, and 36 have span 9. The other 42 cuts are empty and are explicitly excluded from (2). As an additional check, the minimum nonempty cut cardinality is 12, although the proof uses the stronger label-span fact, not this cardinality.

For example, the coefficient \((0,0,1)\), row-space word `0xffffffff000ffffff`, and cut `0x3c3c3c3c000c3c3ff` witness span exactly 7. Thus replacing the lower bound in (2) by 8 would be false.

### Why these 39 cases cover arbitrary complex coefficients

The nonzero rows of \(Y\), modulo nonzero scalar multiples, are the 13 directions represented by nonzero triples in \(\{0,\pm1\}^3\) modulo sign. Fix any \(a\in\mathbb C^3\setminus\{0\}\). The rational directions with \(y\cdot a=0\) have rational span of dimension at most 2: three rationally independent such rows would also be complex-linearly independent, forcing \(a=0\).

Let \(F\) be their rational span. A row direction belonging to \(F\) also annihilates \(a\). Consequently the zero set is exactly the set of row directions in this rational subspace. Such a subspace is generated by zero, one, or two of the 13 directions. The checkers enumerate their closures: one rank-zero flat, thirteen rank-one flats, and twenty-five rank-two flats.

The 39 supplied rational representatives are then checked to realize all 39 resulting supports, with the supplied masks, sizes, and spans. This proves completeness over \(\mathbb C\); it is not bounded-coefficient sampling. The second checker obtains the support sets directly from flats without using those representatives.

### The one-anchor loss classification

Deleting every free-to-\(\beta\) index means retaining \(S(a)\cap H_\beta\). The complete label-span classification is:

* Each of the three coordinate strata drops from 8 to 7 at all 112 anchors: 336 instances.
* Among the 36 span-nine strata, 4,024 instances drop from 9 to 8.
* The other eight instances drop from 9 to 7:

| Coefficient representative | Individual anchors with span \(9\to7\) |
|---|---|
| \((1,-1,-1)\) | 8, 16 |
| \((1,-1,1)\) | 9, 17 |
| \((1,1,-1)\) | 14, 22 |
| \((1,1,1)\) | 15, 23 |

Each listed anchor is a separate singleton-anchor instance. This table is not an assertion about erasing two anchors simultaneously. The total mandatory-span histogram is 344 instances of span 7 and 4,024 of span 8. These losses alone do not decide any complete bill.

## 3. Three elementary consequences

### 3.1 Restriction loses at most one label dimension against a nonzero coordinate combination

For any right index set \(C\), restriction defines

\[
\pi_C:W\longrightarrow\mathbb F_2^C.
\]

Symmetry of \(B\) gives

\[
\dim\pi_C(W)=\operatorname{rank}B[:,C]=s(C).
\]

Hence, for any \(A,C\),

\[
\rho(A,C)=\dim\pi_C(L(A))\ge s(A)+s(C)-9.
\tag{3}
\]

In particular, since \(s(S(b))\ge8\) for \(b\ne0\),

\[
\rho(A,S(b))\ge s(A)-1.
\tag{4}
\]

Also, F3 and symmetry imply, for every left set \(A\),

\[
\rho(A,S(b)\setminus\{\beta\})=\rho(A,S(b)).
\tag{5}
\]

Indeed, the removed row label is a binary linear combination of the retained labels, so the corresponding full column of symmetric \(B\) is the same linear combination of retained columns. Restricting the rows to \(A\) preserves that relation.

### 3.2 Every term with both coordinate coefficient vectors nonzero costs at least seven

Actual complex supports satisfy

\[
\operatorname{supp}(Ya+c u)\supseteq S(a)\cap H_\beta,
\]

because \(u_i=0\) on \(H_\beta\). Likewise,

\[
\operatorname{supp}(Yb+d\lambda e_\beta)
\supseteq S(b)\setminus\{\beta\}.
\]

For \(a,b\ne0\), monotonicity of binary submatrix rank, followed by (5) and F4, therefore gives

\[
\rho(\operatorname{supp}(Ya+c u),
     \operatorname{supp}(Yb+d\lambda e_\beta))\ge7.
\tag{6}
\]

There is no assumption about signs or sizes of the complex amplitudes.

### 3.3 Any price-saving left cancellation forces \(s(U)\ge7\)

Suppose \(a,b\ne0\) and

\[
\rho(\operatorname{supp}(Ya+c u),S(b))<8.
\tag{7}
\]

Put \(A=S(a)\), \(K=\operatorname{supp}(Ya+c u)\), and \(C=S(b)\). By F2 the span of the rows \(B[A,C]\) has dimension at least 8, while by (7) the span of \(B[K,C]\) has dimension at most 7. Thus there is a binary linear functional on \(\mathbb F_2^C\) that vanishes on all rows indexed by \(K\) but not on all rows indexed by \(A\).

Represent it by a vector \(h\) supported in \(C\), and put \(w=Bh\), as a 112-coordinate binary vector. Since \(B\) is symmetric, \(w\) belongs to its row space \(W\). The cut

\[
E=A\cap\operatorname{supp}(w)
\]

is nonempty and disjoint from \(K\). Therefore

\[
E\subseteq A\setminus K\subseteq U.
\]

The last containment uses only actual cancellation: outside \(U\), the new factor still equals \(Ya\). F5 now yields

\[
\boxed{s(U)\ge s(E)\ge7.}
\tag{8}
\]

This is the compensation mechanism. A binary rank saving requires erasing a whole nonempty functional cut, not merely choosing a favorable support container. No reduction of the complex amplitudes modulo two occurs in this argument.

## 4. Exhaustive coupling analysis for \(M^{-T}\)

The dual columns satisfy the ordinary bilinear equations

\[
a_j\cdot b_k+c_jd_k=\delta_{jk}.
\tag{9}
\]

The top three rows of each invertible matrix \(M,N\) have rank 3. Accordingly, each list \((a_j)\) and \((b_j)\) has at most one zero member. If \(a_p=0\), then \(c_p\ne0\). If \(b_k=0\), then \(d_k\ne0\). Equation (9) forbids these two zeros from occurring at different columns: \(c_pd_k\ne0\) would contradict \(\delta_{pk}=0\).

There are exactly four cases.

### Case A: No zero \(a_j\), and no zero \(b_j\)

All four terms satisfy (6). Thus

\[
(r_0,r_1,r_2,r_3)\ge(7,7,7,7),\qquad \sum r_j\ge28.
\tag{10}
\]

### Case B: A column has \(b_p=0\), but \(a_p\ne0\)

Equation (9), paired with column \(p\) of \(N\), gives \(c_j=0\) for \(j\ne p\). Thus the other three left factors are unmodified coordinate combinations \(Ya_j\). Their right factors differ from \(Yb_j\) only at \(\beta\), so F2 and (5) give price at least 8 each.

The remaining right factor is the nonzero singleton \(d_p\lambda e_\beta\). F4 ensures that \(S(a_p)\cap H_\beta\) is nonempty. On this set \(Ya_p+c_pu\) cannot vanish, and its binary pairing with column \(\beta\) contains a one. Hence the remaining price is exactly 1:

\[
(r_j)\ge(8,8,8,1)
\]

up to ordering. The complete COPY bill is at least 65.

### Case C: A column has \(a_p=0\), but \(b_p\ne0\)

Now \(D[:,p]=c_pu\), while (9) gives \(d_j=0\) for \(j\ne p\). The other three right factors are therefore exactly \(Yb_j\). Their coordinate coefficient vectors on both sides are nonzero.

Since \(B[U,\{\beta\}]=0\), the compensating term has the exact price

\[
r_p=\rho(U,\operatorname{supp}(Yb_p+d_p\lambda e_\beta))
    =\rho(U,S(b_p)).
\tag{11}
\]

This equality retains the entire compensation; it merely observes that changing the presence of the zero column \(B[U,\{\beta\}]\) cannot change its rank.

If the other three prices are all at least 8, then \(r_p\ge1\). Indeed, choose any \(i\in U\). F4 applied with anchor \(i\) shows that \(S(b_p)\) contains an index pairing nontrivially with \(i\). Thus this subcase has a lower price vector \((8,8,8,1)\).

Otherwise one of those three prices is below 8. Section 3.3 then forces \(s(U)\ge7\). Equations (4) and (11) give \(r_p\ge6\), while (6) gives price at least 7 for each of the other three terms. Consequently

\[
(r_j)\ge(7,7,7,6),\qquad \sum r_j\ge27,
\tag{12}
\]

up to ordering. The complete COPY bill is at least 67 in this rank-saving subcase.

### Case D: A common column has \(a_p=b_p=0\)

Equation (9) gives \(c_pd_p=1\) and \(c_j=d_j=0\) for \(j\ne p\). The pure correction term is \(u v^T\) and has price zero. The other three terms are unmodified coordinate-combination pairs, each of price at least 8 by F2. Thus the lower price vector is \((8,8,8,0)\).

This proves the COPY bound and the stated equality restriction. In particular, the only possibly optimal configurations isolate the correction rather than exploit it to reduce coordinate prices.

## 5. The separate power bill

A rank-sum bound alone would not suffice: ranks \((9,9,6)\) sum to 24, but at \(q=1/2\),

\[
9^q+9^q+6^q=6+\sqrt6<3\sqrt8.
\]

Instead use the componentwise lower vectors just proved. For every \(0\le x\le8\) and \(0<q\le1\),

\[
x^q\ge 8^{q-1}x,
\tag{13}
\]

with zero handled by the stipulated convention. This follows from the fact that \(x^{q-1}\ge8^{q-1}\) for \(0<x\le8\).

In Cases B and the nonsaving subcase of C, three prices are at least 8 and the fourth is at least 1. Their power sum is at least \(3\,8^q+1\), strictly above the mixed baseline.

In Case A, monotonicity and (13) give

\[
\sum r_j^q\ge4\,7^q\ge\frac{28}{8}\,8^q>3\,8^q.
\]

In the saving subcase of C,

\[
\sum r_j^q\ge3\,7^q+6^q
\ge\frac{27}{8}\,8^q>3\,8^q.
\]

In Case D, the three noncorrection prices are at least 8, so their power sum is at least \(3\,8^q\); equality requires all three to be exactly 8. Adding the unchanged five terms proves the power claim for the entire continuum \(0<q\le1\), without sampling exponents.

## 6. Exact fixtures and the compensation trap

The archive includes five explicit rational fixtures. Each is checked using actual factor values, their exact nonzero supports, the complete identity, every constrained entry, and all four mixed ranks. They are examples and regression tests, not a substitute for the universal proof.

All use \(\beta=0\), \(\lambda=1\). For four fixtures, \(u=e_1+e_2\); both indices are free to anchor zero in the specified sorted geometry.

| Fixture | Four mixed ranks | Complete COPY |
|---|---:|---:|
| Identity mixing | 8, 8, 8, 0 | 64 |
| Pure-left correction, without a saving | 8, 8, 8, 2 | 66 |
| Coordinate cancellation, with compensation paid | 7, 8, 8, 7 | 70 |
| Pure-right target term | 8, 8, 8, 1 | 65 |
| Four nonzero coordinate pairs | 9, 8, 8, 9 | 74 |

The third fixture is particularly relevant. Write the first column of \(Y\), which is \(X[:,2]\), as \(y_0\). Set

\[
u_i=\begin{cases}-y_{0,i},&B_{i0}=0,\\0,&B_{i0}=1,\end{cases}
\qquad
M=\begin{pmatrix}
1&0&0&0\\
0&1&0&0\\
0&0&1&0\\
1&0&0&1
\end{pmatrix}.
\]

Then

\[
D=[y_0+u,y_1,y_2,u],\qquad
T=[y_0,y_1,y_2,e_0-y_0].
\]

The actual support of \(u\) has 24 indices and binary label span 7. Its cancellation lowers the first mixed price to 7, but the complete compensating term \(u(e_0-y_0)^T\) has price 7 as well. The complete COPY bill is

\[
40+7+8+8+7=70,
\]

not the spurious 63 obtained by dropping that last term. Its complete power bill is \(7\,8^q+2\,7^q\), also above baseline by the established argument.

## 7. Verification boundary and scope

The producing GPT-6 Pro session recomputed the finite geometry assertions with both supplied standard-library programs under Python 3.13.5. Codex subsequently audited both complete programs and replayed each under local CPython 3.12.14 in normal and optimized modes. All four local runs passed; stdout was byte-identical between modes for each checker and agreed with the producing-session result except for the recorded Python version. REPLAY.json records the local commands, timings and exact source hashes. No dependency was installed.

The primary checker reconstructs the geometry, verifies the copied support table, enumerates every proper flat and every binary row-space word, checks the finite premises, checks five exact rational fixtures, and runs nine rejection controls. The second checker independently generates the geometry and flats, uses a nine-bit label model with an explicitly inverted binary pairing matrix, and checks rational fixtures by adjugate inversion rather than the primary Gaussian inversion. It does not import the primary checker or use the copied coefficient representatives to generate its finite cases.

These are algorithmically distinct checks by the **same assistant**, not independent authorship, independent human review, or kernel verification. The universal proof still relies on the written arguments connecting finite supports to arbitrary complex coefficients, the binary cut lemma, and the exhaustive dual-column cases. No finite sampling of \(u\), \(M\), or \(q\) is presented as a proof of universality.

The result already applies in the favorable zero-added-overhead relaxation specified in the question. Therefore that relaxation admits no improvement in either separate bill in this fixed scope. There is no reason to pursue physical synthesis for an improvement within this same ansatz. This conclusion does not assert physical admission of any new construction, paid hosting or restoration feasibility, a supplier recurrence, or a new multiplication exponent or kappa value.

The geometry, existing 39-stratum classification, COPY benchmark, pairing-price convention, and earlier two-mode and two-sided obstructions are predecessor material, not claimed anew. The substantive contribution here is the nonempty-functional-cut compensation argument, its exact finite verification for this geometry, and the resulting complete singleton-target three-mode obstruction. See `SOURCES.md` for the supplied attribution and pinned provenance.
