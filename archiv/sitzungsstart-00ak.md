# Sitzungsstart: 00ak (MaR)

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
Volltext, mit stabilen Nummern. Seit D288 hat die Datei **elf Abschnitte** entlang des
Arbeitsbogens; die Nummern stehen darin **nicht** in Reihenfolge. Wer eine Regel sucht, sucht den
Zeitpunkt, an dem sie greift, nicht die Zahl.

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird. **Der Index kennt nur `§<Ziffern>`** — Anhangsverweise wie `01 §C.15`
liefern eine leere Zeile. Wer einen Anhang sucht, greppt.

Was in `00aj` am meisten getragen hat:

- **Die Projektkopie wird ausgepackt und gefahren.** Aus `/tmp/mar-context.xml` lässt sich der
  ganze Baum rekonstruieren — geschnitten am `file`-Tag, die Newline hinter dem öffnenden und vor
  dem schließenden Tag gehören nicht zum Inhalt. `cbor2`, `cryptography`, `pytest`, `hypothesis`,
  `coverage` und `ruff` nachinstallieren, dann den Bestand fahren und die bekannte Testzahl
  reproduzieren: damit ist der Baum geeicht (Prüfregel 51). In `00aj` hat er zwei
  Mutantenkampagnen mit zusammen 74 Läufen, elf vorab gebaute Träger, fünfzehn vorab geeichte
  Rücknahmeproben, drei Splice-Trockenläufe und den vollständigen Nachbau zweier
  Werkzeuglieferungen getragen. **Vorsicht bei Eigenschaften der Datei selbst:** das Auspackskript
  hängt jeder Datei eine Schluss-Newline an.
- **Die gelieferte Fassung wird vor dem Prompt gebaut und gefahren, nicht nur beschrieben.** In
  `00aj` waren zwei von zehn Trägern grün, ohne ihre Zielzeile zu erreichen, und eine von elf
  Rücknahmeproben wäre stumm geblieben. Alle drei sind vor dem Prompt gefunden worden.
- **Golden Numbers gehören nicht in den Prompt.**
- **Der Bericht ist nie die Abnahme, auch nicht der eigene** (Prüfregel 56).
- **Der Sitzungsstart ist eine Hypothese, keine Messung.** Prüfregel 27 gilt auch für diese Datei.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`,
  `ruff`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.

### Shell

- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und
  eine Pipe auf `tail`, `cat`, `awk` oder `grep -q` sind die nützlichen Ausnahmen. Nach Regel 39
  sichert eine Zeile, die nur ausgibt, nichts: `test (git branch --show-current) = main` statt der
  Ausgabe.
- **`grep -c` liefert bei null Treffern Status 1.** Eine Zählzeile, die null ergeben *darf*, geht
  auf `| cat`, sonst bricht die Kette genau dann ab, wenn alles in Ordnung ist.
- **`go` liegt nicht im `PATH`.** Die Toolchain steht unter `~/sdk/go/bin/go`.
- **Im Merge-Block steht `git push` vor `git branch -d`** (Prüfregel 58).
- **Sichtbar und geprüft zugleich geht über eine Datei.** `make check > /tmp/x.txt`, dann
  `tail -1 /tmp/x.txt`, dann `grep -q '^669 passed' /tmp/x.txt`.
- **Mehrere Hashes prüft ein `printf` mit wiederholtem Format**, Ausgabe in `sha256sum -c`.
- **`set -l` und verschachtelte Kommandosubstitution gehören nicht in einen Copy-Block.** Zahlen
  für den `--header-text` werden abgelesen und als Literal eingesetzt.
- **Keine Ausgabe heißt: der Block ist nicht gelaufen.**
- **Jeder Block trägt Marken.** Vor jedem Abschnitt ein `echo "== NAME =="`, am Ende ein
  `echo "== FERTIG =="`.
- **`string`-Kommandos in einer `and`-Kette sind eine Falle.** Sie geben Exit-Status 1 zurück,
  wenn sie nichts zu tun hatten.
- **Kommandosubstitution in doppelten Anführungszeichen braucht `$`.**
- **Spec-Dateien, Prompts und Skripte als Download**, nicht als Copy-Block. **Eine Datei, die
  erzeugt und nicht ausgeliefert wurde, existiert für Oli nicht.**
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet`.
- Bei neuen Dateien `git add` **vor** `make check`. Explizite Pfade, nie `-A`.
- **Prosa bricht bei 100 Zeichen; Tabellenzeilen und Codeblöcke sind ausgenommen** (D222). Für
  Python gibt es **keine** Zeilenlängenregel (D205). Diese Datei ist **nicht** ausgenommen.
- **Eine Regex, die in einen Prompt oder eine Spec-Datei soll, geht nicht.** Regexänderungen
  werden in Prosa beauftragt.

### Die Zitiergrammatik — geschlossen

Seit D232 gibt es keinen offenen Teil. Vier Teile: der Dateiname mit oder ohne `.md`; die
Kurzform `NN`/`NNx` über `LAYER_FILES`; die Bereichsform `NAME §A–§B` (D228, kein Leerraum um den
Strich); die Anhangsnummer als Großbuchstabe mit Punkt vor der Ziffernfolge (D230). Dazu die
Backtick-Toleranz (D231). Alles andere in `.py` ist ein Befund (D227); in `.md` bleibt der bare
Verweis zulässig.

**Prüfregel 47:** ein Verweis und ein Inline-Code-Span werden nicht über die Zeilengrenze getrennt.

**Die Grenze, die bleibt:** die Prüfung sichert, dass das Ziel **existiert**, nicht dass es
**stimmt** (D229, mit Zahlen bestätigt in D233). Daraus folgt D250: ein Anhang wird **angehängt,
nicht eingeschoben**. Anhang C in `01` steht bei C.15.

**Ein Anhang ohne Ziffer ist kein Verweis.** **Ein Prompt darf nicht auf einen Abschnitt zeigen,
den erst sein Lauf erzeugt.** **Befund-Dateien sind zitierfähig.**

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt. Eine **Ersetzung** ist eine Löschung
  plus eine Einfügung; nach Prüfregel 48 werden die randgleichen Zeilen abgezogen.
- **`tools/check_specs.py` zählt eine Zeile mehr als `wc -l`.**
- **Zeichen zählen, nicht Bytes.**
- **Aus einer Zeilennummer folgt kein Abschnitt.**
- **Zählvorschriften:** Registerköpfe `grep -c '^### D' 07-decisions.md`; Prüfregeln
  `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`; Branches `git branch -a | wc -l`.
- **Die Überdeckung geht der Mutation voraus** (Prüfregel 53).
- **Die Überdeckung prüft auch den Träger, nicht nur den Mutanten.** Ein Test, der grün ist und
  seine Zielzeile nicht erreicht, prüft ein Nachbartor. In `00aj` hat ein einziger
  Überdeckungslauf zwei von zehn Trägern so entlarvt — dieselbe Arbeit hätten zehn
  Rücknahmeproben geleistet. Das ist der billige Vorlauf von Prüfregel 49, keine eigene Regel.
- **Die Projektkopie wird nach jedem Push nachgezogen** (D224, Prüfregel 43), mit fünf Kaltzahlen
  im `--header-text`, Aufruf über
  `npx --yes repomix --header-text "..." -o /tmp/mar-context.xml`. **Das `-o` gehört dazu.**
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position,
  **40** vor jeder Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung,
  **43** vor jeder Zahl aus der Kopie, **44** vor jeder abgeleiteten Anzahl, **46** vor jeder
  Zeilenangabe, **49** vor jeder Rücknahmeprobe, **50** vor jedem Kriterium aus einem Modell,
  **51** vor jedem Prüfer, der eine Menge misst, **53** vor jeder Mutantenkampagne, **59** vor
  jeder rekonstruierten Fassung. **28**: die Welt im Prompt ist Feld für Feld die gemessene Welt.

### Splices

Ein Splice ist ein Skript mit `assert`, dass der Anker genau einmal vorkommt. Gefahren mit
`.venv/bin/python tools/splice_run.py /tmp/splice-*.py` (D225). **Die Meldung `AssertionError`
gefolgt von `zweiter Lauf gescheitert` ist die Erfolgsmeldung.**

- **Das Skript liegt in `/tmp`.** `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Das Skript wird erzeugt, nicht getippt.**
- **Ein Skript mit mehreren Paaren rechnet erst alles und schreibt dann.**
- **Der Anker eines angehängten Blocks ist ein Präfix seiner eigenen Ersetzung.** Der Zweitlauf
  scheitert dann nicht am Anker, sondern am **Anzahl-Assert** — und der muss deshalb *vor* jedem
  Schreiben stehen. In `00aj` haben vier Splices genau so geschlossen.
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42); die Anzahl wird
  abgelesen, nicht gerechnet (Prüfregel 55).
- **Die Zeilenlängenprüfung des Harness greift nur bei `.md`.** Ein Splice auf eine `.py`-Datei
  ist zulässig und in `00aj` einmal gefahren worden.
- **Quellhash vor dem Schreiben, Zielhash nach dem Rechnen.**
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. Vor der Testzahl `.hypothesis` und `__pycache__`
löschen (Prüfregel 19). Prüfregel 40: der Kopf wird gemessen, nicht aus dieser Zeile abgeschrieben.

Nach `00aj`: **669 Tests** plus Eigenschaftstests. Register **D1–D292**, Prüfregeln **1–59** in
elf Abschnitten. **Drei Branches**. Keine offenen Läufe. Der Stand ist `3b33cdf`.

- **00** Nukleus, Genesis, Verfassung. `§7` nimmt die Föderationsstimme seit D235 aus.
- **01** Atom, Verifier, **zwölf Reject-Codes**, **sieben** Klassifikationszustände. `§3` trägt
  seit D270 den Arity-Satz. `§6` Punkt 4 führt seit D292 die drei `core/*`-Bedingungen einzeln.
  `§B.2` nennt seit D292 die Mängel, die `NON_CANONICAL_ENCODING` aufheben, **abschließend**.
  Anhang C trägt **sechzehn** Abschnitte; C.7 trägt seit D291 die signierte NV2-Fassung.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II. `§1.3` ist seit D276 die normative Form für jedes Lesen von `v`.
- **04** Governance. `§2.3` trägt seit D274 den Kanonizitätssatz, seit D276 die vier Lagen und
  seit D277 ihre Reihenfolge.
- **Fassade** (`mensch_als_republik/resolve.py`), **Kettenbauer** (`tests/kettenwelt.py`),
  **Werkzeugschicht** (`werkzeuge.md`), **Linter** `ruff` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py`, `tools/check_tree.py`,
  `tools/splice_run.py`.
- **Go-Fassung**: `~/mar-go`, `main` bei `127a74c`, auf dem Spec-Stand `b3cf487`, 40 von 40
  Vektoren grün. **Kein Remote** — die Zweitimplementierung liegt nur auf einer Platte.

### Was `00aj` entschieden hat

- **D283** — die fünf nie erreichten Erzeugerstellen: zwei unerreichbar und gestrichen (zweites
  Versionstor, Formtor unter `nuc:`), drei mit Träger. Die Zahl aus D280 war zu hoch.
- **D284** — `resolve_scope` auf `core/*` wirft `ValueError`, keinen Reject-Code.
- **D285** — NV31, `01 §C.15`: die zehn TV1-Werte als Array statt als Map, 299 Byte.
- **D286** — die Zustandsmatrix ist vollständig, 42 von 42 Paaren gefangen. Nullbefund.
- **D287** — die zehn Doppelerzeuger aus D281 sind erreichbar und haben je einen Träger.
- **D288** — `pruefregeln.md` bekommt elf Abschnitte, die Nummern bleiben.
- **D289** — Bauform der Mutationskampagne, nach Literaturprüfung: erst das vollständige Gitter,
  dann die Kombinationen.
- **D290** — der Anker der Kampagne ist der laufende Stand; die Go-Fassung wird nachgezogen, der
  Preis ist benannt.
- **D291** — NV2 bekommt seine Signatur; der Vektor trug zwei Mängel statt einem.
- **D292** — der Vorrang in `B.2` nennt seine Fälle abschließend, `§6` Punkt 4 wird aufgeteilt.

## Was `00aj` gelehrt hat

**Die Zweitfassung findet Defekte, bevor eine einzige Mutation läuft.** Der Nachzug der Go-Fassung
auf den heutigen Text hat drei Spec-Defekte erzeugt: den zweifachen Mangel in NV2, die
unvollständige Vorrangliste und die Konjunktion in `§6` Punkt 4. Alle drei lösen Referenz und
Go-Fassung gleich auf — eine Mehrdeutigkeit, die alle gleich auflösen, sieht von innen niemand.

**Eine Norm im Anhang ist keine Norm.** D285 hat mit `C.15` entschieden, dass eine Bytefolge ohne
Map an der Spitze `MALFORMED_CBOR` ist. Drei Sitzungen später musste die Go-Fassung dasselbe neu
entscheiden, weil der Vorrangsatz in `B.2` den Fall nicht nannte. Wer eine Regel beschließt, prüft,
ob sie im normativen Absatz steht und nicht nur im Vektor daneben.

**Ein Test, der einen Vektor stillschweigend berichtigt, versteckt einen Spec-Defekt.**
`tests/test_verifier.py` hat die signierte NV2-Fassung seit `00c` im Test selbst gebaut, weil die
gedruckte Folge unvollständig war. Byte-genau dieselben 309 Byte, die D291 jetzt festlegt. Der Code
hatte die Lücke geschlossen, ohne sie zu melden.

**Ein Träger wird an seiner Zielzeile gemessen, nicht an seinem Grün.** Zwei von zehn trafen das
Nachbartor desselben Vermerks.

**Ein Tor kann doppelt geschützt sein, ohne dass man es sieht.** NV31 fängt auch das Key-Typtor,
weil die Iteration über eine Liste deren Werte liefert; `participants` als Zeichenkette fängt auch
die Eintragsschleife. Beide Male hat erst die geeichte Rücknahmeprobe es gezeigt.

**Eine Neutralisierung muss geschlossen sein.** Eine Probe, die ein `elif` ohne Kopf zurücklässt,
färbt die ganze Datei rot und zeigt nichts.

**Der eigene Satz braucht dieselbe Messung wie ein fremder.** Der Supervisor hat in `00aj` einen
Registersatz geschrieben, den der Diff eine Runde später widerlegt hat, und ihn vor dem Merge
berichtigt.

## Der nächste Schritt

1. **Die Kampagne aus D289 bauen.** Stufe 1 ist ein vollständiges Gitter: zehn Felder mal eine
   feste Operatorenmenge, Saat sind die gültigen Vektoren aus Anhang C, mutiert wird die dekodierte
   Map, danach kanonisch neu kodiert und **über den mutierten Core neu signiert**. Dazu die dritte
   Familie ohne Neusignierung. Das Ausgabetupel trägt neben dem Code den Ausgang „angenommen"
   samt `claim_id`. Gegenstück ist die Go-Fassung über ihre Hex-Schnittstelle (D269). Offene
   Vorfrage: wo das Gitter läuft — im Hauptrepo als Werkzeug oder als Wegwerf-Skript im
   ausgepackten Baum. Ein Werkzeug, das die Zweitfassung aufruft, wäre die erste Stelle, an der
   das Hauptrepo etwas außerhalb seiner selbst braucht.
2. **Die sechs offenen Fragen der Go-Fassung lesen.** `~/mar-go/FRAGEN.md`, Einträge 8, 11 bis 13,
   15, 16. In `00aj` nicht gelesen — nur die fünf neuen wurden bewertet.
3. **Der Kleinkram.** Fünf Dateien mit Backslashes, `register_index.py` ohne Anhangsverweise, der
   bare `§B.4` in `02b-abnahme.md`. Ein Lauf, klein, jederzeit einschiebbar.

## Offen

**In `00aj` gemessen:**

- **`~/mar-go` hat kein Remote.** Die Zweitimplementierung liegt nur lokal; ein Plattenschaden
  nimmt sie mit.
- **Sechs Fragen der Go-Fassung sind unverändert offen** (8, 11–13, 15, 16), elf hat der
  reparierte Text geschlossen, fünf sind neu. Zwei der neuen sind bewusst nicht Text geworden:
  der Präfixtest auf den Rohstring (der Text sagt „beginnt mit") und der Schritt, an dem ein Break
  in Wertposition scheitert (`B.2` stellt ihn frei).
- **`LINKED` hängt an genau einem Test, in jede der sechs Richtungen** (D286). Dieselbe Zahl
  sechsmal heißt: derselbe Test.
- **Backslashes in Wurzel-Markdowns.** Nachgemessen: 24 Dateien, davon 19 aus der
  `sitzungsstart`-Reihe (je eine, aus der Zählvorschrift). Der Rest sind **sieben Zeilen in fünf
  Dateien**: `01-claim-atom.md`, `02-spec-nachzug.md`, `02a-maxflow-prompt.md`,
  `02b-golden-anchors.md` (vier) und `welten-nachlauf-prompt.md`.
- **`tools/register_index.py` indiziert keine Anhangsverweise.** Nachgemessen: `01 §C.15` liefert
  eine leere Zeile.
- **Der Verweis in `02b-abnahme.md` auf `§B.4` bleibt bar und ungeprüft.** Nachgemessen: Zeile 29.
- **Die `einlesen-a-*`-Dateien behaupten, NV2 trage keine Drahtbytes.** Seit D291 falsch, bewusst
  nicht nachgezogen (Begründung wie D232).
- **Die Erzeugerstellen von Reject-Codes stehen bei 34, alle vom Bestand erreicht.** Zum ersten
  Mal überdeckungsvollständig.

**Weiterhin offen, in `00aj` nicht neu gemessen:**

- **Anhang C ist gegen Generatordrift nur teilweise gesichert.** Für C.1 gibt es
  `test_tv1_core_bytes_match_spec` mit getipptem Hex; für C.13 bis C.15 gibt es nichts, was den
  Spec-Text an `vectors_01.json` bindet. Gegen einen Prüfer spricht D233.
- **`UNPARSABLE_V` entsteht bei `ratify@1` nicht.** Lage 2 behält dort
  `UNSUPPORTED_RATIFICATION`. Benannter Rückstand aus D276.
- **`cbor_canon.decode` ist tolerant und bleibt es.**
- **`FOREIGN_LIFECYCLE` hat keinen Vektor und kann keinen bekommen** (D263, D268). Seit D283 hat
  es zwei Sondierwelten.
- **`EPOCH_FORK` hat keinen Produktivträger** (D138, D176, bestätigt in D281).
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173).
- **Zwei Registerverweise zeigen ins Leere**, `03 §5.1` und `03 §11`. Bewusst nicht nachgezogen.
- **Ob `tests/profiles/test_credit.py` die einzige Python-Datei ohne Schluss-Newline ist, lässt
  sich aus der Projektkopie nicht messen.** Im Repo zu messen oder zu streichen.
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
Fehlerklassen (D262, D265, ergänzt mit D292). Der Code für den falschen `J.tag` auf `core/*`
(D263). Die Feld-Konsistenz auf `core/*` (D264). Die Codes für Feldsatz-Verstöße (D266). Der
zwölfte Reject-Code (D267). Der Umfang einer Fassung ohne Speicher (D268). Die Hex-Schnittstelle
(D269). Die Arity der Eingabe (D270). Indefinite-Length und doppelte Keys (D271). Der Rückstand von
D266 im Code (D272). Die restlichen sechs Befundabschnitte (D273). Die `v`-Kanonizität in der
Auszählung (D274). Ort und Verdrängung von `NON_CANONICAL_V` (D275). Die vier Lagen und
`UNPARSABLE_V` (D276, D277). Der Träger für `superseded` (D278). Die Bindung der Reject-Codewerte
(D279). Die Vektoren für die Feldtabelle (D280). Die Vermerkskampagne (D281). Die Prüfregeln 52 bis
59 (D282). **Die überlebenden Erzeugerstellen (D283, D284, D285). Die Zustandsmatrix (D286). Die
zehn Doppelerzeuger (D287). Die Gliederung (D288). Die Bauform der Mutation (D289). Der Anker der
Kampagne (D290). Der zweite Mangel in NV2 (D291). Die Vorrangliste und `§6` Punkt 4 (D292).**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht.
