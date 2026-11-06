# Scientific reading route

The central question fixes what a local loss measurement would report: every physical qubit reaches the receiver with the same probability. It then asks how much the global pattern of losses can change quantum communication.

The sharp minimum rate is the familiar independent-erasure value. The sharp supremum is the square of the survival probability. Between those statements lies a capacity upper bound obtained by coupling two draws of the classical loss pattern and counting the quantum carriers they share.

## 1. Define the communication task

[Flagged subset erasure and the overlap converse](model.md) specifies the channel, its complementary output, the unassisted capacity convention, and the resource normalization. It derives the coherent-information expression and proves an input-uniform entropy inequality. The final part extends the bound to arbitrary encodings across independent blocks and shows that the transport quantity is exactly additive.

This is the authoritative home of the model and converse. A coupling compares classical mask distributions; it is not an operation that copies the transmitted quantum state.

## 2. Determine the full extremal range

[Exact extremal capacities](capacity-envelope.md) fixes the per-site survival constraint and proves both endpoints. A maximally mixed input gives the universal lower bound. The upper bound follows from independent coupling. The matching sequence imports Sun–Jafar's exact storage codes, identifies an entire family of exact stochastic capacities, counts every qubit in each finite-field share, and adjusts the mask law to any prescribed real survival probability.

The limiting construction separates two questions: the capacity of a fixed finite block channel, and the supremum over choices of finite block channels. The theorem concerns both in their stated order; it does not use an infinite physical block as one channel input.

## 3. Inspect explicit loss patterns

[Projective geometry and additional loss](geometry-and-loss.md) develops the binary Audoux–Couvreur code with its complete stabilizer and explicit decoder. It then treats three distinct laws: a uniformly retained line, a uniform normal vector, and a uniformly retained line followed by independent thinning.

The normal-vector example explains why one- and two-site channel summaries cannot fix global quantum capacity. The thinning example explains the fragility of one concrete high-loss construction: higher-order structure supports communication, and additional ordinary loss can remove it at an exactly calculable threshold. This is a family-specific conclusion.

## 4. Check dependencies and calculations

[Related work](../references/related-work.md) separates the inherited storage bounds, code constructions, and compound-channel results from the stochastic capacity statements. [Verification](../verification/README.md) gives the executable finite checks and their scope. The general theorems rely on the analytical proofs and the explicitly cited construction dependency, not on extrapolating numerical data.

## Physical interpretation

Local survival probabilities impose a sharp quadratic ceiling on unassisted quantum throughput, even when correlations are chosen optimally. Correlations can remove the independent-erasure zero-capacity region without restoring the linear throughput permitted by a fully protected fraction of positions under an average-only budget.

The result is an information-theoretic limit. Its achieving sequence may use large blocks, large finite-field shares, and elaborate nonlocal masks. The geometric family provides concrete smaller encoders and exact channel statements, while also exposing a precise sensitivity to extra independent losses.

[Return to the repository overview](../README.md).
