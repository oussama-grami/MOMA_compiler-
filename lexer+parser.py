"""
==================== GRAMMAIRE ====================

stmt  → decl | assign

decl  → TYPE ID ';'

assign → ID '=' expr ';'

expr  → term expr'
expr' → '+' term expr' | ε

term  → ID | NUM | STRING

TYPE  → 'int' | 'string'

==================================================
"""

import re

# ===================== LEXER =====================

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


# ===================== AST =====================

class Decl:
    def __init__(self, type_, name):
        self.type = type_
        self.name = name

    def __repr__(self):
        return f"Decl({self.type}, {self.name})"


class Assign:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return f"Assign({self.name}, {self.expr})"


class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, '{self.op}', {self.right})"


class Num:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Num({self.value})"


class Id:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Id({self.name})"


class Str:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Str('{self.value}')"


# ===================== PARSER =====================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, type_, value=None):
        tok = self.current()
        if tok and tok.type == type_ and (value is None or tok.value == value):
            self.pos += 1
            return tok
        raise SyntaxError(f"Expected {type_} {value}, got {tok}")

    # stmt → decl | assign
    def stmt(self):
        tok = self.current()

        if tok.type == 'KEYWORD' and tok.value in ('int', 'string'):
            return self.decl()
        elif tok.type == 'ID':
            return self.assign()
        else:
            raise SyntaxError("Invalid statement")

    # decl → TYPE ID ';'
    def decl(self):
        type_ = self.eat('KEYWORD').value
        name = self.eat('ID').value
        self.eat('SEMI')
        return Decl(type_, name)

    # assign → ID '=' expr ';'
    def assign(self):
        name = self.eat('ID').value
        self.eat('OP', '=')
        expr = self.expr()
        self.eat('SEMI')
        return Assign(name, expr)

    # expr → term expr'
    def expr(self):
        node = self.term()
        while self.current() and self.current().value == '+':
            op = self.eat('OP').value
            right = self.term()
            node = BinOp(node, op, right)
        return node

    # term → ID | NUM | STRING
    def term(self):
        tok = self.current()

        if tok.type == 'NUM':
            self.eat('NUM')
            return Num(tok.value)
        elif tok.type == 'ID':
            self.eat('ID')
            return Id(tok.value)
        elif tok.type == 'STRING':
            self.eat('STRING')
            return Str(tok.value)
        else:
            raise SyntaxError("Invalid term")


# ===================== TEST =====================

if __name__ == '__main__':
    tests = [
        "int x;",
        "x = 5;",
        "x = 5 + 2;",
        "string name;",
        'name = "alice";',
        'name = "hello" + " world";'
    ]

    for src in tests:
        print("Input :", src)
        try:
            tokens = tokenize(src)
            print("Tokens:", tokens)

            parser = Parser(tokens)
            ast = parser.stmt()
            print("AST   :", ast)

        except SyntaxError as e:
            print("ERROR :", e)

        print()