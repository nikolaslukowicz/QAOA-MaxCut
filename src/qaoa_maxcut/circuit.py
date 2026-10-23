from qiskit import QuantumCircuit

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

