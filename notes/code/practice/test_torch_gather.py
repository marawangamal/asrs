import torch

from torch_gather import (
    completion_log_probs,
    next_token_log_probs,
    token_ids_to_one_hot,
)


def test_next_token_log_probs_uses_the_shifted_target_tokens() -> None:
    # The correct next tokens are [2, 0, 1]. The final logits row is unused
    # because there is no token after the last input position.
    logits = torch.tensor(
        [
            [
                [1.0, 2.0, 4.0],
                [5.0, 1.0, 0.0],
                [0.0, 3.0, 1.0],
                [100.0, -100.0, 0.0],
            ]
        ]
    )
    input_ids = torch.tensor([[1, 2, 0, 1]])

    actual = next_token_log_probs(logits, input_ids)
    all_log_probs = torch.log_softmax(logits, dim=-1)
    expected = torch.stack(
        [all_log_probs[0, 0, 2], all_log_probs[0, 1, 0], all_log_probs[0, 2, 1]]
    ).unsqueeze(0)

    assert actual.shape == (1, 3)
    torch.testing.assert_close(actual, expected)


def test_next_token_log_probs_handles_batches() -> None:
    torch.manual_seed(7)
    logits = torch.randn(2, 5, 6)
    input_ids = torch.tensor([[0, 5, 1, 3, 2], [4, 2, 0, 5, 1]])

    actual = next_token_log_probs(logits, input_ids)
    expected = torch.log_softmax(logits[:, :-1], dim=-1).gather(
        -1, input_ids[:, 1:, None]
    )[..., 0]

    assert actual.shape == (2, 4)
    torch.testing.assert_close(actual, expected)


def test_completion_log_probs_sums_only_masked_tokens() -> None:
    torch.manual_seed(11)
    logits = torch.randn(2, 5, 7)
    input_ids = torch.tensor([[0, 1, 2, 3, 4], [6, 5, 4, 3, 2]])
    completion_mask = torch.tensor(
        [[False, False, True, True], [False, True, True, False]]
    )

    token_log_probs = next_token_log_probs(logits, input_ids)
    actual = completion_log_probs(logits, input_ids, completion_mask)
    expected = torch.tensor(
        [
            token_log_probs[0, 2] + token_log_probs[0, 3],
            token_log_probs[1, 1] + token_log_probs[1, 2],
        ]
    )

    assert actual.shape == (2,)
    torch.testing.assert_close(actual, expected)


def test_next_token_log_probs_preserves_gradient_flow() -> None:
    logits = torch.randn(2, 4, 5, requires_grad=True)
    input_ids = torch.tensor([[0, 1, 2, 3], [4, 3, 2, 1]])

    next_token_log_probs(logits, input_ids).sum().backward()

    assert logits.grad is not None
    assert torch.count_nonzero(logits.grad[:, :-1]) > 0
    torch.testing.assert_close(logits.grad[:, -1], torch.zeros_like(logits.grad[:, -1]))


def test_token_ids_to_one_hot() -> None:
    input_ids = torch.tensor([[0, 2, 1], [3, 1, 3]])

    actual = token_ids_to_one_hot(input_ids, vocab_size=4)
    expected = torch.tensor(
        [
            [[1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]],
        ]
    )

    assert actual.shape == (2, 3, 4)
    assert actual.dtype.is_floating_point
    assert actual.device == input_ids.device
    torch.testing.assert_close(actual, expected)
