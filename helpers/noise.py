"""Noise simulation and error mitigation utilities."""

import numpy as np
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error, ReadoutError


def _build_paper_noise_model(single_qubit_error=0.001, cnot_error=0.0373,
                              t1_us=50.0, t2_us=17.0, readout_fidelity=0.95):
    """Build a noise model matching the paper's ibmq device (Supp. Section VIII)."""
    nm = NoiseModel()
    t1s = t1_us * 1e-6
    t2s = t2_us * 1e-6
    gate_time = 50e-9   # single-qubit gate time
    cnot_time = 300e-9  # CNOT gate time

    # Single-qubit errors: depolarizing + thermal relaxation
    e1 = depolarizing_error(single_qubit_error, 1).compose(
        thermal_relaxation_error(t1s, t2s, gate_time))
    nm.add_all_qubit_quantum_error(e1, ["rz", "sx", "x", "h", "ry", "rx", "p", "u"])

    # Two-qubit errors: depolarizing + thermal relaxation on both qubits
    e2 = depolarizing_error(cnot_error, 2).compose(
        thermal_relaxation_error(t1s, t2s, cnot_time).tensor(
            thermal_relaxation_error(t1s, t2s, cnot_time)))
    nm.add_all_qubit_quantum_error(e2, ["cx", "cz", "ecr"])

    # Readout error
    p = 1.0 - readout_fidelity
    nm.add_all_qubit_readout_error(ReadoutError([[1 - p, p], [p, 1 - p]]))

    return nm


def create_noisy_sampler(cnot_error=0.0373, single_qubit_error=0.001,
                          readout_fidelity=0.95, t1_us=50.0, t2_us=17.0,
                          shots=1024, **kwargs):
    """Create an AerSimulator with a noise model matching the paper's ibmq device.

    Returns an AerSimulator instance configured with the paper's noise parameters.
    This can be used as a sampler for VQC training.
    """
    noise_model = _build_paper_noise_model(
        single_qubit_error=single_qubit_error,
        cnot_error=cnot_error,
        t1_us=t1_us,
        t2_us=t2_us,
        readout_fidelity=readout_fidelity,
    )
    sim = AerSimulator(noise_model=noise_model)
    sim.set_options(shots=shots)
    return sim


def apply_readout_mitigation(counts, readout_fidelity=0.95, num_qubits=2):
    """Apply readout error mitigation by inverting the assignment matrix.

    Given raw measurement counts and the readout fidelity per qubit,
    construct the confusion matrix A and apply A^{-1} to the counts
    to correct for readout errors (Supp. Section VIII.B).

    Args:
        counts: dict mapping bitstring (str) -> count (int)
        readout_fidelity: probability of correct readout per qubit
        num_qubits: number of qubits

    Returns:
        dict mapping bitstring -> mitigated count (float)
    """
    p = 1.0 - readout_fidelity  # flip probability per qubit

    # Build full confusion matrix for num_qubits
    # For 2 qubits: A[i,j] = P(measure=i | true=j)
    n_outcomes = 2 ** num_qubits
    A = np.ones((n_outcomes, n_outcomes))

    for i in range(n_outcomes):
        for j in range(n_outcomes):
            prob = 1.0
            for q in range(num_qubits):
                bit_i = (i >> (num_qubits - 1 - q)) & 1
                bit_j = (j >> (num_qubits - 1 - q)) & 1
                if bit_i == bit_j:
                    prob *= (1 - p)
                else:
                    prob *= p
            A[i, j] = prob

    # Convert counts to vector
    raw_vec = np.zeros(n_outcomes)
    total = sum(counts.values())
    for bitstring, count in counts.items():
        idx = int(bitstring, 2) if isinstance(bitstring, str) else bitstring
        raw_vec[idx] = count

    # Apply inverse: mitigated = A^{-1} @ raw
    try:
        A_inv = np.linalg.inv(A)
        mitigated_vec = A_inv @ raw_vec
        # Clip negatives to zero (can happen due to inversion)
        mitigated_vec = np.maximum(mitigated_vec, 0)
    except np.linalg.LinAlgError:
        mitigated_vec = raw_vec

    # Convert back to dict
    mitigated_counts = {}
    for i in range(n_outcomes):
        bitstring = format(i, f'0{num_qubits}b')
        mitigated_counts[bitstring] = mitigated_vec[i]

    return mitigated_counts


def zero_noise_extrapolation(circuit, noise_model, stretch_factors=None, shots=20000):
    """Zero-Noise Extrapolation using Richardson extrapolation (Supp. Section IX).

    Runs the circuit at amplified noise levels (by scaling T1/T2 down) and
    extrapolates to the zero-noise limit.

    Args:
        circuit: QuantumCircuit with measurements
        noise_model: base NoiseModel (not used directly; we rebuild from params)
        stretch_factors: list of noise amplification factors (default [1.0, 1.5])
        shots: number of shots per run

    Returns:
        dict with 'raw_counts' (list of count dicts) and 'extrapolated_counts' (dict)
    """
    if stretch_factors is None:
        stretch_factors = [1.0, 1.5]

    raw_counts_list = []
    for lam in stretch_factors:
        # Amplify noise by reducing T1/T2 by stretch factor
        sim = AerSimulator(noise_model=_build_paper_noise_model(
            t1_us=50.0 / lam, t2_us=17.0 / lam))
        sim.set_options(shots=shots)

        transpiled = transpile(circuit, sim)
        result = sim.run(transpiled).result()
        counts = result.get_counts()
        raw_counts_list.append(counts)

    # Richardson extrapolation (first order for 2 points)
    if len(stretch_factors) == 2:
        c1, c2 = stretch_factors
        all_states = set()
        for counts in raw_counts_list:
            all_states.update(counts.keys())

        extrapolated = {}
        for state in all_states:
            v1 = raw_counts_list[0].get(state, 0)
            v2 = raw_counts_list[1].get(state, 0)
            # Richardson: f(0) = (c2*v1 - c1*v2) / (c2 - c1)
            if c2 != c1:
                extrapolated[state] = (c2 * v1 - c1 * v2) / (c2 - c1)
            else:
                extrapolated[state] = v1
    else:
        # Higher-order: polynomial fit
        all_states = set()
        for counts in raw_counts_list:
            all_states.update(counts.keys())
        extrapolated = {}
        cs = np.array(stretch_factors)
        for state in all_states:
            vs = np.array([counts.get(state, 0) for counts in raw_counts_list])
            extrapolated[state] = np.polyval(np.polyfit(cs, vs, len(cs) - 1), 0)

    return {
        "raw_counts": raw_counts_list,
        "extrapolated_counts": extrapolated,
    }
