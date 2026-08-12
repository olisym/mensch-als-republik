"""T-02b.6 — TP-BOOT (Anker PR-6).

Die asymmetrische Kantenverteilung (11/12/11 ueber die Gruender) darf sich nicht auswirken
-- unter spaltenstochastischer Normalisierung haette F1 (12 Kanten) je Neuling weniger
verteilt als F0/F2 (11 Kanten).
"""

from __future__ import annotations

from mensch_als_republik.trust import RelaxParams, TrustParams, rank

from .helpers import Identity, scope_id, store_with

PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=24)
RP = RelaxParams(base=PARAMS, alpha_num=1, alpha_den=2, rounds=20)


def _build():
    scope = scope_id("PR-6-TP-BOOT")
    founders = [Identity(f"pr6-F{i}") for i in range(3)]
    newcomers = [Identity(f"pr6-N{i}") for i in range(17)]
    pairs = [(0, 1), (0, 2), (1, 2)]
    voucher_sets = [list(pairs[i % 3]) for i in range(17)]
    claims = []
    for newcomer, vouchers in zip(newcomers, voucher_sets):
        for idx in vouchers:
            claims.append(founders[idx].vouch(newcomer, n=2, scope=scope, t=1, t_exp=5000))
    return scope, founders, newcomers, store_with(*claims)


def test_bootstrap_founders_and_newcomers() -> None:
    scope, founders, newcomers, store = _build()
    anchors = frozenset(f.pub for f in founders)
    r = rank(store, anchors=anchors, scope=scope, now=1000, params=RP, include_flagged=True)
    scores = dict(r.scores)

    assert r.denominator == 3 * 48**20

    founder_values = {scores[f.pub] for f in founders}
    assert founder_values == {2107631844899214418882499117580288}

    newcomer_values = {scores[n.pub] for n in newcomers}
    assert newcomer_values == {175635987074934534906874926465024}

    assert min(founder_values) > max(newcomer_values)


def test_bootstrap_edge_asymmetry_11_12_11_has_no_effect() -> None:
    """Alle 17 Neulinge tragen exakt denselben Wert, unabhaengig davon, ueber welches der
    drei Gruender-Paare (mit 11 bzw. 12 Kanten insgesamt je Gruender) sie angebunden sind."""
    scope, founders, newcomers, store = _build()
    anchors = frozenset(f.pub for f in founders)
    r = rank(store, anchors=anchors, scope=scope, now=1000, params=RP, include_flagged=True)
    scores = dict(r.scores)
    values = [scores[n.pub] for n in newcomers]
    assert len(set(values)) == 1
