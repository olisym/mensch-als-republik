"""P-2 — Monotonie in Wissen, mit Vorbehalten (werkzeuge.md §4.2, 02 §7).

Eine Teilmenge des Claim-Bestands liefert nie höheres Vertrauen als der volle
Bestand. Vorbehalte, beide zwingend:

- ``erlaube_ueberzeichnung = False`` — Budgetprüfung Σ n ≤ D ist nicht monoton (D118).
- ``erlaube_equivocation = False`` — ein Zwilling entzieht einem zählenden Claim
  die Wirkung (D117).
"""

from __future__ import annotations

from hypothesis import given

from tests.property.welten import (
    hoeheres_vertrauen,
    speicher,
    teilmengen,
    welten,
)


@given(welten(erlaube_ueberzeichnung=False, erlaube_equivocation=False))
def test_p2_subset_never_higher_trust(welt) -> None:
    claims = welt.claims
    voll = speicher(*claims)
    for subset in teilmengen(claims, welt):
        teil = speicher(*subset)
        assert not hoeheres_vertrauen(teil, voll, welt)
