"""Check finite instances of the projective-line recovery and overlap bridge.

Run with the geometry verifier’s Python, NumPy and SciPy dependencies. All coupling arithmetic is rational. These
checks cover finite graph and mask families and do not compute capacity.
"""

import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
import json

from verify_geometry import line_data


def support_mask(points):
    return sum(1 << point for point in points)


def cnot(pauli, control, target):
    x, z = pauli
    x ^= ((x >> control) & 1) << target
    z ^= ((z >> target) & 1) << control
    return x, z


def check_complete_graph_witnesses(lines):
    witnesses = 0
    for line in lines:
        line_mask = support_mask(line)
        for output in range(len(lines)):
            pivot = output if output in line else line[0]
            others = [point for point in line if point != pivot]
            gates = list(zip(others[::2], others[1::2]))
            logical_x = (line_mask, 0)
            logical_z = (0, line_mask)
            if output != pivot:
                # Include the supplied product ancilla's +Z before its CNOT.
                logical_z = (0, line_mask | (1 << output))
                gates.append((pivot, output))
            for control, target in gates:
                logical_x = cnot(logical_x, control, target)
                logical_z = cnot(logical_z, control, target)
            lx_x, lx_z = logical_x
            lz_x, lz_z = logical_z
            local_anticommutation = (lx_x & lz_z) ^ (lx_z & lz_x)
            assert local_anticommutation == 1 << output
            assert ((lx_x >> output) & 1, (lx_z >> output) & 1) == (1, 0)
            assert ((lz_x >> output) & 1, (lz_z >> output) & 1) == (0, 1)
            terminals = line_mask ^ (1 << output)
            assert len(gates) == terminals.bit_count() // 2
            witnesses += 1
    return witnesses


def check_coupling(line_masks, accepted, full_retention):
    m = len(accepted)
    a = full_retention / len(line_masks)
    p = m * a
    marginal = {mask: a for mask in accepted if a}
    if p < 1:
        marginal[0] = 1 - p
    joint = defaultdict(Fraction)
    if p <= Fraction(1, 2):
        for line in accepted:
            joint[line, 0] = joint[0, line] = a
        joint[0, 0] = 1 - 2 * p
    else:
        for line in accepted:
            joint[line, 0] = joint[0, line] = (1 - p) / m
        for left, right in combinations(accepted, 2):
            joint[left, right] = joint[right, left] = (2 * p - 1) / (m * (m - 1))

    rows, columns = defaultdict(Fraction), defaultdict(Fraction)
    expected_overlap = 0
    for (left, right), probability in joint.items():
        assert probability >= 0
        if probability:
            rows[left] += probability
            columns[right] += probability
            expected_overlap += probability * (left & right).bit_count()
    assert sum(rows.values()) == 1
    assert rows == columns == marginal
    # Both masks being full is necessary for overlap and guarantees at least
    # one site. Its probability is at least max(0, 2p - 1) in any coupling.
    assert expected_overlap == max(0, 2 * p - 1)


def check_filtered_couplings(lines):
    masks = [support_mask(line) for line in lines]
    n = len(masks)
    if n == 7:
        families = [
            [mask for i, mask in enumerate(masks) if family & (1 << i)]
            for family in range(1 << n)
        ]
    else:
        sizes = {0, 1, n // 2, n // 2 + 1, n - 1, n}
        families = [masks[:size] for size in sorted(sizes)]
        families += [[mask for mask in masks if mask & (1 << i)] for i in (0, n - 1)]
    count = 0
    thresholds = 0
    for accepted in families:
        # The first five cases correspond to explicit thinning probabilities t.
        retention = {t ** len(lines[0]) for t in map(Fraction, ('0', '1/2', '3/4', '9/10', '1'))}
        if len(accepted) * 2 >= n:
            # Choose full-line retention t^(q+1) exactly to hit p = 1/2.
            retention.add(Fraction(n, 2 * len(accepted)))
            thresholds += 1
        for full_retention in sorted(retention):
            check_coupling(masks, accepted, full_retention)
            count += 1
    return {'accepted_line_families': len(families), 'couplings': count, 'exact_threshold_cases': thresholds}


def check_fano_hardware(lines):
    import numpy as np

    edges = list(combinations(range(7), 2))
    graph_count = 1 << len(edges)
    even = [mask for mask in range(1 << 7) if not mask.bit_count() % 2]
    parity_column = {mask: i for i, mask in enumerate(even)}
    infinity = 127

    # For each graph, compute a minimum over its edge subsets directly. Adding
    # an available edge either leaves the chosen subset unchanged or increases
    # its cost by one and toggles both of that edge's endpoint parities.
    minimum = np.full((len(even), graph_count), infinity, dtype=np.uint8)
    minimum[parity_column[0], 0] = 0
    for edge_index, (first, second) in enumerate(edges):
        prior_graphs = 1 << edge_index
        changed = (1 << first) ^ (1 << second)
        previous = minimum[:, :prior_graphs]
        added_edge = minimum[:, prior_graphs:2 * prior_graphs]
        for parity_index, mask in enumerate(even):
            np.minimum(previous[parity_index], previous[parity_column[mask ^ changed]] + 1,
                       out=added_edge[parity_index])

    # Use an independent test: Floyd-Warshall distances on each graph, then
    # check all pairings of its two or four terminals. Isolated vertices cover
    # absent sites once they are excluded as output choices.
    placements = [(support_mask(line) ^ (1 << output)) for line in lines for output in range(7)]
    terminal_sets = sorted(set(placements))
    edge_index_by_pair = {pair: i for i, pair in enumerate(edges)}
    line_edge_masks = [support_mask(edge_index_by_pair[pair] for pair in combinations(line, 2)) for line in lines]
    byte_popcounts = np.array([byte.bit_count() for byte in range(256)], dtype=np.uint8)
    maximum_accepted_lines = np.zeros(len(edges) + 1, dtype=np.uint8)
    for start in range(0, graph_count, 1 << 15):
        stop = min(start + (1 << 15), graph_count)
        graph_masks = np.arange(start, stop, dtype=np.uint32)
        distances = np.full((7, 7, stop - start), infinity, dtype=np.uint8)
        for vertex in range(7):
            distances[vertex, vertex] = 0
        for edge_index, (first, second) in enumerate(edges):
            distances[first, second] = np.where(graph_masks & (1 << edge_index), 1, infinity)
            distances[second, first] = distances[first, second]
        for interior in range(7):
            for first in range(7):
                for second in range(first + 1, 7):
                    np.minimum(distances[first, second], distances[first, interior] + distances[interior, second],
                               out=distances[first, second])
                    distances[second, first] = distances[first, second]
        for mask in terminal_sets:
            vertices = [vertex for vertex in range(7) if mask & (1 << vertex)]
            if len(vertices) == 2:
                first, second = vertices
                matching = distances[first, second]
            else:
                first, second, third, fourth = vertices
                matching = np.minimum.reduce((
                    distances[first, second] + distances[third, fourth],
                    distances[first, third] + distances[second, fourth],
                    distances[first, fourth] + distances[second, third],
                    np.full(stop - start, infinity, dtype=np.uint8),
                ))
            assert np.array_equal(minimum[parity_column[mask], start:stop], matching), (start, stop, mask)

        # When only the line's survivors remain available, a selectable output
        # at CNOT budget one accepts exactly those lines with an internal edge.
        accepted_count = np.zeros(stop - start, dtype=np.uint8)
        for line, line_edge_mask in zip(lines, line_edge_masks):
            induced_graph = graph_masks & line_edge_mask
            line_mask = support_mask(line)
            accepted = np.zeros(stop - start, dtype=np.bool_)
            for output in line:
                terminals = line_mask ^ (1 << output)
                accepted |= minimum[parity_column[terminals], induced_graph] <= 1
            assert np.array_equal(accepted, induced_graph != 0), (start, stop, line)
            accepted_count += accepted
        edge_counts = sum(byte_popcounts[(graph_masks >> shift) & 255] for shift in (0, 8, 16))
        np.maximum.at(maximum_accepted_lines, edge_counts, accepted_count)

    assert maximum_accepted_lines.tolist() == [min(len(lines), count) for count in range(len(edges) + 1)]
    return {
        'graphs': graph_count,
        'distinct_terminal_sets_per_graph': len(terminal_sets),
        'graph_terminal_set_comparisons': graph_count * len(terminal_sets),
        'graph_line_output_instances_covered': graph_count * len(placements),
        'survivor_induced_graph_line_acceptances_checked': graph_count * len(lines),
        'maximum_accepted_lines_by_installed_edge_count': maximum_accepted_lines.tolist(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-exhaustive-graphs', action='store_true', help='Run smaller field and coupling checks only.')
    args = parser.parse_args()
    results = {}
    for order in (2, 4, 8):
        _, incidence, _ = line_data(order)
        lines = [tuple(int(point) for point in row.nonzero()[0]) for row in incidence]
        results[f'GF({order})'] = {
            'points': len(lines),
            'complete_graph_witnesses': check_complete_graph_witnesses(lines),
            **check_filtered_couplings(lines),
        }
        if order == 2 and not args.skip_exhaustive_graphs:
            results['Fano unit-cost hardware'] = check_fano_hardware(lines)
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
