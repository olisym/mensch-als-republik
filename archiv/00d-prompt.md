# 00d — Die Epochenkette

## Branch und Basis

Branch `00d-epochenkette`, abgezweigt von `main`. Der Basis-Commit ist
`git merge-base main 00d-epochenkette`. Ein Commit am Ende, kein Merge, kein Push.

## Normative Grundlage

- `04-governance.md §4.5` — die Kette. Der Abschnitt ist die Vorgabe; er ist vollständig zu lesen.
- `04-governance.md §3.5` — die Asymmetrie zwischen Aufruferfehler und Weltzustand.
- `04-governance.md §4.1` bis `§4.4` — Prüfung eines Übergangs, Folgeepoche, ein Ja je Epoche.
- `07-decisions.md` D174, D175, D176.
- `00-nucleus-genesis-constitution.md §6.4` — die Rotationskette, gegen die `§4.5` abgegrenzt wird.

## Auftrag A — `mensch_als_republik/governance/chain.py`

Neue Datei mit `EpochResolution` und `resolve_epoch`.

```
@dataclass(frozen=True, slots=True)
class EpochResolution:
    epoch: Epoch
    constitution_obj: dict | None
    findings: tuple[Finding, ...]


def resolve_epoch(
    store: ClaimStore,
    *,
    scope: bytes,
    genesis_obj: dict,
    known_constitutions: Mapping[bytes, dict],
    known_proposals: Mapping[bytes, Proposal],
    now: int,
) -> EpochResolution:
```

**Start.** Epoche 1 nach `04 §1.1`: `index = 1`, `constitution_hash = genesis_obj[4]`, `N = scope`.
Weicht `scope` von `SHA256(DOM_NUC_GEN || cbor(genesis_obj))` ab, ist das ein Aufruferfehler und
MUSS `ValueError` werfen. Das ist dieselbe Prüfung, die `resolve_policy` bereits führt.

**Schritt.** Zu einer Epoche `i`:

1. Alle Claims im Speicher finden, die `ratify@1` im Scope `scope` sind.
2. Je Claim das Vorschlagsobjekt zu `claim.J[1]` aus `known_proposals` holen. Fehlt es oder passt
   es nicht auf seinen Schlüssel, ist der Vorschlag unbekannt: Vermerk
   `EPOCH_PROPOSAL_UNAVAILABLE` mit `claim.J[1]` als Subjekt, und der Claim trägt nicht.
3. Vorschläge, deren `predecessor` nicht `i.epoch_id` ist, gehören nicht zu dieser Epoche und
   werden übergangen — ohne Vermerk.
4. Je verbleibendem Vorschlag `decide` laufen lassen, dann `verify_ratification` mit dem Claim.
5. Trägt genau eine Ratifizierung, ist `i+1` erreicht; weiter bei 1.
   Trägt keine, endet die Kette bei `i`.
   Tragen zwei auf **verschiedene** Nachfolger, siehe unten.

**Beschaffung.** Jeder Zugriff auf `known_constitutions` und `known_proposals` prüft den Wert
gegen den Schlüssel: `constitution_hash(obj) == h` beziehungsweise `value.proposal_hash == h`.
Passt es nicht, gilt der Eintrag als **unbekannt** und läuft in den Zweig, den ein fehlender
Eintrag nimmt. Kein `ValueError` — der Aufrufer kontrolliert den Inhalt fremder Objekte nicht.

**Policy.** Je Epoche aus deren Verfassung über `resolve_policy`. Ist das Verfassungsobjekt
unbekannt, wird `constitution_obj=None` übergeben; `resolve_policy` liefert dann die
Sicherheits-Default-Policy. Ein bekanntes Objekt wird **vorher** gegen den Hash geprüft, damit
`resolve_policy` nicht in seinen `ValueError` läuft.

**Vermerke.** `EpochResolution.findings` enthält ausschließlich `governance.Finding`:

- die Vermerke aus `verify_ratification` für Ratifizierungen, die auf die **erreichte** Epoche
  zeigen und nicht tragen,
- `EPOCH_PROPOSAL_UNAVAILABLE` für unbekannte Vorschlagsobjekte an der erreichten Epoche,
- `EPOCH_FORK`, falls der unmögliche Fall doch eintritt.

Nicht enthalten: Vermerke aus `decide`, Vermerke aus `resolve_policy` (das ist ein anderer
`Finding`-Typ mit `ProfileFinding`), und Vermerke zu Epochen, die die Kette bereits verlassen hat.
Das Ergebnis wird mit `dedupe_sort` normiert.

**Ist die Verfassung der erreichten Epoche unbekannt**, bleibt `constitution_obj` leer. Dafür
entsteht **kein** Vermerk.

**Zwei tragende Ratifizierungen auf verschiedene Nachfolger.** Kein Kopf ab `i`; `epoch` ist `i`,
und je Nachfolger ein `EPOCH_FORK` mit dessen `epoch_id` als Subjekt. Nach `04 §4.4` ist der Fall
unerreichbar. Er ist zu implementieren und **nicht** zu testen.

**Zwei neue Werte in `GovernanceFinding`:** `EPOCH_PROPOSAL_UNAVAILABLE` und `EPOCH_FORK`.
`resolve_epoch` und `EpochResolution` werden aus `governance/__init__.py` exportiert.

## Auftrag B — `known_proposals` in `decide` prüfen (D175)

`decide` liest heute `known_proposals[other.J[1]]`, ohne den Wert gegen den Schlüssel zu prüfen.
Die drei anderen Objektquellen derselben Funktion — `genesis_obj`, `constitution_obj`,
`target_constitution_obj` — werden geprüft. Nachziehen: passt `proposal_hash` des Werts nicht auf
den Schlüssel, gilt der Vorschlag als unbekannt und läuft in den bestehenden
`UNKNOWN_PROPOSAL`-Zweig. Kein neuer Vermerkstyp, kein `ValueError`, kein geänderter Rückgabetyp.

## Nicht-Ziele

- **Keine Zyklusprüfung** in `resolve_epoch`. Die Terminierung folgt aus `04 §4.5`: jeder Claim
  trägt höchstens einen Übergang, und jede Epoche der Kette ist verschieden. Eine `visited`-Menge
  wie in `_head_from` (`keys.py`) ist ausdrücklich unerwünscht; die Rotationskette dort ist
  autorverkettet, diese nicht.
- **Kein `policy`-Parameter** an `resolve_epoch`.
- **Kein Test auf `EPOCH_FORK`.**
- **Keine Änderung** an `epoch.py`, `objects.py`, `keys.py`, `profiles/`, `03-profiles.md` oder
  `04-governance.md`. Die Spec steht bereits.
- **Kein Anschluss** von `resolve_epoch` an `membership`, `resolve_authorized_keys` oder
  `tools/example_nucleus.py`. Das ist ein eigener Lauf.
- **Kein neues Protocol** für die Objektbeschaffung. `Mapping` genügt.
- Was hier nicht steht, wird **gemeldet, nicht gebaut**.

## Abnahmekriterien

Neue Tests in `tests/governance/test_chain.py`. Alle Werte stammen aus
`tests/governance/fixtures.py` und `tests/helpers.py`; **keine getippten Hashes**.

1. **Die Kette läuft zwei Übergänge.** Ein Speicher mit den Ja-Stimmen aller Teilnehmer von `C1`
   auf `PROPOSAL_1` samt Ratifizierung, dazu den Ja-Stimmen aller Teilnehmer von `C2` auf
   `PROPOSAL_2` samt Ratifizierung. `known_constitutions` enthält `C1`, `C2`, `C3` unter ihren
   Hashes, `known_proposals` beide Vorschläge. Erwartung:
   `result.epoch.epoch_id == EPOCH_3.epoch_id` und `result.constitution_obj == C3`.
   Der Aufbau des ersten Übergangs steht in `test_vectors.py::test_GV_1` und ist dort belegt.
2. **Ohne Ratifizierung bleibt die Kette bei Epoche 1**, `constitution_obj == C1`, `findings`
   leer.
3. **Fehlt `C3` in `known_constitutions`**, endet die Kette dennoch bei `EPOCH_3.epoch_id`, und
   `constitution_obj` ist leer. Kein Vermerk dafür.
4. **Fehlt `PROPOSAL_2` in `known_proposals`**, endet die Kette bei `EPOCH_2.epoch_id` mit genau
   einem `EPOCH_PROPOSAL_UNAVAILABLE`, dessen Subjekt `PROPOSAL_2.proposal_hash` ist.
5. **Ein falsch geschlüsselter Eintrag** in `known_constitutions` — `C3` unter dem Hash von `C2`
   abgelegt — verhält sich wie ein fehlender: die Kette erreicht `EPOCH_3.epoch_id`,
   `constitution_obj` ist leer, und es wird nichts aus `C3` gelesen.
6. **Ein falscher `scope`** wirft `ValueError`.
7. **Vermerke einer überholten Epoche erscheinen nicht.** Eine nicht tragende Ratifizierung an
   Epoche 1, zusätzlich zur tragenden, hinterlässt im Ergebnis keinen Vermerk.
8. **Auftrag B:** ein Vektor in `tests/governance/`, in dem `known_proposals` einen Hash auf ein
   `Proposal` mit falschem `predecessor` abbildet. Erwartung: `CONFLICTING_APPROVAL` bleibt
   bestehen, weil der Eintrag als unbekannt gilt und `UNKNOWN_PROPOSAL` greift.
9. `make check` ist grün. Die Testzahl steigt; der alte Bestand von 544 bleibt vollständig grün.

## Rücknahmeproben

Zwei Änderungen, zwei Proben. Beide werden ausgeführt, das Ergebnis wird berichtet, und der
Zustand wird danach wiederhergestellt.

- **Probe 1 (Auftrag B).** Die neue Schlüsselprüfung in `decide` entfernen. Erwartung: der Test
  aus Kriterium 8 wird rot. Bleibt er grün, prüft er die Reparatur nicht und ist wertlos.
- **Probe 2 (Auftrag A).** Die Schlüsselprüfung für `known_constitutions` in `chain.py` entfernen.
  Erwartung: der Test aus Kriterium 5 wird rot.

Widerspricht eine Messung diesem Prompt, ist das zu **melden, nicht anzupassen**. Keine erwarteten
Werte nachziehen, um einen Test grün zu bekommen.

## Abschluss

Ein Commit auf `00d-epochenkette`. `git add` mit expliziten Pfaden. Kein Merge, kein Push.
Der Bericht nennt: geänderte Dateien mit `git diff --numstat`, die neue Testzahl, das Ergebnis
beider Rücknahmeproben, und jede Stelle, an der der Prompt nicht ausgereicht hat.
