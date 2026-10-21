import numpy as np
import networkx as nx

from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from itertools import product


def maxcut_value(bits, graph):
    """Number of edges connecting different partitions."""
    return sum(
        bits[i] != bits[j]
        for i, j in graph.edges()
    )

def classical_maxcut_exhaustive_search(graph):
    n = graph.number_of_nodes()

    #Generate all possible bitstrings
    best_cut = 0

    for bits in product([0, 1], repeat=n):
        cut = maxcut_value(bits, graph)

        if cut > best_cut:
            best_cut = cut

    return best_cut

def optimal_solution_probability(counts, graph, optimal_cut):
    successful_shots = sum(
        count
        for bitstring, count in counts.items()
        if maxcut_value(
            [int(b) for b in bitstring[::-1]],
            graph
        ) == optimal_cut
    )

    return successful_shots / sum(counts.values())

def build_qaoa_circuit(graph, gammas, betas, p):
    """Build a p-layer QAOA circuit for MaxCut."""
    n = graph.number_of_nodes()

    if len(gammas) != len(betas):
        raise ValueError('gammas and betas must have same length')

    #Initial uniform superposition
    qc = QuantumCircuit(n)
    qc.h(range(n))

    #Apply p QAOA layers
    for y in range(p):
        for i,j in graph.edges():
            #MaxCut Hamiltonian
            qc.rzz(-gammas[y], i, j)
        #Mixer Hamiltonian
        qc.rx(2*betas[y], range(n))

    qc.measure_all()

    return qc


def objective(params, graph, p, simulator, shots=2000):
    # Split parameter vector
    gammas = params[:p]
    betas = params[p:]

    # Construct the QAOA circuit
    qc = build_qaoa_circuit(graph, gammas, betas, p)

    # Run it on the simulator
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()

    # Calculate expected MaxCut value
    total_shots = sum(counts.values())

    expected_cut = sum(
        count * maxcut_value(
            [int(bit) for bit in bitstring[::-1]],
            graph
        )
        for bitstring, count in counts.items()
    ) / total_shots

    # Negative because SciPy minimizes
    return -expected_cut


def optimize_qaoa(graph, p):
    simulator = AerSimulator()

    # Initial parameters: p gammas, p betas
    rng = np.random.default_rng(42)

    initial_params = rng.uniform(
        0, np.pi, size=2 * p
    )

    result = minimize(
        fun=objective,
        x0=initial_params,
        args=(graph, p, simulator, 2000),
        method="COBYLA",
        options={
            "maxiter": 200,
            "rhobeg": 0.3,
            "tol": 1e-4
        }
    )

    optimal_gammas = result.x[:p]
    optimal_betas = result.x[p:]

    print("Optimization successful:", result.success)
    print("Optimal gammas:", optimal_gammas)
    print("Optimal betas:", optimal_betas)
    print("Best estimated cut value:", -result.fun)

    return optimal_gammas, optimal_betas

def main():
    graph = nx.cycle_graph(4)
    p = 2

    # Classical optimization
    gammas, betas = optimize_qaoa(graph, p)

    # Build optimized quantum circuit
    qc = build_qaoa_circuit(graph, gammas, betas, p)

    simulator = AerSimulator()
    counts = simulator.run(qc, shots=10000).result().get_counts()

    # Evaluate optimal solutions
    best_bitstring = max(
        counts,
        key=lambda bits: maxcut_value(
            [int(b) for b in bits[::-1]], graph
        )
    )

    best_cut = maxcut_value(
        [int(b) for b in best_bitstring[::-1]], graph
    )

    #Get the true optimum for the graph
    'TODO: implement other classical solver and compare'
    optimal_cut = classical_maxcut_exhaustive_search(graph)

    #Calculate optimal solution
    optimal_probability = optimal_solution_probability(
        counts, graph, optimal_cut
    )


    print("Best bitstring:", best_bitstring)
    print("Best sampled cut:", best_cut)
    print("Optimal cut:", optimal_cut)
    print("Optimal solution probability:",
          f"{optimal_probability:.2%}")

    fig = plot_histogram(counts)
    plt.show()


if __name__ == "__main__":
    main()
