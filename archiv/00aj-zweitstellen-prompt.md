# 00aj — Zehn Träger für die Doppelerzeuger

## Branch und Basis

Branch `00aj-zweitstellen`, Basis ist der Splice-Commit mit D287 auf diesem Branch. Ein Commit am
Ende, kein Merge.

## Normative Grundlage

- **D287** — die zehn nie erreichten Erzeugerstellen aus D281 sind erreichbar und bekommen je
  einen Träger; keine wird gestrichen.
- **Prüfregel 57** — wo zwei Pfade gekoppelt geprüft werden, braucht jeder zusätzlich einen Träger.
- `03 §1.3` (Form für das Lesen von `v`, D276), `03 §2.4.2`, `03 §3.3.2`, `03 §4`,
  `04 §3` und `04 §3.5`.

## Auftrag

Zehn Tests, nur Tests. **Kein Produktivcode wird geändert.**

Ablage: vier in einer neuen Datei `tests/governance/test_zweitstellen.py`, fünf in einer neuen
Datei `tests/profiles/test_zweitstellen.py`, einer in der bestehenden Datei
`tests/trust/test_payload.py`. Vorhandene Fixtures beider Pakete werden benutzt, keine neuen
angelegt.

Jede Welt ist unten Feld für Feld beschrieben. Werte, die nicht genannt sind, wählt der Lauf
so einfach wie möglich.

### `tests/governance/test_zweitstellen.py`

1. **`read_v` mit kanonischem Nicht-Map.** `read_v` aus `mensch_als_republik/governance/tally.py`
   direkt aufrufen, Argument ist die kanonische Kodierung der Zahl `1`. Erwartet: kein Objekt und
   der Vermerk `UNPARSABLE_V`.
2. **`participants` ist eine Map.** `constitution_governable` direkt aufrufen mit der
   Fixture-Verfassung `C1`, in der `participants` durch eine Map ersetzt ist, deren einziger
   Schlüssel ein 32-Byte-Pubkey aus den Fixtures ist. Erwartet: `MALFORMED_PARTICIPANTS`.
   **Nicht** eine Zeichenkette nehmen: die trifft dasselbe Ergebnis über ein anderes Tor.
3. **Die Schwellenklasse fehlt.** Eine Verfassung aus `C1`, in der `thresholds` keine Map ist.
   Dazu ein Genesis-Objekt mit dieser Verfassung in Key 4, Key 5 auf 2, Key 6 auf 0, und der
   daraus gerechnete Scope. Epoche mit Index 1 auf diese Verfassung, Vorschlag auf
   `CONSTITUTION_HASH_2`. `decide` mit leerem Store aufrufen. Erwartet: Zustand `UNEVALUABLE` und
   der Vermerk `MALFORMED_THRESHOLD`.
4. **Auszählung ohne Teilnehmermenge.** Ein `ratify@1`-Claim im Scope der Fixture-Epoche `EPOCH_1`,
   `J = (3, PROPOSAL_1.proposal_hash)`. Dazu ein von Hand gebautes `TallyResult` mit Zustand
   `PASSED`, leeren Stimmlisten, `participants = None`, `threshold = None`, keinen Vermerken und
   den Kennungen aus `EPOCH_1` und `PROPOSAL_1`. `verify_ratification` damit aufrufen. Erwartet:
   keine Folgeepoche und der Vermerk `TALLY_UNEVALUABLE`.

### `tests/profiles/test_zweitstellen.py`

5. **`read_v` mit kanonischem Nicht-Map.** `read_v` aus `mensch_als_republik/profiles/payload.py`
   direkt aufrufen, Argument ist die kanonische Kodierung der Zahl `1`. Erwartet: kein Objekt und
   `UNPARSABLE_V` als einziger Vermerk.
6. **Obligation mit `v[1]` vom falschen Typ.** Eine `obligation@1` von Alice auf Bob im Scope
   `N_A`, `v` ist die kanonische Kodierung der Map mit Schlüssel `1` und Wert `5`. Store enthält
   nur die Obligation. `settlement` mit der aufgelösten Policy zu `N_A`. Erwartet: der Vermerk
   `INVALID_V_TYPE`.
7. **Quittung mit `v[0]` vom falschen Typ.** Eine `obligation@1` von Alice auf Bob im Scope `N_A`
   ohne `v`, dazu eine `receipt@1` von Bob auf die Obligation, `v` ist die kanonische Kodierung
   der Map mit Schlüssel `0` und einer Zeichenkette als Wert. Store enthält beide. `settlement`
   wie oben. Erwartet: der Vermerk `INVALID_V_TYPE`.
8. **`grant-membership` im fremden Scope.** Ein `grant-membership@1` von Alice auf Bob, dessen
   Prädikat den Scope `N_A` nennt, dessen Feld `N` aber einen anderen 32-Byte-Wert trägt. Store
   enthält nur diesen Claim. `membership` für Bob im Scope `N_A` mit Alice als autorisiertem
   Schlüssel. Erwartet: der Vermerk `SCOPE_MISMATCH`.
9. **Verdikt auf eine unbekannte Anschuldigung.** Ein `verdict@1` von Alice im Scope `N_A` mit
   `J = (2, h)`, wobei `h` ein 32-Byte-Wert ist, zu dem der Store keinen Claim hält. Store enthält
   nur das Verdikt. `verdict_status` mit Alice als Schiedsperson. Erwartet: der Vermerk
   `UNKNOWN_ACCUSATION`, und sein **Subjekt ist `h`**, nicht die Claim-ID des Verdikts. Das
   Subjekt wird mitgeprüft: es unterscheidet diese Stelle von ihrer Nachbarin.

### `tests/trust/test_payload.py`

10. **`n` ist keine Ganzzahl.** `_decode_weight` direkt aufrufen mit der kanonischen Kodierung der
    Map, deren Schlüssel `0` eine Zeichenkette trägt, und einem `D` von 4. Erwartet: kein Gewicht
    und `UNPARSABLE_VOUCH_PAYLOAD`. **Nicht** eine Map ohne Schlüssel `0` nehmen: die trifft
    dasselbe Ergebnis über ein anderes Tor.

## Nicht-Ziele

- **Keine Änderung an Produktivcode.** Nicht in `mensch_als_republik/`, nirgends. Wer beim Bauen
  einen Defekt findet, meldet ihn und behebt ihn nicht.
- **Keine Änderung an `07-decisions.md`.** D287 ist mit dem Splice-Commit fertig.
- **Keine Änderung an bestehenden Tests** außer der einen Ergänzung in
  `tests/trust/test_payload.py`.
- **Keine neuen Fixtures, keine neuen Hilfsmodule.**
- **Keine Vektoren.** Diese zehn Stellen liegen oberhalb des Atoms; Anhang C ist nicht betroffen.

## Abnahmekriterien

1. `make check` läuft durch. Die Testzahl ist **668**.
2. Ein Überdeckungslauf **nur über die zehn neuen Tests** erreicht in jeder der sechs berührten
   Produktivdateien die Zeile, auf die der jeweilige Test zielt. Der Lauf berichtet je Test die
   Datei und die Zeilennummer der erzeugenden Anweisung. Ein Test, der grün ist und seine Zeile
   nicht erreicht, ist kein Träger.
3. `git diff` gegen den Branchpunkt zeigt Änderungen ausschließlich in
   `tests/governance/test_zweitstellen.py`, `tests/profiles/test_zweitstellen.py` und
   `tests/trust/test_payload.py`.

## Rücknahmeproben

Zehn Proben, je eine pro Test. Jede: die Bedingung samt Vermerkserzeugung an der Zielzeile
entfernen, **nur** den zugehörigen Test fahren, rot bestätigen, wiederherstellen. Alle zehn sind
vorab geeicht und schließen einzeln — keine braucht eine zweite Stelle. Wird eine Probe grün, ist
das ein Befund und wird gemeldet.

## Abschluss

Ein Commit auf `00aj-zweitstellen`. Im Bericht: die Testzahl, die zehn Zeilennummern aus dem
Überdeckungslauf, das Ergebnis jeder der zehn Rücknahmeproben und der **vollständige** `git diff`
gegen den Branchpunkt.
