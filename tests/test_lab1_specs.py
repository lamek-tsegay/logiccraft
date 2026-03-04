from logiccraft.expr import parse
from logiccraft.table import truth_table
from logiccraft.qm import prime_implicants, select_implicants, implicants_to_expr
from logiccraft.table import minterms

LAB1 = {
    "part_a": "out_0 = (¬in0 ∧ ¬in1) ∨ (in0 ∧ in1 ∧ in2)",
    "part_b": "out_0 = (in0 ∧ in1) ∨ ¬in2",
    "part_c": "out_0 = (¬in0 ∧ ¬in1 ∧ ¬in2) ∨ (in0 ∧ in1)",
}

def test_truth_tables_run():
    for k, s in LAB1.items():
        name, ast = parse(s)
        vars_sorted, rows = truth_table(ast)
        assert name == "out_0"
        assert len(vars_sorted) > 0
        assert len(rows) == 2 ** len(vars_sorted)

def test_minimize_produces_equivalent_table():
    # Minimization shouldn't change the truth table
    for k, s in LAB1.items():
        _, ast = parse(s)
        vars_sorted, rows = truth_table(ast)

        vo, mts = minterms(ast, vars_sorted)
        primes = prime_implicants(mts, len(vo))
        chosen = select_implicants(mts, primes)
        minimized = implicants_to_expr(chosen, vo)

        _, ast2 = parse("out_0 = " + minimized)
        vars2, rows2 = truth_table(ast2, vars_sorted)

        assert rows2 == rows
