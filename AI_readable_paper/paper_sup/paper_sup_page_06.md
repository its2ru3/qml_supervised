from a low dimensional space in to a high dimensional Hilbert-space $\mathcal{H}$. This space is commonly referred to as the feature space. If a suitable feature map has been chosen, it is then possible to apply the SVM classifier for the mapped data in $\mathcal{H}$, rather than in $\mathbb{R}^d$. This way it is possible to draw exceedingly complex decision surfaces that separate the data points based on their mapped features.

In light of the fact that the optimization problem now has to be solved in a much higher dimensional feature space with $d \ll \dim(\mathcal{H})$ for the vectors $\Phi(\boldsymbol{x})$ with $\boldsymbol{x} \in T$ it is very helpful to consider the dual of the original primal problem $L_P$ in eqn. (5). The primal problem is a convex, quadratic programming problem, for which the Wolfe dual cost function $L_D$ for the Lagrange multipliers can be readily derived by variation with respect to $\mathbf{w}$ and $b$. The dual optimization problem is expressed as an optimization of the Lagrange multipliers $\boldsymbol{\alpha} = \{\alpha_i\}_{i=1 \dots t}$

$$\text{maximize} \quad L_D = \sum_i \alpha_i - \frac{1}{2} \sum_{i,j} \alpha_i \alpha_j y_i y_j \Phi(\boldsymbol{x}_i) \circ \Phi(\boldsymbol{x}_j), \qquad (10)$$
$$\text{subject to:} \quad \sum_i \alpha_i y_i = 0, \qquad (11)$$
$$0 \le \alpha_i \le C, \quad \forall i = 1, \dots, t. \qquad (12)$$

The variables of the primal can be expressed in terms of the optimal dual variables $\boldsymbol{\alpha}^* = \{\alpha_i^*\}_{i=1 \dots t}$ as

$$\sum_i \alpha_i^* y_i \Phi(\boldsymbol{x}_i) = \mathbf{w} \qquad (13)$$

and the bias $b$ can be computed from the Karush-Kuhn-Tucker (KKT) conditions when the corresponding Lagrange multiplier $\alpha_i^*$ does not vanish. The optimal variables satisfy the KKT conditions and play an important role in the understanding of the SVM. They are given for the primal as

$$\partial_{w_\beta} L(\mathbf{w}, \boldsymbol{\alpha}) = w_\beta - \sum_i \alpha_i y_i \Phi_\beta(\boldsymbol{x}_i) = 0 \quad \text{for} \quad \beta = 1, \dots, \dim(\mathcal{H}). \qquad (14)$$
$$\partial_b L(\mathbf{w}, \boldsymbol{\alpha}) = - \sum_i \alpha_i y_i = 0 \qquad (15)$$
$$\alpha_i \ge 0 \qquad (16)$$
$$y_i \left( \Phi(\boldsymbol{x}_i) \circ \mathbf{w} + b \right) - 1 \ge 0 \qquad (17)$$
$$\alpha_i \left( y_i (\mathbf{w} \circ \Phi(\boldsymbol{x}_i) + b) - 1 \right) = 0. \qquad (18)$$

Note that the condition eqn. (18) ensures that either the optimal $\alpha_i^* = 0$ or the corresponding constraint eqn. (18) is tight. This is a property referred to as complementary slackness, and indicates that only the vectors for which the constraint is tight give rise to non-zero $\alpha_i^* > 0$. These vectors are referred to as the support vectors and we will write $N_S$ for their index set. The classifier in the dual picture is given by substituting $\mathbf{w}$ from eqn. (13) and $b$ into the classifier eqn. (4). The bias $b$ is obtained for any $i \in N_S$ from the equality in eqn. (17).

To understand why it is possible to solve the dual optimization problem in high dimensional space efficiently in the number of training samples $t$, it is important to note that it is in fact not necessary to construct the mapped data $\Phi(\boldsymbol{x}_i)$ in $\mathcal{H}$ explicitly. Both the training data, as well as the new data to be classified, enters only through inner products in both the optimization problem for training, c.f. eqn. (10) and in the classifier, eqn. (4). Hence, we can construct the SVM for arbitrarily high dimensional feature maps $(\Phi, \mathcal{H})$, if we can efficiently evaluate the inner products $\Phi(\boldsymbol{x}_i) \circ \Phi(\boldsymbol{x}_j)$ and $\Phi(\boldsymbol{x}_i) \circ \Phi(\boldsymbol{s})$, for $\boldsymbol{x}_i \in T$ and $\boldsymbol{s} \in S$. In particular, if we can evaluate the kernel $K(\boldsymbol{x}, \boldsymbol{y}) = \Phi(\boldsymbol{x}) \circ \Phi(\boldsymbol{y})$ [1, 4], we can construct a classifier by setting

$$\tilde{m}(\boldsymbol{s}) = \text{sign}\left( \sum_{i \in N_S} \alpha_i^* y_i K(\boldsymbol{x}_i, \boldsymbol{s}) + b \right). \qquad (19)$$

Here we only need to sum over all support vectors $i \in N_S$ for which $\alpha_i^* > 0$. Moreover, one can replace the inner product in the optimization problem eqn. (10) by the kernel.

Examples of kernels frequently considered in the classical literature are for instance the polynomial kernel $K(\boldsymbol{x}, \boldsymbol{y}) = (\boldsymbol{x} \circ \boldsymbol{y} + 1)^m$ or the infinite dimensional Gaussian kernel $K(\boldsymbol{x}, \boldsymbol{y}) = \exp(-1/2\|\boldsymbol{x} - \boldsymbol{y}\|^2)$. If the feature map is sufficiently powerful, increasingly complex distributions can be classified.
