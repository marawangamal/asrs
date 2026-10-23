import math

import torch

from multihead_attention import multihead_attention, self_attention


def reference_self_attention(
    inputs: torch.Tensor,
    query_weight: torch.Tensor,
    key_weight: torch.Tensor,
    value_weight: torch.Tensor,
    output_weight: torch.Tensor,
    causal: bool = False,
) -> torch.Tensor:
    model_dim = inputs.shape[-1]
    queries = inputs @ query_weight
    keys = inputs @ key_weight
    values = inputs @ value_weight

    scores = queries @ keys.transpose(-2, -1) / math.sqrt(model_dim)
    if causal:
        sequence_length = inputs.shape[1]
        mask = torch.triu(
            torch.ones(sequence_length, sequence_length, dtype=torch.bool),
            diagonal=1,
        )
        scores = scores.masked_fill(mask, float("-inf"))

    return (torch.softmax(scores, dim=-1) @ values) @ output_weight


def reference_multihead_attention(
    inputs: torch.Tensor,
    query_weight: torch.Tensor,
    key_weight: torch.Tensor,
    value_weight: torch.Tensor,
    output_weight: torch.Tensor,
    num_heads: int,
    causal: bool = False,
) -> torch.Tensor:
    batch_size, sequence_length, model_dim = inputs.shape
    head_dim = model_dim // num_heads

    def split_heads(projected: torch.Tensor) -> torch.Tensor:
        return projected.reshape(
            batch_size, sequence_length, num_heads, head_dim
        ).transpose(1, 2)

    queries = split_heads(inputs @ query_weight)
    keys = split_heads(inputs @ key_weight)
    values = split_heads(inputs @ value_weight)

    scores = queries @ keys.transpose(-2, -1) / math.sqrt(head_dim)
    if causal:
        mask = torch.triu(
            torch.ones(sequence_length, sequence_length, dtype=torch.bool),
            diagonal=1,
        )
        scores = scores.masked_fill(mask, float("-inf"))

    attended = torch.softmax(scores, dim=-1) @ values
    joined = attended.transpose(1, 2).reshape(
        batch_size, sequence_length, model_dim
    )
    return joined @ output_weight


def test_single_head_matches_reference() -> None:
    torch.manual_seed(3)
    inputs = torch.randn(2, 5, 12)
    weights = [torch.randn(12, 12) for _ in range(4)]

    actual = self_attention(inputs, *weights)
    expected = reference_self_attention(inputs, *weights)

    assert actual.shape == (2, 5, 12)
    torch.testing.assert_close(actual, expected)


def test_single_head_causal_attention_does_not_look_ahead() -> None:
    torch.manual_seed(5)
    inputs = torch.randn(2, 6, 8)
    changed_inputs = inputs.clone()
    changed_inputs[:, 4:] = torch.randn_like(changed_inputs[:, 4:])
    weights = [torch.randn(8, 8) for _ in range(4)]

    original = self_attention(inputs, *weights, causal=True)
    changed = self_attention(changed_inputs, *weights, causal=True)

    torch.testing.assert_close(original[:, :4], changed[:, :4])


def test_single_head_preserves_gradient_flow() -> None:
    torch.manual_seed(17)
    inputs = torch.randn(2, 4, 8, requires_grad=True)
    weights = [torch.randn(8, 8, requires_grad=True) for _ in range(4)]

    self_attention(inputs, *weights).sum().backward()

    assert inputs.grad is not None
    assert all(weight.grad is not None for weight in weights)


def test_multi_head_matches_reference() -> None:
    torch.manual_seed(7)
    inputs = torch.randn(2, 5, 12)
    weights = [torch.randn(12, 12) for _ in range(4)]

    actual = multihead_attention(inputs, *weights, num_heads=3)
    expected = reference_multihead_attention(inputs, *weights, num_heads=3)

    assert actual.shape == (2, 5, 12)
    torch.testing.assert_close(actual, expected)


def test_multi_head_causal_attention_does_not_look_ahead() -> None:
    torch.manual_seed(11)
    inputs = torch.randn(2, 6, 8)
    changed_inputs = inputs.clone()
    changed_inputs[:, 4:] = torch.randn_like(changed_inputs[:, 4:])
    weights = [torch.randn(8, 8) for _ in range(4)]

    original = multihead_attention(inputs, *weights, num_heads=2, causal=True)
    changed = multihead_attention(changed_inputs, *weights, num_heads=2, causal=True)

    torch.testing.assert_close(original[:, :4], changed[:, :4])


def test_multi_head_single_token_uses_value_and_output_projections() -> None:
    torch.manual_seed(13)
    inputs = torch.randn(3, 1, 8)
    weights = [torch.randn(8, 8) for _ in range(4)]

    actual = multihead_attention(inputs, *weights, num_heads=4)
    expected = (inputs @ weights[2]) @ weights[3]

    torch.testing.assert_close(actual, expected)


def test_multi_head_preserves_gradient_flow() -> None:
    torch.manual_seed(17)
    inputs = torch.randn(2, 4, 8, requires_grad=True)
    weights = [torch.randn(8, 8, requires_grad=True) for _ in range(4)]

    multihead_attention(inputs, *weights, num_heads=2).sum().backward()

    assert inputs.grad is not None
    assert all(weight.grad is not None for weight in weights)
