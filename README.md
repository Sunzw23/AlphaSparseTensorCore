# AlphaSparseTensorCore

## Algorithms

The folder `algorithms` contains optimal sparse matrix multiplication strategies for $4 \times 4 \times 4$ matrices with varying numbers of zero elements (from 1 to 7). 

Specifically, for the matrix multiplication $AB=C$, we investigated all possible distributions of sparse elements (set to 0) within matrix $A$. This dataset covers every unique configuration where the number of zero elements $n$ ranges from 1 to 7. For each configuration, we provide an optimized multiplication strategy identified through this search, which significantly reduces the number of multiplications required.

The `algorithms` directory is organized into seven subfolders (named `1/` through `7/`), where the folder name $n$ represents the total number of zero elements in matrix $A$. Within each subfolder, individual strategy files are named according to the indices of the zero elements. For example, a file named `a11-a22.exp` contains the optimal algorithm for a case where elements $a_{11}$ and $a_{22}$ are zero.

These strategies were obtained by performing a search using the [ternary_flip_graph](https://github.com/dronperminov/ternary_flip_graph) repository, which was adapted specifically for the discovery of sparse structures.

### How to interpret the algorithms

Take a  $2\times 2\times 2$ sparse matrix multiplication algorithm with the (1,1) element of matrix $\textbf{A}$ being 0 as an example. In our representation method corresponding to low-rank decomposition of three-dimensional spatial tensors, it would be written as:

```
(a22)*(b11+b22)*(c11+c22)
(a21+a22)*(b11)*(c12-c22)
(a22)*(b21-b11)*(c11+c12)
(a12)*(b22)*(-c11+c21)
(a21)*(b11+b12)*(c22)
(a12-a22)*(b21+b22)*(c11)
```

For the part contains a and b, each row corresponds to an intermediate variable $M_i$ calculated by adding or subtracting elements from A and B:

$$
\begin{aligned}
M_1 &= A_{22}(B_{11}+B_{22}) \\
M_2 &= (A_{21}+A_{22})B_{11} \\
M_3 &= A_{22}(B_{21}-B_{11}) \\
M_4 &= A_{12}B_{22} \\
M_5 &= A_{21}(B_{11}+B_{12}) \\
M_6 &= (A_{12}-A_{22})(B_{21}+B_{22})
\end{aligned}
$$


For the part contains c, each row represents the role of the intermediate variable $M_i$ when calculating a specific element of the final matrix C. The coefficient in front of $C_{xy}$ represents the actual coefficient of $M_i$ when computing the element $(y,x)$ of matrix C. (To be consistent with the notation for tensor low-rank decomposition, the subscript of c needs to be **transposed**)

$$
\begin{aligned}
C_{11} &= M_1 + M_3 - M_4 + M_6 \\
C_{12} &= M_4 \\
C_{21} &= M_2 + M_3 \\
C_{22} &= M_1 - M_2 + M_5
\end{aligned}
$$

The decomposition algorithm above is equivalent to the matrix multiplication calculation below:

$$
\left(
\begin{array}{cc}
 c _ { 11 } & c _ { 12 } \\
 c _ { 21 } & c _ { 22 }
\end{array}
\right) =
\left(
\begin{array}{cc}
0 & a _ { 12 } \\
 a _ { 21 } & a _ { 22 }
\end{array}
\right)
\cdot 
\left(
\begin{array}{cc}
 b _ { 11 } & b _ { 12 } \\
 b _ { 21 } & b _ { 22 }
\end{array}
\right)
$$

## Strategy Transformation

The `strategy_transformation` package provides permutation-based transformations for sparse matrix multiplication expressions. It lets us derive equivalent strategies for different sparse layouts of matrix $A$ by reindexing rows and columns, instead of rebuilding an algorithm from scratch.

### Usage

The main API is implemented in:

`strategy_transformation/permutations.py`

#### Transformation by permutation

Use this when you already have a row or column permutation and want to apply it to a full strategy file.

The example below swaps rows 1 and 2, and columns 1 and 2, for a $4 \times 4 \times 4$ matrix multiplication strategy where $a_{11}=0$. The resulting strategy corresponds to the case where the zero elements are located at position $a_{22}$.

```python
from strategy_transformation import (
	create_permutation_from_list,
	apply_permutations_to_solution,
)

# Example: 4x4 matrix, swap row/col 1 and 2 by permutation list [2,1,3,4]
row_perm = create_permutation_from_list([2, 1, 3, 4])
col_perm = create_permutation_from_list([2, 1, 3, 4])

with open("algorithms/1/a11.exp", "r", encoding="utf-8") as f:
	input_text = f.read()

output_text = apply_permutations_to_solution(
	input_text,
	row_perm=row_perm,
	col_perm=col_perm,
)

print(output_text)
```