component $x_i$ of $\boldsymbol{x} \in [0, 1]^n$ so that $n$ qubits are used. The resulting state that is prepared is

$$\bigotimes_{i=1}^n |\phi_i(\boldsymbol{x})\rangle\langle\phi_i(\boldsymbol{x})| = \frac{1}{2^n} \bigotimes_{j=1}^n \left( \sum_{\alpha_j} \Phi_j^{\alpha_j}(\theta_j(\boldsymbol{x})) P_{\alpha_j} \right), \qquad (30)$$

when expanded in terms of the Pauli-matrix basis where $\Phi_i^\alpha(\theta_i(\boldsymbol{x})) = \langle\phi_i(\boldsymbol{x}) | P_{\alpha_i} | \phi_i(\boldsymbol{x})\rangle$ for all $i = 1, \dots n$. and $P_{\alpha_i} \in \{1, X_i, Z_i, Y_i\}$. The corresponding decision function can be constructed as in eqn. (19), with the kernel $K(\boldsymbol{x}, \boldsymbol{y}) = \prod_{i=1}^n |\langle\phi_i(\boldsymbol{x})|\phi_i(\boldsymbol{y})\rangle|^2$. These can be evaluated with resources scaling linearly in the number of qubits, so that no quantum advantage can be expected in this setting.

#### **A. Non-trivial feature map with entanglement**

There are many choices of feature maps, that do not suffer from the malaise of the aforementioned product state feature maps. To obtain a quantum advantage we would like these maps to give rise to a kernel $K(\boldsymbol{x}, \boldsymbol{y}) = |\langle\Phi(\boldsymbol{x})|\Phi(\boldsymbol{y})\rangle|^2$ that is computationally hard to estimate up to an additive polynomially small error by classical means. Otherwise, the map is immediately amenable to classical analysis and we are guaranteed to have lost any conceivable quantum advantage.

Let us therefore turn to a family of feature maps, c.f. Fig 2 for which we conjecture that it is hard to estimate the overlap $|\langle\Phi(\boldsymbol{x})|\Phi(\boldsymbol{y})\rangle|^2$ on a classical computer. We define the family of feature map circuit as follows

$$|\Phi(\boldsymbol{x})\rangle = U_{\Phi(\boldsymbol{x})} H^{\otimes n} U_{\Phi(\boldsymbol{x})} H^{\otimes n} |0\rangle^{\otimes n} \quad \text{where,} \quad U_{\Phi(\boldsymbol{x})} = \exp\left( i \sum_{S \subseteq [n]} \phi_S(\boldsymbol{x}) \prod_{i \in S} Z_i \right). \qquad (31)$$

where the $2^n$ possible coefficients $\phi_S(\boldsymbol{x}) \in \mathbb{R}$ are now non-linear functions of the input data $\boldsymbol{x} \in \mathbb{R}^n$. It is convenient to use maps with low-degree expansions, i.e. $|S| \le d$. Any such map can be efficiently implemented. In the experiments reported in this paper we have restricted to $d = 2$. So we only consider Ising type interactions in the unitaries $U_{\Phi(\boldsymbol{x})}$. It is convenient choose these interactions as the ones that are present in the actual connectivity graph of the superconducting chip $G = (E, V)$. This ensures that the feature map can be generated from a short depth circuit. The resulting unitary can then be generated from one- and two- qubit gates of the form

$$U_{\phi_{\{l,m\}}(\boldsymbol{x})} = \exp\left( i \phi_{\{l,m\}}(\boldsymbol{x}) Z_k Z_l \right) \quad \text{and} \quad U_{\phi_{\{k\}}(\boldsymbol{x})} = \exp\left( i \phi_{\{k\}}(\boldsymbol{x}) Z_k \right), \qquad (32)$$

which leaves $|V| + |E|$, real parameters to encode the data. In particular, we know that we have at least $|V| = n$ real numbers to encode the data. Furthermore, depending on the connectivity of all possible interactions, we have $|E| \le n(n-1)/2$ further parameters that can be used to encode more data or nonlinear relations of the initial data points.

This feature map encodes both the actual function $\Phi_{\boldsymbol{x}}(z)$ of the diagonal phases, as well as the corresponding Fourier-Walsh transform $\hat{\Phi}_{\boldsymbol{x}}(p)$ at $z, p \in \{0,1\}^n$

$$\Phi_{\boldsymbol{x}}(z) = \exp\left( i \sum_{S \subseteq [n]} \phi_S(\boldsymbol{x}) \prod_{i \in S} (-1)^{z_i} \right) \quad \text{and} \quad \hat{\Phi}_{\boldsymbol{x}}(p) = \frac{1}{2^n} \sum_{z \in \{0,1\}^n} \Phi_{\boldsymbol{x}}(z) (-1)^{p \circ z}, \qquad (33)$$

for every basis element respectively. The resulting state, after the datum $\boldsymbol{x} \in \mathbb{R}^d$ has been mapped to the feature space, is given by

$$|\Phi(\boldsymbol{x})\rangle = \sum_{p \in \{0,1\}^N} \Phi_{\boldsymbol{x}}(p) \hat{\Phi}_{\boldsymbol{x}}(p) |p\rangle. \qquad (34)$$

We conjecture that it is hard to estimate this kernel up to an additive polynomially small error by classical means. The intuition for the conjecture stems from a connection of the feature map to a particular circuit family for the hidden shift problem for boolean functions [6]. The feature map is similar to a quantum algorithm introduced by Rötteler for estimating the hidden shift in boolean bent functions, c.f. Ref. [7], algorithm $\mathcal{A}_1$ in Theorem 6. The circuit $\mathcal{U}_\Phi$ we consider is indeed very similar to the one discussed in [7]. Let us make a minor modification, and ask the
