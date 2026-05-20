## Topic
linear-algebra
## Tags
regression,least-squares
### Name
Linear regression closed-form solution
### Question
Derive the closed-form solution to ordinary least squares: given design matrix $X \in \mathbb{R}^{n \times d}$ and targets $y \in \mathbb{R}^n$, find $\beta^* = \arg\min_\beta \|y - X\beta\|_2^2$.
### Answer
**Set up the objective.**
$$
L(\beta) = \|y - X\beta\|_2^2 = (y - X\beta)^T(y - X\beta) = y^T y - 2 y^T X \beta + \beta^T X^T X \beta.
$$

**Gradient.**
$$
\nabla_\beta L = -2 X^T y + 2 X^T X \beta.
$$

**First-order condition.** Set $\nabla_\beta L = 0$:
$$
X^T X \beta^* = X^T y \quad\text{(the \emph{normal equations})}.
$$

**Solution.** If $X^T X$ is invertible (equivalently, $X$ has full column rank):
$$
\boxed{\beta^* = (X^T X)^{-1} X^T y.}
$$

If $X^T X$ is singular (collinear columns, $n < d$), use the Moore–Penrose pseudoinverse: $\beta^* = X^+ y$, which picks the minimum-norm solution among the infinitely many.

**Geometric reading.** $X\beta^*$ is the orthogonal projection of $y$ onto $\operatorname{col}(X)$. The residual $y - X\beta^*$ is orthogonal to every column of $X$, which is exactly what $X^T(y - X\beta^*) = 0$ — i.e., the normal equations — says.

**Practical note.** Never literally compute $(X^T X)^{-1}$ — solve the normal equations with Cholesky on $X^T X$, or better, use a QR or SVD factorization of $X$ directly for numerical stability. With regularization (ridge), it becomes $\beta^* = (X^T X + \lambda I)^{-1} X^T y$, which is always invertible for $\lambda > 0$.
