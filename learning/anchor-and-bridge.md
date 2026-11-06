# From Nielsen–Chuang to correlated erasure capacity

A sender encodes an unknown quantum state into labelled physical qubits. Some qubits arrive and the others are marked as erased. The receiver knows which positions survived. The question is how much quantum information can be transmitted when every position has the same survival probability, while the pattern of losses can be correlated.

The probability that one qubit arrives is only part of this description. A code may recover from a carefully arranged small subset even though an arbitrary subset of the same size reveals little. This project connects that recovery geometry to ordinary quantum capacity, which allows coding across many independent uses of the entire loss process.

## 1. The selected edition

The educational anchor is **Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition, Cambridge University Press, 2010**. The hardback ISBN is **9781107002173** and the book DOI is [10.1017/CBO9780511976667](https://doi.org/10.1017/CBO9780511976667).

The [publisher's edition record](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE) and [official contents](https://assets.cambridge.org/97811070/02173/toc/9781107002173_toc.pdf) establish the edition and the section locators below. The contents and metadata were inspected; the complete commercial text was not available for source verification. This bridge supplies its own explanations and points separately to the research results on which the proofs depend.

Nielsen–Chuang is the single textbook anchor. The [30-milestone map](milestones.md) organizes the project's understanding targets. The relevant sections can be consulted alongside that map; completing the whole book is not a prerequisite for reading the scientific account.

## 2. The route from the textbook to this project

Page numbers refer to the printed pagination listed in the publisher's contents.

| Foundation | Nielsen–Chuang locator | Connection to the project |
|---|---|---|
| Subsystems and purification | Sections 2.4.3, p. 105, and 2.5, p. 109 | A retained set selects a reduced state; a reference system makes preservation of quantum information precise. |
| Channels and environments | Sections 8.2.2, p. 357, and 8.3.1, p. 374 | The [flagged channel and complement](../science/model.md#1-one-channel-use-is-a-finite-block) separate surviving qubits, lost qubits, and the classical mask. |
| Fidelity and channel preservation | Sections 9.2.2, p. 409, and 9.3, p. 416 | [Operational capacity](../science/model.md#2-operational-capacity-and-normalization) requires vanishing error on quantum information, including its correlations with a reference. |
| Linear codes, CSS codes, and stabilizers | Sections 10.4.1–10.4.2, pp. 445–450; 10.5, p. 453; 10.5.8, p. 472 | The [binary plane code](../science/geometry-and-loss.md#1-the-inherited-one-qubit-css-code) uses nested linear spaces, commuting checks, and a decoder on the retained line. |
| Entropy and strong subadditivity | Sections 11.3.4, p. 515; 11.3.6, p. 518; 11.4, p. 519 | Classical flags produce block-diagonal states; entropy inequalities turn two retained sets into an [intersection bound](../science/model.md#3-a-two-set-entropy-inequality). |
| Noisy quantum communication | Sections 12.4.1–12.4.3, pp. 561–568 | Entropy exchange and data processing motivate the converse. The regularized capacity theorem is supplied explicitly by Devetak, as explained below. |

Three kinds of source have distinct roles. The textbook provides foundations. The topic pages supply the probability-sensitive derivations and exact channel statements. Research papers supply the regularized coding theorem and the two achieving code families. Their precise attribution and version limits are recorded in [related work](../references/related-work.md).

## 3. Notation and conventions

The following dictionary translates the foundational concepts into the notation used throughout this repository.

| Concept | Project notation | Meaning and accounting |
|---|---|---|
| Physical input | $A=A_1\cdots A_n$ | One use of the block channel contains all $n$ carriers, including those later lost. |
| Retained subsystem | $S\subseteq[n]$, $\rho_S=\operatorname{Tr}_{S^c}\rho$ | $S$ is a classical set of position labels; $\rho_S$ is the quantum state on those positions. |
| Loss statistics | $\mu(S)$, $\alpha_i=\Pr_\mu(i\in S)$ | $\mu$ is the complete mask law; the $\alpha_i$ are only its individual survival probabilities. |
| Noise map and complement | $\mathcal E_\mu$, $\mathcal E_\mu^c$ | The receiver gets retained systems and a flag; the complementary output gets the other systems and the same classical flag. |
| Entropy | $H(\rho)$ and $H(\mu)$ | Quantum state entropy and classical Shannon entropy, respectively, both in bits. The argument identifies which is intended. |
| Coherent information | $I_c(\rho,\mathcal N)$ | Receiver entropy minus complementary-output entropy for a specified input state. It is not automatically the channel's capacity. |
| Logical throughput | $Q(\mathcal E_\mu)$ | Logical qubits per use of the whole block. For physical qubits, divide by $n$ to obtain the rate per input qubit. |
| Dimension weight | $w_i=\log_2 d_i$ | A carrier of dimension $d_i$ is charged its full logarithmic size. In a binary extension field, a share of dimension $2^r$ counts as $r$ qubits. |
| Classical comparison law | $\pi\in\Pi(\mu,\mu)$ | A joint distribution of two masks with the same marginal law. It is a proof device, not an additional transmitted quantum system. |

More explicitly, $H(\rho)=-\operatorname{Tr}(\rho\log_2\rho)$. When a proof writes $H(JL)$, it means the entropy of the reduced state on the union of the disjoint coordinate sets $J$ and $L$.

The parameter $q$ has different roles in the two construction sections. In the star construction, $q=2^r$ is each node's Hilbert-space dimension. In the plane construction, $q=2^m$ is the order of the finite geometry, and each point still carries just **one qubit**. These conventions give different input sizes and must be kept explicit when comparing rates.

There are also two block sizes to distinguish. A fixed channel contains $n$ physical qubits. A capacity code may use that channel $k$ times, with an input entangled across all $kn$ qubits. The capacity limit sends $k$ to infinity for that fixed channel; the extremal envelope subsequently ranges over different finite choices of $n$ and $\mu$.

## 4. The additional steps supplied by this project

### 4.1 Preserve quantum correlations, not only classical labels

Successful quantum transmission must preserve superpositions and correlations with systems outside the communication apparatus. A useful formulation starts with a maximally entangled state of a logical input $L$ and an untouched reference $R$:

$$
|\Phi_d\rangle_{RL}
=\frac1{\sqrt d}\sum_{j=0}^{d-1}|j\rangle_R|j\rangle_L.
$$

After encoding $L$, sending the physical inputs, and decoding an output $L'$, let the joint reference-output state be $\omega_{RL'}$. The overlap

$$
f_{\mathrm e}=\langle\Phi_d|\omega_{RL'}|\Phi_d\rangle
$$

must approach one for a sequence of capacity codes. This fixes the squared-overlap convention in this explanation; taking its square root gives the same limiting requirement. The reference is not a resource supplied to the decoder. It records whether coherence was preserved through the complete communication procedure.

An exact recovery statement is stronger for the particular code and mask to which it applies: the induced logical channel is the identity, including on entangled inputs. But a capacity upper bound must control every sequence of possible codes, including approximate codes across many uses. The [model's capacity definition](../science/model.md#2-operational-capacity-and-normalization) and the coding theorem below connect these two levels of description.

### 4.2 Keep the mask in both outputs

For a fixed input state $\rho$, the receiver's output is a direct sum of distinguishable sectors:

$$
\mathcal E_\mu(\rho)=\bigoplus_S\mu(S)\rho_S.
$$

The direct-sum label is the classical record of which qubits arrived. A physical dilation can give the environment the same label and the complementary state $\rho_{S^c}$. Copying this classical label is compatible with quantum mechanics; the unknown input state itself is divided between the two outputs, not copied.

The entropy of a block-diagonal state is the entropy of its label plus the average entropy inside the labelled blocks. Applying that identity to both outputs gives

$$
I_c(\rho,\mathcal E_\mu)
=\sum_S\mu(S)\bigl[H(\rho_S)-H(\rho_{S^c})\bigr].
$$

The two Shannon terms $H(\mu)$ cancel. Losing the environment's flag would change the complementary channel and would generally give the wrong coherent information. The [explicit isometry](../science/model.md#a-complementary-channel-that-keeps-the-stochastic-flag) makes this accounting precise, including for entangled inputs.

### 4.3 Turn strong subadditivity into an overlap bound

The form of the entropy inequality used here follows from strong subadditivity and purification. Consider an arbitrary state on three systems $J,K,L$, and purify it with a system $R$. Strong subadditivity on $J,L,R$ says

$$
H(JL)+H(JR)\ge H(J)+H(JLR).
$$

Because the full state on $JKLR$ is pure, complementary subsystems have equal entropies: $H(JR)=H(KL)$ and $H(JLR)=H(K)$. Substitution yields weak monotonicity,

$$
H(JL)+H(KL)\ge H(J)+H(K).
$$

Now partition the physical positions into the overlap $I=S\cap T$, the two exclusive parts $J=S\setminus T$ and $K=T\setminus S$, and the part $L$ in neither set. Subadditivity bounds the receiver entropies by $2H(I)+H(J)+H(K)$. Weak monotonicity bounds the sum of the complementary entropies from below by $H(J)+H(K)$. The exclusive-part terms cancel, leaving

$$
\begin{aligned}
&H(\rho_S)-H(\rho_{S^c})
+H(\rho_T)-H(\rho_{T^c})\\
&\hspace{24mm}\le 2H(\rho_{S\cap T}).
\end{aligned}
$$

This applies to any state and any two retained sets. Neither set needs to be an authorized decoder for a chosen code. That generality is what makes the inequality useful for stochastic masks and unrestricted capacity. The [canonical proof](../science/model.md#3-a-two-set-entropy-inequality) includes empty sets and the subsequent averaging step.

### 4.4 A coupling is a comparison of two mask laws

A self-coupling pairs two possible masks while preserving each mask's probability distribution. Averaging the preceding inequality over such a pair produces twice the same coherent information on the left. The overlap entropy on the right is at most the logarithm of its Hilbert-space dimension. For qubit carriers,

$$
I_c(\rho,\mathcal E_\mu)
\le\mathbb E_\pi |S\cap T|.
$$

The pairing can therefore be chosen to make the expected overlap small. Its correlation is under the analyst's control; the physical channel law $\mu$ stays fixed.

For a complete small example, take one physical qubit with survival probability $3/4$. A valid joint distribution of two copies of its survival flag is

| First mask | Second: retained | Second: erased |
|---|---:|---:|
| Retained | 1/2 | 1/4 |
| Erased | 1/4 | 0 |

Each marginal retains the qubit with probability $3/4$. The intersection contains the qubit only in the first cell, so the expected overlap is $1/2$. No coupling can make that cell smaller: two events each of probability $3/4$ must intersect with probability at least $1/2$.

Independent pairing would instead give $9/16$. Both pairings describe the same individual channel law, but the first gives the tighter converse. For the maximally mixed input, the coherent information is $3/4-1/4=1/2$. The coding theorem and the multi-use converse therefore recover the familiar capacity of **one-half logical qubit per use**. This example illustrates the established erasure benchmark [BDS97], whose general formula is linked in [related work](../references/related-work.md).

### 4.5 Supply the operational capacity theorem

The required research-level supplement is **Devetak [D05], Proposition 7**, together with its coding-theorem development. In the [primary arXiv version](https://arxiv.org/pdf/quant-ph/0304127), Proposition 7 identifies ordinary quantum transmission, entanglement transmission, and entanglement generation capacities with regularized coherent information. The formula used here is

$$
Q(\mathcal N)
=\sup_{k\ge1}\frac1k\max_\rho
I_c(\rho,\mathcal N^{\otimes k}).
$$

This is an imported theorem with both achievability and converse content. The textbook's sections on entropy exchange and data processing supply foundations for understanding it; the proposition is the explicit proof dependency for this repository's capacity formula.

For each $k$, the project applies the two-set inequality to all $kn$ input carriers together and pairs the mask sequences with $\pi^{\otimes k}$. The input state remains arbitrary. Only the classical mask coupling is a product. The intersection's logarithmic dimension adds across blocks, giving

$$
\max_\rho I_c(\rho,\mathcal E_\mu^{\otimes k})
\le k\,C(\mu),
\qquad
C(\mu)=\min_{\pi\in\Pi(\mu,\mu)}
\mathbb E_\pi|S\cap T|.
$$

Substitution into the coding theorem proves $Q(\mathcal E_\mu)\le C(\mu)$. This is the step that covers encoders entangled across different blocks. Additivity of the classical transport cost does not require additivity of quantum capacity. The complete argument and its weak-converse scope are in [optimal overlap transport](../science/model.md#4-optimal-overlap-transport).

### 4.6 Connect exact storage codes to the capacity envelope

Independent pairing of two masks puts a given position in their intersection with probability $\alpha^2$ when every position has survival $\alpha$. This gives the upper rate $\alpha^2$. At the other end, the maximally mixed input has marginal entropy equal to the number of retained qubits, giving coherent information $n(2\alpha-1)$. Capacity is nonnegative, so every allowed law obeys

$$
(2\alpha-1)_+\le\frac{Q(\mathcal E_\mu)}n\le\alpha^2,
\qquad x_+=\max\{x,0\}.
$$

Independent erasures attain the lower endpoint. Establishing that the upper endpoint is a supremum needs a separate construction, not another entropy inequality.

**Sun–Jafar [SJ25, Theorem 6]** supplies that construction. Label nodes by the $m$-element subsets of $[\Delta]$; a star keeps the labels containing a selected element. Their exact storage code recovers $K=\binom{\Delta-2}{m-2}$ logical qudits from every star, using $N=\binom\Delta m$ physical qudits. Two different stars intersect in exactly $K$ nodes. A uniform distinct-star coupling therefore gives the capacity converse that matches this inherited encoder.

For $q=2^r$, replacing each physical qudit by its $r$ constituent qubits preserves the rate $K/N$ while counting every input qubit. As $\Delta$ grows and $m/\Delta$ approaches $\alpha$, this ratio approaches $\alpha^2$. The [extra-retention construction](../science/capacity-envelope.md#5-exact-prescribed-marginals-by-extra-retention) makes the individual survival probability exactly any prescribed real $\alpha$. The receiver uses a complete star contained in the observed mask, so the latent original star is not an extra communication resource.

The [capacity envelope](../science/capacity-envelope.md) owns these quantifiers and the field-size condition. The imported storage-code theorem is a genuine construction dependency; it is not implied just by knowing the CSS formalism. The resulting supremum permits a sequence of finite channels with growing input size. It does not assert a finite maximizer for every $\alpha$.

### 4.7 Read the geometric examples through the CSS framework

**Audoux–Couvreur [AC19, Section 4.1]** supplies the binary plane code and its logical representatives on every line. In the repository's notation, the nested binary spaces are $D\subseteq C$, with $\dim C-\dim D=1$. The complete stabilizer uses $X$ operators indexed by $D$ and $Z$ operators indexed by $C^\perp$. It has $n-1$ independent generators and therefore encodes exactly one qubit. Using only $X(D)$ and $Z(D)$ would leave extra logical degrees of freedom in the larger planes.

Each line supports representatives of both logical Pauli operators. Recovering both complementary observables gives access to the full logical qubit, including its phase coherence. The [geometry account](../science/geometry-and-loss.md#1-the-inherited-one-qubit-css-code) turns this algebra into an explicit decoder with $2q$ CNOTs on the retained line.

For the smallest plane, $q=2$, the code uses seven physical qubits and every line contains three. A uniform retained line transmits one logical qubit exactly, even though each physical qubit survives with probability only $3/7$. A coupling of distinct lines proves that one qubit is also the entire channel's capacity. This is a statement about the specified correlated loss law; independent losses at that same survival probability have zero capacity.

The two further examples change that law in different ways. A uniform normal vector, including the zero vector, produces pairwise independent survival flags. Its one- and two-site reduced channels agree with independent erasure only after the other outputs **and flags** are discarded. Higher-order correlations remain, and the full flag exposes them. Its capacity is bounded between $1$ and $1+2/q^2$, rather than determined exactly.

Independent thinning starts instead from a uniformly retained line and keeps each of its points with probability $t$. The entire line survives with probability $r=t^{q+1}$. Every proper subset is private for the chosen code because it is disjoint from another authorized line. After decoding, the code therefore realizes an ordinary logical erasure channel, giving a lower bound $(2r-1)_+$. A separate coupling of the actual observed masks supplies the matching upper bound for **all** encoders. The resulting exact capacity is

$$
Q(\mathcal E_{\mu_t})=[2t^{q+1}-1]_+.
$$

Recognizing a code's logical erasure behavior alone would establish only the lower bound. The [normalized coupling proof](../science/geometry-and-loss.md#4-uniform-line-channel-followed-by-independent-thinning) is what proves optimality, including zero capacity beyond the loss threshold. This family-specific fragility does not establish a universal fragility law for every channel approaching the envelope.

## 5. Reading routes

For the full conceptual story, use [M01–M12](milestones.md) to assemble the physical systems, flags, entropy tools, and coding framework, then [M13–M30](milestones.md) to connect the converse, achieving sequence, geometric examples, and their physical meaning. The map has exactly 30 project-defined targets; this bridge explains the connections between them rather than defining another sequence.

For a direct proof route, read [the model and overlap converse](../science/model.md), [the extremal capacities](../science/capacity-envelope.md), and [the geometric channel families](../science/geometry-and-loss.md), in that order. The [scientific entrypoint](../science/README.md) summarizes how those topics fit together.

For a construction route, begin with the complete CSS encoder and line decoder, then compare the three mask laws in the geometry account. Consult [verification](../verification/README.md) for finite-field, encoded-state, and transport checks. Those calculations validate specified finite cases and normalization; they do not numerically optimize unrestricted quantum capacity or replace the all-size proofs.

For a source audit, use [related work](../references/related-work.md) and [the bibliography](../references/references.bib). Devetak supplies the operational coding theorem, Sun–Jafar supplies the star codes, Audoux–Couvreur supplies the binary plane code, and Bennett–DiVincenzo–Smolin supplies the ordinary erasure benchmark. These primary research dependencies supplement the one educational anchor.

[Return to the learning route](README.md) · [Repository overview](../README.md).
