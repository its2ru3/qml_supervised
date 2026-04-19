---
**Algorithm 1** Quantum variational classification: the training phase
---
1: **Input** Labeled training samples $T = \{\boldsymbol{x} \in \Omega \subset \mathbb{R}^n\} \times \{y \in C\}$, Optimization routine,
2: **Parameters** Number of measurement shots $R$, and initial parameter $\boldsymbol{\theta}_0$.
3: Calibrate the quantum hardware to generate short depth trial circuits.
4: Set initial values of the variational parameters $\boldsymbol{\theta} = \boldsymbol{\theta}_0$ for the short-depth circuit $W(\boldsymbol{\theta})$
5: **while** Optimization (e.g. SPSA) of $R_{\text{emp}}(\boldsymbol{\theta})$ has not converged **do**
6: &nbsp;&nbsp;&nbsp;&nbsp;**for** $i = 1$ **to** $|T|$ **do**
7: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Set the counter $r_y = 0$ for every $y \in C$.
8: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**for** $shot = 1$ **to** $R$ **do**
9: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use $\mathcal{U}_{\Phi(\boldsymbol{x}_i)}$ to prepare initial feature-map state $|\Phi(\boldsymbol{x}_i)\rangle \langle\Phi(\boldsymbol{x}_i)|$
10: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Apply discriminator circuit $W(\boldsymbol{\theta})$ to the initial feature-map state .
11: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Apply $|C|$ - outcome measurement $\{M_y\}_{y \in C}$
12: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Record measurement outcome label $y$ by setting $r_y \rightarrow r_y + 1$
13: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**end for**
14: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Construct empirical distribution $\hat{p}_y(\boldsymbol{x}_i) = r_y R^{-1}$.
15: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Evaluate $\text{Pr}(\tilde{m}(\boldsymbol{x}_i) \neq y_i | m(\boldsymbol{x}) = y_i)$ with $\hat{p}_y(\boldsymbol{x}_i)$ and $y_i$
16: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Add contribution $\text{Pr}(\tilde{m}(\boldsymbol{x}_i) \neq y_i | m(\boldsymbol{x}) = y_i)$ to cost function $R_{\text{emp}}(\boldsymbol{\theta})$.
17: &nbsp;&nbsp;&nbsp;&nbsp;**end for**
18: &nbsp;&nbsp;&nbsp;&nbsp;Use optimization routine to propose new $\boldsymbol{\theta}$ with information from $R_{\text{emp}}(\boldsymbol{\theta})$
19: **end while**
20: **return** the final parameter $\boldsymbol{\theta}^*$ and value of the cost function $R_{\text{emp}}(\boldsymbol{\theta}^*)$
---

The classification can be applied when the training phase is complete. The optimal parameters are used to decide the correct label for new input data. Again, the same circuit Fig 1 is applied, however, this time the parameters are fixed and and the outcomes are combined to determine the label which is reported as output of the classifier.

---
**Algorithm 2** Quantum variational classification: the classification phase
---
1: **Input** An unlabeled sample from the test set $\boldsymbol{s} \in S$, optimal parameters $\boldsymbol{\theta}^*$ for the discriminator circuit.
2: **Parameters** Number of measurement shots $R$
3: Calibrate the quantum hardware to generate short depth trial circuits.
4: Set the counter $r_y = 0$ for every $y \in C$.
5: **for** $shot = 1$ **to** $R$ **do**
6: &nbsp;&nbsp;&nbsp;&nbsp;Use $\mathcal{U}_{\Phi(\boldsymbol{s})}$ to prepare initial feature-map state $|\Phi(\boldsymbol{s})\rangle \langle\Phi(\boldsymbol{s})|$
7: &nbsp;&nbsp;&nbsp;&nbsp;Apply optimal discriminator circuit $W(\boldsymbol{\theta}^*)$ to the initial feature-map state .
8: &nbsp;&nbsp;&nbsp;&nbsp;Apply $|C|$ - outcome measurement $\{M_y\}_{y \in C}$
9: &nbsp;&nbsp;&nbsp;&nbsp;Record measurement outcome label $y$ by setting $r_y \rightarrow r_y + 1$
10: **end for**
11: Construct empirical distribution $\hat{p}_y(\boldsymbol{s}) = r_y R^{-1}$.
12: Set label = $\text{argmax}_y \{\hat{p}_y(\boldsymbol{s})\}$
13: **return** label
---

#### **B. Quantum kernel estimation**

For the second classification protocol, we restrict ourselves to the binary label case, with $C = \{+1, -1\}$. Here it will be convenient to write $T = \{\boldsymbol{x}_1, \dots, \boldsymbol{x}_t\}$ with $t = |T|$; also let $y_i = m(\boldsymbol{x}_i)$ be the corresponding label. In this protocol we only use the quantum computer to estimate the $t \times t$ kernel matrix $K(\boldsymbol{x}_i, \boldsymbol{x}_j) = |\langle\Phi(\boldsymbol{x}_i)|\Phi(\boldsymbol{x}_j)\rangle|^2$, c.f. section VII. For all pairs of points $\boldsymbol{x}_i, \boldsymbol{x}_j \in T$ in the the training data, we sample the overlap between feature states to obtain the matrix entry in the kernel. This fidelity can be estimated from the output probability of the circuit depicted in Fig. 5.b. by sampling the output distribution with $R$ shots and only taking the $0^n$ count. The frequency of the $0^n$ count is en estimator of the Kernel entry up to an error $\epsilon = \mathcal{O}(R^{-1/2})$. After the kernel matrix for the full training data has been constructed we use the conventional (classical) support vector machine classifier [1, 2]. The optimal hyperplane can be found by solving the dual quadratic program $L_D$ for the variables $\boldsymbol{\alpha} = \{\alpha_i\}_{i=1 \dots t}$ described in section III A eqn. (10). Hence, to train, we maximize

$$L_D(\boldsymbol{\alpha}) = \sum_{i=1}^t \alpha_i - \frac{1}{2} \sum_{i,j=1}^t y_i y_j \alpha_i \alpha_j K(\boldsymbol{x}_i, \boldsymbol{x}_j), \qquad (1)$$

subject to $\sum_{i=1}^t \alpha_i y_i = 0$ and $\alpha_i \ge 0$ . This problem is concave, and therefore efficiently solvable, whenever $K(\boldsymbol{x}_i, \boldsymbol{x}_j)$ is a positive definite matrix. Standard quadratic programming solvers can be used [3]. The solution to this problem
