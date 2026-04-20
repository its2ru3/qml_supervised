"""Circuit building utilities for the VQC paper reproduction project."""

from qiskit.circuit import QuantumCircuit, ParameterVector
from qiskit.circuit.library import ZZFeatureMap


def build_paper_feature_map(depth, feature_dimension=2):
    """Build the paper's feature map circuit.

    For d >= 1: ZZFeatureMap(feature_dimension=feature_dimension, reps=depth, entanglement='full')
    This matches the paper's U_Phi(x) = U_Phi(x) H^n U_Phi(x) H^n with
    phi_{i}=x_i, phi_{1,2}=(pi-x_1)(pi-x_2).

    For d=0: A trivial feature map with ParameterVector("x", 2) and RZ gates.
    Since R_Z(theta)|0> is just a global phase, the encoded state remains |0>,
    matching the paper's "no encoding" baseline while providing 2 input parameters.
    """
    if depth == 0:
        x = ParameterVector("x", feature_dimension)
        fm = QuantumCircuit(feature_dimension)
        for i in range(feature_dimension):
            fm.rz(x[i], i)
    else:
        fm = ZZFeatureMap(
            feature_dimension=feature_dimension, reps=depth, entanglement="full"
        )
    return fm


def build_paper_ansatz(num_layers, num_qubits=2):
    """Build the paper's variational circuit W(theta) per eqn. (38)-(39) from the supplementary.

    The paper's convention: depth l = number of entangler layers.
    - l=0: 1 local rotation layer, 0 entanglers → 2n parameters
    - l=1: 2 local rotation layers, 1 entangler → 4n parameters
    - l=k: (k+1) local rotation layers, k entanglers → (k+1)*2n parameters

    Structure: U_loc^(l) U_ent ... U_loc^(2) U_ent U_loc^(1)
    Each local unitary: U(theta_{m,t}) = RZ(theta^z_{m,t}) RY(theta^y_{m,t})
    Entangler: CZ(i, i+1) for adjacent qubits (linear connectivity).

    Note: This is NOT RealAmplitudes. The paper uses both RY and RZ rotations
    per qubit per layer, with CZ (not CNOT) entanglers.
    """
    n_params = (num_layers + 1) * num_qubits * 2
    theta = ParameterVector("θ", n_params)
    qc = QuantumCircuit(num_qubits)
    param_idx = 0

    for layer in range(num_layers + 1):
        # Local rotations: RZ then RY on each qubit
        for q in range(num_qubits):
            qc.rz(theta[param_idx], q)
            param_idx += 1
            qc.ry(theta[param_idx], q)
            param_idx += 1
        # Entangler: CZ between adjacent qubits (after all but the last local layer)
        if num_qubits > 1 and layer < num_layers:
            for i in range(num_qubits - 1):
                qc.cz(i, i + 1)

    return qc


def parity_interpret(bitstring):
    """Paper's f = Z1*Z2 measurement interpretation function (eqn. 20-21).

    Maps bitstring to class index for VQC's interpret parameter.
    The paper's parity measurement groups outcomes by even/odd parity:
      Even parity (|00⟩, |11⟩) → class +1 → index 0
      Odd parity  (|01⟩, |10⟩) → class -1 → index 1

    This matches the label convention where (y+1)//2 converts +1→0, -1→1.
    Must be used with output_shape=2 in VQC.

    bitstring: integer representing the measured outcome.
    For 2 qubits: 0=|00⟩, 1=|01⟩, 2=|10⟩, 3=|11⟩.
    """
    bit1 = (bitstring >> 1) & 1  # qubit 0 (MSB)
    bit2 = bitstring & 1          # qubit 1 (LSB)
    xor = bit1 ^ bit2
    return 0 if xor == 0 else 1  # even parity → 0 (+1), odd parity → 1 (-1)


def build_custom_rx_zz_circuit(num_qubits, depth=2):
    """Build a custom feature map circuit with RX + ZZ layers.
    NOTE: This is not paper-faithful, kept for reference only.
    Returns a QuantumCircuit with ParameterVector for data binding."""
    x = ParameterVector("x", num_qubits)
    qc = QuantumCircuit(num_qubits)

    for _ in range(depth):
        # Layer 1: RX rotations encoding each feature
        for i in range(num_qubits):
            qc.rx(x[i], i)

        # Layer 2: ZZ entangling blocks for each pair
        for i in range(num_qubits):
            for j in range(i + 1, num_qubits):
                qc.cx(i, j)
                qc.rz(x[i] * x[j], j)
                qc.cx(i, j)

    return qc
