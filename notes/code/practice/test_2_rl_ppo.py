from importlib import import_module

import torch

ppo_policy_loss = import_module("2_rl_ppo").ppo_policy_loss


def reference_ppo_policy_loss(
    token_log_probs: torch.Tensor,
    old_token_log_probs: torch.Tensor,
    completion_mask: torch.Tensor,
    advantages: torch.Tensor,
    epsilon: float,
) -> torch.Tensor:
    ratio = (token_log_probs - old_token_log_probs.detach()).exp()
    advantage = advantages.detach()[:, None]
    surrogate = ratio * advantage
    clipped_surrogate = ratio.clamp(1 - epsilon, 1 + epsilon) * advantage
    objective = torch.minimum(surrogate, clipped_surrogate)
    return -(objective * completion_mask).sum() / completion_mask.sum()


def test_ppo_policy_loss_matches_reference() -> None:
    old_token_log_probs = torch.tensor(
        [
            [-1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0],
        ]
    )
    ratios = torch.tensor(
        [
            [1.0, 1.1, 1.5, 0.7],
            [1.0, 0.8, 0.5, 1.4],
        ]
    )
    token_log_probs = old_token_log_probs + ratios.log()
    completion_mask = torch.tensor(
        [
            [False, True, True, False],
            [False, True, True, False],
        ]
    )
    advantages = torch.tensor([2.0, -1.5])

    actual = ppo_policy_loss(
        token_log_probs,
        old_token_log_probs,
        completion_mask,
        advantages,
        epsilon=0.2,
    )
    expected = reference_ppo_policy_loss(
        token_log_probs,
        old_token_log_probs,
        completion_mask,
        advantages,
        epsilon=0.2,
    )

    torch.testing.assert_close(actual, expected)


def test_ppo_policy_loss_masks_tokens_and_fixed_targets() -> None:
    token_log_probs = torch.randn(2, 5, requires_grad=True)
    old_token_log_probs = torch.randn(2, 5, requires_grad=True)
    completion_mask = torch.tensor(
        [
            [False, False, True, True, False],
            [False, True, True, True, False],
        ]
    )
    advantages = torch.tensor([1.0, -1.0], requires_grad=True)

    ppo_policy_loss(
        token_log_probs,
        old_token_log_probs,
        completion_mask,
        advantages,
        epsilon=0.2,
    ).backward()

    assert token_log_probs.grad is not None
    assert torch.all(token_log_probs.grad[~completion_mask] == 0)
    assert old_token_log_probs.grad is None
    assert advantages.grad is None
