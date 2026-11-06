# Flagged subset erasure and the overlap converse

This document fixes the communication model and proves the probability-sensitive upper bound used in [the capacity envelope](capacity-envelope.md) and [the geometric examples](geometry-and-loss.md). All logarithms and entropies use base two. The [related-work record](../references/related-work.md) identifies the coding-theorem and entropy-bound antecedents.

## 1. One channel use is a finite block

Let $`[n]=\{1,\ldots,n\}`$ and

```math
\mathcal H_A=\bigotimes_{i=1}^n\mathcal H_{A_i},
\qquad d_i=\dim\mathcal H_{A_i}<\infty,
\qquad w_i=\log_2 d_i.
```

A probability law $`\mu`$ on $`2^{[n]}`$ specifies the retained set $`S`$. The draw of $`S`$ is independent of the input state. The receiver obtains the retained tensor factors, with their original labels, and the complete erasure mask. Thus

```math
\mathcal E_\mu(\rho)
 =\bigoplus_{S\subseteq[n]}\mu(S)\rho_S,
\qquad
\rho_S=\mathrm{Tr}_{S^c}\rho.
\qquad\text{(1)}
```

Here the direct sum records the classical flag $`S`$. The empty tensor factor is a one-dimensional system. An equivalent realization puts a distinguished erasure symbol at every missing position. The flag is input-independent and is part of the channel output; it is not a message sent by the encoder.

The sender knows $`\mu`$ but does not know the realized mask. Correlations between positions inside a block are unrestricted. Repeated uses of this fixed channel have the product law $`\mu^{\otimes k}`$, so masks are independent between blocks. The results below concern this memoryless block channel. They do not assume independent losses within a block, and they do not assert a capacity formula for a general process with memory between blocks.

### A complementary channel that keeps the stochastic flag

For each $`S`$, let $`U_S`$ be the canonical rearrangement of input factors into a receiver register $`B_S\cong A_S`$ and an environment register $`E_{S^c}\cong A_{S^c}`$. On the corresponding orthogonal direct-sum sectors, define the isometry

```math
V|\psi\rangle
 =\sum_S\sqrt{\mu(S)}\,
 |S\rangle_{F_B}|S\rangle_{F_E}
 U_S|\psi\rangle_{B_S E_{S^c}}.
\qquad\text{(2)}
```

The expression is linear on entangled input vectors; $`U_S`$ only relocates tensor factors. Orthogonality of the flags and $`\sum_S\mu(S)=1`$ imply $`V^\dagger V=I_A`$. Tracing the environment gives (1). Tracing the receiver gives the complementary channel

```math
\mathcal E_\mu^c(\rho)
 =\bigoplus_S\mu(S)\rho_{S^c}.
\qquad\text{(3)}
```

Both parties' flags are copies of the same classical random variable. The environment flag must be retained when computing coherent information. In particular, the randomness in the mask is not itself secret from the environment.

For a state $`\rho`$ on the full input block, the direct-sum entropy formula gives

```math
\begin{aligned}
H(\mathcal E_\mu(\rho))
 &=H(\mu)+\sum_S\mu(S)H(\rho_S),\\
H(\mathcal E_\mu^c(\rho))
 &=H(\mu)+\sum_S\mu(S)H(\rho_{S^c}).
\end{aligned}
```

Consequently,

```math
I_c(\rho,\mathcal E_\mu)
 =\sum_S\mu(S)\bigl[H(\rho_S)-H(\rho_{S^c})\bigr].
\qquad\text{(4)}
```

The Shannon terms cancel. No assumption on correlations or purity of $`\rho`$ is used.

## 2. Operational capacity and normalization

$`Q(\mathcal E_\mu)`$ denotes ordinary, unassisted quantum capacity, in logical qubits per use of the entire $`n`$-carrier block. For $`k`$ channel uses, an encoder maps a logical system of dimension $`D_k`$ into $`A^{\otimes k}`$, and a decoder acts on the complete output, including its masks. Encoding may couple all carriers and all $`k`$ blocks. The entanglement-transmission error must tend to zero as $`k\to\infty`$; an achievable rate is the corresponding asymptotic value of $`k^{-1}\log_2 D_k`$. There is no preshared entanglement, classical feedback, or supplementary communication resource.

For qubit carriers, capacity per input qubit is $`Q(\mathcal E_\mu)/n`$. For heterogeneous carrier dimensions, the total input size in qubits is $`W=\sum_i w_i`$, and $`Q/W`$ is the corresponding normalized rate. The normalization always counts the entire input block, including the carriers subsequently erased.

We use the standard regularized coherent-information characterization,

```math
Q(\mathcal N)
 =\sup_{k\ge1}\frac1k\max_{\rho_{A^{\otimes k}}}
 I_c(\rho,\mathcal N^{\otimes k}).
\qquad\text{(5)}
```

This is the quantum coding theorem, not an additional assumption on allowed encoders. It characterizes the operational, vanishing-error capacity just defined. See [Devetak, *The private classical capacity and quantum capacity of a quantum channel*](https://arxiv.org/abs/quant-ph/0304127), IEEE Transactions on Information Theory **51**, 44–55 (2005), and the foundational references in [related work](../references/related-work.md).

## 3. A two-set entropy inequality

**Lemma.** For every state $`\rho`$ on $`A`$ and every pair of retained sets $`S,T\subseteq[n]`$,

```math
\begin{aligned}
& H(\rho_S)-H(\rho_{S^c})
 +H(\rho_T)-H(\rho_{T^c})\\
&\hspace{35mm}\le 2H(\rho_{S\cap T}).
\end{aligned}
\qquad\text{(6)}
```

**Proof.** Partition the input coordinates into disjoint sets

```math
I=S\cap T,\qquad J=S\setminus T,\qquad
K=T\setminus S,\qquad L=(S\cup T)^c.
```

In this proof, $`H(X)`$ means the entropy of the indicated marginal of $`\rho`$. Subadditivity gives

```math
H(IJ)+H(IK)\le 2H(I)+H(J)+H(K).
\qquad\text{(7)}
```

Weak monotonicity, applied to the reduced state on $`JKL`$, gives

```math
H(JL)+H(KL)\ge H(J)+H(K).
\qquad\text{(8)}
```

Subtract (8) from (7) and use $`S^c=KL`$ and $`T^c=JL`$. This proves (6), including empty parts. $`\square`$

The inequality does not require that either set support an exact decoder. That is the property needed for probabilistic erasure patterns and arbitrary channel inputs.

## 4. Optimal overlap transport

A self-coupling of $`\mu`$ is a probability law $`\pi`$ on ordered pairs $`(S,T)`$ with both marginals equal to $`\mu`$:

```math
\Pi(\mu,\mu)=
\left\{\pi\ge0:
\sum_T\pi(S,T)=\mu(S),\quad
\sum_S\pi(S,T)=\mu(T)\right\}.
```

For a set $`U`$, write $`w(U)=\sum_{i\in U}w_i`$. Define

```math
C_\cap(\mu;w)
 =\min_{\pi\in\Pi(\mu,\mu)}
   \mathbb E_\pi\,w(S\cap T).
\qquad\text{(9)}
```

The minimum exists because this is a finite linear program over a nonempty compact polytope. For qubit carriers we abbreviate

```math
C(\mu)=C_\cap(\mu;\mathbf 1).
```

A coupling is a mathematical comparison of two mask draws. It does not copy a quantum state or introduce another channel resource. Independent draws give one feasible coupling, but the minimizing coupling may be strongly correlated.

**Theorem (overlap converse).** For the channel in (1),

```math
Q(\mathcal E_\mu)\le C_\cap(\mu;w).
\qquad\text{(10)}
```

**Proof for one input block.** Average (6) over an arbitrary self-coupling $`\pi`$. Both marginals are $`\mu`$, so (4) implies

```math
\begin{aligned}
I_c(\rho,\mathcal E_\mu)
 &\le\mathbb E_\pi H(\rho_{S\cap T})\\
 &\le\mathbb E_\pi\log_2\dim\mathcal H_{A_{S\cap T}}\\
 &=\mathbb E_\pi w(S\cap T).
\end{aligned}
\qquad\text{(11)}
```

This holds for every $`\rho`$ and every $`\pi`$.

**Arbitrarily many input blocks.** Fix $`k`$ and any state on all $`kn`$ input carriers, allowing entanglement between different blocks. Apply the same two-set inequality to this full tensor product, and couple the two sequences of masks using $`\pi^{\otimes k}`$. The entropy of the retained intersection is at most its log dimension, which is the sum of the weights of its carriers. Therefore

```math
\max_\rho I_c(\rho,\mathcal E_\mu^{\otimes k})
 \le k\,\mathbb E_\pi w(S\cap T).
\qquad\text{(12)}
```

Choose a minimizing coupling and insert (12) into (5). This proves (10). $`\square`$

Equation (12) is not restricted to product input states or separate encoders. The standard capacity theorem supplies the operational converse for every sequence of codes whose error vanishes. We make no strong-converse claim, no assertion that error tends to one above (10), and no separate finite-error rate bound.

### Exact additivity of the transport quantity

If $`\mu`$ and $`\nu`$ are mask laws on disjoint carrier blocks, and the cost is the sum of their carrier weights, then

```math
C_\cap(\mu\otimes\nu;w\oplus v)
 =C_\cap(\mu;w)+C_\cap(\nu;v).
\qquad\text{(13)}
```

For the upper bound, take the product of two minimizing self-couplings. For the lower bound, take any self-coupling of $`\mu\otimes\nu`$. Its projection onto the pair of masks from the first block is a self-coupling of $`\mu`$, and its projection onto the second pair is a self-coupling of $`\nu`$. Expected intersection cost is the sum of the two projected costs, each at least its own minimum. This proves (13).

This is additivity of the computable upper bound. It is not a claim that quantum capacity is additive, or that (10) is an equality for every loss law.

## 5. Consequences from marginal survival probabilities

Let

```math
\alpha_i=\Pr_\mu(i\in S).
```

Under the independent self-coupling $`\pi=\mu\otimes\mu`$, a fixed coordinate belongs to $`S\cap T`$ with probability $`\alpha_i^2`$. Hence

```math
Q(\mathcal E_\mu)\le\sum_{i=1}^n\alpha_i^2\log_2d_i.
\qquad\text{(14)}
```

For $`n`$ qubits with the same survival probability $`\alpha`$ at every position, this is

```math
\frac{Q(\mathcal E_\mu)}n\le\alpha^2.
\qquad\text{(15)}
```

The common-marginal requirement in (15) matters. Knowledge of only the average survival probability does not justify replacing the sum of squares in (14) by the square of that average.

As a consistency check, suppose $`\mu`$ is itself a product of independent single-carrier erasure laws. Couple each pair of single-carrier flags so that their joint survival probability is $`(2\alpha_i-1)_+`$, where $`x_+=\max\{x,0\}`$. The product of these couplings is feasible, and yields

```math
C_\cap(\mu;w)=\sum_i(2\alpha_i-1)_+w_i.
\qquad\text{(16)}
```

For the reverse inequality in (16), any coupling has joint survival probability at least $`(2\alpha_i-1)_+`$ at coordinate $`i`$, by the elementary union bound. Thus (16) is exact. Together with independent coding on the useful carriers, it recovers the usual erasure-channel capacity. This benchmark is established work; see [Bennett, DiVincenzo and Smolin (1997)](https://doi.org/10.1103/PhysRevLett.78.3217) and [related work](../references/related-work.md).
