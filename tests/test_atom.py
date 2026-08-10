"""Tests für Claim-Atom Kernfunktionen."""

import json
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mensch_als_republik.atom import (
    Claim,
    claim_id,
    core_bytes,
    id_genesis_anchor,
    is_equivocation_pair,
    sign,
    signed_bytes,
    verify_sig,
)
from tests.vectors.gen import ALICE_PUB, BOB_PUB, build_vectors

VECTORS = json.loads(
    (Path(__file__).resolve().parent / "vectors" / "vectors_01.json").read_text()
)

GOLDEN_CLAIM_IDS = {
    "TV1": "f95d430e40df736cbdffd7bf82af4f77e0c7af8692565f3b2a151c2c1ae8660c",
    "TV2": "29b66881810bbbf1e254e061c35395e15da6c064327c2d33dfa6aa29d47dc2a6",
    "TV3": "8e76a2a9ee6677e6959bf9868dc6d162e5ff7e464a6bb4c6b839f89713e54629",
    "TV4": "0bd77591da5e480a8c9a573382d14407a1770e0a7f6d2d09776b630fbd7ca01c",
    "NV1": "9b25020fee7da6832416f8bcb61e4a05329776d051a4da282db7e973eb96c453",
    "NV3": "e14ebd82eb172672a4a3ccbc330fef64fecd86e4664f72eab538855c9cef5c8b",
}


def _vec(name: str) -> dict:
    for v in VECTORS["vectors"]:
        if v["name"] == name:
            return v
    raise KeyError(name)


def test_golden_id_genesis_anchor():
    assert id_genesis_anchor(ALICE_PUB).hex() == VECTORS["params"]["id_genesis_anchor_ALICE"]
    assert id_genesis_anchor(BOB_PUB).hex() == VECTORS["params"]["id_genesis_anchor_BOB"]


def test_gen_reproduces_golden_claim_ids():
    data = build_vectors()
    for name, expected in GOLDEN_CLAIM_IDS.items():
        vec = next(v for v in data["vectors"] if v.get("name") == name)
        assert vec["claim_id"] == expected


@pytest.mark.parametrize("name", ["TV1", "TV2", "TV3", "TV4", "NV1", "NV3"])
def test_claim_id_from_vectors(name: str):
    assert _vec(name)["claim_id"] == GOLDEN_CLAIM_IDS[name]


def test_verify_sig_positive():
    from mensch_als_republik.atom import claim_from_bytes

    c = claim_from_bytes(bytes.fromhex(_vec("TV1")["signed_bytes"]))
    assert verify_sig(c)


def test_sign_verify_roundtrip():
    sk = Ed25519PrivateKey.from_private_bytes(b"\x03" * 32)
    pub = sk.public_key().public_bytes_raw()
    claim = Claim(
        version=1,
        I=pub,
        J=(1, pub),
        p="core/revoke@1",
        t=100,
        h_prev=id_genesis_anchor(pub),
    )
    sig = sign(sk, claim)
    signed = Claim(
        version=claim.version,
        I=claim.I,
        J=claim.J,
        p=claim.p,
        t=claim.t,
        h_prev=claim.h_prev,
        sigma=sig,
    )
    assert verify_sig(signed)


def test_core_bytes_deterministic():
    from mensch_als_republik.atom import claim_from_bytes

    tv1_data = _vec("TV1")
    c = claim_from_bytes(bytes.fromhex(tv1_data["signed_bytes"]))
    assert core_bytes(c).hex() == tv1_data["core_bytes"]


def test_is_equivocation_pair():
    from mensch_als_republik.atom import claim_from_bytes

    tv1 = claim_from_bytes(bytes.fromhex(_vec("TV1")["signed_bytes"]))
    nv3 = claim_from_bytes(bytes.fromhex(_vec("NV3")["signed_bytes"]))
    assert is_equivocation_pair(tv1, nv3)
    assert not is_equivocation_pair(tv1, tv1)


def test_claim_id_signature_independent():
    from mensch_als_republik.atom import claim_from_bytes

    c = claim_from_bytes(bytes.fromhex(_vec("TV1")["signed_bytes"]))
    assert claim_id(c).hex() == GOLDEN_CLAIM_IDS["TV1"]
    assert len(signed_bytes(c)) > len(core_bytes(c))
