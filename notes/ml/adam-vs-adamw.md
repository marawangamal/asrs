Topic

optimization

Tags

adam,adamw,weight-decay,l2-regularization,optimizers

Name

AdamW decouples weight decay from Adam

Question

What is the primary advantage of AdamW over Adam with L2 regularization? Write the update equations and identify where the weight decay term appears.

Answer

AdamW applies weight decay directly to the weights, instead of inserting the L2 term into Adam’s gradient update. This matters because Adam adaptively rescales gradients using (v_t), so if weight decay is treated as part of the gradient, the decay strength gets distorted by (\sqrt{v_t}).

Example

Suppose we add L2 regularization:

L(\theta)
+
{\color{blue}{\frac{\lambda}{2}|\theta|_2^2}}
]

Then the regularized gradient is:

g_t
+
{\color{blue}{\lambda \theta_t}}
]

Adam with L2 regularization	AdamW
(\displaystyle m_t = \beta_1 m_{t-1} + (1-\beta_1)\left(g_t + {\color{blue}{\lambda \theta_t}}\right))	(\displaystyle m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t)
(\displaystyle v_t = \beta_2 v_{t-1} + (1-\beta_2)\left(g_t + {\color{blue}{\lambda \theta_t}}\right)^2)	(\displaystyle v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2)
(\displaystyle \theta_{t+1} = \theta_t - \eta \frac{m_t}{\sqrt{v_t}+\epsilon})	(\displaystyle \theta_{t+1} = \theta_t - \eta \frac{m_t}{\sqrt{v_t}+\epsilon} - {\color{blue}{\eta\lambda\theta_t}})

In Adam + L2, the decay term ({\color{blue}{\lambda\theta_t}}) is mixed into the gradient and then divided by (\sqrt{v_t}+\epsilon). So the effective decay strength depends on Adam’s adaptive scaling.

In AdamW, the decay term ({\color{blue}{-\eta\lambda\theta_t}}) is applied directly to the weights, separate from the adaptive gradient update. Equivalently:

(1-{\color{blue}{\eta\lambda}})\theta_t

\eta \frac{m_t}{\sqrt{v_t}+\epsilon}
]

So AdamW makes weight decay behave like true weight shrinkage: every step directly scales the weights by approximately (1-\eta\lambda).