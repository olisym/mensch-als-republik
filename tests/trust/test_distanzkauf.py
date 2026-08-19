"""Charakterisierungstest Distanzkauf (D141, 02 §4).

Der Distanzkauf entfernt eine Decke, er traegt keinen Fluss. Eine Kante
minimaler Kapazitaet von einem seed-nahen Knoten hebt die Knotendecke eines
seed-fernen Grenzknotens und gibt damit bereits vorhandenen ehrlichen Fluss
frei. Der Test repariert nichts.
"""

from __future__ import annotations

from mensch_als_republik.atom import Claim, claim_id
from mensch_als_republik.trust import TrustFinding, TrustParams, TrustResult, trust
from mensch_als_republik.trust.derive import Derivation, derive
from mensch_als_republik.trust.graph import capacity
from mensch_als_republik.verifier import InMemoryStore

from tests.helpers import Identity, scope_id, store_with

PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=16)
NOW = 1000
T_EXP = 5000

# Vier Ketten A → a_i → b_i → x_i → h (D141). Distanz von h ohne Angriff ist die Pfadlänge.
N_CHAINS = 4
CHAIN_STEPS = ("a", "b", "x")
D_H_OHNE = len(CHAIN_STEPS) + 1
N_A_TO_AI = 3
N_A_TO_P = PARAMS.D - N_CHAINS * N_A_TO_AI


def _graph(
    n_p_h: int | None,
) -> tuple[InMemoryStore, bytes, Identity, Identity, Identity, Identity, Claim | None]:
    """D141 / 02 §4: Anker A, vier Ketten auf Grenzknoten h, Ziel S, seed-nahes p."""
    scope = scope_id("distanzkauf")
    A = Identity("dk-A")
    h = Identity("dk-h")
    S = Identity("dk-S")
    p = Identity("dk-p")
    claims: list[Claim] = [
        A.vouch(p, n=N_A_TO_P, scope=scope, t=1, t_exp=T_EXP),
        h.vouch(S, n=PARAMS.D, scope=scope, t=1, t_exp=T_EXP),
    ]
    for i in range(N_CHAINS):
        nodes = [Identity(f"dk-{step}-{i}") for step in CHAIN_STEPS]
        claims.append(A.vouch(nodes[0], n=N_A_TO_AI, scope=scope, t=1, t_exp=T_EXP))
        for src, dst in zip(nodes, nodes[1:]):
            claims.append(src.vouch(dst, n=PARAMS.D, scope=scope, t=1, t_exp=T_EXP))
        claims.append(nodes[-1].vouch(h, n=PARAMS.D, scope=scope, t=1, t_exp=T_EXP))
    p_h: Claim | None = None
    if n_p_h is not None:
        p_h = p.vouch(h, n=n_p_h, scope=scope, t=1, t_exp=T_EXP)
        claims.append(p_h)
    return store_with(*claims), scope, A, h, S, p, p_h


def _measure(
    n_p_h: int | None,
) -> tuple[TrustResult, Derivation, Identity, Identity, Claim | None]:
    store, scope, A, h, S, p, p_h = _graph(n_p_h)
    anchors = frozenset({A.pub})
    result = trust(
        store,
        anchors=anchors,
        targets=frozenset({S.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
    )
    derivation = derive(
        store,
        anchors=anchors,
        scope=scope,
        now=NOW,
        params=PARAMS,
    )
    return result, derivation, h, p, p_h


def _n_auf_der_schwelle(derivation: Derivation, p: Identity) -> int:
    """Kleinste n mit cap(p → h) ≥ 1, also (n · C(p)) // D ≥ 1 (02 §2.7 / K8)."""
    C_p = capacity(PARAMS, derivation.bfs.distance[p.pub])
    return (PARAMS.D + C_p - 1) // C_p


def test_ohne_angriff() -> None:
    result, derivation, h, _p, _p_h = _measure(None)
    d_h = derivation.bfs.distance[h.pub]
    C_h = derivation.bfs.node_capacity[h.pub]
    assert d_h == D_H_OHNE
    assert C_h == capacity(PARAMS, D_H_OHNE)
    assert result.value == capacity(PARAMS, D_H_OHNE)
    inflow = sum(e.cap for e in derivation.bfs.edges if e.subject == h.pub)
    assert inflow > C_h
    assert not any(f.kind == TrustFinding.SUBGRANULAR_VOUCH for f in result.findings)


def test_angriff_auf_der_schwelle() -> None:
    honest, honest_derivation, _h0, p0, _ = _measure(None)
    n = _n_auf_der_schwelle(honest_derivation, p0)
    result, derivation, h, p, _p_h = _measure(n)
    d_p = derivation.bfs.distance[p.pub]
    d_h = derivation.bfs.distance[h.pub]
    C_h = derivation.bfs.node_capacity[h.pub]
    C_p = capacity(PARAMS, d_p)
    beitrag_p = (n * C_p) // PARAMS.D
    assert d_h == d_p + 1
    assert C_h == capacity(PARAMS, d_p + 1)
    assert result.value == capacity(PARAMS, d_p + 1)
    von_p = sum(
        e.cap
        for e in derivation.bfs.edges
        if e.author == p.pub and e.subject == h.pub
    )
    assert von_p == beitrag_p
    assert result.value - honest.value > beitrag_p
    assert not any(f.kind == TrustFinding.SUBGRANULAR_VOUCH for f in result.findings)


def test_angriff_unter_der_schwelle() -> None:
    honest, honest_derivation, _h0, p0, _ = _measure(None)
    n = _n_auf_der_schwelle(honest_derivation, p0) - 1
    result, derivation, h, p, p_h = _measure(n)
    d_h = derivation.bfs.distance[h.pub]
    assert d_h == D_H_OHNE
    assert result.value == capacity(PARAMS, D_H_OHNE)
    assert result.value == honest.value
    assert p_h is not None
    sub = [f for f in result.findings if f.kind == TrustFinding.SUBGRANULAR_VOUCH]
    assert len(sub) == 1
    assert sub[0].subject == claim_id(p_h)
    assert not any(e.author == p.pub for e in derivation.bfs.edges)
