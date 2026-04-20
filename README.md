# Reproducing Havlíček et al. (2019)

Faithful reproduction of **"Supervised learning with quantum-enhanced feature spaces"** — Nature 567, 209–212 (2019). Implements both classification strategies (Quantum Kernel Estimation & Variational Classifier) on a noisy simulator with error mitigation.

## Quick Start

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
jupyter notebook main.ipynb
```

Run all cells top-to-bottom. Expect ~30–60 min total (VQC training is the bottleneck).

## Project Structure

```
qml_project/
├── main.ipynb              # Main notebook — run this
├── requirements.txt        # Python dependencies
├── data/                   # Paper's datasets (CSV)
├── helpers/
│   ├── circuits.py         # Feature map, ansatz, parity interpret
│   ├── data.py             # Dataset loading
│   ├── noise.py            # Noise model, readout mitigation, ZNE
│   ├── visualization.py    # All plots
│   └── metrics.py          # Accuracy, comparison, aggregation
└── DETAILS.md              # Implementation details & method comparison
```

## Results

### Kernel Estimator (d=2, noise-free)

| Set | Our Accuracy | Paper Accuracy |
|-----|-------------|----------------|
| I   | _—_         | 1.0000         |
| II  | _—_         | 1.0000         |
| III | _—_         | 0.9475         |

### Variational Classifier (SPSA, 250 iter)

| Depth d | Our Test (noise-free) | Our Test (noisy) | Paper (hardware) |
|---------|----------------------|-------------------|------------------|
| 0       | _—_                  | _—_               | ~0.50            |
| 1       | _—_                  | _—_               | ~0.70            |
| 2       | _—_                  | _—_               | ~0.99            |
| 3       | _—_                  | _—_               | ~0.99            |
| 4       | _—_                  | _—_               | ~0.99            |

> Fill in _—_ after running the notebook.

### Comparison Figure

> **Placeholder:** Insert the "Accuracy vs. Depth" plot from cell 5.4 here — it shows noise-free VQC, noisy VQC (SPSA), and paper's hardware results on the same axes. This is the key result figure matching the paper's Fig. 3a.

## Differences from the Paper

| Aspect | Paper | This Project | Why |
|--------|-------|-------------|-----|
| Hardware | ibmq device | AerSimulator with noise model | No quantum hardware access; simulator matches paper's device specs |
| Cost function | Sigmoid empirical risk (eqn. 47) | Cross-entropy (VQC default) | Custom loss requires bypassing VQC; cross-entropy has similar gradient profile |
| Bias parameter | Optimized $b \in [-1,1]$ | Omitted | Paper found $b^*=0$ anyway |
| Error mitigation | Applied per training step | Demonstrated separately on test circuits | VQC doesn't expose per-step mitigation hooks |
| Shot noise | Present on hardware | Configurable via AerSimulator `shots` | Simulator allows both exact and shot-noisy evaluation |

## Reference

Havlíček, V., Córcoles, A.D., Temme, K. *et al.* Supervised learning with quantum-enhanced feature spaces. **Nature** 567, 209–212 (2019). [DOI: 10.1038/s41586-019-0980-2](https://doi.org/10.1038/s41586-019-0980-2)
