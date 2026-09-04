# Sitzungsstart: 00ae (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`). Das
lokale Arbeitsverzeichnis ist `~/mensch-als-republik`. **Neu seit `00ad`: ein zweites
Arbeitsverzeichnis `~/mar-go`** mit einer unabhängigen Zweitimplementierung von Layer 01 in Go.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 51, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer.

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird.

Was in `00ac` und `00ad` am meisten getragen hat:

- **Die Abnahme läuft über Zielhashes, nicht über gelesenen Diff.** Wird eine Änderung lokal gegen
  eine vollständige Kopie des Bestands gerechnet und dort mit der echten `check_specs.py` geprüft,
  dann belegt ein `sha256sum -c` der Ergebnisdateien byteweise, dass im Repo genau das entsteht,
  was geprüft wurde. Voraussetzung: die Projektkopie ist hash-gleich mit dem Repo, und die Prüfung
  läuft über **alle** Wurzel-`.md`, weil `check_specs.py` Verweise sonst nicht auflösen kann. In
  `00ad` sind so sechs Registereinträge ohne einen einzigen gelesenen Diff abgenommen worden.
- **Fremde Artefakte werden nachgerechnet, nicht gelesen.** Die acht Vektoren aus `00ad` wurden
  aus der Feldspezifikation des Prompts unabhängig neu berechnet und gegen drei Artefakte
  gehalten. Von den 175 Zeilen des Anhangs wurde keine gelesen; geprüft wurde, dass sie die
  gerechneten Werte enthalten. Das ist billiger und schärfer als Lesen.
- **Der Sitzungsstart ist eine Hypothese, keine Messung.** Der Übergabe-Commit dieser Datei liegt
  über dem hier genannten Stand.
- **Diagnoseläufe geben Zahlen aus, keine rohen Trefferlisten.** Die Liste gehört in eine Datei,
  die Zahl in die Antwort.
- **Vor jeder Position gegen fremden Code: die Trägermenge zählen** (D245, Prüfregel 49).
- **Der Bericht ist nie die Abnahme, auch nicht der eigene.** Bei reinen Registeranhängen genügt
  `numstat` plus die Asserts; bei Ersetzungen mitten in Layer-Dateien der Zielhash oder der
  vollständige Diff (D225).
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`, `ruff`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und
  eine Pipe auf `tail` oder `awk` sind die nützlichen Ausnahmen. Nach Regel 39 sichert eine Zeile,
  die nur ausgibt, nichts: `test (git branch --show-current) = main` statt der Ausgabe.
- **Jeder Block trägt Marken.** Vor jedem Abschnitt ein `echo "== NAME =="`, am Ende ein
  `echo "== FERTIG =="`. Fehlt die Schlussmarke in der zurückkopierten Ausgabe, ist die Kette
  abgebrochen — unabhängig davon, ob die letzte sichtbare Zeile erfolgreich aussieht.
- **`string`-Kommandos in einer `and`-Kette sind eine Falle.** `string trim`, `string match` und
  `string replace` geben Exit-Status 1 zurück, wenn sie nichts zu tun hatten. Als Wächter ist das
  nutzbar: `string match -q "*passed*" -- $testline` hält die Kette an, wenn die Testzeile fehlt.
- **Ein Wächter, der nur prüft, sagt nicht, was zu tun ist.** In den Merge-Block gehört
  `git checkout main` **vor** den Wächter, nicht statt seiner. `git branch -d` statt `-D`.
- **Kommandosubstitution in doppelten Anführungszeichen braucht `$`** — fish liest `"(cmd)"`
  wörtlich, `"$(cmd)"` führt aus.
- **Spec-Dateien und Skripte als Download**, nicht als Copy-Block. Downloads landen in
  `~/Downloads` — der Kopierschritt nach `/tmp` gehört in den Block. **Eine Datei, die erzeugt und
  nicht ausgeliefert wurde, existiert für Oli nicht**; das ist in `00ad` zweimal passiert und hat
  jedes Mal einen Umlauf gekostet.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet`.
- Bei neuen Dateien `git add` **vor** `make check`. Explizite Pfade, nie `-A`.
- **Prosa bricht bei 100 Zeichen; Tabellenzeilen und Codeblöcke sind ausgenommen** (D222). Für
  Python gibt es **keine** Zeilenlängenregel; D205 hat das mit Zahlen entschieden. Diese Datei ist
  **nicht** von der Zeilenlänge ausgenommen. Ein Hash gehört in einen Codeblock, wenn er sonst
  eine Prosazeile über die Grenze treibt.
- **Eine Regex, die in einen Prompt oder eine Spec-Datei soll, geht nicht.** Regexänderungen
  werden in Prosa beauftragt: welche Zeichenklasse, an welcher Stelle, optional oder nicht.

### Die Zitiergrammatik — geschlossen

Seit D232 gibt es keinen offenen Teil. Vier Teile: der Dateiname mit oder ohne `.md`; die
Kurzform `NN`/`NNx` über `LAYER_FILES` (dreizehn Einträge, geschlossen); die Bereichsform
`NAME §A–§B` (D228, kein Leerraum um den Strich); die Anhangsnummer als Großbuchstabe mit Punkt
vor der Ziffernfolge (D230). Dazu die Backtick-Toleranz zwischen Namen und Paragraphenzeichen
(D231). Alles andere in `.py` ist ein Befund (D227); in `.md` bleibt der bare Verweis zulässig.

**Prüfregel 47:** ein Verweis und ein Inline-Code-Span werden nicht über die Zeilengrenze
getrennt. Ein Umbruch dazwischen macht den Verweis unsichtbar, nicht falsch — die Prüfung bleibt
grün und sieht ihn nicht mehr.

**Die Grenze, die bleibt:** die Prüfung sichert, dass das Ziel **existiert**, nicht dass es
**stimmt** (D229, mit Zahlen bestätigt in D233). Daraus folgt unmittelbar D250: ein Anhang wird
**angehängt, nicht eingeschoben**, weil eine Umnummerierung genau der Fehlertyp ist, den die
Prüfung nicht sehen kann.

**Ein Anhang ohne Ziffer ist kein Verweis.** `01 §A` matcht `SECTION_REF` nicht. Anhänge werden im
Klartext genannt.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt. Eine **Ersetzung** ist eine Löschung
  plus eine Einfügung, und nach Prüfregel 48 werden die randgleichen Zeilen abgezogen.
- **Erwartete Zeilenzahlen werden abgeleitet, nicht getippt.** In `00ad` habe ich einmal `+50`
  angesagt, wo die eigene Messung `+49` ergeben hatte. Die Abnahme trug nur, weil sie über den
  Zielhash lief.
- **`tools/check_specs.py` zählt eine Zeile mehr als `wc -l`**, weil es die Umbrüche plus eins
  rechnet. Kein Widerspruch, nur zwei Zählweisen.
- **Prüfregel 46: aus der Projektkopie kommt jede absolute Zeilenangabe um eins zu hoch.** Wer
  eine Datei sauber aus dem Archiv extrahiert und den Hash gegen das Repo prüft, hat korrekte
  Zeilennummern.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Aus einer Zeilennummer folgt kein Abschnitt.** Die Zuordnung wird gegen die Überschriften
  gerechnet, immer.
- **Zählvorschriften:** Registerköpfe `grep -c '^### D' 07-decisions.md`; Prüfregeln
  `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`; Branches `git branch -a | wc -l`; Abschnitte je Datei
  `grep -n '^## ' <datei>`.
- **Die Projektkopie wird nach jedem Push nachgezogen** (D224, Prüfregel 43), mit fünf Kaltzahlen
  im `--header-text`, Aufruf über
  `npx --yes repomix --header-text "..." -o /tmp/mar-context.xml`. **Das `-o` gehört dazu.**
- **Die fünf Kaltzahlen werden ausgelesen, nicht abgetippt.** Der Nachzug steht am Kettenende und
  ist deshalb der erste Verlierer jedes stillen Abbruchs.
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position,
  **40** vor jeder Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung,
  **43** vor jeder Zahl aus der Kopie, **44** vor jeder abgeleiteten Anzahl, **46** vor jeder
  Zeilenangabe, **49** vor jeder Rücknahmeprobe, **50** vor jedem Kriterium aus einem Modell,
  **51** vor jedem Prüfer, der eine Menge misst. **28**: die Welt im Prompt ist Feld für Feld die
  gemessene Welt.

### Splices

Ein Splice ist ein Skript mit `assert`, dass der Anker genau einmal vorkommt. Gefahren mit
`python3 tools/splice_run.py /tmp/splice-*.py` (D225). Der Harness verlangt einen sauberen Baum,
erzwingt das Scheitern des zweiten Laufs, prüft die Zeilenlänge am Ergebnis und setzt bei jedem
Fehlschlag zurück.

- **Das Skript liegt in `/tmp`.** `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Das Skript wird erzeugt, nicht getippt.** Anker und Ersetzung je als `repr`.
- **Quellhash vor dem Schreiben, Zielhash nach dem Rechnen.** Ein Skript, das beide prüft, kann
  auf einem falschen Stand nichts anrichten und macht die Abnahme zu einem `sha256sum -c`.
- **Ein Anker am Dateiende braucht `endswith`, nicht nur `count == 1`.** Wer an ein Dateiende
  anhängt, prüft, dass der Anker das Dateiende **ist**. Der Anker wird aus der Kopie **abgelesen**,
  nicht aus dem Gedächtnis; in `00ad` ist ein Splice zweimal an einem erinnerten Schlusssatz
  gescheitert.
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42) — aber er prüft
  auch nur den **eingesetzten** Text auf Form. Ein Verbot von Backslashes über die ganze Datei
  scheitert an Bestand: `01-claim-atom.md` trägt in Zeile 55 ein maskiertes Sternchen.
- **Ein zu grober Assert stoppt zu Recht und kostet trotzdem einen Umlauf.** In `00ad` hat ein
  Schnittskript jede Nennung von `NV4` verboten, obwohl der normative Text Vektoren beim Namen
  nennen darf. Die Prüfung muss die **Daten** treffen, nicht die Erwähnung.
- **Mehrere Dateien in einem Skript**, wenn sie in denselben Commit gehören.
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`. Prüfregel 40: der Kopf wird gemessen, nicht aus dieser Zeile
abgeschrieben.

Nach `00ad`: **617 Tests** plus 14 Eigenschaftstests. Register **D1–D260**, Prüfregeln **1–51**.
**Drei Branches**. Keine offenen Läufe. Der Stand nach D260 ist `1109b89`.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
  `§7` zählt vier Nukleus-Akte auf; die Föderationsstimme ist ausdrücklich keiner.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A. Die Axiome A1 bis A3 stehen in `§1`. **Anhang C trägt seit D257 elf
  Abschnitte**: C.1 bis C.4 positiv, C.5 bis C.7 negativ, C.8 Byte-Vektoren, C.9 TV5, C.10 die
  acht Vektoren NV4 bis NV11. **Zehn der elf Reject-Codes haben damit einen Vektor.**
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung. `§7.2` trägt den benannten
  Föderationsschlüssel, `§8` die Selbstblockade als getragene Grenze.
- **Fassade** (`mensch_als_republik/resolve.py`), **Kettenbauer** (`tests/kettenwelt.py`),
  **Werkzeugschicht** (`werkzeuge.md`), **Linter** `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py`, `tools/check_tree.py`,
  `tools/splice_run.py`.

### Das zweite Arbeitsverzeichnis

`~/mar-go` ist ein eigenes Git-Repo **ohne Remote**, Commit `365df9b` auf `main`. Es enthält die
Go-Zweitimplementierung der zustandslosen Stufe von Layer 01: `main.go`, `cbor.go`, `verify.go`,
drei Testdateien, `go.mod`, dazu `AUFTRAG.md` und `spec/01-claim-atom.md` in der bei C.1
beschnittenen Fassung. 2039 Zeilen, eigenes deterministisches CBOR ohne Bibliothek, Signatur aus
der Standardbibliothek.

Go liegt in `~/.local/go` (1.27.0, in `00ad` installiert) und ist **nicht im PATH**. Aufruf über
`~/.local/go/bin/go`. Die Prüfsummen-URL `go.dev/dl/<v>.linux-amd64.tar.gz.sha256` liefert nichts
Brauchbares; die Summe steht in `go.dev/dl/?mode=json&include=all`.

Der Hash der beschnittenen Spec, gegen die gebaut wurde:

```
b16251fc02d07c8761a0583fe77ddadd6a6f59e6b7167d889231733170cc051a
```

**`~/mar-go/FRAGEN.md` trägt siebzehn Einträge und liegt in keinem Remote.** Die Datei ist der
Hauptertrag von `00ad` und existiert nur auf der lokalen Platte. Sie ins MaR-Repo zu übernehmen
ist der erste Schritt in `00ae`.

**Neu in `00ad`:** D255 bis D260, Prüfregel 51, ein Werkzeug-Lauf, vier Splices und die erste
Außenmessung, die `01` je hatte.

- **D255** — der negative Lookahead in der zusammengesetzten nuc-Regex bekommt seinen Anker
  angepasst statt gestrichen. Gemessen: die gedruckte Fassung schützt bei getauschter
  Alternativenreihenfolge exakt so wenig wie gar kein Lookahead, nämlich 25502 Fehlklassifikationen
  über 200000 Kandidaten; mit dem auf den Schrägstrich gezogenen Anker sind es null. Die Fehlklasse
  war ein nicht mitgeführter Anker beim Einsetzen einer verankerten Teilregex.
- **D256** — Vorentscheidung zur Zweitimplementierung: erst die Messfläche, dann die
  Implementierung; Umfang ist die zustandslose Stufe; gemessen wird gegen die Vektoren und nicht
  gegen die Referenzausgabe. Ein falscher Vektor ist besser als keiner, weil ein fehlender
  Schweigen erzeugt.
- **D257** — acht negative Vektoren NV4 bis NV11 für sieben Fehlerklassen, jeder mit genau einem
  Mangel. Dazu Prüfregel 51.
- **D258** — Sprache ist Go, und die Wahl ist ausdrücklich keine methodische. Der Prompt für eine
  Zweitimplementierung ist **minimal**, was die sonstigen Prompt-Regeln umkehrt. Alle Fassungen
  lesen denselben Spec-Stand.
- **D259** — die Zweitimplementierung sieht genau eine Datei, bei C.1 abgeschnitten, in einem
  eigenen Verzeichnis ohne Sicht auf Python.
- **D260** — das Ergebnis: 18 von 19 Vektoren deckungsgleich, achtzehn davon blind, siebzehn
  Einträge in der Fragenliste.

## Was `00ad` gelehrt hat

**Der Ertrag einer Zweitimplementierung liegt in der Fragenliste, nicht in der Abweichungszahl.**
Achtzehn Treffer haben null Befunde erzeugt, die eine Abweichung einen, die Liste siebzehn. Wer
nur gegen Vektoren misst, wirft den Hauptteil weg.

**Zwei einige Implementierungen können beide falsch liegen, und das ist messbar.** `01 §3` verlangt
wörtlich, den dekodierten Core mit den empfangenen Bytes zu vergleichen — der Core ist die Map ohne
Signatur, die empfangenen Bytes enthalten sie. Wörtlich befolgt lehnt die Regel jeden signierten
Claim ab. Beide Fassungen haben unabhängig dieselbe vernünftige Lesart gewählt; kein Vektor kann
das sehen. Genau diese Korrelation, die Knight und Leveson 1986 als Schwäche der Methode gemessen
haben, ist hier der Zeiger auf den Defekt.

**Die Literatur zur Sprachwahl ist eindeutig und unbequem.** Eine Wiederholung des
Knight-Leveson-Versuchs mit Coding-Agents (Juni 2026, 48 Fassungen, eine Million Eingaben) misst
429 gleichzeitige Ausfälle gegen 115,36 erwartete. Von 146 sprachübergreifenden Paaren mit
definierter Korrelation liegen 81 bei genau eins. Sprachwechsel entkoppelt nicht; die Sprache ist
der schwächste der drei Hebel Werkzeug, Modell und Sprache.

**Ein Vektorsatz mit genau einem Mangel je Stück ist gegen Reihenfolgefragen blind.** Die einzige
Abweichung der Messung sitzt am einzigen Vektor mit zwei Mängeln. Das ist kein Zufall, sondern die
Kehrseite des Konstruktionsprinzips aus D257.

**Ein geeichter Prüfer ist etwas anderes als ein reagierender.** Prüfregel 51 stammt aus einem
eigenen Fehler: ein Diagnoseskript meldete gegen den Vorzustand pflichtgemäß null und gegen den
Zielzustand ebenfalls null, weil es den falschen Wert suchte. Die Rücknahmeprobe sichert die
Richtung, nicht den Maßstab.

**Der Bericht des Werkzeugs war belastbar, mein Verdacht nicht.** Go fehlte im PATH, und ich hielt
für möglich, dass 2039 Zeilen nie übersetzt wurden. Der Bauversuch hat das widerlegt: Cursor hatte
eine eigene Toolchain. Der Verdacht war zulässig, seine Auflösung gehörte in denselben Zug.

## Der nächste Schritt

1. **`FRAGEN.md` ins MaR-Repo übernehmen**, als `00ad-fragen-befund.md`. Vorher die längste
   Zeichenlänge messen: die Datei stammt aus fremder Hand und ist nicht auf 100 Zeichen gebrochen.
   Ohne diesen Schritt existiert der Hauptertrag von `00ad` nur lokal.
2. **`01 §3` reparieren.** Der Durchsetzungssatz kommt genau einmal vor. Die vorbereitete Fassung
   ersetzt den dekodierten Core durch die dekodierte Map und ergänzt einen Satz, der sagt, warum:
   der Core kommt in den empfangenen Bytes nie für sich vor. Registereintrag zuerst, dann ein
   Splice über `01-claim-atom.md` und `07-decisions.md` in einem Commit.
3. **Den BV2-Beschluss aus D260 fassen.** Der Ausgang bleibt, die Begründung nicht: BV2 beruft
   sich auf eine Prüfreihenfolge aus `01 §6`, die er als 2b vor 2c benennt. Diese Nummerierung
   kommt in der ganzen Datei genau einmal vor, nämlich dort, und stammt aus den Kommentaren von
   `verifier.py`. Der Hauptteil nennt die kanonische Kodierung in seiner Aufzählung sogar zuerst,
   und die Einleitung von C.8 sagt ausdrücklich, die Reihenfolge sei gleichgültig. Entweder der
   Hauptteil normiert die Reihenfolge, oder BV2 verliert seine Berufung.
4. **Die beiden messbaren Abweichungen ohne Vektor.** Erstens: die Auslösebedingung der
   Lifecycle-Fremdheit ohne Store — Go meldet sie beim falschen J-Tag, Python meldet dort die
   Kodierungsklasse. Zweitens: ob die Feldkonsistenz von `t` und `t_exp` auf `core/*` mitentfällt,
   wenn die Ablaufzeit dort ignoriert wird. Beide brauchen einen Vektor, sobald sie entschieden
   sind.
5. **Die restlichen dreizehn Einträge der Fragenliste**, einzeln geprüft und einzeln entschieden.
6. **Die Gliederung von `pruefregeln.md`.** Die angekündigte Ordnung nach dem Zeitpunkt, an dem
   eine Regel greift, ist ab Nummer 37 faktisch die Ordnung ihrer Entstehung. Umsortieren würde
   Nummern brechen — die Frage ist, ob die Überschriften nachgezogen werden.

**Nicht vergessen:** eine dritte Fassung ist möglich, aber erst sinnvoll, wenn die siebzehn Fragen
abgearbeitet sind. Nach D258 muss sie denselben Spec-Stand lesen wie die Go-Fassung, also
`1109b89` beziehungsweise die daraus beschnittene Datei — nicht einen reparierten. Sonst ist die
Häufung nicht auswertbar.

## Offen

- **Die dreizehn unbehandelten Einträge aus `~/mar-go/FRAGEN.md`** (D260).
- **`01 §3`: Core gegen empfangene Bytes** — die Reparatur ist formuliert, nicht beschlossen.
- **BV2s Berufung auf eine Nummerierung aus `verifier.py`** (D260).
- **Die Gliederung von `pruefregeln.md` ab Regel 37** (D249).
- **Ein Kandidat ohne Nummer** (D249): eine neu formulierte Norm wird vor dem Commit gegen die
  offenen Befunde derselben Sitzung gehalten. Einziger Anlass ist D248.
- **Siebzehn Wurzel-Markdowns tragen Backslashes**, obwohl die Anweisung keine vorsieht.
  Ungeprüft, ob das je eine Rolle spielt; `check_specs.py` beanstandet es nicht.
- **Der elfte Reject-Code hat keinen Vektor**: sein aktiver Träger sitzt nach D138 in der
  Zustandsprüfung und verlangt ein bekanntes Ziel (D257).
- **Die Kampagne mit mutierten Claims** ist beschlossen und ungebaut (D258). Zufällige Bytes
  liefern fast durchweg dieselbe Fehlerklasse; die Bauform der Mutation ist offen.
- **N09 ist beobachtet, nicht durchgesetzt** (D119, D246). Der Vermerk bleibt ohne Wirkung auf den
  Fluss; so beschlossen.
- **N10 ist teilgemessen** (D246). Drei Erzeugungsstellen für `INVALID_V_TYPE` in `credit.py`, eine
  Teststelle. `verdict.py` erzeugt den Vermerk nirgends.
- **`00z-anhangsform-prompt.md` trägt fünf um eins zu hohe Zeilenangaben.** Bewusst nicht
  berichtigt (D232): die Datei beschreibt einen vergangenen Lauf.
- **Der Verweis in `02b-abnahme.md` auf B.4 bleibt bar und ungeprüft.**
- **`tests/profiles/test_credit.py` ist die einzige Python-Datei ohne Schluss-Newline.**
- **`.claude/settings.local.json` landet in der Projektkopie**, obwohl git sie ignoriert.
- **Die Sitzungsstart-Datei ist ein monolithisches Rewrite** (D218).
- **Es gibt keine Kontextdatei für das Werkzeug** (D218).
- **Das Register ist knapp ein Viertel der Projektkopie** (D224, entschärft mit D225).
- **Die Verweisprüfung kann Listenpunkte nicht von Unterabschnitten unterscheiden** (D209).
- **Der Harness vergleicht Zeilenzahlen, er identifiziert Zeilen nicht** (D226).
- **Zwei Registerverweise zeigen ins Leere**, `03 §5.1` und `03 §11`. Bewusst nicht nachgezogen.
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173).
- **Die Sondierwelt in `test_benennung.py` erzeugt keine Vermerke** (D173).
- **Wie weit die Regierbarkeitsprüfung reicht** (D200). Zurückgestellt — **nicht vorher aufmachen**.
- **`RATIFY_WITH_EXPIRY` und der Zeugenpfad tragen die Weitergaberegel ungeprüft** (D203).
- **Vergleiche gegen `dedupe_sort` sind für die Reihenfolge zirkulär** (D196).
- **Vier `Finding`-Klassen, drei `dedupe_sort`** (D183, mit D207 berichtigt).
- **Eine Schwelle für Autoritätslisten** — mit D166 zurückgestellt, für alle drei Listen zugleich
  oder gar nicht. Nach D236 zusätzlich beleuchtet: alle drei tragen dasselbe Bearer-Problem.
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
- **`FOREIGN_LIFECYCLE` und `EPOCH_FORK` haben keinen Produktivträger** (D138, D176, bewusst).
- **Meldung übersprungener Claims aus `store_laden`** — von D138 zurückgestellt.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** prüfen eine schwächere Aussage als sie
  scheinen (D117). Der Vorbehalt steht in `04-golden-anchors.md §8`.
- **Dreifache Kantensumme in `test_deckenelastizitaet.py`** (D142, notiert, nicht blockierend).
- **`02d-purpose`** (D56), **VR-04.1** (D26), **Zeugenquorum für Fristen** (D100).
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **Braucht der Node eine eigene Beschreibung?** D180 sagt ausdrücklich nein.
- **Layer 05.** Mit D237 ausdrücklich zurückgestellt: Enforcement ohne beobachtete Verstöße ist
  Spekulation. Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf), die Beta-Reputation
  mit dem Moral-Licensing-Problem, und seit D178 die Frage nach wiederholtem Stimmen auf
  unveröffentlichte Vorschläge.

**Erledigt und nicht wieder aufzumachen:** die Zeilenlängenfrage für Python (D205). Die dritte
`ruff`-Gruppe. Der Fork aus D197 (D200). Die Formfrage für `Finding.subject` (D207). Ein
Übersichtsdokument über die Schichten (D209, verworfen). Die Fangbreite der Prädikatprüfer (D213).
Die Löschung von `is_nuc_predicate` (D216). Die Zitierkonvention in allen vier Teilen (D219, D221,
D227, D228, D230, D231, D232). Die Zeilenlängenprüfung (D222). Das Nachziehverfahren (D224). Das
Temp-Verzeichnis für Splices (D225). Ein eigener Test für `tools/` (D229, verworfen). Die zweite
Prüfklasse für Verweisrichtigkeit (D233, mit Zahlen verworfen). Die Föderationsstimme (D235), der
Ausschlussmechanismus (D236). Der Reflow der Stummelzeilen (D238). Die Zuordnung von Pflichten
über Stichworte (D242, mit Zahlen verworfen). Die MUSS-Extraktion selbst (D246) — mit der Grenze
aus D243. Die Nummerierung der Prüfregeln 47 bis 51 (D249, D254, D257). Die Wahl Vektor statt
Sondierwelt für `01 §5.3` (D250). Die Löschung der beiden Lookaheads in `predicates.py` (D251,
ausdrücklich zurückgenommen). Der Zustand von N02 und N07 (D250, D253, D254). **Der Lookahead in
der gedruckten nuc-Regex (D255, angepasst statt gestrichen; D252 damit geschlossen). Die
Reihenfolge Messfläche vor Implementierung und der Umfang der zustandslosen Stufe (D256). Die
Abdeckung des Fehlerkanals durch Anhang C (D257). Sprache, Prompt-Form und Spec-Anker der
Zweitimplementierung (D258). Was die Zweitimplementierung sehen darf (D259).**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht.
