We have that $\text{sig}(-z) = 1 - \text{sig}(z)$ so that, taking in to account the normalization of the argument in terms of denominator that considers the statistical fluctuations at finite $R$, we are left with a loss function $\text{Loss}_{QVC} = 1 - \text{sig}(z)$ that is compared to both the hinge loss and the logistic regression in Fig 4.b.

Note, that the cost function $\text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq 1 | \boldsymbol{s} \in T_1 \right)$ as depicted in Fig 4.a is most sensitive to states for which $\mathbf{w} \circ \Phi(\boldsymbol{x})$ is small. These are states that lie close to the decision boundary. When we perform a gradient based optimization, we see that the largest contribution to the gradient comes from the states that lie close to this boundary, Fig 4.c. The cost function therefore improves mostly by increasing the distance of the Hyperplane relative to the close to the boundary, which can be interpreted as increasing the margin of the linear separator. Note, that the width of this region depends on the parameter $R$. While the single shot case (for which $R = 1$) yields a cost-function $\text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq y | \boldsymbol{s} \in T_y \right) = 1 - p_y(\boldsymbol{s})$ that is sensitive to all points in the training set, we have that as $R$ increases the contributions to the gradient concentrate increasingly at the decision boundary Fig 4.c. This behavior lends itself to the interpretation that, although the optimization considered here is not the conventional SVM problem, its objective of increasing the distance to states that lie close to the decision boundary is in fact similar.

There are many other cost functions that can be considered to train the classifier. Examples range from hinge loss, over logistic - regression, the perceptron criterion to the squared loss and others. We have chosen the cost-function implemented in the experiment based on the statistical analysis of the histogram decision criterion discussed above. Furthermore it has the property of focusing on points that lie close to the decision boundary.

#### **B. Multi label classification**

For multiple labels, one tries to optimize

$$P_{\text{err}} = \frac{1}{|T|} \sum_c \sum_{\boldsymbol{s} \in T_c} \text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq c | \boldsymbol{s} \in T_c \right) ,$$

where:

$$\text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq c | \boldsymbol{s} \in T_c \right) = \text{Pr} \left( n_c < \max_{c'} \left( \{n_{c'}\}_{c' \neq c} \right) \right) .$$

We consider the case of three labels. For $R$ samples with frequencies $\{n_0, n_1, n_2\}$, drawn independently from the output probability distribution, the probability of misclassifying a sample $\boldsymbol{s} \in T_0$ by argmax is given by

$$\text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq 0 | \boldsymbol{s} \in T_0 \right) = \text{Pr}\left( n_0 < \max(n_1, n_2) \right) = \text{Pr}\left( n_0 < \left\lceil \frac{N + |n_1 - n_2|}{3} \right\rceil \right),$$

where the last inequality is derived as follows

$$2n_0 < 2\max(n_1, n_2) = |n_1 - n_2| + n_1 + n_2 = |n_1 - n_2| + N - n_0 .$$

Hence setting $\gamma = \frac{N + |n_1 - n_2|}{3}$, it follows that

$$\text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq 0 | \boldsymbol{s} \in T_0 \right) = \sum_{k=0}^{k=\gamma} \binom{R}{k} p_0^k (1 - p_0)^{N-k} \approx \text{sig} \left( \frac{\gamma - N p_0}{\sqrt{2N(1 - p_0)p_0}} \right) .$$

This however still depends on $n_1, n_2$, which can’t be simply eliminated. Additionally, for a general $k$-label case, there is no simple analytic solution for $\gamma$. For this reason, we try to estimate the above probability by making the approximation $\gamma = \max_{c'} \left( \{n_{c'}\}_{c' \neq c} \right)$. So for $k$-label case, the cost function terms are given by

$$\text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq c | \boldsymbol{s} \in T_c \right) \approx \text{sig} \left( \sqrt{R} \frac{\max_{c'} \left( \{n_{c'}\}_{c' \neq c} \right) - n_c}{\sqrt{2(N - n_c)n_c}} \right) .$$

#### **VII. QUANTUM KERNEL ESTIMATION**

For the second classification method we only use the quantum computer to estimate the kernel $K(\boldsymbol{x}_i, \boldsymbol{x}_j) = |\langle\Phi(\boldsymbol{x}_i)|\Phi(\boldsymbol{x}_j)\rangle|^2$. Then we use the classical optimization problem as outlined again in eqn. (10) to obtain the
