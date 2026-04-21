# MOMA Compiler Playground

A mini compiler project for a small language, with an interactive web interface.

It demonstrates the three core compilation phases:
- Lexical analysis (`lexical_analyser.py`)
- Syntax analysis / parsing (`parser.py`)
- Semantic analysis (`semantic_analyzer.py`)

---

## Overview

This project parses and validates one statement at a time:
- Variable declarations (e.g., `int x;`, `string name;`)
- Assignments (e.g., `x = 5;`, `name = "alice";`)
- `+` expressions with type consistency checks

The web app (`start.py` + `index.html`) visualizes each stage and keeps a session symbol table.

---

## Language Grammar

```text
stmt   → decl | assign

decl   → TYPE ID ';'

assign → ID '=' expr ';'

expr   → term expr'
expr'  → '+' term expr' | ε

term   → ID | NUM | STRING

TYPE   → 'int' | 'string'
```

---

## Features

- **Lexer**
  - Tokenizes keywords, identifiers, numbers, strings, operators, and semicolons.
- **Parser (recursive descent)**
  - Builds AST nodes (`Decl`, `Assign`, `BinOp`, `Num`, `Id`, `Str`).
- **Semantic analyzer**
  - Checks declaration-before-use.
  - Checks duplicate declarations.
  - Checks assignment type compatibility.
  - Checks operand type compatibility for `+`.
- **Web Playground**
  - Runs analysis through `/api/run`.
  - Supports symbol-table reset via `/api/reset`.

---

## Project Structure

```text
MOMA_compiler-/
├── lexical_analyser.py   # Lexer
├── parser.py             # Parser + AST nodes
├── semantic_analyzer.py  # Semantic analyzer + symbol table
├── start.py              # Flask backend + API routes
├── index.html            # Frontend playground
└── README.md
```

---

## Requirements

- Python 3.10+
- Flask
- flask-cors

Install dependencies:

```bash
pip install flask flask-cors
```

---

## Run the Playground

From the repository root:

```bash
python start.py
```

Then open:

```text
http://localhost:5050
```

---

## Quick Example

### Valid

```c
int x;
x = 5 + 2;
```

### Invalid

```c
int x;
x = "hello";   // type mismatch
```

---

## Run Module Self-Tests

Each module includes a small `__main__` test block:

```bash
python lexical_analyser.py
python parser.py
python semantic_analyzer.py
```

---

## Team Members

- Oussema Guerami
- Maram Ghouma
- Mohamed Aziz Dhouibi
- Maram Ben Rhouma

---

## License

This project is for educational purposes.
