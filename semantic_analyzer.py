# ===================== MILESTONE 3 : SEMANTIC ANALYZER =====================

from lexical_analyser import tokenize
from parser import Parser, Decl, Assign, BinOp, Num, Id, Str


# ── Semantic Error ──────────────────────────────────────────────

class SemanticError(Exception):
    """Raised when a semantic rule is violated."""
    pass


# ── Symbol Table ────────────────────────────────────────────────

class SymbolTable:
    """
    Keeps track of declared variables and their types.
    Each entry: name (str) -> type (str)  e.g. 'x' -> 'int'
    """
    def __init__(self):
        self._table = {}

    def declare(self, name: str, type_: str):
        if name in self._table:
            raise SemanticError(f"Variable '{name}' is already declared.")
        self._table[name] = type_

    def lookup(self, name: str) -> str:
        if name not in self._table:
            raise SemanticError(f"Variable '{name}' used before declaration.")
        return self._table[name]

    def __repr__(self):
        return f"SymbolTable({self._table})"


# ── Semantic Analyzer ───────────────────────────────────────────

class SemanticAnalyzer:
    """
    Walks the AST and enforces:
      1. No variable used before declaration       (scope check)
      2. No variable declared twice                (duplicate check)
      3. Assigned value matches declared type      (type check)
      4. Both sides of '+' have the same type      (expression check)
    """

    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, node):
        method = f"visit_{type(node).__name__}"
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise SemanticError(f"No visitor for node type '{type(node).__name__}'")

    # decl → registers the variable in the symbol table
    def visit_Decl(self, node: Decl):
        self.symbol_table.declare(node.name, node.type)
        return node.type

    # assign → checks variable is declared and types match
    def visit_Assign(self, node: Assign):
        declared_type = self.symbol_table.lookup(node.name)
        expr_type     = self.analyze(node.expr)
        if declared_type != expr_type:
            raise SemanticError(
                f"Type mismatch: '{node.name}' is '{declared_type}' "
                f"but assigned a '{expr_type}' value."
            )
        return declared_type

    # binop → both operands must be the same type
    def visit_BinOp(self, node: BinOp):
        left_type  = self.analyze(node.left)
        right_type = self.analyze(node.right)
        if left_type != right_type:
            raise SemanticError(
                f"Type mismatch in expression: "
                f"cannot add '{left_type}' and '{right_type}'."
            )
        return left_type

    def visit_Num(self, node: Num):
        return 'int'

    def visit_Str(self, node: Str):
        return 'string'

    def visit_Id(self, node: Id):
        return self.symbol_table.lookup(node.name)


# ── TEST ────────────────────────────────────────────────────────

if __name__ == '__main__':

    # shared analyzer → keeps the symbol table across all statements
    analyzer = SemanticAnalyzer()

    tests = [
        # (source,                         expect_error)
        ("int x;",                          False),
        ("string name;",                    False),
        ("x = 5;",                          False),
        ("x = 5 + 2;",                      False),
        ('name = "alice";',                 False),
        ('name = "hello" + " world";',      False),
        ("y = 10;",                         True),   # undeclared variable
        ('x = "hello";',                    True),   # int <- string
        ("name = 42;",                      True),   # string <- int
        ('x = 1 + "oops";',                 True),   # int + string in BinOp
    ]

    for src, expect_error in tests:
        print("Input :", src)
        try:
            tokens   = tokenize(src)
            ast      = Parser(tokens).stmt()
            inferred = analyzer.analyze(ast)
            print("AST   :", ast)
            print("Type  :", inferred)
            print("Table :", analyzer.symbol_table)
            result = "✓ OK" if not expect_error else "✗ Expected a SemanticError but got none"

        except SemanticError as e:
            result = f"✓ SemanticError -> {e}" if expect_error else f"✗ Unexpected SemanticError -> {e}"

        except SyntaxError as e:
            result = f"✗ SyntaxError -> {e}"

        print("RESULT:", result)
        print()