import time
import csv
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

from qaoa_maxcut.main import main


import numpy as np

def benchmark_depths(depths=range(1, 11), repetitions=10):
    benchmark_results = []

    for p in depths:
        probabilities = []
        runtimes = []

        for run in range(repetitions):
            start = time.perf_counter()

            results = main(p, verbose=False, plot=False)

            runtime = time.perf_counter() - start

            probabilities.append(results["optimal_probability"])
            runtimes.append(runtime)

        benchmark_results.append({
            "depth": p,
            "mean_probability": np.mean(probabilities),
            "std_probability": np.std(probabilities),
            "mean_runtime": np.mean(runtimes),
            "std_runtime": np.std(runtimes)
        })

    return benchmark_results


def save_results(results):
    output_dir = Path(__file__).resolve().parent.parent / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"depth_benchmark_{timestamp}.csv"

    output_path = output_dir / filename

    with open(output_path, "x", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to: {output_path}")


def plot_results(results):
    depths = [r["depth"] for r in results]

    mean_runtimes = [r["mean_runtime"] for r in results]
    std_runtimes = [r["std_runtime"] for r in results]

    mean_probabilities = [r["mean_probability"] for r in results]
    std_probabilities = [r["std_probability"] for r in results]

    # Runtime
    plt.figure()

    plt.errorbar(
        depths,
        mean_runtimes,
        yerr=std_runtimes,
        fmt="o-",
        capsize=4
    )

    plt.xlabel("QAOA Circuit Depth (p)")
    plt.ylabel("Runtime (seconds)")
    plt.title("QAOA Runtime vs Circuit Depth")
    plt.grid(True)
    plt.show()

    # Solution quality
    plt.figure()

    plt.errorbar(
        depths,
        mean_probabilities,
        yerr=std_probabilities,
        fmt="o-",
        capsize=4
    )

    plt.xlabel("QAOA Circuit Depth (p)")
    plt.ylabel("Optimal Solution Probability")
    plt.title("QAOA Solution Quality vs Circuit Depth")
    plt.ylim(0, 1.05)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    results = benchmark_depths()
    save_results(results)
    plot_results(results)



