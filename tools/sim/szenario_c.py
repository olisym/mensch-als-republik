#!/usr/bin/env python3
"""Szenario C: Rechenschaft ohne Bindung (00av, D332).

Wegwerf-Treiber. Zwei Phasen aus identischen Baseline-Schritten, nicht sequenziell
auf demselben Zustand. Keine Golden Numbers.

Rollen (example_nucleus-Namen):
  A Ankläger      = anna
  B Beschuldigter = bruno
  Z Schiedsrichter = dora   (nicht in constitution_res.arbitration.arbitrators)
  C Beobachter    = chris
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from tools.sim.szenario import _trust_row, _verdict_status_row, run_schritte

T_EXP = 1001000

# A, B, Z, C — siehe Moduldocstring.
A, B, Z, C = "anna", "bruno", "dora", "chris"


def _welt(pfad: str) -> dict[str, Any]:
    return {
        "art": "welt",
        "pfad": pfad,
        "teilnehmer": [
            {"name": A, "seed": "11", "now": 1000},
            {"name": B, "seed": "12", "now": 1000},
            {"name": C, "seed": "13", "now": 1000},
            {"name": Z, "seed": "14", "now": 1000},
        ],
    }


def _baseline() -> list[dict[str, Any]]:
    """Vouch-Graph: C→B, C→Z, Z→B. Obligation B an A. Zwei Pfade C nach B."""
    return [
        {"art": "genesis", "quelle": "beispielnukleus"},
        {
            "art": "claim",
            "autor": C,
            "praedikat": "vouch",
            "scope": "res",
            "subject": B,
            "n": 50,
            "t": 1,
            "t_exp": T_EXP,
            "label": "vouch_c_b",
        },
        {
            "art": "claim",
            "autor": C,
            "praedikat": "vouch",
            "scope": "res",
            "subject": Z,
            "n": 50,
            "t": 2,
            "t_exp": T_EXP,
            "label": "vouch_c_z",
        },
        {
            "art": "claim",
            "autor": Z,
            "praedikat": "vouch",
            "scope": "res",
            "subject": B,
            "n": 50,
            "t": 1,
            "t_exp": T_EXP,
        },
        {"art": "zustellen", "von": C, "an": "alle"},
        {"art": "zustellen", "von": Z, "an": "alle"},
        {
            "art": "claim",
            "autor": B,
            "praedikat": "obligation",
            "scope": "res",
            "subject": A,
            "n": 10,
            "t": 1,
            "label": "obl_b_a",
        },
        {"art": "zustellen", "von": B, "an": "alle"},
    ]


def _bis_verdikt() -> list[dict[str, Any]]:
    return [
        {
            "art": "claim",
            "autor": A,
            "praedikat": "submit-arbitration",
            "scope": "res",
            "subject": Z,
            "t": 1,
            "label": "sub_a_z",
        },
        {
            "art": "claim",
            "autor": B,
            "praedikat": "submit-arbitration",
            "scope": "res",
            "subject": Z,
            "t": 2,
            "label": "sub_b_z",
        },
        {"art": "zustellen", "von": A, "an": "alle"},
        {"art": "zustellen", "von": B, "an": "alle"},
        {
            "art": "claim",
            "autor": A,
            "praedikat": "accusation",
            "scope": "res",
            "target": "obl_b_a",
            "t": 2,
            "label": "acc_a_b",
        },
        {"art": "zustellen", "von": A, "an": "alle"},
        {
            "art": "claim",
            "autor": Z,
            "praedikat": "verdict",
            "scope": "res",
            "target": "acc_a_b",
            "n": 1,
            "t": 2,
            "label": "verdict_z",
        },
        {"art": "zustellen", "von": Z, "an": "alle"},
    ]


def _kennzahlen(ctx: Any, subject: str) -> dict[str, Any]:
    """Trust-Kennzahlen zu subject aus Sicht von C (Anker = C)."""
    row = _trust_row(ctx, subject, [C])
    return row[C]


def _status(ctx: Any) -> dict[str, Any]:
    row = _verdict_status_row(ctx, "verdict_z")
    return row[C]


def _drucke_trust(titel: str, k: dict[str, Any]) -> None:
    print(
        f"{titel}: d={k['d']}  C={k['C']}  edges={k['edges']}  "
        f"flow={k['flow']}  paths={k['paths']}"
    )


def _phase1(pfad: str) -> dict[str, Any]:
    print("=== Phase 1 — Verdikt bindet ===")
    print()
    ctx = run_schritte([_welt(pfad), *_baseline(), *_bis_verdikt()])
    trust_b_vor = _kennzahlen(ctx, B)
    trust_z = _kennzahlen(ctx, Z)
    status = _status(ctx)
    print(f"verdict_status: {status['status']}  findings={status['findings']}")
    _drucke_trust("trust(C→B) vor Widerruf", trust_b_vor)
    _drucke_trust("trust(C→Z)", trust_z)
    print("Bond B: kein Bond-Primitiv im Baum, nichts hinterlegt")
    print()
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
            {"art": "zustellen", "von": C, "an": "alle"},
        ],
    )
    trust_b_nach = _kennzahlen(ctx, B)
    _drucke_trust("trust(C→B) nach Widerruf", trust_b_nach)
    print("Bond B nach verdict_status: unverändert — kein Bond hinterlegt")
    print()
    return {
        "status": status["status"],
        "trust_b_vor": trust_b_vor,
        "trust_b_nach": trust_b_nach,
        "trust_z": trust_z,
        "bond_vor": "kein Bond hinterlegt",
        "bond_nach": "kein Bond hinterlegt",
    }


def _phase2(pfad: str) -> dict[str, Any]:
    print("=== Phase 2 — Verdikt entzogen ===")
    print()
    ctx = run_schritte([_welt(pfad), *_baseline(), *_bis_verdikt()])
    trust_b_vor = _kennzahlen(ctx, B)
    trust_z = _kennzahlen(ctx, Z)
    run_schritte_weiter(
        ctx,
        [
            {
                "art": "claim",
                "autor": B,
                "praedikat": "revoke",
                "target": "sub_b_z",
                "t": 3,
            },
            {"art": "zustellen", "von": B, "an": "alle"},
        ],
    )
    status = _status(ctx)
    print(f"verdict_status: {status['status']}  findings={status['findings']}")
    _drucke_trust("trust(C→B) vor Policy-Widerruf", trust_b_vor)
    _drucke_trust("trust(C→Z)", trust_z)
    print("Bond B: kein Bond-Primitiv im Baum, nichts hinterlegt")
    print()
    # Beobachter-Policy, nicht Protokoll: C widerruft, wenn trust_flow(C, Z) > 0.
    if trust_z["flow"] > 0:
        print(f"Policy C: trust_flow(C,Z)={trust_z['flow']} > 0 → widerruft Vouch auf B")
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
                {"art": "zustellen", "von": C, "an": "alle"},
            ],
        )
    else:
        print(f"Policy C: trust_flow(C,Z)={trust_z['flow']} → kein Widerruf")
    trust_b_nach = _kennzahlen(ctx, B)
    _drucke_trust("trust(C→B) nach Policy-Widerruf", trust_b_nach)
    print("Bond B nach verdict_status: unverändert — kein Bond hinterlegt")
    print()
    return {
        "status": status["status"],
        "trust_b_vor": trust_b_vor,
        "trust_b_nach": trust_b_nach,
        "trust_z": trust_z,
        "bond_vor": "kein Bond hinterlegt",
        "bond_nach": "kein Bond hinterlegt",
        "policy_widerruf": trust_z["flow"] > 0,
    }


def run_schritte_weiter(ctx: Any, schritte: list[dict[str, Any]]) -> None:
    """Hängt Schritte an einen bestehenden Kontext (kein neues Welt-Anlegen)."""
    from tools.sim.szenario import (
        _schritt_claim,
        _schritt_erwarte,
        _schritt_genesis,
        _schritt_uhr,
        _schritt_welt,
        _schritt_zeige,
        _schritt_zustellen,
    )

    for step in schritte:
        art = step["art"]
        if art == "welt":
            _schritt_welt(step, ctx)
        elif art == "genesis":
            _schritt_genesis(step, ctx)
        elif art == "claim":
            _schritt_claim(step, ctx)
        elif art == "zustellen":
            _schritt_zustellen(step, ctx)
        elif art == "uhr":
            _schritt_uhr(step, ctx)
        elif art == "zeige":
            text = _schritt_zeige(step, ctx)
            if text:
                print(text)
                print()
        elif art == "erwarte":
            _schritt_erwarte(step, ctx)
        else:
            raise ValueError(f"unknown step art: {art!r}")


def _gleich(a: dict[str, Any], b: dict[str, Any], felder: tuple[str, ...]) -> bool:
    return all(a[f] == b[f] for f in felder)


def main() -> None:
    print("Szenario C — Rechenschaft ohne Bindung (D332)")
    print("A=anna  B=bruno  Z=dora  C=chris")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _phase1(str(Path(tmp) / "phase1"))
        p2 = _phase2(str(Path(tmp) / "phase2"))

    print("=== Vergleich ===")
    print()
    print(f"Phase 1 verdict_status: {p1['status']}")
    print(f"Phase 2 verdict_status: {p2['status']}")
    print()
    felder = ("d", "C", "edges", "flow", "paths")
    print("trust(C→B) nach jeweiligem Vouch-Widerruf:")
    _drucke_trust("  Phase 1", p1["trust_b_nach"])
    _drucke_trust("  Phase 2", p2["trust_b_nach"])
    gleich = _gleich(p1["trust_b_nach"], p2["trust_b_nach"], felder)
    print(f"  identisch: {gleich}")
    print()
    print(f"Bond Phase 1 vor/nach: {p1['bond_vor']} / {p1['bond_nach']}")
    print(f"Bond Phase 2 vor/nach: {p2['bond_vor']} / {p2['bond_nach']}")
    print("  Unterschied zwischen Phasen: keiner — kein Bond-Primitiv")


if __name__ == "__main__":
    main()
