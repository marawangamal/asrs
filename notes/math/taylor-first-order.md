## Topic
calculus
## Tags
taylor,optimization
### Name
Taylor's Theorem (First-Order)
### Question
State Taylor's Theorem (first-order, mean-value form) for a continuously differentiable $f : \mathbb{R}^n \to \mathbb{R}$ and step $p \in \mathbb{R}^n$. What does it tell you about the change in $f$?
### Answer
If $f : \mathbb{R}^n \to \mathbb{R}$ is continuously differentiable and $p \in \mathbb{R}^n$, then
$$
f(x + p) = f(x) + \nabla f(x + t p)^T p
$$
for some $t \in (0, 1)$.

**Interpretation.** The change in $f$ over the step $p$ equals the gradient at *some intermediate point* on the segment from $x$ to $x+p$, dotted with the step. It's the multivariable mean-value theorem: there's a point along the path where the directional derivative explains the whole change exactly.

This is the workhorse for descent-direction arguments: pick $p$ so that $\nabla f(x)^T p < 0$; by continuity, $\nabla f(x + tp)^T p < 0$ for small enough $\|p\|$, hence $f(x+p) < f(x)$.
