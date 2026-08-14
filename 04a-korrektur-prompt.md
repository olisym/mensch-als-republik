# Korrektur-Prompt — Layer 04a

Eng gefasst. Grundlage: `04-abnahme.md`, Register D108–D111, sowie `04-governance.md` und
`04-golden-anchors.md` in der Fassung auf `main` **nach** dem D108-Merge. Erst `git pull`, dann
lesen, dann bauen.

Der Ausgangsstand ist `impl/04-governance`, Commit `7ed93cd`. Es wird **korrigiert, nicht neu
gebaut**; alle 370 bestehenden Tests bleiben grün, die Zahl steigt.

---

## 1. `governance/tally.py`

**(a) Schwellenform (D108).** `_is_ratio` wird zu einer vollständigen Wohlgeformtheitsprüfung:

```
den >= 1     0 <= num <= den     2 * num >= den
```

Geprüft in **beiden** Verfassungen, nur für die **angewandte** Klasse. Verletzung →
`MALFORMED_THRESHOLD`, Zustand `UNEVALUABLE`.

`[1,2]` ist **zulässig** — die Grenze ist nicht strikt. Ein Test, der `[1,2]` zurückweist, ist rot.

**(b) Paarprüfung vorweg (D110).** Ganz am Anfang von `decide()`, **vor** der Abbruchtabelle:

```
proposal.predecessor != epoch.epoch_id  ->  UNEVALUABLE, STALE_EPOCH_VOTE, Subjekt proposal_hash
```

In der Stimmschleife entfällt die Bedingung **ersatzlos**. Der Vermerk `STALE_EPOCH_VOTE` wird
dort nicht mehr vergeben.

**(c) Identität vor Inhalt (D110).** Beide Verfassungsobjekte werden auf Vorhandensein **und**
Hash geprüft, bevor irgendeine Prüfung ihren Inhalt liest — also
`PROPOSAL_CONSTITUTION_UNAVAILABLE` **vor** der Klassen- und Schwellenbestimmung. Die neue
Reihenfolge steht vollständig in `04 §3.5`; sie ist normativ.

**(d) Leere Teilnehmerliste.** Ein leeres `participants`-Array ist formwidrig →
`MALFORMED_PARTICIPANTS`.

**(e) Keine doppelte Klassenbestimmung.** `decide()` ruft `threshold_for()` auf, statt die
Ableitung inline zu wiederholen. Genau eine Implementierung der Regel.

**(f) `SCOPE_MISMATCH` erst nach der Zuordnung.** Der Vermerk wird nur für Stimmen vergeben, die
auf **diesen** Vorschlag zeigen. Eine `vote@1` eines fremden Nukleus erzeugt keinen Vermerk.

## 2. `governance/epoch.py`

**(a) Bindung an Epoche und Vorschlag (D109).** `TallyResult` trägt zwei neue Felder,
`epoch_id: bytes` und `proposal_hash: bytes`, gefüllt von `decide()`. `verify_ratification`
vergleicht beide mit `epoch.epoch_id` und `proposal.proposal_hash` und wirft bei Abweichung
**`ValueError`** — kein Vermerk. Ein fehlzugeordnetes Objekt ist ein Aufruferfehler (D82, D92).

Auch bei `state = UNEVALUABLE` gelten die beiden Felder und werden verglichen; sie sind nie `None`.

**(b) `TALLY_UNEVALUABLE`.** Ist `tally.state is TallyState.UNEVALUABLE`, entsteht keine Epoche,
Vermerk `TALLY_UNEVALUABLE` statt `UNSUPPORTED_RATIFICATION`.

**(c) Bedingung 4 wird geprüft, nicht impliziert.** Die zitierten `claim_id` dürfen keine zwei
Stimmen **desselben Autors** bezeichnen. Über die Autoren prüfen, nicht über die Identität der
`claim_id`.

## 3. `mensch_als_republik/policy.py`

**(a) `declared` bleibt die Deklaration.** Der Konstruktor überschreibt das Feld nicht mehr. Die
gefilterte Menge steht in `irrevocable`; wird die geprüfte Deklaration zusätzlich gebraucht, tritt
ein eigenes Feld daneben. `declared` und `irrevocable` sagen danach Verschiedenes, und beides ist
ablesbar.

**(b) `warnings` durch `dedupe_sort`.** Pflicht, nicht Kosmetik: bei einem `frozenset` als Eingabe
ist die Reihenfolge sonst unbestimmt, und zwei Läufe über dieselbe Verfassung liefern verschiedene
Tupel. Ein Test stellt das explizit sicher.

**(c) Ein `str` ist kein Array (Präzisierung zu D95).** `list("obligation@1")` liefert zwölf
Einzelzeichen und damit zwölf Vermerke auf Symptome statt einen auf die Ursache. Ein `str` wird
wie ein nicht iterierbarer Wert behandelt: **ein** `MALFORMED_IRREVOCABLE_ENTRY` mit `repr(raw)`,
Liste vollständig ausgefallen.

## 4. `profiles/membership.py` (D111)

Der Parameter `participants: frozenset[bytes] | None` wird ersetzt durch
`constitution_obj: dict | None`.

Ist er gesetzt: zuerst `constitution_hash(constitution_obj)` gegen den Parameter
`constitution_hash` prüfen, bei Abweichung **`ValueError`**. Danach gilt
`subject in constitution_obj["participants"]` als zweite Aufnahmequelle.

Fehlt `participants` im Objekt oder ist es formwidrig, gibt es keine zweite Aufnahmequelle — kein
`ValueError`, kein Vermerk, der Zustand ergibt sich aus der `accept-rules`-Strecke allein.

Die vier Zustände, `grant_claim_id` und die `accept-rules`-Strecke bleiben unverändert.

## 5. Tests

Neu, mindestens:

- `GV-35` bis `GV-45` aus `04-golden-anchors.md §5.3` und `§7`.
- **Eigenschaftstest zu D108:** über alle `[num, den]` mit `1 <= den <= 12` und `0 <= num <= den`
  und alle `n` bis 12 — es existieren genau dann zwei disjunkte Ja-Mengen, die beide `reached`
  erfüllen, wenn `2 * num < den`. Das ist die Herleitung selbst, nicht ein Beispiel dafür.
- Ein Test, der `[1,2]` ausdrücklich als **zulässig** festhält.
- Ein Test, der `warnings` über eine `frozenset`-Eingabe zweimal erzeugt und auf Gleichheit prüft.
- `GV-41` ohne jeden Stimmclaim im Store — der Fall, in dem die alte Fassung `PENDING` lieferte.

Bestehende Tests, die angepasst werden müssen: `GV-11` bis `GV-14` behalten `[1,2]`, aber die
Vermerkerwartung für `STALE_EPOCH_VOTE` wandert von der Stimme auf den `proposal_hash`.

## 6. Ausdrücklich nicht in diesem Schritt

Alles aus `04-prompt.md §9`, unverändert. Zusätzlich: keine feinere Aufschlüsselung von
`UNSUPPORTED_RATIFICATION` in `verify_ratification` — die Sammelform bleibt, auch wenn D94 feiner
nahelegt. Sie ist benannt und nicht übersehen.

## 7. Rückfragen

Wie in `04-prompt.md §11`: jede Frage ohne Antwort in `04-governance.md` ist eine Spec-Lücke und
geht zurück ins Spec-Gespräch. Von siebzehn Abnahmebefunden lagen elf **zwischen** zwei Stellen —
die Wahrscheinlichkeit, dass beim Korrigieren eine zwölfte auftaucht, ist hoch.

Besonders erwartbar: ob `TallyResult.epoch_id` auch dann gesetzt sein soll, wenn `decide()` schon
an der Paarprüfung abbricht. Antwort steht in `§2 (a)` — ja. Wenn sich beim Bauen zeigt, dass das
nicht geht, ist es ein Befund und keine Ermessensfrage.

## 8. Abnahme

Branch `impl/04a-korrektur`. `make check` grün in drei Blöcken. **Committen, bevor gemeldet wird**
— ein Bericht über gestagete Pfade ist kein Ergebnis. `git add` mit expliziten Pfaden.

Erwartete Testzahl: **über 370**. Fällt sie, ist etwas abgeschwächt worden.
