#!/usr/bin/env python3
"""Szenario F: Governance-Ratifizierung unter Partition (00ax, D311).

Wegwerf-Treiber. Zwei unabhängige Läufe, kein geteilter Kontext.
Stimmen und ratify@1 über Welt.zustellen; Verfassungs- und Vorschlagsobjekte
über pro Beobachter geführte Dicts. Keine neuen Primitive.
"""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path
from typing import Any

from symbolon import cbor_canon
from symbolon.atom import Claim, claim_id
from symbolon.domains import DOM_NUC_GEN
from symbolon.governance import Epoch, Proposal, decide, resolve_epoch
from symbolon.governance.findings import Finding
from symbolon.policy import constitution_hash
from tools.sim.welt import Welt

A, B, C, Z = "anna", "bruno", "chris", "dora"
NAMEN = (A, B, C, Z)
NAMEN_SEED = {A: 0x11, B: 0x12, C: 0x13, Z: 0x14}
NOW = 1000


def _nuc(scope: bytes, name: str) -> str:
    return f"nuc:{scope.hex()}/{name}@1"


def _kurz(value: bytes) -> str:
    return value.hex()[:16]


def _verfassung(
    participants: list[bytes],
    *,
    arbitrator: bytes,
) -> dict[str, Any]:
    return {
        "irrevocable_predicates": ["obligation@1", "ratify@1", "vote@1"],
        "thresholds": {
            "ordinary": [1, 2],
            "membership": [1, 2],
            "amendment": [1, 2],
        },
        "arbitration": {"arbitrators": [arbitrator]},
        "participants": participants,
    }


def _welt(pfad: str) -> Welt:
    welt = Welt.anlegen(Path(pfad))
    for name in NAMEN:
        welt.teilnehmer_anlegen(name, bytes([NAMEN_SEED[name]] * 32), NOW)
    return welt


def _aufbau(welt: Welt) -> dict[str, Any]:
    """Genesis, rivalisierende Vorschläge, Stimmen und ratify@1 (04 §1.1, §2, §4.4)."""
    pubs = {name: welt.teilnehmer[name].pub for name in NAMEN}
    participants = sorted(pubs.values())
    constitution_1 = _verfassung(participants, arbitrator=pubs[A])
    constitution_a = _verfassung(participants, arbitrator=pubs[B])
    constitution_b = _verfassung(participants, arbitrator=pubs[Z])
    hash_1 = constitution_hash(constitution_1)
    hash_a = constitution_hash(constitution_a)
    hash_b = constitution_hash(constitution_b)
    genesis = {
        0: 1,
        1: [pubs[A]],
        2: 0,
        3: [pubs[A]],
        4: hash_1,
        5: 2,
        6: 0,
        7: 0,
    }
    n = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    epoch_1 = Epoch(scope=n, index=1, constitution_hash=hash_1)
    proposal_a = Proposal(
        scope=n, predecessor=epoch_1.epoch_id, constitution_hash=hash_a
    )
    proposal_b = Proposal(
        scope=n, predecessor=epoch_1.epoch_id, constitution_hash=hash_b
    )

    def _ja(autor: str, proposal: Proposal, t: int) -> Claim:
        return welt.teilnehmer[autor].claim_signieren(
            p=_nuc(n, "vote"),
            J=(3, proposal.proposal_hash),
            t=t,
            v=cbor_canon.encode({0: 1}),
            N=n,
        )

    anna_a = _ja(A, proposal_a, 1)
    bruno_a = _ja(B, proposal_a, 1)
    chris_a = _ja(C, proposal_a, 1)
    chris_b = _ja(C, proposal_b, 2)
    ratify = welt.teilnehmer[A].claim_signieren(
        p=_nuc(n, "ratify"),
        J=(3, proposal_a.proposal_hash),
        t=2,
        v=cbor_canon.encode(
            {0: [claim_id(anna_a), claim_id(bruno_a), claim_id(chris_a)]}
        ),
        N=n,
    )
    return {
        "N": n,
        "genesis": genesis,
        "epoch_1": epoch_1,
        "constitution_1": constitution_1,
        "constitution_a": constitution_a,
        "constitution_b": constitution_b,
        "hash_1": hash_1,
        "hash_a": hash_a,
        "hash_b": hash_b,
        "proposal_a": proposal_a,
        "proposal_b": proposal_b,
        "anna_a": anna_a,
        "bruno_a": bruno_a,
        "chris_a": chris_a,
        "chris_b": chris_b,
        "ratify": ratify,
        "known_constitutions": {name: {} for name in NAMEN},
        "known_proposals": {name: {} for name in NAMEN},
    }


def _kennt_verfassung(ex: dict[str, Any], name: str, obj: dict[str, Any]) -> None:
    ex["known_constitutions"][name][constitution_hash(obj)] = obj


def _kennt_vorschlag(ex: dict[str, Any], name: str, proposal: Proposal) -> None:
    ex["known_proposals"][name][proposal.proposal_hash] = proposal


def _vermerke(findings: tuple[Finding, ...]) -> list[str]:
    return [f"{f.kind.value} subject={_kurz(f.subject)}" for f in findings]


def _beobachte(welt: Welt, ex: dict[str, Any], name: str) -> dict[str, Any]:
    """resolve_epoch plus decide(A) gegen die lokale Sicht (04 §3, §4.5)."""
    tp = welt.teilnehmer[name]
    store = tp.store_laden()
    now = tp.read_now()
    known_c = ex["known_constitutions"][name]
    known_p = ex["known_proposals"][name]
    resolution = resolve_epoch(
        store,
        scope=ex["N"],
        genesis_obj=ex["genesis"],
        known_constitutions=known_c,
        known_proposals=known_p,
        now=now,
    )
    constitution_1 = known_c.get(ex["hash_1"])
    constitution_a = known_c.get(ex["hash_a"])
    tally = decide(
        store,
        epoch=ex["epoch_1"],
        proposal=ex["proposal_a"],
        genesis_obj=ex["genesis"],
        constitution_obj=constitution_1,
        target_constitution_obj=constitution_a,
        known_proposals=known_p,
        now=now,
    )
    reached_hash = resolution.epoch.constitution_hash
    return {
        "name": name,
        "index": resolution.epoch.index,
        "constitution_hash": reached_hash,
        "tally_state": tally.state.value,
        "tally_findings": _vermerke(tally.findings),
        "chain_findings": _vermerke(resolution.findings),
    }


def _drucke_beobachter(row: dict[str, Any]) -> None:
    print(
        f"  {row['name']}: Epoche {row['index']}  "
        f"constitution_hash={_kurz(row['constitution_hash'])}  "
        f"tally.A={row['tally_state']}"
    )
    print("    Vermerke decide(A):")
    if row["tally_findings"]:
        for line in row["tally_findings"]:
            print(f"      {line}")
    else:
        print("      (keine)")
    print("    Vermerke resolve_epoch:")
    if row["chain_findings"]:
        for line in row["chain_findings"]:
            print(f"      {line}")
    else:
        print("      (keine)")
    print()


def _genesis_allen(ex: dict[str, Any]) -> None:
    for name in NAMEN:
        _kennt_verfassung(ex, name, ex["constitution_1"])


def _lauf1(pfad: str) -> dict[str, dict[str, Any]]:
    print("=== Lauf 1 — Broadcast ===")
    print()
    welt = _welt(pfad)
    ex = _aufbau(welt)
    _genesis_allen(ex)
    for name in NAMEN:
        _kennt_vorschlag(ex, name, ex["proposal_a"])
        _kennt_vorschlag(ex, name, ex["proposal_b"])
        _kennt_verfassung(ex, name, ex["constitution_a"])
        _kennt_verfassung(ex, name, ex["constitution_b"])
    welt.zustellen(A, "alle")
    welt.zustellen(B, "alle")
    welt.zustellen(C, "alle")
    rows = {name: _beobachte(welt, ex, name) for name in NAMEN}
    for name in NAMEN:
        _drucke_beobachter(rows[name])
    return rows


def _lauf2(pfad: str) -> dict[str, Any]:
    print("=== Lauf 2 — Partition ===")
    print()
    welt = _welt(pfad)
    ex = _aufbau(welt)
    _genesis_allen(ex)

    print("--- Stufe 1 — nur A bekannt (bruno) ---")
    welt.zustellen(A, [B])
    welt.zustellen(C, [B], nur=[claim_id(ex["chris_a"])])
    _kennt_vorschlag(ex, B, ex["proposal_a"])
    _kennt_verfassung(ex, B, ex["constitution_a"])
    stufe1 = _beobachte(welt, ex, B)
    _drucke_beobachter(stufe1)

    print("--- Stufe 2 — Konfliktstimme ohne Proposal_B (bruno) ---")
    welt.zustellen(C, [B], nur=[claim_id(ex["chris_b"])])
    stufe2 = _beobachte(welt, ex, B)
    _drucke_beobachter(stufe2)

    print("--- Stufe 3 — Heilung, Proposal_B trifft ein (bruno) ---")
    _kennt_vorschlag(ex, B, ex["proposal_b"])
    stufe3 = _beobachte(welt, ex, B)
    _drucke_beobachter(stufe3)

    print("--- Fall (b) — dauerhafter Objektverlust (dora) ---")
    welt.zustellen(A, [Z])
    welt.zustellen(B, [Z], nur=[claim_id(ex["bruno_a"])])
    welt.zustellen(C, [Z], nur=[claim_id(ex["chris_a"])])
    fall_b = _beobachte(welt, ex, Z)
    _drucke_beobachter(fall_b)

    return {
        "stufe1": stufe1,
        "stufe2": stufe2,
        "stufe3": stufe3,
        "fall_b": fall_b,
    }


def _hat(rows: list[str], kind: str) -> bool:
    return any(line.startswith(kind + " ") for line in rows)


def _befunde(
    lauf1: dict[str, dict[str, Any]],
    lauf2: dict[str, Any],
) -> None:
    print("=== Befunde ===")
    print()

    epochen = {name: lauf1[name]["index"] for name in NAMEN}
    tallies = {name: lauf1[name]["tally_state"] for name in NAMEN}
    konflikte = all(
        _hat(lauf1[name]["tally_findings"], "CONFLICTING_APPROVAL")
        for name in NAMEN
    )
    identisch = (
        len(set(epochen.values())) == 1
        and len(set(tallies.values())) == 1
        and all(lauf1[name]["index"] == 1 for name in NAMEN)
        and all(lauf1[name]["tally_state"] == "PENDING" for name in NAMEN)
        and konflikte
    )
    print(
        f"(Lauf 1) Epochen={epochen} tally.A={tallies} "
        f"CONFLICTING_APPROVAL überall={konflikte}"
    )
    if identisch:
        print(
            "(Lauf 1) bestätigt — alle vier Beobachter bei Epoche 1, "
            "decide(A)=PENDING, CONFLICTING_APPROVAL auf der lokalen Sicht."
        )
    else:
        print(
            "(Lauf 1) widerlegt — Beobachter nicht identisch bei Epoche 1 / "
            "PENDING / CONFLICTING_APPROVAL."
        )
    print()

    s1 = lauf2["stufe1"]
    s2 = lauf2["stufe2"]
    s3 = lauf2["stufe3"]
    print(
        f"(Stufe 1) Epoche {s1['index']} tally.A={s1['tally_state']} "
        f"hash={_kurz(s1['constitution_hash'])}"
    )
    if s1["index"] == 2 and s1["tally_state"] == "PASSED":
        print(
            "(Stufe 1) bestätigt — decide(A)=PASSED, ratify@1 trägt, Epoche 2."
        )
    else:
        print(
            f"(Stufe 1) widerlegt — Epoche {s1['index']}, "
            f"tally.A={s1['tally_state']}."
        )
    print()

    rueckfall = s1["index"] == 2 and s2["index"] == 1
    unknown = _hat(s2["tally_findings"], "UNKNOWN_PROPOSAL")
    print(
        f"(Stufe 2) Epoche {s1['index']}→{s2['index']} "
        f"tally.A={s2['tally_state']} UNKNOWN_PROPOSAL={unknown}"
    )
    if rueckfall and unknown:
        print(
            "(Stufe 2) bestätigt — Epochen-Rückfall 2→1; "
            "UNKNOWN_PROPOSAL schließt chris aus; resolve_epoch baut die "
            "Kette bei jedem Aufruf neu."
        )
    elif unknown and not rueckfall:
        print(
            f"(Stufe 2) kein Rückfall — UNKNOWN_PROPOSAL ja, Epoche bleibt "
            f"{s2['index']}, tally.A={s2['tally_state']}."
        )
    else:
        print(
            f"(Stufe 2) widerlegt — Rückfall={rueckfall}, "
            f"UNKNOWN_PROPOSAL={unknown}, tally.A={s2['tally_state']}."
        )
    print()

    conflict = _hat(s3["tally_findings"], "CONFLICTING_APPROVAL")
    unknown3 = _hat(s3["tally_findings"], "UNKNOWN_PROPOSAL")
    gleich = (
        s3["index"] == s2["index"]
        and s3["tally_state"] == s2["tally_state"]
        and s3["constitution_hash"] == s2["constitution_hash"]
    )
    print(
        f"(Stufe 3) Epoche {s3['index']} tally.A={s3['tally_state']} "
        f"CONFLICTING_APPROVAL={conflict} UNKNOWN_PROPOSAL={unknown3} "
        f"gleich_Stufe2={gleich}"
    )
    if gleich and conflict and not unknown3:
        print(
            "(Stufe 3) bestätigt — Diagnose wechselt auf "
            "CONFLICTING_APPROVAL; Epoche und tally.state unverändert."
        )
    else:
        print(
            "(Stufe 3) widerlegt — Diagnose oder Ergebnis weicht von der "
            "Erwartung (nur präzisere Diagnose) ab."
        )
    print()

    fb = lauf2["fall_b"]
    missing = _hat(fb["chain_findings"], "EPOCH_PROPOSAL_UNAVAILABLE")
    print(
        f"(Fall b) Epoche {fb['index']} tally.A={fb['tally_state']} "
        f"EPOCH_PROPOSAL_UNAVAILABLE={missing}"
    )
    if fb["index"] == 1 and missing:
        print(
            "(Fall b) bestätigt — ohne Proposal_A bleibt die Epoche bei 1, "
            "Vermerk EPOCH_PROPOSAL_UNAVAILABLE."
        )
    else:
        print(
            f"(Fall b) widerlegt — Epoche {fb['index']}, "
            f"EPOCH_PROPOSAL_UNAVAILABLE={missing}."
        )


def main() -> None:
    print("Szenario F — Governance-Ratifizierung unter Partition (00ax)")
    print("A=anna  B=bruno  C=chris  Z=dora")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        lauf1 = _lauf1(str(Path(tmp) / "lauf1"))
        lauf2 = _lauf2(str(Path(tmp) / "lauf2"))
    _befunde(lauf1, lauf2)


if __name__ == "__main__":
    main()
