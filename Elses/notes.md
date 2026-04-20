command to convert ipynb to py file -- 'jupyter nbconvert --to script main.ipynb'

### Other methods to convert pdf to text --
Using marker-pdf --> converts pdf to markdown
> pip install marker-pdf 
> marker file.pdf

## Final Command to correct the code implementation 

# PROMPT 1: Project Restructuring & Cleanup

---

## Context

You are working on [d:\dev\Quantum\qml_project\main.ipynb](cci:7://file:///d:/dev/Quantum/qml_project/main.ipynb:0:0-0:0), a Jupyter notebook that implements the paper *"Supervised Learning with Quantum-Enhanced Feature Space"* (Havlicek *et al.*, Nature 567, 209–212, 2019). The notebook currently has ~81 cells with helper functions inlined, unnecessary exploratory sections, and an incorrect implementation of the VQC. Your job is to **restructure the project** — move helper functions into a separate package, remove sections not needed for paper reproduction, and prepare the notebook for the paper-faithful implementation that will follow in a second prompt.

**Do NOT modify `main_old_wrong_implementation.ipynb`** — it is for reference only.

---

## Task 1: Create the `helpers/` package

Create a directory `d:\dev\Quantum\qml_project\helpers\` with the following files:

### `helpers/__init__.py`
Export all public functions from the sub-modules so they can be imported as `from helpers import ...` or `from helpers.data import ...`.

### `helpers/data.py`
Move all data-loading functions here:
- `load_paper_csv(filepath)` — loads training CSV, returns `(X, y)` with `+1/-1` labels. **Keep** the `df.dropna(how="all")` fix.
- `load_paper_classification(filepath)` — loads classification results CSV, returns `(X, y_true, y_pred)`. **Keep** the `df.dropna(how="all")` fix.
- `DATA_DIR` constant (pointing to `./data/`).
- A new function `load_all_kernel_sets()` that loads all three kernel dataset splits (Sets I, II, III) and returns a dict keyed by set name, each containing `X_train`, `y_train`, `X_test`, `y_test`, `y_pred_paper`.
- A new function `load_all_variational_sets()` that loads all variational dataset splits. The variational data CSVs follow the naming pattern `Variational_Set_{I,II,III}_Depth_{0,1,2,3,4}_Training.csv` and `Variational_Set_{I,II,III}_Depth_{0,1,2,3,4}_Classifications_ResultsOnly.csv`. Return a nested dict keyed by `(set_name, depth)` containing `X_train`, `y_train`, `X_test`, `y_test`, `paper_accuracy`.

💡 **Explanation:** Moving data loading into a separate module keeps the notebook clean and makes the data pipeline reusable. The `load_all_*` functions encapsulate the loop logic currently inlined in the notebook cells.

### `helpers/visualization.py`
Move all visualization functions here, and add new ones:
- `plot_kernel_matrix(kernel_matrix, title)` — existing, unchanged.
- `plot_data(X, y, title)` — existing, unchanged.
- `plot_decision_boundary(classifier, X, y, title, grid_steps)` — existing, unchanged.
- **NEW** `plot_accuracy_vs_depth(depths, our_train_accs, our_test_accs, paper_accs, title)` — plots accuracy vs depth with three curves (our train, our test, paper test) plus a formatted table printed below. Include error bars (standard error of mean) when multiple splits are provided.
- **NEW** `plot_loss_convergence(loss_histories, depths, title)` — plots training loss curves for each depth on the same axes with a legend.
- **NEW** `plot_kernel_comparison(kernels_ideal, kernels_noisy, titles)` — side-by-side comparison of ideal vs noisy kernel matrices (to reproduce Fig. 4 from the paper).
- **NEW** `plot_classification_histogram(accuracies_per_set, depths, paper_accuracies)` — histogram of classification success rates across test sets for each depth, matching Fig. 3c from the paper. Each depth gets a density plot showing the distribution of test accuracies across the 20 test sets, with mean marked as a dot.
- **NEW** `plot_data_with_labels(X, y, support_vectors=None, title="")` — scatter plot of 2D data with optional support vector highlighting (green circles), matching Fig. 3b from the paper.

💡 **Explanation:** These new visualization functions are designed to reproduce specific figures from the paper. The histogram function reproduces the blue histograms in Fig. 3c. The kernel comparison reproduces Fig. 4. The support vector plot reproduces Fig. 3b.

### `helpers/circuits.py`
Move circuit-building functions here:
- `build_custom_rx_zz_circuit(num_qubits, depth)` — existing custom feature map (keep for reference but note it's not paper-faithful).
- **NEW** `build_paper_ansatz(num_qubits, num_layers)` — builds the paper's variational circuit $W(\boldsymbol{\theta})$ per eqn. (38) and (39) from the supplementary: alternating layers of $U_{\text{loc}}^{(t)}(\theta_t) = \otimes_{m=1}^n U(\theta_{m,t})$ with $U(\theta_{m,t}) = e^{i\frac{\theta^z_{m,t}}{2}Z_m} e^{i\frac{\theta^y_{m,t}}{2}Y_m}$, interleaved with CZ entanglers $U_{\text{ent}} = \prod_{(i,j) \in E} \text{CZ}(i,j)$. For 2 qubits with linear connectivity, CZ(0,1). Each layer has $2n$ parameters ($\theta^y$ and $\theta^z$ per qubit). Return a `QuantumCircuit` with `ParameterVector`.
- **NEW** `build_paper_feature_map(feature_dimension, depth)` — wraps `ZZFeatureMap(feature_dimension=feature_dimension, reps=depth, entanglement='full')` for $d \geq 1$. For $d=0$, create a trivial feature map with `ParameterVector("x", 2)` and `RZ` gates on each qubit (since $R_Z(\theta)|0\rangle$ is just a global phase, the state remains $|0\rangle$ — matching the paper's "no encoding" baseline).
- **NEW** `parity_interpret(bitstring)` — the paper's measurement interpretation function $f = Z_1 Z_2$. Maps bitstring to label: $f(z) = (-1)^{z_1 \oplus z_2}$, i.e., if the XOR of the two measured bits is 0, return +1; if 1, return -1. This is a callable to pass as VQC's `interpret` parameter.

💡 **Explanation:** The paper's ansatz uses both $R_Y$ and $R_Z$ rotations per qubit per layer (eqn. 39), unlike `RealAmplitudes` which only has $R_Y$. The parity interpret function implements the $f = Z_1 Z_2$ measurement from the paper, where the label is determined by whether the two measured qubit values agree (+1) or disagree (-1).

### `helpers/noise.py`
Create this new module for noise simulation and error mitigation:
- **NEW** `create_noisy_sampler(backend_name=None, shots=1024)` — creates a `qiskit_aer.AerSimulator` configured with a realistic noise model. If `backend_name` is provided, use `AerSimulator.from_backend()` to extract the noise model from a real IBM backend (via `qiskit_ibm_runtime`). If not, construct a custom noise model with parameters matching the paper's hardware: single-qubit gate error ~0.1%, CNOT error ~3.7%, T₁ ≈ 50 μs, T₂ ≈ 17 μs, readout error ~5%. Return an `AerSimulator` instance configured as a `BaseSamplerV2` compatible sampler.
- **NEW** `apply_readout_mitigation(sampler, qubits)` — creates a `LocalReadoutMitigator` using calibration circuits for the specified qubits. This implements the paper's readout correction (measurement matrix inversion, Supplementary Section VIII.B).
- **NEW** `zero_noise_extrapolation(circuit, observable, sampler, stretch_factors=[1, 1.5])` — implements Richardson extrapolation to first order (the paper's error mitigation technique, Supplementary Section IX). Runs the circuit at normal gate times and at 1.5× stretched gate times, then linearly extrapolates to zero noise. This matches the paper's statement: "a copy of the circuit was run on a timescale slowed down by a factor of 1.5."

💡 **Explanation:** The paper uses three error handling techniques: (1) zero-noise extrapolation (Richardson to first order with stretch factor 1.5), (2) readout correction (measurement matrix inversion), and (3) these are applied at each trial step during training. The noise model parameters are taken from the paper's Supplementary Section VIII.

### `helpers/metrics.py`
Create this new module:
- **NEW** `compute_paper_accuracy(y_true, y_pred)` — accuracy score, same as `sklearn.metrics.accuracy_score` but also returns the number of misclassified points.
- **NEW** `compare_with_paper(our_accuracy, paper_accuracy, set_name, depth=None)` — formatted comparison string.
- **NEW** `aggregate_results(results_dict, set_names, depths)` — aggregates per-(set,depth) results into mean ± std across splits.

💡 **Explanation:** These utility functions keep metric computation consistent and make result comparison easy.

---

## Task 2: Restructure [main.ipynb](cci:7://file:///d:/dev/Quantum/qml_project/main.ipynb:0:0-0:0)

Rewrite the notebook with the following structure. **Remove all sections that are not needed for paper reproduction.** Keep only what's essential.

### New notebook structure:

**Cell 0 — Title & Introduction** (markdown)
Keep the existing title cell but update it to say this is a **faithful reproduction** of the paper using noisy simulation with error mitigation.

**Cell 1 — Part 0: Setup & Imports** (markdown header)

**Cell 2 — Imports** (code)
```python
# Core packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import os

# Qiskit core
import qiskit
from qiskit.circuit import QuantumCircuit, Parameter, ParameterVector
from qiskit.circuit.library import ZZFeatureMap

# Qiskit Aer (noisy simulation)
import qiskit_aer
from qiskit_aer import AerSimulator

# Qiskit Machine Learning
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_machine_learning.algorithms import QSVC
from qiskit_machine_learning.algorithms.classifiers import VQC
from qiskit_machine_learning.state_fidelities import ComputeUncompute
from qiskit_machine_learning.optimizers import SPSA

# Qiskit IBM Runtime (for real backend noise models, optional)
# from qiskit_ibm_runtime import QiskitRuntimeService

# Helper modules
from helpers.data import (load_paper_csv, load_paper_classification, 
                          DATA_DIR, load_all_kernel_sets, load_all_variational_sets)
from helpers.visualization import (plot_kernel_matrix, plot_data, plot_decision_boundary,
                                    plot_accuracy_vs_depth, plot_loss_convergence,
                                    plot_kernel_comparison, plot_classification_histogram,
                                    plot_data_with_labels)
from helpers.circuits import (build_paper_feature_map, build_paper_ansatz, parity_interpret,
                               build_custom_rx_zz_circuit)
from helpers.noise import create_noisy_sampler, apply_readout_mitigation, zero_noise_extrapolation
from helpers.metrics import compute_paper_accuracy, compare_with_paper, aggregate_results

# Scikit-learn
from sklearn.metrics import accuracy_score

warnings.filterwarnings('ignore', category=DeprecationWarning)
print("All imports successful.")
```

💡 **Explanation:** Notice the key changes: (1) `RealAmplitudes`, `ZFeatureMap`, `PauliFeatureMap`, `EfficientSU2`, [COBYLA](cci:2://file:///d:/dev/Quantum/qml_project/venv_qml_project/Lib/site-packages/qiskit_algorithms/optimizers/cobyla.py:19:0-58:77) are removed — we no longer need them. (2) `StatevectorSampler` is removed — replaced by `AerSimulator`. (3) Optimizer is now `SPSA` from `qiskit_machine_learning.optimizers`. (4) All helper functions are imported from the `helpers` package.

**Cell 3 — Explanation** (markdown)
💡 **Explanation:** Brief overview of what changed from the previous version and why.

**Cell 4 — Configuration** (code)
```python
# Paper parameters (Section V of supplementary)
NUM_QUBITS = 2
DEPTHS = [0, 1, 2, 3, 4]
SET_NAMES = ["I", "II", "III"]

# Training parameters (from paper: Fig 3a caption and text)
SPSA_MAXITER = 250        # Paper: "250 iterations of Spall's SPSA algorithm"
TRAINING_SHOTS = 2000     # Paper: 2000 shots for p_y estimates during training
COST_FUNCTION_R = 200     # Paper: R=200 in the cost function (smoother landscape)
CLASSIFICATION_SHOTS = 20000  # Paper: 20,000 shots for classification

# Noise model parameters (from Supplementary Section VIII)
CNOT_ERROR_RATE = 0.0373  # Paper: CNOT error from RB
SINGLE_QUBIT_ERROR = 0.001  # Approximate from paper's RB data
READOUT_FIDELITY = 0.95   # Paper: ~95% readout assignment fidelity
T1_US = 50.0             # Paper: T1 ≈ 55/38 μs
T2_US = 17.0             # Paper: T2* ≈ 16/17 μs

# Error mitigation (Supplementary Section IX)
ZNE_STRETCH_FACTORS = [1.0, 1.5]  # Paper: normal + 1.5× stretched

print("Configuration set.")
```

💡 **Explanation:** All paper-specified parameters are centralized here so they're easy to find and modify. The paper explicitly states 250 SPSA iterations, 2000 training shots, R=200 for cost function, 20000 classification shots, and 1.5× stretch factor for ZNE.

**Cell 5 — Part 1: Paper's Feature Map** (markdown)
Brief explanation of the paper's feature map $\mathcal{U}_{\Phi(\mathbf{x})} = U_{\Phi(\mathbf{x})} H^{\otimes n} U_{\Phi(\mathbf{x})} H^{\otimes n}$ with $\phi_{\{i\}}=x_i$, $\phi_{\{1,2\}}=(\pi-x_1)(\pi-x_2)$.

**Cell 6 — Feature map visualization** (code)
Print the ZZFeatureMap circuit at d=2 to show the structure. Just one cell, no classification.

**Cell 7 — Part 2: Quantum Kernel Estimator** (markdown)

**Cell 8 — Load paper datasets** (code)
```python
kernel_sets = load_all_kernel_sets()
for name, data in kernel_sets.items():
    print(f"Set {name}: train={data['X_train'].shape[0]}, test={data['X_test'].shape[0]}, "
          f"paper_acc={accuracy_score(data['y_test'], data['y_pred_paper']):.4f}")
```

**Cell 9 — Kernel estimation: noiseless** (code)
Run FidelityQuantumKernel + QSVC with `StatevectorSampler` (as a baseline) on all three sets. Store results. Plot kernel matrices.

**Cell 10 — Kernel estimation: noisy + mitigation** (code)
Run the same with `AerSimulator` using the paper's noise model + readout correction. Compare ideal vs noisy kernel matrices using `plot_kernel_comparison`. This reproduces Fig. 4 from the paper.

**Cell 11 — Kernel results comparison** (code)
Table + bar chart comparing noiseless, noisy, noisy+mitigated, and paper's reported accuracy.

**Cell 12 — Part 3: Quantum Variational Classifier** (markdown)

**Cell 13 — Paper's ansatz and measurement** (markdown)
Explain the paper's ansatz structure (eqn. 38-39), the parity measurement $f=Z_1 Z_2$, and the sigmoid cost function (eqn. 47).

**Cell 14 — Ansatz visualization** (code)
Print the paper's ansatz circuit at l=1 and l=4 to show the structure.

**Cell 15 — VQC Training: Depth Sweep (Set I)** (code)
The main training loop. Use `build_paper_feature_map(d)`, `build_paper_ansatz(num_qubits=2, num_layers=d)`, `SPSA(maxiter=SPSA_MAXITER)`, `parity_interpret` as the interpret function, noisy sampler with mitigation. Track loss history via callback. Print results per depth.

**Cell 16 — Loss convergence plot** (code)
Use `plot_loss_convergence`.

**Cell 17 — Accuracy vs depth** (code)
Use `plot_accuracy_vs_depth`. Include noiseless baseline, noisy+mitigated, and paper's results.

**Cell 18 — VQC Training: All Splits** (code)
Train across all 3 sets × 5 depths. Store in `all_vqc_results`.

**Cell 19 — Aggregated results** (code)
Use `aggregate_results` and `plot_accuracy_vs_depth` with error bars. Print comparison table.

**Cell 20 — Classification histograms** (code)
Use `plot_classification_histogram` to reproduce Fig. 3c from the paper.

**Cell 21 — Decision boundaries** (code)
Side-by-side decision boundaries at d=0,2,4 for Set I.

**Cell 22 — Part 4: Summary & Discussion** (markdown)
Discussion of results, comparison with paper, what matches and what doesn't, limitations.

---

## Task 3: Remove these sections entirely

The following sections from the current notebook are **not needed** for paper reproduction and should be removed:

- **Section 1.0** (synthetic data via `ad_hoc_data`) — the paper uses its own datasets, not synthetic
- **Section 1.1** (ZFeatureMap exploration) — the paper only uses ZZFeatureMap
- **Section 1.3** (custom data maps — product, sin) — not in the paper
- **Section 1.4** (PauliFeatureMap) — not in the paper
- **Section 1.5** (third-order expansion on 3D data) — not in the paper
- **Section 1.6** (custom RX+ZZ feature map) — not in the paper
- **Section 1.7** (feature map comparison summary) — not needed without the above
- **The `build_qsvc` helper** — replaced by direct calls in the kernel section
- **The `product_data_map_func` and `sin_data_map_func`** — not in the paper
- **Version check cell** — unnecessary

---

## Task 4: Add `helpers/` to Python path

In the imports cell, add `sys.path` manipulation if needed so that `from helpers import ...` works when the notebook's working directory is `d:\dev\Quantum\qml_project\`.

---

## Verification

After completing all tasks:
1. Confirm `helpers/` directory exists with all 6 files ([__init__.py](cci:7://file:///d:/dev/Quantum/qml_project/venv_qml_project/Lib/site-packages/qiskit_machine_learning/optimizers/__init__.py:0:0-0:0), `data.py`, `visualization.py`, `circuits.py`, `noise.py`, `metrics.py`)
2. Confirm [main.ipynb](cci:7://file:///d:/dev/Quantum/qml_project/main.ipynb:0:0-0:0) has no inline helper functions (all moved to `helpers/`)
3. Confirm all removed sections are gone
4. Confirm the notebook structure matches the new outline above
5. **Do NOT run the notebook** — just verify the structure is correct

---

# PROMPT 2: Paper-Faithful Implementation

---

## Context

You are continuing work on [d:\dev\Quantum\qml_project\main.ipynb](cci:7://file:///d:/dev/Quantum/qml_project/main.ipynb:0:0-0:0). Helper functions are now in `helpers/`, unnecessary sections have been removed, and the notebook skeleton is ready. Your job is to **implement the paper-faithful quantum circuits, noise simulation, error mitigation, and training loops** so that our results closely match the paper's.

The paper is: *"Supervised Learning with Quantum-Enhanced Feature Space"* (Havlicek *et al.*, Nature 567, 209–212, 2019). The main paper is in [d:\dev\Quantum\qml_project\AI_readable_paper\paper_main\](cci:9://file:///d:/dev/Quantum/qml_project/AI_readable_paper/paper_main:0:0-0:0) and the supplementary is in [d:\dev\Quantum\qml_project\AI_readable_paper\paper_sup\](cci:9://file:///d:/dev/Quantum/qml_project/AI_readable_paper/paper_sup:0:0-0:0). Read them if you need clarification on any implementation detail.

**Do NOT modify `main_old_wrong_implementation.ipynb`**.

---

## Critical Implementation Details

These are the exact specifications from the paper that MUST be followed. The previous implementation had several mismatches — this is your checklist to fix them all:

### 1. Feature Map (Paper: eqn. 31, Supplementary Section IV.A)

$$\mathcal{U}_{\Phi(\mathbf{x})} = U_{\Phi(\mathbf{x})} H^{\otimes n} U_{\Phi(\mathbf{x})} H^{\otimes n}$$

with $\phi_{\{i\}}(\mathbf{x}) = x_i$ and $\phi_{\{1,2\}}(\mathbf{x}) = (\pi - x_1)(\pi - x_2)$.

**Implementation**: `ZZFeatureMap(feature_dimension=2, reps=d, entanglement='full')` for $d \geq 1$. This is correct — the default data map matches the paper's $\phi_S$.

For $d=0$: Create a `QuantumCircuit(2)` with `ParameterVector("x", 2)` and `RZ(x[i], i)` on each qubit. Since $R_Z(\theta)|0\rangle = e^{-i\theta/2}|0\rangle$ (global phase only), the encoded state remains $|0\rangle$ — matching the paper's "no encoding" baseline while still providing 2 input parameters so VQC doesn't reject the data.

### 2. Ansatz / Variational Circuit (Paper: eqn. 38-39, Supplementary Section V)

The paper's ansatz is:
$$W(\boldsymbol{\theta}) = U_{\text{loc}}^{(l)}(\theta_l) \; U_{\text{ent}} \; \cdots \; U_{\text{loc}}^{(2)}(\theta_2) \; U_{\text{ent}} \; U_{\text{loc}}^{(1)}(\theta_1)$$

where each local unitary is:
$$U(\theta_{m,t}) = e^{i\frac{\theta^z_{m,t}}{2}Z_m} \; e^{i\frac{\theta^y_{m,t}}{2}Y_m}$$

and the entangler is:
$$U_{\text{ent}} = \text{CZ}(0, 1)$$

**This is NOT `RealAmplitudes`.** The paper uses both $R_Y$ and $R_Z$ rotations per qubit per layer, with CZ (not CNOT) entanglers. Each layer has $2n = 4$ trainable parameters (2 per qubit: $\theta^y$ and $\theta^z$).

**Implementation in `helpers/circuits.py`**:
```python
def build_paper_ansatz(num_qubits, num_layers):
    theta = ParameterVector("θ", num_qubits * num_layers * 2)  # 2 params per qubit per layer
    qc = QuantumCircuit(num_qubits)
    param_idx = 0
    for layer in range(num_layers):
        # Local rotations: RZ then RY on each qubit
        for q in range(num_qubits):
            qc.rz(theta[param_idx], q)
            param_idx += 1
            qc.ry(theta[param_idx], q)
            param_idx += 1
        # Entangler: CZ between adjacent qubits (for 2 qubits, just CZ(0,1))
        if num_qubits > 1:
            for i in range(num_qubits - 1):
                qc.cz(i, i + 1)
    return qc
```

Note: The paper says "depth $l$" for the ansatz (number of entangler layers). At $l=0$, there's still one layer of local rotations (no entangler). At $l=4$, there are 4 entangler layers with 5 local rotation layers. However, the paper's Fig. 2b shows that the ansatz depth $l$ corresponds to the number of repeated entangler+local blocks. Follow the paper's convention: `num_layers` = the number of entangler layers, with local rotations before and after each entangler.

💡 **Explanation:** The paper's ansatz is fundamentally different from `RealAmplitudes`. `RealAmplitudes` uses only $R_Y$ gates and CNOTs, giving $n$ parameters per layer. The paper's ansatz uses $R_Z$ followed by $R_Y$ on each qubit, with CZ entanglers, giving $2n$ parameters per layer. This doubles the expressivity per layer. CZ gates are also different from CNOTs — CZ applies a phase flip when both qubits are |1⟩, while CNOT flips the target conditioned on the control. On hardware, CZ is more natural for certain topologies.

### 3. Optimizer (Paper: page 2, column 2)

The paper explicitly states: *"We have found that Spall's simultaneous perturbation stochastic approximation (SPSA) algorithm performs well in the noisy experimental setting."*

**Implementation**: Use `SPSA` from `qiskit_machine_learning.optimizers` (NOT from `qiskit_algorithms` — the VQC callback only works with `qiskit_machine_learning` optimizers due to an `isinstance` check in [trainable_model.py](cci:7://file:///d:/dev/Quantum/qml_project/venv_qml_project/Lib/site-packages/qiskit_machine_learning/algorithms/trainable_model.py:0:0-0:0)).

```python
from qiskit_machine_learning.optimizers import SPSA
optimizer = SPSA(maxiter=250)
```

Note: SPSA is a stochastic optimizer that perturbs all parameters simultaneously to estimate the gradient. It requires twice the function evaluations per iteration (one for each perturbation direction). With `maxiter=250`, expect ~500 objective function evaluations.

💡 **Explanation:** SPSA is specifically designed for noisy optimization landscapes. Unlike COBYLA (which builds a local linear model), SPSA uses random perturbations to estimate the gradient direction, which helps escape local minima. The paper chose SPSA because quantum circuit evaluations are inherently noisy (shot noise + hardware noise). Even in our noisy simulation, SPSA should outperform COBYLA.

### 4. Measurement / Interpret Function (Paper: eqn. 20-21, Section V)

The paper uses **parity measurement** $f = Z_1 Z_2$:
- Measure both qubits in the Z-basis
- Map bitstring $z \in \{0,1\}^2$ to label via $f(z) = (-1)^{z_1 \oplus z_2}$
- If the XOR of the two bits is 0 → label +1; if 1 → label -1

**Implementation**:
```python
def parity_interpret(bitstring):
    """Paper's f = Z1*Z2 measurement. Maps bitstring to +1 or -1."""
    # bitstring is an integer representing the measured outcome
    # For 2 qubits: 0=|00⟩, 1=|01⟩, 2=|10⟩, 3=|11⟩
    bit1 = (bitstring >> 1) & 1  # qubit 0 (MSB)
    bit2 = bitstring & 1          # qubit 1 (LSB)
    xor = bit1 ^ bit2
    return 1 if xor == 0 else -1  # +1 if parity even, -1 if odd
```

Then pass to VQC as: [VQC(..., interpret=parity_interpret, output_shape=2)](cci:2://file:///c:/Users/isams/AppData/Local/Programs/Python/Python314/Lib/site-packages/qiskit_machine_learning/algorithms/classifiers/vqc.py:29:0-199:21)

💡 **Explanation:** The VQC's `interpret` parameter maps measured bitstrings to class labels. The default (no interpret) uses one-hot encoding where each bitstring is its own class. The paper's parity function groups bitstrings into just 2 classes: even parity (|00⟩, |11⟩ → +1) and odd parity (|01⟩, |10⟩ → -1). This is a much more restrictive measurement that forces the classifier to learn a separating hyperplane based on parity. The `output_shape=2` tells VQC there are 2 possible output labels.

### 5. Cost Function (Paper: eqn. 47, Supplementary Section VI.A)

The paper uses a **sigmoid-based empirical risk**:
$$R_{\text{emp}}(\boldsymbol{\theta}) = \sum_{j=1}^t \text{sig}\left(\sqrt{R}\frac{\frac{1-y_jb}{2} - \hat{p}_{y_j}(\mathbf{x}_j)}{\sqrt{2(1-\hat{p}_{y_j}(\mathbf{x}_j))\hat{p}_{y_j}(\mathbf{x}_j)}}\right)$$

with $R=200$ for the cost function (smoother landscape) and 2000 shots for the actual $\hat{p}_y$ estimates.

**Implementation challenge**: VQC's built-in loss is `cross_entropy`. The paper's cost function is different. There are two approaches:
- **Option A (recommended)**: Use VQC with `loss="cross_entropy"` as an approximation. The cross-entropy loss has similar properties to the paper's sigmoid cost (both focus on points near the decision boundary). This is the pragmatic choice since implementing a custom loss for VQC requires subclassing.
- **Option B (faithful)**: Implement the paper's cost function manually by bypassing VQC and using `SamplerQNN` directly. This is more complex but more faithful.

Go with **Option A** for now, but add a markdown cell explaining the difference and noting that the paper's sigmoid cost focuses more on points near the decision boundary (see Fig. 4b in the supplementary).

💡 **Explanation:** The paper's cost function is derived from the binomial CDF approximation of the misclassification probability. It has the property that the gradient contribution is largest for points near the decision boundary (Fig. 4c), similar to how SVMs maximize the margin. Cross-entropy loss has a similar but not identical profile. The difference is minor for our purposes — the bigger factors affecting accuracy are the ansatz, optimizer, and interpret function.

### 6. Shots (Paper: multiple references)

- **Training**: 2000 shots per data point for $\hat{p}_y$ estimates, but $R=200$ in the cost function
- **Classification**: 20,000 shots per data point
- **Kernel estimation**: 50,000 shots per matrix entry

**Implementation**: When using `AerSimulator`, set `shots=2000` for training and `shots=20000` for classification. For kernel estimation, use `shots=50000`. Note that `StatevectorSampler` doesn't use shots (exact amplitudes), so these parameters only apply to the noisy simulation.

### 7. Bias Parameter (Paper: Section II.A)

The paper optimizes a bias $b \in [-1, 1]$ alongside the circuit parameters $\boldsymbol{\theta}$. They found $b^* = 0$ in their experiments.

**Implementation**: VQC doesn't have a separate bias parameter. This is fine — the paper found $b^* = 0$ anyway, so omitting it doesn't affect results. Add a markdown note explaining this.

### 8. Depth Convention (Paper: Fig. 2b, Section V)

The paper's "depth $d$" for the feature map refers to the number of repetitions of $U_{\Phi(\mathbf{x})} H^{\otimes n}$. The variational ansatz $W(\boldsymbol{\theta})$ has its own depth $l$ (number of entangler layers).

In the paper's experiment, they sweep the **feature map depth** $d \in \{0,1,2,3,4\}$ while keeping the **ansatz depth** fixed at $l$ (the paper doesn't explicitly state the ansatz depth, but from Fig. 2b it appears to be $l=d$ or a fixed small value). From the paper's text: "We implement the quantum variational classifier $W(\boldsymbol{\theta})$ for five different depths ($l=0$ to $l=4$)" — this suggests the ansatz depth varies alongside the feature map depth.

**Implementation**: Use `build_paper_ansatz(num_qubits=2, num_layers=d)` so the ansatz depth matches the feature map depth, as the paper's wording suggests.

### 9. Error Mitigation (Paper: Supplementary Section IX)

The paper uses **zero-noise extrapolation to first order** (Richardson extrapolation with stretch factors 1.0 and 1.5). Implementation:
- Run each circuit at normal gate times → get noisy expectation $\langle O \rangle_{c1}$
- Run the same circuit with all gate times stretched by 1.5× → get noisier expectation $\langle O \rangle_{c1.5}$
- Extrapolate: $\langle O \rangle_{\text{ZNE}} = 3\langle O \rangle_{c1} - 2\langle O \rangle_{c1.5}$ (linear extrapolation to zero noise)

Plus **readout correction** (Supplementary Section VIII.B): measure a $4 \times 4$ calibration matrix $A_{ij} = P(\text{measure } |i\rangle | \text{prepare } |j\rangle)$ and correct observed probabilities by multiplying with $A^{-1}$.

**Implementation in `helpers/noise.py`**: 
- For ZNE: Use `qiskit_aer` with pulse-level stretching or gate-level stretching (insert identity gates to stretch). The simpler approach is to use `AerSimulator` with different `noise_model` configurations (scale T₁/T₂ by the stretch factor).
- For readout correction: Use `qiskit.result.LocalReadoutMitigator` which implements exactly this.

💡 **Explanation:** Zero-noise extrapolation works because gate errors scale roughly linearly with gate duration. By running at two different noise levels and extrapolating, we can estimate what the result would be with zero noise. The factor 1.5 is specifically chosen by the paper because it's large enough to see a noise difference but small enough that the circuit still works. The readout correction matrix accounts for the fact that measuring |0⟩ sometimes gives |1⟩ and vice versa (≈5% error rate).

---

## Implementation Steps

### Step 1: Implement `helpers/circuits.py` fully

Make sure `build_paper_ansatz` and `build_paper_feature_map` and `parity_interpret` are correctly implemented per the specifications above. Test by printing the circuits.

### Step 2: Implement `helpers/noise.py` fully

Implement `create_noisy_sampler`, `apply_readout_mitigation`, and `zero_noise_extrapolation`. The noisy sampler should:
1. Create an `AerSimulator` with a `NoiseModel` that includes:
   - `depolarizing_error` on single-qubit gates with probability ~0.001
   - `depolarizing_error` on CNOT/CZ gates with probability ~0.037
   - `thermal_relaxation_error` with T₁=50μs, T₂=17μs on each qubit
   - `ReadoutError` with ~5% misassignment probability
2. Be usable as a `BaseSamplerV2`-compatible sampler for VQC and FidelityQuantumKernel

### Step 3: Implement the kernel estimation section (Cells 9-11)

For the **noiseless baseline** (Cell 9):
```python
from qiskit.primitives import StatevectorSampler
sampler_ideal = StatevectorSampler()
fidelity_ideal = ComputeUncompute(sampler=sampler_ideal)
qk_ideal = FidelityQuantumKernel(feature_map=ZZFeatureMap(2, reps=2, entanglement='full'), 
                                  fidelity=fidelity_ideal)
```

For the **noisy + mitigated** version (Cell 10):
```python
sampler_noisy = create_noisy_sampler(shots=50000)  # 50K shots per paper
# Apply readout mitigation
mitigator = apply_readout_mitigation(sampler_noisy, qubits=[0, 1])
fidelity_noisy = ComputeUncompute(sampler=sampler_noisy)
qk_noisy = FidelityQuantumKernel(feature_map=ZZFeatureMap(2, reps=2, entanglement='full'),
                                  fidelity=fidelity_noisy)
```

Compute kernel matrices with both, compare side-by-side, and show the maximum deviation $|K - \hat{K}|$ (matching Fig. 4 from the paper).

### Step 4: Implement the VQC training section (Cells 15-21)

The critical training loop (Cell 15):
```python
sampler_noisy = create_noisy_sampler(shots=TRAINING_SHOTS)
mitigator = apply_readout_mitigation(sampler_noisy, qubits=[0, 1])

vqc_results = {}
for d in DEPTHS:
    data = variational_data[("I", d)]
    X_train, y_train = data["X_train"], data["y_train"]
    X_test, y_test = data["X_test"], data["y_test"]
    
    # Convert labels: paper uses +1/-1, VQC needs 0/1
    y_train_01 = (y_train + 1) // 2
    y_test_01 = (y_test + 1) // 2
    
    # Paper-faithful circuits
    feature_map = build_paper_feature_map(feature_dimension=2, depth=d)
    ansatz = build_paper_ansatz(num_qubits=2, num_layers=d)
    
    # Paper-faithful optimizer
    optimizer = SPSA(maxiter=SPSA_MAXITER)
    
    # Callback for loss tracking
    loss_history = []
    def callback(weights, loss):
        loss_history.append(loss)
    
    # Build VQC with parity interpret
    vqc = VQC(
        feature_map=feature_map,
        ansatz=ansatz,
        optimizer=optimizer,
        sampler=sampler_noisy,
        callback=callback,
        interpret=parity_interpret,
        output_shape=2,
    )
    
    vqc.fit(X_train, y_train_01)
    
    train_acc = vqc.score(X_train, y_train_01)
    test_acc = vqc.score(X_test, y_test_01)
    
    vqc_results[d] = {
        "vqc": vqc,
        "train_accuracy": train_acc,
        "test_accuracy": test_acc,
        "paper_accuracy": data["paper_accuracy"],
        "loss_history": loss_history.copy(),
    }
    
    print(f"  d={d}: train={train_acc:.4f}, test={test_acc:.4f}, "
          f"paper={data['paper_accuracy']:.4f}, final_loss={loss_history[-1]:.4f}")
```

### Step 5: Add all visualizations

Implement all the plotting cells using the helper functions from `helpers/visualization.py`. Make sure:
- Loss convergence plots show all depths on one figure
- Accuracy vs depth plots include our results (train + test), paper results, and optionally a noiseless baseline
- Classification histograms match Fig. 3c from the paper
- Kernel comparison matches Fig. 4 from the paper
- Decision boundaries are shown for selected depths

### Step 6: Add 💡 **Explanation:** markdown cells

After every code cell, add a markdown cell with `💡 **Explanation:**` that explains in plain language:
- What the code does
- Why it's implemented this way (referencing specific paper equations/sections)
- What the expected output should look like
- Any deviations from the paper and why

---

## Important Notes

1. **VQC callback compatibility**: You MUST use `SPSA` from `qiskit_machine_learning.optimizers`, NOT from `qiskit_algorithms.optimizers`. The VQC's internal [trainable_model.py](cci:7://file:///d:/dev/Quantum/qml_project/venv_qml_project/Lib/site-packages/qiskit_machine_learning/algorithms/trainable_model.py:0:0-0:0) checks `isinstance(self._optimizer, SciPyOptimizer)` using `qiskit_machine_learning`'s class. Using the wrong package's optimizer causes the callback to never fire, resulting in empty `loss_history`.

2. **AerSimulator as BaseSamplerV2**: Make sure the `AerSimulator` you create is compatible with VQC's `sampler` parameter (which expects `BaseSamplerV2`). Use `AerSimulator()` with appropriate options and wrap it if needed.

3. **Label encoding**: The paper uses labels $\{+1, -1\}$. VQC expects $\{0, 1\}$. Always convert with `(y + 1) // 2` before passing to VQC.

4. **Don't expect exact match**: Even with paper-faithful implementation, our results may differ from the paper because: (a) we use a different cost function (cross-entropy vs sigmoid), (b) SPSA is stochastic so results vary between runs, (c) the paper ran on real hardware with specific calibration states. Our noiseless simulation should achieve *higher* accuracy than the paper's hardware results. Our noisy simulation should achieve *similar* accuracy to the paper's mitigated results.

5. **Do NOT run the full notebook** to test. Just verify the code is syntactically correct and logically consistent. The user will test it themselves.

---

## Verification Checklist

Before finishing, verify:
- [ ] `helpers/circuits.py`: `build_paper_ansatz` uses $R_Z + R_Y$ per qubit with CZ entanglers (NOT `RealAmplitudes`)
- [ ] `helpers/circuits.py`: `parity_interpret` maps bitstrings to +1/-1 based on XOR parity
- [ ] `helpers/circuits.py`: `build_paper_feature_map` handles $d=0$ with trivial RZ circuit
- [ ] `helpers/noise.py`: noise model parameters match paper's Supplementary Section VIII
- [ ] `helpers/noise.py`: ZNE uses stretch factors [1.0, 1.5] per paper
- [ ] `helpers/noise.py`: readout correction implements measurement matrix inversion
- [ ] [main.ipynb](cci:7://file:///d:/dev/Quantum/qml_project/main.ipynb:0:0-0:0): imports SPSA from `qiskit_machine_learning.optimizers` (NOT `qiskit_algorithms`)
- [ ] [main.ipynb](cci:7://file:///d:/dev/Quantum/qml_project/main.ipynb:0:0-0:0): VQC uses `interpret=parity_interpret, output_shape=2`
- [ ] [main.ipynb](cci:7://file:///d:/dev/Quantum/qml_project/main.ipynb:0:0-0:0): VQC uses `build_paper_ansatz` (NOT `RealAmplitudes`)
- [ ] [main.ipynb](cci:7://file:///d:/dev/Quantum/qml_project/main.ipynb:0:0-0:0): training uses 250 SPSA iterations per paper
- [ ] [main.ipynb](cci:7://file:///d:/dev/Quantum/qml_project/main.ipynb:0:0-0:0): noisy simulation uses AerSimulator with paper's noise parameters
- [ ] [main.ipynb](cci:7://file:///d:/dev/Quantum/qml_project/main.ipynb:0:0-0:0): all 💡 **Explanation:** cells are present
- [ ] [main.ipynb](cci:7://file:///d:/dev/Quantum/qml_project/main.ipynb:0:0-0:0): no references to removed sections (synthetic data, ZFeatureMap exploration, etc.)
- [ ] `main_old_wrong_implementation.ipynb` is untouched