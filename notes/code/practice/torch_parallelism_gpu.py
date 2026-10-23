"""Interview exercise: distributing work with ``torch.distributed``.

Run the tests with two processes:

    uv run torchrun --standalone --nproc-per-node=2 -m pytest -q \
        notes/code/practice/test_torch_parallelism_gpu.py

Each process controls one device and has an initialized process group. Rank 0
starts with the complete input tensors; values passed on other ranks are only
same-shaped placeholders and must not affect the result. All partitions are
evenly divisible by the world size.

1. ``distributed_mean``: ``rank_tensors`` has shape ``[world_size, ...]`` on
   rank 0. Distribute one slice to each rank, then return their elementwise
   mean on every rank.

2. ``column_parallel_linear``: rank 0 owns a complete linear-layer input,
   weight, and bias. Replicate the input, distribute weight and bias across
   output features, compute locally, and return the complete output everywhere.

3. ``row_parallel_linear``: rank 0 owns a complete input, weight, and bias.
   Replicate the bias, distribute matching input-feature and weight-column
   shards, and return the complete output everywhere. Apply the bias once.

4. Implement ``distribute_batch`` so rank 0 distributes an equal batch shard
   to every rank. Implement ``wrap_ddp`` so the model is moved to the supplied
   device and wrapped in ``DistributedDataParallel`` for CUDA or CPU.

Use tensor communication primitives from ``torch.distributed``. Do not use
filesystem communication or object collectives.
"""

from torch import Tensor, nn


def distributed_mean(rank_tensors: Tensor) -> Tensor:
    """Distribute rank slices and return their elementwise mean on every rank."""
    raise NotImplementedError


def column_parallel_linear(inputs: Tensor, weight: Tensor, bias: Tensor) -> Tensor:
    """Distribute an output-partitioned linear layer and return its full output."""
    raise NotImplementedError


def row_parallel_linear(inputs: Tensor, weight: Tensor, bias: Tensor) -> Tensor:
    """Distribute an input-partitioned linear layer and return its full output."""
    raise NotImplementedError


def distribute_batch(batch: Tensor) -> Tensor:
    """Distribute equal batch shards from rank 0 and return this rank's shard."""
    raise NotImplementedError


def wrap_ddp(model: nn.Module, device: "object") -> nn.Module:
    """Move ``model`` to ``device`` and wrap it with DDP."""
    raise NotImplementedError
