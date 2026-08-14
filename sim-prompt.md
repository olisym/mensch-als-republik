# Implementierungs-Prompt — Simulation mit getrennten Beobachtern

Kein Layer, kein Modul im Paket. Ein Werkzeug unter `tools/sim/`, das mehrere Teilnehmer mit
**getrennten Stores, getrennten Uhren und getrennten Schlüsseln** nachstellt.

Alles Rechnende kommt aus `mensch_als_republik`. Die Simulation baut auf, stellt zu und zeigt an —
sie rechnet nichts selbst. Eine zweite Kodierung, eine zweite Kapazitätsformel oder eine zweite
Aktivitätsregel macht jede Aussage der Simulation zirkulär.

---

## 1. Was es ist und was nicht

**Kein Explorer.** Es gibt keinen gemeinsamen Zustand, in den man hineinschaut, und keine
laufende Instanz. Es gibt Teilnehmer, die einander Claims schicken, und jeder rechnet sein Bild
selbst aus.

**Ein gemeinsamer Store wäre der Fehler.** Er macht Teilwissen, Konvergenz und Partition
unsichtbar — und damit genau das, was diese Übung zeigen soll. Jeder Teilnehmer bekommt sein
eigenes Verzeichnis, und **nichts** bewegt sich zwischen ihnen, außer ein Szenarioschritt stellt
ausdrücklich zu.

Die interessanteste Ausgabe ist deshalb keine Zustandsanzeige, sondern eine **Tabelle**: dieselbe
Frage, eine Spalte je Teilnehmer, verschiedene Antworten.

## 2. Bauform

```
tools/sim/
  __init__.py
  welt.py         Teilnehmer, Verzeichnisse, Zustellung
  szenario.py     Szenariodatei lesen und ausführen
  anzeige.py      Tabellen
  scenarios/*.json
```

Je Teilnehmer ein Verzeichnis unter einem Weltpfad:

```
<welt>/anna/
  key.bin         32 Byte Seed
  now             Unix-Sekunden, als Text
  inbox/<claim_id_hex>.cbor
```

**Claims sind einzelne Dateien.** Der Dateiname ist die `claim_id` in Hex, der Inhalt die
kanonischen Bytes. Ein Claim ist nach `01 §4` offline selbstenthalten und trägt seinen eigenen
Verify-Key — die Simulation behandelt ihn deshalb wie einen Gegenstand, den man kopieren,
verschicken oder ausdrucken kann.

**Zustellung ist ein Befehl**, nie automatisch: `zustellen anna -> chris` kopiert alle Claims aus
Annas `inbox`, die Chris noch nicht hat. Nichts synchronisiert von selbst.

Ein Store wird aus dem Verzeichnis geladen, `now` aus der Datei gelesen. `now` ist Parameter, nie
Systemuhr.

## 3. Szenariodatei

JSON, stdlib, keine neue Abhängigkeit. Eine Liste von Schritten; jeder Schritt hat eine Art und
Argumente. Nötige Arten:

`welt` (Teilnehmer mit Seeds und Startzeit anlegen) · `genesis` · `claim` (Autor, Prädikat, J, v,
Scope) · `zustellen` · `uhr` (setzt `now` eines Teilnehmers) · `zeige` (Tabelle) · `erwarte`

**`erwarte` ist Pflicht, nicht Zierde.** Jeder Szenarioschritt, der etwas zeigt, führt seine
erwartete Belegung mit; weicht der Lauf ab, bricht das Szenario mit einem Fehler ab. Ein Szenario
ohne Erwartungen ist eine Vorführung und kein Nachweis.

## 4. Die sechs Szenarien

Alle im Beispielnukleus aus `example-nucleus.md`: `N_gov = 50ecec77…`, `N_res = 4d78bcea…`,
`n = 3`, Schwelle `[1,2]`, zwei Ja nötig. Alle Zahlen unten sind vorgerechnet und sind die
Erwartung.

### S1 — Gründung

ANNA, BRUNO, CHRIS legen `accept-rules@1` auf `constitution_hash_gov` an und stellen einander zu.
Erwartet: alle drei `MEMBER` bei allen drei Beobachtern. DORA existiert noch nicht.

### S2 — Der Dritte entscheidet

Vorschlag `7dfb88e9…` an alle. Dann:

| Stimmen | Ja | Nein | Zustand |
|---|---|---|---|
| Anna ja, Bruno nein | 1 | 1 | `PENDING` |
| dazu Chris ja | 2 | 1 | `PASSED` |
| stattdessen Chris nein | 1 | 2 | `FAILED` |

Ratifizierung durch Anna → `epoch_id_2 = bfcf2768…`. Danach sind alle drei gegen
`constitution_hash_2` **`GRANT_ONLY`**, bis sie neu annehmen — D116, und der Grund, warum dieses
Szenario nach der Ratifizierung noch eine Zeile hat.

### S3 — Partition

Vorschlag an alle. Anna stimmt ja, Bruno nein, beide tauschen **nur untereinander**. Dann stimmt
Chris ja und stellt **nur an Anna** zu.

| Beobachter | Ja | Nein | Zustand |
|---|---|---|---|
| Anna | 2 | 1 | `PASSED` |
| Bruno | 1 | 1 | `PENDING` |
| Chris | 1 | 0 | `PENDING` |

Dann alles an alle: alle drei `PASSED`. **Die Uneinigkeit war Wissen, nicht Rechnung** — sie
konvergiert.

### S4 — Überzeichnung

Im Ressourcen-Scope, vier Kanten wie in `example-nucleus.md §7`.

| `n` je Kante | `Σ n` | Ergebnis |
|---|---|---|
| 50 | 100 | in Ordnung; CHRIS in Distanz 1, `C = 50` |
| 100 | 200 | `OVERCOMMITTED_AUTHOR` für ANNA und BRUNO, **alle vier** Kanten weg, CHRIS unerreichbar |

Nicht die zuletzt hinzugefügte Kante fällt und nichts wird anteilig gekürzt. Das ist die
Betriebswarnung aus `§8.1`, in Handlung.

### S5 — Equivocation

**Das tragende Szenario.** Anna signiert zwei `vote@1` mit **demselben `h_prev`**: ein Ja, das sie
nur Bruno zustellt, ein Nein, das sie nur Chris zustellt. Chris stimmt ja und stellt an alle zu.

| Beobachter | kennt | Ja | Nein | Zustand |
|---|---|---|---|---|
| Bruno, vor Austausch | Anna-Ja, Chris-Ja | 2 | 0 | **`PASSED`** |
| Chris, vor Austausch | Anna-Nein, Chris-Ja | 1 | 1 | `PENDING` |
| beide, nach Austausch | Anna `EQUIVOCATION_FLAGGED` | 1 | 0 | `PENDING` |

Brunos `PASSED` **kippt zurück**. Ratifiziert er vorher, verfällt seine Epoche mit
`UNSUPPORTED_RATIFICATION`. Beides ist erwartet und kein Fehler (D117).

Das Szenario zeigt `08 §2.2` in Handlung: Equivocation wird nicht verhindert, sondern
**unbestreitbar** — und zwar erst in dem Moment, in dem die beiden Empfänger einander zustellen.
Vorher sieht keiner von beiden etwas Verdächtiges.

### S6 — Uhrenstreit

Im Ressourcen-Scope, **eine** Kante zu CHRIS, damit sie nur einen Pfad hat:
`BRUNO → CHRIS`, `n = 50`, `t_exp = 5000`. Dazu `ANNA → BRUNO`, `n = 50`, ohne `t_exp`.
Ankerset `{ANNA, BRUNO}`.

| Beobachter | `now` | Kante | CHRIS |
|---|---|---|---|
| Anna | 4000 | gültig | Distanz 1, `C = 50` |
| Bruno | 6000 | `EXPIRED` | unerreichbar, keine Kapazität |

Beide haben **denselben** Claim-Bestand. Diese Uneinigkeit **konvergiert nicht** — sie ist der
einzige legitime Fall (D72, `01 §6`), und die sichere Richtung ist Unter-Vertrauen.

S3 und S6 gehören nebeneinander gelesen: dieselbe Erscheinung, zwei Ursachen, und nur eine heilt
von selbst.

## 5. Was nicht gebaut wird

- Keine interaktive Schale. Sie kann später daraufgesetzt werden; die Szenarien sind zuerst
  wichtiger, weil sie prüfbar sind.
- Keine Netzwerkzustellung. Kopieren im Dateisystem, mehr nicht.
- Kein Schlüsselschutz, keine Wiederherstellung. Seeds liegen im Klartext — es ist eine
  Simulation, und das gehört in die README des Verzeichnisses.
- Keine neuen Abhängigkeiten. `json` aus der stdlib, `cryptography` für Ed25519.

## 6. Tests und Abnahme

`tests/test_sim.py` führt alle sechs Szenarien aus und prüft ihre `erwarte`-Belegungen. Import aus
dem Werkzeug, keine eigene Logik — wie bei `test_example_nucleus.py`.

Erwartete Testzahl: **über 399.**

Branch `impl/sim`. `make check` grün in drei Blöcken, committen **vor** dem Melden, `git add` mit
expliziten Pfaden.

## 7. Rückfragen

Jede Frage ohne Antwort in diesem Prompt oder den Spec-Dateien ist eine Lücke und geht zurück.
Besonders erwartbar: wie zwei Claims mit demselben `h_prev` erzeugt werden, ohne dass die
Autorenkette in `_Author` sie fortschreibt — S5 verlangt es ausdrücklich, und `tools/example_nucleus.py`
kennt diesen Fall nicht.
