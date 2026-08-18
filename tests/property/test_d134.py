"""D134 — gruppenweise Budgetbuchfuehrung unter Equivocation."""

from __future__ import annotations

from hypothesis import given

from mensch_als_republik.index import classify_all
from mensch_als_republik.trust.derive import derive
from mensch_als_republik.trust.findings import TrustFinding
from mensch_als_republik.trust.groups import build_groups

from tests.property.welten import EX, speicher, welten


@given(welten(erlaube_ueberzeichnung=False, erlaube_equivocation=True))
def test_d134_budget_holds_under_equivocation(welt) -> None:
    store = speicher(*welt.claims)
    classifications = classify_all(store, welt.now)
    groups, _ = build_groups(
        store.all_claims(), classifications, EX.N_res, welt.params.D, welt.now
    )
    by_author: dict[bytes, int] = {}
    for (author, _subject), group in groups.items():
        by_author[author] = by_author.get(author, 0) + group.n_budget
    for total in by_author.values():
        assert total <= welt.params.D
    derivation = derive(
        store,
        anchors=welt.anchors,
        scope=EX.N_res,
        now=welt.now,
        params=welt.params,
    )
    assert not any(
        f.kind == TrustFinding.OVERCOMMITTED_AUTHOR for f in derivation.findings
    )
