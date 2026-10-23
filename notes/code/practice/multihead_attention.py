"""Interview exercises: implement scaled dot-product self-attention.

1. Implement ``self_attention`` using one attention head.

2. Implement ``multihead_attention`` by splitting the projected queries,
   keys, and values into ``num_heads`` heads, applying attention independently
   to each head, joining the heads, and applying the output projection.

``inputs`` has shape ``[B, T, D]`` and all projection weights have shape
``[D, D]``.

When ``causal`` is true, a token must not attend to tokens after its own
position. Assume ``D`` is divisible by ``num_heads``. Do not use
``torch.nn.MultiheadAttention`` or ``torch.nn.functional.scaled_dot_product_attention``.
"""

import math
import torch
from torch import Tensor


def self_attention(
    inputs: Tensor,  # (B, T, D)
    query_weight: Tensor,  # (D, D)
    key_weight: Tensor,  # (D, D)
    value_weight: Tensor,  # (D, D)
    output_weight: Tensor,
    causal: bool = False,
) -> Tensor:
    """Return single-head self-attention output with shape ``[B, T, D]``."""
    B, T, D = inputs.shape
    q = torch.einsum("bti,io->bto", inputs, query_weight)
    k = torch.einsum("bti,io->bto", inputs, key_weight)
    v = torch.einsum("bti,io->bto", inputs, value_weight)
    loga = torch.einsum("btd,bsd->bts", q, k)  # a[n, i, j] = <q_i, k_j>

    # get causal mask
    a_tilde = loga / math.sqrt(D)
    if causal:
        m = torch.triu(
            torch.ones(T, T, dtype=torch.bool, device=inputs.device),
            diagonal=1,
        )
        a_tilde = a_tilde.masked_fill(m, float("-inf"))  # (B, T, T)
    a = torch.softmax(a_tilde, dim=-1)  # (B, T, T)
    o = torch.einsum("bts,bsd->btd", a, v)
    proj = torch.einsum("bti,io->bto", o, output_weight)
    return proj


def multihead_attention(
    inputs: Tensor,
    query_weight: Tensor,
    key_weight: Tensor,
    value_weight: Tensor,
    output_weight: Tensor,
    num_heads: int,
    causal: bool = False,
) -> Tensor:
    """Return multi-head self-attention output with shape ``[B, T, D]``."""
    B, T, D = inputs.shape
    q = torch.einsum("bti,io->bto", inputs, query_weight)
    k = torch.einsum("bti,io->bto", inputs, key_weight)
    v = torch.einsum("bti,io->bto", inputs, value_weight)

    # split heads
    Nh = num_heads
    Dh = D // Nh
    q = q.reshape(B, T, Nh, Dh).permute(0, 2, 1, 3)  # (B, Nh, T, Dh)
    k = k.reshape(B, T, Nh, Dh).permute(0, 2, 1, 3)  # (B, Nh, T, Dh)
    v = v.reshape(B, T, Nh, Dh).permute(0, 2, 1, 3)  # (B, Nh, T, Dh)

    loga = torch.einsum("bhtd,bhsd->bhts", q, k)  # a[n, h, i, j] = <q_i, k_j>

    # get causal mask
    a_tilde = loga / math.sqrt(Dh)
    if causal:
        m = torch.triu(
            torch.ones(T, T, dtype=torch.bool, device=inputs.device),
            diagonal=1,
        )
        a_tilde = a_tilde.masked_fill(m, float("-inf"))  # (B, H, T, T)
    a = torch.softmax(a_tilde, dim=-1)  # (B, H, T, T)
    o = torch.einsum("bhts,bhsd->bhtd", a, v)
    proj = torch.einsum(
        "bti,io->bto", o.permute(0, 2, 1, 3).reshape(B, T, D), output_weight
    )
    return proj
