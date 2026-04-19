### **III. THE RELATIONSHIP OF VARIATIONAL QUANTUM CLASSIFIERS TO SUPPORT VECTOR MACHINES**

The references [1, 2] provide a detailed introduction to the construction of support vector machines for pattern recognition. Support vector machines are an important tool to construct classifiers for tasks in supervised learning. We will show that the variational circuit classifier bears many similarities to a classical non-linear support vector machine.

#### **A. Support vector machines (SVMs)**

First, let us briefly review the training task of classical, linear support vector machines for data where $C = \{+1, -1\}$, so that $(\boldsymbol{x}_i, y_i)_{i=1, \dots, t}$ with $\boldsymbol{x}_i \in T \subset \mathbb{R}^d$, $y_i \in \{+1, -1\}$ that is linearly separable. Linear separability asks that the set of points can be split in two regions by a hyperplane $(\mathbf{w}, b)$, parametrized by a normal vector $\mathbf{w} \in \mathbb{R}^d$ and a bias $b \in \mathbb{R}$. The points $\boldsymbol{x} \in \mathbb{R}^d$ that lie directly on the hyperplane satisfy the equation

$$\mathbf{w} \circ \boldsymbol{x} + b = 0 \qquad (2)$$

expressed in terms of the inner product $\circ$ for vectors in $\mathbb{R}^d$. The perpendicular distance of the hyperplane to the origin in $\mathbb{R}^n$ is given by $b\|\mathbf{w}\|^{-1}$. The data set $\{\boldsymbol{x}_i, y_i\}$ is linearly separable by margin $2\|\mathbf{w}\|^{-1}$ in $\mathbb{R}^d$ if there exists a vector $\mathbf{w}$ and a $b$, such that:

$$y_i (\mathbf{w} \circ \boldsymbol{x}_i + b) \ge 1. \quad \forall i = 1, \dots, t \qquad (3)$$

The classification function $\tilde{m}(\boldsymbol{x})$ that is constructed from such a hyperplane for any new data point $\boldsymbol{x} \in \mathbb{R}^n$ assigns the label according to which side of the hyperplane the new data-point lies by setting

$$\tilde{m}(\boldsymbol{x}) = \text{sign}\left( \mathbf{w} \circ \boldsymbol{x} + b \right) . \qquad (4)$$

The task in constructing a linear support vector machine (SVM) in this scenario is the following. One is looking for a hyperplane that separates the data, with the largest possible distance between the two separated sets. The perpendicular distance between the plane and two points with different labels is called a margin and such points are referred to as 'support vectors'. This means that we want to maximize the margin by minimizing $\|\mathbf{w}\|$, or equivalently $\|\mathbf{w}\|^2$ subject to the constraints as given in eqn. (3), for all data points in the training set $T$. The corresponding cost function can be written as:

$$\text{minimize} \quad L_P = \frac{1}{2}\|\mathbf{w}\|^2 \qquad (5)$$
$$\text{subject to:} \quad y_i \left( \mathbf{w} \circ \boldsymbol{x}_i + b \right) \ge 1. \quad \forall i = 1, \dots, t \qquad (6)$$

This can be expressed in terms of the Lagrangian

$$L(\mathbf{w}, \boldsymbol{\alpha}) = \frac{1}{2}\|\mathbf{w}\|^2 - \sum_{i=1}^t \alpha_i y_i (\mathbf{w} \circ \boldsymbol{x}_i + b) + \sum_{i=1}^t \alpha_i, \qquad (7)$$

where $\alpha_i \ge 0$ are Lagrange multipliers chosen to ensure the constraints are satisfied.

For non-separable datasets, it is possible to introduce non-negative slack variables $\{\xi_i\}_{i=1, \dots, t} \in \mathbb{R}_0^+$ which can be used to soften the constraints for linear separability of $(\boldsymbol{x}_i, y_i)$ to

$$y_i (\mathbf{w} \circ \boldsymbol{x}_i + b) \ge (1 - \xi_i),$$
$$\xi_i \ge 0. \qquad (8)$$

These slack variables are then used to modify the objective function by $1/2\|\mathbf{w}\|^2 \rightarrow 1/2\|\mathbf{w}\|^2 + C (\sum_i \xi_i)^r + \sum_i \mu_i \xi_i$. When we choose $r \ge 1$ the optimization problem remains convex and a dual can be constructed. In particular, for $r=1$, neither the $\xi_i$ nor their Lagrange multipliers $\mu_i$ will appear in the dual Lagrangian.

The method can be generalized to the case when the decision function does depend non-linearly on the data by using a trick from [4] and introducing a high-dimensional, non-linear feature map. The data is mapped via a non-linear map

$$\Phi : \mathbb{R}^d \rightarrow \mathcal{H} \qquad (9)$$
