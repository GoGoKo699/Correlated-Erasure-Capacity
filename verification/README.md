# Geometry and transport verification

Run from the repository root:

```bash
python verification/verify_geometry.py
```

The script requires Python 3.10 or newer, NumPy, and SciPy. The recorded run used Python 3.12.14, NumPy 2.3.5, and SciPy 1.17.0. No random sampling or seed is used. The script writes [results.json](results.json), including its source SHA-256, package versions, checks, and numerical residuals. To preserve the recorded file while reproducing the run, choose another output path:

```bash
python verification/verify_geometry.py --output /tmp/geometry-results.json
```

## What is checked

- **Exact integer geometry, for q = 2, 4, 8, 16:** projective point and line counts, incidence degrees, one-point intersections, and binary line-difference spaces.
- **The complete one-qubit CSS code:** the X stabilizers come from the line-difference space, and the Z stabilizers from the orthogonal complement of the full line span. Their combined rank is one less than the number of physical qubits. This distinguishes the encoder used in the proofs from the larger code that would result from using the difference space for both stabilizer types.
- **Logical operators and decoding:** every line supplies the same logical Pauli pair, and the two sequences of CNOTs have the required binary action. For q = 2, a full encoded Bell-state calculation checks all seven retained-line decoders and reference decoupling for all 29 distinct proper masks.
- **Normal-vector flags:** exact counts establish the one- and two-point survival probabilities. Collinear and noncollinear triples give different higher-order statistics.
- **Unrestricted transport optimization:** SciPy's HiGHS solver minimizes the overlap cost over all self-couplings of the *observed* mask law. The mask probabilities are generated directly from line selection and independent thinning, with repeated empty and singleton masks aggregated before optimization. The LP is not restricted to the couplings used in the analytical proof.

The transport checks include eight q = 2 thinning cases: complete loss, complete retention, intermediate losses, and points below, at, and above the analytic threshold. Two q = 4 cases lie on opposite sides of the threshold. The q = 4 problems have 568 observed masks and 322,624 nonnegative transport variables. The script also solves the normal-vector overlap problem for q = 2 and q = 4.

For each LP, the output records normalization, both marginal residuals, nonnegativity, dual feasibility, the primal–dual gap, and agreement with the analytical overlap cost. The acceptance tolerance is 1e-8; the solver's primal and dual feasibility tolerances are 1e-9.

## Recorded results

The run recorded in [results.json](results.json) passed all checks. The largest discrepancy between an LP optimum and its analytical prediction was **8.89e-16** after rounding upward. For example:

| Field order | Additional retention | Observed masks | Minimum expected overlap |
|---|---:|---:|---:|
| 2 | 0.90 | 36 | 0.4580000000000003 |
| 4 | 0.75 | 568 | 0 |
| 4 | 0.95 | 568 | 0.5475618749999986 |

All seven q = 2 decoded Bell fidelities were 0.9999999999999997 in floating-point arithmetic. The largest reference-decoupling Frobenius residual for the 29 proper masks was zero at the recorded precision. These are finite numerical checks, not exact arithmetic claims about state vectors.

The q = 2 and q = 4 normal-vector LP costs agree with the bounds 1.5 and 1.125, respectively. Those are exact overlap-cost predictions; the script does not identify them with exact quantum capacities.

## Relation to the proofs

[Geometry and loss](../science/geometry-and-loss.md) contains the general algebraic arguments, explicit normalized couplings, and the inherited-code attribution. The finite checks target normalization errors, hidden use of a latent-line label, surplus logical degrees of freedom, and incorrect transport costs. They do not establish the all-field theorems, certify literature novelty, or numerically compute unrestricted quantum capacity.
