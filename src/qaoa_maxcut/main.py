import networkx as nx
import matplotlib.pyplot as plt

from qiskit.visualization import plot_histogram

from .optimizer import ScipyOptimizer
from .qaoa import QAOAFacade


def main(p: int, verbose: bool = True, plot: bool = True):
    if verbose:
        print(f"Running QAOA with p = {p}")
    graph = nx.cycle_graph(4)

    optimizer = ScipyOptimizer(
        method="COBYLA",
        maxiter=200
    )

    qaoa = QAOAFacade(
        graph=graph,
        p=p,
        optimizer=optimizer
    )

    results = qaoa.run()

    if verbose:
        print("Optimal gammas:", results["gammas"])
        print("Optimal betas:", results["betas"])
        print("Best cut:", results["best_cut"])
        print("Optimal cut:", results["optimal_cut"])
        print(
            "Optimal probability:",
            f"{results['optimal_probability']:.2%}"
        )

    if plot:
        plot_histogram(results["counts"])
        plt.show()

    return results


if __name__ == "__main__":
    main(p=1)