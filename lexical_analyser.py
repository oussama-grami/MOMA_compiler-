# ===================== MILESTONE 1 : LEXER =====================

import re

TOKEN_SPEC = [
    ('KEYWORD',  r'\b(?:int|string)\b'),
    ('STRING',   r'"[^"]*"'),
    ('ID',       r'[a-zA-Z_]\w*'),
    ('NUM',      r'\d+'),
    ('OP',       r'[=+]'),
    ('SEMI',     r';'),
    ('SKIP',     r'[ \t\n]+'),
    ('MISMATCH', r'.'),
]

MASTER_RE = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC))


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.type == 'KEYWORD':
            return f"KW('{self.value}')"
        if self.type == 'ID':
            return f"ID('{self.value}')"
        if self.type == 'NUM':
            return f"NUM({self.value})"
        if self.type == 'STRING':
            return f"STR('{self.value}')"
        return repr(self.value)


def tokenize(source_code):
    tokens = []
    for mo in MASTER_RE.finditer(source_code):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'NUM':
            tokens.append(Token('NUM', int(value)))
        elif kind == 'KEYWORD':
            tokens.append(Token('KEYWORD', value))
        elif kind == 'ID':
            tokens.append(Token('ID', value))
        elif kind == 'STRING':
            tokens.append(Token('STRING', value.strip('"')))
        elif kind in ('OP', 'SEMI'):
            tokens.append(Token(kind, value))
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Unexpected character {value!r}")

    return tokens


# ===================== TEST =====================

if __name__ == '__main__':
    tests = [
        "int x;",
        "x = 5;",
        "x = 5 + 2;",
        "string name;",
        'name = "alice";',
        'name = "hello" + " world";',
    ]

    for src in tests:
        print("Input :", src)
        tokens = tokenize(src)
        print("Tokens:", tokens)
        print()