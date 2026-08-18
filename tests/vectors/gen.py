#!/usr/bin/env python3
"""Reproduziert Test-Vektoren aus Anhang C (feste Seeds, kanonisches CBOR)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mensch_als_republik.atom import (
    Claim,
    claim_id,
    core_bytes,
    id_genesis_anchor,
    sign,
    signed_bytes,
    signed_map,
)
from mensch_als_republik.domains import DOM_NUC_GEN
from mensch_als_republik import cbor_canon
from tests.helpers import SEED_ALICE, SEED_BOB

VECTORS_PATH = Path(__file__).resolve().parent / "vectors_01.json"

ALICE_SEED = SEED_ALICE
BOB_SEED = SEED_BOB

ALICE_PUB = bytes.fromhex(
    "8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c"
)
BOB_PUB = bytes.fromhex(
    "8139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394"
)

CONST = bytes.fromhex(
    "890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e"
)

# Genesis-Objekt aus 00 §3.1 (uint-Keys, kanonisches CBOR)
GENESIS_OBJ = {
    0: 1,
    1: [ALICE_PUB],
    2: 0,
    3: [ALICE_PUB],
    4: CONST,
    5: 2,
    6: 1,
    7: 0,
}

N = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(GENESIS_OBJ)).digest()

N_HEX = N.hex()
P_VOUCH = f"nuc:{N_HEX}/vouch@1"
P_ACCEPT = f"nuc:{N_HEX}/accept-rules@1"
P_REVOKE = "core/revoke@1"

V_VOUCH = bytes.fromhex("a1001864")

# BV1, BV2 — Byte-Vektoren Anhang C.8 (kein Schlüsselmaterial)
BV1_HEX = "a100ff"
BV2_HEX = "bf616100ff"

# NV2: nicht-kanonisches CBOR desselben TV1-Cores (Key-Reihenfolge 8,6,5,3,2,1,0,7,4)
NV2_CORE_HEX = (
    "a908582062db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d327a28f73b"
    "25625430061a6553f10005582065309fe233da30fda061d7c5ef002b6b80e426"
    "82cd54d703ab13fb6c7d2f555703784c6e75633a363533303966653233336461"
    "3330666461303631643763356566303032623662383065343236383263643534"
    "64373033616231336662366337643266353535372f766f756368403102820158"
    "208139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b3"
    "940158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801"
    "b40f6f5c0001071a677485800444a1001864"
)


def _sk(seed: bytes) -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(seed)


def _finalize(claim: Claim, sk: Ed25519PrivateKey) -> Claim:
    return replace(claim, sigma=sign(sk, claim))


def _vec(name: str, claim: Claim, *, expect_reject: str | None = None) -> dict:
    cid = claim_id(claim)
    core = core_bytes(claim)
    wire = signed_bytes(claim)
    entry = {
        "name": name,
        "claim_id": cid.hex(),
        "core_bytes": core.hex(),
        "signed_bytes": wire.hex(),
        "sigma": claim.sigma.hex() if claim.sigma else None,
    }
    if expect_reject:
        entry["expect_reject"] = expect_reject
    return entry


def build_vectors() -> dict:
    alice_sk = _sk(ALICE_SEED)
    bob_sk = _sk(BOB_SEED)

    h_gen_alice = id_genesis_anchor(ALICE_PUB)
    h_gen_bob = id_genesis_anchor(BOB_PUB)

    # TV1 — Genesis-Vouch Alice → Bob
    tv1_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p=P_VOUCH,
        v=V_VOUCH,
        N=N,
        t=1_700_000_000,
        t_exp=1_735_689_600,
        h_prev=h_gen_alice,
    )
    tv1 = _finalize(tv1_unsigned, alice_sk)
    tv1_cid = claim_id(tv1)

    # BV3 — TV1s signierte Map in indefinite-length-Form (Anhang C.8)
    tv1_signed = signed_map(tv1)
    bv3_wire = (
        b"\xbf"
        + b"".join(
            cbor_canon.encode(k) + cbor_canon.encode(tv1_signed[k])
            for k in sorted(tv1_signed)
        )
        + b"\xff"
    )

    # TV2 — accept-rules Alice, verkettet auf TV1
    tv2_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(3, CONST),
        p=P_ACCEPT,
        N=N,
        t=1_700_000_100,
        h_prev=tv1_cid,
    )
    tv2 = _finalize(tv2_unsigned, alice_sk)
    tv2_cid = claim_id(tv2)

    # TV3 — core/revoke@1 widerruft TV1
    tv3_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(2, tv1_cid),
        p=P_REVOKE,
        t=1_700_000_200,
        h_prev=tv2_cid,
    )
    tv3 = _finalize(tv3_unsigned, alice_sk)

    # TV4 — accept-rules Bob, Genesis
    tv4_unsigned = Claim(
        version=1,
        I=BOB_PUB,
        J=(3, CONST),
        p=P_ACCEPT,
        N=N,
        t=1_700_000_050,
        h_prev=h_gen_bob,
    )
    tv4 = _finalize(tv4_unsigned, bob_sk)

    # NV1 — h_prev = 32×0x00
    nv1_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p=P_VOUCH,
        N=N,
        t=1_700_000_300,
        h_prev=bytes(32),
    )
    nv1 = _finalize(nv1_unsigned, alice_sk)

    # NV3 — Equivocation gegen TV1 (gleiches h_prev, anderes t)
    nv3_unsigned = Claim(
        version=1,
        I=ALICE_PUB,
        J=(1, BOB_PUB),
        p=P_VOUCH,
        N=N,
        t=1_700_000_001,
        h_prev=h_gen_alice,
    )
    nv3 = _finalize(nv3_unsigned, alice_sk)

    nv2_core = bytes.fromhex(NV2_CORE_HEX)

    return {
        "params": {
            "ALICE": ALICE_PUB.hex(),
            "BOB": BOB_PUB.hex(),
            "N": N.hex(),
            "CONST": CONST.hex(),
            "id_genesis_anchor_ALICE": h_gen_alice.hex(),
            "id_genesis_anchor_BOB": h_gen_bob.hex(),
        },
        "vectors": [
            _vec("TV1", tv1),
            _vec("TV2", tv2),
            _vec("TV3", tv3),
            _vec("TV4", tv4),
            _vec("NV1", nv1, expect_reject="INVALID_GENESIS_ANCHOR"),
            _vec("NV3", nv3),
            {
                "name": "NV2",
                "core_bytes_noncanonical": nv2_core.hex(),
                "reserializes_to": core_bytes(tv1).hex(),
                "expect_reject": "NON_CANONICAL_ENCODING",
            },
            {
                "name": "BV1",
                "wire_bytes": BV1_HEX,
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "BV2",
                "wire_bytes": BV2_HEX,
                "expect_reject": "MALFORMED_CBOR",
            },
            {
                "name": "BV3",
                "wire_bytes": bv3_wire.hex(),
                "expect_reject": "NON_CANONICAL_ENCODING",
            },
        ],
    }


def main() -> None:
    data = build_vectors()
    VECTORS_PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Wrote {VECTORS_PATH}")


if __name__ == "__main__":
    main()
