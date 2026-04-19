this hyperplane has the largest possible margin between the two labeled data sets. This is of course only possible when the data is in fact separable by a hyperplane in feature space. In this case, a direct formulation of this problem reads

$$\text{maximize} \quad \gamma$$
$$\text{subject to:} \quad \|\mathbf{w}\|_2^2 = 1$$
$$y_i \left( \mathbf{w} \circ \Phi(\boldsymbol{x}_i) + b \right) \ge \gamma \quad \forall i = 1, \dots, t. \qquad (44)$$

The advantage of the conventional optimization problem for SVMs eqn. (5) is that it turns this non-convex optimization problem in to a convex optimization problem by considering a normal $\mathbf{w}$ that is variable in length. Moreover, if the data is not linearly separable, we have discussed a common trick to allow for outliers by constructing a soft margin SVM, c.f. eqn. (8) and introducing slack variable $\xi_i \ge 0$ with $i = 1 \dots t$ to soften the constraints. Note, that such a soft margin SVM can be implemented by eliminating the slack variables and modifying the SVM optimization problem to [1]

$$\text{minimize} \quad L_P = \frac{1}{2} \|\mathbf{w}\|_2^2 + C \sum_{j=1}^t \max(1 - y_j(\mathbf{w} \circ \Phi(\boldsymbol{x}_j) + b), 0). \qquad (45)$$

The normal of $\mathbf{w}$ is now unconstrained, and the soft margin constraints are implemented through the hinge loss function $\text{Loss}_h(z) = \max(1 - z, 0)$. The term $\|\mathbf{w}\|_2^2$ is often referred to as the regularization and the total cost function is a sum of convex functions and therefore convex itself.

The optimization problem for the quantum variational classifier differs from this optimization problem in several points. First, note that both the non-linear dependence of the variational circuit family $W(\boldsymbol{\theta})$ on $\boldsymbol{\theta}$, as well as the constraint $\text{tr}\left[ \left( W(\boldsymbol{\theta})^\dagger \mathbf{f} W(\boldsymbol{\theta}) \right)^2 \right] = 2^n$ (which is the same as demanding that $\|\mathbf{w}\|_2^2 = 1$ for the appropriate inner product) gives rise to a non-convex optimization problem. But more importantly, note that the label assignment $\tilde{m}(\boldsymbol{x})$ of the variational classifier is subject to shot noise even when a large number of samples $R$ are used. This noise is present during the evaluation of the circuit for training and later during classification as well.

A common approach to training a linear classifier that produces noisy labels is through a logistic regression model. In the optimization of this model the hinge loss cost function is replaced by the logistic regression function that can be seen as the maximization of the log - likelihood with a quadratic regularization term [1]

$$\text{minimize} \quad \frac{1}{2} \|\mathbf{w}\|_2^2 + C \sum_{j=1}^t \log(1 + e^{y_j(\mathbf{w} \circ \Phi(\boldsymbol{x}_j) + b)}). \qquad (46)$$

Here, again the cost function is constructed from a quadratic regularizer and a logistic regression functions $\text{Loss}_{log}(z) = -\log(\text{sig}(z))$, where $\text{sig}(z)$ refers to the sigmoid function defined above. Note, that this logistic regression function can be seen as a smoothing of the hinge loss function used in the soft margin SVM as depicted in Fig 4.b.

The setting we consider is still different. We actually use the noisy labels to optimize the cost-function. While in the logistic regression model the evaluation of the cost function is noise free, we have a scenario where we optimize the classifier based on the output of the quantum circuit directly. So the labels that are observed during training are also subject to statistical uncertainty. This, and the fact that we consider a non-convex optimization over the parametrized hyper plane with unit normal constraint make the optimization problem different from the logistic regression model. As explained above, we motivate the choice of cost-function to minimize the average error of assigning a wrong label and substitute the empirical estimate $\hat{p}_y(\boldsymbol{x})$ in lieu of the actual probability $p_y(\boldsymbol{x})$ in eqn. (43) and optimize

$$\text{minimize} \quad \sum_{j=1}^t \text{sig} \left( \sqrt{R} \frac{\frac{1-y_jb}{2} - \hat{p}_{y_j}(\boldsymbol{x}_j)}{\sqrt{2(1-\hat{p}_{y_j}(\boldsymbol{x}_j))\hat{p}_{y_j}(\boldsymbol{x}_j)}} \right). \qquad (47)$$

By construction we have that $0 \le \hat{p}_y \le 1$ and the optimization is over unitary circuits $W(\boldsymbol{\theta})$, which constraints the norm of the hyperplane normal to unity. Recall, c.f. eqn. (20), that the probability of observing the outcome $y$ is given by $p_y(\boldsymbol{x}) = 2^{-1} (1 + y \langle\Phi_\alpha(\boldsymbol{x}) | W^\dagger(\boldsymbol{\theta}) \mathbf{f} W(\boldsymbol{\theta}) | \Phi_\alpha(\boldsymbol{x})\rangle) = 2^{-1} (1 + y \; \mathbf{w} \circ \Phi(\boldsymbol{x}))$, which can be used to re-express the summands in the total cost -function eqn. (43) as

$$\text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq y | \boldsymbol{s} \in T_y \right) \approx \text{sig} \left( - \frac{y \left( \mathbf{w} \circ \Phi(\boldsymbol{x}) + b \right)}{\sqrt{\frac{2}{R} (1 - (\mathbf{w} \circ \Phi(\boldsymbol{x}))^2)}} \right). \qquad (48)$$
