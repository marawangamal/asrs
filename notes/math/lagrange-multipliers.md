## Topic
optimization
## Tags
constrained,kkt
### Name
Lagrange multipliers
### Question
What are Lagrange multipliers, and how do you use them to solve a constrained optimization problem
$$
\min_x f(x) \quad \text{subject to} \quad g_i(x) = 0,\ i = 1, \dots, m?
$$
### Answer
**Idea.** At a constrained minimum, you can't decrease $f$ without leaving the feasible set. That means the gradient of $f$ has no component *along* the constraint surface — it must lie entirely in the span of the constraint gradients $\nabla g_i$.

**Lagrangian.** Define
$$
\mathcal{L}(x, \lambda) = f(x) - \sum_{i=1}^{m} \lambda_i\, g_i(x).
$$
A regular local minimum $x^*$ of the constrained problem satisfies the first-order conditions
$$
\nabla_x \mathcal{L}(x^*, \lambda^*) = 0 \quad\Longleftrightarrow\quad \nabla f(x^*) = \sum_i \lambda_i^*\, \nabla g_i(x^*),
$$
$$
g_i(x^*) = 0 \text{ for all } i.
$$
The scalars $\lambda_i^*$ are the **Lagrange multipliers**. Geometrically, $\nabla f$ is a linear combination of $\nabla g_i$ at the optimum — the level set of $f$ is tangent to the constraint surface.

**Interpretation of $\lambda_i$.** Sensitivity (shadow price): $\lambda_i^*$ is the rate of change of the optimal value if you relax constraint $i$. If the constraint is $g_i(x) = b_i$, then $\partial f^* / \partial b_i = \lambda_i^*$.

**Inequality constraints.** With $h_j(x) \le 0$, this generalizes to **KKT**: stationarity ($\nabla_x \mathcal{L} = 0$), primal feasibility ($g_i = 0$, $h_j \le 0$), dual feasibility ($\mu_j \ge 0$), and complementary slackness ($\mu_j h_j = 0$). Necessary under a constraint qualification; sufficient for convex problems.

**Recipe.**
1. Write $\mathcal{L}$.
2. Set $\nabla_x \mathcal{L} = 0$ and use $g_i(x) = 0$ to get a system in $(x, \lambda)$.
3. Solve, check feasibility and second-order conditions if multiple stationary points appear.
