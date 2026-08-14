# Implementierungs-Prompt — Eigenschaftstests

Kein Layer, kein Modul im Paket. Prüfungen unter `tests/property/`, die die Zusagen der
Spezifikation gegen zufällig erzeugte Welten halten.

Neue Test-Abhängigkeit: **`hypothesis`**, unter `[project.optional-dependencies] dev`. Sie kommt
nicht ins Paket. Grund für die Ausnahme: `hypothesis` schrumpft ein Gegenbeispiel automatisch auf
das Minimum, und bei Eigenschaften über Claim-Mengen ist das der Unterschied zwischen „irgendetwas
stimmt nicht" und „diese zwei Claims genügen".

---

## 1. Was hier geprüft wird und was nicht

**Geprüft werden Zusagen, die im Text stehen** — nicht, ob der Code tut, was er tut. Jede
Eigenschaft unten zitiert die Stelle, die sie behauptet, und trägt ihre Vorbehalte ausdrücklich.

**Ein Fuzzer findet nur, was jemand aufgeschrieben hat.** Keiner der Befunde D114 bis D118 wäre so
entstanden; sie kamen aus Durchgängen, nicht aus Läufen. Diese Prüfungen ersetzen die Durchgänge
nicht, sie sichern das bereits Formulierte.

**Alles Rechnende kommt aus dem Paket.** Der Generator baut Welten und ruft `derive`, `trust`,
`decide`, `classify_all` auf. Eine zweite Kapazitätsformel oder eine eigene Auszählung macht jede
Aussage zirkulär.

## 2. Generator

`tests/property/welten.py` — `hypothesis`-Strategien, die eine Welt beschreiben:

- 3 bis 6 Identitäten, Seeds deterministisch aus dem Beispiel abgeleitet
- Ankerset: eine bis zwei Identitäten
- `trust_params`: `C₀` und `D` aus `{16, 100}`, `γ` aus `{1/2, 2/3}`
- 0 bis 12 `vouch@1` mit `n` aus `1…D`, Subjekt beliebig, Selbstbezug ausgeschlossen
- optional Stimmen auf **einen** Vorschlag im Governance-Scope
- ein Zustellplan: welcher Beobachter welche Teilmenge kennt

Zwei Schalter, die **einzeln** setzbar sein müssen, weil die Vorbehalte an ihnen hängen:

```
erlaube_ueberzeichnung : bool     Sigma n je Autor darf D ueberschreiten
erlaube_equivocation   : bool     zwei Claims mit demselben h_prev
```

Voreinstellung für beide: `False`.

## 3. Die Eigenschaften

### P-1 — Reihenfolgeunabhängigkeit

> Derselbe Claim-Bestand in beliebiger Einfügereihenfolge liefert byte-identische Ergebnisse.

Für `derive`, `trust`, `decide` und `classify_all`. Ohne Vorbehalte: das muss immer gelten.

**Das ist die Eigenschaft mit dem höchsten Risiko.** Max-Flow-Lösungen sind **nicht eindeutig** —
der Wert ist es, die Flusszerlegung nicht. Hängt irgendwo eine Auswahl an der Zerlegung statt am
Wert, oder eine Iteration an der Einfügereihenfolge eines `dict`, ist das Ergebnis von der
Reihenfolge abhängig. Alle bestehenden Tests bauen ihre Claims in derselben Reihenfolge auf und
könnten das nie zeigen.

Die Ergebnisse werden **byteweise** verglichen, nicht auf Gleichheit einzelner Felder:
sortierte `claim_id`-Tupel, Kapazitätsabbildungen, Vermerklisten.

### P-2 — Monotonie in Wissen, mit Vorbehalten

> Eine Teilmenge des Claim-Bestands liefert nie **höheres** Vertrauen als der volle Bestand.
> (`02 §7`)

**Vorbehalte, beide zwingend, beide mit Registerbezug:**

- `erlaube_ueberzeichnung = False`. Die Budgetprüfung `Σ n ≤ D` ist **nicht monoton**: ein
  hinzukommender Vouch kann alle Kanten seines Autors entfernen (D118). Kleinstes Gegenbeispiel:
  zwei Vouches mit `n = 51` bei `D = 100`.
- `erlaube_equivocation = False`. Ein eintreffender Zwilling entzieht einem bereits zählenden
  Claim die Wirkung (D117).

Ohne diese beiden Schalter ist die Eigenschaft **falsch**, und ein roter Lauf wäre kein Befund,
sondern eine falsch aufgeschriebene Zusage.

### P-3 — Die Vorbehalte selbst, als eigene Eigenschaften

Was P-2 ausschließt, wird **positiv** geprüft — sonst prüft P-2 nur den bequemen Bereich.

- **P-3a:** mit `erlaube_ueberzeichnung = True` existieren Welten, in denen eine Teilmenge
  **höheres** Vertrauen liefert. `hypothesis` muss ein solches Gegenbeispiel finden; es soll auf
  zwei Vouches schrumpfen.
- **P-3b:** mit `erlaube_equivocation = True` existieren Welten, in denen ein zusätzlicher Claim
  eine zählende Stimme entfernt und ein erreichtes `PASSED` auf `PENDING` zurückfällt.

Beide sind **erwartete** Verletzungen. Ein Lauf, der keine findet, ist der Befund.

### P-4 — Konvergenz

> Haben am Ende alle Beobachter denselben Bestand und dieselbe Uhr, rechnen sie dasselbe.

Ohne Vorbehalte. Gleiche Uhr ist Bedingung, nicht Vorbehalt: über `t_exp` dürfen zwei korrekte
Verifizierer dauerhaft uneins sein (`01 §6`, D72), und das ist der einzige zugelassene Fall.

### P-5 — Die sichere Richtung der Auszählung

> Teilwissen erzeugt nie `PASSED`, wo Vollwissen es nicht tut. (`INV-04.3`)

Vorbehalt: `erlaube_equivocation = False` (D117).

### P-6 — Zeitgrenze

> Ein Claim ist zeitlich gültig **gdw. `now ≤ t_exp`**. (`01 §6`)

Über zufällige `t_exp` und `now` beiderseits der Grenze, mit `now = t_exp` als ausdrücklich
erzeugtem Fall. Diese Regel steht seit Layer 01 und war bis `tools/sim/scenarios/s6.json`
nirgends geprüft; sie gehört als Zusicherung hierher und nicht in ein Werkzeug.

## 4. Reihenfolge des Vorgehens

**Zuerst P-1 auf `derive` und `trust`, allein.** Es läuft schnell, und dort ist eine Verletzung
tatsächlich plausibel. Erst wenn das grün ist, kommen die übrigen dazu.

Findet P-1 ein Gegenbeispiel, ist das ein **Befund** und geht zurück ins Spec-Gespräch — nicht
selbst reparieren, nicht die Eigenschaft abschwächen.

## 5. Form

```
tests/property/
  __init__.py
  welten.py       Strategien und Weltaufbau
  test_p1.py      Reihenfolgeunabhaengigkeit
  test_p2.py      Monotonie mit Vorbehalten
  test_p3.py      Die Vorbehalte positiv
  test_p4.py      Konvergenz
  test_p5.py      Sichere Richtung
  test_p6.py      Zeitgrenze
```

Jede Datei nennt im Modul-Docstring die Spec-Stelle und die Registereinträge, auf denen ihre
Vorbehalte stehen.

Läufe klein halten: `max_examples` so, dass die gesamte Suite unter zehn Sekunden bleibt. Ein
langsamer Test wird abgeschaltet, und ein abgeschalteter Test ist keiner.

Erwartete Testzahl: **über 405.**

## 6. Abnahme

Branch `impl/property`. `make check` grün in drei Blöcken, committen **vor** dem Melden,
`git add` mit expliziten Pfaden.

Gefundene Gegenbeispiele werden **mitgeliefert**: als geschrumpfte Belegung im Testkommentar oder
als eigener Vektor. Ein Gegenbeispiel, das nur im Lauf existierte, ist verloren.

## 7. Rückfragen

Wie immer zurück ins Spec-Gespräch. Besonders erwartbar: ob `hypothesis` als `dev`-Abhängigkeit
mit der Hausregel „nur `cbor2` und `cryptography`" verträglich ist — sie ist es, weil die Regel
das **Paket** betrifft und `pytest` bereits unter `dev` steht. Und die Frage, wie zwei Claims mit
demselben `h_prev` erzeugt werden: `tools/sim/welt.py` hat dafür `kette_fortschreiben=False`.
