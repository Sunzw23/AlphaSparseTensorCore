# AlphaSparseTensorCore

## Algorithms

The folder `algorithms` contains optimal sparse matrix multiplication strategies for $4 \times 4 \times 4$ matrices with varying numbers of zero elements (from 1 to 7). 

Specifically, for the matrix multiplication $AB=C$, we investigated all possible distributions of sparse elements (set to 0) within matrix $A$. This dataset covers every unique configuration where the number of zero elements $n$ ranges from 1 to 7. For each configuration, we provide the fast multiplication strategy that achieves the theoretical minimum number of multiplications.

The `algorithms` directory is organized into seven subfolders (named `1/` through `7/`), where the folder name $n$ represents the total number of zero elements in matrix $A$. Within each subfolder, individual strategy files are named according to the indices of the zero elements. For example, a file named `a11_a22.exp` contains the optimal algorithm for a case where elements $a_{11}$ and $a_{22}$ are zero.

These strategies were derived by applying slight modifications to the algorithms provided by the [ternary_flip_graph](https://github.com/dronperminov/ternary_flip_graph) repository, adapted specifically for the discovery of sparse structures.

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

