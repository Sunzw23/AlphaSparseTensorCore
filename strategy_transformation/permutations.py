"""
Expression parsing and permutation transformations.

This module merges parsing utilities, low-level permutation helpers,
and high-level strategy transformation APIs.

Formula convention:
AB = C^T, where A:(n,m), B:(m,l), C:(l,n)
After permutation: (P*A*Q^T) * (Q*B) = (C*P^T)^T
"""
import re


def parse_to_parts(expression):
    """
    Parse expression into multiple polynomial parts within parentheses.

    Example:
        '(a11+a12)*(b11+b12)*(c11+c12)' -> ['a11+a12', 'b11+b12', 'c11+c12']
    """
    expr = expression.replace(' ', '')

    parts = []
    current = []
    depth = 0
    for ch in expr:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth = max(0, depth - 1)

        if ch == '*' and depth == 0:
            part = ''.join(current).strip()
            if part:
                if part.startswith('(') and part.endswith(')'):
                    part = part[1:-1]
                parts.append(part)
            current = []
        else:
            current.append(ch)

    if current:
        part = ''.join(current).strip()
        if part:
            if part.startswith('(') and part.endswith(')'):
                part = part[1:-1]
            parts.append(part)

    return parts


def parse_polynomial(polynomial_str):
    """
    Parse a polynomial string into list of (coefficient, variable) tuples.

    Example:
        'a11+2*a12-a13' -> [(1, 'a11'), (2, 'a12'), (-1, 'a13')]
    """
    polynomial_str = polynomial_str.replace(' ', '')

    term_pattern = r'([+-]?)(\d*)\*?([a-zA-Z]\d+)'
    matches = re.findall(term_pattern, polynomial_str)

    terms = []
    for sign, coeff, var in matches:
        if coeff == '':
            coefficient = 1
        else:
            coefficient = int(coeff)

        if sign == '-':
            coefficient = -coefficient

        terms.append((coefficient, var))

    return terms


def reconstruct_polynomial(terms):
    """
    Reconstruct polynomial string from (coefficient, variable) tuples.

    Example:
        [(1, 'a11'), (2, 'a12'), (-1, 'a13')] -> 'a11+2*a12-a13'
    """
    if not terms:
        return '0'

    result_parts = []
    for i, (coeff, var) in enumerate(terms):
        if i == 0:
            if coeff == 1:
                result_parts.append(f'{var}')
            elif coeff == -1:
                result_parts.append(f'-{var}')
            else:
                result_parts.append(f'{coeff}*{var}')
        else:
            if coeff == 1:
                result_parts.append(f'+{var}')
            elif coeff == -1:
                result_parts.append(f'-{var}')
            elif coeff > 0:
                result_parts.append(f'+{coeff}*{var}')
            else:
                result_parts.append(f'{coeff}*{var}')

    return ''.join(result_parts)


def parse_var_index(var_str):
    """
    Parse variable index like 'a14' into (var_type, row, col).

    Example:
        'a14' -> ('a', 1, 4)
        'b23' -> ('b', 2, 3)
    """
    match = re.match(r'([a-z])(\d+)(\d+)', var_str)
    if match:
        var_type = match.group(1)
        row = int(match.group(2))
        col = int(match.group(3))
        return (var_type, row, col)
    return None


def reconstruct_var(var_type, row, col):
    """Reconstruct variable string from (var_type, row, col)."""
    return f"{var_type}{row}{col}"


def create_permutation_from_list(perm_list):
    """
    Create permutation function from a list.

    Args:
        perm_list: Permutation list like [2, 1, 3, 4] meaning 1->2, 2->1, 3->3, 4->4

    Returns:
        perm_func
    """
    perm_func = lambda i: perm_list[i - 1]

    return perm_func


def swap_rows_permutation(n, i, j):
    """Create permutation that swaps rows i and j."""
    perm_list = list(range(1, n + 1))
    perm_list[i - 1], perm_list[j - 1] = perm_list[j - 1], perm_list[i - 1]
    return create_permutation_from_list(perm_list)


def swap_columns_permutation(n, i, j):
    """Create permutation that swaps columns i and j."""
    perm_list = list(range(1, n + 1))
    perm_list[i - 1], perm_list[j - 1] = perm_list[j - 1], perm_list[i - 1]
    return create_permutation_from_list(perm_list)


def apply_permutation_to_var(var_str, row_perm, col_perm):
    """
    Apply row/column permutations to a single variable.
    """
    var_info = parse_var_index(var_str)
    if var_info is None:
        return var_str

    var_type, row, col = var_info

    if var_type == 'a':
        new_row = row_perm(row)
        new_col = col_perm(col)
    elif var_type == 'b':
        new_row = col_perm(row)
        new_col = col
    elif var_type == 'c':
        new_row = row
        new_col = row_perm(col)
    else:
        return var_str

    return reconstruct_var(var_type, new_row, new_col)


def apply_permutations_to_expression(line, row_perm, col_perm):
    """Apply permutations to a single expression line."""
    parts = parse_to_parts(line)

    result_parts = []
    for part in parts:
        terms = parse_polynomial(part)

        transformed_terms = []
        for coeff, var in terms:
            new_var = apply_permutation_to_var(var, row_perm, col_perm)
            transformed_terms.append((coeff, new_var))

        reconstructed = reconstruct_polynomial(transformed_terms)
        result_parts.append(reconstructed)

        if reconstructed == '0':
            return None

    return '*'.join([f'({part})' for part in result_parts])


def apply_permutations_to_solution(input_text, row_perm, col_perm):
    """Apply permutations to all expressions in input text (one per line)."""
    lines = input_text.strip().split('\n')
    results = []

    for line in lines:
        line = line.strip()
        if line:
            result = apply_permutations_to_expression(line, row_perm, col_perm)
            if result is not None:
                results.append(result)

    return '\n'.join(results)