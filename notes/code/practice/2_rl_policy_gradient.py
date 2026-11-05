"""Interview exercise: implement an LLM policy-gradient loss.

The policy has already produced the log-probability of every sampled token:

* ``token_log_probs`` has shape ``[B, T]``.
* ``completion_mask`` has shape ``[B, T]`` and is true only for sampled
  completion tokens. Prompt and padding positions are false.
* ``advantages`` has shape ``[B]`` and provides one advantage per completion.

For each sequence, sum the log-probabilities of its completion tokens. Multiply
that sum by the sequence advantage, average over the batch, and negate the
result so it can be minimized:

``loss = -mean(advantage * sum(completion token log-probabilities))``

Constraints:

* Do not use Python loops.
* Prompt and padding tokens must not affect the loss.
* Treat advantages as fixed targets; gradients must not flow into them.
* Preserve gradients to the selected completion-token log-probabilities.
"""

from torch import Tensor


def policy_gradient_loss(
    token_log_probs: Tensor,
    completion_mask: Tensor,
    advantages: Tensor,
) -> Tensor:
    """Return the scalar completion-level policy-gradient loss."""
    completion_log_probs = token_log_probs.masked_fill(~completion_mask, 0).sum(
        dim=-1
    )  # (B,)
    return -(advantages.detach() * completion_log_probs).mean()
