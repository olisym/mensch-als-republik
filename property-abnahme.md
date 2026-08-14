# Eigenschaftstests — Abnahme

Gegenstand: `impl/property` (`c7aa248`) und `impl/make-prop` (`3eec778`), gemergt als `7dda951`
und `5873dac`. 415 Tests, `make check` 4,5 s, `make check-all` 13,4 s.

**Abgenommen.**

## 1. Was P-1 beantwortet hat

> Derselbe Claim-Bestand in beliebiger Einfügereihenfolge liefert byte-identische Ergebnisse.

**Grün — und das ist ein Ergebnis, keine Formalie.** Max-Flow-Lösungen sind nicht eindeutig: der
Wert ist es, die Flusszerlegung nicht. Hätte irgendwo eine Auswahl an der Zerlegung gehangen oder
eine Iteration an der Einfügereihenfolge eines `dict`, wäre `derive` reihenfolgeabhängig gewesen —
und **kein bestehender Test hätte es zeigen können**, weil alle 405 ihre Claims in derselben
Reihenfolge aufbauen.

Der Test vergleicht zwei getrennt gebaute Stores über Fingerprints, nicht zweimal denselben.

## 2. P-3 ist der einzige Test, dessen Erfolg eine Verletzung ist

Jede andere Prüfung im Projekt wird grün, indem nichts passiert. P-3 wird grün, indem etwas
passiert: `hypothesis.find` **muss** ein Gegenbeispiel liefern, sonst wirft es und der Test ist
rot. Solche Tests scheitern typischerweise still, wenn jemand den Wurf abfängt — hier ist er es
nicht.

Dazu zwei handgeschriebene Vektoren, die in **beiden** Profilen laufen:

- **P-3a:** zwei Vouches mit `n = 51` bei `D = 100` — die Teilmenge über-vertraut (D118).
- **P-3b:** Annas Zwillingsstimmen, `PASSED` fällt auf `PENDING` (D117).

Sie sind das Rückgrat. Würfelt der Generator eines Tages anders, halten sie die Aussage trotzdem.
Ein Eigenschaftstest ohne festen Vektor ist eine Wette auf den Zufallsgenerator.

## 3. Die Profilwahl, mit Begründung

| Profil | Beispiele | Zeit |
|---|---|---|
| `schnell` (Voreinstellung) | 10 | `make check` 4,5 s |
| `voll` (`MAR_HYPOTHESIS=voll`) | 100 | `make check-all` 13,4 s |

Zunächst standen 300 Beispiele und 37 s. Gemessen: `teilmengen()` ist bereits linear gebaut —
Zustellplan plus Leave-one-out, nicht die Potenzmenge —, die Kosten sitzen also allein bei
`max_examples`.

**Warum 100 und nicht 300.** `hypothesis` sucht nicht gleichverteilt, sondern führt Beispiele
gezielt an Ränder; strukturelle Verletzungen fallen in den ersten Dutzenden. Die zusätzlichen 200
kosteten 22 s und kauften Varianten derselben Form.

**Und warum das keine Bequemlichkeit ist:** 37 s vor jedem Merge sind die Größenordnung, bei der
Menschen anfangen, `make check` statt `make check-all` zu tippen. Ein Lauf, der umgangen wird,
sichert nichts — dieselbe Mechanik wie ein Wächter, der nur eine Richtung kennt.

> **Wer diese Zahl später erhöhen will, erhöhe zuerst nicht `max_examples`, sondern die Zahl der
> Eigenschaften.** Eine weitere geprüfte Zusage bringt mehr als zweihundert weitere Belegungen
> einer bereits geprüften.

`teilmengen()` bleibt, wie es ist. Leave-one-out ist schärfer als eine Zufallsstichprobe, weil
eine P-2-Verletzung sich fast immer beim Weglassen eines **einzelnen** Claims zeigt — des einen
Vouchs, der die Überzeichnung auslöst.

## 4. Der Fund kam ohne Fuzzer

**D118 entstand, bevor eine Zeile Testcode existierte.** Beim Versuch, P-2 exakt hinzuschreiben,
fiel auf, dass die Zusage aus `02 §7` — „die einzige gefährliche Richtung ist ein fehlender
Widerruf" — so nicht stimmt: die Budgetprüfung zwischen Bestand und Graph ist nicht monoton. Der
Lauf hat es danach bestätigt, mit demselben Gegenbeispiel, das vorher von Hand gerechnet war.

Das ist die Regel „vor dem Schreiben rechnen" in ihrer stärksten Form:

> **Eine Eigenschaft so genau zu formulieren, dass eine Maschine sie angreifen kann, ist selbst
> die Prüfung.** Wer eine Zusage nicht als Test hinschreiben kann, ohne zu stolpern, hat sie noch
> nicht verstanden.

Und die Grenze davon, die ebenso deutlich ist: ein Fuzzer findet nur, was jemand aufgeschrieben
hat. Keiner der Befunde D114 bis D117 wäre so entstanden — ein Feld ohne Leser, zwei Definitionen
über einen Epochenwechsel hinweg, ein dritter Ausgang aus einem Zustand. Diese Prüfungen ersetzen
die Durchgänge nicht; sie sichern, was die Durchgänge gefunden haben.

## 5. Drei Werkzeuge, drei Fehlerarten

| Werkzeug | fängt |
|---|---|
| `tools/example_nucleus.py` | Dokument gegen Code — dokumentierte Zahl stimmt nicht mit gerechneter |
| `tools/sim` | getrennte Sichten gegeneinander — Teilwissen, Uhren, Equivocation |
| `tests/property` | Zusagen gegen Zufall — Reihenfolge, Monotonie, Konvergenz, Grenzwerte |

Keines ersetzt ein anderes. Der Beispielnukleus hat die Budgetverletzung im eigenen Dokument
gefunden, die Simulation D117 und den ungeprüften Grenzwert `now = t_exp`, die
Eigenschaftsformulierung D118.
