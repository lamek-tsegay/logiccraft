from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from .expr import Expr, evaluate, vars_in


@dataclass(frozen=True)
class EquivResult:
    equivalent: bool
    var_order: List[str]
    counterexample: Optional[Dict[str, int]]  # first mismatch assignment, if any
    lhs_out: Optional[int]
    rhs_out: Optional[int]


def _all_assignments(var_order: Sequence[str]):
    # yields env dicts in lexicographic bit order
    n = len(var_order)
    for mask in range(2**n):
        env: Dict[str, int] = {}
        for i, v in enumerate(var_order):
            bit = (mask >> (n - 1 - i)) & 1
            env[v] = bit
        yield env


def equivalent(
    lhs: Expr,
    rhs: Expr,
    var_order: Optional[Sequence[str]] = None,
) -> EquivResult:
    """
    Check equivalence of two boolean expressions by exhaustive truth-table comparison.
    Returns the first counterexample if they differ.
    """
    vars_union = sorted(vars_in(lhs) | vars_in(rhs))
    order = list(var_order) if var_order is not None else vars_union

    # sanity: ensure provided order includes all vars
    missing = set(vars_union) - set(order)
    if missing:
        raise ValueError(f"var_order missing variables: {sorted(missing)}")

    for env in _all_assignments(order):
        a = evaluate(lhs, env)
        b = evaluate(rhs, env)
        if a != b:
            return EquivResult(
                equivalent=False,
                var_order=order,
                counterexample=dict(env),
                lhs_out=a,
                rhs_out=b,
            )

    return EquivResult(
        equivalent=True,
        var_order=order,
        counterexample=None,
        lhs_out=None,
        rhs_out=None,
    )