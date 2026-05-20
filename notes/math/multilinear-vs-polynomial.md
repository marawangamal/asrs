## Topic
algebra
## Tags
functions,polynomials,multilinear
### Name
Multilinear vs linear vs polynomial vs monomial
### Question
Define each of the following and distinguish them: **monomial**, **polynomial**, **homogeneous polynomial**, **linear**, **affine**, **multivariate linear**, **bilinear**, **multilinear ($k$-linear)**, **quadratic form**.
### Answer

| Name | Definition | Example |
|---|---|---|
| **Monomial** | One term: coefficient $\times$ variables to non-negative integer powers. Degree = sum of exponents. | $3x^2 y$ (degree 3) |
| **Polynomial** | Finite sum of monomials. Degree = max monomial degree. | $3x^2 + 2xy - 5$ |
| **Homogeneous polynomial (deg $d$)** | Polynomial whose every monomial has total degree $d$. Equivalently $p(\alpha x) = \alpha^d p(x)$. | $x^2 + xy + y^2$ |
| **Linear** | $f(\alpha x + \beta y) = \alpha f(x) + \beta f(y)$. Forces $f(0)=0$. Homogeneous degree-1 polynomial. | $f(\mathbf{x}) = \mathbf{a}^\top \mathbf{x}$ |
| **Affine** | Linear + constant. **Not** linear unless $b=0$. The school "$ax+b$" lives here. | $f(\mathbf{x}) = A\mathbf{x} + b$ |
| **Multivariate linear** | Linear map $\mathbb{R}^n \to \mathbb{R}$. One vector input — *is* linear. | $a_1 x_1 + \cdots + a_n x_n$ |
| **Bilinear** | $B(\cdot, \cdot)$ linear in each argument separately. **Not** linear on $V\times W$ (degree 2). | $B(x,y) = x^\top M y$ |
| **Multilinear ($k$-linear)** | Linear in each of $k$ slots separately. Homogeneous of total degree $k$ — not linear for $k\ge 2$. | $\det(v_1,\dots,v_n)$ |
| **Quadratic form** | Homogeneous degree-2 polynomial in one vector. Arises as $B(x,x)$ from a symmetric bilinear form. | $q(\mathbf{x}) = \mathbf{x}^\top A \mathbf{x}$ |

**Trap.** *Multilinear* $\neq$ "linear in many variables." Multilinear = linear in each slot *separately*; the map itself is degree $k$, not degree 1. *Multivariate linear* is the honestly-linear one (one vector input). Stats sometimes calls "multiple linear regression" *multilinear regression* — colliding usage.
