In this paper, the feature map is a classical to quantum mapping by a tunable quantum circuit family, that maps $\Phi : \mathbb{R}^d \rightarrow \mathcal{S}(\mathcal{H}_2^{\otimes n})$ in to the state space (space of density matrices) of $n$ qubits with $\dim\left(\mathcal{S}(\mathcal{H}_2^{\otimes n})\right) = 4^n$. The example of the Gaussian kernel indicates, that the sheer dimension of the Hilbert space available on a quantum computer by itself does not provide an advantage, since even classically infinite dimensional spaces are available (e.g. the Gaussian kernel). However, this procedure provides a path towards a quantum advantage as we may construct states in feature space with classically hard-to-estimate overlaps.

#### **B. Variational circuit classifiers**

Let us now turn to the case of binary classification based on variational quantum circuits. Recall that in our setting, we first take the data $\boldsymbol{x} \in \mathbb{R}^d$ and map it to a quantum state $|\Phi(\boldsymbol{x})\rangle \langle \Phi(\boldsymbol{x})| \in \mathcal{S}(\mathcal{H}_2^{\otimes n})$ on $n$-qubits, c.f. eqn. (27). Then we apply a variational circuit $W(\boldsymbol{\theta})$ to the initial state that depends on some variational parameters $\boldsymbol{\theta}$, c.f. eqn. (38). Lastly, for a binary classification task, we measure the resulting state in the canonical Z-basis and assign the resulting bit-string $z \in \{0, 1\}^n$ to a label based on a predetermined boolean function $f : \{0, 1\}^n \rightarrow \{+1, -1\}$. Hence the probability of measuring either label $y \in \{+1, -1\}$ is given by:

$$p_y = \frac{1}{2} \left( 1 + y \langle \Phi(\boldsymbol{x}) | W^\dagger(\boldsymbol{\theta}) \, \mathbf{f} \, W(\boldsymbol{\theta}) | \Phi(\boldsymbol{x}) \rangle \right), \qquad (20)$$

where we have defined the diagonal operator

$$\mathbf{f} = \sum_{z \in \{0,1\}^n} f(z) |z\rangle\langle z| . \qquad (21)$$

In classification tasks we assign c.f. eqn. (41), the label with the highest empirical weight of the distribution $p_y$. We ask whether the outcome $+1$ is more likely than $-1$, or vice versa. That is, we ask, whether $p_{+1} > p_{-1} - b$ or whether the converse is true. This of course depends on the sign of the expectation value $\langle \Phi(\boldsymbol{x}) | W^\dagger(\boldsymbol{\theta}) \, \mathbf{f} \, W(\boldsymbol{\theta}) | \Phi(\boldsymbol{x}) \rangle$ for the data point $\boldsymbol{x}$.

To understand how this relates to the SVM in greater detail, we need to choose an orthonormal operator basis, such as for example the Pauli group

$$\mathcal{P}_n = \langle X_i, Y_i, Z_i \rangle_{i=1, \dots, n}. \qquad (22)$$

Note that when fixing the phase to $+1$ every element $P_\beta \in \mathcal{P}_n$, with $\beta = 1, \dots, 4^n$ of the Pauli-group is an orthogonal reflection $P_\beta^2 = \mathbb{1}$. Furthermore, Pauli matrices are mutually orthogonal in terms of the trace inner product

$$\text{tr}\left[ P_\alpha P_\beta \right] = \delta_{\alpha, \beta} 2^n . \qquad (23)$$

This means that both the measurement operator $\mathbf{w} = W^\dagger(\boldsymbol{\theta}) \, \mathbf{f} \, W(\boldsymbol{\theta})$ in the $W$-rotated frame as well as the state $\Phi(\boldsymbol{x}) = |\Phi(\boldsymbol{x})\rangle \langle \Phi(\boldsymbol{x})|$ can be expanded in terms of the operator basis with only real coefficients as

$$\mathbf{w} = \frac{1}{2^n} \sum_\beta w_\beta(\boldsymbol{\theta}) P_\beta \quad \text{with} \quad w_\beta(\boldsymbol{\theta}) = \text{tr}\left[ W^\dagger(\boldsymbol{\theta}) \, \mathbf{f} \, W(\boldsymbol{\theta}) P_\beta \right]$$
$$\Phi(\boldsymbol{x}) = \frac{1}{2^n} \sum_\beta \Phi_\beta(\boldsymbol{x}) P_\beta \quad \text{with} \quad \Phi_\beta(\boldsymbol{x}) = \text{tr}\left[ |\Phi(\boldsymbol{x})\rangle \langle \Phi(\boldsymbol{x})| P_\beta \right] . \qquad (24)$$

Note, that the values $w_\beta(\boldsymbol{\theta})$ as well as $\Phi_\beta(\boldsymbol{x})$ are constrained due to the fact that they originate from a rotated projector and from a pure state. Since $\mathbf{f}^2 = \mathbb{1}$, we have that $\text{tr}\left[ \left( W^\dagger(\boldsymbol{\theta}) \, \mathbf{f} \, W(\boldsymbol{\theta}) \right)^2 \right] = 2^n$. Furthermore, the projector squares to itself so that $\text{tr}\left[ |\Phi(\boldsymbol{x})\rangle \langle \Phi(\boldsymbol{x})|^2 \right] = 1$. In particular, this means that the norms of both vectors satisfy $\sum_\beta \Phi_\beta^2(\boldsymbol{x}) = 2^n$ as well as $\sum_\beta w_\beta^2(\boldsymbol{\theta}) = 4^n$.

Since the expectation value of the measured observable is $\langle \Phi(\boldsymbol{x}) | W^\dagger(\boldsymbol{\theta}) \mathbf{f} W(\boldsymbol{\theta}) | \Phi(\boldsymbol{x}) \rangle = \text{tr}\left[ \mathbf{w} \, \Phi(\boldsymbol{x}) \right]$, we can express this Hilbert-Schmidt inner-product explicitly in the Pauli basis:

$$\langle \Phi(\boldsymbol{x}) | W^\dagger(\boldsymbol{\theta}) \, \mathbf{f} \, W(\boldsymbol{\theta}) | \Phi(\boldsymbol{x}) \rangle = \frac{1}{2^n} \sum_\beta w_\beta(\boldsymbol{\theta}) \Phi_\beta(\boldsymbol{x}) . \qquad (25)$$
