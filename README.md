# LogicCraft

LogicCraft is a lightweight toolkit for analyzing and optimizing digital logic expressions.
It provides utilities for parsing boolean expressions, generating truth tables, and minimizing logic using classical algorithms used in hardware design.

The project was built to explore how high-level logical specifications translate into optimized digital circuits and to provide a simple command-line workflow for reasoning about boolean systems.



## Overview

Digital systems are built from combinations of logical operators such as AND, OR, and NOT.
When designing or analyzing these systems, engineers often need to:

* verify that a logical specification behaves as expected
* generate complete truth tables
* simplify logic expressions to reduce circuit complexity
* test equivalence between multiple implementations of the same logic

LogicCraft provides a small toolkit to support these tasks.



## Features

* Boolean expression parsing
* Truth table generation for arbitrary boolean expressions
* Logic minimization using the Quine–McCluskey algorithm
* Command-line interface for quick experimentation
* Unit tests validating logical equivalence across examples



## Example

Given the boolean specification:

```
out_0 = (!in0 & !in1) | (in0 & in1 & in2)
```

Generate the truth table:

```
logiccraft truth-table "out_0 = (!in0 & !in1) | (in0 & in1 & in2)"
```

Minimize the expression:

```
logiccraft minimize "out_0 = (in0 & in1) | !in2"
```



## Installation

Clone the repository and install in development mode:

```
git clone https://github.com/YOUR_USERNAME/logiccraft.git
cd logiccraft

python -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
```

Run tests:

```
pytest
```



## Project Structure

```
logiccraft
│
├── src/logiccraft
│   ├── tokenize.py
│   ├── expr.py
│   ├── table.py
│   ├── qm.py
│   └── cli.py
│
├── tests
│   └── test_logic_specs.py
│
├── examples
│   └── lab1
│
└── README.md
```

Core components:

* **tokenize.py** – tokenization of boolean expressions
* **expr.py** – expression parsing and evaluation
* **table.py** – truth table generation
* **qm.py** – Quine–McCluskey minimization algorithm
* **cli.py** – command-line interface



## Design Goals

LogicCraft was designed to be:

* **small and understandable** – easy to read and extend
* **algorithmically transparent** – core logic algorithms implemented directly in Python
* **tool-oriented** – usable from both code and the command line



## Future Work

Planned extensions include:

* circuit verification against logical specifications
* Karnaugh map visualization
* exporting minimized expressions to Verilog
* equivalence checking between logic implementations



## License

MIT License
