import torch
import torch.nn.functional as F
from torch import nn

from torch_parallelism import (
    column_parallel_linear,
    data_parallel_forward,
    pipeline_forward,
    row_parallel_linear,
)


class RecordingModule(nn.Module):
    def __init__(self, module: nn.Module) -> None:
        super().__init__()
        self.module = module
        self.seen_shapes: list[tuple[int, ...]] = []

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        self.seen_shapes.append(tuple(inputs.shape))
        return self.module(inputs)


def test_data_parallel_forward_uses_one_uneven_shard_per_replica() -> None:
    replicas = [RecordingModule(nn.Identity()) for _ in range(3)]
    batch = torch.arange(20, dtype=torch.float32).reshape(5, 4)

    actual = data_parallel_forward(replicas, batch)

    torch.testing.assert_close(actual, batch)
    assert [replica.seen_shapes for replica in replicas] == [
        [(2, 4)],
        [(2, 4)],
        [(1, 4)],
    ]


def test_column_parallel_linear_matches_an_unsharded_layer() -> None:
    torch.manual_seed(3)
    inputs = torch.randn(4, 6)
    weight = torch.randn(8, 6)
    bias = torch.randn(8)
    weight_shards = weight.tensor_split(3, dim=0)
    bias_shards = bias.tensor_split(3, dim=0)

    actual = column_parallel_linear(inputs, weight_shards, bias_shards)
    expected = F.linear(inputs, weight, bias)

    assert actual.shape == (4, 8)
    torch.testing.assert_close(actual, expected)


def test_row_parallel_linear_matches_an_unsharded_layer() -> None:
    torch.manual_seed(5)
    inputs = torch.randn(4, 7)
    weight = torch.randn(5, 7)
    bias = torch.randn(5)
    input_shards = inputs.tensor_split(3, dim=-1)
    weight_shards = weight.tensor_split(3, dim=1)

    actual = row_parallel_linear(input_shards, weight_shards, bias)
    expected = F.linear(inputs, weight, bias)

    assert actual.shape == (4, 5)
    torch.testing.assert_close(actual, expected)


def test_row_parallel_linear_applies_bias_only_once() -> None:
    inputs = torch.ones(2, 4)
    weight = torch.zeros(3, 4)
    bias = torch.tensor([1.0, 2.0, 3.0])

    actual = row_parallel_linear(
        inputs.tensor_split(2, dim=-1),
        weight.tensor_split(2, dim=1),
        bias,
    )

    torch.testing.assert_close(actual, bias.expand(2, -1))


def test_pipeline_forward_uses_each_stage_for_every_microbatch() -> None:
    stage_1 = RecordingModule(nn.Linear(4, 6))
    stage_2 = RecordingModule(nn.ReLU())
    stage_3 = RecordingModule(nn.Linear(6, 2))
    stages = [stage_1, stage_2, stage_3]
    batch = torch.randn(7, 4)

    actual = pipeline_forward(stages, batch, num_microbatches=3)
    expected = stage_3.module(stage_2.module(stage_1.module(batch)))

    assert actual.shape == (7, 2)
    torch.testing.assert_close(actual, expected)
    assert stage_1.seen_shapes == [(3, 4), (3, 4), (1, 4)]
    assert stage_2.seen_shapes == [(3, 6), (3, 6), (1, 6)]
    assert stage_3.seen_shapes == [(3, 6), (3, 6), (1, 6)]
