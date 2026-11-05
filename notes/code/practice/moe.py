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

import torch
from torch import Tensor


def mixture_of_experts(
    inputs: Tensor,
    router_weight: Tensor,
    expert_weights: Sequence[Tensor],
    top_k: int,
) -> Tensor:
    """Return the top-k routed expert output for every input token."""
    alphas = torch.einsum("...d,de->...e", inputs, router_weight)  # (*, E)
    topk_vals, topk_ids = torch.topk(alphas, top_k, dim=-1)  # (*, K), (*, K)
    topk_vals_sm = torch.softmax(topk_vals, dim=-1)  # (*, K)

    w = torch.stack([w for w in expert_weights])  # [E, D, D_out]
    y_all = torch.einsum("...i,eio->...eo", inputs, w)  # [*, E, D_out]
    y_select = torch.gather(
        y_all, dim=-2, index=topk_ids.unsqueeze(-1)
    )  # [*, K, D_out]
    y = (y_select * topk_vals_sm.unsqueeze(-1)).sum(dim=-2)  # [*, D_out]
    return y
