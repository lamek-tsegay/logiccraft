from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Set, Tuple

# Minimal Quine–McCluskey for small n (good for labs / small logic blocks)

@dataclass(frozen=True)
class Implicant:
    bits: Tuple[int | None, ...]   # None = don't care
    covers: frozenset[int]         # minterms covered

def _popcount(x: int) -> int:
    return bin(x).count("1")

def _to_bits(n: int, width: int) -> Tuple[int, ...]:
    return tuple((n >> (width - 1 - i)) & 1 for i in range(width))

def _combine(a: Implicant, b: Implicant) -> Implicant | None:
    diff = 0
    new_bits: List[int | None] = []
    for x, y in zip(a.bits, b.bits):
        if x == y:
            new_bits.append(x)
        elif x is None or y is None:
            return None
        else:
            diff += 1
            new_bits.append(None)
            if diff > 1:
                return None
    if diff == 1:
        return Implicant(tuple(new_bits), a.covers | b.covers)
    return None

def prime_implicants(minterms: Sequence[int], num_vars: int) -> List[Implicant]:
    groups: Dict[int, List[Implicant]] = {}
    for m in sorted(set(minterms)):
        bits = _to_bits(m, num_vars)
        imp = Implicant(bits, frozenset([m]))
        groups.setdefault(sum(bits), []).append(imp)

    primes: Set[Implicant] = set()
    while groups:
        next_groups: Dict[int, List[Implicant]] = {}
        used: Set[Implicant] = set()

        keys = sorted(groups.keys())
        for k in keys:
            for a in groups.get(k, []):
                for b in groups.get(k + 1, []):
                    c = _combine(a, b)
                    if c is not None:
                        used.add(a); used.add(b)
                        ones = sum(1 for t in c.bits if t == 1)
                        next_groups.setdefault(ones, []).append(c)

        for k in keys:
            for imp in groups[k]:
                if imp not in used:
                    primes.add(imp)

        # dedupe next_groups
        dedup: Dict[int, List[Implicant]] = {}
        for k, imps in next_groups.items():
            uniq = list({imp: None for imp in imps}.keys())
            dedup[k] = uniq
        groups = dedup

    return sorted(primes, key=lambda i: (len(i.covers), i.bits))

def select_implicants(minterms: Sequence[int], primes: Sequence[Implicant]) -> List[Implicant]:
    mts = set(minterms)
    if not mts:
        return []

    cover_map: Dict[int, List[Implicant]] = {m: [] for m in mts}
    for p in primes:
        for m in p.covers:
            if m in cover_map:
                cover_map[m].append(p)

    chosen: Set[Implicant] = set()
    uncovered = set(mts)

    # essential primes
    changed = True
    while changed:
        changed = False
        for m in list(uncovered):
            options = cover_map.get(m, [])
            if len(options) == 1:
                p = options[0]
                if p not in chosen:
                    chosen.add(p)
                    uncovered -= set(p.covers)
                    changed = True

    # greedy for the rest
    while uncovered:
        best = max(primes, key=lambda p: len(set(p.covers) & uncovered))
        chosen.add(best)
        uncovered -= set(best.covers)

    return sorted(chosen, key=lambda i: (-len(i.covers), i.bits))

def implicants_to_expr(implicants: Sequence[Implicant], var_order: Sequence[str]) -> str:
    if not implicants:
        return "0"
    terms: List[str] = []
    for imp in implicants:
        lits: List[str] = []
        for v, b in zip(var_order, imp.bits):
            if b is None:
                continue
            lits.append(v if b == 1 else f"¬{v}")
        if not lits:
            return "1"
        terms.append("(" + " ∧ ".join(lits) + ")")
    return " ∨ ".join(terms)
