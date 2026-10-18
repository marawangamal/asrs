"""Interview exercise: next-token log-probabilities with ``torch.gather``.

Problem
-------
An autoregressive language model produces:

* ``logits`` with shape ``[B, T, V]``. ``logits[b, t]`` predicts the token
  following input position ``t``.
* ``input_ids`` with shape ``[B, T]`` containing the tokens fed to the model.

Implement ``next_token_log_probs`` so it returns the log-probability assigned
to every actual next token. The result must have shape ``[B, T - 1]``.

Requirements:

1. Align the logits at position ``t`` with the target token at ``t + 1``.
2. Convert logits to log-probabilities in a numerically stable way.
3. Use ``torch.gather`` to select the target token without Python loops.

Follow-up
---------
Given a boolean or numeric mask with shape ``[B, T - 1]`` identifying
completion tokens, return the summed completion log-probability for each
sequence (shape ``[B]``).
"""

import torch
from torch import Tensor


def next_token_log_probs(logits: Tensor, input_ids: Tensor) -> Tensor:
    """Return each actual next token's log-probability, shaped ``[B, T-1]``."""

    raise NotImplementedError


def completion_log_probs(
    logits: Tensor,
    input_ids: Tensor,
    completion_mask: Tensor,
) -> Tensor:
    """Sum next-token log-probabilities selected by ``completion_mask``."""
    raise NotImplementedError
