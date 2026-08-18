"""P-5 — Die sichere Richtung der Auszählung (werkzeuge.md §4.2, INV-04.3).

Teilwissen erzeugt nie PASSED, wo Vollwissen es nicht tut.

Vorbehalt: ``erlaube_equivocation = False`` (D117).
"""

from __future__ import annotations

from hypothesis import given

from mensch_als_republik.governance.tally import TallyState

from tests.property.welten import auszaehlung, speicher, teilmengen, welten


@given(welten(erlaube_ueberzeichnung=False, erlaube_equivocation=False))
def test_p5_partial_knowledge_never_passed_alone(welt) -> None:
    claims = welt.claims
    voll = auszaehlung(speicher(*claims), welt)
    for subset in teilmengen(claims, welt):
        teil = auszaehlung(speicher(*subset), welt)
        if teil.state is TallyState.PASSED:
            assert voll.state is TallyState.PASSED
