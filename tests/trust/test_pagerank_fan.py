"""T-02b.4 — TP-FAN (Anker PR-4): kein Knoten-Splitting (K13, D49).

Ueber dem gespaltenen 02a-Graphen faellt u(X) anders aus, weil jeder Pfad einen
zusaetzlichen Knoten durchlaeuft und damit einen weiteren (1-alpha)-Faktor bekaeme. Dieser
Test faengt genau diesen Fehler.
"""

from __future__ import annotations

from mensch_als_republik.trust import rank

from tests.helpers import Identity, scope_id, store_with
from .pr02 import RP
from .tp02 import NOW, T_EXP


def test_TP_FAN_no_node_split() -> None:
    scope = scope_id("PR-4-TP-FAN")
    A, B1, B2, X = (Identity(n) for n in ("pr4-A", "pr4-B1", "pr4-B2", "pr4-X"))
    claims = [
        A.vouch(B1, n=2, scope=scope, t=1, t_exp=T_EXP),
        A.vouch(B2, n=2, scope=scope, t=1, t_exp=T_EXP),
        B1.vouch(X, n=4, scope=scope, t=1, t_exp=T_EXP),
        B2.vouch(X, n=4, scope=scope, t=1, t_exp=T_EXP),
    ]
    store = store_with(*claims)
    r = rank(
        store, anchors=frozenset({A.pub}), scope=scope, now=NOW, params=RP,
        include_flagged=True,
    )
    scores = dict(r.scores)

    assert scores[B1.pub] == scores[B2.pub] == 144115188075855872  # Symmetrie
    assert scores[X.pub] == 144115188075855872
    assert r.mass == 7 * (r.denominator // 8)  # exakt, weil 8 den Nenner 2**60 teilt
