import re

TOKEN_SPEC = [
    ('KEYWORD',  r'\b(?:if|then|else)\b'),
    ('ID',       r'[a-zA-Z_]\w*'),
    ('NUM',      r'\d+'),
    ('OP',       r'[+\-*/=><]'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('SEMI',     r';'),
    ('SKIP',     r'[ \t\n]+'),
    ('MISMATCH', r'.'),
]

MASTER_RE = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)) #This line loops over TOKEN_SPEC and turns each one into a named group in regex syntax


class Token:
    def __init__(self, type_, value):
        self.type  = type_
        self.value = value

    def __repr__(self):
        if self.type == 'KEYWORD':
            return f"KW('{self.value}')"
        if self.type == 'ID':
            return f"ID('{self.value}')"
        if self.type == 'NUM':
            return f"NUM({self.value})"
        return repr(self.value)


def tokenize(source_code: str) -> list[Token]:
    tokens = []
    for mo in MASTER_RE.finditer(source_code):    #scans the string from left to right, and at each position it tries every | alternative in order. When one matches, it returns a match object mo and advances past it.
        kind  = mo.lastgroup
        value = mo.group()
        if kind == 'NUM':
            tokens.append(Token('NUM', int(value)))
        elif kind == 'KEYWORD':
            tokens.append(Token('KEYWORD', value))
        elif kind == 'ID':
            tokens.append(Token('ID', value))
        elif kind in ('OP', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMI'):
            tokens.append(Token(kind, value))
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Unexpected character {value!r}")
    return tokens

if __name__ == '__main__':
    tests = [
        "x = 5 + 2;",
        "z = x * (y - 3);",
        "if a = b then\n    a = a + 1;\nelse\n    b = b - 1;",
        "if x > 10 then { x = x - 1; }",
    ]

    for src in tests:
        print("Input :", src.replace('\n', ' ↵ '))
        try:
            toks = tokenize(src)
            print("Output:", toks)
        except SyntaxError as e:
            print("ERROR :", e)
        print()