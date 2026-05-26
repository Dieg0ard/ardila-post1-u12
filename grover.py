from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def grover_2qubits(target="11", shots=1024):
    """Grover para n=2 qubits buscando el estado target."""
    qc = QuantumCircuit(2, 2)
    
    # Paso 1: superposición uniforme
    qc.h([0, 1])
    
    # Paso 2: oráculo de fase marca el estado target
    # Para target "11": CZ (fase -1 solo en |11>)
    if target == "11":
        qc.cz(0, 1)
    elif target == "00":
        qc.x([0, 1])
        qc.cz(0, 1)
        qc.x([0, 1])
    elif target == "01":
        qc.x(0)
        qc.cz(0, 1)
        qc.x(0)
    elif target == "10":
        qc.x(1)
        qc.cz(0, 1)
        qc.x(1)
        
    # Paso 3: difusor (inversión alrededor de la media)
    qc.h([0, 1])
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])
    
    # Medición
    qc.measure([0, 1], [0, 1])
    
    sim = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()
    
    print(f"Grover buscando |{target}> ({shots} shots):")
    for state, count in sorted(counts.items()):
        pct = (count / shots) * 100
        print(f"  |{state}>: {count:4d} ({pct:.1f}%)")
        
    top = max(counts, key=counts.get)
    print(f"Estado más probable: |{top}> -> {'CORRECTO' if top == target else 'ERROR'}")
    
    # Guardar histograma
    fig = plot_histogram(counts)
    fig.savefig(f"capturas/grover_{target}.png", dpi=150)
    plt.close(fig)  # Cierra la figura para liberar memoria
    return counts

if __name__ == "__main__":
    for t in ["00", "01", "10", "11"]:
        grover_2qubits(target=t)
        print()