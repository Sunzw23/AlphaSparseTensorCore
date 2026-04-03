"""
Strategy transformation utilities for sparse matrix multiplication expressions.
"""

from .permutations import (
    parse_to_parts,
    parse_polynomial,
    reconstruct_polynomial,
    parse_var_index,
    reconstruct_var,
    create_permutation_from_list,
    swap_rows_permutation,
    swap_columns_permutation,
    apply_permutation_to_var,
    apply_permutations_to_expression,
    apply_permutations_to_solution,
)

__all__ = [
    'parse_to_parts',
    'parse_polynomial',
    'reconstruct_polynomial',
    'parse_var_index',
    'reconstruct_var',
    'create_permutation_from_list',
    'swap_rows_permutation',
    'swap_columns_permutation',
    'apply_permutation_to_var',
    'apply_permutations_to_expression',
    'apply_permutations_to_solution',
]