# LogicCraft

Turn “digital logic lab” circuits into a **useful engineering tool**.

LogicCraft is a lightweight toolkit that can:

- parse boolean expressions (supports `¬ ∧ ∨` plus `! & |` aliases)
- evaluate expressions for input assignments
- generate truth tables
- minimize logic with a small Quine–McCluskey implementation (good for small # of inputs)
- ship with your CSE12 Lab 1 artifacts as **examples + regression tests**

## Why this is a real project (not just homework)

In real hardware/embedded work, you often need to:
- confirm an implementation matches a spec (truth-table equivalence)
- simplify logic to reduce gates / cost / power
- generate repeatable tests for a combinational block

This repo packages that workflow into a CLI + library.

## Install (dev)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## CLI usage

### Truth table

```bash
logiccraft truth-table "out_0 = (¬in0 ∧ ¬in1) ∨ (in0 ∧ in1 ∧ in2)"
```

### Minimize

```bash
logiccraft minimize "out_0 = (in0 ∧ in1) ∨ ¬in2"
```

## Included examples

See `examples/lab1/` for your original `.dig` files + the boolean specs you wrote in `part_a.txt`, `part_b.txt`, `part_c.txt`.

## Next upgrades (if you want to go bigger)
- parse `.dig` files and extract gate-level netlists
- equivalence check: `.dig` implementation vs expression spec
- export minimized expressions as Verilog
- interactive Karnaugh map rendering
