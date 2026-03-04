from __future__ import annotations

import argparse
from pathlib import Path

from .expr import parse
from .table import truth_table, minterms
from .qm import prime_implicants, select_implicants, implicants_to_expr

def cmd_truth_table(s: str) -> int:
    name, ast = parse(s)
    vars_sorted, rows = truth_table(ast)
    header = " | ".join(vars_sorted + [name])
    print(header)
    print("-" * len(header))
    for bits, out in rows:
        print(" | ".join(str(b) for b in bits) + f" | {out}")
    return 0

def cmd_minimize(s: str) -> int:
    name, ast = parse(s)
    vars_sorted, mts = minterms(ast)
    primes = prime_implicants(mts, len(vars_sorted))
    chosen = select_implicants(mts, primes)
    expr = implicants_to_expr(chosen, vars_sorted)
    print(f"{name} = {expr}")
    return 0

def cmd_from_file(path: str, do_minimize: bool) -> int:
    p = Path(path)
    text = p.read_text(encoding="utf-8", errors="replace").strip()
    if do_minimize:
        return cmd_minimize(text)
    return cmd_truth_table(text)

def main() -> int:
    ap = argparse.ArgumentParser(prog="logiccraft")
    sub = ap.add_subparsers(dest="cmd", required=True)

    tt = sub.add_parser("truth-table", help="Print truth table for an expression or assignment")
    tt.add_argument("expr", help="Example: out_0 = (!in0 & !in1) | (in0 & in1 & in2)")

    mn = sub.add_parser("minimize", help="Minimize an expression using Quine–McCluskey (small n)")
    mn.add_argument("expr", help="Expression or assignment")

    ttf = sub.add_parser("truth-table-file", help="Read expression from a .txt file and print truth table")
    ttf.add_argument("path")

    mnf = sub.add_parser("minimize-file", help="Read expression from a .txt file and print minimized form")
    mnf.add_argument("path")

    args = ap.parse_args()
    if args.cmd == "truth-table":
        return cmd_truth_table(args.expr)
    if args.cmd == "minimize":
        return cmd_minimize(args.expr)
    if args.cmd == "truth-table-file":
        return cmd_from_file(args.path, do_minimize=False)
    if args.cmd == "minimize-file":
        return cmd_from_file(args.path, do_minimize=True)
    raise SystemExit(2)

if __name__ == "__main__":
    raise SystemExit(main())
