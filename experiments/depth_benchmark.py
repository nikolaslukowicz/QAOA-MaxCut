import time
import csv
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

from qaoa_maxcut.main import main


def benchmark_depths(depths=range(1, 11)):
    benchmark_results = []

    for p in depths:
        start = time.perf_counter()

        results = main(p, verbose=False, plot=False)

        runtime = time.perf_counter() - start

        benchmark_results.append({
            "depth": p,
            "runtime": runtime,
            "best_cut": results["best_cut"],
            "optimal_cut": results["optimal_cut"],
            "optimal_probability": results["optimal_probability"]
        })

        print(
            f"p={p:2d} | "
            f"Time={runtime:.2f}s | "
            f"Best cut={results['best_cut']} | "
            f"Optimal probability={results['optimal_probability']:.2%}"
        )

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
    runtimes = [r["runtime"] for r in results]
    probabilities = [r["optimal_probability"] for r in results]

    plt.figure()
    plt.plot(depths, runtimes, marker="o")
    plt.xlabel("QAOA Circuit Depth (p)")
    plt.ylabel("Runtime (seconds)")
    plt.title("QAOA Runtime vs Circuit Depth")
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot(depths, probabilities, marker="o")
    plt.xlabel("QAOA Circuit Depth (p)")
    plt.ylabel("Optimal Solution Probability")
    plt.title("QAOA Solution Quality vs Circuit Depth")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    results = benchmark_depths()
    save_results(results)
    plot_results(results)



