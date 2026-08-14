"""P-4 — Konvergenz (fuzz-prompt.md §3).

Haben am Ende alle Beobachter denselben Bestand und dieselbe Uhr, rechnen sie
dasselbe. Ohne Vorbehalte. Gleiche Uhr ist Bedingung, nicht Vorbehalt: über
``t_exp`` dürfen zwei korrekte Verifizierer dauerhaft uneins sein (01 §6, D72).
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
def test_p4_same_stock_same_clock_same_result(welt) -> None:
    claims = welt.claims
    fingerprints = []
    for _ in welt.pubs:
        store = speicher(*claims)
        fingerprints.append(
            (
                fingerprint_derive(store, welt),
                fingerprint_trust(store, welt),
                fingerprint_decide(store, welt),
                fingerprint_classify(store, welt),
            )
        )
    assert len(set(fingerprints)) == 1
