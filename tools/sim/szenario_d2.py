#!/usr/bin/env python3
"""Szenario D′: saubere Isolierung von (a) und (b) (00aw, D338).

Wegwerf-Treiber. Drei unabhängige Läufe, kein geteilter Kontext.
Bausteine aus szenario_c.py und szenario_d.py, keine neuen Primitive.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from tools.sim.szenario import (
    _classify_row,
    _trust_row,
    _verdict_status_row,
    run_schritte,
)
from tools.sim.szenario_c import (
    A,
    B,
    C,
    Z,
    _baseline,
    _bis_verdikt,
    _welt,
    run_schritte_weiter,
)
from tools.sim.szenario_d import (
    _bis_verdikt_ohne_acc_verdict_zustellung,
    _verdict_status_namen,
)

FELDER = ("d", "C", "edges", "flow", "paths")
NAMEN = (A, B, C, Z)


def _drucke_trust_alle(titel: str, row: dict[str, dict[str, Any]]) -> None:
    print(titel)
    for name in NAMEN:
        k = row[name]
        print(
            f"  {name}: d={k['d']}  C={k['C']}  edges={k['edges']}  "
            f"flow={k['flow']}  paths={k['paths']}"
        )
    print()


def _drucke_status(titel: str, row: dict[str, dict[str, Any]], wer: tuple[str, ...]) -> None:
    print(titel)
    for name in wer:
        print(f"  {name}: {row[name]['status']}  findings={row[name]['findings']}")
    print()


def _drucke_classify(titel: str, row: dict[str, str], wer: tuple[str, ...]) -> None:
    print(titel)
    for name in wer:
        print(f"  {name}: {row[name]}")
    print()


def _gleich(a: dict[str, Any], b: dict[str, Any]) -> bool:
    return all(a[f] == b[f] for f in FELDER)


def _lauf1(pfad: str) -> dict[str, Any]:
    print("=== Lauf 1 — Broadcast ===")
    print()
    ctx = run_schritte([_welt(pfad), *_baseline(), *_bis_verdikt()])
    status = _verdict_status_row(ctx, "verdict_z")
    trust_b = _trust_row(ctx, B, [C])
    _drucke_status("verdict_status", status, NAMEN)
    _drucke_trust_alle("trust(C→B), Anker=chris", trust_b)
    return {"status": status, "trust_b": trust_b}


def _lauf2(pfad: str) -> dict[str, Any]:
    print("=== Lauf 2 — Umordnung ===")
    print()
    ctx = run_schritte(
        [_welt(pfad), *_baseline(), *_bis_verdikt_ohne_acc_verdict_zustellung()]
    )
    run_schritte_weiter(
        ctx,
        [
            {
                "art": "zustellen",
                "von": Z,
                "an": [B, C],
                "nur": ["verdict_z"],
            },
        ],
    )
    status_vor = _verdict_status_namen(ctx, "verdict_z", (B, C))
    classify_vor = _classify_row(ctx, "verdict_z")
    _drucke_status("verdict_status vor acc_a_b (bruno, chris)", status_vor, (B, C))
    _drucke_classify("classify(verdict_z) vor acc_a_b (bruno, chris)", classify_vor, (B, C))

    print("--- Nachlieferung acc_a_b an alle ---")
    run_schritte_weiter(ctx, [{"art": "zustellen", "von": A, "an": "alle"}])
    status_nach = _verdict_status_namen(ctx, "verdict_z", (B, C))
    classify_nach = _classify_row(ctx, "verdict_z")
    _drucke_status("verdict_status nach acc_a_b (bruno, chris)", status_nach, (B, C))
    _drucke_classify("classify(verdict_z) nach acc_a_b (bruno, chris)", classify_nach, (B, C))
    return {
        "status_vor": status_vor,
        "classify_vor": classify_vor,
        "status_nach": status_nach,
        "classify_nach": classify_nach,
    }


def _lauf3(pfad: str) -> dict[str, Any]:
    print("=== Lauf 3 — Dauerhafter Verlust ===")
    print()
    ctx = run_schritte([_welt(pfad), *_baseline(), *_bis_verdikt()])
    run_schritte_weiter(
        ctx,
        [
            {
                "art": "claim",
                "autor": C,
                "praedikat": "revoke",
                "target": "vouch_c_b",
                "t": 3,
            },
            {"art": "zustellen", "von": C, "an": [B, C, Z]},
        ],
    )
    trust_b = _trust_row(ctx, B, [C])
    _drucke_trust_alle("trust(C→B) nach partiellem Widerruf, Anker=chris", trust_b)
    return {"trust_b": trust_b}


def _befunde(lauf1: dict[str, Any], lauf2: dict[str, Any], lauf3: dict[str, Any]) -> None:
    print("=== Befunde ===")
    print()

    # (a)
    vor_b = lauf2["status_vor"][B]
    vor_c = lauf2["status_vor"][C]
    cl_b = lauf2["classify_vor"][B]
    cl_c = lauf2["classify_vor"][C]
    nach_b = lauf2["status_nach"][B]
    nach_c = lauf2["status_nach"][C]
    erwartung_vor = (
        vor_b["status"] == "ATTRIBUTED_OPINION"
        and "UNKNOWN_ACCUSATION" in vor_b["findings"]
        and vor_c["status"] == "ATTRIBUTED_OPINION"
        and "UNKNOWN_ACCUSATION" in vor_c["findings"]
        and cl_b == "active"
        and cl_c == "active"
    )
    erwartung_nach = nach_b["status"] == "BINDING" and nach_c["status"] == "BINDING"
    print(
        f"(a) Umordnung: vor bruno={vor_b['status']} {vor_b['findings']} "
        f"chris={vor_c['status']} {vor_c['findings']} "
        f"classify={cl_b}/{cl_c}; nach bruno={nach_b['status']} chris={nach_c['status']}"
    )
    if erwartung_vor and erwartung_nach:
        print(
            "(a) bestätigt — bruno/chris zeigen ATTRIBUTED_OPINION + "
            "UNKNOWN_ACCUSATION bei classify=active; nach Nachlieferung BINDING."
        )
    else:
        print(
            f"(a) widerlegt — vor wie erwartet={erwartung_vor}, "
            f"nach BINDING={erwartung_nach}."
        )
    print()

    # (b)
    t1 = lauf1["trust_b"]
    t3 = lauf3["trust_b"]
    anna_wie_lauf1 = _gleich(t3[A], t1[A])
    andere_weichen_ab = all(not _gleich(t3[n], t1[n]) for n in (B, C, Z))
    print(
        f"(b) Dauerverlust: anna={ {f: t3[A][f] for f in FELDER} } "
        f"Lauf-1={ {f: t1[A][f] for f in FELDER} }"
    )
    if anna_wie_lauf1 and andere_weichen_ab:
        print(
            "(b) bestätigt — anna behält den Vor-Widerruf-Wert aus Lauf 1, "
            "bruno/chris/dora zeigen den Nach-Widerruf-Wert."
        )
    else:
        print(
            f"(b) widerlegt — anna_wie_lauf1={anna_wie_lauf1}, "
            f"andere_weichen_ab={andere_weichen_ab}."
        )


def main() -> None:
    print("Szenario D′ — saubere Isolierung von (a) und (b) (D338)")
    print("A=anna  B=bruno  Z=dora  C=chris")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        lauf1 = _lauf1(str(Path(tmp) / "lauf1"))
        lauf2 = _lauf2(str(Path(tmp) / "lauf2"))
        lauf3 = _lauf3(str(Path(tmp) / "lauf3"))
    _befunde(lauf1, lauf2, lauf3)


if __name__ == "__main__":
    main()
