#!/usr/bin/env python3
"""Finite verification of the projective-plane erasure channels.

Run from the repository root:
    python verification/verify_geometry.py

The integer checks cover q=2,4,8,16. State-vector checks cover q=2.
Transport LPs independently minimize the overlap on aggregated observed-mask
laws for q=2 and q=4; they do not assume the constructive coupling ansatz.
See science/geometry-and-loss.md for the general proofs and attribution.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


# Irreducible binary polynomials defining the small finite fields.
MODULI = {2: 0b11, 4: 0b111, 8: 0b1011, 16: 0b10011}
LP_TOLERANCE = 1e-8


def require(condition, message):
    """Keep verification active even if Python is invoked with optimization."""
    if not condition:
        raise AssertionError(message)


def mul(a, b, q):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & q:
            a ^= MODULI[q]
    return out


def dot(a, b, q):
    out = 0
    for x, y in zip(a, b):
        out ^= mul(x, y, q)
    return out


def projective(q):
    """Represent each one-dimensional subspace by first nonzero entry one."""
    return [(1, a, b) for a in range(q) for b in range(q)] + [
        (0, 1, a) for a in range(q)
    ] + [(0, 0, 1)]


def xor_basis(vectors):
    pivots = {}
    for x in vectors:
        while x:
            pivot = x.bit_length() - 1
            if pivot in pivots:
                x ^= pivots[pivot]
            else:
                pivots[pivot] = x
                break
    return list(pivots.values())


def nullspace_basis(vectors, n):
    """A basis of the orthogonal complement over F_2, in bit-mask form."""
    pivots = {row.bit_length() - 1: row for row in xor_basis(vectors)}
    free = [j for j in range(n) if j not in pivots]
    basis = []
    for free_bit in free:
        vector = 1 << free_bit
        # A row's highest bit is its pivot, so its lower variables are ready.
        for pivot, row in sorted(pivots.items()):
            if (row & vector).bit_count() % 2:
                vector ^= 1 << pivot
        basis.append(vector)
    require(len(basis) == n - len(pivots), "Nullspace dimension mismatch")
    require(all((u & v).bit_count() % 2 == 0
                for u in vectors for v in basis), "Nullspace orthogonality")
    return basis


def line_data(q):
    points = projective(q)
    incidence = np.array(
        [[int(dot(a, x, q) == 0) for x in points] for a in points],
        dtype=np.int64,
    )
    masks = [sum(int(bit) << j for j, bit in enumerate(row))
             for row in incidence]
    return points, incidence, masks


def all_submasks(mask):
    subset = mask
    while True:
        yield subset
        if subset == 0:
            return
        subset = (subset - 1) & mask


def encoded_bell(rows, basis):
    n = 7
    code = np.zeros((2, 1 << n), dtype=np.complex128)
    for coeff in itertools.product([0, 1], repeat=len(basis)):
        vector = 0
        for coefficient, row in zip(coeff, basis):
            if coefficient:
                vector ^= row
        for logical in range(2):
            code[logical, vector ^ (rows[0] if logical else 0)] = (
                1 / math.sqrt(2 ** len(basis))
            )
    require(np.allclose(code @ code.conj().T, np.eye(2), atol=1e-14),
            "Encoder isometry check")
    bell = np.zeros(1 << (n + 1), dtype=np.complex128)
    for logical in range(2):
        bell[(logical << n):((logical + 1) << n)] = code[logical] / math.sqrt(2)
    return bell


def reduced_reference_and_mask(state, physical_n, mask):
    """Order the retained systems as reference first, then selected qubits."""
    retained = [j for j in range(physical_n) if (mask >> j) & 1]
    discarded = [j for j in range(physical_n) if not ((mask >> j) & 1)]
    matrix = np.zeros(
        (1 << (1 + len(retained)), 1 << len(discarded)),
        dtype=np.complex128,
    )
    for label, amplitude in enumerate(state):
        row = (((label >> physical_n) & 1) << len(retained))
        row |= sum(((label >> j) & 1) << k for k, j in enumerate(retained))
        column = sum(((label >> j) & 1) << k for k, j in enumerate(discarded))
        matrix[row, column] = amplitude
    return matrix @ matrix.conj().T


def state_checks_fano(rows, basis):
    n = 7
    bell = encoded_bell(rows, basis)
    fidelities = []
    phi = np.array([1, 0, 0, 1], dtype=np.complex128) / math.sqrt(2)
    for row in rows:
        line = [j for j in range(n) if (row >> j) & 1]
        pivot = line[0]
        gates = [(j, pivot) for j in line[1:]] + [(pivot, j) for j in line[1:]]
        decoded = np.zeros_like(bell)
        for label, amplitude in enumerate(bell):
            output_label = label
            for control, target in gates:
                if (output_label >> control) & 1:
                    output_label ^= 1 << target
            decoded[output_label] = amplitude
        rho = reduced_reference_and_mask(decoded, n, 1 << pivot)
        fidelities.append(float(np.real(phi.conj() @ rho @ phi)))
    require(min(fidelities) > 1 - 1e-12, "Fano Bell recovery")

    proper_masks = sorted({subset for row in rows for subset in all_submasks(row)
                           if subset != row})
    decoupling_residuals = []
    for subset in proper_masks:
        rho = reduced_reference_and_mask(bell, n, subset)
        d = 1 << subset.bit_count()
        rho_s = rho[:d, :d] + rho[d:, d:]
        decoupled = np.kron(np.eye(2) / 2, rho_s)
        decoupling_residuals.append(float(np.linalg.norm(rho - decoupled)))
    require(len(proper_masks) == 29, "Fano proper observable-mask count")
    require(max(decoupling_residuals) < 1e-12, "Proper-mask reference decoupling")
    return {
        "encoded_reference": "maximally entangled qubit",
        "fano_bell_entanglement_fidelities_all_lines": fidelities,
        "proper_observable_masks_checked": len(proper_masks),
        "maximum_reference_decoupling_frobenius_residual": max(decoupling_residuals),
    }


def geometry_check(q):
    points, incidence, rows = line_data(q)
    n = len(points)
    require(n == q * q + q + 1, "Projective point count")
    require(len(set(rows)) == n, "Distinct projective lines")
    gram = incidence @ incidence.T
    require(np.all(incidence.sum(axis=0) == q + 1), "Point incidence degree")
    require(np.all(incidence.sum(axis=1) == q + 1), "Line size")
    require(np.all(gram[np.triu_indices(n, 1)] == 1), "Distinct-line intersection")

    differences = [row ^ rows[0] for row in rows]
    basis_d = xor_basis(differences)
    basis_c = xor_basis(basis_d + [rows[0]])
    basis_z = nullspace_basis(basis_c, n)
    require(all((u & v).bit_count() % 2 == 0
                for u in basis_d for v in basis_d), "D self-orthogonality")
    require(all((u & rows[0]).bit_count() % 2 == 0 for u in basis_d),
            "Reference line orthogonal to D")
    require(rows[0].bit_count() % 2 == 1, "Odd line size")
    require(len(basis_c) == len(basis_d) + 1, "Logical coset independence")
    require(all((d & z).bit_count() % 2 == 0 for d in basis_d for z in basis_z),
            "Full CSS stabilizer commutation")
    require(len(basis_d) + len(basis_z) == n - 1, "Exactly one logical qubit")
    require(all((line & z).bit_count() % 2 == 0 for line in rows for z in basis_z),
            "Every line supports a commuting logical X")
    require(all((line & d).bit_count() % 2 == 0 for line in rows for d in basis_d),
            "Every line supports a commuting logical Z")
    require(all((line & rows[0]).bit_count() % 2 == 1 for line in rows),
            "Every line represents the same nontrivial logical Pauli class")

    # A uniform normal in F_q^3 gives q-1 copies of every line and one full mask.
    counts = (q - 1) * gram + np.ones((n, n), dtype=np.int64)
    require(np.all(np.diag(counts) == q * q), "Normal-vector single flag count")
    require(np.all(counts[np.triu_indices(n, 1)] == q),
            "Normal-vector pair flag count")
    require(n * (q - 1) + 1 == q ** 3, "Normal-vector law normalization")
    collinear_triple = [j for j in range(n) if (rows[0] >> j) & 1][:3]
    noncollinear_triple = next(
        triple for triple in itertools.combinations(range(n), 3)
        if not any(all((line >> j) & 1 for j in triple) for line in rows)
    )
    triple_counts = []
    for triple in (collinear_triple, noncollinear_triple):
        triple_counts.append(
            (q - 1) * sum(all((line >> j) & 1 for j in triple) for line in rows) + 1
        )
    require(triple_counts == [q, 1], "Collinear versus noncollinear triple flags")

    # Known binary incidence rank; recovery does not require this formula.
    m = q.bit_length() - 1
    require(len(basis_d) == 3 ** m, "Known binary difference-space rank")
    decoder_size = q + 1
    decoder = np.eye(decoder_size, dtype=np.int64)
    for j in range(1, decoder_size):
        decoder[0] ^= decoder[j]
    for j in range(1, decoder_size):
        decoder[j] ^= decoder[0]
    require(np.array_equal(decoder[0], np.ones(decoder_size, dtype=np.int64)),
            "Decoder first row")
    require(np.array_equal(
        (decoder @ np.ones(decoder_size, dtype=np.int64)) % 2,
        np.array([1] + [0] * (decoder_size - 1)),
    ), "Decoder logical X action")
    require(np.array_equal(decoder.T[:, 0], np.ones(decoder_size, dtype=np.int64)),
            "Decoder logical Z action via M^T e_1 = 1")

    result = {
        "q": q,
        "physical_qubits": n,
        "line_size": q + 1,
        "difference_rank": len(basis_d),
        "full_css_x_stabilizer_rank": len(basis_d),
        "full_css_z_stabilizer_rank": len(basis_z),
        "full_css_logical_qubits": n - len(basis_d) - len(basis_z),
        "self_orthogonal_css_logicals_before_fixing": n - 2 * len(basis_d),
        "decoder_cnot_count": 2 * q,
        "normal_count": q ** 3,
        "single_survival_numerator": q ** 2,
        "pair_survival_numerator": q,
        "collinear_triple_survival_numerator": triple_counts[0],
        "noncollinear_triple_survival_numerator": triple_counts[1],
        "survival_denominator": q ** 3,
        "achievable_rate": 1 / n,
        "universal_marginal_upper_rate": 1 / q ** 2,
        "achievable_fraction_of_upper": q ** 2 / n,
        "normal_vector_block_upper_via_coupling": 1 + 2 / q ** 2,
        "integer_checks_passed": True,
    }
    if q == 2:
        result["state_vector_checks"] = state_checks_fano(rows, basis_d)
    return result


def thinned_mask_law(lines, t):
    """Enumerate the physical experiment, summing duplicate observed masks."""
    line_size = lines[0].bit_count()
    distribution = defaultdict(float)
    for line in lines:
        for subset in all_submasks(line):
            size = subset.bit_count()
            probability = t ** size * (1 - t) ** (line_size - size) / len(lines)
            if probability > 0:
                distribution[subset] += probability
    return dict(distribution)


def transport_lp(distribution):
    """Unrestricted self-coupling LP on actual output masks, with dual checks."""
    masks = sorted(distribution)
    marginal = np.array([distribution[mask] for mask in masks], dtype=float)
    normalization_error = float(abs(marginal.sum() - 1))
    require(normalization_error < 1e-12, "Observed-mask law normalization")
    count = len(masks)
    costs = np.array([[(s & t).bit_count() for t in masks] for s in masks], dtype=float)

    # Every variable pi_ij enters one row-marginal and one column-marginal constraint.
    variable_indices = np.arange(count * count)
    constraint_rows = np.concatenate([
        np.repeat(np.arange(count), count),
        count + np.tile(np.arange(count), count),
    ])
    equality = coo_matrix(
        (np.ones(2 * count * count),
         (constraint_rows, np.concatenate([variable_indices, variable_indices]))),
        shape=(2 * count, count * count),
    ).tocsr()
    rhs = np.concatenate([marginal, marginal])
    result = linprog(
        costs.ravel(), A_eq=equality, b_eq=rhs, bounds=(0, None), method="highs",
        options={"primal_feasibility_tolerance": 1e-9,
                 "dual_feasibility_tolerance": 1e-9},
    )
    require(result.success, f"Transport LP failed: {result.message}")
    coupling = result.x.reshape((count, count))
    row_error = float(np.max(np.abs(coupling.sum(axis=1) - marginal)))
    column_error = float(np.max(np.abs(coupling.sum(axis=0) - marginal)))
    minimum_entry = float(coupling.min())

    # Dual potentials are independent LP certificates: u_s + v_t <= |s intersect t|.
    potentials = result.eqlin.marginals
    dual_value = float(rhs @ potentials)
    dual_violation = float(max(0.0, np.max(
        potentials[:count, None] + potentials[None, count:] - costs
    )))
    duality_gap = float(abs(result.fun - dual_value))
    require(max(row_error, column_error, max(0.0, -minimum_entry)) < LP_TOLERANCE,
            "LP primal marginal or nonnegativity residual")
    require(max(dual_violation, duality_gap) < LP_TOLERANCE,
            "LP dual certificate residual")
    return {
        "observable_mask_support": count,
        "nonnegative_transport_variables": count * count,
        "marginal_constraints": 2 * count,
        "input_law_normalization_error": normalization_error,
        "minimum_expected_overlap": float(result.fun),
        "maximum_row_marginal_error": row_error,
        "maximum_column_marginal_error": column_error,
        "minimum_coupling_entry": minimum_entry,
        "dual_objective": dual_value,
        "maximum_dual_constraint_violation": dual_violation,
        "primal_dual_gap": duality_gap,
        "solver_success": bool(result.success),
        "solver_message": result.message,
    }


def lp_checks(q):
    _, _, lines = line_data(q)
    n = len(lines)
    threshold_t = 2 ** (-1 / (q + 1))
    if q == 2:
        t_cases = [0.0, 0.25, 0.5, threshold_t - 0.01,
                   threshold_t, threshold_t + 0.01, 0.9, 1.0]
    else:
        t_cases = [0.75, 0.95]
    thinning = []
    for t in t_cases:
        distribution = thinned_mask_law(lines, t)
        check = transport_lp(distribution)
        prediction = max(2 * t ** (q + 1) - 1, 0.0)
        discrepancy = abs(check["minimum_expected_overlap"] - prediction)
        require(discrepancy < LP_TOLERANCE, "Thinning LP versus exact capacity formula")
        check.update({
            "q": q,
            "additional_retention_t": t,
            "full_line_probability": t ** (q + 1),
            "predicted_minimum_overlap_and_capacity": prediction,
            "absolute_prediction_error": discrepancy,
            "empty_mask_probability": distribution.get(0, 0.0),
            "singleton_probability_range": [
                min(distribution.get(1 << j, 0.0) for j in range(n)),
                max(distribution.get(1 << j, 0.0) for j in range(n)),
            ],
        })
        thinning.append(check)

    p = q ** -3
    normal_law = {line: (1 - p) / n for line in lines}
    normal_law[(1 << n) - 1] = p
    normal = transport_lp(normal_law)
    normal_prediction = 1 + 2 / q ** 2
    require(abs(normal["minimum_expected_overlap"] - normal_prediction) < LP_TOLERANCE,
            "Normal-vector exact overlap cost")
    normal.update({
        "q": q,
        "predicted_minimum_overlap": normal_prediction,
        "absolute_prediction_error": abs(normal["minimum_expected_overlap"] - normal_prediction),
        "interpretation": "Overlap bound, not an assertion of exact channel capacity",
    })
    return thinning, normal


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results.json"))
    arguments = parser.parse_args()
    geometry = [geometry_check(q) for q in (2, 4, 8, 16)]
    thinning, normal = [], []
    for q in (2, 4):
        thin_q, normal_q = lp_checks(q)
        thinning.extend(thin_q)
        normal.append(normal_q)
    result = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "lp_solver": "scipy.optimize.linprog, method=highs",
        },
        "all_checks_passed": True,
        "lp_acceptance_tolerance": LP_TOLERANCE,
        "geometry_and_code": geometry,
        "thinning_transport_lp": thinning,
        "normal_vector_transport_lp": normal,
        "scope": {
            "integer_geometry_q": [2, 4, 8, 16],
            "state_vector_q": [2],
            "transport_lp_q": [2, 4],
            "general_proof": "science/geometry-and-loss.md",
            "normal_vector_capacity": "Only lower and upper bounds are claimed",
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "all_checks_passed": result["all_checks_passed"],
        "geometry_cases": len(geometry),
        "thinning_lp_cases": len(thinning),
        "normal_vector_lp_cases": len(normal),
        "maximum_lp_prediction_error": max(
            case["absolute_prediction_error"] for case in thinning + normal
        ),
        "output": str(arguments.output),
    }, indent=2))


if __name__ == "__main__":
    main()
