"""Testaufbau: signierte Vouch-/Lifecycle-Claims ohne Systemuhr, deterministisch aus Labels."""

from __future__ import annotations

import hashlib

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import Claim, claim_id, id_genesis_anchor, sign
from mensch_als_republik.verifier import InMemoryStore


def scope_id(label: str) -> bytes:
    return hashlib.sha256(b"scope:" + label.encode()).digest()


class Identity:
    """Eine Autorenkette: jeder Aufruf hängt an, h_prev wird intern fortgeführt."""

    def __init__(self, label: str) -> None:
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
        unsigned = Claim(
            version=1,
            I=self.pub,
            J=J,
            p=p,
            t=t,
            h_prev=self._h_prev,
            v=v,
            N=N,
            t_exp=t_exp,
        )
        signed = Claim(
            version=unsigned.version,
            I=unsigned.I,
            J=unsigned.J,
            p=unsigned.p,
            t=unsigned.t,
            h_prev=unsigned.h_prev,
            v=unsigned.v,
            N=unsigned.N,
            t_exp=unsigned.t_exp,
            sigma=sign(self._sk, unsigned),
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

    def revoke(self, target: Claim, *, t: int) -> Claim:
        return self._append(J=(2, claim_id(target)), p="core/revoke@1", t=t)

    def supersede(self, target: Claim, *, t: int) -> Claim:
        return self._append(J=(2, claim_id(target)), p="core/supersede@1", t=t)


def store_with(*claims: Claim) -> InMemoryStore:
    store = InMemoryStore()
    for c in claims:
        store.add(c)
    return store
