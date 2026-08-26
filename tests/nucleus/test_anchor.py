"""resolve_authorized_keys — Lagen aus 00 §5.4, 00 §6.4 und D150, D161, D163, D164."""

from __future__ import annotations

import hashlib

import pytest

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import claim_id
from mensch_als_republik.domains import DOM_NUC_GEN
from mensch_als_republik.findings import Finding, NucleusFinding
from mensch_als_republik.keys import resolve_authorized_keys
from mensch_als_republik.policy import constitution_hash
from tests.helpers import Identity, store_with

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


def _world(root_keys: list[bytes], constitution: dict):
    ch = constitution_hash(constitution)
    genesis = {
        0: 1,
        1: list(root_keys),
        2: 0,
        3: list(root_keys),
        4: ch,
        5: 2,
        6: 0,
        7: 0,
    }
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    return scope, genesis, ch


def _resolve(store, scope, genesis, ch, constitution):
    return resolve_authorized_keys(
        store,
        scope=scope,
        genesis_obj=genesis,
        constitution_hash=ch,
        constitution_obj=constitution,
        now=NOW,
    )


def test_a_constitution_without_nucleus_keys_uses_root_keys() -> None:
    """Verfassung ohne nucleus_keys: Anker ist root_keys, keine Vermerke."""
    root = Identity("ank-a-root")
    other = Identity("ank-a-other")
    constitution: dict = {}
    scope, genesis, ch = _world([root.pub, other.pub], constitution)
    result = _resolve(store_with(), scope, genesis, ch, constitution)
    assert result.keys == frozenset({root.pub, other.pub})
    assert result.findings == ()


def test_b_nucleus_keys_replaces_root_keys() -> None:
    """nucleus_keys mit zwei wohlgeformten Einträgen ersetzt root_keys, vereinigt nicht (D150)."""
    root = Identity("ank-b-root")
    other = Identity("ank-b-other")
    y1 = Identity("ank-b-y1")
    y2 = Identity("ank-b-y2")
    constitution = {"nucleus_keys": [y1.pub, y2.pub]}
    scope, genesis, ch = _world([root.pub, other.pub], constitution)
    result = _resolve(store_with(), scope, genesis, ch, constitution)
    assert result.keys == frozenset({y1.pub, y2.pub})
    assert root.pub not in result.keys
    assert other.pub not in result.keys
    assert result.findings == ()


def test_c_empty_nucleus_keys_is_empty_not_root_keys() -> None:
    """nucleus_keys = []: leere Menge, nicht root_keys (D163, 00 §5.4)."""
    root = Identity("ank-c-root")
    constitution = {"nucleus_keys": []}
    scope, genesis, ch = _world([root.pub], constitution)
    result = _resolve(store_with(), scope, genesis, ch, constitution)
    assert result.keys == frozenset()
    assert root.pub not in result.keys
    assert result.findings == ()


def test_d_one_malformed_entry_keeps_well_formed() -> None:
    """Ein formwidriger Eintrag neben einem wohlgeformten: der wohlgeformte wirkt, ein Vermerk (D163)."""
    root = Identity("ank-d-root")
    y = Identity("ank-d-y")
    constitution = {"nucleus_keys": [y.pub, 42]}
    scope, genesis, ch = _world([root.pub], constitution)
    result = _resolve(store_with(), scope, genesis, ch, constitution)
    assert result.keys == frozenset({y.pub})
    assert result.findings == (
        Finding(NucleusFinding.MALFORMED_NUCLEUS_KEY, ch),
    )


def test_e_two_malformed_entries_one_finding() -> None:
    """Zwei formwidrige Einträge neben einem wohlgeformten: weiterhin genau ein Vermerk (D163)."""
    root = Identity("ank-e-root")
    y = Identity("ank-e-y")
    constitution = {"nucleus_keys": [y.pub, 42, "nope"]}
    scope, genesis, ch = _world([root.pub], constitution)
    result = _resolve(store_with(), scope, genesis, ch, constitution)
    assert result.keys == frozenset({y.pub})
    assert result.findings == (
        Finding(NucleusFinding.MALFORMED_NUCLEUS_KEY, ch),
    )


def test_f_all_entries_malformed_empty_not_root_keys() -> None:
    """Alle Einträge formwidrig: leere Menge, nicht root_keys, Vermerk gesetzt (D163)."""
    root = Identity("ank-f-root")
    constitution = {"nucleus_keys": [42, "nope"]}
    scope, genesis, ch = _world([root.pub], constitution)
    result = _resolve(store_with(), scope, genesis, ch, constitution)
    assert result.keys == frozenset()
    assert root.pub not in result.keys
    assert result.findings == (
        Finding(NucleusFinding.MALFORMED_NUCLEUS_KEY, ch),
    )


def test_g_nucleus_keys_str_empty_with_finding() -> None:
    """nucleus_keys ist ein str: leere Menge, Vermerk gesetzt (D163)."""
    root = Identity("ank-g-root")
    constitution = {"nucleus_keys": "not-a-list"}
    scope, genesis, ch = _world([root.pub], constitution)
    result = _resolve(store_with(), scope, genesis, ch, constitution)
    assert result.keys == frozenset()
    assert root.pub not in result.keys
    assert result.findings == (
        Finding(NucleusFinding.MALFORMED_NUCLEUS_KEY, ch),
    )


def test_h_missing_constitution_uses_root_keys_with_finding() -> None:
    """constitution_obj=None: root_keys plus CONSTITUTION_UNAVAILABLE (D164)."""
    root = Identity("ank-h-root")
    other = Identity("ank-h-other")
    constitution: dict = {}
    scope, genesis, ch = _world([root.pub, other.pub], constitution)
    result = _resolve(store_with(), scope, genesis, ch, None)
    assert result.keys == frozenset({root.pub, other.pub})
    assert result.findings == (
        Finding(NucleusFinding.CONSTITUTION_UNAVAILABLE, ch),
    )


def test_i_constitution_hash_mismatch_raises() -> None:
    """constitution_hash passt nicht zu constitution_obj: ValueError (D161)."""
    root = Identity("ank-i-root")
    constitution: dict = {}
    scope, genesis, ch = _world([root.pub], constitution)
    other = {"nucleus_keys": []}
    with pytest.raises(ValueError):
        _resolve(store_with(), scope, genesis, ch, other)


def test_j_scope_mismatch_raises() -> None:
    """scope passt nicht zu genesis_obj: ValueError (D161)."""
    root = Identity("ank-j-root")
    constitution: dict = {}
    _scope, genesis, ch = _world([root.pub], constitution)
    with pytest.raises(ValueError):
        _resolve(store_with(), bytes(32), genesis, ch, constitution)


def test_k_malformed_genesis_root_keys_raises() -> None:
    """genesis_obj ohne Schlüssel 1, Eintrag falscher Länge, Eintrag kein bytes: je ValueError (D161)."""
    root = Identity("ank-k-root")
    ch = bytes(32)
    store = store_with()

    genesis_missing = {0: 1, 2: 0, 3: [root.pub], 4: ch, 5: 2, 6: 0, 7: 0}
    scope_missing = hashlib.sha256(
        DOM_NUC_GEN + cbor_canon.encode(genesis_missing)
    ).digest()
    with pytest.raises(ValueError):
        resolve_authorized_keys(
            store,
            scope=scope_missing,
            genesis_obj=genesis_missing,
            constitution_hash=ch,
            constitution_obj=None,
            now=NOW,
        )

    genesis_short = {
        0: 1,
        1: [b"short"],
        2: 0,
        3: [root.pub],
        4: ch,
        5: 2,
        6: 0,
        7: 0,
    }
    scope_short = hashlib.sha256(
        DOM_NUC_GEN + cbor_canon.encode(genesis_short)
    ).digest()
    with pytest.raises(ValueError):
        resolve_authorized_keys(
            store,
            scope=scope_short,
            genesis_obj=genesis_short,
            constitution_hash=ch,
            constitution_obj=None,
            now=NOW,
        )

    genesis_not_bytes = {
        0: 1,
        1: [42],
        2: 0,
        3: [root.pub],
        4: ch,
        5: 2,
        6: 0,
        7: 0,
    }
    scope_not_bytes = hashlib.sha256(
        DOM_NUC_GEN + cbor_canon.encode(genesis_not_bytes)
    ).digest()
    with pytest.raises(ValueError):
        resolve_authorized_keys(
            store,
            scope=scope_not_bytes,
            genesis_obj=genesis_not_bytes,
            constitution_hash=ch,
            constitution_obj=None,
            now=NOW,
        )


def test_l_nucleus_keys_drops_rotated_unnamed_root() -> None:
    """Anker nucleus_keys=Y plus Rotation root→X: Ergebnis Y, weder root noch X (00 §5.4)."""
    root = Identity("ank-l-root")
    x = Identity("ank-l-x")
    y = Identity("ank-l-y")
    constitution = {"nucleus_keys": [y.pub]}
    scope, genesis, ch = _world([root.pub], constitution)
    rotate = _rotate(root, x, scope, t=1)
    ack = _ack(x, rotate, scope, t=2)
    result = _resolve(store_with(rotate, ack), scope, genesis, ch, constitution)
    assert result.keys == frozenset({y.pub})
    assert root.pub not in result.keys
    assert x.pub not in result.keys
    assert result.findings == ()
