"""Interview exercise: implement the clipped PPO policy loss for an LLM.

The current and sampling policies assign log-probabilities to the same sampled
tokens:

* ``token_log_probs`` has shape ``[B, T]`` and comes from the current policy.
* ``old_token_log_probs`` has shape ``[B, T]`` and comes from the policy that
  sampled the completions.
* ``completion_mask`` has shape ``[B, T]`` and is true only for completion
  tokens.
* ``advantages`` has shape ``[B]`` and provides one advantage per completion.

For every token, compute:

```
ratio = exp(token_log_prob - old_token_log_prob)
surrogate = ratio * advantage
clipped_surrogate = clamp(ratio, 1 - epsilon, 1 + epsilon) * advantage
```

The loss is the negative masked mean of
``minimum(surrogate, clipped_surrogate)`` over completion tokens.

Constraints:

* Do not use Python loops.
* Prompt and padding tokens must not affect the loss.
* Gradients must flow only into ``token_log_probs``. Treat the old
  log-probabilities and advantages as fixed targets.
"""

from torch import Tensor
import torch


def ppo_policy_loss(
    token_log_probs: Tensor,
    old_token_log_probs: Tensor,
    completion_mask: Tensor,
    advantages: Tensor,  # (B,)
    epsilon: float,
) -> Tensor:
    """Return the scalar clipped PPO policy loss over completion tokens."""
    ratio = torch.exp(token_log_probs - old_token_log_probs.detach())  # (B, T)
    surrogate = ratio * advantages[:, None].detach()  # (B, T)
    clipped_surrogate = (
        torch.clamp(ratio, 1 - epsilon, 1 + epsilon) * advantages[:, None].detach()
    )  # (B, T)
    objective = -torch.minimum(surrogate, clipped_surrogate)
    return (objective.masked_fill(~completion_mask, 0) / completion_mask.sum()).sum()
