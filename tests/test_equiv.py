from logiccraft.expr import parse
from logiccraft.equiv import equivalent


def test_equiv_true():
    # De Morgan: !(a & b) == (!a | !b)
    _, a1 = parse("out = !(a & b)")
    _, a2 = parse("out = (!a | !b)")
    res = equivalent(a1, a2)
    assert res.equivalent is True


def test_equiv_false():
    _, a1 = parse("out = a & b")
    _, a2 = parse("out = a | b")
    res = equivalent(a1, a2)
    assert res.equivalent is False
    assert res.counterexample is not None