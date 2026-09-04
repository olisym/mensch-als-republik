# Sitzungsstart: 00aj (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, selbst gehostete Gitea-Instanz (`git.h.error13.de`). Das lokale
Arbeitsverzeichnis ist `~/mensch-als-republik`, daneben `~/mar-go` mit der unabhängigen
Zweitimplementierung von Layer 01 in Go.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 59, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer.

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird. **Der Index kennt nur `§<Ziffern>`** — Anhangsverweise wie `01 §C.13`
liefern eine leere Zeile, obwohl `check_specs.py` sie seit D230 prüft. Wer einen Anhang sucht,
greppt.

Was in `00ai` am meisten getragen hat:

- **Die Projektkopie wird ausgepackt und gefahren.** Aus `/tmp/mar-context.xml` lässt sich der
  ganze Baum rekonstruieren — geschnitten am `file`-Tag, die Newline hinter dem öffnenden und vor
  dem schließenden Tag gehören nicht zum Inhalt. `cbor2`, `cryptography`, `pytest`, `hypothesis`
  und `coverage` nachinstallieren, dann den Bestand fahren und die bekannte Testzahl reproduzieren:
  damit ist der Baum geeicht (Prüfregel 51). In `00ai` hat er zwei Mutantenkampagnen, elf vorab
  gerechnete Vektoren, zwölf vorab geeichte Rücknahmeproben und zwei Splice-Trockenläufe getragen.
  **Vorsicht bei Eigenschaften der Datei selbst:** das Auspackskript hängt jeder Datei eine
  Schluss-Newline an, also ist die Frage nach fehlenden Schluss-Newlines aus der Kopie **nicht**
  messbar.
- **Vier bis sechs Dateien aus der Kopie, von Oli mit `sha256sum -c` geprüft, verankern sie**
  (Prüfregel 59). Der Archivhash taugt nicht; der `--header-text` kann eine Sitzung alt sein.
- **Die gelieferte Fassung wird vor dem Prompt gebaut und gefahren, nicht nur beschrieben.** In
  `00ai` sind die elf Vektoren, die Testzahl und alle zwölf Rücknahmeproben vor dem Prompt im
  ausgepackten Baum gemessen worden. Zwei der zwölf Proben wären sonst stumm grün geblieben, weil
  ihr Tor doppelt geschützt ist. Die gerechneten Bytes bleiben beim Supervisor; der Prompt fixiert
  die Welten Feld für Feld.
- **Golden Numbers gehören nicht in den Prompt.**
- **Der Bericht ist nie die Abnahme, auch nicht der eigene** (Prüfregel 56).
- **Der Sitzungsstart ist eine Hypothese, keine Messung.** In `00ai` hat ein einziger Lesegriff
  gezeigt, dass der dort als „größter ungelöster Strukturpunkt" geführte Föderations-Fork
  vollständig entschieden **und** gebaut war. Wer die offene Liste ungeprüft weiterträgt, arbeitet
  an Gespenstern. Prüfregel 27 gilt auch für die eigene Übergabedatei.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`,
  `ruff`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.

### Shell

- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und
  eine Pipe auf `tail`, `awk` oder `grep -q` sind die nützlichen Ausnahmen. Nach Regel 39 sichert
  eine Zeile, die nur ausgibt, nichts: `test (git branch --show-current) = main` statt der Ausgabe.
- **Im Merge-Block steht `git push` vor `git branch -d`** (Prüfregel 58).
- **Sichtbar und geprüft zugleich geht über eine Datei.** `pytest -q > /tmp/x.txt`, dann
  `tail -1 /tmp/x.txt`, dann `grep -q '^654 passed' /tmp/x.txt`: ein Lauf, eine Ausgabe, ein
  Wächter. Eine Pipe würde eines von beidem fressen.
- **Mehrere Hashes prüft ein `printf` mit wiederholtem Format.** Ein Formatstring aus zwei
  Platzhaltern und Zeilenumbruch, dahinter die Paare aus Hash und Dateiname, die Ausgabe in
  `sha256sum -c`: eine Zeile, ein Wächter, kein Heredoc. `~/Downloads/...` wird darin expandiert.
- **`set -l` und verschachtelte Kommandosubstitution gehören nicht in einen Copy-Block.** Zahlen
  für den `--header-text` werden abgelesen und als Literal eingesetzt. Der **Kopf** ist die
  Ausnahme: `$(git rev-parse --short HEAD)` in doppelten Anführungszeichen hat in `00ah` und `00ai`
  viermal getragen. Ein `echo` des Headers vor dem Aufruf zeigt, ob die Kette so weit gekommen ist.
- **Keine Ausgabe heißt: der Block ist nicht gelaufen.**
- **Jeder Block trägt Marken.** Vor jedem Abschnitt ein `echo "== NAME =="`, am Ende ein
  `echo "== FERTIG =="`.
- **`string`-Kommandos in einer `and`-Kette sind eine Falle.** Sie geben Exit-Status 1 zurück,
  wenn sie nichts zu tun hatten. Kommandosubstitution entfernt Leerraum ohnehin selbst.
- **Kommandosubstitution in doppelten Anführungszeichen braucht `$`** — fish liest `"(cmd)"`
  wörtlich, `"$(cmd)"` führt aus.
- **Spec-Dateien, Prompts und Skripte als Download**, nicht als Copy-Block. Downloads landen in
  `~/Downloads`; der Kopierschritt nach `/tmp` gehört in den Block. **Eine Datei, die erzeugt und
  nicht ausgeliefert wurde, existiert für Oli nicht.**
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet`.
- Bei neuen Dateien `git add` **vor** `make check`. Explizite Pfade, nie `-A`.
- **Prosa bricht bei 100 Zeichen; Tabellenzeilen und Codeblöcke sind ausgenommen** (D222). Für
  Python gibt es **keine** Zeilenlängenregel (D205). Diese Datei ist **nicht** ausgenommen.
- **Eine Regex, die in einen Prompt oder eine Spec-Datei soll, geht nicht.** Regexänderungen
  werden in Prosa beauftragt.

### Die Zitiergrammatik — geschlossen

Seit D232 gibt es keinen offenen Teil. Vier Teile: der Dateiname mit oder ohne `.md`; die
Kurzform `NN`/`NNx` über `LAYER_FILES` (dreizehn Einträge, geschlossen); die Bereichsform
`NAME §A–§B` (D228, kein Leerraum um den Strich); die Anhangsnummer als Großbuchstabe mit Punkt
vor der Ziffernfolge (D230). Dazu die Backtick-Toleranz zwischen Namen und Paragraphenzeichen
(D231). Alles andere in `.py` ist ein Befund (D227); in `.md` bleibt der bare Verweis zulässig.

**Prüfregel 47:** ein Verweis und ein Inline-Code-Span werden nicht über die Zeilengrenze getrennt.

**Die Grenze, die bleibt:** die Prüfung sichert, dass das Ziel **existiert**, nicht dass es
**stimmt** (D229, mit Zahlen bestätigt in D233). Daraus folgt D250: ein Anhang wird **angehängt,
nicht eingeschoben**. In `00ai` ist das zum dritten Mal so gefahren worden; Anhang C in `01` steht
bei C.14.

**Ein Anhang ohne Ziffer ist kein Verweis.** `01 §A` matcht `SECTION_REF` nicht. Anhänge werden im
Klartext genannt. **Ein Prompt darf nicht auf einen Abschnitt zeigen, den erst sein Lauf erzeugt.**
**Befund-Dateien sind zitierfähig.**

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt, und in einem Wegwerf-Repo gerechnet.
  Eine **Ersetzung** ist eine Löschung plus eine Einfügung; nach Prüfregel 48 werden die
  randgleichen Zeilen abgezogen.
- **`tools/check_specs.py` zählt eine Zeile mehr als `wc -l`.**
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Aus einer Zeilennummer folgt kein Abschnitt.**
- **Zählvorschriften:** Registerköpfe `grep -c '^### D' 07-decisions.md`; Prüfregeln
  `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`; Branches `git branch -a | wc -l`; Abschnitte je Datei
  `grep -n '^## ' <datei>`.
- **Die Überdeckung geht der Mutation voraus** (Prüfregel 53). `coverage run --source=... -m pytest`
  trennt „nie erreicht" von „erreicht"; nur die zweite Klasse braucht Mutanten. In `00ai` hat das
  bei den Reject-Codes 16 von 19 überlebenden Mutanten vorab erklärt und bei 82 Vermerksstellen
  elf, bevor ein einziger Mutant lief.
- **Die Projektkopie wird nach jedem Push nachgezogen** (D224, Prüfregel 43), mit fünf Kaltzahlen
  im `--header-text`, Aufruf über
  `npx --yes repomix --header-text "..." -o /tmp/mar-context.xml`. **Das `-o` gehört dazu.**
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position,
  **40** vor jeder Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung,
  **43** vor jeder Zahl aus der Kopie, **44** vor jeder abgeleiteten Anzahl, **46** vor jeder
  Zeilenangabe, **49** vor jeder Rücknahmeprobe, **50** vor jedem Kriterium aus einem Modell,
  **51** vor jedem Prüfer, der eine Menge misst, **52** vor jeder Suche nach ungebundenem
  Verhalten, **53** vor jeder Mutantenkampagne, **59** vor jeder rekonstruierten Fassung.
  **28**: die Welt im Prompt ist Feld für Feld die gemessene Welt.

### Splices

Ein Splice ist ein Skript mit `assert`, dass der Anker genau einmal vorkommt. Gefahren mit
`python3 tools/splice_run.py /tmp/splice-*.py` (D225). Der Harness verlangt einen sauberen Baum,
erzwingt das Scheitern des zweiten Laufs, prüft die Zeilenlänge am Ergebnis und setzt bei jedem
Fehlschlag zurück. **Die Meldung `AssertionError` gefolgt von `zweiter Lauf gescheitert` ist die
Erfolgsmeldung**, nicht der Fehlerfall.

- **Das Skript liegt in `/tmp`.** `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Das Skript wird erzeugt, nicht getippt.** Anker und Ersetzung je als `repr`. Mehrere
  Anker-Paare in einer Liste sind billiger als mehrere Skripte.
- **Ein Skript mit mehreren Paaren rechnet erst alles und schreibt dann.** Aus `00ai`: die erste
  Fassung schrieb jede Datei sofort, der Zweitlauf des Harness wandte das erste Paar erneut an,
  bevor er am zweiten Anker scheiterte, und hinterließ 284 Registerköpfe statt 282. Der Anker eines
  angehängten Blocks ist ein Präfix seiner eigenen Ersetzung und matcht darum weiter. Alle Anker
  prüfen, alle Zielzahlen prüfen, dann schreiben.
- **Der Anker am Dateiende wird aus der Kopie abgelesen, nicht getippt.**
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42). Ein Assert auf
  eine erwartete **Anzahl** fängt mehr als eine Anwesenheitsprüfung — **und die Anzahl wird
  abgelesen, nicht gerechnet** (Prüfregel 55).
- **Quellhash vor dem Schreiben, Zielhash nach dem Rechnen.** Die Abnahme eines reinen
  Textschnitts liegt vollständig im Zielhash; Commit und Merge dürfen im selben Block stehen.
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`. Vor der Testzahl `.hypothesis` und `__pycache__` löschen
(Prüfregel 19). Prüfregel 40: der Kopf wird gemessen, nicht aus dieser Zeile abgeschrieben.

Nach `00ai`: **654 Tests** plus Eigenschaftstests. Register **D1–D282**, Prüfregeln **1–59**.
**Drei Branches**. Keine offenen Läufe. Der Stand nach D282 ist `aa0d974`.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`. `§7`
  nimmt die Föderationsstimme seit D235 ausdrücklich aus.
- **01** Atom, Verifier, **zwölf Reject-Codes**, **sieben** Klassifikationszustände. Prädikat-
  Grammatik in `§2.2` und Anhang A. `§3` trägt seit D270 den Arity-Satz. Anhang C trägt seit D280
  **fünfzehn** Abschnitte; C.14 belegt die Feldtabelle Zeile für Zeile mit NV20 bis NV30.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`. `§1.3` ist
  seit D276 die normative Form für jedes Lesen von `v` in jeder Schicht.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung. `§2.3` trägt seit D274 den
  Kanonizitätssatz für `v`, seit D276 die vier Lagen und seit D277 ihre Reihenfolge. `§7.2` und
  `§8` tragen seit D235 und D236 die Föderationsform und die Selbstblockade.
- **Fassade** (`mensch_als_republik/resolve.py`), **Kettenbauer** (`tests/kettenwelt.py`),
  **Werkzeugschicht** (`werkzeuge.md`), **Linter** `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py`, `tools/check_tree.py`,
  `tools/splice_run.py`.

### Was `00ai` entschieden hat

- **D279** — der Wert eines Reject-Codes ist seine Drahtform. Alle zwölf Werte überlebten die
  Sentinel-Mutation, weil `tests/test_verifier.py` über den **Membernamen** nachschlägt. Ein
  Träger über die Aufzählung bindet jetzt Name und Wert.
- **D280** — die Feldtabelle aus `01 §2` bekommt Zeile für Zeile einen negativen Vektor. Gemessen
  war: zwölf Tore, eines ausgelöst. D266 hatte vier Fälle benannt und drei davon nie einen Vektor
  bekommen; D272 hatte den Lauf beauftragt, die Vektoren dazuzulegen, und für `version` als CBOR
  `true` ist keiner entstanden. Elf Vektoren NV20 bis NV30, alle `MALFORMED_CBOR`.
- **D281** — die Vermerkskampagne. 48 Member an 82 Erzeugerstellen, elf Stellen nie erreicht,
  47 von 48 Mutanten gefangen. Einziger Überlebender: `EPOCH_FORK`, der nach D138 und D176 bewusst
  keinen Produktivträger hat. Nullbefund, kein Lauf.
- **D282** — Prüfregeln 52 bis 59 aus der geleerten Kandidatenliste.

## Was `00ai` gelehrt hat

**Die Abnahme läuft gegen das Geschuldete, nicht gegen das Gelieferte.** D266 hat vier Fälle
benannt, D272 hat einen Lauf beauftragt, die Vektoren dazuzulegen — und beide Abnahmen haben
geprüft, was ankam, statt was der Beschluss verlangte. Vier fehlende Vektoren sind so durch zwei
Abnahmen gelaufen. Wer einen Lauf abnimmt, liest den auslösenden Registereintrag neben dem Diff.

**Ein Tor ohne Test ist stärker, als es aussieht.** Gemessen an NV22: hängt man an ein gültiges
TV1 ein drittes Element in `J`, ohne die Signatur anzufassen, ist die Folge 343 Byte lang,
kanonisch, und trägt dieselbe `claim_id` wie die 309-Byte-Form — weil das Preimage aus der
zurückgeschnittenen Map gebaut wird. Genau der Angriff aus D272 an einer zweiten Stelle. Das
einzige, was ihn abfängt, ist das Längentor auf `J`, und das hatte keinen Test. Ein Typtor kann
eine Invariante tragen, die niemand ihm zugeschrieben hat.

**Überdeckung vor Mutation halbiert die Rechenzeit und schärft den Befund.** Von 19 überlebenden
Mutanten waren 16 nie erreicht — das ist ein anderer Befund als „erreicht und ungebunden" und
verlangt eine andere Antwort. Bei den Vermerken hat dieselbe Trennung elf von 82 Stellen erklärt,
bevor ein Mutant lief. Jetzt Prüfregel 53.

**Ein Nullbefund ist ein Ergebnis.** Die Vermerksschicht ist gebunden. Ohne die Messung wäre die
Vermutung „so dünn wie der Fehlerkanal" stehen geblieben und hätte irgendwann einen Lauf gekostet.

**Die offene Liste veraltet schneller als der Code.** Der Föderations-Fork stand als „größter
ungelöster Strukturpunkt" in der Übergabe und war in `00 §7`, `04 §7.2`, `04 §8` und
`example-nucleus.md §8.1` vollständig gebaut. Ein Lesegriff hat das gezeigt. Die Liste unten ist
in `00ai` einmal durchgemessen worden; was nicht nachgemessen werden konnte, ist als solches
markiert.

## Der nächste Schritt

1. **Die acht überlebenden Erzeugerstellen aus D280 und die zehn Doppelstellen aus D281.** Je
   Stelle eine Entscheidung: Träger bauen oder Code streichen. Der schärfste Einzelfall ist das
   zweite Versionstor hinter dem Aufbau des Claims — nach dem Kontrollfluss vermutlich
   **unerreichbar**, also toter Code. Das ist eine Ableitung und braucht eine Messung; eine
   Sondierwelt entscheidet es in einem Zug.
2. **Die Gliederung von `pruefregeln.md`** (D249). Bei 59 Regeln ist die Datei ohne Abschnitte
   nicht mehr überblickbar. Der Schnitt berührt jede Nummer und muss die Nummern stabil lassen.
3. **Die restlichen vierzehn Zustandspaare der Mutantenmatrix** (Mutationen nach `SUPERSEDED`,
   `EXPIRED`, `EQUIVOCATION_FLAGGED` und `ACTIVE`). Billig, mechanisch, kein Zug an Oli.
4. **Die Kampagne mit mutierten Claims** (D258), beschlossen und ungebaut.

**Zur dritten Fassung:** sie ist möglich, aber der Anker hat sich bewegt. Nach D258 muss sie
denselben Spec-Stand lesen wie die Go-Fassung — das ist `1109b89`, **nicht** der jetzige. Wer
gegen den reparierten Stand baut, misst die Reparatur und nicht die Häufung. Beides ist zulässig,
aber es sind zwei verschiedene Versuche, und die Wahl gehört ins Register.

## Offen

**Aus `00ai`, gemessen:**

- **Acht überlebende Erzeugerstellen außerhalb der Feldtabelle** (D280): das zweite Versionstor,
  das Tor für `FOREIGN_LIFECYCLE` in der Klassifikation und sein Duplikat im Index, das Formtor
  unter `nuc:` für einen Scope, der weder kanonisch noch Alias ist, das Tor für `core/*` in
  `resolve_scope`. Dazu drei erreichte, aber ungebundene Stellen.
- **Zehn tote Doppelerzeuger von Vermerken** (D281): `INVALID_V_TYPE` und `UNPARSABLE_V` je
  zweimal, dazu `MALFORMED_PARTICIPANTS`, `MALFORMED_THRESHOLD`, `SCOPE_MISMATCH`,
  `TALLY_UNEVALUABLE`, `UNKNOWN_ACCUSATION`, `UNPARSABLE_VOUCH_PAYLOAD`. Der Vermerk ist jeweils
  anderswo erzeugt und geprüft; die zweite Stelle ist es nicht.
- **`UNPARSABLE_V` entsteht bei `ratify@1` nicht.** Lage 2 behält dort `UNSUPPORTED_RATIFICATION`,
  weil D276 nur den Kandidatenfilter beschlossen hat. Benannter Rückstand.
- **`LINKED` hängt an genau einem Test** (D278). Nachgemessen in `00ai`: genau eine Fundstelle in
  `tests/test_verifier.py`.
- **Die Mutantenmatrix der Zustände ist unvollständig:** 28 von 42 Paaren gefahren. Die
  Reject-Codes und die Vermerke sind durch.
- **Wurzel-Markdowns tragen Backslashes.** Nachgemessen: 27 Zeilen in 23 Dateien, davon 19 in der
  `sitzungsstart`-Reihe — je eine, aus der Zählvorschrift für die Prüfregeln. Der eigentliche Rest
  sind **acht Zeilen in fünf Dateien**.
- **Ob `tests/profiles/test_credit.py` die einzige Python-Datei ohne Schluss-Newline ist, lässt
  sich aus der Projektkopie nicht messen** — das Auspackskript hängt jeder Datei eine an. Im Repo
  zu messen oder zu streichen.
- **`tools/register_index.py` indiziert keine Anhangsverweise.** Nachgemessen: `01 §C.13` liefert
  eine leere Zeile. Ein eigener Lauf, klein.
- **Der Verweis in `02b-abnahme.md` auf `§B.4` bleibt bar und ungeprüft.** Nachgemessen: Zeile 29,
  Ziel in derselben Datei vorhanden.
- **Zwei Registerverweise zeigen ins Leere**, `03 §5.1` und `03 §11`. Nachgemessen: `03-profiles.md`
  hat weder einen Unterabschnitt 5.1 noch einen Abschnitt 11. Bewusst nicht nachgezogen.
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173). Nachgemessen: neun Teststellen, alle auf
  `f.kind`, keine auf `f.subject`.

**Weiterhin offen, nicht neu gemessen:**

- **Anhang C ist gegen Generatordrift nur teilweise gesichert.** Für C.1 gibt es
  `test_tv1_core_bytes_match_spec` mit getipptem Hex; für C.13 und C.14 gibt es nichts, was den
  Spec-Text an `vectors_01.json` bindet. Gegen einen Prüfer spricht D233.
- **`cbor_canon.decode` ist tolerant und bleibt es.**
- **`FOREIGN_LIFECYCLE` hat keinen Vektor und kann keinen bekommen**, solange die Vektoren
  zustandslos gelesen werden (D263). Nach D268 liegt er als einziger Punkt außerhalb der
  selbstenthaltenen Gültigkeit.
- **`EPOCH_FORK` hat keinen Produktivträger** (D138, D176, bewusst; bestätigt in D281).
- **Die Gliederung von `pruefregeln.md` ab Regel 37** (D249).
- **N09 ist beobachtet, nicht durchgesetzt** (D119, D246). **N10 ist teilgemessen** (D246).
- **`00z-anhangsform-prompt.md` trägt fünf um eins zu hohe Zeilenangaben.** Bewusst nicht
  berichtigt (D232).
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
- **Vier `Finding`-Klassen, drei `dedupe_sort`** (D183, mit D207 berichtigt). Nachgemessen: vier
  `Finding`-Klassen, dazu `PolicyNote`; `trust/findings.py` hat kein `dedupe_sort`.
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
- **Meldung übersprungener Claims aus `store_laden`** — von D138 zurückgestellt.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** prüfen eine schwächere Aussage als sie
  scheinen (D117).
- **Dreifache Kantensumme in `test_deckenelastizitaet.py`** (D142, notiert, nicht blockierend).
- **`02d-purpose`** (D56), **VR-04.1** (D26), **Zeugenquorum für Fristen** (D100).
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **Braucht der Node eine eigene Beschreibung?** D180 sagt ausdrücklich nein.
- **Layer 05.** Mit D237 ausdrücklich zurückgestellt: Enforcement ohne beobachtete Verstöße ist
  Spekulation.

**Erledigt und nicht wieder aufzumachen:** die Zeilenlängenfrage für Python (D205). Der Fork aus
D197 (D200). Die Formfrage für `Finding.subject` (D207). Die Fangbreite der Prädikatprüfer (D213).
Die Zitierkonvention in allen vier Teilen (D219, D221, D227, D228, D230, D231, D232). Die
Zeilenlängenprüfung (D222). Das Nachziehverfahren (D224). Das Temp-Verzeichnis für Splices (D225).
Die zweite Prüfklasse für Verweisrichtigkeit (D233, mit Zahlen verworfen). **Der Föderations-Fork
in allen drei Fällen (D234, D235, D236) — entschieden und in `00 §7`, `04 §7.2`, `04 §8` und
`example-nucleus.md §8.1` gebaut; in `00ai` nachgelesen.** Die Zuordnung von Pflichten über
Stichworte (D242, mit Zahlen verworfen). Die MUSS-Extraktion selbst (D246). Die Wahl Vektor statt
Sondierwelt für `01 §5.3` (D250). Der Lookahead in der gedruckten nuc-Regex (D255). Reihenfolge
und Umfang der Zweitimplementierung (D256, D258, D259). Die Abdeckung des Fehlerkanals durch
Anhang C (D257). Der Vergleichsgegenstand der Kanonizitätsprüfung (D261). Der Vorrang der
Fehlerklassen (D262). Der Code für den falschen `J.tag` auf `core/*` (D263). Die Feld-Konsistenz
auf `core/*` (D264). Die Gesamtordnung der Fehlerklassen (D265). Die Codes für Feldsatz-Verstöße
(D266). Der zwölfte Reject-Code (D267). Der Umfang einer Fassung ohne Speicher (D268). Die
Hex-Schnittstelle des Auftrags (D269). Die Arity der Eingabe (D270). Die Lesart von
Indefinite-Length und doppelten Keys (D271). Der Rückstand von D266 im Code (D272). Die restlichen
sechs Befundabschnitte (D273). Die Geltung der `v`-Kanonizität in der Auszählung (D274). Der Ort
und die Verdrängung von `NON_CANONICAL_V` (D275). Die vier Lagen und `UNPARSABLE_V` (D276). Ihre
Reihenfolge (D277). Der Träger für `superseded` und die Löschung von `State.MALFORMED` (D278).
**Die Bindung der Reject-Codewerte (D279). Die Vektoren für die Feldtabelle (D280). Die
Vermerkskampagne (D281). Die Prüfregeln 52 bis 59 (D282).**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht.
