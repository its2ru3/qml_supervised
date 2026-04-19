<center><b>CONTENTS</b></center>

I. Classification problems &nbsp;&nbsp;&nbsp; 1

II. Description of the algorithms &nbsp;&nbsp;&nbsp; 2
A. Quantum variational classification &nbsp;&nbsp;&nbsp; 2
B. Quantum kernel estimation &nbsp;&nbsp;&nbsp; 3

III. The relationship of variational quantum classifiers to support vector machines &nbsp;&nbsp;&nbsp; 5
A. Support vector machines (SVMs) &nbsp;&nbsp;&nbsp; 5
B. Variational circuit classifiers &nbsp;&nbsp;&nbsp; 7

IV. Encoding of the data using a suitable feature map &nbsp;&nbsp;&nbsp; 8
A. Non-trivial feature map with entanglement &nbsp;&nbsp;&nbsp; 9

V. Quantum variational classification &nbsp;&nbsp;&nbsp; 11

VI. Choosing the cost-function for the circuit optimization &nbsp;&nbsp;&nbsp; 11
A. Binary label classification &nbsp;&nbsp;&nbsp; 12
B. Multi label classification &nbsp;&nbsp;&nbsp; 15

VII. Quantum kernel estimation &nbsp;&nbsp;&nbsp; 15

VIII. Device parameters &nbsp;&nbsp;&nbsp; 17
A. Gate characterization &nbsp;&nbsp;&nbsp; 17
B. Readout correction &nbsp;&nbsp;&nbsp; 18

IX. Error mitigation and additional experimental results &nbsp;&nbsp;&nbsp; 18
A. Results for additional data sets &nbsp;&nbsp;&nbsp; 19

References &nbsp;&nbsp;&nbsp; 21

---

### **I. CLASSIFICATION PROBLEMS**

Consider a classification task on a set $C = \{1, 2 \ldots c\}$ of $c$ classes (labels) in a supervised learning scenario. In such settings, we are given a training set $T$ and a test set $S$, both are assumed to be labeled by a map $m : T \cup S \rightarrow C$ unknown to the programmer. Both sets $S$ and $T$ are provided to the programmer, but the programmer only receives the labels of the training set. So, formally, the programmer has only access to a restriction $m_{|T}$ of the indexing map $m$:

$$m_{|T} : T \rightarrow C, \; \text{s.t.:} \; m_{|T}(\boldsymbol{t}) = m(\boldsymbol{t}), \; \forall \boldsymbol{t} \in T.$$

It is the programmer's goal to use the knowledge of $m_{|T}$ to infer an indexing map $\tilde{m} : S \rightarrow C$ over the set $S$, such that $m(\boldsymbol{s}) = \tilde{m}(\boldsymbol{s})$ with high probability for any $\boldsymbol{s} \in S$. The accuracy of the approximation to the map is quantified by a classification success rate, proportional to the number of collisions of $m$ and $\tilde{m}$:

$$\nu_{succ.} = \frac{|\{\boldsymbol{s} \in S | m(\boldsymbol{s}) = \tilde{m}(\boldsymbol{s})\}|}{|S|}.$$

For such a learning task to be meaningful it is assumed that there is a correlation in output of the indexing map $m$ over the sets $S$ and $T$. For that reason, we assume that both sets could in principle be constructed by drawing the $S$ and $T$ sample sets from a family of $d$-dimensional distributions $\{p_c : \Omega \subset \mathbb{R}^d \rightarrow \mathbb{R}\}_{c \in C}$ and labeling the outputs according to the distribution. It is assumed that the hypothetical classification function $m$ to be learned is constructed this way. The programmer, however, does not have access to these distributions and the labeling function directly. She is only provided with a large, but finite, number of samples and the matching labels.

The conventional approach to this problem is to construct a family of classically computable function $\tilde{m} : \langle \boldsymbol{\theta}, S \rangle \rightarrow C$, indexed by a set of parameters $\boldsymbol{\theta}$. These weights are then inferred from $m_{|T}$ by an optimization procedure on a classical cost function. Here, we consider a scenario where the whole, or parts of the classification protocol $m$, are generated on a quantum computer.
