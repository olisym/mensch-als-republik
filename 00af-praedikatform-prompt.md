# Prompt 00af — `INVALID_PREDICATE` (D267)

## Branch und Basis

Branch `lauf/00af-praedikatform`, Basis-Commit `52bb5bd`. Ein einziger Commit am Ende. Kein
Merge, kein Push, kein Rebase.

## Normative Grundlage

- **D267** im Register: zwölfter Reject-Code für Formverstöße unter `nuc:`.
- `01 §B.2` — die Tabelle trägt seit D267 zwölf Zeilen; `INVALID_PREDICATE` steht zwischen
  `UNKNOWN_NAMESPACE` und `BAD_SCOPE_BINDING`.
- `01 §6` Punkt 4 — die Reihenfolge der Prüfungen für `p` ist dort **keine** Folge, sondern eine
  Konjunktion (D262, D265). Der Code hängt am Befund, nicht am Schritt.
- `01 §2.2` und Anhang A von `01-claim-atom.md` — die Grammatik ist normativ; der Prädikat-Name
  ist bedeutungs-opak, nicht form-frei.
- **D250** — ein Anhangsabschnitt wird angehängt, nicht eingeschoben.
- **D265** — eine Prüfreihenfolge wird nicht normiert und auch nicht implizit gebaut.

## Auftrag

### Schritt 1 — `mensch_als_republik/errors.py`

Ein zwölfter Code `INVALID_PREDICATE` in `ErrorCode` und eine Klasse
`InvalidPredicate(VerifierError)` mit diesem Code. Beide stehen unmittelbar hinter
`UNKNOWN_NAMESPACE` beziehungsweise hinter der Klasse `UnknownNamespace`; das ist die
Reihenfolge aus `01 §B.2`.

### Schritt 2 — `mensch_als_republik/predicates.py`

In `parse_predicate` werfen die beiden `raise` **innerhalb** des `nuc:`-Zweigs künftig
`InvalidPredicate` statt `UnknownNamespace`. Das abschließende `raise` am Funktionsende — der
Fall ohne `core/`- und ohne `nuc:`-Präfix — bleibt unverändert `UnknownNamespace`.

Die Regexe im Modulkopf werden **nicht** angefasst. Es ändert sich nur, welche Ausnahme geworfen
wird.

### Schritt 3 — Vektor NV13 in `tests/vectors/gen.py`

Ein weiterer negativer Vektor, gebaut wie seine Nachbarn über `Claim` und `_finalize`, mit dieser
Welt Feld für Feld:

- `version` = 1
- `I` = `ALICE_PUB`
- `J` = `(1, BOB_PUB)`
- `p` = `"nuc:" + N.hex() + "/VOUCH@1"` — kanonischer Scope, Großbuchstaben im Namen
- `v` = `V_VOUCH`
- `N` = `N`
- `t` = `1_700_000_411`
- `h_prev` = `h_gen_alice`
- signiert mit `alice_sk`

Der Eintrag lautet `_vec("NV13", nv13, expect_reject="INVALID_PREDICATE")` und steht unmittelbar
hinter dem von NV12. Danach `tests/vectors/vectors_01.json` neu erzeugen.

NV13 trägt **genau einen** Mangel: Scope und `N` stimmen überein, die Signatur ist gültig, der
Anker ist der Genesis-Anker von ALICE, `t_exp` fehlt.

### Schritt 4 — Anhang C.12 in `01-claim-atom.md`

Ein neuer Abschnitt `### C.12 NV13 — Formverstoß unter nuc:`, **angehängt** hinter C.11 und vor
der Änderungshistorie. Aufbau, Wortwahl und Zeilenbreite wie bei NV12 in `01 §C.11`: ein kurzer
Absatz, der den Mangel benennt und den Code begründet, dann ein Codeblock mit `core`, `bytes`,
`claim_id`, `σ` und der Zeile `erwartet = Reject: INVALID_PREDICATE`.

Die Hexwerte werden aus `tests/vectors/vectors_01.json` **abgelesen**, nicht getippt: `bytes` ist
`core_bytes`, dazu `claim_id` und `sigma`. Die Hexzeilen brechen bei 64 Zeichen, wie in C.10 und
C.11. Der Prädikat-String wird in `core` wie bei NV5 abgekürzt geschrieben.

### Schritt 5 — Zusicherungen

In `tests/test_predicates.py` drei Zusicherungen, dass `parse_predicate` `InvalidPredicate` wirft:
Großbuchstabe im Namen, Version `0`, Großbuchstabe im Alias-Scope. Die bestehende Zusicherung für
`svc:foo/bar@1` bleibt unverändert `UnknownNamespace`.

**Kein** zusätzlicher Test in `tests/test_verifier.py`: der Tabellentest über die Vektoren mit
`expect_reject` nimmt NV13 von selbst auf. Wird dort trotzdem etwas gebraucht, ist das ein Befund
und wird gemeldet, nicht gebaut.

### Schritt 6 — Rücknahmeprobe

Schritt 2 zurücknehmen — beide `raise` im `nuc:`-Zweig wieder auf `UnknownNamespace` —, den
Testlauf wiederholen und **namentlich** berichten, welche Tests rot werden. Danach Schritt 2
wiederherstellen. Ein Regressionstest, der die Regression nicht sieht, ist keiner.

## Nicht-Ziele

- Keine weitere Fehlerklasse außer `INVALID_PREDICATE`.
- Keine Änderung an den Regexen in `predicates.py`.
- Keine Änderung an bestehenden Vektoren, an ihren erwarteten Codes oder an ihren Zeitstempeln.
- Keine Änderung an `UNKNOWN_NAMESPACE` über die beiden `raise` hinaus.
- Keine Prüfreihenfolge, weder normiert noch als Kommentar behauptet.
- Keine Änderung an `07-decisions.md`, `pruefregeln.md` oder an einer Sitzungsstart-Datei.
- Keine Aufräumarbeit nebenher.

## Abnahmekriterien

1. `make check` läuft grün. Die Testzahl steigt; die Differenz wird berichtet, nicht gerundet.
2. `errors.py` trägt zwölf Codes, `01 §B.2` zwölf Tabellenzeilen. Beide Zahlen werden gegrept,
   nicht geschätzt.
3. `vectors_01.json` trägt genau einen Eintrag mit `expect_reject` gleich `INVALID_PREDICATE`.
4. Die drei Hexwerte in C.12 sind byte-gleich mit `core_bytes`, `claim_id` und `sigma` des
   NV13-Eintrags aus `vectors_01.json`. Der Abgleich wird ausgeführt und sein Ergebnis berichtet.
5. Die Rücknahmeprobe nennt die rot gewordenen Tests mit Namen und Anzahl.
6. `python3 tools/check_specs.py` meldet alle Spec-Dateien sauber.

Widerspricht eine Messung diesem Prompt, wird sie **gemeldet, nicht angepasst**. Erwartete Werte
werden abgeleitet, nie getippt.

## Abschluss

Ein Commit auf `lauf/00af-praedikatform`. Zurück kommen: der vollständige `git diff` gegen
`52bb5bd`, die Testzahl, das Ergebnis der Rücknahmeprobe und das Ergebnis des Hex-Abgleichs aus
Kriterium 4.
