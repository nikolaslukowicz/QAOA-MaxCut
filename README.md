# QAOA MaxCut Solver

A Python implementation of the **Quantum Approximate Optimization Algorithm (QAOA)** for solving the Maximum Cut (MaxCut) problem using Qiskit.

The project explores hybrid quantum-classical optimization and compares QAOA results against classical MaxCut solvers.

## Features

- Parameterized QAOA circuits with configurable depth
- Quantum simulation using Qiskit Aer
- Classical parameter optimization using SciPy
- Exact MaxCut solution via exhaustive search
- Evaluation of optimal solution probabilities and measurement distributions
- Modular architecture using Strategy and Facade design patterns

## Installation

Clone the repository:

```bash
git clone https://github.com/nikolaslukowicz/QAOA-MaxCut.git
cd qaoa_maxcut
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

Install the project and its dependencies:

```bash
python -m pip install -e .
```

## Usage

Run the main script from the project root:

```bash
python main.py
```

The program constructs and optimizes a QAOA circuit for a MaxCut instance, simulates its execution, and compares the results against an exact classical solution.

The graph, QAOA circuit depth (`p`), and optimizer settings can be configured in `main.py`.
## Future Work

- Benchmark different QAOA circuit depths and classical optimizers
- Evaluate performance on different graph structures and sizes
- Compare variational QAOA with adiabatic-inspired parameter initialization
- Investigate finite-shot sampling and quantum noise

## Status

**Work in progress** — Core QAOA implementation and classical benchmarking functionality are available. Further experiments and performance evaluations are planned.
