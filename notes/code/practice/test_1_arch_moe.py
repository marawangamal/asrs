from collections.abc import Sequence
from importlib import import_module

import torch

mixture_of_experts = import_module("1_arch_moe").mixture_of_experts


def reference_moe(
    inputs: torch.Tensor,
    router_weight: torch.Tensor,
    expert_weights: Sequence[torch.Tensor],
    top_k: int,
) -> torch.Tensor:
    original_shape = inputs.shape[:-1]
    flat_inputs = inputs.reshape(-1, inputs.shape[-1])
    router_logits = flat_inputs @ router_weight
    selected_logits, selected_experts = router_logits.topk(top_k, dim=-1)
    routing_weights = selected_logits.softmax(dim=-1)

    all_expert_outputs = torch.stack(
        [flat_inputs @ weight for weight in expert_weights], dim=1
    )
    gather_index = selected_experts[..., None].expand(
        -1, -1, all_expert_outputs.shape[-1]
    )
    selected_outputs = all_expert_outputs.gather(1, gather_index)
    output = (selected_outputs * routing_weights[..., None]).sum(dim=1)
    return output.reshape(*original_shape, output.shape[-1])


def test_moe_top_two_routing_matches_reference() -> None:
    torch.manual_seed(17)
    inputs = torch.randn(2, 5, 6)
    router_weight = torch.randn(6, 4)
    expert_weights = [torch.randn(6, 8) for _ in range(4)]

    actual = mixture_of_experts(inputs, router_weight, expert_weights, top_k=2)
    expected = reference_moe(inputs, router_weight, expert_weights, top_k=2)

    assert actual.shape == (2, 5, 8)
    torch.testing.assert_close(actual, expected)


def test_moe_top_one_uses_only_the_selected_expert() -> None:
    inputs = torch.tensor([[[2.0, 1.0], [1.0, 3.0]]])
    router_weight = torch.tensor([[2.0, 0.0], [0.0, 2.0]])
    expert_weights = [torch.eye(2), -torch.eye(2)]

    actual = mixture_of_experts(inputs, router_weight, expert_weights, top_k=1)
    expected = torch.tensor([[[2.0, 1.0], [-1.0, -3.0]]])

    torch.testing.assert_close(actual, expected)


def test_moe_top_all_matches_dense_router_mixture() -> None:
    torch.manual_seed(19)
    inputs = torch.randn(3, 4)
    router_weight = torch.randn(4, 3)
    expert_weights = [torch.randn(4, 5) for _ in range(3)]

    actual = mixture_of_experts(inputs, router_weight, expert_weights, top_k=3)
    expected = reference_moe(inputs, router_weight, expert_weights, top_k=3)

    torch.testing.assert_close(actual, expected)


def test_moe_preserves_gradient_flow_to_selected_paths() -> None:
    torch.manual_seed(23)
    inputs = torch.randn(3, 4, requires_grad=True)
    router_weight = torch.randn(4, 3, requires_grad=True)
    expert_weights = [torch.randn(4, 5, requires_grad=True) for _ in range(3)]

    mixture_of_experts(
        inputs, router_weight, expert_weights, top_k=2
    ).sum().backward()

    assert inputs.grad is not None
    assert router_weight.grad is not None
    assert any(weight.grad is not None for weight in expert_weights)
