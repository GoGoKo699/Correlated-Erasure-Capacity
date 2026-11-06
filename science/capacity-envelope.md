# Exact extremal capacities at fixed single-carrier survival

Consider the unassisted, independently repeated block channel defined in [the model](model.md). Fix a common survival probability $\alpha$ for every physical input qubit, while allowing arbitrary correlations between erasures inside each finite block.

The extremal capacities, per physical input qubit, are

$$
\inf_{n,\mu}\frac{Q(\mathcal E_\mu)}n=(2\alpha-1)_+,
\qquad
\sup_{n,\mu}\frac{Q(\mathcal E_\mu)}n=\alpha^2.
\tag{1}
$$

Both optimizations impose $\Pr_\mu(i\in S)=\alpha$ at every coordinate. The infimum is attained by independent erasures. The supremum is approached by a sequence of finite channels built from the exact storage codes of Sun and Jafar. This statement does not assert that a finite maximizing block exists for every $\alpha$.

The [related-work record](../references/related-work.md) details the antecedents. In particular, the achieving storage codes below are inherited from Sun–Jafar; the use made of them here is an ordinary stochastic-channel capacity statement with a probability-sensitive converse.

## 1. Quantifiers and the universal interval

For each $n\ge1$, let

$$
\mathcal M_n(\alpha)=
\left\{\mu\text{ a probability law on }2^{[n]}:
\Pr_\mu(i\in S)=\alpha\ \text{for every }i\in[n]\right\}.
$$

Define

$$
\begin{aligned}
F_-(\alpha)&=\inf_{n\ge1}\ \inf_{\mu\in\mathcal M_n(\alpha)}
\frac{Q(\mathcal E_\mu)}n,\\
F_+(\alpha)&=\sup_{n\ge1}\ \sup_{\mu\in\mathcal M_n(\alpha)}
\frac{Q(\mathcal E_\mu)}n.
\end{aligned}
\tag{2}
$$

For every member of these families,

$$
(2\alpha-1)_+\le\frac{Q(\mathcal E_\mu)}n\le\alpha^2.
\tag{3}
$$

The upper bound is the independent-coupling consequence of the overlap converse in [model.md, Section 5](model.md#5-consequences-from-marginal-survival-probabilities).

For the lower bound, use the maximally mixed input $\tau=I_A/2^n$. Its marginal entropy is $H(\tau_S)=|S|$, so

$$
\begin{aligned}
I_c(\tau,\mathcal E_\mu)
 &=\mathbb E_\mu\bigl[|S|-|S^c|\bigr]\\
 &=2\sum_i\Pr_\mu(i\in S)-n\\
 &=n(2\alpha-1).
\end{aligned}
\tag{4}
$$

The quantum coding theorem gives $Q\ge I_c(\tau,\mathcal E_\mu)$, and capacity is nonnegative. No independence within a mask was used. Independent single-qubit erasures attain $(2\alpha-1)_+$, so

$$
F_-(\alpha)=(2\alpha-1)_+.
\tag{5}
$$

The familiar formula for the independent channel is due to [Bennett, DiVincenzo and Smolin](https://doi.org/10.1103/PhysRevLett.78.3217). It also follows from (4) and the antithetic coupling described in [model.md](model.md#5-consequences-from-marginal-survival-probabilities).

## 2. The exact storage-code input

Fix integers $\Delta\ge3$ and $2\le m\le\Delta-1$. Let

$$
\mathcal J=\binom{[\Delta]}m,
\qquad
N=\binom\Delta m,
\qquad
K=\binom{\Delta-2}{m-2},
\qquad
\delta=\binom{\Delta-2}{m-1}.
\tag{6}
$$

There is one physical node $A_J$ for each label $J\in\mathcal J$. Define the $\Delta$ authorized sets

$$
D_a=\{J\in\mathcal J:a\in J\},\qquad a\in[\Delta].
\tag{7}
$$

**Imported coding theorem.** Theorem 6 of [Sun and Jafar, *On the Capacity of Distributed Quantum Storage*, arXiv:2510.10568](https://arxiv.org/abs/2510.10568), with the construction in Section 5.7, supplies an encoding of $K$ logical $q$-dimensional systems into these $N$ nodes, one $q$-dimensional system per node, such that the entire logical state is recovered exactly from every $D_a$. One may choose a sufficiently large binary extension field $\mathbb F_q$, $q=2^r$.

For a concrete sufficient choice, take a power of two satisfying

$$
q>(K+\delta)+\Delta\delta.
\tag{8}
$$

This is the determinant-degree bound in the proof of that paper's Lemma 3. Keeping the expression in $K,\delta$ avoids the inconsistent binomial substitution printed there. The [source review](../references/related-work.md) records this detail. The coding theorem is the sole nontrivial construction dependency used in the argument below; it is not proved anew here.

## 3. Exact capacity of a random-star channel

Choose $a$ uniformly from $[\Delta]$, keep the nodes in $D_a$, and erase all other nodes. Denote this flagged channel by $\mathcal E_{\Delta,m}^{(q)}$. A retained set is resampled independently for each use of the entire channel. Every node has survival probability

$$
\alpha_0=\frac m\Delta,
\tag{9}
$$

because its label contains exactly $m$ of the $\Delta$ possible choices of $a$.

**Theorem.** For the dimensions in Section 2,

$$
Q\bigl(\mathcal E_{\Delta,m}^{(q)}\bigr)=K\log_2q.
\tag{10}
$$

**Achievability.** Use the imported storage encoder. The erasure mask identifies $D_a$, and its prescribed decoder recovers all $K$ logical systems exactly. Applying this code in each block achieves $K\log_2q$ qubits per channel use with zero error.

**Converse.** For distinct $a,b$,

$$
|D_a\cap D_b|=\binom{\Delta-2}{m-2}=K.
\tag{11}
$$

The law that chooses an ordered pair of distinct indices uniformly,

$$
\Pr(a,b)=\frac{1}{\Delta(\Delta-1)}\quad(a\ne b),
\tag{12}
$$

has both marginals uniform. It is therefore a self-coupling of the mask law with constant weighted intersection cost $K\log_2q$. The regularized overlap converse gives the matching upper bound in (10), even for encoders entangled across arbitrarily many channel uses. In fact the transport optimum itself equals $K\log_2q$: every pair of available masks has intersection size at least $K$, and (12) attains it. $\square$

The normalized exact capacity is

$$
\begin{aligned}
\frac{Q(\mathcal E_{\Delta,m}^{(q)})}{N\log_2q}
 &=\frac KN\\
 &=\frac{m(m-1)}{\Delta(\Delta-1)}\\
 &=\alpha_0^2-\frac{\alpha_0(1-\alpha_0)}{\Delta-1}.
\end{aligned}
\tag{13}
$$

The cases $m=1$ and $m=\Delta$ can be handled directly. At $m=1$ the available retained sets are disjoint singletons and capacity is zero. At $m=\Delta$ the channel retains its entire input and is an identity channel. They are unnecessary for the asymptotic construction below.

## 4. Conversion to an actual qubit erasure channel

A $q$-dimensional carrier with $q=2^r$ is exactly an $r$-qubit Hilbert space. Fix a local identification

$$
\mathbb C^{q}\cong(\mathbb C^2)^{\otimes r}
$$

at every physical node and every logical node. The channel in Section 3 is then a channel on

$$
n=Nr
\tag{14}
$$

physical input qubits. Each block of $r$ qubits belonging to node $J$ is retained or erased together. These within-node correlations are allowed in $\mathcal M_n(\alpha_0)$. The code transmits exactly $Kr$ logical qubits, and its rate remains $K/N$.

There is no dimensional rounding or uncounted local share size. The $r$ qubits in each node are all included in $n$. No independence of their loss flags is claimed. In particular, this conversion alone is not a construction with pairwise independent physical-qubit losses.

## 5. Exact prescribed marginals by extra retention

Fix an arbitrary real $\alpha\in(0,1)$. Choose $\Delta$ large enough that

$$
m=\lfloor\alpha\Delta\rfloor\ge2,
\qquad m\le\Delta-1,
\qquad \alpha_0=\frac m\Delta\le\alpha.
\tag{15}
$$

Start with the qubit channel of Section 4. After selecting its base star, independently for each erased node retain that entire node with probability

$$
\beta=\frac{\alpha-\alpha_0}{1-\alpha_0}.
\tag{16}
$$

All originally retained nodes remain retained. The final mask has some law $\widetilde\mu$ on the $Nr$ qubits. Every qubit now survives with probability

$$
\alpha_0+(1-\alpha_0)\beta=\alpha,
\tag{17}
$$

so $\widetilde\mu\in\mathcal M_{Nr}(\alpha)$ exactly, including when $\alpha$ is irrational.

The receiver is given only the final erasure mask. That mask always contains at least one complete star. The receiver can find any contained $D_a$—for example, the first such set in a fixed ordering—discard the additional nodes, and use the corresponding exact storage decoder. Each authorized decoder works for the same encoder. The original random choice of $a$ need not be revealed separately, and no side channel is assumed.

The same code therefore still transmits $Kr$ logical qubits exactly, giving

$$
\frac{Q(\mathcal E_{\widetilde\mu})}{Nr}
 \ge\frac KN
 =\frac{m(m-1)}{\Delta(\Delta-1)}.
\tag{18}
$$

Equation (18) is a lower bound for the channel after extra retention. We do not assert its exact capacity.

## 6. The supremal envelope

Let $\Delta\to\infty$ in (15), choosing a finite allowed $r$ separately for each pair $(\Delta,m)$. Then $m/\Delta\to\alpha$, so (18) implies

$$
F_+(\alpha)\ge
\lim_{\Delta\to\infty}
\frac{\lfloor\alpha\Delta\rfloor
      (\lfloor\alpha\Delta\rfloor-1)}
     {\Delta(\Delta-1)}
=\alpha^2.
\tag{19}
$$

The universal upper bound in (3) proves equality. At $\alpha=0$, every coordinate is erased almost surely, so $F_+(0)=0$. At $\alpha=1$, every coordinate is retained almost surely, so $F_+(1)=1$. We conclude

$$
\boxed{F_+(\alpha)=\alpha^2\quad\text{for every }\alpha\in[0,1].}
\tag{20}
$$

In explicit approximation form: for every $\alpha\in(0,1)$ and every $\varepsilon>0$, there is a finite number $n$ of physical qubits and a law $\mu\in\mathcal M_n(\alpha)$ with an exact code of rate greater than $\alpha^2-\varepsilon$. Indeed, the deficit of the construction is bounded by

$$
\alpha^2-\frac{m(m-1)}{\Delta(\Delta-1)}
\le\frac{2}{\Delta}+\frac{1}{4(\Delta-1)},
\tag{21}
$$

since $0\le\alpha-\alpha_0<1/\Delta$ and $\alpha_0(1-\alpha_0)\le1/4$. Every channel and code in this sequence is finite; the supremum permits their sizes to grow.

## 7. What the extremal statement establishes

At any $0<\alpha\le1/2$, independent erasures have zero ordinary quantum capacity, while other erasure laws with the same single-qubit survival probability have rates approaching $\alpha^2>0$. At $1/2<\alpha<1$, the maximal possible improvement over the independent-erasure benchmark, understood as a supremum over finite blocks, is

$$
\alpha^2-(2\alpha-1)=(1-\alpha)^2.
$$

Thus single-carrier survival probabilities give sharp extremal bounds but do not specify a unique capacity. The law of the joint mask remains operationally relevant.

This is an information-theoretic statement with explicit resource accounting. The number of nodes $N=\binom\Delta m$ and the field size needed by the inherited construction can be large. No efficient encoder, small-block approximation guarantee, or finite-block attainment of the supremum is claimed here. The smaller binary geometric constructions and their separate local-diagnostic and loss-robustness statements appear in [geometry-and-loss.md](geometry-and-loss.md).
