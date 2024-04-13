import sympy
import numpy as np

g = np.array([[1, 1, 0, 1, 0, 0, 0],
       [0, 1, 1, 0, 1, 0, 0],
       [0, 0, 1, 1, 0, 1, 0],
       [0, 0, 0, 1, 1, 0, 1]])

h = np.array(sympy.Matrix(g).nullspace()) % 2

print(h)