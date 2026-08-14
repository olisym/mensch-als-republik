"""P-1 — Reihenfolgeunabhängigkeit (fuzz-prompt.md §3).

Derselbe Claim-Bestand in beliebiger Einfügereihenfolge liefert byte-identische
Ergebnisse. Ohne Vorbehalte. Spec: Ableitung ist eine Funktion der Menge, nicht
der Einfügereihenfolge.
"""

from __future__ import annotations

from hypothesis import given

from tests.property.welten import (
    fingerprint_classify,
    fingerprint_decide,
    fingerprint_derive,
    fingerprint_trust,
    speicher,
    welten,
)


@given(welten())
def test_p1_derive_and_trust_ignore_insertion_order(welt) -> None:
    claims = welt.claims
    a = speicher(*claims)
    b = speicher(*reversed(claims))
    assert fingerprint_derive(a, welt) == fingerprint_derive(b, welt)
    assert fingerprint_trust(a, welt) == fingerprint_trust(b, welt)


@given(welten())
def test_p1_decide_and_classify_ignore_insertion_order(welt) -> None:
    claims = welt.claims
    a = speicher(*claims)
    b = speicher(*reversed(claims))
    assert fingerprint_decide(a, welt) == fingerprint_decide(b, welt)
    assert fingerprint_classify(a, welt) == fingerprint_classify(b, welt)
