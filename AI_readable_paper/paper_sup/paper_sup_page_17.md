$K$ matrix and the trivial diagonals, $|T|(|T| - 1)2^{-1}$ matrix entries have to be estimated. Thus the full sampling complexity is expected to scale as $\mathcal{O}(\epsilon^{-2}|T|^4)$. A more careful analysis of the statistical error could be carried out by using one of the matrix-concentration results [16].

Note that the optimization problem, eqn. (10) is only concave, when the matrix $K \ge 0$ is positive semi-definite. It can happen, that the shot noise and other errors in the experiment lead to a $\hat{K}$ that is no longer positive semi-definite. We have indeed observed this multiple times in the experiment. A possible way of dealing with this problem is a method developed in [17], where an optimization problem is solved to find the closest positive semi-definite $K$-matrix in trace norm to $\hat{K}$ consistent with the constraint. In our experiments however, we have found this not to be necessary and the performance has been almost optimal without performing this method.

#### **VIII. DEVICE PARAMETERS**

Our experimental device consists of five coupled superconducting transmons, only two of which are used in this work. Two co-planar waveguide (CPW) resonators, acting as quantum buses, provide the device connectivity. Each qubit has one additional CPW resonator for control and readout. Entanglement in our system is achieved via CNOT gates, which use cross-resonance [18] as well as single qubit gates as primitives. The quantum processor is thermally anchored to the mixing chamber plate of a dilution refrigerator.

Our device is fabricated on a $720$-$\mu\text{m}$-thick Si substrate. A single optical lithography step is used to define all CPW structures and the qubit capacitors with Nb. The Josephson junctions are patterned via electron beam lithography and made by double-angle deposition of Al.

The dispersive readout signals are amplified by Josephson Parametric Converters [19] (JPC). Both the quantum processor and the JPC amplifiers are thermally anchored to the mixing chamber plate of a dilution refrigerator.

The two qubit fundamental transition frequencies are $\omega_i/2\pi = \{5.2760(4), 5.2122(3)\} \text{ GHz}$, with anharmonicities $\Delta_i/2\pi = \{-330.3, -331.9\} \text{ MHz}$, where $i \in \{0, 1\}$. The readout resonator frequencies used are $\omega_{Ri}/2\pi = \{6.530553, 6.481651\} \text{ GHz}$, while the CPW bus resonator connecting $Q_0$ and $Q_1$ was unmeasured and designed to be $7.0 \text{ GHz}$. The dispersive shifts and line widths of the readout resonators are measured to be $2\chi_i/2\pi = \{-1.06, -1.02\} \text{ MHz}$ and $\kappa_i/2\pi = \{661, 681\} \text{ kHz}$, respectively.

The two qubit lifetimes and coherences were measured intermittently throughout our experiments. The observed mean values were $T_{1(i)} = \{55, 38\}, T_{2(i)}^* = \{16, 17\}, T_{2(i)}^{\text{echo}} = \{43, 46\} \;\mu\text{s}$ with $i \in \{0, 1\}$

#### **A. Gate characterization**

Our experiments use calibrated $X-$rotations ($X_\pi$ and $X_{\pi/2}$) as single-qubit unitary primitives. $Y-$rotations are attained by appropriate adjustment of the pulse phases, whereas $Z-$rotations are implemented via frame changes in software [20]. A time buffer is added at the end of each physical pulse to mitigate effects from reflections and evanescent waves in the cryogenic control lines and components.

We use two sets of gate times in order to perform the Richardson extrapolation of the noise in our system [21, 22]. For the first set of gate times we use $83 \text{ ns}$ for single-qubit gates and $333 \text{ ns}$ for each cross-resonance pulse. The buffer after each physical pulse is $6.5 \text{ ns}$. The single-qubit gates are gaussian shaped pulses with $\sigma = 20.75 \text{ ns}$. The cross-resonance gates are flat with turn-on and -off gaussian shapes of $\sigma = 10 \text{ ns}$. Our implementation of a CNOT has a duration of two single-qubit pulses and two cross-resonance pulses, giving a total of $858 \text{ ns}$ for the first set of gate times, including buffers. For our second set of gate times we use the times of the first set but stretched by a factor of 1.5, including the pulses $\sigma$s and the buffers. This gives a total CNOT time of $1.287 \;\mu\text{s}$ and single-qubit gates of $\sim 125 \text{ ns}$.

We experimentally verified our single- and two-qubit unitaries by Randomized Benchmarking (RB) [23, 24]. The following table shows the RB results for all single-qubit gates used in our experiments, including individual and simultaneous RB.
