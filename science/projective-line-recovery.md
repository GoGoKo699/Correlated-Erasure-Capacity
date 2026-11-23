# Recovery cost and capacity for filtered projective-line erasures

Take the [binary one-qubit CSS code of Audoux and Couvreur](geometry-and-loss.md#1-the-inherited-one-qubit-css-code) on the $`n=q^2+q+1`$ points of $`\mathrm{PG}(2,q)`$, where $`q`$ is a power of two and $`q\ge 2`$. The physical channel chooses one projective line uniformly, retains each of its $`q+1`$ points independently with probability $`t`$, and flags the final surviving set. Blocks are independent. Only surviving sites and their internal couplers are available for the installed-graph calculation. Each CNOT costs one, and the receiver uses the flag to choose a surviving output. Single-qubit stabilizer operations and classical feedforward are free, following the [companion compiler's resource model](https://github.com/GoGoKo699/Quantum-Erasure-Recovery-Compiler/blob/b960d290edd538ce18b7b0ecd04efddea4907539/science/model.md).

## Exact extraction from a known line

Both logical Pauli axes have representatives supported on each complete line $`L`$. For any $`x\in L`$, choose a second line $`M`$ through $`x`$ with $`M\cap L=\{x\}`$. A code stabilizer supported on $`L`$ must commute with both logical axes on $`M`$. Both tests act locally at $`x`$, forcing that stabilizer to be the identity there. This holds for each $`x\in L`$. Thus the restriction to the untouched reference $`R`$ is injective on the reduced Choi stabilizer group of $`R\cup L`$. The group already contains $`X_R X(L)`$ and $`Z_R Z(L)`$, so those two operators generate it. Every admissible pair of independent reference axes anticommutes at exactly the points of $`L`$.

The [compiler theorem](https://github.com/GoGoKo699/Quantum-Erasure-Recovery-Compiler/blob/b960d290edd538ce18b7b0ecd04efddea4907539/science/theorem.md) gives the exact cost at any available output $`o`$ as $`\tau_G(L\triangle\{o\})`$. Here $`G`$ is the graph actually available after erasure and $`\tau_G(T)`$ is the minimum weight of an edge set with odd-degree set $`T`$, with cost $`+\infty`$ when none exists. The lower bound holds on each successful branch of an exact heralded recovery. On unit-cost complete survivor hardware, $`q/2`$ CNOTs are necessary and sufficient for any $`o\in L`$. At this cap more generally, $`G[L]`$ must contain a matching that covers the other $`q`$ points. A join needs at least one edge incidence per terminal and the $`q/2`$ edges supply exactly $`q`$ incidences. Each terminal has degree one, and every other vertex has degree zero.

Apply the matching CNOTs in one layer. On each pair $`(a,b)`$, the CNOT $`a\to b`$ maps $`X_aX_b`$ to $`X_a`$ and $`Z_aZ_b`$ to $`Z_b`$. Measure $`X_a`$ and $`Z_b`$. The products of the respective signs determine the signs of $`X_RX_o`$ and $`Z_RZ_o`$, so a Pauli on $`o`$ restores the Bell state with $`R`$. The recovery therefore preserves an arbitrary reference. This is the pairwise Bell measurement used to unlock generalized Smolin states. The compiler gives its exact optimality and the graph-dependent cost. The [companion benchmark](https://github.com/GoGoKo699/Quantum-Erasure-Recovery-Compiler/blob/main/science/benchmarks.md#projective-line-recovery) gives implementation details.

Every proper subset of $`L`$ is private for this encoder. A second line through a missing point meets $`L`$ only at that point and can recover perfectly. The retained subset is therefore decoupled from the reference, including after conditioning on any local measurement outcome of nonzero probability. Its exact extraction probability is zero.

## Sharp installed-coupler curve

With at most $`H`$ installed unit-cost couplers among the $`n`$ points, the maximum number of full lines that can be served at a cap of $`q/2`$ executed CNOTs is

```math
m(H)=\min\{n,\lfloor 2H/q\rfloor\}.
```

Every installed edge has two distinct endpoints, which lie on one and only one projective line. Each successful line needs at least $`q/2`$ internal edges, all charged exclusively to that line. To attain the bound, choose any $`m(H)`$ lines and install a matching on each, leaving one point for the output. The matchings use disjoint edge sets. Since the internal-edge lower bound holds for any feasible join, $`m(H)`$ also holds for a larger cap at fixed $`H`$. A cap below $`q/2`$ serves zero lines.

All-line delivery needs $`nq/2`$ installed couplers. It can use a $`q`$-regular physical graph. A perfect matching exists in the regular point–line incidence bipartite graph and assigns a distinct output point to each line. Pair all other points on each line. Each point belongs to $`q+1`$ lines and is unmatched once, so its final degree is $`q`$.

## Exact capacity with an explicit mask filter

For a chosen graph, let $`m`$ be the number of budget-feasible full lines and set $`p=t^{q+1}m/n`$. The filter retains the physical qubits and the flag on each accepted full line and replaces every other output with an erasure flagged by the empty mask. Independent uses of the filtered physical channel have mass $`1-p`$ on the empty mask and equal mass $`t^{q+1}/n`$ on each accepted full line. Its unassisted quantum capacity is

```math
Q(\mathcal E_{\mathrm{filtered}})=[2p-1]_+.
```

The rate is in qubits per entire physical block. Maximizing over graphs with at most $`H`$ installed couplers gives the formula with $`m=m(H)`$.

For achievability, use the projective encoder and recover from each budget-feasible full line. The extracted qubit and the erasure flag realize a memoryless qubit erasure channel of survival $`p`$. The receiver learns the selected output address from the mask and knows where each accepted logical qubit is for outer erasure decoding. The per-block budget charges the postloss extraction gates. Outer coding operations and transport to a single fixed physical port are separate resources.

For the converse, apply the [overlap bound](model.md#4-optimal-overlap-transport) to the *filtered physical mask law*. When $`p=0`$, the mask is always empty. For $`0\lt p\le 1/2`$, pair a uniform accepted line with empty in both directions, for mass $`p`$ in each direction. Pair the remaining empty mass $`1-2p`$ with itself. Every overlap is zero. For $`p>1/2`$, couple the empty mass $`1-p`$ with a uniform accepted line in both directions. Couple the residual mass $`2p-1`$ uniformly over ordered pairs of distinct accepted lines. There are at least two accepted lines since each has probability at most $`1/n`$. Each pair of distinct lines meets in one point and gives overlap one. Both marginal laws are unchanged, so the expected overlap is $`2p-1`$. These couplings are optimal, since the probability of two full lines in any self-coupling is at least $`[2p-1]_+`$ and their intersection is nonempty. The converse holds for arbitrary inputs and coding across independent filtered physical blocks. It relies on the explicit discard interface. Keeping rejected quantum outputs for joint processing with an unrestricted decoder is a separate channel.

For $`q=2`$ there are seven lines and the gate cap is one. Install one coupler on each of four distinct lines. With $`t=1`$ this gives $`p=4/7`$ and $`Q=1/7`$ qubit per physical block. At three couplers or fewer the acceptance probability is at most $`3/7`$. Seven couplers suffice to serve all lines. See the [verification guide](../verification/README.md) for finite checks.

## Boundary checks and attribution

If a designated output was erased, using its position requires a replacement site and retained couplers. On unit-cost complete hardware with such a replacement, the same T-join formula gives $`q/2+1`$ when the output lies off the line and $`q/2`$ when it lies on the line. With a fixed output and cap $`q/2`$, at most a fraction $`(q+1)/n<1/2`$ of the lines can be accepted, giving zero filtered capacity. The installed-graph optimum above uses flag-selected outputs and removes erased positions. The normal-vector law includes an all-points mask and requires a separate calculation.

- Audoux and Couvreur, *On tensor products of CSS codes*, 2019, §4.1, Definition 4.9 and Lemma 4.11, supplies the CSS code and its complete-line logical Paulis. [Primary paper](https://numdam.org/item/10.4171/aihpd/71.pdf)
- Wang and Ying, *Multipartite unlockable bound entanglement in the stabilizer formalism*, 2007, Example 2, supplies the generalized Smolin state and Bell-pair unlocking. The capacity repository's `2q` circuit remains a coherent construction, with its own resources. [Primary paper](https://arxiv.org/abs/quant-ph/0703033)
- Bennett, DiVincenzo and Smolin, *Capacities of Quantum Erasure Channels*, 1997, Eq. (2), supplies the ordinary outer erasure-channel formula. [Primary paper](https://arxiv.org/abs/quant-ph/9701015)
- The joint result uses the line geometry and [overlap converse](model.md) from Correlated Erasure Capacity and the exact weighted [T-join theorem](https://github.com/GoGoKo699/Quantum-Erasure-Recovery-Compiler/blob/b960d290edd538ce18b7b0ecd04efddea4907539/science/theorem.md) from Quantum Erasure Recovery Compiler. The complete-line reduction, installed-graph bound and filtered capacity combine these results.
