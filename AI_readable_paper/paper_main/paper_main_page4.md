set $\boldsymbol{x}_i \in T$ obtained from the optimization. This is sufficient to construct the full SVM classifier. A detailed description is provided in Supplementary Information.

To estimate the inner product for the kernel, standard methods could be used$^{25,26}$. However, since the feature map circuits are given, the overlap can be estimated directly from the transition amplitude $|\langle \Phi(\boldsymbol{x}) | \Phi(\boldsymbol{z}) \rangle|^2 = |\langle 0^n | \mathcal{U}^\dagger_{\Phi(\boldsymbol{x})} \mathcal{U}_{\Phi(\boldsymbol{z})} | 0^n \rangle|^2$. First, we apply the circuit Fig. 2c, a composition of two feature map circuits to $|0^n\rangle$. Then, we measure the final state in the Z-basis $R$ times and record the frequency of observing the $0^n$ string. This frequency is the estimate of the transition probability. Each kernel entry is obtained to an additive sampling error of $\epsilon$ when $\mathcal{O}(\epsilon^{-2})$ shots are used. In the training phase a total of $\mathcal{O}(|T|^2)$ amplitudes have to be estimated. An estimator $\hat{K}$ for the kernel matrix that deviates with high probability in operator norm from the exact kernel $K$ by at most $\|K - \hat{K}\| \le \delta$ can be obtained with $R = \mathcal{O}(\delta^{-2} |T|^4)$ shots in total. The sampling error can compromise the positive semi-definiteness of the kernel. Although not applied in this work, this can be remedied by employing an adaption of the scheme presented in ref. $^{27}$.

For the experimental implementation of estimating the kernel matrix $\hat{K}$ (see circuit in Fig. 2c), we again apply the error-mitigation protocol$^{10,24}$ to first order. We use 50,000 shots per matrix entry. We run the training stage on data obtained from three different unitaries, which we will label as Set I, Set II and Set III. Set III is shown in Fig. 3b. The training data used to obtain the kernel and the support vectors are the same data used in the training of our variational classifier. The support vectors (green circles in Fig. 3b) are then used to classify ten different test sets randomly drawn from each entire set. Set I and Set II each yield 100% success over the classification of all ten different test sets, whereas Set III averages a success of 94.75%. For more details see Supplementary Information. These classification results are given in Fig. 3c as dashed red lines to compare with the results of our variational method. In Fig. 4a we show the ideal and the experimentally obtained kernel matrices, $K$ and $\hat{K}$, for Set III. The largest deviation between $K$ and $\hat{K}$ is found in row (or column) 8, depicted in Fig. 4b. All support vectors for the three sets and equivalent plots are given in Supplementary Information.

The two classifiers—a variational quantum classifier and a quantum kernel estimator—build upon the realization that a feature map that is hard to estimate classically is an important part of creating a quantum advantage. This realization enables us to search for machine learning algorithms that are accessible to noisy intermediate-scale (NISQ) devices. It will be intriguing to develop suitable feature maps for quantum state spaces, which have a provable quantum advantage while providing a substantial improvement on real-world datasets. Given the ubiquity of kernel methods in machine learning, we are optimistic that our technique will extend application beyond binary classification. Our experiments also highlight the impact of noise on the success of such hybrid algorithms, and demonstrate that these error-mitigation techniques present a route to accurate classification even with NISQ hardware.

During the preparation of this manuscript we became aware of the independent theoretical work by Schuld et al.$^{28,29}$.

**Data availability**
All data generated or analysed during this study are included in this Letter (and its Supplementary Information).

**Online content**
Any methods, additional references, Nature Research reporting summaries, source data, statements of data availability and associated accession codes are available at https://doi.org/10.1038/s41586-019-0980-2.

Received: 26 June 2018; Accepted: 16 January 2019; Published online 13 March 2019.

1. Mitarai, K., Negoro, M., Kitagawa, M. & Fujii, K. Quantum circuit learning. Preprint at https://arxiv.org/abs/1803.00745 (2018).
2. Farhi, E. & Neven, H. Classification with quantum neural networks on near term processors. Preprint at https://arxiv.org/abs/1802.06002 (2018).
3. Preskill, J. Quantum computing in the NISQ era and beyond. Preprint at https://arxiv.org/abs/1801.00862 (2018).
4. Arunachalam, S. & de Wolf, R. Guest column: a survey of quantum learning theory. *SIGACT News* **48**, 41–67 (2017).
5. Ciliberto, C. et al. Quantum machine learning: a classical perspective. *Proc. R. Soc. Lond. A* **474**, 20170551 (2018).
6. Dunjko, V. & Briegel, H. J. Machine learning & artificial intelligence in the quantum domain: a review of recent progress. *Rep. Prog. Phys.* **81**, 074001 (2018).
7. Biamonte, J. et al. Quantum machine learning. *Nature* **549**, 195–202 (2017).
8. Romero, J., Olson, J. P. & Aspuru-Guzik, A. Quantum autoencoders for efficient compression of quantum data. *Quant. Sci. Technol.* **2**, 045001 (2017).
9. Wan, K. H., Dahlsten, O., Kristjánsson, H., Gardner, R. & Kim, M. Quantum generalisation of feedforward neural networks. Preprint at https://arxiv.org/abs/1612.01045 (2016).
10. Temme, K., Bravyi, S. & Gambetta, J. M. Error mitigation for short-depth quantum circuits. *Phys. Rev. Lett.* **119**, 180509 (2017).
11. Li, Y. & Benjamin, S. C. Efficient variational quantum simulator incorporating active error minimization. *Phys. Rev. X* **7**, 021050 (2017).
12. Terhal, B. M. & DiVincenzo, D. P. Adaptive quantum computation, constant depth quantum circuits and Arthur-Merlin games. *Quantum Inf. Comput.* **4**, 134–145 (2004).
13. Bremner, M. J., Montanaro, A. & Shepherd, D. J. Achieving quantum supremacy with sparse and noisy commuting quantum computations. *Quantum* **1**, 8 (2017).
14. Vapnik, V. *The Nature of Statistical Learning Theory* (Springer Science & Business Media, 2013).
15. Rebentrost, P., Mohseni, M. & Lloyd, S. Quantum support vector machine for big data classification. *Phys. Rev. Lett.* **113**, 130503 (2014).
16. Kandala, A. et al. Hardware-efficient variational quantum eigensolver for small molecules and quantum magnets. *Nature* **549**, 242–246 (2017).
17. Farhi, E., Goldstone, J., Gutmann, S. & Neven, H. Quantum algorithms for fixed qubit architectures. Preprint at https://arxiv.org/abs/1703.06199 (2017).
18. Burges, C. J. A tutorial on support vector machines for pattern recognition. *Data Min. Knowl. Discov.* **2**, 121–167 (1998).
19. Boser, B. E., Guyon, I. M. & Vapnik, V. N. A training algorithm for optimal margin classifiers. In *Proc. 5th Annual Workshop on Computational Learning Theory* 144–152 (ACM, 1992).
20. Goldberg, L. A. & Guo, H. The complexity of approximating complex-valued Ising and Tutte partition functions. *Computat. Complex.* **26**, 765–833 (2017).
21. Demarie, T. F., Ouyang, Y. & Fitzsimons, J. F. Classical verification of quantum circuits containing few basis changes. *Phys. Rev. A* **97**, 042319 (2018).
22. Spall, J. C. A one-measurement form of simultaneous perturbation stochastic approximation. *Automatica* **33**, 109–112 (1997).
23. Spall, J. C. Adaptive stochastic approximation by the simultaneous perturbation method. *IEEE Trans. Automat. Contr.* **45**, 1839 (2000).
24. Kandala, A. et al. Extending the computational reach of a noisy superconducting quantum processor. Preprint at https://arxiv.org/abs/1805.04492 (2018).
25. Buhrman, H., Cleve, R., Watrous, J. & de Wolf, R. Quantum fingerprinting. *Phys. Rev. Lett.* **87**, 167902 (2001).
26. Cincio, L., Subasi, Y., Sornborger, A. T. & Coles, P. J. Learning the quantum algorithm for state overlap. Preprint at https://arxiv.org/abs/1803.04114 (2018).
27. Smolin, J. A., Gambetta, J. M. & Smith, G. Efficient method for computing the maximum-likelihood quantum state from measurements with additive Gaussian noise. *Phys. Rev. Lett.* **108**, 070502 (2012).
28. Schuld, M. & Killoran, N. Quantum machine learning in feature Hilbert spaces. Preprint at https://arxiv.org/abs/1803.07128 (2018).
29. Schuld, M., Bocharov, A., Svore, K. & Wiebe, N. Circuit-centric quantum classifiers. Preprint at https://arxiv.org/abs/1804.00633 (2018).

**Acknowledgements** We thank S. Bravyi for discussions. A.W.H. acknowledges funding from the MIT-IBM Watson AI Lab under the project 'Machine Learning in Hilbert Space'. The research was supported by the IBM Research Frontiers Institute. We acknowledge support from IARPA under contract W911NF-10-1-0324 for device fabrication.

**Reviewer information** *Nature* thanks Christopher Eichler, Seth Lloyd, Maria Schuld and the other anonymous reviewer(s) for their contribution to the peer review of this work.

**Author contributions** The work on the classifier theory was led by V.H. and K.T. The experiment was designed by A.D.C., J.M.G. and K.T. and implemented by A.D.C. All authors contributed to the manuscript.

**Competing interests** The authors declare competing interests: Elements of this work are included in a patent filed by the International Business Machines Corporation with the US Patent and Trademark office.

**Additional information**
**Supplementary information** is available for this paper at https://doi.org/10.1038/s41586-019-0980-2.
**Reprints and permissions information** is available at http://www.nature.com/reprints.
**Correspondence and requests for materials** should be addressed to A.D.C. or K.T.
**Publisher's note:** Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

© The Author(s), under exclusive licence to Springer Nature Limited 2019
