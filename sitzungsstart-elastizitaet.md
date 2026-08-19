# Sitzungsstart: Elastizität (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen seit D144 in `pruefregeln.md`** — 1 bis
21, im Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert,
zitiert die Nummer.

Was in der Praxis am häufigsten gebraucht wird:

- **Design vor Code.** Alle Forks und Zahlen stehen fest, bevor ein Prompt geschrieben wird.
  **Modulcode vor Prompt** — alle betroffenen Quellen lesen, bevor ein Prompt entsteht. Die
  Signaturen von `trust()` und `derive()` zu kennen hat in der letzten Sitzung den Zuschnitt des
  Messlaufs entschieden.
- **Der Bericht des Werkzeugs ist nie die Abnahme.** Geprüft wird der Diff. In der letzten
  Sitzung lagen in einem korrekt beschriebenen Commit fünf Defekte.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt — auch dir
  selbst aus der vorigen Runde.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: nur `cbor2` und `cryptography`, unter `dev` `pytest` und
  `hypothesis`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`,
  **nie `and` innerhalb einer Pipe**. `grep -c` mit Ergebnis null gibt Status 1 und bricht die
  Kette — das ist nutzbar, muss aber angesagt werden.
- **Spec-Dateien als Download**, nicht als Copy-Block. Werkzeug-Prompts als Copy-Box oder, wenn
  lang, als Datei. Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher
  trocken gegen die Projektkopie gelaufen.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet -- <datei>`, damit
  niemand seit dem Basis-Commit dazwischengegriffen hat.
- Bei neuen Dateien `git add` **vor** `make check` / `check_specs.py`, sonst danach. `git add`
  mit expliziten Pfaden, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`; `check_specs.py` prüft Prompt- und
  Abnahme-Dateien im Wurzelverzeichnis mit.
- **Der Vergleichspunkt eines Laufs ist der Prompt-Commit.** Liegt ein Nachlauf-Prompt auf dem
  Branch, sind zwei geänderte Dateien richtig und nicht falsch.
- Claude darf `sha256sum` einer Projektkopie selbst rechnen und sie dann lesen statt anfordern.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`.

**`main` liegt auf `82e0a44`**, gepusht (der Commit dieser Datei kommt darüber). Keine offenen
Branches. **500 Tests**, dazu **14 Eigenschaftstests** unter `MAR_HYPOTHESIS=voll`. **53
Spec-Dateien**, Register **D1–D144**. Die Zahlen beim Sitzungsstart ablesen, nicht schätzen.

- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests.

**Neu in der letzten Sitzung:** D142, D143, D144, dazu `tests/trust/test_deckenelastizitaet.py`
(vier Testfunktionen, sechs gemessene Zustände) und `pruefregeln.md`.

- **D142** — die Decke wandert **genau dann**, wenn ein Zug die Distanz eines Grenzknotens
  verschiebt. Bewegt er `d` nicht, steht `Σ C(h)` still und der Zug addiert höchstens den Fluss,
  den er selbst trägt: Hebel `3` beim Distanzkauf gegen Hebel `≤ 1` bei allem anderen. Wo die
  Decke nicht bindet, ist die Schranke schlaff und **überschätzt den Angreifer** — die sichere
  Richtung, kein Defekt. Der Defekt ist allein die Beweglichkeit. Nebenbei geschlossen: die
  Skalierung wächst linear bei konstantem Hebel, und in der gemessenen Topologie bindet das
  Budget des **Ankers** vor dem Budget des verwirrten Knotens.
- **D143** — kein Mechanismus gegen den Distanzkauf. Begründung nicht nur über `08 §3`, sondern
  über den Befund: der Hebel entsteht daraus, dass die Decke ehrlichen Fluss abschneidet, der
  bereits anliegt. Wer den Kauf verhindert, hält genau diesen ehrlichen Fluss draußen. Die
  Rücknahmeprobe steht im Voraus fest — entsteht je ein Mechanismus, werden zwei Testdateien rot.
- **D144** — `pruefregeln.md`, Nummern 8 und 9 vergeben, sechs abgelöste Sitzungsstarts gelöscht.
- **`02 §4`** hat einen Querverweisblock auf D142/D143 im bestehenden D139-Warnabschnitt.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem
echten gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand;
so tun als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in
der nächsten Sitzung eine Gelegenheit zu erfinden.

## Das Aufnahmekriterium

Aus `08 §3`, vor jedem neuen Mechanismus:

> **Senkt er die Kosten dafür, festzustellen, wer was gesagt hat — oder verteilt er Macht?**
> Senken: Protokoll. Verteilen: Policy. Keines von beidem: Werkzeug.

Es hat in der letzten Sitzung den Fork geschlossen, gemeinsam mit der Messung.

## Was die letzte Sitzung gelehrt hat

**Vier Anläufe, vier Defekte, alle vier im Prompt.** Das Werkzeug hat viermal richtig gemeldet
statt still zu reparieren — die falsche Erwartung in Fall B, ein Abnahmekriterium, das zwei
Dateien verbot, die richtig waren, eine Rücknahmeprobe, die nicht greifen konnte, und eine, deren
Erwartung schlampig formuliert war. Der Supervisor war in dieser Sitzung die Fehlerquelle, nicht
der Engpass des Werkzeugs.

**Zweimal derselbe Fehlertyp, daraus Prüfregel 21.** Eine Kapazität als Ertrag geführt: erst
`cap(p → h) = 8` als Beitrag, obwohl `p` nur `4` empfängt, dann `C(p)` in einem `min`, obwohl
`02 §3` ihn als nie allein bindend beweist. Beide Male fiel die Behauptung erst, als sie an einer
konkreten Topologie präzise werden musste — das D118-Muster.

**Ein Kontrollfall ist mehr wert als ein zweiter Beleg.** Fall B sollte nur zeigen, dass ein Zug
ohne Distanzbewegung die Schranke stillstehen lässt. Er hat stattdessen die gerechnete Erwartung
widerlegt und den eigentlichen Befund geliefert. Die drei Fälle, die trafen, haben nichts Neues
gesagt.

**Eine Schranke, die den Angreifer überschätzt, ist kein Defekt.** Der Supervisor hat die
Schlaffheit von `Σ C(h)` zunächst als Mangel geführt und daraus fast ein Verbot für Gates
abgeleitet — nach dem Vorbild von `§5`. Die Analogie trägt nicht: `§5` ist verboten, weil es gar
keine Schranke ist. Bei einer Verteidigungsschranke ist Überschätzung die sichere Richtung.

**Ein Aufräumen kann Datenverlust sein.** Die sieben Sitzungsstarts sahen nach Ballast aus. Der
Volltext der Prüfregeln stand nur dort, verteilt über fünf Dateien, und wäre in einem Commit
namens „abgelöste Sitzungsstarts entfernt" verschwunden. Prüfregel 17 hat gegriffen, weil sie vor
dem Löschen und nicht danach angewandt wurde.

## Der nächste Schritt

Vorschlag, nicht entschieden: **`00a-rotate-key` und der Sicherungsblob (D120)**. Begründung —
die Anwendung wartet auf Menschen, aber die Dinge, die *beim* Eintreffen von Menschen sofort
gebraucht werden, sind beschreibbar und derzeit ungebaut. D62 (`resolve_current_key`) steht seit
Layer 00 offen; nach D123 ist ein zweites Gerät eine **Rotation**, keine Delegation, und der Fall
tritt beim ersten Gerätewechsel ein, also **vor** dem ersten echten Nukleus. Offen bleiben dort
der Effektivpunkt der Governance-Rotation (uhrfrei zu formulieren) und die Schwellenfrage
(`00 §4`).

Vor jeder Entscheidung dort: Prüfregel 15. Die Schlüsselrotation ist der eine von drei
SSB-Befunden, der in MaR strukturell **nicht** geschlossen ist.

## Offen

- **`00a-rotate-key` / D62**, D125 und D126 stehen. Siehe oben.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut.
- **`disjoint_paths` bewegt sich nicht** (bleibt `1` in allen gemessenen Fällen). Ob das trägt
  oder ein Artefakt der Topologien ist, ist nicht gemessen.
- **`make check` steigt in `.venv` ab:** `find . -name __pycache__ -type d -exec rm -rf {} +`
  ohne `-not -path "./.venv/*"`. Unter `-j1` nur langsam, parallel eine Kollision.
- **Ausgang 5 / Selbst-Equivocation.** Entschieden: nicht im Einlesepfad, kein zwölfter
  Reject-Code. Offen bleibt der Ort — eine Diagnoseoperation über den geladenen Store, ohne den
  `Ausgang`-Port zu verbreitern (D127).
- **`FOREIGN_LIFECYCLE` hat keinen Produktivträger mehr** (D138, bewusst).
- **Meldung übersprungener Claims aus `store_laden`** — von D138 zurückgestellt.
- **`03-prompt.md`-Verweise im Paketcode** — vier Stellen unter `mensch_als_republik/profiles/`
  und `policy.py`. Nach Prüfregel 17 doppelt relevant.
- **Gleichstand bei `kante_claim_id`** — der Bruch über `sorted(...)[0]` ist von nichts geprüft.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** prüfen eine schwächere Aussage als sie
  scheinen (D117).
- **Dreifache Kantensumme in `test_deckenelastizitaet.py`.** `cap(A → p)` und `Σ cap(p → h)`
  stehen im Helfer und in zwei Testfunktionen. Änderte sich die Kantenauswahl im Helfer, blieben
  die Behauptungen still grün. Bewusst so, weil die Alternative Zirkularität wäre — notiert,
  nicht blockierend.
- **`02d-purpose`** (D56), **VR-04.1** (D26), **Zeugenquorum für Fristen** (D100).
- **`04 §7.2` Föderation** nicht durchgerechnet.
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **`example-nucleus.md`** unvollständig.
- **Layer 05.** Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf) und die
  Beta-Reputation mit dem Moral-Licensing-Problem, gegen das Layer 02s Flussmodell immun ist und
  `05` es nicht wäre.
- **Die Anwendung.** Wartet auf Menschen. Siehe oben.
