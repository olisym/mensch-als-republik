"""Austritt aus dem Budget-Set über die Uhr wird generativ erreicht."""

from __future__ import annotations

from hypothesis import find, settings

from symbolon.index import classify_all
from symbolon.trust.groups import build_groups

from tests.property.welten import EX, Welt, speicher, welten


def _austritt_ueber_uhr(welt: Welt) -> bool:
    expired = [c.t_exp for c in welt.vouches if c.t_exp is not None and c.t_exp < welt.now]
    if not expired:
        return False
    now_b = min(expired) - 1
    if now_b < 1:
        now_b = 1
    store = speicher(*welt.vouches)
    class_a = classify_all(store, welt.now)
    groups_a, _findings_a = build_groups(
        store.all_claims(), class_a, EX.N_res, welt.params.D, welt.now
    )
    class_b = classify_all(store, now_b)
    groups_b, _findings_b = build_groups(
        store.all_claims(), class_b, EX.N_res, welt.params.D, now_b
    )
    return set(groups_a) < set(groups_b)


def test_finds_budget_exit_via_clock() -> None:
    welt = find(
        welten(),
        _austritt_ueber_uhr,
        settings=settings(max_examples=200, derandomize=True, deadline=None),
    )
    assert _austritt_ueber_uhr(welt)
