# Sitzungsstart: Buchführung und Anwendung (MaR)

## Kontext

Wir arbeiten an **Mensch als Republik (MaR)**, einem dezentralen Koordinationsprotokoll.
Python-Referenzimplementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz
(`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

**Arbeitsweise:**
- Design vor Code. Alle Forks und Zahlen stehen fest, **bevor** ein Prompt geschrieben wird.
- Die Spec ist normative Wahrheit. Der committete Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: nur `cbor2` und `cryptography`. Unter `dev` zusätzlich `pytest` und
  `hypothesis`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. **Ein Job pro Zeile, `and` am Zeilenanfang** — nie
  `;`, und **innerhalb einer Pipe steht nie ein `and`**. Merke: `and` hinter einer Pipe prüft den
  Status des letzten Pipeglieds, nicht den des ersten. Das ist nutzbar: eine Pipe auf `tail`
  hält die Kette am Leben, wenn ein Zwischenschritt rot werden **darf** — etwa bei einem
  Experiment, das mit `git checkout --` zurückgenommen werden muss.
- **Spec-Dateien werden als Download geliefert**, nicht als Copy-Block. Der Shell-Block setzt
  voraus, dass die Datei bereits im Repo-Wurzelverzeichnis liegt.
- **Hash-Test als erster Job.** `test (sha256sum datei | cut -d' ' -f1) = <hash>` hält die Kette
  an, wenn die Grundlage eine andere ist. Ein `sha256sum` allein prüft nichts, es druckt nur.
  Bei vollständigen Dateiersetzungen zusätzlich prüfen, dass seit dem Basis-Commit niemand die
  Datei angefasst hat: `test (git log --oneline <basis>..HEAD -- <datei> | wc -l) -eq 0`.
- **Bei neuen Dateien `git add` vor `make check`**, sonst danach.
- `git add` mit expliziten Pfaden, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'` — das gilt auch für Prompt-Dateien im
  Wurzelverzeichnis, `check_specs.py` prüft sie mit.
- **Ein Implementierungslauf endet mit einem Commit auf einem benannten Branch.**
- **Der Vergleichspunkt eines Laufs ist der Prompt-Commit**, nicht der Branchpunkt der
  Spec-Reihe. Ein Abnahmekriterium `git diff --stat <branchpunkt>` ist falsch und wurde in der
  letzten Sitzung zweimal so geschrieben; beide Male hat das Werkzeug es gefangen.

⚠ **Dateien nie manuell editieren.** Spec-Dateien kommen vollständig von Claude. Vor einer
Ersetzung mitten in einer Datei per `sha256sum` abgleichen — **und den vollständigen zu
ersetzenden Absatz als Anker nennen**, nicht die eine Zeile, an der es sich festmachen lässt.

⚠ **Das Projektwissen ist nicht die Quelle für Dateien.** Frag nach dem Repo-Stand. Stimmt der
`sha256sum` einer Projektkopie mit dem Repo überein, darf sie als Grundlage dienen — sonst nicht.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`.

**`main` lag zuletzt auf `99ffa00`** (Merge Budget-Set D135). **Offen: `spec/d135-wirkung`
(`dabb480`) ist noch nicht gemergt** — enthält die Korrektur des Wirkungsabsatzes in D135 und
die Wirkungsprüfung. Das gehört als erstes nach `main`.

Register **D1–D135**. **490 Tests**, dazu **13 Eigenschaftstests** unter `MAR_HYPOTHESIS=voll`.
`make check-all` sind **zwei** pytest-Läufe, also zwei Endzeilen. Die Zahl der von
`check_specs.py` geführten Spec-Dateien ist seit der letzten Sitzung gestiegen (vier neue
Prompt- und Abnahmedateien) — beim Sitzungsstart ablesen, nicht schätzen.

- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, **`read_claim`** (Einlesepfad).
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests. Die Kettenfortführung existiert **einmal**, in `tools/autor.py`.

**Neu in der letzten Sitzung:** D130–D135.

- **D130** Der Rundlauf (`decode` → `encode` → Vergleich) steht auf jeder Schicht im selben `try`
  wie das Dekodieren; was von dort kommt, ist unlesbar. Layer 01 hatte D83 nie nachgezogen.
  Mitbefund: `Anhang B.2` führte dekodierbare indefinite-length unter `MALFORMED_CBOR` statt
  `NON_CANONICAL_ENCODING`. Byte-Vektoren `BV1`–`BV3` in `01 Anhang C.8`.
- **D131** `read_claim` fängt `VerifierError` und nichts sonst; „wirft nie" ist eine bewiesene
  Eigenschaft, kein breiter `except`. Programmierfehler schlagen durch.
- **D132** Eine Tür pro Sprache: fremde Bytes gehen an keiner Stelle durch `claim_from_bytes`.
  **Noch nicht umgesetzt** — das ist Lauf B.
- **D133** `welten()` erzeugt in der Voreinstellung strukturell gültige Claims. Vierte `t_exp`-Lage
  `"grenze"` mit `t_exp = now`. **Noch nicht umgesetzt.**
- **D134** Die Budgetbuchführung des Erzeugers ist gruppenweise (`max` innerhalb `(I, J, N)`,
  Summe darüber). B-4 ist darin aufgegangen. **Noch nicht umgesetzt.**
- **D135** `EQUIVOCATION_FLAGGED` gehört ins Budget-Set. Umgesetzt und gemergt.

## Das Aufnahmekriterium

Aus `08 §3`, vor jedem neuen Mechanismus:

> **Senkt er die Kosten dafür, festzustellen, wer was gesagt hat — oder verteilt er Macht?**
> Senken: Protokoll. Verteilen: Policy. Keines von beidem: Werkzeug.

Die dritte Spalte hat ein eigenes Dach: `werkzeuge.md`. Was dort landet, bekommt keine Zahl im
Dateinamen, keine Golden Anchors und keinen Layer — bleibt aber normativ.

## Prüfregeln

Die fünfzehn aus den Vorsitzungen gelten unverändert: **vor dem Schreiben rechnen**,
**Standprüfung**, **Feldinventur**, **Zugehörigkeitsliste am Datentyp**, **Ausgänge aufzählen**,
**Monotonie stufenweise**, **Abhängigkeitssatz bei Reihenfolgeänderungen**, **Parallelenprüfung**,
**Begründungsprüfung**, **Leserprüfung**, **Geschwisterformel**, **zwei Läufe, eine Variable**,
**Neustart als Annahme**, **Zählregel**, **Literaturprüfung vor der Entscheidung**.

Neu:

16. **Wirkungsprüfung.** Bevor einem Befund eine Folge zugeschrieben wird, wird der falsche Wert
    **bis zu seinem Verbraucher** verfolgt. Bei D135 war `Σ n_budget` ausgerechnet, aber nicht
    weiterverfolgt; der erste Wirkungsabsatz behauptete die Gegenrichtung, weil `derive.py`
    Schritt 5 geflaggte Autoren **autorweit** ausschließt und nicht gruppenweit. Die Wirkung liegt
    nie dort, wo die Zahl entsteht.
17. **Prompt-Dateien sind normativer Text, solange Code auf sie zeigt.** Die Parallelenprüfung
    wurde bisher nur auf Layer-Dateien angewandt. `02a-maxflow-prompt.md` trug Befund und
    Widerlegung **neun Zeilen** voneinander entfernt — eine Aufzählung, die
    `EQUIVOCATION_FLAGGED` wegließ, direkt über dem Satz „ein Vouch verlässt das Budget-Set
    ausschließlich durch `t_exp`". Der Code folgte der Aufzählung. Docstrings, die `02a §…`
    zitieren, machen `02a` zu prüfbarem Text.
18. **Aufzählung gegen Satz.** Steht in einer Spec eine Bedingung als Satz **und** als
    ausgerechnete Aufzählung, gilt der Satz, und die Aufzählung wird als abgeleitet markiert. So
    steht es jetzt in `02a §2.6`. Aufzählungen verlieren beim Wandern still ihren
    Geltungsbereich — D77, D83, D87, D91, D130, D135 sind alle diese Form.

## Was die letzte Sitzung gelehrt hat

**Beide echten Löcher wurden nicht durch Lesen gefunden, sondern durch den Versuch, etwas für eine
Maschine präzise genug zu formulieren.** Der Fehlerkanal in `structural_check` fiel auf, als ein
Testvektor gebraucht wurde und die Frage „welchen Code erwarte ich hier eigentlich" die Tabelle aus
`Anhang B.2` zum ersten Mal gegen einen konkreten Byte-String hielt. Der Budget-Reset fiel auf, als
für einen **Testgenerator** die richtige Verankerung gesucht wurde. Dieselbe Bewegung wie D118.

**Ein Befund kann auf dem Weg zu etwas ganz anderem liegen.** D135 ist ein Loch im Protokoll, seit
Layer 02 gebaut wurde, und es stand im Weg zu einer Reparatur an einem Testhilfsmittel.

**Das Werkzeug hat dreimal richtig blockiert:** die widersprüchliche Treue-Formulierung nicht mit
`assume` weggefiltert, sondern gemeldet; `except Exception` in Schritt 2a als zweite Fundstelle
benannt; ein Byte-Escape in einer Prompt-Datei gegen `check_specs` gefangen. Alle drei waren Fehler des
Supervisors.

**Zwei Abnahmedefekte, beide in Tests, beide aus der Parallelenprüfung ableitbar** — eine
Parametrisierung, die still auf null fallen konnte, und ein Vektor, der nur an seinen Reject
gebunden war, nicht an seine Bedeutung.

## Offen

- **Lauf an `welten.py`: D133 und D134.** Der nächste Schritt. Details unten.
- **Lauf B / D132** — unsigniertes Bündelformat, `store_laden` und `zustellen` über `read_claim`,
  `claim_id` nachgerechnet statt Dateiname geglaubt. `read_claim` hat heute **keinen**
  Produktivaufrufer; `tools/sim/welt.py:86` ist der einzige Verstoß gegen D132 im Produktivcode.
- **Ausgang 5 / Selbst-Equivocation.** Entschieden: **nicht** im Einlesepfad, kein zwölfter
  Reject-Code — Layer 01 führt `equivocation-flagged` als Zustand. Offen bleibt der Ort: eine
  Diagnoseoperation über den geladenen Store, **ohne** den `Ausgang`-Port zu verbreitern (D127).
- **Der Kopplungstest in `test_read_claim.py` hat einen praktisch toten Ablehnungszweig** —
  2 von 534 Claims. Die Aussage trägt faktisch die Vektorparametrisierung, nicht der
  Eigenschaftstest. Kein Auftrag, aber nicht für die Absicherung halten, die er nicht leistet.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut.
- **`00a-rotate-key`.** D125 und D126 stehen; offen bleiben der Effektivpunkt der
  Governance-Rotation (uhrfrei formulieren) und die Schwellenfrage (`00 §4`).
- **`03-prompt.md`-Verweise im Paketcode** — vier Stellen unter `mensch_als_republik/profiles/`
  und `policy.py`. Nach Prüfregel 17 ist das doppelt relevant: solange sie zeigen, ist
  `03-prompt.md` prüfbarer Text.
- **Welche Prompt-Dateien zitiert der Code sonst noch?** Ein Grep-Durchgang über Docstrings nach
  `-prompt.md` und `02a §`, `fuzz-prompt.md`, `sim-prompt.md`. `fuzz-prompt.md` und
  `sim-prompt.md` sind **gelöscht**, werden aber in Docstrings noch zitiert.
- **Gleichstand bei `kante_claim_id`** — `test_groups.py:196` und `test_pagerank_groups.py:22`
  tragen den Fall, der Bruch über `sorted(...)[0]` ist von nichts geprüft.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** prüfen eine schwächere Aussage als sie
  scheinen (D117).
- **`02d-purpose`** (D56), **VR-04.1** (D26), **Zeugenquorum für Fristen** (D100).
- **`04 §7.2` Föderation** nicht durchgerechnet.
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **Aufräumen im Repo** — Branches mit stehengebliebenen `voraus`-Zählern;
  `sitzungsstart-einlesepfad.md` ist durch diese Datei abgelöst. Vor jedem Löschen prüfen, ob Code
  oder Spec die Datei referenziert (Prüfregel 17).

## Der nächste Schritt

**Lauf an `tests/property/welten.py`: D133 und D134 gemeinsam**, weil beides Buchführung desselben
Erzeugers ist und zwei Läufe an derselben Datei die Anker zweimal bewegen würden.

Drei Punkte:

1. **`t_exp` gegen das nächste `t`** (D133). `_Signer.claim()` zählt `_t` **innerhalb** der
   Methode hoch; der Aufrufer kennt das `t` nicht und kann deshalb keine Untergrenze setzen. Die
   Reparatur ist, das nächste `t` sichtbar zu machen — nicht, eine feste Untergrenze zu raten.
   `tools/autor.py` bleibt außen vor: `Autor` kennt `t` gar nicht, es ist Parameter von
   `signieren`/`gabeln`.
2. **Vierte Lage `"grenze"`** mit `t_exp = now`, Gewichtung `4 : 4 : 1 : 1`. Schließt nebenbei den
   Grenzwertvektor `now = t_exp`, der seit D119 offen ist — er war ungebaut, weil der Erzeuger ihn
   nicht ziehen konnte.
3. **Gruppenweise Budgetbuchführung** (D134). `remaining` muss `Σ_J max n` je Gruppe führen, nicht
   `Σ n` je Claim. Zwei Symptome derselben Ursache: der Zwilling und die Wiederholung derselben
   `(Autor, Empfänger)` über Schleifendurchläufe. Die Ablaufregel erbt die Form — Budget wird erst
   frei, wenn **alle** Mitglieder der Gruppe abgelaufen sind.

**Vor dem Prompt zu klären:** die Ziehungsreihenfolge. Die Gruppenrechnung braucht `t_exp`, bevor
sie `n` beschränken kann; heute wird `n` **vor** `lage` gezogen. Das Umdrehen ändert den
Ziehungsstrom von hypothesis und damit den erzeugten Weltkorpus. Golden Anchors hängen nicht daran
(`tests/trust/test_anchors.py` und die PageRank-Anker fahren eigene Fixtures, `tp02`/`pr02`) —
aber eine bisher grüne Eigenschaft kann auf neu erreichbaren Welten rot werden. **Das wäre ein
Befund, kein Grund zum Zurückdrehen**, und muss so im Prompt stehen.

Der Test zu D134 darf die Buchführung **nicht nachbauen** — sonst machen Erzeuger und Prüfung
denselben Fehler. Er rechnet mit Layer 02s eigener Gruppenbildung:
`build_groups(claims, classifications, scope, D, now)` liefert `Group.n_budget`;
`OVERCOMMITTED_AUTHOR` entsteht erst in `derive.py` Schritt 4 mit dem **Autor-Pubkey** als Subjekt.
Wirkungsprüfung: beides behaupten, Summe **und** Finding.

**Danach Lauf B, dann die Anwendung.** Vier Menschen erzeugen eigene Schlüssel, ein Genesis trägt
ihre Namen statt der Seeds `0x11×32` ff., und jemand geht die erste Obligation ein, die er erfüllen
will. Der Grund steht in `08 §2.2` — eine Aussage wird nicht dadurch überprüfbar, dass sie signiert
ist, sondern dadurch, dass sie mit anderem Signierten **kollidieren kann**. Ein weiterer Spec-Layer
erhöht die Kollisionsdichte um null.

Erst danach `05`. Dessen zwei bekannte Baustellen bleiben: **Über-Commitment als Stufe-3-Auslöser**
(D40, mit D118 scharf) und die **Beta-Reputation** mit dem Moral-Licensing-Problem, gegen das
Layer 02s Flussmodell immun ist und `05` es nicht wäre.
