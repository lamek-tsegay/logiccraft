from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Union, Optional

from .tokenize import Token, tokenize

# AST nodes
@dataclass(frozen=True)
class Var:
    name: str

@dataclass(frozen=True)
class Const:
    value: int  # 0 or 1

@dataclass(frozen=True)
class Not:
    x: "Expr"

@dataclass(frozen=True)
class And:
    a: "Expr"
    b: "Expr"

@dataclass(frozen=True)
class Or:
    a: "Expr"
    b: "Expr"

Expr = Union[Var, Const, Not, And, Or]

class Parser:
    def __init__(self, toks: List[Token]):
        self.toks = toks
        self.i = 0

    def peek(self) -> Optional[Token]:
        return self.toks[self.i] if self.i < len(self.toks) else None

    def eat(self, kind: str) -> Token:
        tok = self.peek()
        if tok is None or tok.kind != kind:
            raise ValueError(f"Expected {kind}, got {tok}")
        self.i += 1
        return tok

    # Grammar (precedence: NOT > AND > OR)
    # expr  := or_expr
    # or_expr := and_expr (OR and_expr)*
    # and_expr := not_expr (AND not_expr)*
    # not_expr := (NOT not_expr) | primary
    # primary := VAR | CONST | LPAREN expr RPAREN

    def parse(self) -> Expr:
        e = self.or_expr()
        if self.peek() is not None:
            raise ValueError(f"Unexpected token: {self.peek()}")
        return e

    def or_expr(self) -> Expr:
        e = self.and_expr()
        while self.peek() is not None and self.peek().kind == "OR":
            self.eat("OR")
            rhs = self.and_expr()
            e = Or(e, rhs)
        return e

    def and_expr(self) -> Expr:
        e = self.not_expr()
        while self.peek() is not None and self.peek().kind == "AND":
            self.eat("AND")
            rhs = self.not_expr()
            e = And(e, rhs)
        return e

    def not_expr(self) -> Expr:
        if self.peek() is not None and self.peek().kind == "NOT":
            self.eat("NOT")
            return Not(self.not_expr())
        return self.primary()

    def primary(self) -> Expr:
        tok = self.peek()
        if tok is None:
            raise ValueError("Unexpected end of input")
        if tok.kind == "VAR":
            self.eat("VAR")
            return Var(tok.value)
        if tok.kind == "CONST":
            self.eat("CONST")
            return Const(int(tok.value))
        if tok.kind == "LPAREN":
            self.eat("LPAREN")
            e = self.or_expr()
            self.eat("RPAREN")
            return e
        raise ValueError(f"Unexpected token: {tok}")

def parse(expr_or_assignment: str) -> Tuple[str, Expr]:
    """Parse either:
      - 'out_0 = ...'  (returns ('out_0', ast))
      - '...'         (returns ('out', ast))
    """
    s = expr_or_assignment.strip()
    if "=" in s:
        lhs, rhs = s.split("=", 1)
        out_name = lhs.strip()
        rhs_s = rhs.strip()
    else:
        out_name = "out"
        rhs_s = s

    ast = Parser(tokenize(rhs_s)).parse()
    return out_name, ast

def vars_in(ast: Expr) -> Set[str]:
    if isinstance(ast, Var):
        return {ast.name}
    if isinstance(ast, Const):
        return set()
    if isinstance(ast, Not):
        return vars_in(ast.x)
    if isinstance(ast, And) or isinstance(ast, Or):
        return vars_in(ast.a) | vars_in(ast.b)
    raise TypeError(ast)

def evaluate(ast: Expr, env: Dict[str, int]) -> int:
    if isinstance(ast, Var):
        try:
            v = env[ast.name]
        except KeyError as e:
            raise KeyError(f"Missing variable {ast.name!r} in env") from e
        return 1 if v else 0
    if isinstance(ast, Const):
        return 1 if ast.value else 0
    if isinstance(ast, Not):
        return 1 - evaluate(ast.x, env)
    if isinstance(ast, And):
        return evaluate(ast.a, env) & evaluate(ast.b, env)
    if isinstance(ast, Or):
        return evaluate(ast.a, env) | evaluate(ast.b, env)
    raise TypeError(ast)
