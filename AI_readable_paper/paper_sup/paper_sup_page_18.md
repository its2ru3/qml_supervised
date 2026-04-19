| Qubit label | $Q_0$ (83 ns) ($\times 10^{-3}$) | $Q_1$ (83 ns) ($\times 10^{-3}$) | $Q_0$ (125 ns) ($\times 10^{-3}$) | $Q_1$ (125 ns) ($\times 10^{-3}$) |
|---|---|---|---|---|
| 01 | - | $0.715 \pm 0.005$ | - | $1.244 \pm 0.010$ |
| 10 | $1.319 \pm 0.017$ | - | $1.410 \pm 0.010$ | - |
| 11 | $1.367 \pm 0.011$ | $0.763 \pm 0.005$ | $1.484 \pm 0.014$ | $1.271 \pm 0.010$ |

TABLE I. RB of our single-qubit gates. Qubit labels indicate which qubit was benchmarked on each case, with label 11 indicating simultaneous RB.

Our two-qubit unitaries are CNOTs constructed from echo cross-resonance sequences [24, 25]. Each of the two cross-resonance pulses in a CNOT has durations of $333$ and $500 \text{ ns}$ for the two different gate lengths used in our experiments. For our two-qubit RB we obtain a CNOT error of $0.0373 \pm .0015$ ($0.0636 \pm .0021$) for the $333$ ($500$) $\text{ns}$ cross-resonance pulse.

#### **B. Readout correction**

Our readout assigned fidelity was $\sim 95\%$ for both qubits.

For each experiment, we run $4 \; (2^2)$ calibration sequences preparing our two qubits in their joint computational states. We gather statistics of these calibrations and create a measurement matrix $A_{ij} = P(|i\rangle ||j\rangle)$ where $P(|n\rangle ||m\rangle)$ is the probability of measuring state $|m\rangle$ having prepared state $|n\rangle$. We then correct the observed outcomes of our experiments by inverting this matrix and multiplying our output probability distributions by this inverse.

#### **IX. ERROR MITIGATION AND ADDITIONAL EXPERIMENTAL RESULTS**

The experimental estimation of the kernel matrices shown in Fig. 9 and in Fig. 4 in the main text involves running the experiments at different gate lengths and extrapolating the expectation value of the observable of interest to its zero-noise value. The technique [21, 22] is extremely powerful in coping with incoherent errors, at the cost of increased sampling and without requiring any additional quantum resources. However, the experimental readout assignment fidelities also determine how precisely an expectation value can be estimated.

Even though for our Sets I and II we attain $100 \; \%$ classification success over $10$ randomly drawn test sets in each case, we can quantify how close our experimentally determined separating hyperplane is to the ideal.

The optimal hyperplane for a given training set can be expressed as the linear combination $\sum_i \alpha_i y_i \Phi(\boldsymbol{x}_i) = \mathbf{w}$ (eqn. 13), where $\mathbf{w}$ is a vector orthogonal to the optimal separating hyperplane and $\Phi(\boldsymbol{x}_i)$ are the support vectors. We can therefore quantify the distance between the experimentally obtained hyperplane and the ideal hyperplane by calculating the inner product $\langle\mathbf{w}, \mathbf{w}_{\text{ideal}}\rangle = \sum_{i \in N_S} \sum_{j \in N_S'} y_i y_j \alpha_i^* \alpha_j | \langle \boldsymbol{x}_i \boldsymbol{x}_j \rangle |^2 / ||\mathbf{w}|| ||\mathbf{w}_{\text{ideal}}||$ where $N_S$ and $N_S'$ are the sets of experimentally obtained and ideal support vectors, respectively.

In Fig. 6 we show the inner products between the ideal and all experimental hyperplanes, including the two sets of gate times used throughout our experiments, $c1$ and $c1.5$, as well as the error-mitigated hyperplanes.

For Sets I and II, which classify at $100 \; \%$ success, it is clear that error mitigation improves our results very significantly. This is not the case for Set III, which classifies at $94.75 \; \%$ success. In fact, for Set III we see that error-mitigation worsens the hyperplane, as the results are closer to the ideal for the unmitigated experiments than both Sets I and II.

A look at the calibration data taken along the direct kernel estimation experiments for each set, we see that the readout assignment fidelities of $Q_0$($Q_1$) are $96.56\%$ ($96.31\%$) for Set I, $95.90\%$ ($96.36\%$) for Set II, and $93.99\%$ ($95.47\%$) for Set III. The slightly worse readout fidelities for Set III could partially explain the worse classification results for this set. However, one can not discount other experimental imperfections such as finite sampling effects and gate tune - up errors.
