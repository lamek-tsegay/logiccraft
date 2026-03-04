from __future__ import annotations

import itertools
from typing import Dict, Iterable, List, Sequence, Tuple

from .expr import Expr, evaluate, vars_in

def truth_table(ast: Expr, var_order: Sequence[str] | None = None) -> Tuple[List[str], List[Tuple[Tuple[int, ...], int]]]:
    vars_sorted = sorted(vars_in(ast)) if var_order is None else list(var_order)
    rows: List[Tuple[Tuple[int, ...], int]] = []
    for bits in itertools.product([0, 1], repeat=len(vars_sorted)):
        env = dict(zip(vars_sorted, bits))
        out = evaluate(ast, env)
        rows.append((bits, out))
    return vars_sorted, rows

def minterms(ast: Expr, var_order: Sequence[str] | None = None) -> Tuple[List[str], List[int]]:
    vars_sorted, rows = truth_table(ast, var_order)
    mts: List[int] = []
    for bits, out in rows:
        if out == 1:
            idx = 0
            for b in bits:
                idx = (idx << 1) | b
            mts.append(idx)
    return vars_sorted, mts
