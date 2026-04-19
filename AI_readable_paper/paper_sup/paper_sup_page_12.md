**FIG. 3.** (a) Circuit representation of short depth quantum circuit to define the separating hyperplane. The single qubit rotations $U(\theta_{i,t}) \in \text{SU}(2)$ are depicted by single line boxes parametrized by the angles $\theta_i$, while the entangling operation $U_{ent}$ is determined by the interaction graph of the superconducting chip. (b) Depiction of entangling gate as a product of $\text{CZ}_{i, i+1}$ for $i=1, \dots, 5$ gates following the interaction graph of a circle $G = C_5$.

we may consider a ‘winner takes all’ scenario, where we assign the label according to the outcome with the largest probability estimate. We choose a cost function, so that the optimization procedure minimizes the probability of assigning the wrong label after having constructed the distribution after $R$ shots.

There are various ways of performing a multi-label classification. We only need to modify the final measurement $M$, to correspond to multiple partitions. This can be achieved by multiple strategies. For example one could choose to measure again in the computational basis, i.e. the basis in which Pauli $Z$ are diagonal and then constructing classical labels form the measured samples, such as a labeling the outcome $z \in \{0,1\}^n$ according to a function $f : \{0,1\}^n \rightarrow \{1, \dots, c\}$. The resulting $\{M_y\}_{y=1, \dots, c}$ is therefore diagonal in the computational basis. Alternatively one could construct a commuting measurement akin to the syndrome check measurement for quantum stabilizers. For this approach we choose a set $\{g_i\}_{i=1 \dots \lceil \log_2(c) \rceil}$ of Pauli matrices $g_i \in \mathcal{P}_N$ that are commuting $[g_i, g_j] = 0$. The resulting measurement that would need to be performed is similar to that of an error correcting scheme. The measurement operators are given by $M_y = 2^{-1} \left( 1 - \prod_{i=1}^{\lceil \log_2(c) \rceil} g_i^{y^i} \right)$. Here $y^i$ denotes the $i$'th bit in the binary representation of $y$. In either case, the decision rule that assigns the labels can be written as

$$\tilde{m}_{|T}(\boldsymbol{x}) = \text{arg}\max_{c'} \langle \Phi(\boldsymbol{x}) | W(\boldsymbol{\theta})^\dagger M_{c'} W(\boldsymbol{\theta}) | \Phi(\boldsymbol{x}) \rangle. \qquad (41)$$

This corresponds to taking $R$ shots in order to estimate the largest outcome probability from the outcome statistics of the measurement $M_y$ for $y = 1, \dots, c$. Labelling $T_c$ the subset of samples $T$ labelled with $c$, the avarage expected misclassification rate is given by:

$$P_{\text{err}} = \frac{1}{|T|} \left( \sum_c \sum_{\boldsymbol{s} \in T_c} \text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq c | \boldsymbol{s} \in T_c \right) \right). \qquad (42)$$

The error probability of misclassifying an individual datum is written as $\text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq c | \boldsymbol{s} \in T_c \right)$. This error probability is now used to define the empirical risk function $R_{\text{emp}}(\boldsymbol{\theta}) = P_{\text{err}}$. We discuss of how to find suitable ways of evaluating the cost function for this classification scheme.

#### **A. Binary label classification**

Assume the programmer classifies labels $y \in \{-1, 1\}$ by taking $R$ shots for a single datapoint. She obtains an empirical estimates of probability of the datum being labeled by a label $y$

$$\hat{p}_y = \frac{r_y}{R}.$$

After $R = r_y + r_{-y}$ shots and a prior bias $b$, she misclassifies into a label $y$ if

$$\hat{p}_y < \hat{p}_{-y} + yb \rightarrow r_y < r_{-y} + ybR \rightarrow r_y < \left\lceil \frac{1 - yb}{2} R \right\rceil$$
