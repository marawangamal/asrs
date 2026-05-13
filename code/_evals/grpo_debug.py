"""
GRPO Debug Exercise
===================

You're given a working-looking GRPO trainer for a tiny contextual-bandit task.
There are THREE bugs. Run the tests:

    python python/grpo_debug.py

Read the failures, find the root cause for each, fix in place. Do not rewrite.

Quick recap of GRPO:
- For each prompt, sample a GROUP of G actions (no critic network).
- Advantage per sample = (reward - group_mean) / group_std.
- Update with PPO's clipped surrogate objective:
      L = -E[ min(ratio * A, clip(ratio, 1 - eps, 1 + eps) * A) ]
  where ratio = pi_new(a) / pi_old(a).

Hint: one of the bugs is subtle — it's the reason the policy ratio drifts from
1 even before the first optimizer step. The other two are formula-level errors
that anyone with GRPO familiarity should spot on a careful read.


Follow-up questions (verbal, for after the bugs are fixed):

1. Why does GRPO use group-relative advantages instead of learning a critic /
   value function? What does it gain, what does it give up?

2. What's the bias/variance tradeoff of the group size G? What happens as
   G -> 1? As G -> infinity?

3. PPO-style clipping AND a KL penalty against a reference policy are both
   common in GRPO. What does each provide? When would you use one but not
   the other?

4. The on-policy-ratio test below asserts ratio == 1 on the very first step.
   Why is that a good sanity check? What real-world bugs does it catch in
   LLM-scale RL pipelines?

5. The standard advantage normalization is (r - mean) / std. What goes wrong
   if you skip the /std term? What goes wrong if rewards are nearly constant
   within a group (std ~ 0)?
"""

import unittest

import numpy as np
import torch
import torch.nn as nn
from torch.distributions import Categorical


# ---------------------------------------------------------------------------
# Toy environment: contextual bandit.
# ---------------------------------------------------------------------------

N_STATES = 4
N_ACTIONS = 3
GROUP_SIZE = 8
HIDDEN = 32

# Reward matrix: best action per state is the one with reward 1.0.
REWARD_MATRIX = torch.tensor([
    [1.0, 0.2, 0.0],
    [0.0, 1.0, 0.2],
    [0.2, 0.0, 1.0],
    [1.0, 0.0, 0.5],
])


def reward_fn(states, actions):
    """Look up reward for each (state, action) pair."""
    return REWARD_MATRIX[states, actions]


# ---------------------------------------------------------------------------
# Policy network.
# ---------------------------------------------------------------------------

class Policy(nn.Module):
    def __init__(self, n_states=N_STATES, n_actions=N_ACTIONS, hidden=HIDDEN):
        super().__init__()
        self.embed = nn.Embedding(n_states, hidden)
        self.head = nn.Sequential(
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden, n_actions),
        )

    def forward(self, states):
        return self.head(self.embed(states))


# ---------------------------------------------------------------------------
# GRPO trainer.
# ---------------------------------------------------------------------------

class GRPOTrainer:
    def __init__(self, policy, lr=1e-2, clip_eps=0.2, group_size=GROUP_SIZE):
        self.policy = policy
        self.opt = torch.optim.Adam(policy.parameters(), lr=lr)
        self.clip_eps = clip_eps
        self.group_size = group_size

    def collect_rollouts(self, prompts):
        """Sample group_size actions for each prompt.

        Returns:
            states:        (B*G,) long
            actions:       (B*G,) long
            rewards:       (B*G,) float
            old_log_probs: (B*G,) float, no grad
        """
        states = prompts.repeat_interleave(self.group_size)
        with torch.no_grad():
            logits = self.policy(states)
            dist = Categorical(logits=logits)
            actions = dist.sample()
            old_log_probs = dist.log_prob(actions)
        rewards = reward_fn(states, actions)
        return states, actions, rewards, old_log_probs

    def compute_advantages(self, rewards):
        """GRPO advantages: normalize rewards within each group."""
        rewards_grouped = rewards.view(-1, self.group_size)
        baseline = rewards_grouped.mean(dim=1, keepdim=True)
        advantages = rewards_grouped - baseline
        return advantages.view(-1)

    def ppo_loss(self, ratio, advantages):
        """PPO clipped surrogate loss (to minimize)."""
        clipped = torch.clamp(ratio, 1 - self.clip_eps, 1 + self.clip_eps)
        return -(clipped * advantages).mean()

    def train_step(self, prompts):
        states, actions, rewards, old_log_probs = self.collect_rollouts(prompts)
        advantages = self.compute_advantages(rewards)

        logits = self.policy(states)
        dist = Categorical(logits=logits)
        new_log_probs = dist.log_prob(actions)

        ratio = torch.exp(new_log_probs - old_log_probs)
        loss = self.ppo_loss(ratio, advantages)

        self.opt.zero_grad()
        loss.backward()
        self.opt.step()

        return {
            "loss": loss.item(),
            "mean_ratio": ratio.mean().item(),
            "mean_reward": rewards.mean().item(),
        }


# ---------------------------------------------------------------------------
# Tests. These currently fail. Fix the trainer so they all pass.
# ---------------------------------------------------------------------------

class TestGRPO(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(0)
        np.random.seed(0)
        self.policy = Policy()
        self.trainer = GRPOTrainer(self.policy)

    def test_advantages_normalized(self):
        """Per-group advantages should have mean ~ 0 and std ~ 1."""
        torch.manual_seed(42)
        rewards = torch.randn(3 * GROUP_SIZE)
        adv = self.trainer.compute_advantages(rewards).view(3, GROUP_SIZE)
        for i in range(3):
            self.assertAlmostEqual(adv[i].mean().item(), 0.0, places=4)
            self.assertAlmostEqual(
                adv[i].std(unbiased=False).item(), 1.0, places=2,
                msg="Per-group advantage std should be ~1 (not just mean-centered).",
            )

    def test_ppo_clip_uses_pessimistic_min(self):
        """PPO takes the min of (ratio*A) and (clipped_ratio*A) per sample.

        With ratio=1.5, A=+1: ratio*A=1.5, clipped*A=1.2 -> min=1.2
        With ratio=0.5, A=+1: ratio*A=0.5, clipped*A=0.8 -> min=0.5
        Expected loss = -mean([1.2, 0.5]) = -0.85
        """
        ratio = torch.tensor([1.5, 0.5])
        adv = torch.tensor([1.0, 1.0])
        expected = -(1.2 + 0.5) / 2
        self.assertAlmostEqual(self.trainer.ppo_loss(ratio, adv).item(),
                               expected, places=5)

    def test_on_policy_ratio_is_one(self):
        """Strictly on-policy: before any optimizer step,
        recomputing log_probs must give the same values as at sample time,
        so the ratio is exactly 1."""
        torch.manual_seed(0)
        prompts = torch.arange(N_STATES)
        states, actions, _, old_log_probs = self.trainer.collect_rollouts(prompts)

        # No optimizer step yet. Same policy, same actions -> ratio must be 1.
        logits = self.policy(states)
        dist = Categorical(logits=logits)
        new_log_probs = dist.log_prob(actions)
        ratio = torch.exp(new_log_probs - old_log_probs)

        np.testing.assert_allclose(
            ratio.detach().numpy(),
            np.ones_like(ratio.detach().numpy()),
            atol=1e-5,
            err_msg=("On-policy first-step ratio should be exactly 1. "
                     "If it isn't, something is making the two forward passes "
                     "produce different log_probs."),
        )

    def test_training_improves(self):
        """End-to-end smoke: after some steps, mean reward should rise
        toward the optimum (1.0). Won't reliably pass until the other
        three bugs are fixed."""
        torch.manual_seed(0)
        prompts = torch.arange(N_STATES)

        self.policy.eval()
        with torch.no_grad():
            _, _, init_r, _ = self.trainer.collect_rollouts(prompts)
        self.policy.train()
        initial = init_r.mean().item()

        for _ in range(300):
            self.trainer.train_step(prompts)

        self.policy.eval()
        with torch.no_grad():
            _, _, final_r, _ = self.trainer.collect_rollouts(prompts)
        self.policy.train()
        final = final_r.mean().item()

        self.assertGreater(
            final, 0.7,
            msg=f"Training failed to converge: init={initial:.3f}, final={final:.3f}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
