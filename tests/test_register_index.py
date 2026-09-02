"""Registerindex: Ziffernform und Anhangsform (D209, D230, D300, Prüfregel 38)."""

from __future__ import annotations

import re

import pytest

from tools.register_index import REGISTER, build_index, entries, refs_in

_APPENDIX = ("01 §B.1", "01 §B.2", "01 §B.3", "01 §C.10", "01 §C.13", "01 §C.15")
_DIGIT_SECTION = "04 §4.1"


def _register_text() -> str:
    return REGISTER.read_text(encoding="utf-8")


def _named_in_register(text: str, needle: str) -> list[str]:
    found: list[str] = []
    for did, body in entries(text):
        if needle in body:
            found.append(did)
    return found


def test_digit_form_still_recognised() -> None:
    index = build_index(_register_text())
    assert index.get(_DIGIT_SECTION, []) != []


@pytest.mark.parametrize("section", _APPENDIX)
def test_appendix_form_is_recognised(section: str) -> None:
    index = build_index(_register_text())
    assert index.get(section, []) != []


def test_b2_list_is_derived_from_register_text() -> None:
    text = _register_text()
    expected = _named_in_register(text, "01 §B.2")
    assert build_index(text)["01 §B.2"] == expected


def test_letter_without_digit_is_not_a_key() -> None:
    assert "01 §B" not in refs_in("siehe 01 §B und weiter")
    index = build_index(_register_text())
    for key in index:
        assert re.search(r"§[A-Z]$", key) is None


def test_lists_are_register_order_without_duplicates() -> None:
    text = _register_text()
    order = [did for did, _body in entries(text)]
    position = {did: i for i, did in enumerate(order)}
    for _section, ids in build_index(text).items():
        assert len(ids) == len(set(ids))
        assert ids == sorted(ids, key=lambda did: position[did])
