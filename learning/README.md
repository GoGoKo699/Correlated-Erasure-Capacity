# Learning the correlated-erasure problem

The learning route begins with labelled qubits that may arrive or be erased. It develops the distinction between an individual survival probability and the complete pattern of losses, then explains how that pattern constrains quantum communication.

The single educational anchor is **Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition, Cambridge University Press, 2010**. The [anchor and bridge](anchor-and-bridge.md) provides verified section locators, notation, and the additional steps needed for this project's proofs. The [30-milestone map](milestones.md) gives the common understanding route.

## The two-phase story

The **12 background/preliminaries milestones, M01–M12**, move from individual quantum systems to the complete communication task: subsystems, erasure flags, preservation of a reference, entropy inequalities, coding, and physical-resource accounting. Their final synthesis identifies precisely what is fixed, what is optimized, and what counts as successful transmission.

The **18 narrative/innovation milestones, M13–M30**, connect the two-mask inequality to a regularized capacity converse, determine the extremal interval, and explain the imported codes that approach its upper endpoint. The geometric examples then separate exact recovery, pairwise local agreement, and fragility under additional loss. The final synthesis brings the claims, limitations, source dependencies, and finite verification together.

This allocation follows the project's argument: a compact quantum-information foundation supports a longer chain linking entropy, mask probabilities, coding constructions, and physical interpretation. The map records central questions, understanding targets, dependencies, conceptual connections, and source pointers. Detailed lemmas and complete proofs remain in their scientific topic pages.

## Choose a reading route

| Purpose | Start here | Continue with |
|---|---|---|
| Understand the complete story | [Milestone map](milestones.md) | [Anchor and bridge](anchor-and-bridge.md), consulted alongside the relevant milestones |
| Translate textbook foundations into the present model | [Section map and notation](anchor-and-bridge.md#2-the-route-from-the-textbook-to-this-project) | [The missing connections](anchor-and-bridge.md#4-the-additional-steps-supplied-by-this-project) |
| Inspect the main converse and its quantifiers | [Model and overlap converse](../science/model.md) | [Exact extremal capacities](../science/capacity-envelope.md) |
| Understand an explicit encoder and loss threshold | [Projective geometry and additional loss](../science/geometry-and-loss.md) | [Verification guide](../verification/README.md) |
| Check attribution and imported results | [Related work](../references/related-work.md) | [Structured bibliography](../references/references.bib) |

The textbook's channel, fidelity, CSS/stabilizer, and entropy sections supply the foundation. The bridge explicitly supplements them with Devetak's regularized coding theorem and the Sun–Jafar and Audoux–Couvreur constructions. These papers are research dependencies within the same route.

## Connections that organize the results

A mask specifies which physical qubits remain; a decoder extracts a logical state from them. A rate counts logical qubits per complete channel use, and its normalized version charges every physical input qubit. Exact recovery by a particular code supplies an achievable rate. The overlap converse controls arbitrary encoders, including ones entangled across many independently repeated blocks.

The distinction between those roles explains the main result. Independent erasures attain the lowest possible rate at fixed common survival probability. The best correlated laws approach a quadratic upper endpoint. The latter is a supremum over finite channels, while the star and thinned-line formulas evaluate the capacities of specified finite channel families.

The three geometric loss laws remain separate throughout the route. Uniform lines have capacity exactly one qubit per block. Normal-vector masks have pairwise independent local flags and a bounded capacity interval. Uniform lines followed by independent thinning have an exact capacity curve. Their recovery geometry is shared, but their probability laws and conclusions differ.

The [finite checks](../verification/README.md) confirm incidence identities, encoded recovery, and coupling calculations in documented cases. The general conclusions depend on the analytical arguments and attributed construction theorems. The [scientific reading route](../science/README.md) provides direct access to those authoritative accounts.

[Repository overview](../README.md) · [Reader and retrieval guide](../llms.txt).
