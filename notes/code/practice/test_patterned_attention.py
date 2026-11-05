import ast
import inspect
import textwrap

import torch

from patterned_attention import patterned_attention_mask


def reference_patterned_attention_mask(
    num_heads: int,
    sequence_length: int,
    window_size: int,
    stride: int,
) -> torch.Tensor:
    positions = torch.arange(sequence_length)
    distance = positions[:, None] - positions[None, :]

    sliding = (distance >= 0) & (distance < window_size)
    strided = (distance >= 0) & (distance.remainder(stride) == 0)

    heads = torch.arange(num_heads)[:, None, None]
    return torch.where(heads.remainder(2) == 0, sliding, strided)


def test_patterned_attention_mask_matches_reference() -> None:
    actual = patterned_attention_mask(
        num_heads=4,
        sequence_length=6,
        window_size=3,
        stride=2,
    )
    expected = reference_patterned_attention_mask(4, 6, 3, 2)

    assert actual.shape == (4, 6, 6)
    assert actual.dtype == torch.bool
    torch.testing.assert_close(actual, expected)


def test_patterned_attention_mask_uses_no_python_loops() -> None:
    source = textwrap.dedent(inspect.getsource(patterned_attention_mask))
    tree = ast.parse(source)
    forbidden = (ast.For, ast.AsyncFor, ast.While, ast.ListComp, ast.SetComp)

    assert not any(isinstance(node, forbidden) for node in ast.walk(tree)), (
        "patterned_attention_mask must use broadcasting, not Python loops"
    )
