"""resolve_current_key — Lagen aus 00 §6.4 und D125, D149, D152–D155."""

from __future__ import annotations

from mensch_als_republik.atom import claim_id
from mensch_als_republik.index import classify_all
from mensch_als_republik.keys import resolve_current_key
from mensch_als_republik.policy import NucleusPolicy
from mensch_als_republik.verifier import State
from tests.helpers import Identity, scope_id, store_with

NOW = 1000


def _nuc(scope: bytes, name: str) -> str:
    return f"nuc:{scope.hex()}/{name}@1"


def _rotate(author: Identity, successor: Identity, scope: bytes, *, t: int):
    return author.claim(
        p=_nuc(scope, "rotate-key"),
        J=(1, successor.pub),
        t=t,
        N=scope,
    )


def _ack(successor: Identity, rotate, scope: bytes, *, t: int):
    return successor.claim(
        p=_nuc(scope, "rotate-ack"),
        J=(2, claim_id(rotate)),
        t=t,
        N=scope,
    )


def _resolve(store, scope: bytes, *keys: Identity):
    return resolve_current_key(
        store,
        scope=scope,
        anchor_keys=frozenset(k.pub for k in keys),
        now=NOW,
    )


def test_no_rotate_returns_anchor_keys() -> None:
    """Kein Rotate im Store: Ergebnis ist anchor_keys."""
    scope = scope_id("rk-1")
    root = Identity("rk-1-root")
    assert _resolve(store_with(), scope, root) == frozenset({root.pub})


def test_complete_rotation_head_is_successor() -> None:
    """Eine vollständige Rotation: Ergebnis ist der Nachfolger, nicht die Wurzel."""
    scope = scope_id("rk-2")
    root = Identity("rk-2-root")
    nxt = Identity("rk-2-next")
    rotate = _rotate(root, nxt, scope, t=1)
    ack = _ack(nxt, rotate, scope, t=2)
    got = _resolve(store_with(rotate, ack), scope, root)
    assert nxt.pub in got
    assert root.pub not in got
    assert got == frozenset({nxt.pub})


def test_rotate_without_ack_stays_at_root() -> None:
    """Rotate ohne Ack: Ergebnis bleibt die Wurzel (D125)."""
    scope = scope_id("rk-3")
    root = Identity("rk-3-root")
    nxt = Identity("rk-3-next")
    rotate = _rotate(root, nxt, scope, t=1)
    assert _resolve(store_with(rotate), scope, root) == frozenset({root.pub})


def test_ack_from_predecessor_is_incomplete() -> None:
    """Ack vom Vorgängerschlüssel statt vom Nachfolger: unvollständig (D152)."""
    scope = scope_id("rk-4")
    root = Identity("rk-4-root")
    nxt = Identity("rk-4-next")
    rotate = _rotate(root, nxt, scope, t=1)
    ack = root.claim(
        p=_nuc(scope, "rotate-ack"),
        J=(2, claim_id(rotate)),
        t=2,
        N=scope,
    )
    assert _resolve(store_with(rotate, ack), scope, root) == frozenset({root.pub})


def test_ack_with_foreign_n_is_incomplete() -> None:
    """Ack mit fremdem N: unvollständig (D152, vierte Bedingung)."""
    scope = scope_id("rk-5")
    other = scope_id("rk-5-other")
    root = Identity("rk-5-root")
    nxt = Identity("rk-5-next")
    rotate = _rotate(root, nxt, scope, t=1)
    ack = nxt.claim(
        p=_nuc(other, "rotate-ack"),
        J=(2, claim_id(rotate)),
        t=2,
        N=other,
    )
    assert _resolve(store_with(rotate, ack), scope, root) == frozenset({root.pub})


def test_ack_as_revoke_is_incomplete() -> None:
    """Ack als core/revoke@1 statt rotate-ack@1: unvollständig (D152).

    ``K_n``-signiertes ``core/revoke@1`` auf den Rotate von ``K_{n-1}`` wirft
    ``ForeignLifecycle`` in ``classify_all`` (Layer 01). Der Test zeigt denselben
    Defekt mit einem klassifizierbaren Widerruf desselben Autors.
    """
    scope = scope_id("rk-6")
    root = Identity("rk-6-root")
    nxt = Identity("rk-6-next")
    rotate = _rotate(root, nxt, scope, t=1)
    fake = root.revoke(rotate, t=2)
    assert _resolve(store_with(rotate, fake), scope, root) == frozenset({root.pub})


def test_rotate_with_claim_ref_j_is_invalid() -> None:
    """Rotate mit J.tag == claim-ref statt identity: kein gültiger Rotate (D152)."""
    scope = scope_id("rk-7")
    root = Identity("rk-7-root")
    nxt = Identity("rk-7-next")
    rotate = root.claim(
        p=_nuc(scope, "rotate-key"),
        J=(2, nxt.pub),
        t=1,
        N=scope,
    )
    ack = _ack(nxt, rotate, scope, t=2)
    assert _resolve(store_with(rotate, ack), scope, root) == frozenset({root.pub})


def test_two_roots_one_rotated_both_heads() -> None:
    """Zwei Wurzeln, eine rotiert: Ergebnis enthält beide Köpfe (D149)."""
    scope = scope_id("rk-8")
    a = Identity("rk-8-a")
    b = Identity("rk-8-b")
    nxt = Identity("rk-8-next")
    rotate = _rotate(a, nxt, scope, t=1)
    ack = _ack(nxt, rotate, scope, t=2)
    got = _resolve(store_with(rotate, ack), scope, a, b)
    assert got == frozenset({nxt.pub, b.pub})


def test_equivocation_at_chain_point_drops_that_root() -> None:
    """Equivocation an einem Kettenpunkt: diese Wurzel liefert nichts, die andere weiter (D155)."""
    scope = scope_id("rk-9")
    a1 = Identity("rk-9-a")
    a2 = Identity("rk-9-a")
    other = Identity("rk-9-b")
    s1 = Identity("rk-9-s1")
    s2 = Identity("rk-9-s2")
    r1 = _rotate(a1, s1, scope, t=1)
    r2 = _rotate(a2, s2, scope, t=1)
    got = _resolve(store_with(r1, r2), scope, a1, other)
    assert a1.pub not in got
    assert s1.pub not in got
    assert s2.pub not in got
    assert got == frozenset({other.pub})


def test_two_complete_rotates_earlier_binds_with_link() -> None:
    """Zwei vollständige Rotationen, Zwischenglied vorhanden: die frühere bindet (D154)."""
    scope = scope_id("rk-10")
    root = Identity("rk-10-root")
    first = Identity("rk-10-first")
    second = Identity("rk-10-second")
    filler = Identity("rk-10-filler")
    r_a = _rotate(root, first, scope, t=1)
    mid = root.claim(
        p=_nuc(scope, "obligation"),
        J=(1, filler.pub),
        t=2,
        N=scope,
    )
    r_b = _rotate(root, second, scope, t=3)
    ack_a = _ack(first, r_a, scope, t=4)
    ack_b = _ack(second, r_b, scope, t=5)
    got = _resolve(store_with(r_a, mid, r_b, ack_a, ack_b), scope, root)
    assert got == frozenset({first.pub})


def test_two_complete_rotates_incomparable_without_link() -> None:
    """Dieselbe Lage ohne Zwischenglied im Store: kein Kopf aus dieser Wurzel (D155 a).

    Messung: der spätere Rotate ist ``PENDING`` (Vorgänger fehlt), nur die frühere
    Rotation ist vollständig — der Kopf ist deren Nachfolger, nicht die leere Menge.
    """
    scope = scope_id("rk-11")
    root = Identity("rk-11-root")
    first = Identity("rk-11-first")
    second = Identity("rk-11-second")
    filler = Identity("rk-11-filler")
    r_a = _rotate(root, first, scope, t=1)
    root.claim(
        p=_nuc(scope, "obligation"),
        J=(1, filler.pub),
        t=2,
        N=scope,
    )
    r_b = _rotate(root, second, scope, t=3)
    ack_a = _ack(first, r_a, scope, t=4)
    ack_b = _ack(second, r_b, scope, t=5)
    store = store_with(r_a, r_b, ack_a, ack_b)
    classified = classify_all(store, NOW, NucleusPolicy(scope=scope))
    assert classified[claim_id(r_b)].state is State.PENDING
    got = _resolve(store, scope, root)
    assert got == frozenset({first.pub})


def test_head_rewinds_when_earlier_ack_arrives() -> None:
    """Rücksprung unter Wissenszuwachs (D154): beide Ergebnisse, nicht nur das zweite."""
    scope = scope_id("rk-12")
    root = Identity("rk-12-root")
    first = Identity("rk-12-first")
    second = Identity("rk-12-second")
    filler = Identity("rk-12-filler")
    r_a = _rotate(root, first, scope, t=1)
    mid = root.claim(
        p=_nuc(scope, "obligation"),
        J=(1, filler.pub),
        t=2,
        N=scope,
    )
    r_b = _rotate(root, second, scope, t=3)
    ack_a = _ack(first, r_a, scope, t=4)
    ack_b = _ack(second, r_b, scope, t=5)
    store = store_with(r_a, mid, r_b, ack_b)
    later_only = _resolve(store, scope, root)
    store.add(ack_a)
    after_earlier = _resolve(store, scope, root)
    assert later_only == frozenset({second.pub})
    assert after_earlier == frozenset({first.pub})
    assert later_only != after_earlier


def test_cycle_yields_no_head_and_terminates() -> None:
    """Zyklus K_1 → K_2 → K_1: kein Kopf, Lauf terminiert (D155 d)."""
    scope = scope_id("rk-13")
    k1 = Identity("rk-13-k1")
    k2 = Identity("rk-13-k2")
    r12 = _rotate(k1, k2, scope, t=1)
    r21 = _rotate(k2, k1, scope, t=2)
    a12 = _ack(k2, r12, scope, t=3)
    a21 = _ack(k1, r21, scope, t=4)
    got = _resolve(store_with(r12, r21, a12, a21), scope, k1)
    assert got == frozenset()


def test_expired_rotate_still_counts() -> None:
    """Rotate mit gesetztem t_exp, now darüber hinaus: zählt weiter (D155 c)."""
    scope = scope_id("rk-14")
    root = Identity("rk-14-root")
    nxt = Identity("rk-14-next")
    rotate = root.claim(
        p=_nuc(scope, "rotate-key"),
        J=(1, nxt.pub),
        t=1,
        N=scope,
        t_exp=50,
    )
    ack = _ack(nxt, rotate, scope, t=2)
    classified = classify_all(store_with(rotate, ack), NOW)
    assert classified[claim_id(rotate)].state is State.EXPIRED
    got = _resolve(store_with(rotate, ack), scope, root)
    assert got == frozenset({nxt.pub})
