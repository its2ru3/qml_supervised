All TODO items are completed. Here's the final verification summary:

## Paper-Faithful Verification Checklist

| Paper Requirement | Implementation | Status |
|---|---|---|
| **Feature map** (eqn. 31): $\mathcal{U}_{\Phi(\mathbf{x})}$ with $\phi_S$ | `ZZFeatureMap(reps=d, entanglement='full')`; d=0 → trivial RZ | ✅ |
| **Ansatz** (eqn. 38-39): $R_Z + R_Y$ + CZ, depth $l=d$ | [build_paper_ansatz(num_layers=d)](cci:1://file:///d:/dev/Quantum/qml_project/helpers/circuits.py:29:0-58:13) — $(d{+}1)$ rotation layers, $d$ entanglers | ✅ |
| **Parity interpret** (eqn. 20-21): $f = Z_1 Z_2$ | [parity_interpret](cci:1://file:///d:/dev/Quantum/qml_project/helpers/circuits.py:64:0-81:80) returns 0/1 class indices; VQC uses `interpret=parity_interpret, output_shape=2` | ✅ |
| **Optimizer**: SPSA, 250 iterations | `SPSA(maxiter=250)` from `qiskit_machine_learning.optimizers` | ✅ |
| **Cost function**: sigmoid cost ≈ cross-entropy | VQC default cross-entropy; bias $b^*=0$ omitted | ✅ |
| **Label encoding**: ±1 → 0/1 | `(y+1)//2` conversion in all VQC cells | ✅ |
| **Shots**: 200 train, 2000 prob, 20000 classify, 50000 kernel | Config cell defines all four | ✅ |
| **Noise**: $\epsilon_1=0.001$, $\epsilon_2=0.0373$, $T_1=50\mu s$, $T_2=17\mu s$, readout 0.95 | [_build_paper_noise_model](cci:1://file:///d:/dev/Quantum/qml_project/helpers/noise.py:8:0-32:13) + [create_noisy_sampler](cci:1://file:///d:/dev/Quantum/qml_project/helpers/noise.py:35:0-52:14) | ✅ |
| **ZNE**: stretch [1.0, 1.5], Richardson | [zero_noise_extrapolation](cci:1://file:///d:/dev/Quantum/qml_project/helpers/noise.py:114:0-174:5) with Richardson extrapolation | ✅ |
| **Readout mitigation**: $A^{-1}\mathbf{c}$ | [apply_readout_mitigation](cci:1://file:///d:/dev/Quantum/qml_project/helpers/noise.py:55:0-111:27) inverts confusion matrix | ✅ |
| **No RealAmplitudes** | Import removed; all ansatz via [build_paper_ansatz](cci:1://file:///d:/dev/Quantum/qml_project/helpers/circuits.py:29:0-58:13) | ✅ |
| **No COBYLA** | Import removed; all VQC cells use SPSA | ✅ |
| **Paper equations in markdown** | Added to Part 1 intro, Part 2 intro/section, Part 4 intro, Part 5, Summary | ✅ |

### Changes Made

**`@d:\dev\Quantum\qml_project\helpers\circuits.py`**:
- [build_paper_ansatz](cci:1://file:///d:/dev/Quantum/qml_project/helpers/circuits.py:29:0-58:13): Fixed structure to match paper — $(l{+}1)$ local rotation layers with $l$ entanglers between them; `num_layers=0` now gives 1 rotation layer (4 params for 2 qubits)
- [parity_interpret](cci:1://file:///d:/dev/Quantum/qml_project/helpers/circuits.py:64:0-81:80): Changed from returning +1/−1 to returning 0/1 class indices, matching VQC's `interpret` contract

**`@d:\dev\Quantum\qml_project\main_v2.ipynb`** (10 cells edited):
- Removed `RealAmplitudes` and `COBYLA` imports
- All 4 VQC training cells: [build_paper_ansatz(reps=3)](cci:1://file:///d:/dev/Quantum/qml_project/helpers/circuits.py:29:0-58:13) → [build_paper_ansatz(num_layers=d)](cci:1://file:///d:/dev/Quantum/qml_project/helpers/circuits.py:29:0-58:13) + added `interpret=parity_interpret, output_shape=2`
- 2 error mitigation demo cells: fixed [build_paper_feature_map(d=2)](cci:1://file:///d:/dev/Quantum/qml_project/helpers/circuits.py:6:0-26:13) → `depth=2`, [build_paper_ansatz(reps=1)](cci:1://file:///d:/dev/Quantum/qml_project/helpers/circuits.py:29:0-58:13) → `num_layers=1`
- Updated all markdown cells with paper equation references (eqn. 14, 20-21, 31, 32, 38-39, 47, 48-49)
- Removed all stale COBYLA/RealAmplitudes references from plot labels and explanations