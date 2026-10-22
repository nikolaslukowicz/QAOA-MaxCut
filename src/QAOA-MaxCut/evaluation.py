from circuit import *
from classical import *

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