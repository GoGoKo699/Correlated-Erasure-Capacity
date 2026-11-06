# Correlated Erasure Capacity

How much quantum information can survive loss if every physical qubit has the same probability of reaching the receiver, but the losses can be correlated?

For survival probability $\alpha$, the exact extremal rates are

$$
\inf_{n,\mu}\frac{Q(\mathcal E_\mu)}{n}=(2\alpha-1)_+,
\qquad
\sup_{n,\mu}\frac{Q(\mathcal E_\mu)}{n}=\alpha^2,
\qquad 0\leq\alpha\leq1.
$$

Both optimizations require every one of the $n$ physical qubits to survive with probability $\alpha$. The channel draws an input-independent survivor set from a known law $\mu$, returns those qubits and their erasure flags, and resamples independently on each use of the entire block. Quantum capacity is unassisted: the sender has no realized-mask knowledge, feedback, or preshared entanglement. Encoding may entangle arbitrarily many blocks.

Independent erasures attain the lower endpoint. Correlated constructions approach the upper endpoint as their block sizes grow. Thus correlations can support quantum communication at arbitrarily small survival probabilities, while the best possible rate remains quadratic in survival. The attaining storage codes are due to Sun and Jafar; the stochastic capacity converse and its consequences are developed here with the inherited ingredients explicitly attributed.

## The overlap converse

A self-coupling $\pi$ of $\mu$ is a joint distribution of two survivor sets $S,T$, each individually distributed as $\mu$. Define

$$
C(\mu)=\min_{\pi\in\Pi(\mu,\mu)}\mathbb E_\pi|S\cap T|.
$$

The general capacity bound is

$$
Q(\mathcal E_\mu)\leq C(\mu)\leq\sum_{i=1}^{n}\Pr_\mu(i\in S)^2.
$$

Its proof is an entropy inequality valid for every channel input. Applying it to two coupled sequences of masks bounds inputs entangled across any number of channel uses. The transport quantity itself is additive on independent blocks; this does not assume additivity of quantum capacity.

Read the [precise model and converse](science/model.md), then the [sharp capacity envelope and achieving construction](science/capacity-envelope.md).

## Explicit geometric channels

The binary projective-plane code of Audoux and Couvreur supplies a smaller family of examples. For a power of two $q$, put one qubit at each of the $q^2+q+1$ projective points. Every complete line recovers the encoded qubit. Three loss laws give different operational conclusions:

| Loss law | Quantum capacity per block | Main consequence |
|---|---|---|
| Uniformly retained projective line | Exactly one qubit | An exact stochastic capacity from a known recovery geometry. |
| Zero set of a uniform normal vector, including zero | Between 1 and 1 + 2/q² qubits | Pairwise independent local erasures coexist with nearly optimal high-loss transmission. |
| Uniform line, then independent retention with probability t | Exactly max{0, 2t^(q+1) - 1} qubits | A complete capacity curve and a sharp additional-loss threshold. |

For the normal-vector law, the local survival probability is $\alpha=1/q$, and the achievable rate is

$$
\frac{1}{q^2+q+1}=\frac{\alpha^2}{1+\alpha+\alpha^2}.
$$

Every one- and two-carrier reduced channel equals independent erasure noise when only those carriers and their local flags are retained. The full flag record exposes the higher-order correlations.

For the thinned uniform-line law, additional independent loss with probability $\eta=1-t$ destroys all capacity at

$$
\eta_c=1-2^{-1/(q+1)}.
$$

The [geometry and loss account](science/geometry-and-loss.md) gives the full one-qubit CSS encoder, a decoder using $2q$ CNOTs on the retained line, the capacity proofs, and the normalized couplings. The thinning formula applies to uniform-line selection, not to the normal-vector mixture.

## Learn the project

The single educational anchor is **Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (Cambridge University Press, 2010)**. The [source bridge](learning/anchor-and-bridge.md) connects its treatment of channels, error correction, stabilizers, and entropy to this project's stochastic capacity arguments. It identifies the further research ingredients and explains how their assumptions enter the proofs.

The [30-milestone map](learning/milestones.md) develops the background and then assembles the scientific argument, from individual erasures to the sharp rate envelope and its geometric examples. Each milestone gives an understanding target, earlier dependencies, conceptual connections, and source pointers. Start with the [learning route](learning/README.md), or use the direct scientific routes below to inspect a particular result.

## Read and reproduce

- [Scientific reading route](science/README.md): the question, model, proof dependencies, and physical interpretation.
- [Related work](references/related-work.md) and [bibliography](references/references.bib): source-level attribution and the scope of the comparison.
- [Verification guide](verification/README.md): exact geometry checks, encoded-state checks, and unrestricted optimal-transport calculations.
- [Reader and retrieval guide](llms.txt): where to find a particular definition, theorem, or calculation.

From the repository root, run:

```bash
python verification/verify_geometry.py --output /tmp/geometry-results.json
```

Python, NumPy, and SciPy are required; versions and tested cases are documented in the verification guide. The recorded calculations check geometry through 273 physical qubits, full seven-qubit recovery, and transport optimizations on the observed mask distributions. Finite calculations support the analytical arguments; they do not compute unrestricted quantum capacity numerically.

## Scope

The extremal law permits arbitrary within-block correlations and growing block sizes. Every input qubit is counted, including all qubits in a larger coding share. The cost of engineering the loss correlations is not optimized. Equal survival at every site is essential: an average-only survival budget can concentrate transmission on protected positions and permit linear rates. The supremum need not be attained by a finite channel, and the overlap bound is not claimed to equal capacity for every mask law.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
