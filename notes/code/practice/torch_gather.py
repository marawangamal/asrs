"""Interview exercise: next-token log-probabilities with ``torch.gather``.

Problem
-------
An autoregressive language model produces:

* ``logits`` with shape ``[B, T, V]``. ``logits[b, t]`` predicts the token
  following input position ``t``.
* ``input_ids`` with shape ``[B, T]`` containing the token IDs fed to the
  model.

Here, ``B`` is the batch size, ``T`` is the sequence length, and ``V`` is the
vocabulary size.

1. Implement ``next_token_log_probs``. Return the log-probability assigned to
   each token in ``input_ids`` by the preceding position. The output must have
   shape ``[B, T - 1]``.

2. Implement ``completion_log_probs``. ``completion_mask`` has shape
   ``[B, T - 1]`` and contains ``True``/``1`` at next-token positions that
   belong to the completion and ``False``/``0`` elsewhere. Return the sum of
   the completion-token log-probabilities for each sequence, with shape
   ``[B]``.

Use ``torch.gather`` and do not use Python loops.
"""

from torch import Tensor


def next_token_log_probs(logits: Tensor, input_ids: Tensor) -> Tensor:
    """Return each actual next token's log-probability, shaped ``[B, T-1]``."""
    y_selected = input_ids[:, 1:].unsqueeze(-1)  # (B, T', 1)
    # (B, T', D) -> (B, T', 1)
    logp = logits.log_softmax(dim=-1)
    logp_y = logp[:, :-1].gather(dim=-1, index=y_selected)
    return logp_y.squeeze(-1)


def completion_log_probs(
    logits: Tensor,
    input_ids: Tensor,
    completion_mask: Tensor,
) -> Tensor:
    """Sum next-token log-probabilities selected by ``completion_mask``."""
    y_selected = input_ids[:, 1:]
    # (B, T, D) -> (B, T', D) -> (B, T, 1)
    logp = logits.log_softmax(dim=-1)
    logp_y = logp[:, :-1].gather(dim=-1, index=y_selected.unsqueeze(-1))  # (B, T', 1)
    # (B, T, 1) ->  (B, T) ->  (B,)
    logp_y = (logp_y.squeeze(-1) * completion_mask).sum(dim=-1)
    return logp_y
