## Topic
calculus
## Tags
taylor,hessian
### Name
Taylor's Theorem (Integral Form, Hessian)
### Question
For a twice continuously differentiable $f : \mathbb{R}^n \to \mathbb{R}$, write the integral form of Taylor's theorem for the gradient $\nabla f(x + p)$. What kinematic analogy does it match?
### Answer
$$
\nabla f(x + p) = \nabla f(x) + \int_{0}^{1} \nabla^2 f(x + t p)\, p \, dt.
$$

**Kinematic analogy.** Treat the gradient as a velocity and the Hessian-times-step as an acceleration:
$$
\text{Final velocity} = \text{Initial velocity} + \int \text{Acceleration}\, dt.
$$

Why it matters: it's the gradient version of the integral mean-value Taylor expansion. Used to derive convergence rates for second-order methods (the curvature $\nabla^2 f$ along the path between iterates controls the gradient change), and to bound $\|\nabla f(x+p) - \nabla f(x)\|$ using a Lipschitz constant for $\nabla^2 f$ or for $\nabla f$ (L-smoothness).
