will be given by a nonnegative vector $\boldsymbol{\alpha}^* = (\alpha_1^*, \dots, \alpha_t^*)$. Due to complementary slackness, c.f. eqn. (18) we expect that many of the $\alpha_i^*$ will be zero. Hence, there will be only subset of training samples that are needed to construct the optimal hyperplane. These samples are referred to as the support vectors.

The training phase consists of the following steps:

---
**Algorithm 3** Quantum kernel estimation: the training phase
---
1: **Input** Labeled training samples $T = \{\boldsymbol{x} \in \Omega \subset \mathbb{R}^n\} \times \{y \in C\}$, quadratic program solver.
2: **Parameters** Number of measurement shots $R$.
3: Calibrate the quantum hardware to generate short depth circuits.
4: **for** $i = 1$ **to** $t$ **do**
5: &nbsp;&nbsp;&nbsp;&nbsp;**for** $j = 1$ **to** $t$ **do**
6: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Set the counter $r_{0^n} = 0$
7: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**for** $shot = 1$ **to** $R$ **do**
8: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Run circuit from Fig. 5.b with parameters $\boldsymbol{x}_i, \boldsymbol{x}_j$.
9: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Measure outcome in Z-basis.
10: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**if** Measurement outcome is $0^n$ **then**
11: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Increase counter by one, setting $r_{0^n} \rightarrow r_{0^n} + 1$.
12: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**end if**
13: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**end for**
14: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Construct kernel estimate $\hat{K}(\boldsymbol{x}_i, \boldsymbol{x}_j) = r_{0^n} R^{-1}$.
15: &nbsp;&nbsp;&nbsp;&nbsp;**end for**
16: **end for**
17: Use quadratic program solver to optimize $\boldsymbol{\alpha}$ in $L_D$ in eqn. (1) with kernel $K = \hat{K}$ and set $T$.
18: **return** the final parameters $\boldsymbol{\alpha}^*$ and value of the cost function $L_D$ and kernel estimator $\hat{K}$.
---

In the classification phase, we want to assign a label to a new datum $\boldsymbol{s} \in S$ of the test set. For this, the inner products $K(\boldsymbol{x}_i, \boldsymbol{s})$ between all support vectors $\boldsymbol{x}_j \in T$ with $\alpha_i^* > 0$ and the new datum $\boldsymbol{s}$ have to be estimated on the quantum computer, c.f. Fig. 5.b. The new label $\tilde{m}(\boldsymbol{s})$ for the datum is assigned according to eqn. (19). Since all support vectors are known from the training phase and we have obtained access to the kernel $K(\boldsymbol{x}_i, \boldsymbol{s})$ from the quantum hardware, the label can be directly computed according to

$$\tilde{m}(\boldsymbol{s}) = \text{sign}\left( \sum_{i=1}^t y_i \alpha_i^* K(\boldsymbol{x}_i, \boldsymbol{s}) + b \right).$$

Note that the bias $b$ in $\tilde{m}(\boldsymbol{s})$ can calculated from the weights $\alpha_i^*$ by choosing any $i$ with $\alpha_i^* > 0$ and solving $\sum_j y_j \alpha_j^* K(\boldsymbol{x}_j, \boldsymbol{x}_i) + b = y_i$ for $b$.

---
**Algorithm 4** Quantum kernel estimation: the classification phase
---
1: **Input** An unlabeled sample from the test set $\boldsymbol{s} \in S$, optimal SVM parameters $\boldsymbol{\alpha}^*$, $b$ and training data set $T$.
2: **Parameters** Number of measurement shots $R$
3: Calibrate the quantum hardware to generate short depth circuits.
4: **for** $i = 1$ **to** $t$ with $\alpha_i^* > 0$ **do**
5: &nbsp;&nbsp;&nbsp;&nbsp;Set the counter $r_{0^n} = 0$.
6: &nbsp;&nbsp;&nbsp;&nbsp;**for** $shot = 1$ **to** $R$ **do**
7: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Run circuit from Fig. 5.b with parameters $\boldsymbol{x}_i, \boldsymbol{s}$
8: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Measure outcome in Z-basis
9: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**if** Measurement outcome is $0^n$ **then**
10: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Increase counter by one, setting $r_{0^n} \rightarrow r_{0^n} + 1$
11: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**end if**
12: &nbsp;&nbsp;&nbsp;&nbsp;**end for**
13: &nbsp;&nbsp;&nbsp;&nbsp;Construct kernel estimate $\hat{K}(\boldsymbol{x}_i, \boldsymbol{s}) = r_{0^n} R^{-1}$.
14: **end for**
15: **return** $\text{sign}\left( \sum_{i=1}^t y_i \alpha_i^* \hat{K}(\boldsymbol{x}_i, \boldsymbol{s}) + b \right)$.
---
