# Sitzungsstart: Kollisionsdichte (MaR)

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
- Die Spec ist normative Wahrheit. Der committete Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt — auch dir
  selbst aus der vorigen Runde.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: nur `cbor2` und `cryptography`. Unter `dev` zusätzlich `pytest` und
  `hypothesis`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. **Ein Job pro Zeile, `and` am Zeilenanfang** — nie
  `;`, und **innerhalb einer Pipe steht nie ein `and`**. `and` hinter einer Pipe prüft den Status
  des letzten Pipeglieds. Das ist nutzbar: eine Pipe auf `tail` hält die Kette am Leben, wenn ein
  Zwischenschritt rot werden **darf**. Muss ein Schritt rot werden dürfen und der Rückweg
  trotzdem laufen, wird die Kette bewusst unterbrochen — mit Begründung im Fließtext.
- **Spec-Dateien werden als Download geliefert**, nicht als Copy-Block. **Werkzeug-Prompts als
  Copy-Box** oder, wenn sie lang sind, ebenfalls als Datei.
- **Hash-Test als erster Job.** `test (sha256sum datei | cut -d' ' -f1) = <hash>` hält die Kette
  an. Ein `sha256sum` allein prüft nichts, es druckt nur. Bei Ersetzungen mitten in einer Datei
  gilt zusätzlich: **den vollständigen zu ersetzenden Absatz als Anker nennen**, und der Splice
  behauptet per `assert`, dass der Anker genau einmal vorkommt.
- **Bei neuen Dateien `git add` vor `make check`**, sonst danach. `git add` mit expliziten Pfaden,
  nie `-A` — besonders nicht bei Spec-Commits während eines offenen Laufs.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`; `check_specs.py` prüft Prompt-Dateien im
  Wurzelverzeichnis mit.
- **Der Vergleichspunkt eines Laufs ist der Prompt-Commit**, nicht der Branchpunkt der Spec-Reihe.
- Claude darf `sha256sum` einer Projektkopie selbst rechnen. Stimmt sie mit dem Repo, wird sie
  gelesen statt angefordert.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`.

**`main` liegt auf `dc844c5`**, gepusht, `origin/main..main` leer. Keine offenen Branches, keine
ungemergten Läufe.

**493 Tests**, dazu **14 Eigenschaftstests** unter `MAR_HYPOTHESIS=voll`. `make check-all` sind
zwei pytest-Läufe, also zwei Endzeilen. **51 Spec-Dateien**, Register **D1–D138**. Die Zahlen beim
Sitzungsstart ablesen, nicht schätzen.

- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim` (Einlesepfad).
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests. Die Kettenfortführung existiert **einmal**, in `tools/autor.py`.

**Neu in der letzten Sitzung:** D136, D137, D138, dazu Nachträge an D134 und D137.

- **D134 Nachtrag** — ein dritter Symptompfad kehrt die Fehlerrichtung um. Der Satz
  „`erlaube_ueberzeichnung = False` hält, was es verspricht" war falsch: bei abgelaufenem Ersten
  und lebendem Zwilling zahlte die Gruppe `n2`, während der Erzeuger null buchte. Die
  Buchführung ist seither über **lebende Mitglieder** formuliert, nicht über den ersten Claim.
- **D136** — gelöschte Prompt-Dateien werden umgelenkt, nicht wiederhergestellt. Achtzehn
  Docstring-Zitate zeigten auf `fuzz-prompt.md` und `sim-prompt.md`; Ziel ist `werkzeuge.md`.
- **D137** — `find` bekommt `max_examples=200` und `derandomize=True`, unabhängig vom Profil. Eine
  Existenzbehauptung handelt keine Abdeckung.
- **D138** — Zuschnitt von Lauf B korrigiert (kein Bündelformat, das ist D121), `read_claim` ohne
  Store im Einlesepfad, `hat_claim` antwortet aus dem Inhalt.

**Erledigt und aus der Offen-Liste raus:** D132 (Lauf B), D133, D134, das `welten.py`-Loch, die
Verweise auf gelöschte Prompt-Dateien, der Grenzwertvektor `now = t_exp` aus D119.

## Das Aufnahmekriterium

Aus `08 §3`, vor jedem neuen Mechanismus:

> **Senkt er die Kosten dafür, festzustellen, wer was gesagt hat — oder verteilt er Macht?**
> Senken: Protokoll. Verteilen: Policy. Keines von beidem: Werkzeug.

Die dritte Spalte hat ein eigenes Dach: `werkzeuge.md`. Was dort landet, bekommt keine Zahl im
Dateinamen, keine Golden Anchors und keinen Layer — bleibt aber normativ.

## Prüfregeln

Die achtzehn aus den Vorsitzungen gelten unverändert: **vor dem Schreiben rechnen**,
**Standprüfung**, **Feldinventur**, **Zugehörigkeitsliste am Datentyp**, **Ausgänge aufzählen**,
**Monotonie stufenweise**, **Abhängigkeitssatz bei Reihenfolgeänderungen**, **Parallelenprüfung**,
**Begründungsprüfung**, **Leserprüfung**, **Geschwisterformel**, **zwei Läufe, eine Variable**,
**Neustart als Annahme**, **Zählregel**, **Literaturprüfung vor der Entscheidung**,
**Wirkungsprüfung**, **Prompt-Dateien sind normativer Text, solange Code auf sie zeigt**,
**Aufzählung gegen Satz**.

Neu:

19. **Kalte Messung.** Ein grüner Testlauf auf der Arbeitskopie ist keine Aussage über den
    Commit. Zustand außerhalb von git — `.hypothesis/`, `__pycache__`, warme Caches — wird vor
    jeder Behauptung über `main` gelöscht. `make check-all` führt `check_tree.py` und hat damit
    ein Tor gegen vergessene **Dateien**; gegen vergessene **Zustände** gibt es keines. Genau
    darin lag D137: zwei Existenzbehauptungen standen zwei Sitzungen lang auf einem gitignorierten
    Cache, und `main` war auf einem frischen Klon rot.

## Was die letzte Sitzung gelehrt hat

**Die Form „Satz und Aufzählung" ist jetzt achtmal aufgetreten** — D77, D83, D87, D91, D130, D134,
D135 und der Zuschnitt-Absatz in D132. Prüfregel 18 fängt sie, aber offenbar erst beim Hinsehen,
nie beim Vorbeigehen. Wo eine Spec eine Bedingung zweimal führt, gilt der Satz.

**Ein Befund liegt auf dem Weg zu etwas anderem.** D137 ist ein zwei Sitzungen alter Defekt,
gefunden beim Abnehmen eines Laufs, der ihn beiläufig repariert hatte. Das Werkzeug meldete ihn
als neue Fragilität seines eigenen Laufs; die Gegenprobe kehrte die Zuordnung um — kalt bei
`4da3304` grün, kalt bei `40ee7a5` rot. Der Bericht war ehrlich, die Zuordnung falsch. Genau
deshalb ist der Bericht nie die Abnahme.

**Der Supervisor hat dreimal Ungemessenes behauptet** und wurde jedes Mal von der nächsten
Messung widerlegt: `derandomize=True` schalte die Beispieldatenbank ab (falsch), Behauptung 3 im
Türtest sei die eigentliche Aussage (falsch, sie war vorher grün), P-3a sei vorher schon fragil
gewesen (richtig, aber ungeprüft behauptet). Keine neue Regel nötig — das ist Regel 12, zwei
Läufe eine Variable, angewandt auf den eigenen letzten Zug.

**Das Werkzeug hat zweimal richtig gemeldet statt still zu reparieren:** die falsch gewordene
Zeile in `werkzeuge.md §3.1`, und dass die Rücknahmeprobe zu Kriterium 2 nur die erste von drei
Behauptungen rot macht. Das zweite hat einen Fehler des Supervisors aufgedeckt.

**Die Rücknahmeprobe deckt nur das ab, wofür sie verlangt wird.** Ein Prompt mit zwei Änderungen
braucht zwei Rücknahmeproben. Fehlt eine, kann ein Test grün sein, weil er nie etwas anderes
gesehen hat.

## Offen

- **Die Anwendung.** Der nächste Schritt, Details unten.
- **`make check` steigt in `.venv` ab:** `find . -name __pycache__ -type d -exec rm -rf {} +` ohne
  `-not -path "./.venv/*"`. Unter `-j1` nur langsam, parallel eine Kollision, im schlechten Fall
  räumt es im virtualenv auf.
- **Ausgang 5 / Selbst-Equivocation.** Entschieden: **nicht** im Einlesepfad, kein zwölfter
  Reject-Code — Layer 01 führt `equivocation-flagged` als Zustand. Offen bleibt der Ort: eine
  Diagnoseoperation über den geladenen Store, **ohne** den `Ausgang`-Port zu verbreitern (D127).
- **`FOREIGN_LIFECYCLE` hat keinen Produktivträger mehr** (D138, bewusst). Als Zustandsprüfung in
  `index.py` doppelt vorhanden. Steht dort, damit es niemand für einen Bug hält.
- **Meldung übersprungener Claims aus `store_laden`** — von D138 ausdrücklich zurückgestellt. Wenn
  die Stille beim Debuggen teuer wird, ist das ein eigener Fork mit eigener Begründung.
- **Der Kopplungstest in `test_read_claim.py`** hat seit D133 einen **leeren** Ablehnungszweig,
  nicht mehr nur einen fast leeren. Die Aussage trägt die Vektorparametrisierung.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut.
- **`00a-rotate-key`.** D125 und D126 stehen; offen bleiben der Effektivpunkt der
  Governance-Rotation (uhrfrei formulieren) und die Schwellenfrage (`00 §4`).
- **`03-prompt.md`-Verweise im Paketcode** — vier Stellen unter `mensch_als_republik/profiles/`
  und `policy.py`. Nach Prüfregel 17 doppelt relevant.
- **Gleichstand bei `kante_claim_id`** — der Bruch über `sorted(...)[0]` ist von nichts geprüft.
  Seit D134 ist der Fall generativ erreichbar geworden (Wiederholung derselben `(I, J)` kostet
  kein zusätzliches Budget mehr), aber kein Test behauptet ihn.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** prüfen eine schwächere Aussage als sie
  scheinen (D117).
- **`02d-purpose`** (D56), **VR-04.1** (D26), **Zeugenquorum für Fristen** (D100).
- **`04 §7.2` Föderation** nicht durchgerechnet.
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **Aufräumen im Repo** — `sitzungsstart-einlesepfad.md` und `sitzungsstart-buchfuehrung.md` sind
  durch diese Datei abgelöst. Vor jedem Löschen prüfen, ob Code oder Spec sie referenziert
  (Prüfregel 17).
- **Layer 05.** Zwei bekannte Baustellen: Über-Commitment als Stufe-3-Auslöser (D40, mit D118
  scharf) und die Beta-Reputation mit dem Moral-Licensing-Problem, gegen das Layer 02s Flussmodell
  immun ist und `05` es nicht wäre.

## Der nächste Schritt: vier Menschen, ein Genesis, eine Obligation

`08 §2.2` steht seit drei Sitzungen als Begründung da: **eine Aussage wird nicht dadurch
überprüfbar, dass sie signiert ist, sondern dadurch, dass sie mit anderem Signierten kollidieren
kann.** Ein weiterer Spec-Layer erhöht die Kollisionsdichte um null.

Die Voraussetzung ist seit `dc844c5` weg. `tools/sim/welt.py::Teilnehmer` **ist** bereits die
Anwendung: eigenes Verzeichnis, `key.bin`, Inbox, eigene Uhr, und eine Tür, die fremde Bytes über
`read_claim` prüft, statt Dateinamen zu glauben. Vier Menschen mit echten Seeds sind vier
`Teilnehmer`. Sitzen sie auf getrennten Rechnern, ersetzt Dateikopie das `zustellen` — und die
Dateinamen kommen zum ersten Mal wirklich von Fremden.

**Das ist kein Lauf im bisherigen Sinn.** Es gibt keine Golden Numbers zu rechnen und zunächst
keinen Prompt zu schreiben. Drei Fragen sind vor allem anderen zu klären, und sie sind an den
Operator gerichtet, nicht an die Spec:

1. **Sind die vier real?** Vier Menschen, die zustimmen, oder vier Rollen auf einem Rechner? Das
   entscheidet, ob Schlüsselverwahrung und Zustellung echte Probleme sind oder Kulisse.
2. **Ein Rechner oder vier?** Auf einem bleibt `zustellen` das Transportmittel. Auf vieren wird
   der Transport zur ersten offenen Frage — und `00a-rotate-key` plus der Sicherungsblob (D120)
   rücken von „beschrieben und ungebaut" nach „gebraucht".
3. **Hat die erste Obligation einen Gegenstand?** Jemand geht sie ein, weil er sie erfüllen will —
   nicht als Testvektor. Ohne konkreten Gegenstand entsteht wieder eine Simulation, nur mit
   anderen Seeds.

Erst danach steht fest, ob der nächste Schritt ein Genesis mit vier Namen ist, ein
Schlüsselverwahrungs-Werkzeug oder ein Prädikat, das es noch nicht gibt.
