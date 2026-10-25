import torch

from rope import apply_rope


def reference_rope(
    x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor
) -> torch.Tensor:
    even = x[..., 0::2]
    odd = x[..., 1::2]
    cos = cos[None, None, :, :]
    sin = sin[None, None, :, :]
    rotated = torch.stack(
        (even * cos - odd * sin, even * sin + odd * cos), dim=-1
    )
    return rotated.flatten(-2)


def test_rope_matches_reference_rotation() -> None:
    torch.manual_seed(3)
    x = torch.randn(2, 3, 5, 8)
    angles = torch.randn(5, 4)
    cos, sin = angles.cos(), angles.sin()

    actual = apply_rope(x, cos, sin)
    expected = reference_rope(x, cos, sin)

    assert actual.shape == x.shape
    torch.testing.assert_close(actual, expected)


def test_rope_identity_rotation_leaves_input_unchanged() -> None:
    x = torch.randn(2, 4, 6, 8)
    cos = torch.ones(6, 4)
    sin = torch.zeros(6, 4)

    torch.testing.assert_close(apply_rope(x, cos, sin), x)


def test_rope_preserves_each_pair_norm() -> None:
    torch.manual_seed(5)
    x = torch.randn(2, 3, 7, 10)
    angles = torch.randn(7, 5)

    actual = apply_rope(x, angles.cos(), angles.sin())
    before = x.reshape(2, 3, 7, 5, 2).square().sum(dim=-1)
    after = actual.reshape(2, 3, 7, 5, 2).square().sum(dim=-1)

    torch.testing.assert_close(after, before)


def test_rope_preserves_gradient_flow() -> None:
    x = torch.randn(2, 3, 4, 8, requires_grad=True)
    angles = torch.randn(4, 4)

    apply_rope(x, angles.cos(), angles.sin()).sum().backward()

    assert x.grad is not None
