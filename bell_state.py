from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def bell_state_experiment(shots=1024):
    """Prepara el estado de Bell |\u03a6+> y mide."""
    # 2 qubits, 2 bits clásicos
    qc = QuantumCircuit(2, 2)
    
    # Paso 1: Hadamard en qubit 0 (crea superposición)
    qc.h(0)
    
    # Paso 2: CNOT (control=0, target=1) para entrelazamiento
    qc.cx(0, 1)
    
    # Paso 3: medir ambos qubits
    qc.measure([0, 1], [0, 1])
    
    # Simular con AerSimulator
    simulator = AerSimulator()
    job = simulator.run(qc, shots=shots)
    counts = job.result().get_counts()
    
    print(f"Resultados Bell |+> ({shots} shots):")
    for state, count in sorted(counts.items()):
        pct = (count / shots) * 100
        print(f"  |{state}> : {count:4d} ({pct:.1f}%)")
        
    # Verificar: solo deben aparecer |00> y |11>
    assert "01" not in counts and "10" not in counts, \
        "ERROR: aparecieron estados no entrelazados"
    print("OK: correlación perfecta verificada")
    
    # Guardar histograma
    fig = plot_histogram(counts)
    fig.savefig("capturas/bell_histogram.png", dpi=150)
    
    print(f"\nDiagrama del circuito:\n{qc.draw()}")
    return counts

if __name__ == "__main__":
    bell_state_experiment()