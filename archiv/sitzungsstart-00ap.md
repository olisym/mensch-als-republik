# Sitzungsstart: 00ap (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, selbst gehostete Gitea-Instanz (`git.h.error13.de`). Das lokale
Arbeitsverzeichnis ist `~/mensch-als-republik`, daneben `~/mar-go` mit der unabhängigen
Zweitimplementierung von Layer 01 in Go, auf eingefrorenem Anker.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

**Der Abschnitt hat gewechselt.** Layer 01 ist ausgelesen; die Mutantenkampagne hat über 2511
Einzel- und 16958 Paarmutanten keinen einzigen Befund aus einem Verdikt-Unterschied getragen.
Seit D311 läuft der **Anwendungsabschnitt**, und für ihn gilt ein anderer Modus.

## Der Prototypmodus (D311 Beschluss 1)

Szenarioskripte sind **Wegwerfcode**. Für sie gelten **nicht**: Registerpflicht für den Code,
Golden Numbers, Rücknahmeproben, Zweitimplementierung, Abnahme gegen erwartete Zahlen.

Es gelten **weiter**: die Spec als normative Wahrheit, das Register als oberste Instanz, die
Zitiergrammatik, und dass eine Messung eine Position ändern können muss.

Ins Register wandert aus einem Prototyplauf ausschliesslich der **Befund**: die Stelle, an der die
Spec keine Antwort hatte, eine falsche gab, oder eine erzwang, die ein Zentrum voraussetzt.

Die Abnahme prüft im Prototypmodus **nicht den Code gegen den Bericht**, sondern die **Befunde
gegen die Spec**. Das ist billiger und aussagekräftiger; in `00an` hat es zwei Fehler im eigenen
Prompt gefunden.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 64, im
Volltext, in elf Abschnitten entlang des Arbeitsbogens. Die Nummern stehen darin **nicht** in
Reihenfolge. Wer eine Regel sucht, sucht den Zeitpunkt, an dem sie greift.

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird.

**Die neuen Regeln 63 und 64 stammen beide aus eigenen Fehlern dieser Sitzung.** 63: vor einem
Prompt, der etwas bauen lässt, wird gemessen, ob es das schon gibt. 64: eine Regel, die eine Menge
ausdünnt, wird auf ihren zweiten Lauf geprüft.

- **Die Projektkopie wird ausgepackt und gefahren.** Aus `/tmp/mar-context.xml` lässt sich der
  ganze Baum rekonstruieren — geschnitten am `file`-Tag, die Newline hinter dem öffnenden und vor
  dem schliessenden Tag gehören nicht zum Inhalt. `cbor2`, `cryptography`, `pytest` und
  `hypothesis` nachinstallieren, dann den Bestand fahren und die bekannte Testzahl reproduzieren:
  damit ist der Baum geeicht (Prüfregel 51). **Vorsicht bei Eigenschaften der Datei selbst:** das
  Auspackskript hängt jeder Datei eine Schluss-Newline an.
- **Der Blob-Hash aus dem Diff ist der Anker der Rekonstruktion.** `git hash-object` auf die
  nachgebaute Datei gegen die `index`-Zeile des Diffs. In `00am` viermal getroffen, auf beiden
  Seiten; damit stand auch die Basis.
- **Golden Numbers gehören nicht in den Prompt**, sondern in die Abnahme.
- **Der Bericht ist nie die Abnahme, auch nicht der eigene** (Prüfregel 56).
- **Der Sitzungsstart ist eine Hypothese, keine Messung.** Prüfregel 27 gilt auch für diese Datei,
  und ebenso für jeden Posten ihrer offenen Liste (D301). Sie nennt den Stand **vor** ihrer eigenen
  Übergabe; der Kopf wird gemessen, nicht abgeschrieben (Prüfregel 40).
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`,
  `ruff`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.

### Shell

- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und
  eine Pipe auf `tail`, `cat`, `tee` oder `grep -q` sind die nützlichen Ausnahmen.
- **Sichtbar und geprüft zugleich geht über `tee`.** `make check 2>&1 | tee /tmp/x.txt | tail -6`,
  danach `grep -q '^789 passed' /tmp/x.txt`.
- **Kommandosubstitution in doppelten Anführungszeichen braucht kein `$` in fish, aber sie wird
  darin auch nicht ausgeführt.** In `00am` landete der ganze Ausdruck wörtlich im Kopf der
  Projektkopie. Der Weg, der trägt: die Zahlen mit `printf` und Kommandosubstitution **ausserhalb**
  von Anführungszeichen in eine Datei schreiben, dann `--header-text "$(cat /tmp/stand.txt)"`.
- **`grep` ohne `-E` kennt kein `|` als Alternative.** **`grep -c` liefert bei null Treffern
  Status 1**; eine Zählzeile, die null ergeben *darf*, geht auf `| cat`.
- **`diff a b > datei` bricht die Kette**, weil `diff` bei Unterschieden Status 1 liefert.
- **Ein Glob ohne Treffer bricht die Kette**, auch vor einem `rm -f`. Zum Aufräumen deshalb
  `find /tmp -maxdepth 1 -name 'splice-*.py' -delete`.
- **Ein Fragment aus einem Antwortabsatz gehört nicht in den Block.** In `00ao` ist ein
  schliessendes Tag aus der Prosa in einen Copy-Block geraten; fish meldete
  `Erwartete a string, aber fand end of the input`. Der Block wird vor dem Absenden von hinten
  gelesen.
- **Eine lange Ausgabe passt nicht in jedes Konsolenfenster.** Diagnoseskripte **aggregieren**
  und schreiben die volle Liste in eine Datei; ein `| cut -c1-150` verhindert den Umbruch.
- **`go` liegt nicht im `PATH`.** Die Toolchain steht unter `~/sdk/go/bin/go`.
- **Die Werkzeuge unter `tools/` laufen nur als Modul.** `python -m tools.gitter`.
- **Im Merge-Block steht `git push` vor `git branch -d`** (Prüfregel 58).
- **Neue Dateien kommen nach dem Splice, nicht davor.** `splice_run.py` verlangt einen sauberen
  Arbeitsbaum und scheitert schon an einer unverfolgten Datei.
- **Mehrere Hashes prüft ein `printf` mit wiederholtem Format**, Ausgabe in `sha256sum -c`.
- **`set -l` und verschachtelte Kommandosubstitution gehören nicht in einen Copy-Block.**
- **Keine Ausgabe heisst: der Block ist nicht gelaufen.**
- **Jeder Block trägt Marken.** Vor jedem Abschnitt ein `echo "== NAME =="`, am Ende ein
  `echo "== FERTIG =="`.
- **`string`-Kommandos in einer `and`-Kette sind eine Falle.**
- **Spec-Dateien, Prompts und Skripte als Download**, nicht als Copy-Block. **Eine Datei, die
  erzeugt und nicht ausgeliefert wurde, existiert für Oli nicht.**
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet`.
- **Prosa bricht bei 100 Zeichen; Tabellenzeilen und Codeblöcke sind ausgenommen** (D222). Für
  Python gibt es **keine** Zeilenlängenregel (D205). Diese Datei ist **nicht** ausgenommen.
  **Zeichen zählen, nicht Bytes** — `awk length` zählt Bytes.
- **Eine Regex, die in einen Prompt oder eine Spec-Datei soll, geht nicht.** Regexänderungen
  werden in Prosa beauftragt.

### Das Wurzelverzeichnis ist seit D314 gebunden

**27 Markdown-Dateien in der Wurzel, 104 unter `archiv/`.** Eine Wurzeldatei ist gebunden, wenn
sie in `LAYER_FILES` oder `ALWAYS_BOUND` steht, oder wenn eine Python-Datei oder eine **andere
gebundene** Wurzeldatei sie als `NAME §X` nennt. Eine blosse namentliche Nennung bindet nicht.
`check_specs` meldet die Zahlen am Ende und **schlägt dabei nicht fehl**.

**Verweise mit Paragraphen auf archivierte Dateien sind ab jetzt ein Befund** — der Zitiername ist
unbekannt, sobald die Datei die Wurzel verlässt. Wer eine Archivdatei erwähnt, nennt sie ohne
Abschnitt.

### Die Zitiergrammatik — geschlossen

Seit D232 gibt es keinen offenen Teil. Vier Teile: der Dateiname mit oder ohne `.md`; die
Kurzform `NN`/`NNx` über `LAYER_FILES`; die Bereichsform `NAME §A–§B` (D228, kein Leerraum um den
Strich); die Anhangsnummer als Grossbuchstabe mit Punkt vor der Ziffernfolge (D230). Dazu die
Backtick-Toleranz (D231). Alles andere in `.py` ist ein Befund (D227); in `.md` bleibt der bare
Verweis zulässig.

**Ein Verweis auf einen Abschnitt derselben Datei braucht die Dateinamensform** (D301).

**Prüfregel 47:** ein Verweis und ein Inline-Code-Span werden nicht über die Zeilengrenze getrennt.

**Die Grenze, die bleibt:** die Prüfung sichert, dass das Ziel **existiert**, nicht dass es
**stimmt** (D229, D233). Daraus folgt D250: ein Anhang wird **angehängt, nicht eingeschoben**.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt. Eine **Ersetzung** ist eine Löschung
  plus eine Einfügung; nach Prüfregel 48 werden die randgleichen Zeilen abgezogen.
- **`grep -c '^+'` auf einen unified diff zählt die `+++`-Kopfzeile mit.**
- **Ein eigener Print-Separator ist keine Messung.**
- **Aus einer Zeilennummer folgt kein Abschnitt.**
- **Zwei Messungen desselben Gegenstands gehören gegeneinander gehalten**, bevor die zweite eine
  Entscheidung trägt.
- **Zählvorschriften:** Registerköpfe `grep -c '^### D' 07-decisions.md`; Prüfregeln
  `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`; Branches `git branch -a | wc -l` — die Zahl
  schliesst `origin/main` und `origin/HEAD` ein, drei heisst also ein lokaler Branch.
- **Die Projektkopie wird nach jedem Push nachgezogen** (D224, Prüfregel 43), mit fünf Kaltzahlen
  im `--header-text`. **Das `-o` gehört dazu.** Ob der Header in der Datei steht, sagt erst ein
  `grep` auf `user_provided_header`.
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position, **40**
  vor jeder Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung gegen den
  Prompt, **43** vor jeder Zahl aus der Kopie, **44** vor jeder abgeleiteten Anzahl, **46** vor
  jeder Zeilenangabe, **49** vor jeder Rücknahmeprobe, **51** vor jedem Prüfer, der eine Menge
  misst, **59** vor jeder rekonstruierten Fassung, **60** vor jeder Meldung über eine Probe, **61**
  vor jeder Bewertung einer Abweichung zwischen zwei Fassungen, **62** vor jeder Probe, die eine
  Menge verkleinert, **63** vor jedem Prompt, der etwas bauen lässt, **64** vor jeder Regel, die
  eine Menge ausdünnt.

### Splices

Ein Splice ist ein Skript mit `assert`, dass der Anker genau einmal vorkommt. Gefahren mit
`.venv/bin/python tools/splice_run.py /tmp/splice-*.py` (D225). **Die Meldung `AssertionError`
gefolgt von `zweiter Lauf gescheitert` ist die Erfolgsmeldung.**

- **Das Skript liegt in `/tmp`.** `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Das Skript wird erzeugt, nicht getippt.** Der Anker wird aus der Zieldatei **gelesen**.
- **Ein Skript mit mehreren Paaren rechnet erst alles und schreibt dann.** In dieser Sitzung
  zweimal mit zwei Dateien zugleich gefahren, beide Male sauber.
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42). Der belastbare
  Assert misst jede Zeile der neuen Fassung, die in der alten nicht vorkommt.
- **Das Anhängen an das Dateiende wird über `rstrip` normalisiert** und ist damit unabhängig davon,
  wie die Zieldatei endet; deshalb lässt sich der Zielhash vorher rechnen.
- **Ein Zielhash-Assert vor dem Schreiben ersetzt den Quellhash.** Weicht die Datei ab, schreibt
  das Skript nicht. Das trägt auch dann, wenn der Nachbau aus der Projektkopie am Dateiende
  abweichen könnte.
- **`alt.count("### D")` ist nicht die Zählvorschrift.** Ein Registereintrag zitiert im Fliesstext
  eine Überschrift, und der Teilstring trifft mitten in der Zeile. Zeilenweise mit `startswith`.
- **Ein Nachtrag an einen bestehenden Eintrag erhöht die Registerzahl nicht.**
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. Vor der Testzahl `.hypothesis` und `__pycache__`
löschen (Prüfregel 19).

Nach `00ao`: **789 Tests**. Register **D1–D315**, Prüfregeln **1–64**. **Drei Branches**. Keine
offenen Läufe. Der Stand ist `960634d`.

- **00** Nukleus, Genesis, Verfassung. `§4.2` empfiehlt Governance und Substanz in getrennte
  Scopes — Obligationen gehören **nicht** in den Scope, dessen `participants` abgestimmt werden.
- **01** Atom, Verifier, **zwölf Reject-Codes**, **sieben** Klassifikationszustände. Anhang C
  trägt **sechzehn** Abschnitte. Seit D308 die Versionsausnahme.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II. `§3.1` Preisblindheit, `§3.2` Trägerwert extern, `§3.3` gegenseitiger Kredit.
- **04** Governance. Ein Vorschlag besteht aus Scope, Vorgängerepoche und Verfassungshash.
- **08** Zweck und Geltungsbereich. `§3` trägt das Aufnahmekriterium und die Prüftabelle.
- **Werkzeuge**: `register_index.py`, `check_specs.py`, `check_tree.py`, `splice_run.py`,
  `korpus.py`, `verdikt.py`, `gitter.py`, `paare.py`, `szenario_absicherung.py`, dazu **`sim/`**.
- **`tools/sim/` ist ein vollständiger Simulationsrahmen** — getrennte Beobachter, getrennte Uhren
  und Schlüssel, ein Verzeichnis je Teilnehmer mit Inbox, deklarative Szenarien in JSON mit den
  Schritten `claim`, `zustellen`, `uhr`, `zeige` und `erwarte`, sechs Szenarien, eigene Tests.
  **Jeder weitere Szenariolauf setzt darauf auf.**
- **Die Kampagne steht über beide Stufen.** `gitter.py` liefert **2511** Einzelmutanten in drei
  Familien (1174 in A, 1264 in B, 73 in C); `paare.py` **16958** Paarmutanten (85 Vorrangprobe,
  2059 / 4378 / 10436 in den Klassen). Elf der zwölf Reject-Codes sind erreichbar.
- **Go-Fassung**: `~/mar-go`, Remote unter `git.h.error13.de/oli/mar-go`, Spec-Kopie auf
  eingefrorenem Anker (D302).

### Was diese Sitzung entschieden hat

- **D309, D310** — die drei Rückstände aus `00al`: Klassentest, Namensöffnung, Schritt 26 auf 27.
  Berichtigung von D304: neun Zeilen, nicht zwölf.
- **D311** — Moduswechsel in den Anwendungsabschnitt; drei Befunde vor der ersten Prototypzeile.
- **D312** — Abnahme von Stufe A; zwei Fehler im eigenen Prompt; Prüfregel 63.
- **D313** — zwei Vorarbeiten zur Risikoteilung, und wohin eine Versicherung gehört.
- **D314, D315** — Bindungsregel und Archiv; Prüfregel 64.

## Was diese Sitzung gelehrt hat

**Der Bestand wird gemessen, bevor ein Prompt etwas bauen lässt.** Der Prompt zu Stufe A liess
einen Simulationsrahmen neu bauen, den es unter `tools/sim/` längst gab. Das Werkzeug fand ihn,
benannte ihn und baute trotzdem, weil der Prompt es verlangte — regelkonform. Prüfregel 63.

**Eine Ausdünnungsregel wird auf ihren zweiten Lauf geprüft.** Die Bindungsregel im Prompt hielt
28 Dateien im ersten und 27 im zweiten Durchgang. Das Werkzeug schloss die Lücke von selbst und
sagte es. Prüfregel 64.

**Prüfregel 38 wurde in derselben Sitzung übergangen, in der sie zitiert wurde.** Der Prompt zu
Stufe A ordnete Obligationen in den Governance-Scope, was `00 §4.2` ausdrücklich abrät. Der
billigste Griff ist `tools/register_index.py`, und er wurde nicht getan.

**Die Abnahme im Prototypmodus zielt auf die Befunde, nicht auf den Code.** Vier Befunde gegen die
Spec geprüft, zwei Prompt-Fehler gefunden, einen Befund als ungenau erkannt. Der Code wurde nicht
rekonstruiert, und das war richtig.

**Eine Zahl, die abweicht, ist ein Geschenk.** Beide Abweichungen dieser Sitzung — neun statt
zwölf, 27 statt 28 — führten auf einen Fehler in der eigenen Erwartung, nicht im Lauf.

## Der nächste Schritt

**Stufe B beginnt als Spec-Arbeit, nicht als Lauf** (D313 Beschluss). Die drei Befunde ohne Ort
aus D312 werden durch das Aufnahmekriterium aus `08 §3` geschickt und als Zeilen in die Prüftabelle
eingetragen:

1. **Das Gruppen-Soll.** Vermutung: verteilt Macht, gehört nicht ins Protokoll, und die Umlage aus
   bilateralen Zusagen ist die Antwort statt ein Ersatz. Vermutungen sind keine Einträge.
2. **Die Verwahrerrolle.** Vermutung: Policy, und `00 §4.2` warnt zusätzlich vor dem Ort.
3. **Das Prädikat für den Fall.** Vermutung: `accusation@1` trägt ihn bereits, vollständig opak
   nach D67, dann ist es keine Lücke.

Erst danach ein weiterer Durchlauf, und dann mit der Frage, ob Vertrauensentzug als Durchsetzung
reicht, wo vergleichbare Projekte Mittelsperrung brauchen. Der Rahmen dafür ist `tools/sim/`, und
die Substanz liegt in einem eigenen Scope ohne `participants`.

**Vor dem ersten Zug: `ALWAYS_BOUND` in `tools/check_specs.py` nennt die Übergabedatei beim
Namen.** Diese Datei wird deshalb als ungebunden gemeldet. Die Meldung blockiert nicht, aber sie
entwertet sich, wenn sie dauerhaft eine Zeile trägt. Der kleine Auftrag: die feste Liste auf ein
Muster umstellen, das die alphabetisch letzte Übergabedatei der Wurzel bindet.

## Offen

**Aus dem Anwendungsabschnitt (D312):**

- **Es gibt kein Gruppen-Soll.** Drei bilaterale Obligationen an dieselbe Person sind drei
  Obligationen, kein Anspruch gegen eine Gemeinschaft.
- **Es gibt keine Verwahrerrolle.** Wer sammelt, ist eine benannte Person, und das Protokoll kann
  feststellen, dass sie nicht auszahlt, aber nichts erzwingen.
- **`OPEN` unterscheidet Verweigerung nicht von Partition.** Das begrenzt, was Reputation aus
  Nichtleistung ableiten darf.
- **Gleicher Zustand bei allen Beobachtern ist eine Eigenschaft der Verteilung**, nicht von
  `settlement`. Das Protokoll erzwingt die Kopie nicht.
- **Preisblindheit ist die Stelle, an der `03` eine Versicherungsphase nicht mehr trägt.**
- **`settlement` prüft keine Mitgliedschaft.** Eine Obligation eines Nichtmitglieds ist ebenso
  `OPEN` oder `SETTLED`.
- **Ohne `t_exp` bleibt eine Obligation ohne Ende offen.** Ein Gläubiger-Timeout gibt es nicht.
- **`tools/szenario_absicherung.py` ist Wegwerfcode** und wird nicht fortgeschrieben.

**Aus dem Verifikationsabschnitt, weiterhin offen:**

- **Anhang C ist gegen Generatordrift nur teilweise gesichert.** Für C.1 gibt es einen Test mit
  getipptem Hex; für C.13 bis C.15 gibt es nichts, was den Spec-Text an `vectors_01.json` bindet.
  **Die andere Achse ist seit D295 geschlossen**: Datei gegen Generator.
- **`UNPARSABLE_V` entsteht bei `ratify@1` nicht** (D276).
- **`cbor_canon.decode` ist tolerant und bleibt es.**
- **`FOREIGN_LIFECYCLE` hat keinen Vektor und kann keinen bekommen** (D263, D268); es ist auch vom
  Gitter unerreichbar, weil es einen Speicher braucht.
- **`EPOCH_FORK` hat keinen Produktivträger** (D138, D176, D281).
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173).
- **Sechs Zeilen mit wahrer Expiry-Inkohärenz** wählt die Zweitfassung anders; beide Codes sind
  wahr, die Spec stellt frei, der Grund des Unterschieds ist ungeklärt.
- **Zwei Registerverweise zeigen ins Leere**, `03 §5.1` und `03 §11`. Bewusst nicht nachgezogen.
- **Die Einlese-Dateien behaupten, NV2 trage keine Drahtbytes.** Seit D291 falsch, bewusst nicht
  nachgezogen; sie liegen jetzt im Archiv.
- **N09 ist beobachtet, nicht durchgesetzt** (D119, D246). **N10 ist teilgemessen** (D246).
- **Die Anhangsform-Datei trägt fünf um eins zu hohe Zeilenangaben** (D232); sie liegt im Archiv,
  der Posten bleibt.
- **`.claude/settings.local.json` landet in der Projektkopie**, obwohl git sie ignoriert.
- **Die Sitzungsstart-Datei ist ein monolithisches Rewrite** (D218).
- **Es gibt keine Kontextdatei für das Werkzeug** (D218).
- **Die Verweisprüfung kann Listenpunkte nicht von Unterabschnitten unterscheiden** (D209).
- **Der Harness vergleicht Zeilenzahlen, er identifiziert Zeilen nicht** (D226).
- **Die Sondierwelt in `test_benennung.py` erzeugt keine Vermerke** (D173).
- **Wie weit die Regierbarkeitsprüfung reicht** (D200). Zurückgestellt — **nicht vorher aufmachen**.
- **`RATIFY_WITH_EXPIRY` und der Zeugenpfad tragen die Weitergaberegel ungeprüft** (D203).
- **Vergleiche gegen `dedupe_sort` sind für die Reihenfolge zirkulär** (D196).
- **Vier `Finding`-Klassen, drei `dedupe_sort`** (D183, mit D207 berichtigt).
- **Eine Schwelle für Autoritätslisten** — mit D166 zurückgestellt, für alle drei Listen zugleich
  oder gar nicht. Nach D236 tragen alle drei dasselbe Bearer-Problem.
- **Darf ein Amendment ein deklariertes Prädikat weglassen?** Gehört an `04 §5` (D167).
- **Der Beispielnukleus kann Epoche-1- von Epoche-2-Policy nicht unterscheiden** (D169, D188).
- **`genesis[4]` und die Auszählung**: `GV-24` führt ein Genesis, dessen deklarierte Verfassung in
  der Auszählung nirgends vorkommt.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut.
- **`D >= C₀` ist ein SHOULD** in `00 §4.0` und `02 §8` und wird nirgends geprüft (D147).
- **`anchor_set` (`genesis[3]`) bleibt ungebunden** (D147).
- **`TrustParams.__post_init__` und `00 §4.0`** prüfen dieselbe Wohlgeformtheit zweimal (D147).
- **`disjoint_paths` bewegt sich nicht** (bleibt `1` in allen gemessenen Fällen).
- **Ausgang 5 / Selbst-Equivocation** — entschieden, aber der Ort ist offen (D127).
- **Meldung übersprungener Claims aus `store_laden`** — von D138 zurückgestellt.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** prüfen eine schwächere Aussage als sie
  scheinen (D117).
- **Dreifache Kantensumme in `test_deckenelastizitaet.py`** (D142, nicht blockierend).
- **`02d-purpose`** (D56), **VR-04.1** (D26), **Zeugenquorum für Fristen** (D100).
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **Layer 05.** Mit D237 ausdrücklich zurückgestellt.
- **Eine dritte Implementierung** bleibt möglich (D311), aber sie prüft dieselbe Achse wie die
  Kampagne, und die hat nichts geliefert. Erst wenn der Anwendungsabschnitt Fragen an `01`
  zurückwirft.
- **Tripel bleiben zurückgestellt** (D305 Beschluss 4), solange Stufe 2 keinen Befund erzeugt hat.

**Die Wertschicht bleibt leer, und das ist kein Versäumnis.** `08 §3` nennt sie als benannten
Empfänger. Jede Anbindung an ein Inhaberinstrument hängt an einem Verwahrer — an einem Betreiber,
an einer Gruppe von Treuhändern oder an einem Hersteller gesicherter Hardware. Für die Frage, ob
Absicherung ohne Machtstelle möglich ist, liefert keine dieser Formen eine neue Antwort (D313).

**Die Anwendung mit echten Menschen bleibt zurückgestellt.** `08 §2.2` verlangt vier Menschen mit
einem echten gemeinsamen Anliegen. Warten ist ein zulässiger Zustand; so tun als ob nicht. Ein
simulierter Durchlauf ist kein Ersatz dafür, aber er ist auch nicht nichts: er beantwortet, was
das Protokoll trägt, bevor jemand sich darauf verlässt.
