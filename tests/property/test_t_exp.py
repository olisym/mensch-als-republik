"""Austritt aus dem Budget-Set über die Uhr wird generativ erreicht."""

from __future__ import annotations

from hypothesis import find, settings

from mensch_als_republik.index import classify_all
from mensch_als_republik.trust.groups import build_groups

from tests.property.welten import EX, Welt, speicher, welten


def _austritt_ueber_uhr(welt: Welt) -> bool:
    expired = [c for c in welt.vouches if c.t_exp is not None and c.t_exp < welt.now]
    if not expired:
        return False
    store = speicher(*welt.vouches)
    classifications = classify_all(store, welt.now)
    groups, _findings = build_groups(
        store.all_claims(), classifications, EX.N_res, welt.params.D, welt.now
    )
    return any((c.I, c.J[1]) not in groups for c in expired)


def test_finds_budget_exit_via_clock() -> None:
    welt = find(
        welten(),
        _austritt_ueber_uhr,
        settings=settings(),
    )
    assert _austritt_ueber_uhr(welt)
