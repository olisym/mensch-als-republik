"""Messlauf Deckenelastizität (D141, 02 §4).

Misst, ob Σ_{h ∈ Grenze} C(h) gegen den Zug des Angreifers invariant ist
oder mitwandert. Der Min-Cut-Satz bleibt unberührt — ungemessen war die
Schranke selbst. Der Lauf repariert nichts.
"""

from __future__ import annotations

from symbolon.atom import Claim
from symbolon.trust import TrustFinding, TrustParams, TrustResult, trust
from symbolon.trust.derive import Derivation, derive
from symbolon.trust.graph import capacity
from symbolon.verifier import InMemoryStore

from tests.helpers import Identity, scope_id, store_with

PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=16)
NOW = 1000
T_EXP = 5000

N_A_TO_P = 4
CHAIN_STEPS = ("a", "b", "x")
D_H_FERN = len(CHAIN_STEPS) + 1
# A → h ist eine einzelne Kante.
D_H_NAH = 1

N_CHAINS_A = 4
N_A_TO_AI_A = 3
N_P_H_A = 2

N_A_TO_H_B = 1
N_P_H_B = PARAMS.D

K_VALUES = (1, 2, 3)
N_CHAINS_PER_H = 2
N_A_TO_AI_C = 2
N_P_H_C = 2


def _vouch(author: Identity, subject: Identity, n: int, scope: bytes) -> Claim:
    return author.vouch(subject, n=n, scope=scope, t=1, t_exp=T_EXP)


def _run(
    store: InMemoryStore,
    A: Identity,
    targets: frozenset[bytes],
    scope: bytes,
) -> tuple[TrustResult, Derivation]:
    anchors = frozenset({A.pub})
    result = trust(
        store,
        anchors=anchors,
        targets=targets,
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
    return result, derivation


def _sigma(derivation: Derivation, grenze: tuple[bytes, ...]) -> int:
    return sum(derivation.bfs.node_capacity[pub] for pub in grenze)


def _beitrag_p(
    derivation: Derivation,
    A: Identity,
    p: Identity,
    grenze: tuple[bytes, ...],
) -> int:
    """min(cap(A→p), Σ cap(p→h)): zugefuehrter Fluss (02 §4).

    02 §3, Nachtrag seit D1: unter gueltigem Budget ist die interne Knotenkante
    nie allein bindend, der Term C(p) ist redundant.
    """
    cap_a_p = sum(
        e.cap
        for e in derivation.bfs.edges
        if e.author == A.pub and e.subject == p.pub
    )
    cap_p_grenze = sum(
        e.cap
        for e in derivation.bfs.edges
        if e.author == p.pub and e.subject in grenze
    )
    return min(cap_a_p, cap_p_grenze)


def _graph_a(
    n_p_h: int | None,
) -> tuple[InMemoryStore, bytes, Identity, Identity, Identity, Identity]:
    """D141-Topologie: vier Ketten auf h, Ziel S, seed-nahes p (02 §4)."""
    scope = scope_id("decken-a")
    A = Identity("dea-A")
    h = Identity("dea-h")
    S = Identity("dea-S")
    p = Identity("dea-p")
    claims: list[Claim] = [
        _vouch(A, p, N_A_TO_P, scope),
        _vouch(h, S, PARAMS.D, scope),
    ]
    for i in range(N_CHAINS_A):
        nodes = [Identity(f"dea-{step}-{i}") for step in CHAIN_STEPS]
        claims.append(_vouch(A, nodes[0], N_A_TO_AI_A, scope))
        for src, dst in zip(nodes, nodes[1:]):
            claims.append(_vouch(src, dst, PARAMS.D, scope))
        claims.append(_vouch(nodes[-1], h, PARAMS.D, scope))
    if n_p_h is not None:
        claims.append(_vouch(p, h, n_p_h, scope))
    return store_with(*claims), scope, A, h, S, p


def _graph_b(
    n_p_h: int | None,
    *,
    n_a_p: int = N_A_TO_P,
) -> tuple[InMemoryStore, bytes, Identity, Identity, Identity, Identity]:
    """Kontrollfall: h sitzt seed-nah und ausgehungert (02 §4)."""
    scope = scope_id("decken-b")
    A = Identity("deb-A")
    h = Identity("deb-h")
    S = Identity("deb-S")
    p = Identity("deb-p")
    claims: list[Claim] = [
        _vouch(A, h, N_A_TO_H_B, scope),
        _vouch(A, p, n_a_p, scope),
        _vouch(h, S, PARAMS.D, scope),
    ]
    if n_p_h is not None:
        claims.append(_vouch(p, h, n_p_h, scope))
    return store_with(*claims), scope, A, h, S, p


def _graph_c(
    k: int,
    n_p_h: int | None,
) -> tuple[InMemoryStore, bytes, Identity, Identity, tuple[Identity, ...], tuple[Identity, ...]]:
    """k Grenzknoten mit je zwei Ketten, Multi-Sink über {S_j} (VR-02.1)."""
    scope = scope_id(f"decken-c-{k}")
    A = Identity(f"dec-{k}-A")
    p = Identity(f"dec-{k}-p")
    hs = tuple(Identity(f"dec-{k}-h-{j}") for j in range(k))
    Ss = tuple(Identity(f"dec-{k}-S-{j}") for j in range(k))
    claims: list[Claim] = [_vouch(A, p, N_A_TO_P, scope)]
    for j, h in enumerate(hs):
        claims.append(_vouch(h, Ss[j], PARAMS.D, scope))
        for i in range(N_CHAINS_PER_H):
            nodes = [Identity(f"dec-{k}-{step}-{j}-{i}") for step in CHAIN_STEPS]
            claims.append(_vouch(A, nodes[0], N_A_TO_AI_C, scope))
            for src, dst in zip(nodes, nodes[1:]):
                claims.append(_vouch(src, dst, PARAMS.D, scope))
            claims.append(_vouch(nodes[-1], h, PARAMS.D, scope))
        if n_p_h is not None:
            claims.append(_vouch(p, h, n_p_h, scope))
    return store_with(*claims), scope, A, p, hs, Ss


def _keine_budget_oder_granular_findings(result: TrustResult) -> None:
    kinds = {f.kind for f in result.findings}
    assert TrustFinding.OVERCOMMITTED_AUTHOR not in kinds
    assert TrustFinding.SUBGRANULAR_VOUCH not in kinds


def _ratio_a() -> int:
    store_ohne, scope, A, h, S, p = _graph_a(None)
    res_ohne, _der_ohne = _run(store_ohne, A, frozenset({S.pub}), scope)
    store_mit, scope, A, h, S, p = _graph_a(N_P_H_A)
    res_mit, der_mit = _run(store_mit, A, frozenset({S.pub}), scope)
    grenze = (h.pub,)
    beitrag = _beitrag_p(der_mit, A, p, grenze)
    return (res_mit.value - res_ohne.value) // beitrag


def test_fall_a_distanzkauf() -> None:
    store_ohne, scope, A, h, S, p = _graph_a(None)
    grenze = (h.pub,)
    res_ohne, der_ohne = _run(store_ohne, A, frozenset({S.pub}), scope)
    d_h_ohne = der_ohne.bfs.distance[h.pub]
    sigma_ohne = _sigma(der_ohne, grenze)

    store_mit, scope, A, h, S, p = _graph_a(N_P_H_A)
    res_mit, der_mit = _run(store_mit, A, frozenset({S.pub}), scope)
    d_p = der_mit.bfs.distance[p.pub]
    d_h_mit = der_mit.bfs.distance[h.pub]
    sigma_mit = _sigma(der_mit, grenze)
    beitrag = _beitrag_p(der_mit, A, p, grenze)

    assert d_h_ohne == D_H_FERN
    assert d_h_mit == d_p + 1
    assert d_h_mit < d_h_ohne
    assert d_p < d_h_ohne - 1
    assert sigma_ohne == capacity(PARAMS, D_H_FERN)
    assert sigma_mit == capacity(PARAMS, d_h_mit)
    assert res_ohne.value == capacity(PARAMS, D_H_FERN)
    assert res_mit.value == capacity(PARAMS, d_h_mit)
    assert res_ohne.value == sigma_ohne
    assert res_mit.value == sigma_mit
    assert res_mit.value - res_ohne.value > beitrag
    assert any(e.author == p.pub and e.subject in grenze for e in der_mit.bfs.edges)
    _keine_budget_oder_granular_findings(res_ohne)
    _keine_budget_oder_granular_findings(res_mit)


def test_fall_b_kapazitaetsspende() -> None:
    store_ohne, scope, A, h, S, p = _graph_b(None)
    grenze = (h.pub,)
    res_ohne, der_ohne = _run(store_ohne, A, frozenset({S.pub}), scope)
    d_h_ohne = der_ohne.bfs.distance[h.pub]
    sigma_ohne = _sigma(der_ohne, grenze)
    d_A = der_ohne.bfs.distance[A.pub]
    value_ohne_erwartet = (N_A_TO_H_B * capacity(PARAMS, d_A)) // PARAMS.D

    store_mit, scope, A, h, S, p = _graph_b(N_P_H_B)
    res_mit, der_mit = _run(store_mit, A, frozenset({S.pub}), scope)
    d_h_mit = der_mit.bfs.distance[h.pub]
    sigma_mit = _sigma(der_mit, grenze)
    beitrag = _beitrag_p(der_mit, A, p, grenze)
    cap_a_p = sum(
        e.cap for e in der_mit.bfs.edges
        if e.author == A.pub and e.subject == p.pub
    )
    cap_p_h = sum(
        e.cap for e in der_mit.bfs.edges
        if e.author == p.pub and e.subject in grenze
    )

    assert d_h_ohne == D_H_NAH
    assert d_h_mit == D_H_NAH
    assert sigma_ohne == capacity(PARAMS, D_H_NAH)
    assert sigma_mit == sigma_ohne
    assert res_ohne.value == value_ohne_erwartet
    assert res_mit.value == value_ohne_erwartet + beitrag
    assert res_ohne.value < sigma_ohne
    assert res_mit.value < sigma_mit
    assert res_mit.value - res_ohne.value == beitrag
    assert beitrag == cap_a_p
    assert beitrag < cap_p_h
    assert any(e.author == p.pub and e.subject in grenze for e in der_mit.bfs.edges)
    _keine_budget_oder_granular_findings(res_ohne)
    _keine_budget_oder_granular_findings(res_mit)


def test_fall_b2_gesaettigte_spende() -> None:
    n_a_p = PARAMS.D - N_A_TO_H_B
    store_ohne, scope, A, h, S, p = _graph_b(None, n_a_p=n_a_p)
    grenze = (h.pub,)
    res_ohne, der_ohne = _run(store_ohne, A, frozenset({S.pub}), scope)
    d_h_ohne = der_ohne.bfs.distance[h.pub]
    sigma_ohne = _sigma(der_ohne, grenze)

    store_mit, scope, A, h, S, p = _graph_b(N_P_H_B, n_a_p=n_a_p)
    res_mit, der_mit = _run(store_mit, A, frozenset({S.pub}), scope)
    d_h_mit = der_mit.bfs.distance[h.pub]
    sigma_mit = _sigma(der_mit, grenze)
    beitrag = _beitrag_p(der_mit, A, p, grenze)
    cap_a_p = sum(
        e.cap for e in der_mit.bfs.edges
        if e.author == A.pub and e.subject == p.pub
    )
    cap_p_h = sum(
        e.cap for e in der_mit.bfs.edges
        if e.author == p.pub and e.subject in grenze
    )

    assert d_h_ohne == D_H_NAH
    assert d_h_mit == D_H_NAH
    assert sigma_ohne == capacity(PARAMS, D_H_NAH)
    assert sigma_mit == sigma_ohne
    assert beitrag == cap_p_h
    assert beitrag < cap_a_p
    assert res_ohne.value < sigma_ohne
    assert res_mit.value == sigma_mit
    assert res_mit.value - res_ohne.value < beitrag
    assert any(e.author == p.pub and e.subject in grenze for e in der_mit.bfs.edges)
    _keine_budget_oder_granular_findings(res_ohne)
    _keine_budget_oder_granular_findings(res_mit)


def test_fall_c_skalierung() -> None:
    ratio_a = _ratio_a()
    ratios: list[int] = []
    spent_A_last = 0
    for k in K_VALUES:
        spent_A = N_A_TO_P + k * N_CHAINS_PER_H * N_A_TO_AI_C
        spent_p = k * N_P_H_C
        assert spent_A <= PARAMS.D
        assert spent_p <= PARAMS.D
        spent_A_last = spent_A

        store_ohne, scope, A, p, hs, Ss = _graph_c(k, None)
        grenze = tuple(h.pub for h in hs)
        targets = frozenset(S.pub for S in Ss)
        res_ohne, der_ohne = _run(store_ohne, A, targets, scope)
        sigma_ohne = _sigma(der_ohne, grenze)

        store_mit, scope, A, p, hs, Ss = _graph_c(k, N_P_H_C)
        res_mit, der_mit = _run(store_mit, A, targets, scope)
        sigma_mit = _sigma(der_mit, grenze)
        d_p = der_mit.bfs.distance[p.pub]
        d_h_mit = der_mit.bfs.distance[hs[0].pub]
        beitrag = _beitrag_p(der_mit, A, p, grenze)
        beitrag_erwartet = k * ((N_P_H_C * capacity(PARAMS, d_p)) // PARAMS.D)

        for h in hs:
            assert der_ohne.bfs.distance[h.pub] == D_H_FERN
            assert der_mit.bfs.distance[h.pub] == d_h_mit
            assert der_mit.bfs.distance[h.pub] < D_H_FERN
        assert d_h_mit == d_p + 1
        assert d_p < D_H_FERN - 1
        assert sigma_ohne == k * capacity(PARAMS, D_H_FERN)
        assert sigma_mit == k * capacity(PARAMS, d_h_mit)
        assert res_ohne.value == k * capacity(PARAMS, D_H_FERN)
        assert res_mit.value == k * capacity(PARAMS, d_h_mit)
        assert beitrag == beitrag_erwartet
        zuwachs = res_mit.value - res_ohne.value
        assert beitrag != 0
        assert zuwachs % beitrag == 0
        ratios.append(zuwachs // beitrag)
        assert any(e.author == p.pub and e.subject in grenze for e in der_mit.bfs.edges)
        _keine_budget_oder_granular_findings(res_ohne)
        _keine_budget_oder_granular_findings(res_mit)

    assert spent_A_last == PARAMS.D
    assert len(set(ratios)) == 1
    assert ratios[0] == ratio_a
