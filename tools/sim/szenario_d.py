#!/usr/bin/env python3
"""Szenario D: Rechenschaft unter Partition (00aw, D336).

Wegwerf-Treiber nach dem Vorbild von szenario_c.py. Keine neuen Primitive.
Zwei unabhängige Läufe aus denselben Stufe-C-Bausteinen.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from symbolon.profiles import verdict_status

from tools.sim.szenario import (
    _classify_row,
    _policy,
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

FELDER = ("d", "C", "edges", "flow", "paths")
NAMEN = (A, B, C, Z)
ANNA_NOW_DRIFT = 2_000_000


def _bis_verdikt_ohne_acc_verdict_zustellung() -> list[dict[str, Any]]:
    """Wie _bis_verdikt, aber ohne die Zustellung von acc_a_b und verdict_z."""
    schritte: list[dict[str, Any]] = []
    skip_naechste_zustellung = False
    for step in _bis_verdikt():
        if step.get("art") == "claim" and step.get("label") in ("acc_a_b", "verdict_z"):
            schritte.append(step)
            skip_naechste_zustellung = True
            continue
        if skip_naechste_zustellung and step.get("art") == "zustellen":
            skip_naechste_zustellung = False
            continue
        schritte.append(step)
    return schritte


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


def _drucke_classify(titel: str, row: dict[str, str], wer: tuple[str, ...] | None = None) -> None:
    print(titel)
    for name in wer or NAMEN:
        print(f"  {name}: {row[name]}")
    print()


def _gleich(a: dict[str, Any], b: dict[str, Any]) -> bool:
    return all(a[f] == b[f] for f in FELDER)


def _verdict_status_namen(
    ctx: Any, label: str, namen: tuple[str, ...]
) -> dict[str, dict[str, Any]]:
    """Wie `_verdict_status_row`, beschränkt auf `namen`.

    `_verdict_status_row` läuft über alle Teilnehmer und wirft
    `ValueError("verdict not in store")`, sobald der Claim lokal fehlt.
    """
    assert ctx.welt is not None and ctx.ex is not None
    verdict = ctx.labels[label]
    arbitrators = frozenset(ctx.ex.constitution_res["arbitration"]["arbitrators"])
    policy = _policy(ctx.ex, ctx.ex.N_res)
    row: dict[str, dict[str, Any]] = {}
    for name in namen:
        tp = ctx.welt.teilnehmer[name]
        result = verdict_status(
            tp.store_laden(),
            verdict=verdict,
            scope=ctx.ex.N_res,
            arbitrators=arbitrators,
            now=tp.read_now(),
            policy=policy,
        )
        row[name] = {
            "status": result.status.value,
            "findings": sorted(f.kind.value for f in result.findings),
        }
    return row


def _lauf1(pfad: str) -> dict[str, Any]:
    print("=== Lauf 1 — Broadcast ===")
    print()
    ctx = run_schritte([_welt(pfad), *_baseline(), *_bis_verdikt()])
    status = _verdict_status_row(ctx, "verdict_z")
    trust_b = _trust_row(ctx, B, [C])
    _drucke_status("verdict_status", status, NAMEN)
    _drucke_trust_alle("trust(C→B), Anker=chris", trust_b)
    return {"status": status, "trust_b": trust_b}


def _lauf2(pfad: str, lauf1: dict[str, Any]) -> dict[str, Any]:
    print("=== Lauf 2 — Funkstille ===")
    print()
    ctx = run_schritte(
        [_welt(pfad), *_baseline(), *_bis_verdikt_ohne_acc_verdict_zustellung()]
    )

    # (a) verdict_z vor acc_a_b, nur an anna und chris.
    print("--- (a) Umordnung: verdict vor accusation ---")
    ausnahme_a: str | None = None
    try:
        run_schritte_weiter(
            ctx,
            [
                {
                    "art": "zustellen",
                    "von": Z,
                    "an": [A, C],
                    "nur": ["verdict_z"],
                },
            ],
        )
        status_vor = _verdict_status_namen(ctx, "verdict_z", (A, C))
        classify_vor = _classify_row(ctx, "verdict_z")
        _drucke_status("verdict_status vor acc_a_b (anna, chris)", status_vor, (A, C))
        _drucke_classify("classify(verdict_z) vor acc_a_b (anna, chris)", classify_vor, (A, C))
    except Exception as exc:  # noqa: BLE001 — Szenario: Exception ist selbst der Befund
        ausnahme_a = f"{type(exc).__name__}: {exc}"
        print(f"AUSNAHME bei (a) vor Nachlieferung: {ausnahme_a}")
        print()
        status_vor = {}
        classify_vor = {}

    print("--- (a) Nachlieferung acc_a_b an alle ---")
    run_schritte_weiter(ctx, [{"art": "zustellen", "von": A, "an": "alle"}])
    status_nach = _verdict_status_namen(ctx, "verdict_z", (A, C))
    _drucke_status("verdict_status nach acc_a_b (anna, chris)", status_nach, (A, C))

    # (c) vor (b): Annas Uhr über T_EXP, die anderen bleiben bei 1000.
    print("--- (c) Uhrendrift anna ---")
    assert ctx.welt is not None
    ctx.welt.teilnehmer[A].write_now(ANNA_NOW_DRIFT)
    classify_vouch = _classify_row(ctx, "vouch_c_b")
    _drucke_classify("classify(vouch_c_b) nach Uhrendrift", classify_vouch)
    trust_nach_uhr = _trust_row(ctx, B, [C])
    _drucke_trust_alle("trust(C→B) nach Uhrendrift, vor Widerruf", trust_nach_uhr)

    # (b) Revoke nur an bruno und dora, niemals an anna.
    print("--- (b) Widerruf vouch_c_b, nicht an anna ---")
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
            {"art": "zustellen", "von": C, "an": [B, Z]},
        ],
    )
    trust_b = _trust_row(ctx, B, [C])
    _drucke_trust_alle("trust(C→B) nach partiellem Widerruf, Anker=chris", trust_b)

    return {
        "ausnahme_a": ausnahme_a,
        "status_vor": status_vor,
        "classify_vor": classify_vor,
        "status_nach": status_nach,
        "classify_vouch": classify_vouch,
        "trust_nach_uhr": trust_nach_uhr,
        "trust_b": trust_b,
        "lauf1": lauf1,
    }


def _befunde(lauf1: dict[str, Any], lauf2: dict[str, Any]) -> None:
    print("=== Befunde ===")
    print()

    # (a)
    if lauf2["ausnahme_a"] is not None:
        print(
            f"(a) widerlegt — Exception statt Degradation: {lauf2['ausnahme_a']}"
        )
    else:
        vor_a = lauf2["status_vor"].get(A, {})
        vor_c = lauf2["status_vor"].get(C, {})
        cl_a = lauf2["classify_vor"].get(A)
        cl_c = lauf2["classify_vor"].get(C)
        degrad_a = (
            cl_a == "pending"
            or "UNRESOLVED_ACCUSED" in vor_a.get("findings", ())
            or "UNKNOWN_ACCUSATION" in vor_a.get("findings", ())
            or vor_a.get("status") != "BINDING"
        )
        degrad_c = (
            cl_c == "pending"
            or "UNRESOLVED_ACCUSED" in vor_c.get("findings", ())
            or "UNKNOWN_ACCUSATION" in vor_c.get("findings", ())
            or vor_c.get("status") != "BINDING"
        )
        konvergenz = (
            lauf2["status_nach"][A] == lauf1["status"][A]
            and lauf2["status_nach"][C] == lauf1["status"][C]
        )
        print(
            f"(a) Umordnung: classify anna={cl_a} chris={cl_c}; "
            f"status anna={vor_a.get('status')} findings={vor_a.get('findings')} "
            f"chris={vor_c.get('status')} findings={vor_c.get('findings')}"
        )
        if degrad_a and degrad_c and konvergenz:
            print(
                "(a) bestätigt — kein Absturz; anna/chris degradieren vor der "
                "Nachlieferung und konvergieren danach auf Lauf 1."
            )
        elif konvergenz and not (degrad_a and degrad_c):
            print(
                "(a) widerlegt — kein Absturz, Nachlieferung konvergiert auf Lauf 1, "
                "aber PENDING / UNRESOLVED_ACCUSED treten nicht ein. "
                "anna bleibt BINDING, weil sie Autorin von acc_a_b ist "
                "(der Claim liegt ohne Zustellung in ihrem inbox). "
                "chris zeigt UNKNOWN_ACCUSATION, nicht UNRESOLVED_ACCUSED "
                "(fehlende Anklage, nicht unaufgelöster Beschuldigter). "
                "classify(verdict_z) ist active, nicht pending "
                "(Vorgänger der Verdikt-Kette wurde in der Baseline an alle zugestellt)."
            )
        else:
            print(
                f"(a) widerlegt — Konvergenz anna/chris auf Lauf 1: {konvergenz}."
            )
    print()

    # (b)
    t1 = lauf1["trust_b"]
    t2 = lauf2["trust_b"]
    t_uhr = lauf2["trust_nach_uhr"]
    anna_wie_lauf1 = _gleich(t2[A], t1[A])
    anna_stabil = _gleich(t2[A], t_uhr[A])
    andere_weichen_ab = all(not _gleich(t2[n], t2[A]) for n in (B, C, Z))
    print(
        f"(b) Dauerverlust: anna nach Widerruf={ {f: t2[A][f] for f in FELDER} } "
        f"Lauf-1={ {f: t1[A][f] for f in FELDER} } "
        f"nach Uhr vor Widerruf={ {f: t_uhr[A][f] for f in FELDER} }"
    )
    if anna_wie_lauf1 and andere_weichen_ab:
        print(
            "(b) bestätigt — anna behält den Vor-Widerruf-Wert aus Lauf 1, "
            "bruno/chris/dora weichen ab, kein Fehler."
        )
    elif anna_stabil and andere_weichen_ab and not anna_wie_lauf1:
        print(
            "(b) widerlegt — anna zeigt nicht den Vor-Widerruf-Wert aus Lauf 1. "
            "Annas trust bleibt nach dem Widerruf gleich dem Wert nach Uhrendrift "
            "(d/C unerreichbar) und weicht von bruno/chris/dora ab; kein Fehler. "
            "Ursache: (c) setzt annas now über T_EXP vor der Messung, "
            "alle Baseline-Vouches sind für anna expired."
        )
    else:
        print(
            f"(b) widerlegt — anna_wie_lauf1={anna_wie_lauf1}, "
            f"anna_stabil={anna_stabil}, andere_weichen_ab={andere_weichen_ab}."
        )
    print()

    # (c)
    cl = lauf2["classify_vouch"]
    nur_anna = cl[A] == "expired" and all(cl[n] != "expired" for n in (B, C, Z))
    print(f"(c) Uhrendrift classify(vouch_c_b): {dict(cl)}")
    if nur_anna:
        print("(c) bestätigt — nur anna zeigt expired.")
    else:
        print("(c) widerlegt — expired nicht allein bei anna.")


def main() -> None:
    print("Szenario D — Rechenschaft unter Partition (D336)")
    print("A=anna  B=bruno  Z=dora  C=chris")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        lauf1 = _lauf1(str(Path(tmp) / "lauf1"))
        lauf2 = _lauf2(str(Path(tmp) / "lauf2"), lauf1)
    _befunde(lauf1, lauf2)


if __name__ == "__main__":
    main()
