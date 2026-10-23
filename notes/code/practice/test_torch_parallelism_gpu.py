import os

import pytest
import torch
import torch.distributed as dist
import torch.nn.functional as F
from torch import nn
from torch.nn.parallel import DistributedDataParallel

from torch_parallelism_gpu import (
    column_parallel_linear,
    distribute_batch,
    distributed_mean,
    row_parallel_linear,
    wrap_ddp,
)


pytestmark = pytest.mark.skipif(
    "RANK" not in os.environ,
    reason="run with torchrun as shown in torch_parallelism_gpu.py",
)


@pytest.fixture(scope="session", autouse=True)
def distributed_process_group():
    local_rank = int(os.environ["LOCAL_RANK"])
    world_size = int(os.environ["WORLD_SIZE"])
    if world_size != 2:
        pytest.fail("These tests require --nproc-per-node=2")

    use_cuda = torch.cuda.is_available() and torch.cuda.device_count() >= world_size
    if use_cuda:
        torch.cuda.set_device(local_rank)
        backend = "nccl"
        device = torch.device("cuda", local_rank)
    else:
        backend = "gloo"
        device = torch.device("cpu")

    dist.init_process_group(backend=backend)
    yield device
    dist.destroy_process_group()


def rank_zero_value(value: torch.Tensor) -> torch.Tensor:
    if dist.get_rank() == 0:
        return value
    return torch.full_like(value, -999.0)


def test_distributed_mean_distributes_rank_slices(
    distributed_process_group: torch.device,
) -> None:
    device = distributed_process_group
    complete = torch.tensor([[1.0, 0.0], [2.0, 3.0]], device=device)

    actual = distributed_mean(rank_zero_value(complete))
    expected = torch.tensor([1.5, 1.5], device=device)

    torch.testing.assert_close(actual, expected)


def test_column_parallel_linear_distributes_output_shards(
    distributed_process_group: torch.device,
) -> None:
    device = distributed_process_group
    torch.manual_seed(21)
    inputs = torch.randn(3, 6, device=device)
    weight = torch.randn(8, 6, device=device)
    bias = torch.randn(8, device=device)
    expected = F.linear(inputs, weight, bias)

    actual = column_parallel_linear(
        rank_zero_value(inputs), rank_zero_value(weight), rank_zero_value(bias)
    )

    torch.testing.assert_close(actual, expected)


def test_row_parallel_linear_distributes_input_shards(
    distributed_process_group: torch.device,
) -> None:
    device = distributed_process_group
    torch.manual_seed(34)
    inputs = torch.randn(3, 6, device=device)
    weight = torch.randn(5, 6, device=device)
    bias = torch.randn(5, device=device)
    expected = F.linear(inputs, weight, bias)

    actual = row_parallel_linear(
        rank_zero_value(inputs), rank_zero_value(weight), rank_zero_value(bias)
    )

    torch.testing.assert_close(actual, expected)


def test_distribute_batch_sends_a_different_shard_to_each_rank(
    distributed_process_group: torch.device,
) -> None:
    device = distributed_process_group
    rank = dist.get_rank()
    complete = torch.arange(24, dtype=torch.float32, device=device).reshape(6, 4)

    actual = distribute_batch(rank_zero_value(complete))
    expected = complete.chunk(dist.get_world_size(), dim=0)[rank]

    torch.testing.assert_close(actual, expected)


def test_wrap_ddp_synchronizes_gradients(
    distributed_process_group: torch.device,
) -> None:
    device = distributed_process_group
    rank = dist.get_rank()
    torch.manual_seed(55)
    model = wrap_ddp(nn.Linear(4, 2), device)

    assert isinstance(model, DistributedDataParallel)
    local_inputs = torch.randn(3, 4, device=device) + rank
    model(local_inputs).sum().backward()

    gradient = next(model.parameters()).grad
    assert gradient is not None
    gathered = [torch.empty_like(gradient) for _ in range(dist.get_world_size())]
    dist.all_gather(gathered, gradient)
    for other_gradient in gathered[1:]:
        torch.testing.assert_close(gathered[0], other_gradient)
