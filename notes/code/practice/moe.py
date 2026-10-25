"""Interview exercise: implement a top-k mixture-of-experts (MoE) layer.

``inputs`` has shape ``[..., D]`` and ``router_weight`` has shape ``[D, E]``,
where ``E`` is the number of experts. ``expert_weights`` is a sequence of
``E`` matrices, each with shape ``[D, D_out]``.

For every input token:

1. Compute router logits and select the ``top_k`` experts.
2. Apply softmax only to the selected logits.
3. Run the token through each selected linear expert (no bias).
4. Return the routing-weighted sum with shape ``[..., D_out]``.

Tokens may choose different experts. Do not detach routing weights or use
``torch.nn`` MoE implementations.
"""

from collections.abc import Sequence

from torch import Tensor


def mixture_of_experts(
    inputs: Tensor,
    router_weight: Tensor,
    expert_weights: Sequence[Tensor],
    top_k: int,
) -> Tensor:
    """Return the top-k routed expert output for every input token."""
    raise NotImplementedError
