## Topic
linear-algebra
## Tags
column-space,factorization
### Name
Column space ⟺ matrix factorization
### Question
State the equivalence between "every column of $X$ lies in the column space of $U$" and a matrix factorization of $X$ through $U$. Why is it true?
### Answer
$$
\operatorname{col}(X) \subseteq \operatorname{col}(U) \iff X = U A \text{ for some matrix } A.
$$

**Why.** Right-multiplying $U$ by a vector produces a linear combination of the columns of $U$. So column $j$ of $X$ being in $\operatorname{col}(U)$ means $x_j = U a_j$ for some coefficient vector $a_j$. Stack those $a_j$ as the columns of $A$ and you get $X = UA$. The converse is immediate: every column of $UA$ is $U$ times a vector, hence in $\operatorname{col}(U)$.

This is the underlying reason **low-rank factorizations** work: writing $X = U A$ with $U \in \mathbb{R}^{m \times r}$ is equivalent to claiming the columns of $X$ live in an $r$-dimensional subspace spanned by the columns of $U$. PCA, matrix completion, and bottleneck layers all exploit this.
