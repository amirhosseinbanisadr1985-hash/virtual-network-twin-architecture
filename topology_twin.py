"""Minimal VNT topology example using a binary undirected adjacency matrix.

This is a standalone educational demonstration, not the paper's implementation.
"""
from __future__ import annotations

from copy import deepcopy


def validate_matrix(matrix: list[list[int]]) -> None:
    """Check that a binary adjacency matrix describes an undirected simple graph."""
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("Matrix must be nonempty and square")
    for i in range(n):
        if matrix[i][i] != 0:
            raise ValueError("Self-loops are not supported")
        for j in range(n):
            if matrix[i][j] not in (0, 1) or matrix[i][j] != matrix[j][i]:
                raise ValueError("Matrix must be binary and symmetric")


def create_twin(original: list[list[int]]) -> list[list[int]]:
    """Return an independent snapshot of the original network topology."""
    validate_matrix(original)
    return deepcopy(original)


def set_link(matrix: list[list[int]], a: int, b: int, connected: bool) -> None:
    """Add or remove an undirected link between two distinct nodes."""
    validate_matrix(matrix)
    n = len(matrix)
    if not (0 <= a < n and 0 <= b < n) or a == b:
        raise ValueError("Node indices must be distinct and within bounds")
    matrix[a][b] = matrix[b][a] = int(connected)


def topology_accuracy(original: list[list[int]], twin: list[list[int]]) -> float:
    """Fraction of matching possible undirected edges (including absent links).

    This simple illustrative metric is NOT a validated VNT fidelity KPI.
    """
    validate_matrix(original)
    validate_matrix(twin)
    if len(original) != len(twin):
        raise ValueError("Original and twin must have the same number of nodes")
    n = len(original)
    if n == 1:
        return 1.0
    possible_edges = n * (n - 1) // 2
    matches = sum(original[i][j] == twin[i][j] for i in range(n) for j in range(i + 1, n))
    return matches / possible_edges


def main() -> None:
    labels = ["Router", "Switch", "Server", "Client"]
    original = [
        [0, 1, 0, 0],
        [1, 0, 1, 1],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
    ]
    twin = create_twin(original)
    print("Nodes:", ", ".join(labels))
    print(f"Initial topology agreement: {topology_accuracy(original, twin):.1%}")
    set_link(original, 1, 3, False)  # Original network changes; twin is now stale.
    print(f"After link removal, before refresh: {topology_accuracy(original, twin):.1%}")
    twin = create_twin(original)  # Manual snapshot refresh, not live synchronization.
    print(f"After manual twin refresh: {topology_accuracy(original, twin):.1%}")


if __name__ == "__main__":
    main()
