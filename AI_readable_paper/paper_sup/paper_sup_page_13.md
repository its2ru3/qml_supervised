The probability of her misclassifying a $y$ sample according to the argmax rule is hence estimated by

$$\text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq y | \boldsymbol{s} \in T_y \right) = \text{Pr}\left( r_y < r_{-y} - yb \right) = \sum_{j=0}^{\lceil \frac{1-yb}{2} R \rceil} \binom{R}{j} p_y^j (1 - p_y)^{R-j}.$$

Assuming large $R$, computing this exactly may be difficult. Setting $R p_y = a, R p_y(1-p_y) = \beta^2$ and $\lceil \left( \frac{1+yb}{2} \right) R \rceil = \gamma$, we can approximate the binomial CDF as an error function:

$$\begin{aligned} \text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq y | \boldsymbol{s} \in T_y \right) &= \sum_{j=0}^{\lceil \left(\frac{1-yb}{2}\right) R \rceil} \binom{R}{j} p_c^{R-j} (1 - p_c)^j \approx \int_{-\infty}^{\gamma} dx \frac{1}{\sqrt{2\pi}\beta} \text{exp} \left( -\frac{1}{2} \left(\frac{x-a}{\beta}\right)^2 \right) \\ &= \frac{1}{\sqrt{\pi}} \int_{-\infty}^{\frac{\gamma-a}{\sqrt{2}\beta}} dz \; e^{-z^2} = \frac{1}{2} \text{erf} \left( \frac{\gamma - a}{\sqrt{2}\beta} \right) + \frac{1}{2} \\ &= \frac{1}{2} \text{erf} \left( \sqrt{R} \frac{\frac{1-yb}{2} - p_y}{\sqrt{2(1-p_y)p_y}} \right) + \frac{1}{2}. \end{aligned}$$

See Fig. 4 a. The error function can be consequently approximated with a sigmoid

$$\text{sig}(x) = \frac{1}{1 + \exp(-x)} \approx \frac{1}{2} \left( \text{erf}(x) + 1 \right),$$

which gives

$$\text{Pr}\left( \tilde{m}_{|T}(\boldsymbol{s}) \neq y | \boldsymbol{s} \in T_y \right) \approx \text{sig} \left( \sqrt{R} \frac{\frac{1-yb}{2} - p_y}{\sqrt{2(1-p_y)p_y}} \right). \qquad (43)$$

as an estimate for misclassifying a sample $\boldsymbol{s}$. The cost function to optimize is then given by using this in eqn. (42).

**FIG. 4.** (a) For a single shot (R=1) the assignment error of the decision rule is given by $1 - p_y$. The sigmoid contribution, eqn. (43) to the cost-function interpolates from linear to logistic-normal CDF (approximately sigmoid). In the experiment the data was sampled with 2000 shots, although the cost-function was evaluated with only $R = 200$ to provide a smoother function to the optimization routine. The plot depicts the cost-function as a function of the inner product of feature vector and separating hyperplane. (b) Comparison of different loss function that can be used in the optimization of linear threshold functions. We depict the hinge loss $\text{Loss}_h(z)$, logistic regression $\text{Loss}_{log}(z)$ and the reversed sigmoid cost-function $\text{Loss}_{QVC}(z)$ used for the variational circuit classifier in the experiment. (c) The derivative of the sigmoid cost-function eqn. (43) contribution with respect to the inner product of feature vector and separating hyperplane

To better compare the quantum variational classification with support vector machines we will provide some additional background and highlight the similarities and differences in terms of the optimization problem. The goal of a classical support vector machine, c.f. section III A, is to optimize a linear threshold function in feature space so that
