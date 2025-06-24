import numpy as np


def svd_decompose(matrix):
    """Return U, S, Vt for the given matrix using numpy."""
    return np.linalg.svd(matrix)
