# Scheme Interpreter

A lightweight interpreter for the Scheme programming language, built in Python. It supports many core features of Scheme, including conditionals, lists, recursion, variable bindings, and functional programming utilities. I implemented this as a lab assignment in the MIT 6.101 course.

## Supported Features

This interpreter supports:

1. **REPL** – Write and evaluate scheme code in an interactive manner.
2. **Variables** - Support for variable definitions and variable scopes (frames).
3. **Functions** – Basic arithmetic, logic, and function definitions in Scheme.
4. **Scheme Syntax Errors** – Handles invalid syntax with informative error messages.
5. **Conditionals** – Includes `if`, `cond`, boolean logic (`#t`, `#f`), and comparison operators (`=`, `<`, `>`, `not`, etc.).
6. **Lists** – Full support for pairs (`cons`, `car`, `cdr`), linked lists, and the empty list `()`.
7. **Built-in List Functions** – Functions like `length`, `append`, `map`, `filter`, `reduce`, etc.
8. **Evaluating Multiple Expressions** – Use `begin` to evaluate expressions in sequence.
9. **Reading From Files** – Load and run Scheme code from `.scm` files.
10. **Command-Line Arguments** – Evaluate Scheme code passed directly from the command line.
11. **Map, Filter, and Reduce** – Includes higher-order functions with lambda support.
12. **Variable-Binding Manipulation**:
    - `define` – Create variables and functions.
    - `let` – Scoped variable declarations.
    - `set!` – Reassign existing variables.
    - `del` – Delete variable bindings.

## Running

1. Download this repository with `git clone https://github.com/salvi1mucyo/lisp-interpreter.git`
2. Launch the interpreter:
```bash
python3 lab.py
```
