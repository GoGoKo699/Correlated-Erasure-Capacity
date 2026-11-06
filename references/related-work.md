# Related work, attribution, and source versions

Source review dated **6 November 2026**. This document distinguishes inherited coding ingredients from the stochastic channel statements proved in this repository. The mathematical model is specified in [the model account](../science/model.md); the results and proofs are in [the capacity account](../science/capacity-envelope.md) and [the geometry account](../science/geometry-and-loss.md).

## 1. Operational question and the added derivation

One channel use accepts a block of physical qubits. A known, input-independent probability law chooses a surviving subset, and the receiver obtains both that subset's quantum systems and its classical flag. Different block uses are independent. Quantum capacity permits arbitrary encoding across these uses and vanishing decoding error, without shared entanglement, feedback, or auxiliary communication.

The main derivation is a probability-sensitive capacity converse:

$$
Q(\mathcal E_\mu)
\leq \inf_{\pi\in\Pi(\mu,\mu)}\mathbb E_\pi |S\cap T|
\leq \sum_i\alpha_i^2,
\qquad \alpha_i=\Pr_\mu(i\in S).
$$

Here $\Pi(\mu,\mu)$ is the set of joint laws with both marginals equal to $\mu$. The entropy inequality underlying the converse is elementary; the step that matters for this operational question is retaining the mask probabilities and applying a product coupling to every number of channel uses, including entangled inputs. Combining that converse with existing exact-storage codes gives

$$
\sup_{n,\,\mu:\Pr(i\in S)=\alpha\ \forall i}
\frac{Q(\mathcal E_\mu)}{n}=\alpha^2.
$$

This is a supremum over block sizes and admissible correlations. It is not a formula for every individual mask law. The capacity equalities for uniform intersection stars and independently thinned projective lines are further applications of the same converse. The quantum codes that supply their lower bounds are attributed below.

## 2. Distributed storage: the closest coding antecedent

**Sun and Jafar [SJ25]** give an intersection converse for exact distributed storage (Theorem 1), a classical secure-storage to quantum CSS construction (Theorem 2), a Fano result (Theorem 5), and intersection-graph codes (Theorem 6). Their Remark 1 explicitly describes a compound channel: an erasure pattern is selected once and held fixed across uses. Theorem 6 supplies the achieving codes used here. With $N=\binom{\Delta}{m}$ equal-size shares, the code stores $k=\binom{\Delta-2}{m-2}$ qudits recoverable from each star; the inherited ratio is $k/N=m(m-1)/[\Delta(\Delta-1)]$.

The source's storage intersection argument and code design are substantive predecessors. This repository does not claim either as a new construction. Its stochastic converse permits different random masks at successive uses and codes that need not recover from every individual mask. For the uniform-star law, coupling two distinct stars bounds ordinary capacity by exactly the inherited code size. Taking growing $\Delta$, with $m/\Delta$ approaching a prescribed survival probability, then gives the matching extremal envelope. This changes the operational optimization while using the existing achievability machinery.

### Finite fields and physical-qubit accounting

The [SJ25] construction works over a sufficiently large finite field, including fields of characteristic two. A $2^r$-dimensional share can therefore be represented by exactly $r$ qubits, all of which are counted in the input block and erased together. The normalization never treats an arbitrarily large share as a single physical qubit.

A minor algebraic detail in the inspected v1 proof deserves care. In Section 5.7, write

$$
k=\binom{\Delta-2}{m-2},\quad
\delta=\binom{\Delta-2}{m-1},\quad
d=k+\delta=\binom{\Delta-1}{m-1}.
$$

The determinant product in Lemma 3 has total degree at most $d+\Delta\delta$. Substitution gives the sufficient choice

$$
q>\binom{\Delta-1}{m-1}+\Delta\binom{\Delta-2}{m-1}.
$$

The displayed expansion of $(k+\delta)+\Delta\delta$ in that version instead uses $\binom{\Delta-2}{m-2}$ in its second term. The bound above follows directly from the determinant sizes and avoids relying on that expansion. The nonzero-minor assignments and the linear identities in Section 5.7.1 remain valid in characteristic two. Arbitrarily large binary extension fields are available, so this correction changes neither the code rate nor the envelope argument.

## 3. Projective-plane codes are inherited

**Audoux and Couvreur [AC19, Section 4.1]** give the binary one-qubit code used in the geometry account. For $q=2^s$, Proposition 4.7 and Remark 4.8 identify the even subcode of the line-incidence code; Definition 4.9 gives the CSS code; Lemma 4.11 supplies line-supported representatives of both logical operator types. Remark 4.10 identifies $q=2$ with the Steane code. Thus the code and its recovery from every complete line are prior ingredients, including for arbitrarily large powers of two.

The geometry account supplies an explicit decoder and studies three specified stochastic laws on this existing code: uniform lines, zeros of uniform normal vectors, and uniform lines followed by independent thinning. The final family has ordinary capacity $[2t^{q+1}-1]_+$ qubits per block. Its upper bound applies to all multi-block encoders, rather than only assessing this code's decoding success. The normal-vector construction has pairwise independent flags, but its capacity is bounded rather than evaluated exactly.

**Song and Cao [SC26, Theorem 1]** provide a particularly close recent Fano comparison. An encoding of one $D$-dimensional system into seven $D$-dimensional sites with their specified Fano erasure-correction pattern exists exactly when $D$ is a power of two; they also analyze rigidity and stabilizer-state entanglement. Their current paper discusses fixed-code erasure performance. Its Fano recovery and dimension results must not be attributed to this repository. The random-mask capacity envelope here optimizes a different, probability-weighted communication problem.

The relation between recoverable subsets, privacy of their complements, and quantum codes is foundational quantum secret sharing [CGL99, G00]. Matroidal constructions and information-rate bounds also precede this project [SR10, S11]. These sources establish the broader setting; [AC19] is the direct source for the specific all-$q$ binary plane code used here.

## 4. Approximate secret sharing and compound-channel capacity

**Lalou, Natur, and Pereg [QSS26]** already treat asymptotic quantum secret-sharing rates, rather than only finite exact codes. Definition 11 associates each qualified coalition with a member of a compound channel. Theorems 1–3 and Corollary 1 identify the relevant capacity through a regularized maximized minimum of coherent information; the decoder knows the coalition. The reliability requirement is uniform over qualified sets, with one compound index fixed across the block.

Consequently, allowing approximate recovery or using regularized coherent information does not by itself distinguish the present work. The distinction is the specified iid law of masks, its probability weights, and the resulting average-overlap converse and extremal rate. The ordinary channel coding formula used in that argument is standard [D05, BST98].

## 5. Probabilistic recovery and erasure-channel simulation

**Alhejji, Lordi, Baraskar, Shlosberg, and Knill [ALBSK26]** study feasible vectors of probabilities for conclusively recovering a quantum system from particular carrier subsets. The inspected manuscript allows finite but otherwise unrestricted carrier dimensions and gives Lovász-number bounds for disjointness graphs, including uniform-subset consequences. It also proves an erasure-simulation obstruction and includes approximate-recovery estimates. Its probabilistic recovery constraints are therefore directly relevant antecedents, not merely a general invocation of no cloning.

The quantity bounded here is a rate per fixed physical-qubit budget. The overlap cost charges the Hilbert-space size of an intersection and then controls ordinary capacity for every blocklength. A recovery-probability bound whose carrier dimensions are unrestricted does not, without an additional dimension-sensitive argument, establish this normalization. This comparison concerns the inspected manuscript identified in Section 7; it is not a claim about unread revisions.

**Ahmed and Smith [AS26]** introduce fractional extendibility and a robust distributed-monogamy bound. For uniform small subsets, they constrain average EPR recovery; Theorem 10 of the inspected manuscript rules out simulating a more transmissive erasure channel from a less transmissive one when both survival probabilities are at most one half. Tensor-power invariance and processing monotonicity are central to that result.

That question retains distinctions among zero-capacity iid erasure channels. Here, correlated masks within each input block can yield positive capacity even when each physical marginal is below one-half survival. This does not circumvent their obstruction: the correlated block channel is a different resource from the independent erasure channel with the same individual survival probabilities. The comparison again has the source-version limitation below.

## 6. Related channel-diagnostic examples

The insufficiency of low-order channel information is also present in related repository work. [Quantum-Phase-Drift-Capacity](https://github.com/GoGoKo699/Quantum-Phase-Drift-Capacity/blob/4673a1227badca5358519e524e4f9d64e2a285cf/science/indistinguishability.md) studies phase-noise channels agreeing on selected few-carrier reduced maps but having different asymptotic capacity deficits. [LWE-Noise-Geometry](https://github.com/GoGoKo699/LWE-Noise-Geometry/blob/e28ac6c911c6f558013a0083b60268cd9174a9b6/science/channels.md) constructs agreement on every proper reduced channel in a learning comparison. [Nonclassical-Quantum-Access](https://github.com/GoGoKo699/Nonclassical-Quantum-Access/blob/195bc71936d298f01815629d7ca4fc137d022a9e/science/access_profiles.md) separates conclusive recovery profiles from mixtures of deterministic access structures; its example is antidegradable and has zero unassisted capacity.

The pairwise-independent erasure example here is a specific loss-channel consequence of the capacity analysis. Its local comparison discards every unselected quantum output **and flag**. The receiver's complete subset flag exposes the global loss pattern, and higher-order flag statistics distinguish it from independent erasure. No general novelty claim for local-diagnostic insufficiency is needed.

## 7. Source versions and limits of this review

| Reference | Version or publication inspected | Scope of access |
|---|---|---|
| [SJ25] | arXiv v1, 12 October 2025; primary history lists only v1 | Primary full text; model, intersection bound, CSS translation, and Theorem 6 proof inspected |
| [AC19] | Published 2019 article; arXiv history identifies v3, 25 September 2018 | Published full text, especially Section 4.1 |
| [QSS26] | arXiv v2, 26 April 2026, verified by primary history | Primary full text; capacity definitions and compound/QSS results inspected |
| [SC26] | arXiv v2, 31 October 2026, printed on the retrieved primary PDF | Current introduction, Theorem 1, and relevant Fano consequences inspected; not every proof in the 61-page paper independently checked |
| [ALBSK26] | Full manuscript transcription with printed arXiv v1 footer dated 19 July 2026 and manuscript date 21 July 2026 | Relevant primary manuscript text available through the authors' paper on ResearchGate; exact correspondence to a current v2 not verified |
| [AS26] | Full manuscript transcription with printed arXiv v1 footer dated 9 July 2026 and manuscript date 10 July 2026 | Relevant primary manuscript text available through the authors' paper on ResearchGate; exact correspondence to a current v2 not verified |

For the two July 2026 papers, secondary bibliographic records explicitly mention v2, but attempts to retrieve current arXiv history and v2 text did not succeed. This is a bounded source-access gap, not evidence that those versions do not exist. Their primary manuscript texts were inspected; abstracts and title searches were not used to certify the absence of a competing theorem. Any priority-sensitive description should be checked against those current versions when accessible. The attribution and model distinctions above are limited accordingly.

## References

- **[AC19]** Benjamin Audoux and Alain Couvreur, *On tensor products of CSS codes*, Annales de l'Institut Henri Poincaré D **6**(2), 239–287 (2019). DOI [10.4171/AIHPD/71](https://doi.org/10.4171/AIHPD/71). [Published full text](https://numdam.org/item/10.4171/aihpd/71.pdf); [arXiv:1512.07081v3](https://arxiv.org/abs/1512.07081v3).
- **[ALBSK26]** Mohammad A. Alhejji, Noah Lordi, Omkar Baraskar, Ariel Shlosberg, and Emanuel Knill, *Constraints on recovering quantum information after erasure*, [arXiv:2607.17319](https://arxiv.org/abs/2607.17319) (2026). [Inspected manuscript text](https://www.researchgate.net/publication/410634986_Constraints_on_recovering_quantum_information_after_erasure). Version limitation described above.
- **[AS26]** Rabsan Galib Ahmed and Graeme Smith, *Distributed Monogamy of Entanglement limits Quantum Channel Simulation*, [arXiv:2607.08591](https://arxiv.org/abs/2607.08591) (2026). [Inspected manuscript text](https://www.researchgate.net/publication/408698971_Distributed_Monogamy_of_Entanglement_limits_Quantum_Channel_Simulation). Version limitation described above.
- **[BDS97]** Charles H. Bennett, David P. DiVincenzo, and John A. Smolin, *Capacities of Quantum Erasure Channels*, Physical Review Letters **78**, 3217–3220 (1997). DOI [10.1103/PhysRevLett.78.3217](https://doi.org/10.1103/PhysRevLett.78.3217); [arXiv:quant-ph/9701015](https://arxiv.org/abs/quant-ph/9701015). Supplies the ordinary erasure-capacity formula used for the encoded thinning channel.
- **[BST98]** Howard Barnum, John A. Smolin, and Barbara M. Terhal, *The quantum capacity is properly defined without encodings*, Physical Review A **58**, 3496 (1998). DOI [10.1103/PhysRevA.58.3496](https://doi.org/10.1103/PhysRevA.58.3496); [arXiv:quant-ph/9711032](https://arxiv.org/abs/quant-ph/9711032).
- **[CGL99]** Richard Cleve, Daniel Gottesman, and Hoi-Kwong Lo, *How to share a quantum secret*, Physical Review Letters **83**, 648–651 (1999). DOI [10.1103/PhysRevLett.83.648](https://doi.org/10.1103/PhysRevLett.83.648); [arXiv:quant-ph/9901025](https://arxiv.org/abs/quant-ph/9901025).
- **[D05]** Igor Devetak, *The private classical capacity and quantum capacity of a quantum channel*, IEEE Transactions on Information Theory **51**(1), 44–55 (2005). DOI [10.1109/TIT.2004.839515](https://doi.org/10.1109/TIT.2004.839515); [arXiv:quant-ph/0304127v6](https://arxiv.org/abs/quant-ph/0304127v6).
- **[G00]** Daniel Gottesman, *Theory of quantum secret sharing*, Physical Review A **61**, 042311 (2000). DOI [10.1103/PhysRevA.61.042311](https://doi.org/10.1103/PhysRevA.61.042311). The preprint is titled *On the Theory of Quantum Secret Sharing*: [arXiv:quant-ph/9910067](https://arxiv.org/abs/quant-ph/9910067).
- **[QSS26]** Gabrielle Lalou, Husein Natur, and Uzi Pereg, *Quantum Secret Sharing Rates*, [arXiv:2512.22049v2](https://arxiv.org/abs/2512.22049v2) (2026); [primary HTML](https://arxiv.org/html/2512.22049v2). Published in the 2026 IEEE International Symposium on Information Theory, DOI [10.1109/ISIT62367.2026.11654175](https://doi.org/10.1109/ISIT62367.2026.11654175).
- **[S11]** Pradeep Sarvepalli, *Bounds on the information rate of quantum-secret-sharing schemes*, Physical Review A **83**, 042324 (2011). DOI [10.1103/PhysRevA.83.042324](https://doi.org/10.1103/PhysRevA.83.042324); [arXiv:1007.1232](https://arxiv.org/abs/1007.1232).
- **[SC26]** Xidan Song and Ruifeng Cao, *Arithmetic of qudit dimensions governs erasure correction on the Fano plane and stabilizer-state entanglement*, [arXiv:2610.18905v2](https://arxiv.org/abs/2610.18905v2) (31 October 2026). [Retrieved primary PDF](https://arxiv.org/pdf/2610.18905).
- **[SJ25]** Hua Sun and Syed A. Jafar, *On the Capacity of Distributed Quantum Storage*, [arXiv:2510.10568v1](https://arxiv.org/abs/2510.10568v1) (12 October 2025). [Primary HTML](https://arxiv.org/html/2510.10568v1); [author-institution PDF](https://escholarship.org/content/qt83p769jm/qt83p769jm_noSplash_12f88a042a6db1c90cdbf1769511eb52.pdf).
- **[SR10]** Pradeep Sarvepalli and Robert Raussendorf, *Matroids and quantum-secret-sharing schemes*, Physical Review A **81**, 052333 (2010). DOI [10.1103/PhysRevA.81.052333](https://doi.org/10.1103/PhysRevA.81.052333); [arXiv:0909.0549v3](https://arxiv.org/abs/0909.0549v3).
