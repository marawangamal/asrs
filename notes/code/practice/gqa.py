"""Interview exercise: implement grouped-query self-attention (GQA).

``inputs`` has shape ``[B, T, D]``. Queries use ``num_query_heads`` heads,
while keys and values use fewer ``num_kv_heads`` heads. Each KV head is shared
by an equal-sized group of query heads.

The projection weights have shapes:

* ``query_weight``: ``[D, D]``
* ``key_weight`` and ``value_weight``: ``[D, num_kv_heads * head_dim]``
* ``output_weight``: ``[D, D]``

Assume ``D`` is divisible by ``num_query_heads`` and ``num_query_heads`` is
divisible by ``num_kv_heads``. Support causal attention. Do not use
``torch.nn.MultiheadAttention`` or scaled-dot-product-attention helpers.
"""

from torch import Tensor


def grouped_query_attention(
    inputs: Tensor,
    query_weight: Tensor,
    key_weight: Tensor,
    value_weight: Tensor,
    output_weight: Tensor,
    num_query_heads: int,
    num_kv_heads: int,
    causal: bool = False,
) -> Tensor:
    """Return grouped-query attention output with shape ``[B, T, D]``."""
    raise NotImplementedError
