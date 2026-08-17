"""Tests für mensch_als_republik.policy und den policy-Parameter von verifier.classify (01a)."""

from __future__ import annotations

import pytest

from mensch_als_republik.policy import (
    NucleusPolicy,
    PolicyNote,
    PolicyWarning,
    is_irrevocable,
)
from mensch_als_republik.verifier import State, classify
from tests.helpers import Identity, scope_id, store_with


def _unsafe(*predicates: str) -> tuple[PolicyNote, ...]:
    return tuple(
        PolicyNote(PolicyWarning.UNSAFE_IRREVOCABLE_PREDICATE, p) for p in sorted(predicates)
    )


# --- 5.1 Normalisierung ------------------------------------------------------


@pytest.mark.parametrize(
    "declared, irrevocable, warnings",
    [
        (frozenset(), frozenset({"obligation@1"}), ()),  # P-1
        (frozenset({"obligation@1"}), frozenset({"obligation@1"}), ()),  # P-2
        (frozenset({"foo@1"}), frozenset({"obligation@1", "foo@1"}), ()),  # P-3
        (frozenset({"vouch@1"}), frozenset({"obligation@1"}), _unsafe("vouch@1")),  # P-4
        (
            frozenset({"vouch@1", "foo@1"}),
            frozenset({"obligation@1", "foo@1"}),
            _unsafe("vouch@1"),
        ),  # P-5
        (
            frozenset({"revoke@1", "supersede@1"}),
            frozenset({"obligation@1"}),
            (),
        ),  # P-6
    ],
)
def test_normalization(declared, irrevocable, warnings):
    policy = NucleusPolicy(scope=scope_id("policy-norm"), declared=declared)
    assert policy.irrevocable == irrevocable
    assert policy.warnings == warnings


# --- 5.2 Prädikat-Abgleich ---------------------------------------------------


def test_predicate_match_obligation_is_irrevocable():
    scope = scope_id("policy-match")
    policy = NucleusPolicy(scope=scope)
    assert is_irrevocable(f"nuc:{scope.hex()}/obligation@1", policy) is True


def test_predicate_match_vouch_is_not_irrevocable():
    scope = scope_id("policy-match")
    policy = NucleusPolicy(scope=scope)
    assert is_irrevocable(f"nuc:{scope.hex()}/vouch@1", policy) is False


def test_predicate_match_core_is_never_irrevocable():
    scope = scope_id("policy-match")
    policy = NucleusPolicy(scope=scope)
    assert is_irrevocable("core/revoke@1", policy) is False


def test_predicate_match_version_is_part_of_name():
    scope = scope_id("policy-match")
    policy = NucleusPolicy(scope=scope)
    assert is_irrevocable(f"nuc:{scope.hex()}/obligation@2", policy) is False


def test_predicate_match_none_policy_never_irrevocable():
    scope = scope_id("policy-match")
    assert is_irrevocable(f"nuc:{scope.hex()}/obligation@1", None) is False


# --- 5.3 Zustandsmaschine -----------------------------------------------------


def test_c1_obligation_revoked_without_policy():
    alice = Identity("alice-c1")
    bob = Identity("bob-c1")
    scope = scope_id("c1")
    obl = alice.claim(p=f"nuc:{scope.hex()}/obligation@1", J=(1, bob.pub), t=1, N=scope)
    rev = alice.revoke(obl, t=2)
    store = store_with(obl, rev)

    result = classify(obl, store, now=100, policy=None)

    assert result.state == State.REVOKED


def test_c2_obligation_active_with_policy():
    alice = Identity("alice-c2")
    bob = Identity("bob-c2")
    scope = scope_id("c2")
    obl = alice.claim(p=f"nuc:{scope.hex()}/obligation@1", J=(1, bob.pub), t=1, N=scope)
    rev = alice.revoke(obl, t=2)
    store = store_with(obl, rev)
    policy = NucleusPolicy(scope=scope)

    result = classify(obl, store, now=100, policy=policy)

    assert result.state == State.ACTIVE
    assert result.trust_usable is True


def test_c3_obligation_active_against_supersede_with_policy():
    alice = Identity("alice-c3")
    bob = Identity("bob-c3")
    scope = scope_id("c3")
    obl = alice.claim(p=f"nuc:{scope.hex()}/obligation@1", J=(1, bob.pub), t=1, N=scope)
    sup = alice.supersede(obl, t=2)
    store = store_with(obl, sup)
    policy = NucleusPolicy(scope=scope)

    result = classify(obl, store, now=100, policy=policy)

    assert result.state == State.ACTIVE


def test_c4_vouch_still_revoked_with_policy():
    alice = Identity("alice-c4")
    bob = Identity("bob-c4")
    scope = scope_id("c4")
    v = alice.vouch(bob, n=1, scope=scope, t=1, t_exp=5000)
    rev = alice.revoke(v, t=2)
    store = store_with(v, rev)
    policy = NucleusPolicy(scope=scope)

    result = classify(v, store, now=100, policy=policy)

    assert result.state == State.REVOKED


def test_c5_expired_beats_irrevocable():
    alice = Identity("alice-c5")
    bob = Identity("bob-c5")
    scope = scope_id("c5")
    obl = alice.claim(
        p=f"nuc:{scope.hex()}/obligation@1", J=(1, bob.pub), t=1, N=scope, t_exp=50
    )
    rev = alice.revoke(obl, t=2)
    store = store_with(obl, rev)
    policy = NucleusPolicy(scope=scope)

    result = classify(obl, store, now=100, policy=policy)

    assert result.state == State.EXPIRED


def test_c9_expired_and_revoked_without_policy_is_revoked():
    """Ohne Policy greift der Widerruf-Zweig vor der Zeitprüfung (D76); Ist-Zustand, keine
    Rangfolge aus Anhang B."""
    alice = Identity("alice-c9")
    bob = Identity("bob-c9")
    scope = scope_id("c9")
    obl = alice.claim(
        p=f"nuc:{scope.hex()}/obligation@1", J=(1, bob.pub), t=1, N=scope, t_exp=50
    )
    rev = alice.revoke(obl, t=2)
    store = store_with(obl, rev)

    result = classify(obl, store, now=100, policy=None)

    assert result.state == State.REVOKED


def test_c6_revoke_itself_stays_active():
    alice = Identity("alice-c6")
    bob = Identity("bob-c6")
    scope = scope_id("c6")
    obl = alice.claim(p=f"nuc:{scope.hex()}/obligation@1", J=(1, bob.pub), t=1, N=scope)
    rev = alice.revoke(obl, t=2)
    store = store_with(obl, rev)
    policy = NucleusPolicy(scope=scope)

    result = classify(rev, store, now=100, policy=policy)

    assert result.state == State.ACTIVE


def test_c7_pending_unaffected_by_policy():
    alice = Identity("alice-c7")
    bob = Identity("bob-c7")
    scope = scope_id("c7")
    # Vorgänger wird erzeugt (rückt h_prev vor), aber nicht in den Store gelegt.
    alice.claim(p=f"nuc:{scope.hex()}/obligation@1", J=(1, bob.pub), t=1, N=scope)
    obl = alice.claim(p=f"nuc:{scope.hex()}/obligation@1", J=(1, bob.pub), t=2, N=scope)
    store = store_with(obl)
    policy = NucleusPolicy(scope=scope)

    result = classify(obl, store, now=100, policy=policy)

    assert result.state == State.PENDING


def test_P_7_character_set_from_text() -> None:
    """P-7: ein str ist kein Array — ein Vermerk, Liste ausgefallen (D95, 04a)."""
    raw = "obligation@1"
    policy = NucleusPolicy(scope=scope_id("p7"), declared=raw)
    assert policy.declared == raw
    assert policy.irrevocable == frozenset({"obligation@1"})
    assert policy.warnings == (
        PolicyNote(PolicyWarning.MALFORMED_IRREVOCABLE_ENTRY, repr(raw)),
    )


def test_P_8_non_str_entry() -> None:
    """P-8: Eintrag, der kein str ist (D95)."""
    raw = [42]
    policy = NucleusPolicy(scope=scope_id("p8"), declared=raw)
    assert policy.declared is raw
    assert policy.irrevocable == frozenset({"obligation@1"})
    assert policy.warnings == (
        PolicyNote(PolicyWarning.MALFORMED_IRREVOCABLE_ENTRY, "42"),
    )


def test_P_8_non_iterable_declared() -> None:
    policy = NucleusPolicy(scope=scope_id("p8b"), declared=42)
    assert policy.declared == 42
    assert policy.irrevocable == frozenset({"obligation@1"})
    assert policy.warnings == (
        PolicyNote(PolicyWarning.MALFORMED_IRREVOCABLE_ENTRY, "42"),
    )


def test_P_9_scope_prefix() -> None:
    """P-9: Eintrag mit Scope-Präfix schützt niemanden (D95)."""
    raw = ["nuc:N/obligation@1"]
    policy = NucleusPolicy(scope=scope_id("p9"), declared=raw)
    assert policy.declared is raw
    assert policy.irrevocable == frozenset({"obligation@1"})
    assert policy.warnings == (
        PolicyNote(PolicyWarning.MALFORMED_IRREVOCABLE_ENTRY, "nuc:N/obligation@1"),
    )


def test_warnings_frozenset_deterministic() -> None:
    raw = frozenset({"???", "not-a-predicate", "also::bad"})
    a = NucleusPolicy(scope=scope_id("warn-a"), declared=raw)
    b = NucleusPolicy(scope=scope_id("warn-b"), declared=raw)
    assert a.warnings == b.warnings
    assert len(a.warnings) == 3
    assert all(w.code == PolicyWarning.MALFORMED_IRREVOCABLE_ENTRY for w in a.warnings)


def test_c8_scope_mismatch_raises():
    alice = Identity("alice-c8")
    bob = Identity("bob-c8")
    scope = scope_id("c8")
    other_scope = scope_id("c8-other")
    obl = alice.claim(p=f"nuc:{scope.hex()}/obligation@1", J=(1, bob.pub), t=1, N=scope)
    store = store_with(obl)
    policy = NucleusPolicy(scope=other_scope)

    with pytest.raises(ValueError):
        classify(obl, store, now=100, policy=policy)
