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

```bash
git clone https://github.com/nikolaslukowicz/QAOA-MaxCut.git
cd QAOA-MaxCut
pip install qiskit qiskit-aer scipy numpy networkx matplotlib
```

## Usage

Run the main script:

```bash
python main.py
```

The program optimizes a QAOA circuit for a given graph and evaluates the results against a classical MaxCut solution.

## Future Work

- Benchmark different QAOA circuit depths and classical optimizers
- Evaluate performance on different graph structures and sizes
- Compare variational QAOA with adiabatic-inspired parameter initialization
- Investigate finite-shot sampling and quantum noise

## Status

**Work in progress** — Core QAOA implementation and classical benchmarking functionality are available. Further experiments and performance evaluations are planned.
