import math

import torch

from gqa import grouped_query_attention


def reference_gqa(
    inputs: torch.Tensor,
    query_weight: torch.Tensor,
    key_weight: torch.Tensor,
    value_weight: torch.Tensor,
    output_weight: torch.Tensor,
    num_query_heads: int,
    num_kv_heads: int,
    causal: bool = False,
) -> torch.Tensor:
    batch_size, sequence_length, model_dim = inputs.shape
    head_dim = model_dim // num_query_heads
    queries = (inputs @ query_weight).reshape(
        batch_size, sequence_length, num_query_heads, head_dim
    ).transpose(1, 2)
    keys = (inputs @ key_weight).reshape(
        batch_size, sequence_length, num_kv_heads, head_dim
    ).transpose(1, 2)
    values = (inputs @ value_weight).reshape(
        batch_size, sequence_length, num_kv_heads, head_dim
    ).transpose(1, 2)

    repeats = num_query_heads // num_kv_heads
    keys = keys.repeat_interleave(repeats, dim=1)
    values = values.repeat_interleave(repeats, dim=1)
    scores = queries @ keys.transpose(-2, -1) / math.sqrt(head_dim)

    if causal:
        mask = torch.triu(
            torch.ones(
                sequence_length,
                sequence_length,
                dtype=torch.bool,
                device=inputs.device,
            ),
            diagonal=1,
        )
        scores = scores.masked_fill(mask, float("-inf"))

    attended = torch.softmax(scores, dim=-1) @ values
    joined = attended.transpose(1, 2).reshape(
        batch_size, sequence_length, model_dim
    )
    return joined @ output_weight


def test_gqa_matches_reference() -> None:
    torch.manual_seed(7)
    inputs = torch.randn(2, 5, 12)
    query_weight = torch.randn(12, 12)
    key_weight = torch.randn(12, 4)
    value_weight = torch.randn(12, 4)
    output_weight = torch.randn(12, 12)

    actual = grouped_query_attention(
        inputs,
        query_weight,
        key_weight,
        value_weight,
        output_weight,
        num_query_heads=3,
        num_kv_heads=1,
    )
    expected = reference_gqa(
        inputs,
        query_weight,
        key_weight,
        value_weight,
        output_weight,
        num_query_heads=3,
        num_kv_heads=1,
    )

    assert actual.shape == (2, 5, 12)
    torch.testing.assert_close(actual, expected)


def test_gqa_supports_multiple_kv_groups() -> None:
    torch.manual_seed(11)
    inputs = torch.randn(2, 4, 16)
    weights = [
        torch.randn(16, 16),
        torch.randn(16, 8),
        torch.randn(16, 8),
        torch.randn(16, 16),
    ]

    actual = grouped_query_attention(
        inputs, *weights, num_query_heads=4, num_kv_heads=2
    )
    expected = reference_gqa(
        inputs, *weights, num_query_heads=4, num_kv_heads=2
    )

    torch.testing.assert_close(actual, expected)


def test_gqa_causal_attention_does_not_look_ahead() -> None:
    torch.manual_seed(13)
    inputs = torch.randn(2, 6, 8)
    changed_inputs = inputs.clone()
    changed_inputs[:, 4:] = torch.randn_like(changed_inputs[:, 4:])
    weights = [
        torch.randn(8, 8),
        torch.randn(8, 4),
        torch.randn(8, 4),
        torch.randn(8, 8),
    ]

    original = grouped_query_attention(
        inputs, *weights, num_query_heads=4, num_kv_heads=2, causal=True
    )
    changed = grouped_query_attention(
        changed_inputs, *weights, num_query_heads=4, num_kv_heads=2, causal=True
    )

    torch.testing.assert_close(original[:, :4], changed[:, :4])


def test_gqa_preserves_gradient_flow() -> None:
    inputs = torch.randn(2, 4, 8, requires_grad=True)
    weights = [
        torch.randn(8, 8, requires_grad=True),
        torch.randn(8, 4, requires_grad=True),
        torch.randn(8, 4, requires_grad=True),
        torch.randn(8, 8, requires_grad=True),
    ]

    grouped_query_attention(
        inputs, *weights, num_query_heads=4, num_kv_heads=2
    ).sum().backward()

    assert inputs.grad is not None
    assert all(weight.grad is not None for weight in weights)
