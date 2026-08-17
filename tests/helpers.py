"""Testaufbau: signierte Vouch-/Lifecycle-Claims ohne Systemuhr, deterministisch aus Labels."""

from __future__ import annotations

import hashlib

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import Claim, build_signed, claim_id, id_genesis_anchor
from mensch_als_republik.verifier import InMemoryStore

# Normative Seeds aus 00 §3.1 / 03-golden-anchors.md §3.1 — eine Definition (D88).
SEED_ALICE = bytes([0x01] * 32)
SEED_BOB = bytes([0x02] * 32)
SEED_CAROL = bytes([0x03] * 32)


def scope_id(label: str) -> bytes:
    return hashlib.sha256(b"scope:" + label.encode()).digest()


class Identity:
    """Eine Autorenkette: jeder Aufruf hängt an, h_prev wird intern fortgeführt."""

    def __init__(self, label: str, *, seed: bytes | None = None) -> None:
        if seed is None:
            seed = hashlib.sha256(b"identity:" + label.encode()).digest()
        self._sk = Ed25519PrivateKey.from_private_bytes(seed)
        self.label = label
        self.pub = self._sk.public_key().public_bytes_raw()
        self._h_prev = id_genesis_anchor(self.pub)

    def _append(
        self,
        *,
        J: tuple[int, bytes],
        p: str,
        t: int,
        v: bytes | None = None,
        N: bytes | None = None,
        t_exp: int | None = None,
    ) -> Claim:
        signed = build_signed(
            self._sk,
            J=J,
            p=p,
            t=t,
            h_prev=self._h_prev,
            v=v,
            N=N,
            t_exp=t_exp,
        )
        self._h_prev = claim_id(signed)
        return signed

    def vouch(
        self,
        subject: "Identity",
        *,
        n: int | None,
        scope: bytes,
        t: int,
        t_exp: int | None = None,
        extra: dict[int, object] | None = None,
    ) -> Claim:
        """n=None => v abwesend (Default n=D, §2.3)."""
        if n is None:
            v = None
        else:
            payload: dict[int, object] = {0: n}
            if extra:
                payload.update(extra)
            v = cbor_canon.encode(payload)
        return self.vouch_raw(subject, v=v, scope=scope, t=t, t_exp=t_exp)

    def vouch_raw(
        self,
        subject: "Identity",
        *,
        v: bytes | None,
        scope: bytes,
        t: int,
        t_exp: int | None = None,
    ) -> Claim:
        p = f"nuc:{scope.hex()}/vouch@1"
        return self._append(J=(1, subject.pub), p=p, t=t, v=v, N=scope, t_exp=t_exp)

    def claim(
        self,
        *,
        p: str,
        J: tuple[int, bytes],
        t: int,
        v: bytes | None = None,
        N: bytes | None = None,
        t_exp: int | None = None,
    ) -> Claim:
        """Generischer Anhänger für Prädikate jenseits von vouch@1."""
        return self._append(J=J, p=p, t=t, v=v, N=N, t_exp=t_exp)

    def revoke(self, target: Claim, *, t: int) -> Claim:
        return self._append(J=(2, claim_id(target)), p="core/revoke@1", t=t)

    def supersede(self, target: Claim, *, t: int) -> Claim:
        return self._append(J=(2, claim_id(target)), p="core/supersede@1", t=t)


def store_with(*claims: Claim) -> InMemoryStore:
    store = InMemoryStore()
    for c in claims:
        store.add(c)
    return store
