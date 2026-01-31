# SPDX-FileCopyrightText: 2024 Alexandru Fikl <alexfikl@gmail.com>
# SPDX-License-Identifier: MIT

from __future__ import annotations


def test_pyiso4() -> None:
    from pyiso4.ltwa import Abbreviate

    abbrev = Abbreviate.create()
    result = abbrev("Journal of Computational Physics", remove_part=True)
    assert result == "J. Comput. Phys."  # spell: disable


def test_latex_encoding() -> None:
    from pyiso4.ltwa import Abbreviate

    # NOTE: pyiso4 will not handle the escaped \&, but our code will

    abbrev = Abbreviate.create()
    result = abbrev(r"Computers \& Mathematics With Applications", remove_part=True)
    assert result == r"Comput.\& Math. Appl."  # spell: disable

    from papis_abbrev.command import abbreviate

    (result,) = abbreviate([{"journal": r"Computers \& Mathematics With Applications"}])
    assert result["journal_abbrev"] == "Comput. Math. Appl."  # spell: disable
