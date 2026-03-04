from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterator, List, Optional

# Supported operators:
# NOT: ¬ or ! or ~
# AND: ∧ or &
# OR : ∨ or |
#
# Parentheses: ( )
# Variables: in0, x, foo123

_TOKEN_RE = re.compile(
    r"""\s*(
        ¬|!|~|
        ∧|&|
        ∨|\||
        \(|\)|
        [A-Za-z_][A-Za-z0-9_]*|
        0|1
    )\s*""",
    re.VERBOSE,
)

@dataclass(frozen=True)
class Token:
    kind: str
    value: str

def tokenize(s: str) -> List[Token]:
    pos = 0
    out: List[Token] = []
    while pos < len(s):
        m = _TOKEN_RE.match(s, pos)
        if not m:
            raise ValueError(f"Unexpected character at position {pos}: {s[pos:pos+20]!r}")
        raw = m.group(1)
        pos = m.end()

        if raw in ("¬", "!", "~"):
            out.append(Token("NOT", raw))
        elif raw in ("∧", "&"):
            out.append(Token("AND", raw))
        elif raw in ("∨", "|"):
            out.append(Token("OR", raw))
        elif raw == "(":
            out.append(Token("LPAREN", raw))
        elif raw == ")":
            out.append(Token("RPAREN", raw))
        elif raw in ("0", "1"):
            out.append(Token("CONST", raw))
        else:
            out.append(Token("VAR", raw))
    return out
