## Topic

deep-learning

## Tags

rmsnorm,layernorm,normalization,backpropagation,llms

### Name

RMSNorm has fewer coupled terms than LayerNorm

### Question

Why is RMSNorm often more efficient than LayerNorm in modern LLMs? Show the forward and backward equations, and identify the coupled/global reduction terms.

### Answer

RMSNorm is more efficient because it removes mean-centering and only normalizes by the root-mean-square magnitude. In the backward pass, this gives fewer coupled/global reduction terms than LayerNorm.

Let $g_i^{(y)} = \partial L / \partial y_i$ be the upstream gradient with respect to the normalized output $y$.

**RMSNorm.**

Forward:

$$
r = \sqrt{\frac{1}{d}\sum_{j=1}^{d} x_j^2+\epsilon}
$$

$$
y_i = \frac{x_i}{r}
$$

Backward:

$$
\frac{\partial L}{\partial x_i}
= \frac{g_i^{(y)}}{r}
- \frac{x_i}{d r^3}
{\color{red}{\sum_{j=1}^{d} g_j^{(y)}x_j}}
$$

The coupled/global reduction term is:

$$
{\color{red}{\sum_{j=1}^{d} g_j^{(y)}x_j}}
$$

So RMSNorm needs one main global sum in the backward pass.

**LayerNorm.**

Forward:

$$
\mu = \frac{1}{d}\sum_{j=1}^{d} x_j
$$

$$
\sigma = \sqrt{\frac{1}{d}\sum_{j=1}^{d}(x_j-\mu)^2+\epsilon}
$$

$$
\hat{x}_i = \frac{x_i-\mu}{\sigma}
$$

$$
y_i = \hat{x}_i
$$

Backward:

$$
\frac{\partial L}{\partial x_i}
= \frac{1}{\sigma}
\left[
g_i^{(y)}
- {\color{red}{\frac{1}{d}\sum_{j=1}^{d} g_j^{(y)}}}
- \hat{x}_i
{\color{red}{\frac{1}{d}\sum_{j=1}^{d} g_j^{(y)}\hat{x}_j}}
\right]
$$

The coupled/global reduction terms are:

$$
{\color{red}{\sum_{j=1}^{d} g_j^{(y)}}}
$$

and

$$
{\color{red}{\sum_{j=1}^{d} g_j^{(y)}\hat{x}_j}}
$$

So LayerNorm needs two main global sums in the backward pass.

These global sums are computed once per normalized vector and reused for all coordinates $i$. The difference is that RMSNorm has fewer coupled terms and fewer intermediate quantities: it only needs the RMS scale, while LayerNorm needs both the mean-centering path and the variance-rescaling path.

In short, LayerNorm backpropagates through both $\mu$ and $\sigma$, while RMSNorm only backpropagates through $r$. This makes RMSNorm's backward pass simpler and typically faster.
