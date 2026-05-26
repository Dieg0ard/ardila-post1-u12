from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def oracle_constante(n):
    """Oráculo constante f(x)=0: no hace nada."""
    return QuantumCircuit(n + 1)  # ancilla qubit incluido

def oracle_balanceada(n):
    """Oráculo balanceado: aplica CNOT del qubit i al ancilla."""
    qc = QuantumCircuit(n + 1)
    for i in range(n):
        qc.cx(i, n)  # CNOT qubit_i -> ancilla
    return qc

def deutsch_jozsa(oracle_qc, n, shots=1024):
    """Ejecuta el algoritmo Deutsch-Jozsa con el oráculo dado."""
    qc = QuantumCircuit(n + 1, n)
    
    # Inicializar ancilla en |-> = H|1>
    qc.x(n)
    qc.h(range(n + 1))  # H en todos los qubits
    
    # Aplicar oráculo
    qc.compose(oracle_qc, inplace=True)
    
    # Interferencia: H en qubits de entrada
    qc.h(range(n))
    
    # Medir solo los qubits de entrada (no el ancilla)
    qc.measure(range(n), range(n))
    
    sim = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()
    return counts

if __name__ == "__main__":
    n = 2
    
    # Oráculo constante: todos los resultados deben ser "00"
    counts_c = deutsch_jozsa(oracle_constante(n), n)
    print(f"Constante: {counts_c}")  # esperado: {"00": 1024}
    
    # Oráculo balanceado: ningún resultado debe ser "00"
    counts_b = deutsch_jozsa(oracle_balanceada(n), n)
    print(f"Balanceada: {counts_b}")  # esperado: sin "00"
    
    assert "00" in counts_c, "Error: oráculo constante no retornó 00"
    assert "00" not in counts_b, "Error: oráculo balanceado retornó 00"
    print("OK: Deutsch-Jozsa verifica correctamente")