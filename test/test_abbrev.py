# SPDX-FileCopyrightText: 2024 Alexandru Fikl <alexfikl@gmail.com>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import pytest


def test_pyiso4() -> None:
    ltwa = pytest.importorskip("pyiso4.ltwa")

    abbrev = ltwa.Abbreviate.create()
    result = abbrev("Journal of Computational Physics", remove_part=True)
    assert result == "J. Comput. Phys."  # spell: disable
