"""Interview exercise: common forms of deep-learning parallelism.

These exercises simulate multiple devices with ordinary PyTorch tensors and
modules, so they can be completed and tested on a CPU-only machine. Preserve
the original sample order in every returned tensor. Do not use Python threads,
processes, or ``torch.distributed``.

1. Data parallelism

   Implement ``data_parallel_forward``. Split ``batch`` into
   ``len(replicas)`` chunks along the batch dimension, send one chunk to each
   model replica, and combine the outputs. ``torch.chunk`` may produce chunks
   of different sizes when the batch size is not evenly divisible.

2. Tensor parallelism

   Implement ``column_parallel_linear`` for a linear layer whose weight is
   partitioned across its output dimension. ``weight_shards`` and
   ``bias_shards`` contain corresponding partitions. Return the complete
   linear-layer output.

   Implement ``row_parallel_linear`` for a linear layer whose input and weight
   are partitioned across the input-feature dimension. ``input_shards[i]`` and
   ``weight_shards[i]`` are corresponding partitions. ``bias`` is the bias of
   the complete layer and must be applied once. Return the complete output.

3. Pipeline parallelism

   Implement ``pipeline_forward``. Divide ``batch`` into ``num_microbatches``
   chunks, pass every microbatch through all stages in order, and combine the
   results in the original sample order.

Assume all supplied partitions and dimensions are compatible. You may use
``torch.nn.functional`` operations, but do not reconstruct a full weight
matrix inside either tensor-parallel function.
"""

from collections.abc import Sequence

from torch import Tensor, nn


def data_parallel_forward(replicas: Sequence[nn.Module], batch: Tensor) -> Tensor:
    """Run one batch shard on each replica and combine their outputs."""
    # batch: (B, D)
    n_gpu = len(replicas)
    n_sample = len(batch)
    n_sample_per_gpu = n_gpu // n_sample
    out = list()
    for i in range(n_gpu):
        out.append(
            replicas[i](batch[i * n_sample_per_gpu : (i + 1) * n_sample_per_gpu])
        )
    torch.stack(out)


def column_parallel_linear(
    inputs: Tensor,
    weight_shards: Sequence[Tensor],
    bias_shards: Sequence[Tensor],
) -> Tensor:
    """Evaluate a linear layer partitioned across its output features."""
    raise NotImplementedError


def row_parallel_linear(
    input_shards: Sequence[Tensor],
    weight_shards: Sequence[Tensor],
    bias: Tensor,
) -> Tensor:
    """Evaluate a linear layer partitioned across its input features."""
    raise NotImplementedError


def pipeline_forward(
    stages: Sequence[nn.Module],
    batch: Tensor,
    num_microbatches: int,
) -> Tensor:
    """Run microbatches through each pipeline stage and combine the outputs."""
    raise NotImplementedError
