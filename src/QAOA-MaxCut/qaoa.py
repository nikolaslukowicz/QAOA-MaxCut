import numpy as np

from qiskit_aer import AerSimulator
from evaluation import *

class QAOAFacade:

    def __init__(self, graph, p, optimizer):
        self.graph = graph
        self.p = p
        self.optimizer = optimizer
        self.simulator = AerSimulator()

    def run(self):
        # Initial parameters
        initial_params = np.random.uniform(
            0, np.pi, size=2 * self.p
        )

        # Objective for the chosen strategy
        def cost_function(params):
            return objective(
                params,
                self.graph,
                self.p,
                self.simulator,
                2000
            )

        # Strategy Pattern
        result = self.optimizer.optimize(
            cost_function,
            initial_params
        )

        gammas = result.x[:self.p]
        betas = result.x[self.p:]

        # Build and execute optimized circuit
        qc = build_qaoa_circuit(
            self.graph, gammas, betas, self.p
        )

        counts = self.simulator.run(
            qc, shots=10000
        ).result().get_counts()

        # Classical benchmark
        optimal_cut = classical_maxcut_exhaustive_search(
            self.graph
        )

        optimal_probability = optimal_solution_probability(
            counts,
            self.graph,
            optimal_cut
        )

        best_bitstring = max(
            counts,
            key=lambda bits: maxcut_value(
                [int(b) for b in bits[::-1]],
                self.graph
            )
        )

        best_cut = maxcut_value(
            [int(b) for b in best_bitstring[::-1]],
            self.graph
        )

        return {
            "gammas": gammas,
            "betas": betas,
            "optimization_success": result.success,
            "estimated_cut": -result.fun,
            "best_bitstring": best_bitstring,
            "best_cut": best_cut,
            "optimal_cut": optimal_cut,
            "optimal_probability": optimal_probability,
            "counts": counts
        }