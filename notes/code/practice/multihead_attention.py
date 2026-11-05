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
from torch import Tensor, triu


def self_attention(
    inputs: Tensor,  # (B, T, D)
    query_weight: Tensor,  # (D, D)
    key_weight: Tensor,  # (D, D)
    value_weight: Tensor,  # (D, D)
    output_weight: Tensor,  # (D, D)
    causal: bool = False,
) -> Tensor:
    """Return single-head self-attention output with shape ``[B, T, D]``."""
    B, T, D = inputs.shape
    q = torch.einsum("bti,io->bto", inputs, query_weight)  # (B, T, D)
    k = torch.einsum("bti,io->bto", inputs, key_weight)
    v = torch.einsum("bti,io->bto", inputs, value_weight)

    a = torch.einsum("bsd,btd->bst", q, k)  # a[i, j] = <qi, kj>
    a = a / math.sqrt(D)
    if causal:
        m = torch.triu(torch.ones_like(a), 1) == 1
        a = a.masked_fill(m, float("-inf"))
    a = torch.softmax(a, dim=-1)

    o = torch.einsum("bst,bti,io->bso", a, v, output_weight)
    return o


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
    q = torch.einsum("bti,io->bto", inputs, query_weight)  # (B, T, D)
    k = torch.einsum("bti,io->bto", inputs, key_weight)
    v = torch.einsum("bti,io->bto", inputs, value_weight)

    q = q.reshape(B, T, num_heads, D // num_heads)
    k = k.reshape(B, T, num_heads, D // num_heads)
    v = v.reshape(B, T, num_heads, D // num_heads)

    a = torch.einsum("bshd,bthd->bhst", q, k)  # a[i, j] = <qi, kj>
    a = a / math.sqrt(D // num_heads)
    if causal:
        m = torch.triu(torch.ones_like(a), 1) == 1
        a = a.masked_fill(m, float("-inf"))
    a = torch.softmax(a, dim=-1)

    o_prime = torch.einsum("bhst,bthd->bshd", a, v)
    o = torch.einsum("bti,io->bto", o_prime.reshape(B, T, D), output_weight)
    return o
