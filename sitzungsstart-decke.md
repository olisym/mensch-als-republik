# Sitzungsstart: Knotendecke (MaR)

## Kontext

Wir arbeiten an **Mensch als Republik (MaR)**, einem dezentralen Koordinationsprotokoll.
Python-Referenzimplementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz
(`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise — die Kurzform

Die dauerhafte Anweisung gilt. Was in der Praxis am häufigsten gebraucht wird:

- **Design vor Code.** Alle Forks und Zahlen stehen fest, **bevor** ein Prompt geschrieben wird.
  **Modulcode vor Prompt** — alle betroffenen Quellen lesen, bevor ein Prompt entsteht.
- **Der Bericht des Werkzeugs ist nie die Abnahme.** Geprüft wird der Diff.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt — auch dir
  selbst aus der vorigen Runde. In dieser Sitzung war das dreimal nötig und zweimal richtig.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: nur `cbor2` und `cryptography`. Unter `dev` zusätzlich `pytest` und
  `hypothesis`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. **Ein Job pro Zeile, `and` am Zeilenanfang** — nie
  `;`, und **innerhalb einer Pipe steht nie ein `and`**. Eine Pipe auf `tail` hält die Kette am
  Leben, wenn ein Zwischenschritt rot werden **darf**. `grep -c` mit Ergebnis null gibt Status 1
  und bricht die Kette — das ist nutzbar, muss aber angesagt werden.
- **Spec-Dateien werden als Download geliefert**, nicht als Copy-Block. **Werkzeug-Prompts als
  Copy-Box** oder, wenn sie lang sind, ebenfalls als Datei. Splices kommen als Skript mit
  `assert`, dass der Anker genau einmal vorkommt, und werden vorher trocken gegen die
  Projektkopie gelaufen.
- **Hash-Test als erster Job.** `test (sha256sum datei | cut -d' ' -f1) = <hash>` hält die Kette
  an. Ein `sha256sum` allein prüft nichts, es druckt nur.
- **Bei neuen Dateien `git add` vor `make check`**, sonst danach. `git add` mit expliziten
  Pfaden, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`; `check_specs.py` prüft Prompt- und
  Abnahme-Dateien im Wurzelverzeichnis mit.
- **Der Vergleichspunkt eines Laufs ist der Prompt-Commit**, nicht der Branchpunkt der
  Spec-Reihe. In dieser Sitzung stand einmal die falsche Basis im Abnahmekriterium; das Werkzeug
  hat gemeldet statt zu rebasen.
- Claude darf `sha256sum` einer Projektkopie selbst rechnen. Stimmt sie mit dem Repo, wird sie
  gelesen statt angefordert. Das hat in dieser Sitzung mehrere Züge gespart.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`.

**`main` liegt auf `95e0b4d`**, gepusht. Keine offenen Branches, keine ungemergten Läufe.

**496 Tests**, dazu **14 Eigenschaftstests** unter `MAR_HYPOTHESIS=voll`. **54 Spec-Dateien**,
Register **D1–D141**. Die Zahlen beim Sitzungsstart ablesen, nicht schätzen.

- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim` (Einlesepfad).
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests.

**Neu in der letzten Sitzung:** D139, D140, D141, dazu der erste Charakterisierungstest.

- **D139** — `02 §4` schloss mit der Behauptung, eine seed-ferne Angriffskante sei „ohnehin
  billig, weil `C(h)` mit der Distanz fällt: doppelter Schutz". Der Satz behandelt `d(s,h)` als
  Eigenschaft des ehrlichen Knotens. Das ist es nicht — `d` ist BFS über dem aktuellen `E⁺`,
  und der Angreifer gestaltet `E⁺` mit. Satz gestrichen, Warnabsatz eingefügt.
- **D140** — `02 §5` beschrieb `P` als spaltenstochastisch über `Σw` normalisiert, obwohl **D45
  das aufgehoben hatte**. Zwei Jahre lang. Kein Test konnte rot werden, weil die Implementierung
  K9 folgt und nur die Spec falsch war. Nachgezogen. Nebenbei beantwortet: die Relaxation ist
  gegen den Distanzkauf immun, aber wegen Massenerhaltung, nicht weil sie keine Kapazität kennt
  — `C(x)` geht sehr wohl ein, als `E⁺`-Filter (K13).
- **D141** — die Zahlen in D139 waren falsch. `Σ C(h)` ist eine **Schranke**, kein Ertrag; die
  dort beschriebene Konstruktion hätte gar keinen Fluss getragen. Gemessen gilt: `p` bei `d = 1`
  bürgt mit `n = 2` von Budget `16`, die Kante trägt `cap = 1`, und `maxflow` springt von `1` auf
  `4`. **Gekauft wird nicht Fluss, sondern das Entfernen einer Decke.** Drei der vier Einheiten
  sind ehrlicher Fluss, der vorher an `C(h) = 1` abgeschnitten wurde.
- **`tests/trust/test_distanzkauf.py`** — drei Fälle, alle Erwartungen aus `capacity(PARAMS, d)`
  abgeleitet, nichts getippt. Fall 3 isoliert den `E⁺`-Filter: eine Einheit unter der Schwelle
  ist wirkungslos, genau auf der Schwelle vervierfacht dieselbe Kante den Fluss.

**Die Anwendung ist ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das: die Kraft wächst mit dem Anteil des
tatsächlichen Zusammenlebens, der als verknüpfte Claims ausgedrückt wird. Ein Paket von einem
Fremden ist das nicht, vier Rollen auf einem Rechner auch nicht. Warten ist ein zulässiger
Zustand; so tun als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine
Aufforderung, in der nächsten Sitzung eine Gelegenheit zu erfinden.

## Das Aufnahmekriterium

Aus `08 §3`, vor jedem neuen Mechanismus:

> **Senkt er die Kosten dafür, festzustellen, wer was gesagt hat — oder verteilt er Macht?**
> Senken: Protokoll. Verteilen: Policy. Keines von beidem: Werkzeug.

## Prüfregeln

Die neunzehn aus den Vorsitzungen gelten unverändert. Neu:

20. **Kostenaussage braucht Kostenmodell.** Ein Satz, der etwas „billig", „teuer" oder „ohnehin
    unattraktiv" nennt, ist eine Aussage über Angriffskosten. Steht in der Spec kein
    Kostenmodell, das ihn trägt, fällt der Satz — auch und gerade dann, wenn der Satz daneben
    bewiesen ist. Ein bewiesener Nachbar macht eine unbelegte Behauptung nicht wahr, er macht sie
    nur schwerer sichtbar.

**Konvention aus D140:** Hebt ein Registereintrag einen älteren auf, weist der Titel das aus und
der Text nennt **Datei und Abschnitt**, die nachzuziehen sind. Ohne diese Angabe ist die
Aufhebung im Register vollständig und in der Spec unsichtbar.

## Was die letzte Sitzung gelehrt hat

**Die Literaturprüfung hat die Runde entschieden, nicht die Spec.** Der Advogato-Strang liefert
beides: Levien betrieb die Metrik jahrelang mit echten Nutzern und berichtet, entscheidend sei
die Deckung zwischen den Annahmen der abstrakten Berechnung und der realen Implementierung.
Ruderman fand den eigentlichen Defekt beim **Nachlesen des Beweises**, nicht im Feldbetrieb.
Daraus die Reihenfolge-Lehre: **Feldbetrieb findet Implementierungsränder, Nachrechnen findet
Beweislücken.** Bei SSB waren es Replikationslecks, eine Kanonisierung ohne deterministische
Schlüsselordnung und ein einzelnes langlebiges Signaturschlüsselpaar — zwei davon sind in MaR
strukturell geschlossen, das dritte ist die offene Schlüsselrotation.

**Der Supervisor hat vier eigene Behauptungen kassiert.** Der quadratische Ertrag (falsch,
Schranke mit Ertrag verwechselt), „`§5` kennt keinen Distanzterm" (falsch, `C` ist `E⁺`-Filter),
zweimal eine geschätzte Zeilenzahl statt einer gerechneten. Die ersten beiden fielen erst, als
die Behauptung für eine Maschine präzise genug werden musste — das **D118-Muster**, jetzt zum
wiederholten Mal. Die letzten beiden sind Prüfregel 1 gegen den eigenen Text.

**Ein Testgraph ist ein Beweisversuch.** Die falsche Zahl in D139 hatte einen Registereintrag,
einen Warnblock in der Layer-Datei und eine Runde Prosa überstanden. Sie fiel beim Versuch, die
Topologie zu bauen — weil aller Fluss durch `p` gemusst hätte und `p` deckelt.

**Der erste Lauf behauptete weniger, als er schien.** `d_h == d_p + 1` ist eine Aussage über die
Lage von `h` relativ zu `p`, nicht darüber, dass `h` sich bewegt hat. Nachgetragen wurden
`d_h < D_H_OHNE` und `d_p < D_H_OHNE - 1`. Die Form ist bekannt: ein Test kann grün sein, weil er
nie etwas anderes gesehen hat.

**Das Werkzeug hat dreimal richtig gemeldet statt still zu reparieren** — die falsche Basis im
Abnahmekriterium, das fehlende Re-Export von `derive`, und dass Rücknahmeprobe 2 auch Fall 3 rot
färbt. Zwei davon waren Fehler im Prompt.

## Der nächste Schritt: eine Decke, die niemand kaufen kann

Der Fork aus D140/D141, jetzt mit einer Messlatte:

> **Gibt es eine harte Knotendecke, die nicht über den Graphen gekauft werden kann?**

Der Trade-off steht sauber. Der Min-Cut-Beweis in `§4` braucht eine harte Obergrenze pro Knoten;
die Obergrenze braucht eine Positionsgröße; jede Positionsgröße über dem Vouch-Graphen ist mit
Vouches beeinflussbar. `§5` ist unverwundbar, weil es nichts verspricht — keine harte Schranke,
für Gates verboten. **Die Verwundbarkeit von `§4` ist der Preis der harten Schranke**, kein
Fehler in der Wahl der Sicht.

Zuerst eine Literaturrunde (Prüfregel 15), bevor irgendetwas entschieden wird. Die
SybilLimit-Linie arbeitet mit Random Routes statt mit Distanz; zu prüfen ist, was dort als
Kostenmodell für verwirrte ehrliche Knoten angesetzt wird und ob sich eine Decke daraus
konstruieren lässt, die MaRs Constraints erfüllt: kein globaler Zustand, keine globalen
Identifikatoren, exakte Ganzzahlarithmetik, kein `float`.

**Die Frage hat soziale Konsequenz** — es geht darum, wessen Position kaufbar ist. Die
Entscheidung liegt beim Operator, nicht beim Supervisor. Fällt sie gegen einen Mechanismus, ist
das ein Registereintrag mit Begründung, kein Versäumnis: `test_distanzkauf.py` hält den Preis
dann sichtbar fest.

## Offen

- **Der Fork oben.** Nächster Schritt.
- **Skalierung des Distanzkaufs** über `p`s Budget — `p` kann `C(p)` solche Kanten legen, ohne
  dass der eigene Durchsatz je gebraucht wird. Gerechnet plausibel, **nicht gemessen**, steht
  deshalb in keiner Spec-Datei.
- **`disjoint_paths` bewegt sich nicht** (bleibt `1` in beiden Fällen). Ob das trägt oder ein
  Artefakt der Topologie ist, ist nicht gemessen.
- **Die Anwendung.** Wartet auf Menschen. Siehe oben.
- **`make check` steigt in `.venv` ab:** `find . -name __pycache__ -type d -exec rm -rf {} +`
  ohne `-not -path "./.venv/*"`. Unter `-j1` nur langsam, parallel eine Kollision.
- **Ausgang 5 / Selbst-Equivocation.** Entschieden: nicht im Einlesepfad, kein zwölfter
  Reject-Code. Offen bleibt der Ort — eine Diagnoseoperation über den geladenen Store, ohne den
  `Ausgang`-Port zu verbreitern (D127).
- **`FOREIGN_LIFECYCLE` hat keinen Produktivträger mehr** (D138, bewusst).
- **Meldung übersprungener Claims aus `store_laden`** — von D138 zurückgestellt.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut.
- **`00a-rotate-key`.** D125 und D126 stehen; offen bleiben der Effektivpunkt der
  Governance-Rotation (uhrfrei formulieren) und die Schwellenfrage (`00 §4`).
- **`03-prompt.md`-Verweise im Paketcode** — vier Stellen unter `mensch_als_republik/profiles/`
  und `policy.py`. Nach Prüfregel 17 doppelt relevant.
- **Gleichstand bei `kante_claim_id`** — der Bruch über `sorted(...)[0]` ist von nichts geprüft.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** prüfen eine schwächere Aussage als sie
  scheinen (D117).
- **`02d-purpose`** (D56), **VR-04.1** (D26), **Zeugenquorum für Fristen** (D100).
- **`04 §7.2` Föderation** nicht durchgerechnet.
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **Aufräumen im Repo.** Es gibt jetzt **sieben** `sitzungsstart-*.md`; sechs davon sind
  abgelöst. Vor jedem Löschen prüfen, ob Code oder Spec sie referenziert (Prüfregel 17). Der
  Stapel wächst schneller als die Layer.
- **Layer 05.** Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf) und die
  Beta-Reputation mit dem Moral-Licensing-Problem, gegen das Layer 02s Flussmodell immun ist und
  `05` es nicht wäre.
