# MIMO COMPILER (Lexer + Parser + Semantic Analysis)

## 📌 Overview

This project implements a **mini compiler** for a simple programming language. It covers the fundamental phases of compilation:

* ✅ Lexical Analysis (Lexer)
* ✅ Syntax Analysis (Parser - LL(1))
* ✅ Semantic Analysis (Type Checking & Validation)

The goal of this project is to simulate how a real compiler works, from reading source code to validating its correctness.

---

## 👨‍💻 Team Members

* **Oussema Guerami**
* **Maram Ghouma**
* **Mohamed Aziz Dhouibi**
* **Maram Ben Rhouma**

---

## 🧩 Language Grammar

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

## ⚙️ Features

### 🔹 Lexer

* Tokenizes input source code into:

  * Keywords (`int`, `string`)
  * Identifiers
  * Numbers
  * Strings
  * Operators (`=`, `+`)
  * Symbols (`;`)

---

### 🔹 Parser (LL(1))

* Implements a **recursive descent parser**
* Builds an **Abstract Syntax Tree (AST)**
* Supports:

  * Variable declarations
  * Assignments
  * Arithmetic expressions

---

### 🔹 Semantic Analyzer

* Type checking:

  * Prevents assigning a `string` to an `int`
  * Ensures variable declarations before use
* Detects semantic errors such as:

  * Undeclared variables
  * Type mismatches

---

## 🧪 Example Inputs

### ✅ Valid Code

```c
int x;
x = 5;

string name;
name = "alice";

x = 5 + 2;
```

### ❌ Invalid Code

```c
int x;
x = "hello";   // Type error

y = 5;         // Undeclared variable
```

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mini-compiler.git
cd mini-compiler
```

### 2. Run the compiler

```bash
python compiler.py
```

---

## 📂 Project Structure

```
mini-compiler/
│
├── compiler.py      # Lexer + Parser + Tests
├── semantic.py      # Semantic Analyzer (if separated)
├── README.md
```

---

## 🛠️ Technologies Used

* Python 🐍
* Regular Expressions (`re`)
* Recursive Descent Parsing

---

## 📈 Learning Outcomes

Through this project, we learned:

* How compilers are structured
* The difference between **syntax errors** and **semantic errors**
* How to design and implement a **grammar**
* Building and traversing an **AST**
* Implementing **type checking**

---

## 🔮 Future Improvements

* Add support for:

  * `float` type
  * Control structures (`if`, `while`)
* Improve error messages
* Build a simple interpreter or code generator

---

## 📜 License

This project is for educational purposes.

---

## ⭐ Acknowledgment

This project was developed as part of a **Compiler Design / Systems Programming course**.

---

💡 *Feel free to fork, improve, and experiment with the compiler!*
