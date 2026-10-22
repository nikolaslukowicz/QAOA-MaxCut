import networkx as nx
import matplotlib.pyplot as plt

from qiskit.visualization import plot_histogram

from optimizer import ScipyOptimizer
from qaoa import QAOAFacade


def main():
    graph = nx.cycle_graph(4)

    optimizer = ScipyOptimizer(
        method="COBYLA",
        maxiter=200
    )

    qaoa = QAOAFacade(
        graph=graph,
        p=5,
        optimizer=optimizer
    )

    results = qaoa.run()

    print("Optimal gammas:", results["gammas"])
    print("Optimal betas:", results["betas"])
    print("Best cut:", results["best_cut"])
    print("Optimal cut:", results["optimal_cut"])
    print(
        "Optimal probability:",
        f"{results['optimal_probability']:.2%}"
    )

    plot_histogram(results["counts"])
    plt.show()


if __name__ == "__main__":
    main()