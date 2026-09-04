#!/usr/bin/env python3
"""Szenario Absicherung, Stufe A (00an-szenario-a-prompt.md, D311).

Wegwerf-Prototyp. Keine Golden Numbers. Jede Stelle, an der die Spec keine
Antwort hat, ist ein Befund — im Bericht, nicht als stiller Default.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import Claim, claim_id, signed_bytes
from mensch_als_republik.domains import DOM_NUC_GEN
from mensch_als_republik.governance import Epoch
from mensch_als_republik.policy import NucleusPolicy, constitution_hash
from mensch_als_republik.predicates import is_nuc_name
from mensch_als_republik.profiles import (
    MembershipState,
    SettlementState,
    membership,
    resolve_policy,
    settlement,
)
from mensch_als_republik.verifier import InMemoryStore, read_claim
from tools.autor import Autor, DateiRueckhalt

NOW = 10_000

# SZENARIO, nicht Protokoll (03 §3.1). Das Protokoll liest amount nie.
SZENARIO_BEITRAG = 10
SZENARIO_AUSZAHLUNG = 40
SZENARIO_UMLAGE = 20
SZENARIO_UNIT_REF = hashlib.sha256(b"szenario-a/unit-ref").digest()

NAMEN = ("anna", "bruno", "chris", "dora")
SEEDS = {
    "anna": bytes([0x11] * 32),
    "bruno": bytes([0x12] * 32),
    "chris": bytes([0x13] * 32),
    "dora": bytes([0x14] * 32),
}

# BRUNO ist Verwahrer, weil jemand es sein muss — das Protokoll hat keine
# Verwahrer-Rolle (D311 Befund 1). Die Wahl ist Szenario.
VERWAHRER = "bruno"
BETROFFENE = "anna"
BEITRAGENDE = ("anna", "chris", "dora")
UMLAGE_LEISTENDE = ("bruno", "chris", "dora")
UMLAGE_OHNE_QUITTUNG = "chris"


def _nuc(scope: bytes, name: str) -> str:
    return f"nuc:{scope.hex()}/{name}@1"


def _hex(value: bytes) -> str:
    return value.hex()


def _ist_claimdatei(name: str) -> bool:
    return len(name) == 64 and all(c in "0123456789abcdef" for c in name)


class DateiAusgang:
    """Legt jeden ausgesendeten Claim als Datei ab (D311 Befund 3).

    Dateiname = claim_id in Hex. Liegt im selben Verzeichnis wie der
    DateiRueckhalt — die Spec sagt den Ort nicht; ein zweites Verzeichnis
    waere eine weitere unbelegte Wahl.
    """

    def __init__(self, pfad: Path) -> None:
        self._pfad = pfad

    def kennt(self, cid: bytes) -> bool:
        path = self._pfad / cid.hex()
        if not path.is_file():
            return False
        result = read_claim(path.read_bytes())
        return isinstance(result, Claim) and claim_id(result) == cid

    def aufnehmen(self, claim: Claim) -> None:
        cid = claim_id(claim)
        (self._pfad / cid.hex()).write_bytes(signed_bytes(claim))


def verzeichnis_laden(pfad: Path) -> InMemoryStore:
    """Liest ein Verzeichnis in einen InMemoryStore (D311 Befund 3, D131).

    Ueberspringt spitze/redo und jede Datei, die read_claim nicht als Claim
    nimmt. Dateiname muss der claim_id in Hex gleichen — Konvention des
    Szenarios, nicht der Spec.
    """
    store = InMemoryStore()
    if not pfad.is_dir():
        return store
    for path in sorted(pfad.iterdir()):
        if not path.is_file() or not _ist_claimdatei(path.name):
            continue
        result = read_claim(path.read_bytes())
        if not isinstance(result, Claim):
            continue
        if claim_id(result).hex() != path.name:
            continue
        store.add(result)
    return store


def claims_verteilen(
    claims: list[Claim],
    quelle: Path,
    ziele: list[Path],
) -> int:
    """Kopiert eine Menge von Claims in fremde Verzeichnisse (D311 Befund 3).

    Wer was weiss, ist danach die Menge der Claim-Dateien je Verzeichnis.
    """
    kopiert = 0
    for claim in claims:
        name = claim_id(claim).hex()
        src = quelle / name
        data = src.read_bytes()
        for ziel in ziele:
            if ziel.resolve() == quelle.resolve():
                continue
            dest = ziel / name
            if dest.exists():
                continue
            dest.write_bytes(data)
            kopiert += 1
    return kopiert


class Beteiligter:
    """Ein Beobachter: Autor mit DateiRueckhalt und DateiAusgang auf dasselbe Verzeichnis."""

    def __init__(self, name: str, pfad: Path, seed: bytes) -> None:
        pfad.mkdir(parents=True, exist_ok=True)
        self.name = name
        self.pfad = pfad
        self.autor = Autor(seed, DateiRueckhalt(pfad), DateiAusgang(pfad))
        self.pub = self.autor.pub
        self._t = 0
        self.autor.wiederaufnehmen()

    def signieren(
        self,
        *,
        p: str,
        J: tuple[int, bytes],
        v: bytes | None = None,
        N: bytes | None = None,
    ) -> Claim:
        self._t += 1
        return self.autor.signieren(p=p, J=J, t=self._t, v=v, N=N)


@dataclass
class Welt:
    """Vier Beteiligte, ein Nukleus, beschriftete Claims."""

    basis: Path
    beteiligte: dict[str, Beteiligter]
    constitution: dict
    genesis: dict
    constitution_hash: bytes
    N: bytes
    epoch_1: Epoch
    policy: NucleusPolicy
    labels: dict[str, Claim] = field(default_factory=dict)
    by_pub: dict[bytes, str] = field(default_factory=dict)


def _obligation_v(amount: int) -> bytes:
    """CBOR fuer obligation.v. amount und unit_ref sind SZENARIO (03 §3.1)."""
    return cbor_canon.encode({0: amount, 1: SZENARIO_UNIT_REF})


def _name_von(welt: Welt, pub: bytes) -> str:
    return welt.by_pub.get(pub, pub.hex()[:8])


def build(basis: Path) -> Welt:
    """Nukleus, vier Verzeichnisse, Genesis, Epoche 1, accept-rules (Prompt Aufbau)."""
    if basis.exists():
        shutil.rmtree(basis)
    basis.mkdir(parents=True, exist_ok=True)

    beteiligte = {name: Beteiligter(name, basis / name, SEEDS[name]) for name in NAMEN}
    pubs_sorted = sorted(b.pub for b in beteiligte.values())
    by_pub = {b.pub: name for name, b in beteiligte.items()}

    # Schwellen aus 00 §3.1, ungenutzt in diesem Lauf: es wird nicht abgestimmt.
    constitution = {
        "irrevocable_predicates": ["obligation@1"],
        "thresholds": {
            "ordinary": [1, 2],
            "membership": [2, 3],
            "amendment": [3, 4],
        },
        "arbitration": {"arbitrators": pubs_sorted},
        "participants": pubs_sorted,
    }
    ch = constitution_hash(constitution)
    genesis = {
        0: 1,
        1: pubs_sorted,
        2: 0,
        3: pubs_sorted,
        4: ch,
        5: 2,
        6: 0,
        7: 0,
    }
    N = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    epoch_1 = Epoch(scope=N, index=1, constitution_hash=ch)
    resolved = resolve_policy(
        scope=N,
        genesis_obj=genesis,
        constitution_hash=ch,
        constitution_obj=constitution,
    )
    if resolved.findings != ():
        raise AssertionError(f"resolve_policy findings: {resolved.findings!r}")

    welt = Welt(
        basis=basis,
        beteiligte=beteiligte,
        constitution=constitution,
        genesis=genesis,
        constitution_hash=ch,
        N=N,
        epoch_1=epoch_1,
        policy=resolved.policy,
        by_pub=by_pub,
    )

    akzeptiert: list[Claim] = []
    for name in NAMEN:
        claim = beteiligte[name].signieren(
            p=_nuc(N, "accept-rules"),
            J=(3, ch),
            N=N,
        )
        welt.labels[f"accept-{name}"] = claim
        akzeptiert.append(claim)
        _an_alle(welt, [claim], von=name)

    return welt


def _an_alle(welt: Welt, claims: list[Claim], *, von: str) -> None:
    quelle = welt.beteiligte[von].pfad
    ziele = [b.pfad for b in welt.beteiligte.values()]
    claims_verteilen(claims, quelle, ziele)


def _obligation(
    welt: Welt,
    *,
    schuldner: str,
    glaeubiger: str,
    amount: int,
    label: str,
) -> Claim:
    claim = welt.beteiligte[schuldner].signieren(
        p=_nuc(welt.N, "obligation"),
        J=(1, welt.beteiligte[glaeubiger].pub),
        v=_obligation_v(amount),
        N=welt.N,
    )
    welt.labels[label] = claim
    _an_alle(welt, [claim], von=schuldner)
    return claim


def _receipt(welt: Welt, *, glaeubiger: str, obligation: Claim, label: str) -> Claim:
    claim = welt.beteiligte[glaeubiger].signieren(
        p=_nuc(welt.N, "receipt"),
        J=(2, claim_id(obligation)),
        N=welt.N,
    )
    welt.labels[label] = claim
    _an_alle(welt, [claim], von=glaeubiger)
    return claim


def phase1_mit_quittung(welt: Welt) -> None:
    """Fonds: drei Perioden Beitraege, quittiert; Auszahlung quittiert.

    Der Fall selbst ist kein Claim. accusation waere Stufe C (Prompt Nicht-Ziele).
    Die Auszahlung ist die Obligation des Verwahrers — keine Abstimmung
    (D311 Befund 2, Weg B).
    """
    for periode in (1, 2, 3):
        for name in BEITRAGENDE:
            label = f"beitrag-a-{periode}-{name}"
            o = _obligation(
                welt,
                schuldner=name,
                glaeubiger=VERWAHRER,
                amount=SZENARIO_BEITRAG,
                label=label,
            )
            _receipt(
                welt,
                glaeubiger=VERWAHRER,
                obligation=o,
                label=f"quittung-a-{periode}-{name}",
            )
    # ANNA meldet den Fall. Es gibt kein Prädikat dafuer.
    o = _obligation(
        welt,
        schuldner=VERWAHRER,
        glaeubiger=BETROFFENE,
        amount=SZENARIO_AUSZAHLUNG,
        label="auszahlung-a",
    )
    _receipt(
        welt,
        glaeubiger=BETROFFENE,
        obligation=o,
        label="quittung-auszahlung-a",
    )


def phase1_ohne_quittung(welt: Welt) -> None:
    """Dieselbe Phase noch einmal: Verwahrer quittiert nicht und zahlt nicht aus."""
    for periode in (1, 2, 3):
        for name in BEITRAGENDE:
            _obligation(
                welt,
                schuldner=name,
                glaeubiger=VERWAHRER,
                amount=SZENARIO_BEITRAG,
                label=f"beitrag-b-{periode}-{name}",
            )
    # Fall gemeldet, keine Auszahlungs-Obligation.


def phase2_umlage(welt: Welt) -> None:
    """Umlage ohne Verwahrer. Einer der drei wird nicht quittiert."""
    for name in UMLAGE_LEISTENDE:
        o = _obligation(
            welt,
            schuldner=name,
            glaeubiger=BETROFFENE,
            amount=SZENARIO_UMLAGE,
            label=f"umlage-{name}",
        )
        if name != UMLAGE_OHNE_QUITTUNG:
            _receipt(
                welt,
                glaeubiger=BETROFFENE,
                obligation=o,
                label=f"quittung-umlage-{name}",
            )


@dataclass(frozen=True, slots=True)
class Zeile:
    beobachter: str
    label: str
    state: str
    schuldner: str
    glaeubiger: str
    fehlgrund: str | None


def _obligation_labels(welt: Welt, prefixes: tuple[str, ...]) -> list[str]:
    out: list[str] = []
    for label, claim in welt.labels.items():
        if not any(label.startswith(p) for p in prefixes):
            continue
        if is_nuc_name(claim, "obligation"):
            out.append(label)
    return sorted(out)


def check_tilgung(welt: Welt, labels: list[str]) -> list[Zeile]:
    """Tilgungszustand jeder Obligation aus jedem Verzeichnis (03 §3.3.2)."""
    zeilen: list[Zeile] = []
    for name, beteiligter in welt.beteiligte.items():
        store = verzeichnis_laden(beteiligter.pfad)
        for label in labels:
            o = welt.labels[label]
            o_cid = claim_id(o)
            if store.get(o_cid) is None:
                zeilen.append(
                    Zeile(
                        beobachter=name,
                        label=label,
                        state="FEHLT",
                        schuldner=_name_von(welt, o.I),
                        glaeubiger=_name_von(welt, o.J[1]) if o.J[0] == 1 else "?",
                        fehlgrund=f"obligation {o_cid.hex()[:12]} nicht im Verzeichnis",
                    )
                )
                continue
            result = settlement(
                store,
                obligation=o,
                scope=welt.N,
                now=NOW,
                policy=welt.policy,
            )
            zeilen.append(
                Zeile(
                    beobachter=name,
                    label=label,
                    state=result.state.value,
                    schuldner=_name_von(welt, o.I),
                    glaeubiger=_name_von(welt, o.J[1]) if o.J[0] == 1 else "?",
                    fehlgrund=None,
                )
            )
    return zeilen


def check_offen(zeilen: list[Zeile]) -> list[Zeile]:
    """Offene Obligationen und wem gegenueber, je Beobachter."""
    return [z for z in zeilen if z.state == SettlementState.OPEN.value]


def check_uebereinstimmung(zeilen: list[Zeile]) -> tuple[bool, list[str]]:
    """Ob alle vier zum selben Ergebnis kommen; sonst welcher Claim fehlt bei wem."""
    by_label: dict[str, list[Zeile]] = {}
    for z in zeilen:
        by_label.setdefault(z.label, []).append(z)
    abweichungen: list[str] = []
    for label, gruppe in sorted(by_label.items()):
        zustaende = {z.state for z in gruppe}
        if len(zustaende) == 1 and "FEHLT" not in zustaende:
            continue
        if len(zustaende) == 1 and zustaende == {"FEHLT"}:
            abweichungen.append(
                f"{label}: bei allen vier FEHLT — Verteilung, nicht Protokoll"
            )
            continue
        fehlend = [z.beobachter for z in gruppe if z.state == "FEHLT"]
        andere = sorted({z.state for z in gruppe if z.state != "FEHLT"})
        if fehlend:
            abweichungen.append(
                f"{label}: fehlt bei {','.join(fehlend)}; "
                f"uebrige {andere} — Verteilung, nicht Protokoll"
            )
        else:
            abweichungen.append(
                f"{label}: Zustaende {sorted(zustaende)} — Protokoll oder "
                "ungleich verteilte Quittung"
            )
    return (len(abweichungen) == 0, abweichungen)


def check_mitgliedschaft(welt: Welt) -> dict[str, str]:
    """accept-rules der vier, je aus dem eigenen Verzeichnis."""
    lagen: dict[str, str] = {}
    keys = frozenset(welt.genesis[1])
    for name, beteiligter in welt.beteiligte.items():
        store = verzeichnis_laden(beteiligter.pfad)
        result = membership(
            store,
            subject=beteiligter.pub,
            scope=welt.N,
            constitution_hash=welt.constitution_hash,
            now=NOW,
            authorized_keys=keys,
            constitution_obj=welt.constitution,
            policy=welt.policy,
        )
        lagen[name] = result.state.value
    return lagen


def check_phase1_quittung(welt: Welt) -> list[Zeile]:
    labels = _obligation_labels(welt, ("beitrag-a-", "auszahlung-a"))
    zeilen = check_tilgung(welt, labels)
    for z in zeilen:
        if z.state != SettlementState.SETTLED.value:
            raise AssertionError(
                f"phase1 mit Quittung: {z.label} bei {z.beobachter} ist {z.state}"
            )
    ok, abweichungen = check_uebereinstimmung(zeilen)
    if not ok:
        raise AssertionError(f"phase1 mit Quittung uneins: {abweichungen}")
    return zeilen


def check_phase1_ohne(welt: Welt) -> list[Zeile]:
    labels = _obligation_labels(welt, ("beitrag-b-",))
    zeilen = check_tilgung(welt, labels)
    for z in zeilen:
        if z.state != SettlementState.OPEN.value:
            raise AssertionError(
                f"phase1 ohne Quittung: {z.label} bei {z.beobachter} ist {z.state}"
            )
    if "auszahlung-b" in welt.labels:
        raise AssertionError("ohne Auszahlung wurde trotzdem eine Obligation erzeugt")
    ok, abweichungen = check_uebereinstimmung(zeilen)
    if not ok:
        raise AssertionError(f"phase1 ohne Quittung uneins: {abweichungen}")
    return zeilen


def check_phase2(welt: Welt) -> list[Zeile]:
    labels = _obligation_labels(welt, ("umlage-",))
    zeilen = check_tilgung(welt, labels)
    for z in zeilen:
        if z.label.endswith(UMLAGE_OHNE_QUITTUNG):
            erwartet = SettlementState.OPEN.value
        else:
            erwartet = SettlementState.SETTLED.value
        if z.state != erwartet:
            raise AssertionError(
                f"phase2: {z.label} bei {z.beobachter} ist {z.state}, erwartet {erwartet}"
            )
    ok, abweichungen = check_uebereinstimmung(zeilen)
    if not ok:
        raise AssertionError(f"phase2 uneins: {abweichungen}")
    return zeilen


def check_wiederlesen(welt: Welt, zuvor: list[Zeile]) -> None:
    """Dieselbe Welt aus frisch gelesenen Verzeichnissen, dasselbe Ergebnis."""
    labels = sorted({z.label for z in zuvor})
    nochmal = check_tilgung(welt, labels)
    a = {(z.beobachter, z.label, z.state) for z in zuvor}
    b = {(z.beobachter, z.label, z.state) for z in nochmal}
    if a != b:
        raise AssertionError(f"Wiederlesen weicht ab: {sorted(a ^ b)}")


def _wissen(welt: Welt) -> dict[str, int]:
    counts: dict[str, int] = {}
    for name, beteiligter in welt.beteiligte.items():
        n = 0
        for path in beteiligter.pfad.iterdir():
            if path.is_file() and _ist_claimdatei(path.name):
                n += 1
        counts[name] = n
    return counts


def _print_identitaet(welt: Welt) -> None:
    rows = [(name.upper(), welt.beteiligte[name].pub) for name in NAMEN]
    rows.append(("constitution_hash", welt.constitution_hash))
    rows.append(("N", welt.N))
    rows.append(("epoch_id_1", welt.epoch_1.epoch_id))
    width = max(len(n) for n, _ in rows)
    for name, value in rows:
        print(f"{name:<{width}}  {value.hex()}")


def _print_tilgung(titel: str, zeilen: list[Zeile]) -> None:
    print()
    print(titel)
    by_label: dict[str, list[Zeile]] = {}
    for z in zeilen:
        by_label.setdefault(z.label, []).append(z)
    print(f"{'obligation':<28}  {'schuldner':<8}  {'glaeubiger':<10}  zustand")
    for label, gruppe in by_label.items():
        z = gruppe[0]
        zustaende = {g.state for g in gruppe}
        zustand = z.state if len(zustaende) == 1 else ",".join(sorted(zustaende))
        print(f"{label:<28}  {z.schuldner:<8}  {z.glaeubiger:<10}  {zustand}")
    offen = check_offen(zeilen)
    print("offen:")
    if not offen:
        print("  (keine)")
    else:
        gesehen: set[tuple[str, str, str]] = set()
        for z in offen:
            key = (z.label, z.schuldner, z.glaeubiger)
            if key in gesehen:
                continue
            gesehen.add(key)
            print(f"  {z.schuldner} -> {z.glaeubiger}  ({z.label})")
    ok, abweichungen = check_uebereinstimmung(zeilen)
    print(f"alle vier gleich: {'ja' if ok else 'nein'}")
    for a in abweichungen:
        print(f"  {a}")


def _print_szenario_summen() -> None:
    n_beitraege = 3 * len(BEITRAGENDE)
    print()
    print("SZENARIO-Summen (03 §3.1: nicht das Protokoll)")
    print(
        f"  phase1 Beitraege  {n_beitraege} x {SZENARIO_BEITRAG} = "
        f"{n_beitraege * SZENARIO_BEITRAG}"
    )
    print(f"  phase1 Auszahlung {SZENARIO_AUSZAHLUNG}")
    print(
        f"  phase2 Umlage     {len(UMLAGE_LEISTENDE)} x {SZENARIO_UMLAGE} = "
        f"{len(UMLAGE_LEISTENDE) * SZENARIO_UMLAGE}"
    )
    print(
        f"  phase2 quittiert  {len(UMLAGE_LEISTENDE) - 1} x {SZENARIO_UMLAGE} = "
        f"{(len(UMLAGE_LEISTENDE) - 1) * SZENARIO_UMLAGE}"
    )


def verify_all(basis: Path) -> tuple[Welt, list[Zeile], list[Zeile], list[Zeile]]:
    welt = build(basis)
    lagen = check_mitgliedschaft(welt)
    for name, state in lagen.items():
        if state != MembershipState.MEMBER.value:
            raise AssertionError(f"Aufbau: {name} ist {state}, nicht MEMBER")
    phase1_mit_quittung(welt)
    z1 = check_phase1_quittung(welt)
    phase1_ohne_quittung(welt)
    z1b = check_phase1_ohne(welt)
    phase2_umlage(welt)
    z2 = check_phase2(welt)
    check_wiederlesen(welt, z1 + z1b + z2)
    return welt, z1, z1b, z2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "basis",
        nargs="?",
        default="/tmp/szenario-absicherung",
        help="Basispfad der vier Verzeichnisse (Voreinstellung unter /tmp)",
    )
    args = parser.parse_args()
    basis = Path(args.basis)
    try:
        welt, z1, z1b, z2 = verify_all(basis)
    except AssertionError as exc:
        print(f"szenario-absicherung: {exc}", file=sys.stderr)
        return 1

    print("weg: Beobachtung der Obligationen (D311 Befund 2, Weg B)")
    print("verworfen: Auszahlung als Verfassungsänderung — 04 §2.4 kennt nur")
    print("  (scope, Vorgaengerepoche, constitution_hash). Ein Sachverhalt hat")
    print("  darin keinen Platz, und settlement liest keine Verfassung.")
    print()
    _print_identitaet(welt)
    wissen = _wissen(welt)
    print()
    print("wissen (Claim-Dateien je Verzeichnis)")
    print("  " + "  ".join(f"{n}={wissen[n]}" for n in NAMEN))

    _print_tilgung("phase 1 — Fonds, quittiert und ausgezahlt", z1)
    print("  Protokoll sagt: jede Beitragspflicht SETTLED, Auszahlung SETTLED.")
    print("  Protokoll sagt nicht: ob der Topf gedeckt war, ob 40 aus 90 folgt,")
    print("  ob ein Fall vorlag, ob der Verwahrer haette zahlen muessen.")

    _print_tilgung("phase 1 — nochmals, ohne Quittung und ohne Auszahlung", z1b)
    print("  Protokoll sagt: neun Obligationen OPEN an den Verwahrer.")
    print("  Protokoll sagt nicht: Verweigerung, Unterschlagung, Anspruch,")
    print("  Deckung. OPEN ist ununterscheidbar von 'Quittung noch nicht da'.")

    _print_tilgung("phase 2 — Umlage ohne Verwahrer", z2)
    print("  Protokoll sagt: zwei SETTLED, eine OPEN (chris -> anna).")
    print("  Protokoll sagt nicht: ob die Umlage reicht, ob chris leisten")
    print("  muesste, ob der Fall berechtigt war. Kein Gruppen-Soll.")

    print()
    print("wiederlesen: gleiches Ergebnis")
    _print_szenario_summen()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
