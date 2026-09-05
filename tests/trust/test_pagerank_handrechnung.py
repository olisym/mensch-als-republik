"""T-02b.8 — Handrechnung: die azyklische Kette gegen die Formel, nicht gegen Literale.

t(ALICE) = alpha
t(BOB)   = (1-alpha) * t(ALICE) * (4/4)
t(CAROL) = (1-alpha) * t(BOB)   * (4/4)

Als Integer-Identitaeten ueber Delta, kreuzmultipliziert um Division zu vermeiden:
u(J) * (b*D) == (b-a) * n * u(I)  fuer eine einzelne eingehende Kante I->J mit Gewicht n.

Wenn dieser Test und T-02b.1 gleichzeitig gruen sind, ist die Rekursion richtig verdrahtet.
"""

from __future__ import annotations

from symbolon.trust import rank

from .pr02 import RP
from .tp02 import NOW, build


def test_handrechnung_acyclic_chain() -> None:
    g = build("B")  # Rumpf ALICE->BOB->CAROL ist in allen Varianten identisch
    r = rank(
        g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    scores = dict(r.scores)
    a, b, D = RP.alpha_num, RP.alpha_den, RP.base.D

    u_alice = scores[g.ALICE.pub]
    u_bob = scores[g.BOB.pub]
    u_carol = scores[g.CAROL.pub]

    # t(ALICE) = alpha  <=>  u(ALICE) * b == a * Delta   (|A| = 1)
    assert u_alice * b == a * r.denominator

    # t(BOB) = (1-alpha) * t(ALICE) * (4/4)  <=>  u(BOB)*b*D == (b-a)*4*u(ALICE)
    assert u_bob * b * D == (b - a) * 4 * u_alice

    # t(CAROL) = (1-alpha) * t(BOB) * (4/4)  <=>  u(CAROL)*b*D == (b-a)*4*u(BOB)
    assert u_carol * b * D == (b - a) * 4 * u_bob
