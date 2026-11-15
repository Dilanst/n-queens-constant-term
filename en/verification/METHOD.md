# Definitions and independent checks

**A line containing one square.** On the domain where the expressions are defined, p is the weight of the
square, q=1−p, τ_d=pq/(1−dp), and b_d=(1−dp)/q^d. Schur elimination subtracts τ_d²/(q+τ_d) from τ_d
and multiplies b_d by q+τ_d. Polynomial cross-multiplication verifies that the results are τ_(d−1) and
b_(d−1), respectively, without sampling p.

**Four positions of a rectangle.** At each position the choice is q or −V. The number of V choices
determines the sign. Finite differences in four markers recover each labeled coefficient individually.
Counting eight positive and eight negative signs alone would not suffice. A second construction compares,
monomial by monomial, the sum over rectangles with the squared entries of the Gram matrix of q−V.
The 2×3 example includes degenerate rectangles.

**Prefactor.** To isolate the coefficient, take k full rows and k full columns, p=1/k, and two auxiliary
single-square lines per position. The local factor is (b₄/b₂) raised to k², and the row and column block
contributes (τ₄/τ₂) raised to r=2k−1. For the remaining block, let X be the incidence matrix of squares
against rows and columns with one redundant column removed, and let P=X(XᵀX)⁻¹Xᵀ. If Y duplicates the
coordinate of each square, the block is qI+τ₄Y(I−P)Yᵀ. It acts as qI on differences between duplicate
coordinates and as qI+2τ₄(I−P) on their sums. This gives the factors q^(k²+r) and (q+2τ₄)^(k²−r).
The constant-order coefficients of the three logarithms are evaluated using [t^j] log(1−ut)=−u^j/j
with t=1/k. They are −5, +4, and +1. Here the sum of the squared weights equals one. For k=5, the full
matrix is also assembled and its determinant calculated by Bareiss integer elimination. The error in
the nonuniform model lies outside the scope of this example.

**Histories.** For a partial placement B, Q(B) is its number of completions, and w(B)>0 is an arbitrary
weight. Let S(B,r) be the sum of the weights of the children obtained by playing in row r. The reference
law chooses the free row uniformly and the child with probability w(child)/S(B,r). If that row has no
child, the outcome is recorded as a failure, with no redraw. The other law chooses a solution and a row
ordering uniformly. For every stopped history with positive mass under the uniform law, the following
exact ratio is checked.

    μ(history)/ν(history) = Q(B_final) w(B_initial) / [Q(B_initial) w(B_final)]
                            × the product of S(B,r)/w(B) over the steps.

The uniform law is counted from complete permutations, while Q(B) is counted by legal extensions of the
partial placement. Comparing the exponents of each weight and normalizer verifies the telescoping identity
for arbitrary weights on the trees tested. The two choices of rational weights also check probability mass
and failures. Four stopping rules are tested. They stop immediately, after one move, at the first descent
in the sequence of rows, or at the end. The ratio is evaluated only when μ is positive. Taking logarithms
and averaging recovers the sign of the relative entropy in the paper. The exact equality is checked
without computing a rounded logarithm.

**Labels.** For a solution π, choosing K row labels also determines the corresponding columns π(j).
Two distinct squares (i,π(j)) and (u,π(v)) form a witness if |i−u|=|π(j)−π(v)|. They are counted as an
unordered pair. The number of labels is the size of {i,u,j,v}. With two labels, the two label pairs
coincide, and equality of the distances would contradict the assumption that π is a solution. With three
labels the pairs share one label, and with four they are disjoint. For a distance d, an independent
count uses the edges joining rows at distance d and the edges joining labels whose columns are that
distance apart. Taking the Cartesian product of the two lists gives the edge pairs, with two assignments
per pair. A witness with j labels occurs in binom(n−j,K−j) subsets of size K. The check by subsets is
independent of this multiplicity. The columns `subconjuntos_con_3` and `subconjuntos_con_4` can count
the same subset.

**Correspondence with the text.** The catalog lists readable items for each file in their original
order, including inline and displayed formulas, definitions, and numbers in the prose. A reader can
identify a discrepancy without inspecting binary values. The comparison ignores TeX comments and
differences in spacing within expressions. The program lists the number words it recognizes. Its
comparison covers selected elements of the prose and does not interpret arbitrary macros. A change to a
formula requires human review before another edition is adopted. Textual comparison and mathematical
calculation provide independent checks.

## Checks for the complete edition

For each partial placement examined, a rationally weighted mixture of its completions gives a matrix
with row and column sums equal to one. The probability of losing a square is counted directly by playing
each possible edge. This checks the triple-incidence correction, including at positions with zero
weight. For doubly stochastic circulant matrices with zeros and unequal weights, rational arithmetic
is used to compare the cofactor, the zero-mode shift, and the determinant of the centered product.
The permanent is also computed by enumerating permutations before and after scaling. The sizes and
outputs are listed in `resultados/ampliacion.json`. These tests do not approximate the asymptotic
remainder in the permanent estimate.
