# Sitzungsstart: 00e (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 28, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu ist **28** (aus D179). Sie steht neben **22**, **26** und **27**: vier Regeln, die
sich an den Supervisor richten, keine an das Werkzeug. Das ist kein Zufall.

Was in der Praxis am häufigsten gebraucht wird:

- **Design vor Code.** Alle Forks und Zahlen stehen fest, bevor ein Prompt geschrieben wird.
  **Modulcode vor Prompt** — alle betroffenen Quellen lesen, bevor ein Prompt entsteht.
- **Der Bericht des Werkzeugs ist nie die Abnahme.** Geprüft wird der Diff. In dieser Sitzung war
  der Bericht viermal zutreffend, und viermal hat erst das Lesen des Diffs gezeigt, was fehlte.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt — auch dir
  selbst aus der vorigen Runde. Diese Sitzung hat einen eigenen Fork als gegenstandslos
  zurückgenommen und einen eigenen Reparaturvorschlag als Schönreparatur verworfen.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: nur `cbor2` und `cryptography`, unter `dev` `pytest` und `hypothesis`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**. Eine Ausnahme ist nützlich:
  `sha256sum -c` am Ende einer Pipe druckt `FAILED` je Datei, dort ist der Statusverlust
  unschädlich.
- **Spec-Dateien als Download**, nicht als Copy-Block. Werkzeug-Prompts als Copy-Box oder, wenn
  lang, als Datei im Wurzelverzeichnis.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet -- <datei>`.
- Bei neuen Dateien `git add` **vor** `make check` / `check_specs.py`, sonst danach. `git add`
  mit expliziten Pfaden, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. Zeilen brechen bei 100 Zeichen; Tabellenzeilen
  sind ausgenommen. `check_specs.py` prüft Escapes, Steuerzeichen, D-Nummern und hängende
  D-Verweise — **keine Zeilenlängen**. Die 100 sind Konvention, kein Tor.
- **Der Vergleichspunkt eines Laufs ist der Prompt-Commit.** Ein Prompt kann den Commit, der ihn
  enthält, nicht nennen — er nennt den Branchpunkt (`git merge-base main <branch>`). Spec-Nachzug
  gehört **vor** den Lauf auf `main`. Läuft ein Branch bereits, wird `main` in ihn gemergt, damit
  das Werkzeug die Verweise lesen kann, auf die der Prompt zeigt.
- Claude darf `sha256sum` einer Projektkopie selbst rechnen und sie dann lesen statt anfordern.
  **Prüfregel 26:** dieser Abgleich gilt für den Commit, an dem er gemacht wurde.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie mit selbstgebautem `grep`.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch. Diese
  Sitzung hat so drei Zeilen als zu lang gemeldet, die es nicht waren.
- Vor jeder Zahl in einem Prompt: **ist sie gemessen, und ist die Messung noch gültig?**
- **Prüfregel 27:** vor jedem Verweis in einem Prompt die Stelle **aufschlagen**. Auch wenn er
  aus dem eigenen Register stammt. Zweimal in dieser Sitzung gebrochen; einmal stand die Antwort
  wörtlich im Register (D107), einmal in der Spec (`04 §3.5`).
- **Prüfregel 28:** ein Abnahmekriterium behauptet einen **Weltzustand**. Vor dem Prompt den
  Zustand konstruieren, nicht nur die Erwartung prüfen.
- **Eine Zusage ist keine Messung.** Ein „ja" auf einen Shell-Block heißt Zustimmung, nicht
  Vollzug. Diese Sitzung hat einen Push zwei Züge lang für gelaufen gehalten, der nicht lief; der
  Commit-Bereich im nächsten Push hat es verraten.
- Eine Auffälligkeit an einer Stelle ist erst ein Befund, wenn die Nachbarstellen dieselbe
  Erwartung erfüllen (Prüfregel 8).

### Splices

Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher trocken gegen eine
Kopie gelaufen. Diese Sitzung hat drei Splice-Läufe mit zusammen elf Ankern gefahren, alle im
ersten Zug grün.

- **Jeder Splice läuft trocken gegen den Stand nach dem vorigen**, nicht gegen die Projektkopie.
- **Ein anhängender Splice braucht eine eigene Negativprüfung.** Ersetzt ein Anker sich selbst
  plus einen neuen Absatz, kommt der Ankertext im Ergebnis weiterhin vor, und „genau ein Treffer"
  ist kein Wiederholungsschutz mehr. Diese Sitzung hat es an zwei Skripten gefunden — beide waren
  nur deshalb sicher, weil die Registerprüfung zufällig vorher bremste. Jeder Anker bekommt eine
  Marke, die nach dem Einfügen im Text steht.
- **Ans Register wird über eine Regex-Prüfung angehängt**: der letzte Registerkopf muss der
  erwartete sein. `### D5a` und `### D16 / D22` fallen aus dem Muster heraus, das hinter dem D
  eine reine Ziffernfolge und dann einen Gedankenstrich erwartet; die Zahl
  liegt deshalb um zwei unter der Zahl aus `grep -c '^### D'`. Das ist bekannt und unschädlich.
- **Blöcke werden ersetzt, nicht Teilstrings geflickt.**
- **Zeilenlängen nach dem Trockenlauf prüfen**, nur die *neuen* Zeilen, in Zeichen.
- Umlaute schreiben, nicht Umschrift.
- Die Splice-Skripte danach aus dem Wurzelverzeichnis **löschen**.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`, das System-Python hat es nicht. Die Registerköpfe sind `###`,
nicht `##`; die Prüfregeln stehen als `**N.**` im Fließtext, nicht als Überschrift.

Zum Ende dieser Sitzung: `main` bei `e402ab7`, gepusht. **556 Tests**. Register **D1–D179**,
Prüfregeln **1–28**. Keine offenen Läufe. Der Branch `00d-epochenkette` ist gemergt.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys` in
  `mensch_als_republik/keys.py`, Vermerke in `mensch_als_republik/findings.py`.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`, `§4.1` Benennungsregel.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung, Genesis-Bindung in `decide`
  — und seit dieser Sitzung `§4.5`, die **Kettenauflösung**.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests.

**Neu in dieser Sitzung:** D174 bis D179, Prüfregel 28, `04 §4.5`, Nachzüge an `04 §4.4`, `§5`
und `§8`, `mensch_als_republik/governance/chain.py`, `tests/governance/test_chain.py` mit zwölf
Vektoren, zwei Vermerke `EPOCH_PROPOSAL_UNAVAILABLE` und `EPOCH_FORK`.

- **D174** — `resolve_epoch` in `governance/chain.py`. Startet bei Epoche 1 aus dem Genesis,
  läuft Übergang für Übergang über `decide` und `verify_ratification`. Kein `policy`-Parameter:
  die Policy wird je Epoche aus deren Verfassung hergeleitet, sonst gälte nach einem Amendment
  still die falsche. Keine Zyklusprüfung: jeder `ratify@1` trägt höchstens einen Übergang.
- **D175** — Objektbeschaffung als geprüfte Abbildung. Der Wert wird gegen den Schlüssel geprüft;
  passt er nicht, gilt der Eintrag als unbekannt. In `decide` wurde `known_proposals` bis dahin
  geglaubt — drei von vier Objektquellen waren geprüft, eine nicht.
- **D176** — Zwei Nachfolger derselben Epoche sind **unerreichbar**, nicht nur unwahrscheinlich.
  `EPOCH_FORK` ist implementiert und hat ausdrücklich keinen Produktivfall.
- **D177** — Berichtigung `04 §8`: `resolve_current_key` stand in der Vertagungsliste und war
  seit `00a` gebaut.
- **D178** — Die Aussetzung aus D103 wirkt **über Epochengrenzen**. Ein Mitglied kann die Kette
  rückwirkend anhalten, indem es auf einen nie veröffentlichten Vorschlag Ja stimmt.
- **D179** — Abnahme `00d`, Prüfregel 28, und die Zählung.

## Warum D176 den Fork aufgelöst hat statt ihn zu entscheiden

Die Designrunde hatte gefragt, welche Ordnung einen Gleichstand zwischen zwei tragenden
Nachfolgern bricht, und D172 als Antwort erwogen. Die Prämisse war falsch: `04 §3.5` verlangt
`2 * num >= den`, eine Schwelle unter der Hälfte ergibt `MALFORMED_THRESHOLD`, und `§3.2`
vergleicht strikt. Jede erreichte Schwelle ist damit eine echte Mehrheit. Disjunkte Ja-Mengen
schließt `§3.5` aus, überschneidende schlägt `§4.4`. Es gibt keinen Gleichstand.

Die Literatur hat das gestützt und die Form geliefert: Quorum-Überschneidung ist die notwendige
Bedingung, und wo sie fehlt, ist die Konfiguration kaputt statt auflösbar. Tendermint hält im
Fork-Fall an und erzeugt einen Beweis, statt einen Kopf zu wählen. Ein Tiebreak über eine
abgeleitete Ordnung kommt in keiner gesichteten Quelle vor.

## Was diese Sitzung gelehrt hat

**Der Supervisor war die Fehlerquelle, das Werkzeug nicht — fünfte Sitzung in Folge.** Vier von
neun Testfällen aus den Prompts behaupteten unmögliche Weltzustände. Alle vier lasen sich
schlüssig. Daraus Prüfregel 28.

**Die Messung wird zum Vektor, nicht gelöscht.** Der erste Reparaturvorschlag hätte die drei
fehlgeschlagenen Kriterien durch drei bequemere ersetzt. Der Operator hat gefragt, ob die
Literatur das trägt und ob wir uns das schön reparieren — und genau diese Frage hat D178
freigelegt. Ein nachgezogener Anker löscht die Beobachtung, ein aufgeschriebener Vektor bewahrt
sie.

**Eine Probe, die einen unmöglichen Zustand ansteuert, ist keine Probe.** Sie bleibt rot, egal
was man zurücknimmt, und sieht dabei aus wie eine funktionierende Rücknahmeprobe.

**Das eigene Register ist eine Quelle, die man aufschlagen muss.** D107 nannte Equivocation
wörtlich als den Grund, aus dem die Aktivitätsprüfung auf `ratify@1` behalten wurde. Der
Supervisor hat den Eintrag nicht gelesen und stattdessen einen unbaubaren Widerrufs-Test
geschrieben.

## Der nächste Schritt

**Zuerst die Literatur, dann die Frage, dann die Antwort.** In dieser Reihenfolge, ausdrücklich.

`resolve_epoch` liefert Epoche und Verfassungsobjekt aus dem Speicher. Damit ist der Anschluss aus
D160 und D161 zum ersten Mal baubar: `resolve_epoch` nach `resolve_authorized_keys` nach
`membership`. Die hintere Hälfte dieser Naht steht seit `00b` in `tools/example_nucleus.py`
(Zeile 467 bis 485); es fehlt allein, dass `constitution_hash` aus der Kette kommt statt aus einem
Funktionsparameter.

**Wonach zu suchen ist**, bevor die Frage gestellt wird:

- Referenzimplementierungen, die **zwei Ebenen** anbieten — eine tief gelegte Objekt-API und einen
  angeleiteten Weg darüber. `python-tuf` hat diesen Fork ausdrücklich entschieden (`ngclient`
  neben der Metadata-API); die Begründung dort ist der direkteste Präzedenzfall.
- Missbrauchsresistente Schnittstellengestaltung: wann eine Bibliothek den sicheren Weg vorgibt,
  statt ihn dem Aufrufer zu überlassen.
- Ob und wie `did:plc`, CONIKS oder Sigstore eine High-Level-Auflösung neben ihren Primitiven
  führen — und wo sie die Grenze ziehen.

**Dann die Frage genau stellen.** Der erste Entwurf lautet: *Bekommt `mensch_als_republik/` eine
Fassade, die Speicher, Genesis und die beiden Objektabbildungen nimmt und daraus Mitgliedschaft
ausrechnet — oder bleibt die Verkettung Sache des Aufrufers?* Sie ist noch nicht scharf genug.
Drei Größen sind vorher zu trennen: **wo** der Code liegt (`mensch_als_republik/` oder `tools/`),
**wieviel** er tut (nur Kette plus Schlüssel, oder bis `membership` durch), und **ob** er der
einzige empfohlene Weg ist oder ein Angebot neben den Primitiven.

**Was die Positionen tragen soll.** D161 hält fest, dass `membership` seinen Parameter behält;
das entscheidet nichts, denn eine Fassade *über* `03` bricht keine Schichtung. Gegen sie spricht
`08 §3`: sie senkt keine Kollisionskosten und verteilt keine Macht, ist also Werkzeug. Dafür
spricht, dass „Werkzeug" heute heißt, jeder Aufrufer baut die Kette selbst nach — und dieselbe
Regel an zwei Stellen war in diesem Projekt schon dreimal ein Befund (D147, D175, und
`_is_nuc_name` in dieser Sitzung).

## Aufräumen — nicht vergessen

Steht seit mehreren Sitzungen und wird jedes Mal verschoben. Beim Sitzungsstart einplanen, nicht
ans Ende.

- **Gemergte Branches löschen.** Tier 1. Zahl vorher ablesen; zuletzt 72 plus
  `00d-epochenkette`. Sie schaden nicht, solange sie liegen bleiben — aber die Zahl wächst je
  Sitzung um mindestens eins, und sie verdeckt den Blick auf offene Läufe.
- **`make check` steigt in `.venv` ab:** `find . -name __pycache__ -type d -exec rm -rf {} +`
  ohne `-not -path "./.venv/*"`. Mit einer Messung vorher und nachher fahren.
- **`_is_nuc_name` trägt einen führenden Unterstrich und wird über Modulgrenzen importiert.**
  `chain.py` holt sie aus `epoch.py`. Der Unterstrich sagt modulprivat, der Import sagt geteilt;
  eines von beiden stimmt nicht. Entweder umbenennen oder beide aus einem gemeinsamen Ort ziehen.

## Offen

- **Der Anschluss der Kette an `03 §4`** (D160, D161). Erster Punkt der neuen Sitzung, siehe oben.
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173): die Gleichstandsgruppe sitzt am Anker,
  dort wird `cap` nie null.
- **Die Sondierwelt in `test_benennung.py` erzeugt keine Vermerke** (D173).
- **`00` hält die Form seiner Vermerke nirgends fest** (D173).
- **Eine Schwelle für Autoritätslisten** — mit D166 zurückgestellt. Wird für `root_keys`,
  `nucleus_keys` und `arbitration.arbitrators` **zugleich** beantwortet oder gar nicht.
- **Darf ein Amendment ein deklariertes Prädikat weglassen?** Gehört an `04 §5` (D167).
- **Der Beispielnukleus kann Epoche-1- von Epoche-2-Policy nicht unterscheiden** (D169).
- **`genesis[4]` und die Auszählung**: `GV-24` führt ein Genesis, dessen deklarierte Verfassung in
  der Auszählung nirgends vorkommt.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut.
- **`D >= C₀` ist ein SHOULD** in `00 §4.0` und `02 §8` und wird nirgends geprüft (D147).
- **`anchor_set` (`genesis[3]`) bleibt ungebunden** (D147).
- **`TrustParams.__post_init__` und `00 §4.0`** prüfen dieselbe Wohlgeformtheit zweimal (D147).
- **`disjoint_paths` bewegt sich nicht** (bleibt `1` in allen gemessenen Fällen).
- **Ausgang 5 / Selbst-Equivocation** — entschieden, aber der Ort ist offen (D127).
- **`FOREIGN_LIFECYCLE` hat keinen Produktivträger mehr** (D138, bewusst). Seit dieser Sitzung
  hat `EPOCH_FORK` denselben Status (D176) — und aus demselben Grund: der Fall ist unerreichbar,
  der Ausgang ist trotzdem definiert.
- **Meldung übersprungener Claims aus `store_laden`** — von D138 zurückgestellt.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** prüfen eine schwächere Aussage als sie
  scheinen (D117). Der Vorbehalt steht in `04-golden-anchors.md §8`.
- **Dreifache Kantensumme in `test_deckenelastizitaet.py`** (D142, notiert, nicht blockierend).
- **`02d-purpose`** (D56), **VR-04.1** (D26), **Zeugenquorum für Fristen** (D100).
- **`04 §7.2` Föderation** nicht durchgerechnet.
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **`example-nucleus.md`** unvollständig.
- **Layer 05.** Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf), die Beta-Reputation
  mit dem Moral-Licensing-Problem — und seit D178 die Frage, ob wiederholtes Stimmen auf
  unveröffentlichte Vorschläge eine Folge tragen soll.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.
