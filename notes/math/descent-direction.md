## Topic
optimization
## Tags
gradient,descent
### Name
Descent direction condition
### Question
If $\nabla f(x + t p)^T p < 0$ for some $t \in (0, 1)$, what does that tell you about $f$ in the direction $p$?
### Answer
$f$ **decreases** along $p$ — i.e. $f(x + p) < f(x)$.

This follows from the first-order Taylor expansion:
$$
f(x + p) = f(x) + \nabla f(x + t p)^T p < f(x).
$$

The practical version: a direction $p$ is a **descent direction** at $x$ if $\nabla f(x)^T p < 0$; by continuity, the inequality survives at some nearby $x + tp$ for small enough $\|p\|$, so taking a small step in $p$ strictly decreases $f$. All of gradient descent, Newton's method, and quasi-Newton methods are about picking such a $p$.
