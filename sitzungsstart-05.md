# Sitzungsstart: nach Layer 04 (MaR)

## Kontext

Wir arbeiten an **Mensch als Republik (MaR)**, einem dezentralen Koordinationsprotokoll.
Python-Referenzimplementierung, Branch-per-Layer, selbst gehostete Gitea-Instanz
(`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

**Arbeitsweise:**
- Design vor Code. Alle Forks und Zahlen stehen fest, **bevor** ein Prompt geschrieben wird.
- Die Spec ist normative Wahrheit. Der committete Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten im Paket: nur `cbor2` und `cryptography`. Unter `dev` zusätzlich
  `pytest` und `hypothesis`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer
  Parameter, nie Systemuhr.
- Shell-Befehle als **ein** Copy-Block, fish, kein Heredoc, verbunden mit **`and`** und nicht mit
  `;` — eine rote Prüfung muss die Kette anhalten. Ein `;` hat in der letzten Sitzung einen roten
  `main` erzeugt und gepusht.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`.
- `git add` mit expliziten Pfaden, nie `-A`.
- **Ein Implementierungslauf endet mit einem Commit auf einem benannten Branch**, nie mit einem
  Bericht über gestagete Pfade. Eine Runde ist so schon einmal verlorengegangen.

⚠️ **Dateien nie manuell editieren.** Spec-Dateien kommen vollständig von Claude oder über ein
Patch-Skript, das anhängt. Vor einer Ersetzung mitten in einer Datei per `sha256sum` abgleichen.

⚠️ **Das Projektwissen ist nicht die Quelle für Dateien.** Frag nach dem Repo-Stand. Für **Code**
gilt das noch mehr als für Spec.

## Stand

**Layer 01, 02, 03 und 04 sind auf `main`, das v1-Ziel ist vollständig.** Register **D1–D118**,
**415 Tests**, `make check` 4,5 s, `make check-all` 13,4 s.

- **01** Atom, Verifier, elf Reject-Codes, acht Zustände.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung. Kein Snapshot, keine
  gewichtete Auszählung, kein Zweckgraph.
- **08-scope.md** Zweckbestimmung und Aufnahmekriterium.

**Drei Werkzeuge** neben der Spec:
- `tools/example_nucleus.py` — der Beispielnukleus, gerechnet und gegen `example-nucleus.md`
  geprüft; reproduziert die Bestandsanker aus `00 §3.1`.
- `tools/sim` — Simulation mit **getrennten** Beobachterstores, sechs Szenarien S1–S6.
- `tests/property` — Eigenschaftstests P-1 bis P-6 über `hypothesis`, zwei Profile.

## Das Aufnahmekriterium

Vor jedem neuen Mechanismus, aus `08 §3`:

> **Senkt er die Kosten dafür, festzustellen, wer was gesagt hat — oder verteilt er Macht?**
> Senken: Protokoll. Verteilen: Policy.

Dieses Kriterium hat in Layer 04 mehr Forks geschlossen als jede Rechnung. Die Schicht wurde
dadurch kleiner, als sie geplant war, und das war der Gewinn.

## Sieben Prüfregeln

Aus den Befunden der letzten Sitzungen, geordnet nach dem Zeitpunkt, an dem sie greifen:

1. **Vor dem Schreiben rechnen.** Jede Zahl, die aus einer Regel folgt, wird gerechnet, bevor sie
   geschrieben wird — nicht danach geprüft. Eine Eigenschaft so genau zu formulieren, dass eine
   Maschine sie angreifen kann, ist selbst die Prüfung.
2. **Standprüfung.** Vor jedem Mechanismus zu Nebenläufigkeit, Ordnung oder Schwellen fragen,
   unter welchem Namen das Problem außerhalb des Projekts gelöst ist. CALM und ein Raft-Befund
   haben je einen eigenen Vorschlag widerlegt (D96, D102).
3. **Feldinventur.** Für jedes Feld eines Schemas benennen, welche Funktion es liest. Felder ohne
   Leser sind zu streichen oder als deklarativ zu kennzeichnen (D114).
4. **Zugehörigkeitsliste am Datentyp.** Welche Felder eine Zugehörigkeit behaupten und wogegen sie
   zu prüfen sind, wird bei der **Definition** des Typs aufgeschrieben (D112).
5. **Ausgänge aufzählen.** Wo eine Invariante einen Zustandsübergang ausschließt, werden **alle**
   Ausgänge aus dem Zustand aufgezählt — aus dem Code, nicht aus dem Gedächtnis (D117).
6. **Monotonie stufenweise.** Eine Monotonieaussage gilt zunächst nur für die letzte Stufe. Jede
   Stufe davor wird einzeln geprüft (D118).
7. **Abhängigkeitssatz bei Reihenfolgeänderungen.** Wird eine Reihenfolge geändert, wird für jede
   Größe, die in der alten nebenbei entstand, benannt, woher sie in der neuen kommt (D113).

Dazu die beiden älteren: **Parallelenprüfung** (zwei Stellen, die dasselbe tun, nebeneinanderlegen)
und **Begründungsprüfung** (ist eine Begründung an einen Fehlermodus gebunden, und gibt es einen
zweiten).

## Was die letzte Sitzung gelehrt hat

**Elf von neunzehn Abnahmebefunden lagen zwischen zwei Stellen**, nicht in einer. Kein einziger war
eine Abweichung vom Prompt — das Werkzeug hat gebaut, was dastand, und viermal zurückgefragt statt
umzudeuten. Was gefehlt hat, hat in den Dokumenten gefehlt.

**Fünf Befunde lagen in bereits abgenommenen Schichten** (D114–D118), einer davon in Layer 02, das
seit Wochen grün ist. Eine Abnahme sichert den Stand, nicht die Zukunft.

**Die Kette D105 → D107 → D109 → D111 → D112** war viermal dieselbe Unvollständigkeit: eine
Reparatur, die richtig war und nicht auf die Geschwister ihrer eigenen Art durchgezogen wurde.
Regeln 4 und 5 setzen genau dort an.

## Offen, nicht blockierend

- **Der Grenzwerttest `now = t_exp`** lebt in `tests/property/test_p6.py` und
  `tools/sim/scenarios/s6.json`, aber nicht in den Vektoren von Layer 01, wo die Regel steht.
  Beim nächsten `01`-Durchgang nachziehen.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** in der bestehenden Suite laufen grün, weil
  ihre Claim-Folgen zufällig keine Equivocation enthalten. Sie prüfen eine schwächere Aussage als
  die, die sie zu prüfen scheinen (D117).
- **`02d-purpose`** (Zweck-Tag am Vouch, D56), **`00a-rotate-key`** (`resolve_current_key`, D62),
  **VR-04.1** (Kettenbindung von Ämtern, D26), **Zeugenquorum für Fristen** (D100).
- **`04 §7.2` Föderation** ist eine Belegung desselben Loops und nicht durchgerechnet.
- **Ein dritter Scope nur für Schlichtung** — der Ausweg aus dem Dilemma „änderbare Regeln **und**
  unangreifbare Substanz" (`example-nucleus.md §6`). Fork, nicht entschieden.

## Wenn Layer 05 kommt

Sieben Prüfregeln **vor** dem ersten Prompt anwenden, nicht danach. Konkret heißt das: Feldinventur
über `05`s Schemata, Zugehörigkeitsliste für jeden neuen Datentyp, alle Ausgänge aus jedem neuen
Zustand aufzählen, und jede Monotonieaussage stufenweise prüfen.

`05` hat zwei bekannte Baustellen: **Über-Commitment als Stufe-3-Auslöser** (D40, jetzt mit D118
scharf geworden) und die **Beta-Reputation**, die dem Moral-Licensing-Problem ausgesetzt ist —
Layer 02s Flussmodell ist immun, `05` wäre es nicht.

**Aber `05` ist nicht der nächste Schritt.** Der ist: vier Menschen erzeugen ihre eigenen
Schlüssel, ein Genesis trägt ihre Namen statt der Seeds `0x11×32` bis `0x14×32`, und jemand geht
die erste Obligation ein, die er tatsächlich erfüllen will. Dafür fehlt eine Anwendungsschicht —
Schlüssel aufbewahren, Claims bauen und verschicken, Empfangenes einlesen —, und die steht in
`06-services.md` und ist nie angefasst worden.

Der Grund steht in `08 §2.2`: eine Aussage wird nicht dadurch überprüfbar, dass sie signiert ist,
sondern dadurch, dass sie mit anderem Signierten **kollidieren kann**. Ein weiterer Spec-Layer
erhöht die Kollisionsdichte um null.
