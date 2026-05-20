## Topic
linear-algebra
## Tags
norm,trace,frobenius
### Name
Norm & trace expansion
### Question
Expand the squared Frobenius norm $\|A X - B\|_F^2$ (or, for vectors, $\|Ax - b\|_2^2$) using the trace. Why is the trace form useful?
### Answer
**Scalar fact.** For any matrix $M$, $\|M\|_F^2 = \operatorname{tr}(M^T M) = \operatorname{tr}(M M^T)$.

**Expansion.**
$$
\|A X - B\|_F^2 = \operatorname{tr}\big((A X - B)^T (A X - B)\big)
$$
$$
= \operatorname{tr}(X^T A^T A X) - 2\operatorname{tr}(B^T A X) + \operatorname{tr}(B^T B).
$$

(The cross term combines via $\operatorname{tr}(X^T A^T B) = \operatorname{tr}(B^T A X)$, using cyclic invariance of the trace.)

**Vector case** ($X = x$, $B = b$):
$$
\|Ax - b\|_2^2 = x^T A^T A x - 2 b^T A x + b^T b.
$$

**Why trace.** Three reasons:

1. **It linearizes Frobenius norms** — lets you treat $\|\cdot\|_F^2$ as an inner product, so calculus and matrix identities apply directly.
2. **Cyclic invariance** $\operatorname{tr}(ABC) = \operatorname{tr}(BCA) = \operatorname{tr}(CAB)$ lets you move factors around to expose the variable you're differentiating w.r.t. or to combine terms.
3. **Matrix gradients are clean in trace form.** The handy identities
   $$
   \nabla_X \operatorname{tr}(X^T M) = M, \qquad
   \nabla_X \operatorname{tr}(X^T M X) = (M + M^T) X
   $$
   drop out immediately. Differentiating the expansion above gives the matrix normal equations $A^T A X = A^T B$ in a few lines — exactly the multivariate generalization of OLS.
