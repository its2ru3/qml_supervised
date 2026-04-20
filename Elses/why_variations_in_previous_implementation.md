# Question 
You have read both the papers, right? did they specify the number of iterations and other circuit and algorithm features in the text? what things are we assuming and what things are we taking using calcualted guess? why is there so much of difference in test accuracy in paper and ours? like even when i tried maxiter=1000, it gives 82% accuracy only while paper has 98% accuracy. we are using same systems for testing the algorithms, right? or did they use actual quantum hardware for it? 
the paper given at link https://doi.org/10.1038/s41586-019-0980-2 is the stored in the directory ./AI_readable_paper/paper_main with images of all it's figures and the suplementary paper is stored in ./AI_readable_paper/paper_sup with it's all figures. 

# Answer 

## Did they use actual quantum hardware?

**Yes.** The paper ran experiments on a **5-qubit superconducting quantum processor** (IBM), using only qubits Q₀ and Q₁. This is real hardware with T₁ ≈ 55/38 μs, CNOT error ≈ 3.7%, and readout fidelity ≈ 95%. They also used **error mitigation** (zero-noise extrapolation to first order) and **readout correction** (measurement matrix inversion).

We use `StatevectorSampler` — a **perfect, noiseless simulator**. So our simulation should actually be *better* than their hardware results, not worse. The accuracy gap is in the opposite direction from what hardware noise would cause.

---

## What the paper specifies vs. what we assume

| Component | Paper specifies | Our implementation | Match? |
|---|---|---|---|
| **Feature map** | $\mathcal{U}_{\Phi(\boldsymbol{x})} H^{\otimes n} U_{\Phi(\boldsymbol{x})} H^{\otimes n}$ with $\phi_{\{i\}}=x_i$, $\phi_{\{1,2\}}=(\pi-x_1)(\pi-x_2)$ | `ZZFeatureMap(feature_dimension=2, reps=d)` | ✅ Match (reps=2 = d=2 in paper notation) |
| **Ansatz** | $U_{\text{loc}}^{(l)} U_{\text{ent}} \cdots U_{\text{loc}}^{(1)}$ with $U(\theta)=e^{i\frac{\theta^z}{2}Z}e^{i\frac{\theta^y}{2}Y}$ and CZ entanglers | `RealAmplitudes(num_qubits=2, reps=1)` | ❌ **Mismatch** — see below |
| **Optimizer** | **SPSA** (Spall's simultaneous perturbation stochastic approximation) | COBYLA | ❌ **Mismatch** |
| **Cost function** | Sigmoid-based empirical risk (eqn. 47): $\text{sig}\left(\sqrt{R}\frac{\frac{1-yb}{2}-\hat{p}_y}{\sqrt{2(1-\hat{p}_y)\hat{p}_y}}\right)$ | Cross-entropy (VQC default) | ❌ **Mismatch** |
| **Shots (training)** | R=200 for cost function, 2000 shots for $\hat{p}_y$ estimates | None (statevector = infinite shots) | ⚠️ Different regime |
| **Shots (classification)** | 20,000 shots per data point | None (statevector) | ⚠️ Different regime |
| **Iterations** | **250 SPSA iterations** (Fig. 3a caption) | 200 COBYLA iterations | ❌ Different count + different optimizer |
| **Bias parameter** | $b \in [-1,1]$ optimized (though $b^*=0$ found) | Not explicitly set | ⚠️ Minor |
| **Interpret function** | Parity $f = Z_1 Z_2$ (measures both qubits, XOR of outcomes) | VQC default (one-hot encoding) | ❌ **Major mismatch** |
| **Depth d=0** | No feature map, just ansatz on $|0\rangle$ | Our RZ workaround | ⚠️ Approximate |

---

## The 3 critical mismatches causing the accuracy gap

### 1. **Ansatz structure** (biggest issue)

The paper uses **$Y$ and $Z$ rotations** per layer (eqn. 39):
$$U(\theta_{m,t}) = e^{i\frac{\theta^z_{m,t}}{2}Z_m} e^{i\frac{\theta^y_{m,t}}{2}Y_m}$$

with **CZ entanglers** between layers. Each layer has $2n$ parameters (both $Y$ and $Z$ rotations per qubit).

Our `RealAmplitudes(reps=1)` uses **only $R_Y$ rotations** + CNOT entanglers. No $R_Z$ rotations in the ansatz. This means our ansatz has **half the expressivity** per layer compared to the paper's.

### 2. **Optimizer: SPSA vs COBYLA**

The paper explicitly states (page 2, col 2): *"We have found that Spall's simultaneous perturbation stochastic approximation (SPSA) algorithm performs well in the noisy experimental setting."*

SPSA is a **stochastic gradient estimator** that perturbs all parameters simultaneously — it's specifically designed for noisy/no-gradient settings and tends to escape local minima better than COBYLA. COBYLA is deterministic and can get stuck in local minima for non-convex landscapes.

### 3. **Measurement/interpret function**

The paper uses **parity measurement** $f = Z_1 Z_2$: measure both qubits in Z-basis, then map bitstring to label via $f(z) = (-1)^{z_1 \oplus z_2}$. This is a **binary** interpret function.

VQC by default uses **one-hot encoding** — it outputs a 2-dimensional probability vector (one probability per class) and uses cross-entropy loss. This is a fundamentally different measurement scheme.

---

## What we should fix (in priority order)

1. **Use SPSA optimizer** instead of COBYLA — already imported, just needs `SPSA(maxiter=250)` or similar
2. **Fix the ansatz** to match the paper's $R_Y + R_Z$ structure with CZ entanglers
3. **Set the interpret function** to parity ($f = Z_1 Z_2$) in VQC
4. **Increase iterations** to 250 to match paper

Would you like me to implement these fixes? I'd need to switch to Code mode to edit the notebook cells.