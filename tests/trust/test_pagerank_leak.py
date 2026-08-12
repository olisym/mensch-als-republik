"""T-02b.5 — Leck / ungenutztes Budget (Anker PR-5, D45).

Entscheidet die sub-stochastische Fassung (K9) gegen die spaltenstochastische: unter
Spaltenstochastik wuerde die Normalisierung ueber Sigma n den absoluten Pegel von w
loeschen, sobald der Autor nur eine Kante traegt, und t(BOB) waere 1/4 statt 1/16.
"""

from __future__ import annotations

from mensch_als_republik.trust import rank

from .helpers import Identity, scope_id, store_with
from .pr02 import RP
from .tp02 import NOW, T_EXP


def test_single_vouch_n_1_of_D_4_leaves_budget_unused() -> None:
    scope = scope_id("PR-5-leak")
    ALICE, BOB = Identity("pr5-ALICE"), Identity("pr5-BOB")
    claims = [ALICE.vouch(BOB, n=1, scope=scope, t=1, t_exp=T_EXP)]
    store = store_with(*claims)
    r = rank(
        store, anchors=frozenset({ALICE.pub}), scope=scope, now=NOW, params=RP,
        include_flagged=True,
    )
    scores = dict(r.scores)

    assert scores[BOB.pub] == 72057594037927936  # 1/16, nicht 1/4 (288230376151711744)
    assert scores[BOB.pub] != 288230376151711744
    assert r.mass == 9 * (r.denominator // 16)  # exakt, weil 16 den Nenner 2**60 teilt
