#!/usr/bin/env python3
"""Beispielnukleus — Zwei und eine Dritte (example-nucleus.md)."""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import Claim, claim_id, id_genesis_anchor, sign
from mensch_als_republik.domains import DOM_NUC_GEN
from mensch_als_republik.governance import (
    Epoch,
    GovernanceFinding,
    Proposal,
    TallyState,
    decide,
    verify_ratification,
)
from mensch_als_republik.governance.tally import threshold_class
from mensch_als_republik.policy import NucleusPolicy, constitution_hash
from mensch_als_republik.profiles import MembershipState, membership
from mensch_als_republik.trust.derive import derive
from mensch_als_republik.trust.graph import capacity
from mensch_als_republik.trust.params import TrustParams
from mensch_als_republik.verifier import InMemoryStore

NOW = 1000

DOC_STOCK_CONSTITUTION_HASH = bytes.fromhex(
    "890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e"
)
DOC_STOCK_N = bytes.fromhex(
    "65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557"
)
DOC_ANNA = bytes.fromhex(
    "d04ab232742bb4ab3a1368bd4615e4e6d0224ab71a016baf8520a332c9778737"
)
DOC_BRUNO = bytes.fromhex(
    "204040e364c10f2bec9c1fe500a1cd4c247c89d650a01ed7e82caba867877c21"
)
DOC_CHRIS = bytes.fromhex(
    "66cd608b928b88e50e0efeaa33faf1c43cefe07294b0b87e9fe0aba6a3cf7633"
)
DOC_DORA = bytes.fromhex(
    "20828bf5c5bdcacb684863336c202fb5599da48be5596615742170705beca9f7"
)
DOC_CONSTITUTION_HASH_GOV = bytes.fromhex(
    "f5cddafcaa18068aba72079a7a8c87194a13b0dcd6d5c22bfcacbe2c3991e923"
)
DOC_N_GOV = bytes.fromhex(
    "50ecec77a0fc064b8404f1ea74d5f85ed9ea4abc49e477e3c98a9c59525a8f63"
)
DOC_EPOCH_ID_1 = bytes.fromhex(
    "7f4b12a76f41c4d10aa58b6c8a9f7a7575eb271132d08708e053fba3494823a0"
)
DOC_CONSTITUTION_HASH_RES = bytes.fromhex(
    "3af74c182d52af10afd8828120703fdf7672ad9f0c21381af47650fcc40dc502"
)
DOC_N_RES = bytes.fromhex(
    "4d78bcea4a44af89c0728fbc5f3a0300a853291f744a1657b3ecc2926717f355"
)
DOC_CONSTITUTION_HASH_2 = bytes.fromhex(
    "6cbcd33f2f82257153517d565a821d6d069129826efbfe1b737ff2c3a80f6f1b"
)
DOC_PROPOSAL_HASH = bytes.fromhex(
    "7dfb88e9a6b2b9b8ef5a2e5b6b5e8e429033da12274fa4480e5a1a42f8a1b089"
)
DOC_EPOCH_ID_2 = bytes.fromhex(
    "bfcf27681adf4bbadc71f0e04238cee9a58bc7b3ff22ff12a940b007b5771eef"
)


def _hex(value: bytes) -> str:
    return value.hex()


def _eq(got: bytes, expected: bytes, name: str) -> None:
    if got != expected:
        raise AssertionError(f"{name}: got {_hex(got)}, expected {_hex(expected)}")


def _nuc(scope: bytes, name: str) -> str:
    return f"nuc:{scope.hex()}/{name}@1"


class _Author:
    """Autorenkette; h_prev beginnt bei SHA-256(DOM_ID_GEN ‖ I) (01 §4, example-nucleus-prompt.md §7)."""

    def __init__(self, seed: bytes) -> None:
        self._sk = Ed25519PrivateKey.from_private_bytes(seed)
        self.pub = self._sk.public_key().public_bytes_raw()
        self._h_prev = id_genesis_anchor(self.pub)

    def claim(
        self,
        *,
        p: str,
        J: tuple[int, bytes],
        t: int,
        v: bytes | None = None,
        N: bytes | None = None,
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

    def vouch(self, subject: "_Author", *, n: int, scope: bytes, t: int) -> Claim:
        return self.claim(
            p=_nuc(scope, "vouch"),
            J=(1, subject.pub),
            t=t,
            N=scope,
            v=cbor_canon.encode({0: n}),
        )


def _store(*claims: Claim) -> InMemoryStore:
    store = InMemoryStore()
    for c in claims:
        store.add(c)
    return store


def people() -> tuple[_Author, _Author, _Author, _Author]:
    """Ed25519 aus Seeds 0x11×32 … 0x14×32 (example-nucleus.md §2)."""
    return (
        _Author(bytes([0x11] * 32)),
        _Author(bytes([0x12] * 32)),
        _Author(bytes([0x13] * 32)),
        _Author(bytes([0x14] * 32)),
    )


def probe_stock_anchors() -> None:
    """Bestandsanker aus 00 §3.1 über denselben Kodierungsweg (example-nucleus.md §9)."""
    alice = _Author(bytes([0x01] * 32))
    constitution = {
        "irrevocable_predicates": ["obligation@1"],
        "thresholds": {
            "ordinary": [1, 2],
            "membership": [2, 3],
            "amendment": [3, 4],
        },
        "arbitration": {"arbitrators": [alice.pub]},
    }
    h = constitution_hash(constitution)
    _eq(h, DOC_STOCK_CONSTITUTION_HASH, "stock constitution_hash")
    genesis = {
        0: 1,
        1: [alice.pub],
        2: 0,
        3: [alice.pub],
        4: h,
        5: 2,
        6: 1,
        7: 0,
    }
    raw = cbor_canon.encode(genesis)
    n = hashlib.sha256(DOM_NUC_GEN + raw).digest()
    _eq(n, DOC_STOCK_N, "stock N")


@dataclass(frozen=True, slots=True)
class ExampleNucleus:
    """Gerechnete Objekte des Beispielnukleus (example-nucleus.md §2–§5)."""

    anna: _Author
    bruno: _Author
    chris: _Author
    dora: _Author
    constitution_gov: dict
    constitution_res: dict
    constitution_2: dict
    genesis_gov: dict
    genesis_res: dict
    constitution_hash_gov: bytes
    constitution_hash_res: bytes
    constitution_hash_2: bytes
    N_gov: bytes
    N_res: bytes
    genesis_gov_cbor: bytes
    genesis_res_cbor: bytes
    epoch_1: Epoch
    proposal: Proposal
    epoch_2: Epoch
    params: TrustParams


def build() -> ExampleNucleus:
    """Baut Identitäten, Verfassungen, Genesis und Epochen (example-nucleus.md §2–§5)."""
    probe_stock_anchors()
    anna, bruno, chris, dora = people()
    _eq(anna.pub, DOC_ANNA, "ANNA")
    _eq(bruno.pub, DOC_BRUNO, "BRUNO")
    _eq(chris.pub, DOC_CHRIS, "CHRIS")
    _eq(dora.pub, DOC_DORA, "DORA")
    founders = [bruno.pub, chris.pub, anna.pub]
    if founders != sorted(founders):
        raise AssertionError("founding participants are not byte-sorted")
    admitted = [bruno.pub, dora.pub, chris.pub, anna.pub]
    if admitted != sorted(admitted):
        raise AssertionError("admitted participants are not byte-sorted")
    if admitted != sorted(founders + [dora.pub]):
        raise AssertionError("DORA does not sort between BRUNO and CHRIS")

    thresholds = {
        "ordinary": [1, 2],
        "membership": [1, 2],
        "amendment": [1, 2],
    }
    arbitration = {"arbitrators": [bruno.pub, chris.pub, anna.pub]}
    constitution_gov = {
        "irrevocable_predicates": ["obligation@1", "ratify@1", "vote@1"],
        "thresholds": thresholds,
        "arbitration": arbitration,
        "participants": founders,
    }
    constitution_hash_gov = constitution_hash(constitution_gov)
    _eq(constitution_hash_gov, DOC_CONSTITUTION_HASH_GOV, "constitution_hash_gov")

    genesis_gov = {
        0: 1,
        1: [bruno.pub, anna.pub],
        2: 0,
        3: [bruno.pub, anna.pub],
        4: constitution_hash_gov,
        5: 2,
        6: 0,
        7: 0,
    }
    genesis_gov_cbor = cbor_canon.encode(genesis_gov)
    if cbor_canon.encode(cbor_canon.decode(genesis_gov_cbor)) != genesis_gov_cbor:
        raise AssertionError("genesis_gov CBOR is not canonical")
    N_gov = hashlib.sha256(DOM_NUC_GEN + genesis_gov_cbor).digest()
    _eq(N_gov, DOC_N_GOV, "N_gov")

    epoch_1 = Epoch(scope=N_gov, index=1, constitution_hash=constitution_hash_gov)
    _eq(epoch_1.epoch_id, DOC_EPOCH_ID_1, "epoch_id_1")

    constitution_2 = dict(constitution_gov)
    constitution_2["participants"] = admitted
    constitution_hash_2 = constitution_hash(constitution_2)
    _eq(constitution_hash_2, DOC_CONSTITUTION_HASH_2, "constitution_hash_2")

    proposal = Proposal(
        scope=N_gov,
        predecessor=epoch_1.epoch_id,
        constitution_hash=constitution_hash_2,
    )
    _eq(proposal.proposal_hash, DOC_PROPOSAL_HASH, "proposal_hash")

    epoch_2 = Epoch(scope=N_gov, index=2, constitution_hash=constitution_hash_2)
    _eq(epoch_2.epoch_id, DOC_EPOCH_ID_2, "epoch_id_2")

    constitution_res = {
        "irrevocable_predicates": ["obligation@1"],
        "thresholds": thresholds,
        "arbitration": arbitration,
    }
    constitution_hash_res = constitution_hash(constitution_res)
    _eq(constitution_hash_res, DOC_CONSTITUTION_HASH_RES, "constitution_hash_res")

    genesis_res = {
        0: 1,
        1: [bruno.pub, anna.pub],
        2: 0,
        3: [bruno.pub, anna.pub],
        4: constitution_hash_res,
        5: 2,
        6: 0,
        7: 0,
        9: {0: 100, 1: 1, 2: 2, 3: 100},
    }
    genesis_res_cbor = cbor_canon.encode(genesis_res)
    if cbor_canon.encode(cbor_canon.decode(genesis_res_cbor)) != genesis_res_cbor:
        raise AssertionError("genesis_res CBOR is not canonical")
    N_res = hashlib.sha256(DOM_NUC_GEN + genesis_res_cbor).digest()
    _eq(N_res, DOC_N_RES, "N_res")

    klass = threshold_class(constitution_gov, constitution_2, genesis_gov)
    if klass != "membership":
        raise AssertionError(f"proposal class is {klass!r}, expected 'membership'")

    return ExampleNucleus(
        anna=anna,
        bruno=bruno,
        chris=chris,
        dora=dora,
        constitution_gov=constitution_gov,
        constitution_res=constitution_res,
        constitution_2=constitution_2,
        genesis_gov=genesis_gov,
        genesis_res=genesis_res,
        constitution_hash_gov=constitution_hash_gov,
        constitution_hash_res=constitution_hash_res,
        constitution_hash_2=constitution_hash_2,
        N_gov=N_gov,
        N_res=N_res,
        genesis_gov_cbor=genesis_gov_cbor,
        genesis_res_cbor=genesis_res_cbor,
        epoch_1=epoch_1,
        proposal=proposal,
        epoch_2=epoch_2,
        params=TrustParams(C0=100, gamma_num=1, gamma_den=2, D=100),
    )


def _policy(ex: ExampleNucleus) -> NucleusPolicy:
    return NucleusPolicy(
        ex.N_gov, declared=ex.constitution_gov["irrevocable_predicates"]
    )


def _vote(identity: _Author, ex: ExampleNucleus, *, choice: int, t: int) -> Claim:
    return identity.claim(
        p=_nuc(ex.N_gov, "vote"),
        J=(3, ex.proposal.proposal_hash),
        t=t,
        N=ex.N_gov,
        v=cbor_canon.encode({0: choice}),
    )


def _accept(identity: _Author, scope: bytes, constitution_h: bytes, *, t: int) -> Claim:
    return identity.claim(
        p=_nuc(scope, "accept-rules"),
        J=(3, constitution_h),
        t=t,
        N=scope,
    )


def decide_votes(ex: ExampleNucleus, votes: list[Claim]) -> TallyState:
    """Auszählung der Aufnahme gegen Epoche 1 (example-nucleus.md §5)."""
    return decide(
        _store(*votes),
        epoch=ex.epoch_1,
        proposal=ex.proposal,
        genesis_obj=ex.genesis_gov,
        constitution_obj=ex.constitution_gov,
        target_constitution_obj=ex.constitution_2,
        known_proposals={ex.proposal.proposal_hash: ex.proposal},
        now=NOW,
        policy=_policy(ex),
    ).state


def check_tally(ex: ExampleNucleus) -> None:
    """Drei Läufe der Tabelle in example-nucleus.md §5."""
    anna, bruno, chris, _dora = people()
    pending = decide_votes(
        ex,
        [
            _vote(anna, ex, choice=1, t=1),
            _vote(bruno, ex, choice=0, t=1),
        ],
    )
    if pending is not TallyState.PENDING:
        raise AssertionError(f"ANNA yes, BRUNO no: {pending}")

    anna, bruno, chris, _dora = people()
    passed = decide_votes(
        ex,
        [
            _vote(anna, ex, choice=1, t=1),
            _vote(bruno, ex, choice=0, t=1),
            _vote(chris, ex, choice=1, t=1),
        ],
    )
    if passed is not TallyState.PASSED:
        raise AssertionError(f"ANNA yes, BRUNO no, CHRIS yes: {passed}")

    anna, bruno, chris, _dora = people()
    failed = decide_votes(
        ex,
        [
            _vote(anna, ex, choice=1, t=1),
            _vote(bruno, ex, choice=0, t=1),
            _vote(chris, ex, choice=0, t=1),
        ],
    )
    if failed is not TallyState.FAILED:
        raise AssertionError(f"ANNA yes, BRUNO no, CHRIS no: {failed}")


@dataclass(frozen=True, slots=True)
class ClaimSet:
    """Signiertes Claim-Set plus die Autorenketten (example-nucleus.md §7)."""

    claims: dict[str, Claim]
    anna: _Author
    bruno: _Author
    chris: _Author
    dora: _Author


def claim_set(ex: ExampleNucleus) -> ClaimSet:
    """Neun Governance-Claims und vier Vouches (example-nucleus.md §7)."""
    anna, bruno, chris, dora = people()
    a1 = _accept(anna, ex.N_gov, ex.constitution_hash_gov, t=1)
    b1 = _accept(bruno, ex.N_gov, ex.constitution_hash_gov, t=1)
    c1 = _accept(chris, ex.N_gov, ex.constitution_hash_gov, t=1)
    propose = anna.claim(
        p=_nuc(ex.N_gov, "propose"),
        J=(3, ex.proposal.proposal_hash),
        t=2,
        N=ex.N_gov,
    )
    v_anna = _vote(anna, ex, choice=1, t=3)
    v_bruno = _vote(bruno, ex, choice=0, t=2)
    v_chris = _vote(chris, ex, choice=1, t=2)
    ratify_anna = anna.claim(
        p=_nuc(ex.N_gov, "ratify"),
        J=(3, ex.proposal.proposal_hash),
        t=4,
        N=ex.N_gov,
        v=cbor_canon.encode({0: [claim_id(v_anna), claim_id(v_chris)]}),
    )
    a9 = _accept(dora, ex.N_gov, ex.constitution_hash_2, t=1)
    n = 100
    return ClaimSet(
        claims={
            "accept_anna": a1,
            "accept_bruno": b1,
            "accept_chris": c1,
            "propose": propose,
            "vote_anna": v_anna,
            "vote_bruno": v_bruno,
            "vote_chris": v_chris,
            "ratify_anna": ratify_anna,
            "accept_dora": a9,
            "vouch_anna_bruno": anna.vouch(bruno, n=n, scope=ex.N_res, t=5),
            "vouch_bruno_anna": bruno.vouch(anna, n=n, scope=ex.N_res, t=3),
            "vouch_anna_chris": anna.vouch(chris, n=n, scope=ex.N_res, t=6),
            "vouch_bruno_chris": bruno.vouch(chris, n=n, scope=ex.N_res, t=4),
        },
        anna=anna,
        bruno=bruno,
        chris=chris,
        dora=dora,
    )


def _member(ex: ExampleNucleus, store, subject: bytes, constitution_h: bytes, obj: dict):
    return membership(
        store,
        subject=subject,
        scope=ex.N_gov,
        constitution_hash=constitution_h,
        now=NOW,
        authorized_keys=frozenset(),
        constitution_obj=obj,
        policy=_policy(ex),
    )


def check_membership_epoch1(ex: ExampleNucleus) -> None:
    """Nach den drei accept-rules sind alle drei MEMBER (example-nucleus.md §7)."""
    claims = claim_set(ex).claims
    store = _store(
        claims["accept_anna"], claims["accept_bruno"], claims["accept_chris"]
    )
    for subject in (ex.anna.pub, ex.bruno.pub, ex.chris.pub):
        result = _member(
            ex, store, subject, ex.constitution_hash_gov, ex.constitution_gov
        )
        if result.state is not MembershipState.MEMBER:
            raise AssertionError(f"epoch 1 {subject.hex()[:8]}: {result.state}")


def check_ratification(ex: ExampleNucleus) -> None:
    """Zwei ratify@1 mit verschiedener Zeugenmenge, derselbe epoch_id_2 (D99)."""
    cs = claim_set(ex)
    claims = cs.claims
    yes = [claim_id(claims["vote_anna"]), claim_id(claims["vote_chris"])]
    store = _store(
        claims["accept_anna"],
        claims["accept_bruno"],
        claims["accept_chris"],
        claims["propose"],
        claims["vote_anna"],
        claims["vote_bruno"],
        claims["vote_chris"],
        claims["ratify_anna"],
    )
    tally = decide(
        store,
        epoch=ex.epoch_1,
        proposal=ex.proposal,
        genesis_obj=ex.genesis_gov,
        constitution_obj=ex.constitution_gov,
        target_constitution_obj=ex.constitution_2,
        known_proposals={ex.proposal.proposal_hash: ex.proposal},
        now=NOW,
        policy=_policy(ex),
    )
    if tally.state is not TallyState.PASSED:
        raise AssertionError(f"ratification tally: {tally.state}")
    first = verify_ratification(
        store,
        ratify=claims["ratify_anna"],
        epoch=ex.epoch_1,
        proposal=ex.proposal,
        tally=tally,
        now=NOW,
        policy=_policy(ex),
    )
    if first.next_epoch is None:
        raise AssertionError("ANNA ratify produced no epoch")
    _eq(first.next_epoch.epoch_id, DOC_EPOCH_ID_2, "ratify epoch_id_2")

    ratify_chris = cs.chris.claim(
        p=_nuc(ex.N_gov, "ratify"),
        J=(3, ex.proposal.proposal_hash),
        t=3,
        N=ex.N_gov,
        v=cbor_canon.encode({0: list(reversed(yes))}),
    )
    store.add(ratify_chris)
    second = verify_ratification(
        store,
        ratify=ratify_chris,
        epoch=ex.epoch_1,
        proposal=ex.proposal,
        tally=tally,
        now=NOW,
        policy=_policy(ex),
    )
    if second.next_epoch is None:
        raise AssertionError("CHRIS ratify produced no epoch")
    if first.next_epoch.epoch_id != second.next_epoch.epoch_id:
        raise AssertionError("two ratify claims produced different epoch_id")


def check_membership_epoch2(ex: ExampleNucleus) -> None:
    """D116: Gründer GRANT_ONLY, DORA GRANT_ONLY vor und MEMBER nach Annahme."""
    claims = claim_set(ex).claims
    before = _store(
        claims["accept_anna"],
        claims["accept_bruno"],
        claims["accept_chris"],
        claims["propose"],
        claims["vote_anna"],
        claims["vote_bruno"],
        claims["vote_chris"],
        claims["ratify_anna"],
    )
    for subject in (ex.anna.pub, ex.bruno.pub, ex.chris.pub):
        result = _member(ex, before, subject, ex.constitution_hash_2, ex.constitution_2)
        if result.state is not MembershipState.GRANT_ONLY:
            raise AssertionError(f"epoch 2 founder {subject.hex()[:8]}: {result.state}")
    dora_before = _member(
        ex, before, ex.dora.pub, ex.constitution_hash_2, ex.constitution_2
    )
    if dora_before.state is not MembershipState.GRANT_ONLY:
        raise AssertionError(f"DORA before accept: {dora_before.state}")
    before.add(claims["accept_dora"])
    dora_after = _member(
        ex, before, ex.dora.pub, ex.constitution_hash_2, ex.constitution_2
    )
    if dora_after.state is not MembershipState.MEMBER:
        raise AssertionError(f"DORA after accept: {dora_after.state}")


def check_trust_flow(ex: ExampleNucleus) -> None:
    """Reichweitentabelle und C(CHRIS)=50 (example-nucleus.md §4.3)."""
    table = [capacity(ex.params, d) for d in range(8)]
    expected = [100, 50, 25, 12, 6, 3, 1, 0]
    if table != expected:
        raise AssertionError(f"reach table: {table}, expected {expected}")
    store = _store(*claim_set(ex).claims.values())
    derivation = derive(
        store,
        anchors=frozenset({ex.bruno.pub, ex.anna.pub}),
        scope=ex.N_res,
        now=NOW,
        params=ex.params,
    )
    d_chris = derivation.bfs.distance.get(ex.chris.pub)
    c_chris = derivation.bfs.node_capacity.get(ex.chris.pub)
    if d_chris != 1 or c_chris != 50:
        raise AssertionError(f"CHRIS d={d_chris} C={c_chris}, expected d=1 C=50")


def check_scope_separation(ex: ExampleNucleus) -> None:
    """Kein Claim des einen Scopes wirkt im anderen (example-nucleus.md §7)."""
    store = _store(*claim_set(ex).claims.values())
    for subject in (ex.anna.pub, ex.bruno.pub, ex.chris.pub, ex.dora.pub):
        result = membership(
            store,
            subject=subject,
            scope=ex.N_res,
            constitution_hash=ex.constitution_hash_res,
            now=NOW,
            authorized_keys=frozenset(),
            constitution_obj=ex.constitution_res,
        )
        if result.state is not MembershipState.NONE:
            raise AssertionError(f"membership on N_res: {result.state}")
    epoch_res = Epoch(
        scope=ex.N_res, index=1, constitution_hash=ex.constitution_hash_res
    )
    proposal_res = Proposal(
        scope=ex.N_res,
        predecessor=epoch_res.epoch_id,
        constitution_hash=ex.constitution_hash_res,
    )
    tally = decide(
        store,
        epoch=epoch_res,
        proposal=proposal_res,
        genesis_obj=ex.genesis_res,
        constitution_obj=ex.constitution_res,
        target_constitution_obj=ex.constitution_res,
        known_proposals={proposal_res.proposal_hash: proposal_res},
        now=NOW,
    )
    if tally.state is not TallyState.UNEVALUABLE:
        raise AssertionError(f"decide on N_res: {tally.state}")
    kinds = {f.kind for f in tally.findings}
    if GovernanceFinding.PARTICIPANTS_UNDECLARED not in kinds:
        raise AssertionError(f"decide on N_res findings: {tally.findings}")


def check_malformed_appended_dora(ex: ExampleNucleus) -> None:
    """DORA angehängt statt einsortiert → MALFORMED_PARTICIPANTS (example-nucleus.md §2)."""
    unsorted = dict(ex.constitution_gov)
    unsorted["participants"] = [
        ex.bruno.pub,
        ex.chris.pub,
        ex.anna.pub,
        ex.dora.pub,
    ]
    epoch = Epoch(
        scope=ex.N_gov,
        index=1,
        constitution_hash=constitution_hash(unsorted),
    )
    proposal = Proposal(
        scope=ex.N_gov,
        predecessor=epoch.epoch_id,
        constitution_hash=ex.constitution_hash_2,
    )
    tally = decide(
        _store(),
        epoch=epoch,
        proposal=proposal,
        genesis_obj=ex.genesis_gov,
        constitution_obj=unsorted,
        target_constitution_obj=ex.constitution_2,
        known_proposals={proposal.proposal_hash: proposal},
        now=NOW,
        policy=_policy(ex),
    )
    if tally.state is not TallyState.UNEVALUABLE:
        raise AssertionError(f"appended DORA: {tally.state}")
    kinds = {f.kind for f in tally.findings}
    if GovernanceFinding.MALFORMED_PARTICIPANTS not in kinds:
        raise AssertionError(f"appended DORA findings: {tally.findings}")


def verify_all() -> ExampleNucleus:
    """Alle Prüfungen aus example-nucleus.md; bricht bei der Bestandsanker-Probe zuerst."""
    ex = build()
    check_membership_epoch1(ex)
    check_tally(ex)
    check_ratification(ex)
    check_membership_epoch2(ex)
    check_trust_flow(ex)
    check_scope_separation(ex)
    check_malformed_appended_dora(ex)
    return ex


def _print_table(ex: ExampleNucleus) -> None:
    rows = [
        ("ANNA", ex.anna.pub),
        ("BRUNO", ex.bruno.pub),
        ("CHRIS", ex.chris.pub),
        ("DORA", ex.dora.pub),
        ("constitution_hash_gov", ex.constitution_hash_gov),
        ("N_gov", ex.N_gov),
        ("cbor(genesis_gov)", ex.genesis_gov_cbor),
        ("epoch_id_1", ex.epoch_1.epoch_id),
        ("constitution_hash_res", ex.constitution_hash_res),
        ("N_res", ex.N_res),
        ("cbor(genesis_res)", ex.genesis_res_cbor),
        ("constitution_hash_2", ex.constitution_hash_2),
        ("proposal_hash", ex.proposal.proposal_hash),
        ("epoch_id_2", ex.epoch_2.epoch_id),
    ]
    width = max(len(name) for name, _ in rows)
    for name, value in rows:
        print(f"{name:<{width}}  {value.hex()}")


def main() -> int:
    try:
        ex = verify_all()
    except AssertionError as exc:
        print(f"example-nucleus: {exc}", file=sys.stderr)
        return 1
    _print_table(ex)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
