# Sitzungsstart: 00al (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, selbst gehostete Gitea-Instanz (`git.h.error13.de`). Das lokale
Arbeitsverzeichnis ist `~/mensch-als-republik`, daneben `~/mar-go` mit der unabhängigen
Zweitimplementierung von Layer 01 in Go — **seit `00ak` mit Remote**.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 61, im
Volltext, mit stabilen Nummern, in elf Abschnitten entlang des Arbeitsbogens. Die Nummern stehen
darin **nicht** in Reihenfolge. Wer eine Regel sucht, sucht den Zeitpunkt, an dem sie greift.

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird. **Seit D300 kennt der Index auch Anhangsverweise** — `01 §B.2` liefert
zwölf Einträge. Vorher lieferte er eine leere Zeile, und das hat in `00ak` zwei Züge gekostet.

Was in `00ak` am meisten getragen hat:

- **Die Projektkopie wird ausgepackt und gefahren.** Aus `/tmp/mar-context.xml` lässt sich der
  ganze Baum rekonstruieren — geschnitten am `file`-Tag, die Newline hinter dem öffnenden und vor
  dem schließenden Tag gehören nicht zum Inhalt. `cbor2`, `cryptography`, `pytest`, `hypothesis`,
  `coverage` und `ruff` nachinstallieren, dann den Bestand fahren und die bekannte Testzahl
  reproduzieren: damit ist der Baum geeicht (Prüfregel 51). In `00ak` hat er zwei vollständige
  Prototypen getragen — die Zeilenschnittstelle und das Mutationsgitter —, elf Rücknahmeproben,
  vier Splice-Trockenläufe und den Nachbau von fünf Werkzeugdateien gegen ihre Blob-Hashes.
  **Vorsicht bei Eigenschaften der Datei selbst:** das Auspackskript hängt jeder Datei eine
  Schluss-Newline an.
- **Der Blob-Hash aus dem Diff ist der Anker der Rekonstruktion.** `git hash-object` auf die
  nachgebaute Datei gegen die `index`-Zeile des Diffs. In `00ak` fünfmal getroffen; damit ist
  Prüfregel 59 auf eine Zeile geschrumpft und braucht keine Quellhashliste mehr.
- **Die gelieferte Fassung wird vor dem Prompt gebaut und gefahren, nicht nur beschrieben.**
- **Golden Numbers gehören nicht in den Prompt.**
- **Der Bericht ist nie die Abnahme, auch nicht der eigene** (Prüfregel 56).
- **Der Sitzungsstart ist eine Hypothese, keine Messung.** Prüfregel 27 gilt auch für diese Datei,
  und ebenso für jeden Posten ihrer offenen Liste (D301).
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`,
  `ruff`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.

### Shell

- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten** — `--include='*.go'` ohne Anführungszeichen bricht die Kette, in `00ak`
  einmal passiert. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und eine Pipe
  auf `tail`, `cat`, `awk` oder `grep -q` sind die nützlichen Ausnahmen.
- **`grep` ohne `-E` kennt kein `|` als Alternative.** In `00ak` einmal als leeres Ergebnis
  erschienen, das wie eine Messung aussah.
- **`grep -c` liefert bei null Treffern Status 1.** Eine Zählzeile, die null ergeben *darf*, geht
  auf `| cat`.
- **`diff a b > datei` bricht die Kette**, weil `diff` bei Unterschieden Status 1 liefert. Ein
  angehängtes `| cat` hält sie am Leben; die Zeilenzahl wird danach gezählt.
- **`go` liegt nicht im `PATH`.** Die Toolchain steht unter `~/sdk/go/bin/go`.
- **Die Werkzeuge unter `tools/` laufen nur als Modul.** `python tools/gitter.py` scheitert, weil
  `sys.path` dann auf `tools` zeigt; `python -m tools.gitter` läuft.
- **Im Merge-Block steht `git push` vor `git branch -d`** (Prüfregel 58).
- **Neue Dateien kommen nach dem Splice, nicht davor.** `splice_run.py` verlangt einen sauberen
  Arbeitsbaum und scheitert schon an einer unverfolgten Datei. In `00ak` einmal passiert.
- **Sichtbar und geprüft zugleich geht über eine Datei.** `make check > /tmp/x.txt`, dann
  `tail -1 /tmp/x.txt`, dann `grep -q '^779 passed' /tmp/x.txt`.
- **Mehrere Hashes prüft ein `printf` mit wiederholtem Format**, Ausgabe in `sha256sum -c`.
- **`set -l` und verschachtelte Kommandosubstitution gehören nicht in einen Copy-Block.**
- **Keine Ausgabe heißt: der Block ist nicht gelaufen.**
- **Jeder Block trägt Marken.** Vor jedem Abschnitt ein `echo "== NAME =="`, am Ende ein
  `echo "== FERTIG =="`.
- **`string`-Kommandos in einer `and`-Kette sind eine Falle.**
- **Kommandosubstitution in doppelten Anführungszeichen braucht `$`.**
- **Spec-Dateien, Prompts und Skripte als Download**, nicht als Copy-Block. **Eine Datei, die
  erzeugt und nicht ausgeliefert wurde, existiert für Oli nicht.**
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet`.
- **Prosa bricht bei 100 Zeichen; Tabellenzeilen und Codeblöcke sind ausgenommen** (D222). Für
  Python gibt es **keine** Zeilenlängenregel (D205). Diese Datei ist **nicht** ausgenommen.
  **Zeichen zählen, nicht Bytes** — `awk 'length>100'` misst Bytes und meldet Umlautzeilen falsch.
- **Eine Regex, die in einen Prompt oder eine Spec-Datei soll, geht nicht.** Regexänderungen
  werden in Prosa beauftragt; in `00ak` hat das für D300 einwandfrei funktioniert.

### Die Zitiergrammatik — geschlossen

Seit D232 gibt es keinen offenen Teil. Vier Teile: der Dateiname mit oder ohne `.md`; die
Kurzform `NN`/`NNx` über `LAYER_FILES`; die Bereichsform `NAME §A–§B` (D228, kein Leerraum um den
Strich); die Anhangsnummer als Großbuchstabe mit Punkt vor der Ziffernfolge (D230). Dazu die
Backtick-Toleranz (D231). Alles andere in `.py` ist ein Befund (D227); in `.md` bleibt der bare
Verweis zulässig.

**Ein Verweis auf einen Abschnitt derselben Datei braucht die Dateinamensform**, nicht die
Kurzform: `02b-abnahme §B.4`, nicht `02b §B.4` — die Kurzform zeigt auf `02b-golden-anchors.md`,
und `check_specs.py` fängt sie (D301).

**Prüfregel 47:** ein Verweis und ein Inline-Code-Span werden nicht über die Zeilengrenze getrennt.

**Die Grenze, die bleibt:** die Prüfung sichert, dass das Ziel **existiert**, nicht dass es
**stimmt** (D229, mit Zahlen bestätigt in D233). Daraus folgt D250: ein Anhang wird **angehängt,
nicht eingeschoben**.

**Ein Anhang ohne Ziffer ist kein Verweis.** **Ein Prompt darf nicht auf einen Abschnitt zeigen,
den erst sein Lauf erzeugt.** **Befund-Dateien sind zitierfähig.**

### Backslashes

**Ein Backslash in einer Wurzel-Markdown ist kein Rückstand** (D301). Die Regel gilt
Escape-Sequenzen in normativem Text — Bytes als `h'ff'` —, nicht der Markdown-Auszeichnung und
nicht zitierten Suchmustern. Der senkrechte Strich in einer Tabellenzelle und der Stern am
Zeilenanfang müssen escapt werden, sonst bricht die Zelle oder die Fußnote wird ein Listenpunkt.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt. Eine **Ersetzung** ist eine Löschung
  plus eine Einfügung; nach Prüfregel 48 werden die randgleichen Zeilen abgezogen.
- **`tools/check_specs.py` zählt eine Zeile mehr als `wc -l`.**
- **Aus einer Zeilennummer folgt kein Abschnitt.**
- **Zählvorschriften:** Registerköpfe `grep -c '^### D' 07-decisions.md`; Prüfregeln
  `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`; Branches `git branch -a | wc -l` — die Zahl schließt
  `origin/main` und `origin/HEAD` ein, drei heißt also ein lokaler Branch.
- **Die Überdeckung geht der Mutation voraus** (Prüfregel 53), und sie prüft auch den Träger.
- **Ein Assert im Splice darf nicht strenger sein als `check_specs.py`.** Eine Längenprüfung über
  die ganze Zieldatei schlägt am Bestand an, weil D222 Tabellen und Codeblöcke ausnimmt; geprüft
  wird der Einschub.
- **Die Projektkopie wird nach jedem Push nachgezogen** (D224, Prüfregel 43), mit fünf Kaltzahlen
  im `--header-text`, Aufruf über
  `npx --yes repomix --header-text "..." -o /tmp/mar-context.xml`. **Das `-o` gehört dazu.** Der
  npm-Hinweis zeigt `argv` ungequotet; ob der Header in der Datei steht, sagt erst ein `grep`.
  Der Nachzug steht besser am **Anfang** eines Blocks als am Ende — am Ende ist er der erste
  Verlierer.
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position,
  **40** vor jeder Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung gegen
  den Prompt, **43** vor jeder Zahl aus der Kopie, **44** vor jeder abgeleiteten Anzahl, **46** vor
  jeder Zeilenangabe, **49** vor jeder Rücknahmeprobe, **50** vor jedem Kriterium aus einem Modell,
  **51** vor jedem Prüfer, der eine Menge misst, **53** vor jeder Mutantenkampagne, **59** vor
  jeder rekonstruierten Fassung, **60** vor jeder Meldung über eine Probe, **61** vor jeder
  Bewertung einer Abweichung zwischen zwei Fassungen. **28**: die Welt im Prompt ist Feld für Feld
  die gemessene Welt.

### Splices

Ein Splice ist ein Skript mit `assert`, dass der Anker genau einmal vorkommt. Gefahren mit
`.venv/bin/python tools/splice_run.py /tmp/splice-*.py` (D225). **Die Meldung `AssertionError`
gefolgt von `zweiter Lauf gescheitert` ist die Erfolgsmeldung.**

- **Das Skript liegt in `/tmp`.** `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Das Skript wird erzeugt, nicht getippt.** Der Anker wird aus der Zieldatei **gelesen**, nicht
  abgeschrieben; in `00ak` hat eine Umschrift-Ersetzung einmal einen getippten Anker zerstört.
- **Ein Skript mit mehreren Paaren rechnet erst alles und schreibt dann.** In `00ak` hat genau das
  die Zieldatei gerettet, als ein Assert nach der Rechnung fiel.
- **Der Anker eines angehängten Blocks ist ein Präfix seiner eigenen Ersetzung.** Der Zweitlauf
  scheitert dann am **Eindeutigkeits-Assert**, nicht am Anker — und ein Anzahl-Assert allein
  genügt nicht: bei einem zweiten Anhängen stimmt die Differenz wieder.
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42); die Anzahl wird
  abgelesen, nicht gerechnet (Prüfregel 55).
- **Die Zeilenlängenprüfung des Harness greift nur bei `.md`.** Ein Splice auf eine `.py`-Datei
  ist zulässig.
- **Quellhash vor dem Schreiben, Zielhash nach dem Rechnen.**
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. Vor der Testzahl `.hypothesis` und `__pycache__`
löschen (Prüfregel 19). Prüfregel 40: der Kopf wird gemessen, nicht aus dieser Zeile abgeschrieben.

Nach `00ak`: **779 Tests** plus Eigenschaftstests. Register **D1–D301**, Prüfregeln **1–61** in
elf Abschnitten. **Drei Branches**. Keine offenen Läufe. Der Stand ist `2fa8f99`.

- **00** Nukleus, Genesis, Verfassung. `§7` nimmt die Föderationsstimme seit D235 aus.
- **01** Atom, Verifier, **zwölf Reject-Codes**, **sieben** Klassifikationszustände. `§3` trägt
  seit D270 den Arity-Satz. `§6` Punkt 4 führt seit D292 die drei `core/*`-Bedingungen einzeln.
  `§B.2` nennt seit D292 die Mängel, die `NON_CANONICAL_ENCODING` aufheben, **abschließend**, und
  stellt die Wahl unter mehreren wahren Codes ausdrücklich frei — der Absatz, der D299 entschieden
  hat. Anhang C trägt **sechzehn** Abschnitte; C.7 trägt seit D291 die signierte NV2-Fassung.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II. `§1.3` ist seit D276 die normative Form für jedes Lesen von `v`.
- **04** Governance. `§2.3` trägt seit D274 den Kanonizitätssatz, seit D276 die vier Lagen und
  seit D277 ihre Reihenfolge.
- **Fassade** (`mensch_als_republik/resolve.py`), **Kettenbauer** (`tests/kettenwelt.py`),
  **Werkzeugschicht** (`werkzeuge.md`), **Linter** `ruff` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py`, `tools/check_tree.py`,
  `tools/splice_run.py`, **`tools/korpus.py`**, **`tools/verdikt.py`**, **`tools/gitter.py`**.
- **Die Kampagne steht.** `korpus.py` liefert Anhang C als **40** Hexzeilen, `gitter.py` die
  Stufe-1-Mutanten als **2438** Zeilen in zwei Familien, `verdikt.py` je Eingabezeile eine
  Verdiktzeile in der Form der Go-Fassung: `ok <claim_id>` oder `reject <CODE>`.
- **Go-Fassung**: `~/mar-go`, `main` bei `127a74c`, **mit Remote** unter
  `git.h.error13.de/oli/mar-go`. Gebaut mit `~/sdk/go/bin/go build -o /tmp/margo .`, gefahren über
  stdin.

### Was `00ak` entschieden hat

- **D293** — Ort und Schnitt der Kampagne: Korpusbauer und Verdiktläufer im Repo, der Vergleich
  außerhalb. Das Repo ruft die Zweitfassung nie auf.
- **D294** — der Rückstand der Go-Fassung ist dokumentarisch; D290 wurde gemessen statt nachgezogen.
- **D295** — die Vektordatei war nicht an ihren Generator gebunden; ein Test bindet sie.
- **D296** — Prüfregel 60: eine Rücknahmeprobe wird an ihrem roten Test abgenommen, nicht an ihrer
  Anzahl.
- **D297** — die Operatorenmenge aus D289 erreicht fünf von zwölf Codes; drei Operatoren kommen
  hinzu, danach sind es zehn.
- **D298** — die Mutantenzahlen in D297 sind Prototypzahlen; die Wahl der Typmuster entscheidet
  sie, die Reichweite nicht.
- **D299** — erster Kampagnenlauf: 2438 Mutanten, **null Befunde**. Prüfregel 61.
- **D300** — der Registerindex lernt Anhangsverweise.
- **D301** — die Backslashes sind tragend; zwei bare Verweise bekommen die Dateinamensform.

## Was `00ak` gelehrt hat

**Der Vergleich zweier Fassungen misst nur, wo der Text etwas festlegt.** Der erste Lauf der
Kampagne meldete zwölf Abweichungen und enthielt keinen Befund: `01 §B.2` stellt die Wahl unter
mehreren wahren Codes frei. Der Supervisor hat daraus zwei Züge lang einen Fork gebaut, eine
Position bezogen, eine Literaturrecherche geführt, seine eigene Begründung zurückgenommen — und
erst danach den normativen Absatz gelesen. Prüfregel 38 hätte es im ersten Zug beendet.

**Ein Werkzeug, das den billigsten ersten Griff trägt, muss vollständig sein.** Der Index war
genau dort stumm, wo der Text stand. Ein Mangel an einem Prüfwerkzeug ist teurer als sein Umfang.

**Ein Posten auf der offenen Liste ist eine Behauptung.** Von drei angekündigten Kleinkram-Punkten
waren zwei keine Mängel. Messen war billiger als der Lauf.

**Ein Trennfall trennt nur, wenn beide Nachbarn ihn durchlassen.** Die Fälle mit Innen-Whitespace
hatten ungerade Länge und blieben am Längentor hängen; und selbst mit gerader Länge blieben sie
stumm, weil ihre Nutzlast ohnehin `MALFORMED_CBOR` ergab. Zwei Bedingungen, nicht eine.

**Ein Bericht, der nur zählt, kann eine Lücke nicht zeigen.** „Ein roter Test" war wahr und
nutzlos. Erst der Name zeigte, dass der falsche rot war.

**Der Blob-Hash im Diff macht die Rekonstruktion billig.** Fünfmal in `00ak` genutzt: Datei
nachbauen, `git hash-object`, gegen die `index`-Zeile. Danach misst man die Fassung statt ihrer
Beschreibung.

**Die eigene Zahl veraltet an der eigenen Entscheidung.** D300 nannte elf Einträge zu `01 §B.2`;
der Eintrag selbst nennt den Abschnitt und machte zwölf daraus.

## Der nächste Schritt

1. **Stufe 2 der Kampagne (D289).** Kombinationen aus zwei und drei Mängeln, aufgesetzt auf
   `tools/gitter.py`. Die zweistufige Auswertung aus D299 gilt von Anfang an: Stufe eins ist
   Annahme gegen Ablehnung oder verschiedene `claim_id`, Stufe zwei ist verschiedener Code bei
   geteilter Ablehnung und wird gegen die Auslöserspalte in `01 §B.2` beurteilt. Offene Vorfrage:
   ob die Kombinationsmenge vollständig aufgezählt oder gezogen wird — der Bestand hat 2438
   Einzelmutanten, das Paarprodukt wäre sechsstellig.
2. **Die Spec-Kopie unter `~/mar-go/spec` auf `2fa8f99` bringen.** Benannter Rückstand aus D294.
   Eine Dateikopie, kein Lauf.
3. **`01 §B.2` als Erreichbarkeitsgrenze prüfen.** Das Gitter erreicht zehn Codes;
   `NON_CANONICAL_ENCODING` ist bauartbedingt unerreichbar. Eine Familie, die **nicht** kanonisch
   neu kodiert, wäre die vierte und würde ihn erreichen.

## Offen

**In `00ak` gemessen:**

- **Die Spec-Kopie unter `~/mar-go/spec` trägt den Text vor `88361b2`.** Verhaltensgleich, aber
  der mit D290 eingefrorene Anker steht dort falsch.
- **Die Werkzeuge unter `tools/` sind über den Dateipfad nicht aufrufbar**, nur als Modul.
- **`test_b2_list_is_derived_from_register_text` leitet über eine Zeichenfolge ab, nicht über die
  Grammatik.** Entstünde je ein Abschnitt `B.2.1` oder `B.20`, würde er falsch rot (D300).
- **Die Feldkopie trägt keinen eigenen Reject-Code**, nur sechzehn eigene Annahmen — 466 Mutanten
  für sechzehn Beobachtungen (D298).
- **Vier Fünftel aller Mutanten enden in `MALFORMED_CBOR`.** Die Warnung aus D258 eine Ebene höher.
- **`FOREIGN_LIFECYCLE` ist auch vom Gitter unerreichbar**, weil es einen Speicher braucht (D268).

**Weiterhin offen, in `00ak` nicht neu gemessen:**

- **Anhang C ist gegen Generatordrift nur teilweise gesichert.** Für C.1 gibt es
  `test_tv1_core_bytes_match_spec` mit getipptem Hex; für C.13 bis C.15 gibt es nichts, was den
  Spec-Text an `vectors_01.json` bindet. Gegen einen Prüfer spricht D233. **Die andere Achse ist
  seit D295 geschlossen**: Datei gegen Generator.
- **`UNPARSABLE_V` entsteht bei `ratify@1` nicht.** Benannter Rückstand aus D276.
- **`cbor_canon.decode` ist tolerant und bleibt es.**
- **`FOREIGN_LIFECYCLE` hat keinen Vektor und kann keinen bekommen** (D263, D268).
- **`EPOCH_FORK` hat keinen Produktivträger** (D138, D176, bestätigt in D281).
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173).
- **Zwei Registerverweise zeigen ins Leere**, `03 §5.1` und `03 §11`. Bewusst nicht nachgezogen.
- **Die `einlesen-a-*`-Dateien behaupten, NV2 trage keine Drahtbytes.** Seit D291 falsch, bewusst
  nicht nachgezogen.
- **Ob `tests/profiles/test_credit.py` die einzige Python-Datei ohne Schluss-Newline ist, lässt
  sich aus der Projektkopie nicht messen.**
- **N09 ist beobachtet, nicht durchgesetzt** (D119, D246). **N10 ist teilgemessen** (D246).
- **`00z-anhangsform-prompt.md` trägt fünf um eins zu hohe Zeilenangaben** (D232).
- **`.claude/settings.local.json` landet in der Projektkopie**, obwohl git sie ignoriert.
- **Die Sitzungsstart-Datei ist ein monolithisches Rewrite** (D218).
- **Es gibt keine Kontextdatei für das Werkzeug** (D218).
- **Das Register ist knapp ein Viertel der Projektkopie** (D224, entschärft mit D225).
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
- **Braucht der Node eine eigene Beschreibung?** D180 sagt ausdrücklich nein.
- **Layer 05.** Mit D237 ausdrücklich zurückgestellt.

**Erledigt und nicht wieder aufzumachen:** die Zeilenlängenfrage für Python (D205). Der Fork aus
D197 (D200). Die Formfrage für `Finding.subject` (D207). Die Fangbreite der Prädikatprüfer (D213).
Die Zitierkonvention in allen vier Teilen (D219, D221, D227, D228, D230, D231, D232). Die
Zeilenlängenprüfung (D222). Das Nachziehverfahren (D224). Das Temp-Verzeichnis für Splices (D225).
Die zweite Prüfklasse für Verweisrichtigkeit (D233, mit Zahlen verworfen). Der Föderations-Fork
(D234, D235, D236). Die Zuordnung von Pflichten über Stichworte (D242). Die MUSS-Extraktion (D246).
Die Wahl Vektor statt Sondierwelt für `01 §5.3` (D250). Der Lookahead in der nuc-Regex (D255).
Reihenfolge und Umfang der Zweitimplementierung (D256, D258, D259). Die Abdeckung des Fehlerkanals
durch Anhang C (D257). Der Vergleichsgegenstand der Kanonizitätsprüfung (D261). Der Vorrang der
Fehlerklassen (D262, D265, ergänzt mit D292, angewandt in D299). Der Code für den falschen `J.tag`
auf `core/*` (D263). Die Feld-Konsistenz auf `core/*` (D264). Die Codes für Feldsatz-Verstöße
(D266). Der zwölfte Reject-Code (D267). Der Umfang einer Fassung ohne Speicher (D268). Die
Hex-Schnittstelle (D269). Die Arity der Eingabe (D270). Indefinite-Length und doppelte Keys (D271).
Der Rückstand von D266 im Code (D272). Die restlichen sechs Befundabschnitte (D273). Die
`v`-Kanonizität in der Auszählung (D274). Ort und Verdrängung von `NON_CANONICAL_V` (D275). Die
vier Lagen und `UNPARSABLE_V` (D276, D277). Der Träger für `superseded` (D278). Die Bindung der
Reject-Codewerte (D279). Die Vektoren für die Feldtabelle (D280). Die Vermerkskampagne (D281). Die
Prüfregeln 52 bis 59 (D282). Die überlebenden Erzeugerstellen (D283, D284, D285). Die
Zustandsmatrix (D286). Die zehn Doppelerzeuger (D287). Die Gliederung (D288). Die Bauform der
Mutation (D289). Der Anker der Kampagne (D290). Der zweite Mangel in NV2 (D291). Die Vorrangliste
und `§6` Punkt 4 (D292). **Ort und Schnitt der Kampagne (D293). Der Nachzug der Go-Fassung (D294).
Die Bindung der Vektordatei (D295). Prüfregel 60 (D296). Die Operatorenmenge (D297, D298). Der
erste Kampagnenlauf und Prüfregel 61 (D299). Die Anhangsverweise im Index (D300). Der Kleinkram
(D301).**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht.
