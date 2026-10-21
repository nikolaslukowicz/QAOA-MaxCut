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