from importlib import import_module

import torch

policy_gradient_loss = import_module(
    "2_rl_policy_gradient"
).policy_gradient_loss


def test_policy_gradient_loss_matches_reference() -> None:
    token_log_probs = torch.tensor(
        [
            [-0.1, -0.2, -0.3, -0.4],
            [-1.0, -1.1, -1.2, -1.3],
        ]
    )
    completion_mask = torch.tensor(
        [
            [False, True, True, False],
            [False, False, True, True],
        ]
    )
    advantages = torch.tensor([2.0, -0.5])

    actual = policy_gradient_loss(
        token_log_probs, completion_mask, advantages
    )
    expected = -torch.tensor(
        [2.0 * (-0.2 - 0.3), -0.5 * (-1.2 - 1.3)]
    ).mean()

    torch.testing.assert_close(actual, expected)


def test_policy_gradient_loss_masks_tokens_and_detaches_advantages() -> None:
    token_log_probs = torch.randn(2, 5, requires_grad=True)
    completion_mask = torch.tensor(
        [
            [False, False, True, True, False],
            [False, True, True, True, False],
        ]
    )
    advantages = torch.tensor([1.5, -2.0], requires_grad=True)

    policy_gradient_loss(
        token_log_probs, completion_mask, advantages
    ).backward()

    assert token_log_probs.grad is not None
    assert torch.all(token_log_probs.grad[~completion_mask] == 0)
    assert torch.all(token_log_probs.grad[completion_mask] != 0)
    assert advantages.grad is None
