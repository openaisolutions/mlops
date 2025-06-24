from pathlib import Path

import nbformat
import pytest

NB_DIR = Path(__file__).resolve().parents[1] / "notebooks"

notebooks = sorted(NB_DIR.glob("*.ipynb"))


def test_notebook_count():
    # Expect at least 10 notebooks for the book scaffolding
    assert len(notebooks) >= 10


@pytest.mark.parametrize("nb_file", notebooks)
def test_notebook_has_cells(nb_file):
    nb = nbformat.read(nb_file, as_version=4)
    assert len(nb.cells) > 0
