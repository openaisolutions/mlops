import sys
from pathlib import Path
import numpy as np

# Ensure utils package is on path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.math_helpers import svd_decompose


def test_svd_reconstruction():
    A = np.array([[3, 1], [1, 3]])
    U, S, Vt = svd_decompose(A)
    A_recon = (U * S) @ Vt
    assert np.allclose(A, A_recon)
