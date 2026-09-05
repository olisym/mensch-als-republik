#!/usr/bin/env python3
"""Szenario E: Equivocation unter Partition (00aw, D340).

Wegwerf-Treiber. Zwei unabhängige Läufe, kein geteilter Kontext.
Bausteine aus szenario_c.py und szenario.py, keine neuen Primitive.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from tools.sim.szenario import _classify_row, _trust_row, run_schritte
from tools.sim.szenario_c import (
    A,
    B,
    C,
    T_EXP,
    Z,
    _baseline,
    _welt,
    run_schritte_weiter,
)

FELDER = ("d", "C", "edges", "flow", "paths")
NAMEN = (A, B, C, Z)


def _gabel() -> list[dict[str, Any]]:
    """Brunos Equivocation-Paar plus unbeteiligte Dritt-Vouch (D340)."""
    return [
        {
            "art": "claim",
            "autor": B,
            "praedikat": "vouch",
            "scope": "res",
            "subject": Z,
            "n": 40,
            "t": 2,
            "t_exp": T_EXP,
            "label": "fork_b_dora",
            "kette_fortschreiben": False,
        },
        {
            "art": "claim",
            "autor": B,
            "praedikat": "vouch",
            "scope": "res",
            "subject": C,
            "n": 30,
            "t": 2,
            "t_exp": T_EXP,
            "label": "real_b_chris",
        },
        {
            "art": "claim",
            "autor": B,
            "praedikat": "vouch",
            "scope": "res",
            "subject": A,
            "n": 20,
            "t": 3,
            "t_exp": T_EXP,
            "label": "legit_b_anna",
        },
    ]


def _drucke_trust_alle(titel: str, row: dict[str, dict[str, Any]]) -> None:
    print(titel)
    for name in NAMEN:
        k = row[name]
        print(
            f"  {name}: d={k['d']}  C={k['C']}  edges={k['edges']}  "
            f"flow={k['flow']}  paths={k['paths']}"
        )
    print()


def _drucke_classify(titel: str, row: dict[str, str]) -> None:
    print(titel)
    for name in NAMEN:
        print(f"  {name}: {row[name]}")
    print()


def _kennzahlen(k: dict[str, Any]) -> dict[str, Any]:
    return {f: k[f] for f in FELDER}


def _gleich(a: dict[str, Any], b: dict[str, Any]) -> bool:
    return all(a[f] == b[f] for f in FELDER)


def _niedriger(nach: dict[str, Any], vor: dict[str, Any]) -> bool:
    """Wahr, wenn flow fällt oder das Ziel unerreichbar wird."""
    if vor["flow"] is None:
        return False
    if nach["flow"] is None:
        return True
    return nach["flow"] < vor["flow"]


def _lauf1(pfad: str) -> dict[str, Any]:
    print("=== Lauf 1 — Getrennte Partition ===")
    print()
    ctx = run_schritte([_welt(pfad), *_baseline(), *_gabel()])
    run_schritte_weiter(
        ctx,
        [
            {"art": "zustellen", "von": B, "an": [Z], "nur": ["fork_b_dora"]},
            {
                "art": "zustellen",
                "von": B,
                "an": [A, C],
                "nur": ["real_b_chris", "legit_b_anna"],
            },
        ],
    )
    trust_dora = _trust_row(ctx, Z, [C])
    trust_anna = _trust_row(ctx, A, [C])
    _drucke_trust_alle("trust(C→dora), Anker=chris", trust_dora)
    _drucke_trust_alle("trust(C→anna), Anker=chris", trust_anna)
    return {
        "trust_dora": trust_dora,
        "trust_anna": trust_anna,
        "classify_real": _classify_row(ctx, "real_b_chris"),
        "classify_fork": _classify_row(ctx, "fork_b_dora"),
    }


def _lauf2(pfad: str) -> dict[str, Any]:
    print("=== Lauf 2 — Späte Konvergenz ===")
    print()
    ctx = run_schritte([_welt(pfad), *_baseline(), *_gabel()])
    run_schritte_weiter(
        ctx,
        [
            {
                "art": "zustellen",
                "von": B,
                "an": [A, C],
                "nur": ["real_b_chris", "legit_b_anna"],
            },
        ],
    )
    classify_vor = _classify_row(ctx, "real_b_chris")
    trust_dora_vor = _trust_row(ctx, Z, [C])
    trust_anna_vor = _trust_row(ctx, A, [C])
    print("--- vorher ---")
    _drucke_classify("classify(real_b_chris)", classify_vor)
    _drucke_trust_alle("trust(C→dora), Anker=chris", trust_dora_vor)
    _drucke_trust_alle("trust(C→anna), Anker=chris", trust_anna_vor)

    run_schritte_weiter(
        ctx,
        [{"art": "zustellen", "von": B, "an": [C], "nur": ["fork_b_dora"]}],
    )
    classify_nach = _classify_row(ctx, "real_b_chris")
    trust_dora_nach = _trust_row(ctx, Z, [C])
    trust_anna_nach = _trust_row(ctx, A, [C])
    print("--- nachher (fork_b_dora nur an chris) ---")
    _drucke_classify("classify(real_b_chris)", classify_nach)
    _drucke_trust_alle("trust(C→dora), Anker=chris", trust_dora_nach)
    _drucke_trust_alle("trust(C→anna), Anker=chris", trust_anna_nach)
    return {
        "classify_vor": classify_vor,
        "classify_nach": classify_nach,
        "trust_dora_vor": trust_dora_vor,
        "trust_anna_vor": trust_anna_vor,
        "trust_dora_nach": trust_dora_nach,
        "trust_anna_nach": trust_anna_nach,
    }


def _befunde(lauf1: dict[str, Any], lauf2: dict[str, Any]) -> None:
    print("=== Befunde ===")
    print()

    td = lauf1["trust_dora"]
    ta = lauf1["trust_anna"]
    dora_c_z_anders = all(not _gleich(td[Z], td[n]) for n in (A, B, C))
    # C→anna: anna/chris haben legit_b_anna, dora nicht; bruno schließt alle eigenen Vouches aus.
    anna_chris_gleich = _gleich(ta[A], ta[C])
    dora_wie_bruno = ta[Z]["flow"] == ta[B]["flow"] == 0
    anna_chris_positiv = ta[A]["flow"] > 0 and ta[C]["flow"] > 0
    print(
        f"(Lauf 1) trust(C→dora) dora={_kennzahlen(td[Z])} "
        f"anna={_kennzahlen(td[A])} bruno={_kennzahlen(td[B])} chris={_kennzahlen(td[C])}"
    )
    print(
        f"(Lauf 1) trust(C→anna) dora={_kennzahlen(ta[Z])} "
        f"anna={_kennzahlen(ta[A])} bruno={_kennzahlen(ta[B])} chris={_kennzahlen(ta[C])}"
    )
    print(
        f"(Lauf 1) classify real/fork: "
        f"anna={lauf1['classify_real'][A]}/{lauf1['classify_fork'][A]} "
        f"bruno={lauf1['classify_real'][B]}/{lauf1['classify_fork'][B]} "
        f"chris={lauf1['classify_real'][C]}/{lauf1['classify_fork'][C]} "
        f"dora={lauf1['classify_real'][Z]}/{lauf1['classify_fork'][Z]}"
    )
    if (
        dora_c_z_anders
        and anna_chris_gleich
        and dora_wie_bruno
        and anna_chris_positiv
    ):
        print(
            "(Lauf 1) widerlegt — kein Fehler, stille Divergenz ja, aber nicht die "
            "Prompt-Gruppe „dora vs chris/anna/bruno“. C→dora: dora flow=70/paths=2, "
            "die anderen flow=50/paths=1 (bruno mit weniger Kanten, weil er beide "
            "Hälften besitzt und alle eigenen Vouches ausschließt). C→anna: "
            "anna/chris flow=10, dora/bruno flow=0. classify der jeweils fehlenden "
            "Hälfte ist flagged, weil classify das Label-Objekt gegen den Store "
            "prüft; im eigenen inbox bleibt die besessene Hälfte active."
        )
    else:
        print(
            f"(Lauf 1) widerlegt — dora_c_z_anders={dora_c_z_anders}, "
            f"anna_chris_gleich={anna_chris_gleich}, "
            f"dora_wie_bruno={dora_wie_bruno}, "
            f"anna_chris_positiv={anna_chris_positiv}."
        )
    print()

    cl_vor = lauf2["classify_vor"][C]
    cl_nach = lauf2["classify_nach"][C]
    dora_flow_faellt = _niedriger(lauf2["trust_dora_nach"][C], lauf2["trust_dora_vor"][C])
    anna_flow_faellt = _niedriger(lauf2["trust_anna_nach"][C], lauf2["trust_anna_vor"][C])
    dora_edges_faellt = (
        lauf2["trust_dora_nach"][C]["edges"] < lauf2["trust_dora_vor"][C]["edges"]
    )
    print(
        f"(Lauf 2) classify(real_b_chris) chris: {cl_vor} → {cl_nach}; "
        f"trust(C→dora) chris {_kennzahlen(lauf2['trust_dora_vor'][C])} → "
        f"{_kennzahlen(lauf2['trust_dora_nach'][C])}; "
        f"trust(C→anna) chris {_kennzahlen(lauf2['trust_anna_vor'][C])} → "
        f"{_kennzahlen(lauf2['trust_anna_nach'][C])}"
    )
    if cl_vor == "active" and cl_nach == "equivocation_flagged" and dora_flow_faellt and anna_flow_faellt:
        print(
            "(Lauf 2) bestätigt — classify kippt bei chris auf equivocation_flagged; "
            "trust(chris→dora) und trust(chris→anna) fallen beide."
        )
    elif (
        cl_vor == "active"
        and cl_nach == "equivocation_flagged"
        and anna_flow_faellt
        and not dora_flow_faellt
    ):
        print(
            "(Lauf 2) widerlegt — classify kippt wie erwartet und trust(chris→anna) "
            "fällt (10→0: legit_b_anna wird mit allen Vouch-Gruppen des Autors "
            "ausgeschlossen). trust-flow(chris→dora) fällt nicht (50→50); "
            f"nur die Kantenanzahl {'fällt' if dora_edges_faellt else 'bleibt'} "
            f"({lauf2['trust_dora_vor'][C]['edges']}→"
            f"{lauf2['trust_dora_nach'][C]['edges']}), weil chris fork_b_dora "
            "vorher nicht hatte und C→Z in der Baseline das Flag überlebt."
        )
    else:
        print(
            f"(Lauf 2) widerlegt — classify {cl_vor}→{cl_nach}, "
            f"dora_flow_fällt={dora_flow_faellt}, anna_flow_fällt={anna_flow_faellt}."
        )


def main() -> None:
    print("Szenario E — Equivocation unter Partition (D340)")
    print("A=anna  B=bruno  Z=dora  C=chris")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        lauf1 = _lauf1(str(Path(tmp) / "lauf1"))
        lauf2 = _lauf2(str(Path(tmp) / "lauf2"))
    _befunde(lauf1, lauf2)


if __name__ == "__main__":
    main()
