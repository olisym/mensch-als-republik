# Sitzungsstart: 00ai (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, selbst gehostete Gitea-Instanz (`git.h.error13.de`). Das lokale
Arbeitsverzeichnis ist `~/mensch-als-republik`, daneben `~/mar-go` mit der unabhängigen
Zweitimplementierung von Layer 01 in Go.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 51, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer.

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird. **Der Index kennt nur `§<Ziffern>`** — Anhangsverweise wie `01 §B.2`
fallen durch, obwohl `check_specs.py` sie seit D230 prüft. Wer einen Anhang sucht, greppt.

Was in `00ah` am meisten getragen hat:

- **Die Projektkopie wird ausgepackt und gefahren, und das ist inzwischen der Normalfall.** Aus
  `/tmp/mar-context.xml` lässt sich der ganze Baum rekonstruieren — geschnitten am `file`-Tag,
  Newline hinter dem öffnenden und vor dem schließenden Tag gehören nicht zum Inhalt, die
  Schluss-Newline wird wieder angehängt. `cbor2` und `cryptography` nachinstallieren, dann den
  Bestand fahren und die bekannte Testzahl reproduzieren: damit ist der Baum geeicht
  (Prüfregel 51). In `00ah` hat er sechs Sondierwelten, eine Mutantenmatrix aus 28 Läufen, zwei
  Nullproben, drei nachgebaute Werkzeugfassungen und alle Rücknahmeproben getragen — **ohne einen
  einzigen Zug an Oli**. Die ganze Sitzung brauchte neun Blöcke.
- **Vier bis sechs Dateien aus der Kopie, von Oli mit `sha256sum -c` geprüft, verankern sie.**
  Der Archivhash taugt nicht; der `--header-text` kann eine Sitzung alt sein.
- **Die gelieferte Fassung wird aus dem Diff nachgebaut und selbst gefahren.** Das ist in `00ah`
  dreimal geschehen und hat zweimal einen Defekt gefunden, den der Bericht nicht sah. Der Diff
  enthält genug, um die Fassung im ausgepackten Baum zu rekonstruieren; danach laufen die
  Sondierwelten gegen sie statt gegen eine Beschreibung von ihr.
- **Golden Numbers gehören nicht in den Prompt.** Der Prompt fixiert die Welten Feld für Feld.
- **Vor dem Prompt eine Nullprobe.** Die Codeänderung ohne die neuen Tests lokal nachbauen und den
  Bestand fahren: bewegt sich nichts, ist gemessen statt vermutet, dass der Bestand blind ist, und
  die Rücknahmeproben sind vorab geeicht (Prüfregeln 49, 51).
- **Der Bericht ist nie die Abnahme, auch nicht der eigene.**
- **Der Sitzungsstart ist eine Hypothese, keine Messung.** Der Übergabe-Commit dieser Datei liegt
  über dem hier genannten Stand.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`,
  `ruff`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.

### Shell

- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und
  eine Pipe auf `tail`, `awk` oder `grep -q` sind die nützlichen Ausnahmen. Nach Regel 39 sichert
  eine Zeile, die nur ausgibt, nichts: `test (git branch --show-current) = main` statt der
  Ausgabe.
- **Im Merge-Block steht `git push` vor `git branch -d`.** `-d` prüft gegen den **Upstream**, und
  ein lokal gemergter Branch gilt als unzusammengeführt, solange `main` nicht gepusht ist.
- **Sichtbar und geprüft zugleich geht über eine Datei.** `pytest -q > /tmp/x.txt`, dann
  `tail -1 /tmp/x.txt`, dann `grep -q '^642 passed' /tmp/x.txt`: ein Lauf, eine Ausgabe, ein
  Wächter. Eine Pipe würde eines von beidem fressen.
- **Mehrere Hashes prüft ein `printf` mit wiederholtem Format.** Ein Formatstring aus zwei
  Platzhaltern und Zeilenumbruch, dahinter die Paare aus Hash und Dateiname, die Ausgabe in
  `sha256sum -c`: eine Zeile, ein Wächter, kein Heredoc. `~/Downloads/...` wird darin expandiert.
- **`set -l` und verschachtelte Kommandosubstitution gehören nicht in einen Copy-Block.** Zahlen
  für den `--header-text` werden abgelesen und als Literal eingesetzt. Der **Kopf** ist die
  Ausnahme, weil er erst nach dem Commit feststeht: `$(git rev-parse --short HEAD)` in doppelten
  Anführungszeichen ist eine einfache Substitution und hat in `00ah` zweimal getragen. Ein `echo`
  des Headers vor dem Aufruf zeigt, ob die Kette so weit gekommen ist.
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

**Prüfregel 47:** ein Verweis und ein Inline-Code-Span werden nicht über die Zeilengrenze
getrennt.

**Die Grenze, die bleibt:** die Prüfung sichert, dass das Ziel **existiert**, nicht dass es
**stimmt** (D229, mit Zahlen bestätigt in D233). Daraus folgt D250: ein Anhang wird **angehängt,
nicht eingeschoben**.

**Ein Anhang ohne Ziffer ist kein Verweis.** `01 §A` matcht `SECTION_REF` nicht. Anhänge werden im
Klartext genannt. **Ein Prompt darf nicht auf einen Abschnitt zeigen, den erst sein Lauf
erzeugt.** **Befund-Dateien sind zitierfähig.**

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
- **Die Projektkopie wird nach jedem Push nachgezogen** (D224, Prüfregel 43), mit fünf Kaltzahlen
  im `--header-text`, Aufruf über
  `npx --yes repomix --header-text "..." -o /tmp/mar-context.xml`. **Das `-o` gehört dazu.**
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
Fehlschlag zurück. **Die Meldung `AssertionError` gefolgt von `zweiter Lauf gescheitert` ist die
Erfolgsmeldung**, nicht der Fehlerfall.

- **Das Skript liegt in `/tmp`.** `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Das Skript wird erzeugt, nicht getippt.** Anker und Ersetzung je als `repr`. Mehrere
  Anker-Paare in einer Liste sind billiger als mehrere Skripte.
- **Der Anker am Dateiende wird aus der Kopie abgelesen, nicht getippt.**
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42). Ein Assert auf
  eine erwartete **Anzahl** fängt mehr als eine Anwesenheitsprüfung — **aber die Anzahl wird
  gemessen, nicht gerechnet.** In `00ah` sind drei von vier Anzahl-Asserts beim ersten Lauf
  gefallen, jedes Mal, weil die Zahl im Kopf ausgerechnet statt im Wegwerfbaum abgelesen war. Das
  kostet je einen Durchlauf und ist der billigste vermeidbare Fehler der Sitzung.
- **Quellhash vor dem Schreiben, Zielhash nach dem Rechnen.** Die Abnahme eines reinen
  Textschnitts liegt vollständig im Zielhash; Commit und Merge dürfen im selben Block stehen.
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`. Vor der Testzahl `.hypothesis` und `__pycache__` löschen
(Prüfregel 19). Prüfregel 40: der Kopf wird gemessen, nicht aus dieser Zeile abgeschrieben.

Nach `00ah`: **642 Tests** plus Eigenschaftstests. Register **D1–D278**, Prüfregeln **1–51**.
**Drei Branches**. Keine offenen Läufe. Der Stand nach D278 ist `7141ccb`.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
- **01** Atom, Verifier, **zwölf Reject-Codes**, **sieben** Klassifikationszustände. Prädikat-
  Grammatik in `§2.2` und Anhang A. `§3` trägt seit D270 den Arity-Satz. Anhang C trägt seit D272
  vierzehn Abschnitte. Anhang B.1 führt acht Zeilen, der `State`-Enum sieben Werte: `malformed`
  ist kein Klassifikationsergebnis, sondern die Verweigerung der Speicherung (D278).
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`. `§1.3` ist
  seit D276 die normative Form für jedes Lesen von `v` in jeder Schicht.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung. `§2.3` trägt seit D274 den
  Kanonizitätssatz für `v`, seit D276 die vier Lagen und seit D277 ihre Reihenfolge — **alles
  gebaut**. Die Vermerke `NON_CANONICAL_V` und `UNPARSABLE_V` sind neu.
- **Fassade** (`mensch_als_republik/resolve.py`), **Kettenbauer** (`tests/kettenwelt.py`),
  **Werkzeugschicht** (`werkzeuge.md`), **Linter** `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py`, `tools/check_tree.py`,
  `tools/splice_run.py`.

### Was `00ah` entschieden hat

- **D275** — wo `NON_CANONICAL_V` entsteht und was er verdrängt. Die Prüfung steht vor der
  Zusammenfassung nach Autor; bei `ratify@1` verdrängt sie `UNSUPPORTED_RATIFICATION`; die
  Ausschlussschleife nach `04 §4.4` zieht mit. Dazu die **Berichtigung an D274**: dort stand, die
  Frage nach der Ausschlusslogik entfalle mit dem Beschluss. Sie entfällt nicht, sie kippt — vor
  dem Beschluss fielen beide Stimmen desselben Autors weg, danach zählt die kanonische. Der Satz
  war eine Ableitung ohne Messung.
- **D276** — die Form aus `03 §1.3` ist normativ, nicht nur der gemeinsame `try`. Der Lauf hatte
  `decode` und `is_canonical` korrekt in einen `try` gestellt und den `except`-Zweig auf `pass`
  gesetzt; damit fiel ein `v`, dessen **Re-Serialisierung** wirft, durch die Prüfung und wurde
  danach erneut dekodiert. `h'a2000101ff'` zählte weiter als Ja. Governance bekam einen Leser mit
  vier Lagen und den Vermerk `UNPARSABLE_V` — womit D275 Beschluss 3 fiel, der ihn
  zurückgestellt hatte.
- **D277** — die Lagen 2 und 3 überschneiden sich, und die Kanonizität wird zuerst geprüft.
  `h'1801'` ist weder kanonisch noch eine Map und trägt `NON_CANONICAL_V`; `h'01'` trägt
  `UNPARSABLE_V`. Kein Vektor, weil beide Ausgänge unschädlich sind und die angrenzenden Lagen
  je einen haben.
- **D278** — `superseded` überlebte drei von sechs Mutanten, `malformed` hatte keinen Erzeuger.
  Zwei Träger, die den Namen behaupten, je einer für `classify` und `classify_all`; `MALFORMED`
  aus dem Enum gelöscht.

## Was `00ah` gelehrt hat

**Der teuerste Defekttyp ist der geschlossene Beschluss ohne Lauf — und der zweitteuerste ist der
Lauf, der den Buchstaben trifft und den Satz verfehlt.** D276 ist der zweite Fall: der Prompt
verlangte `decode` und `is_canonical` im selben `try`, das Werkzeug hat genau das gebaut, und der
tragende Teil war ein anderer — dass der `except`-Zweig **abbricht**. Wer eine Form vorschreibt,
muss ihren tragenden Teil benennen, nicht ihre Silhouette. Das ist ein Kandidat für Prüfregel 52.

**Die Umkehrung des Suchmusters trägt, das Suchmuster selbst nicht.** „Welcher Registereintrag
beschließt Verhalten und taucht in keinem Test auf" liefert 47 Kandidaten und damit kein Signal.
„Welcher Vermerks- oder Verdiktcode im Produktivcode taucht in keinem Test auf" liefert vier, von
denen zwei benannt waren und zwei nicht. Der Grund ist einfach: D-Nummern stehen selten im Code,
Codes stehen immer dort. **Der Prüfer misst am Code, nicht am Register.**

**Ein Zustand, der nur über seine Wirkung gebunden ist, ist nicht gebunden.** `SUPERSEDED` wurde
34-mal je Testlauf erzeugt und war trotzdem austauschbar gegen `REVOKED`, `PENDING` und
`EQUIVOCATION_FLAGGED`. Getestet war „gültig, inaktiv", nicht der Name. Die Mutantenmatrix — jeden
Zustand gegen jeden anderen, je Mutant der volle Bestand — findet das mechanisch und kostet
zwanzig Minuten Rechenzeit im ausgepackten Baum. Sie sollte auf die Reject-Codes und die
Vermerkskonstanten ausgedehnt werden.

**Ein Kopplungstest bindet die Übereinstimmung, nicht den Wert.** Bei der Probe, die beide
Klassifikationspfade zugleich mutiert, blieb der Kopplungstest grün, weil beide denselben falschen
Namen lieferten. Er war die ganze Zeit da und hat `SUPERSEDED` nie gesichert. Wo zwei Pfade
gekoppelt geprüft werden, braucht es zusätzlich je einen Träger, der den Wert behauptet.

**Prüfregel 27 gilt für den Supervisor auch dann, wenn er die Messung selbst gefahren hat.** Der
Prompt zu D278 verlangte zwei Gegenproben auf `REVOKED`. Die Mutantenmatrix von zwei Runden davor
enthielt bereits die Antwort — `REVOKED` war zehnfach gebunden. Die Gegenproben schaden nicht,
aber sie sind zwei Tests, die nichts binden, und die Messung dagegen lag im eigenen Protokoll.

**„Der Diff steht oben" ist kein Diff.** Ein Bericht, der den Diff als geliefert bezeichnet, ohne
ihn zu enthalten, wird nicht als Lieferung behandelt. Der Diff wurde nachgefordert und enthielt
den Defekt, den der Bericht nicht sah.

## Der nächste Schritt

1. **Die Mutantenmatrix ausdehnen.** Zustände sind durch; offen sind die zwölf Reject-Codes aus
   `01` und die Vermerkskonstanten aus `00`, `03` und `04`. Dasselbe Verfahren: Erzeugerstelle
   mutieren, vollen Bestand fahren, überlebende Mutanten notieren. Das ist der billigste bekannte
   Weg zu ungebundenem Verhalten und braucht keinen Zug an Oli.
2. **Prüfregeln 52 und folgende setzen.** Die Kandidatenliste ist auf sechs gewachsen und wird
   nicht kürzer, solange sie nicht geschrieben wird. Zusammen mit der Gliederung ab Regel 37
   (D249).
3. **Der Föderations-Fork D234.** Dreiweg-Widerspruch zwischen `00 §7`, `04 §7.2` und `04 §3.1`
   zur Schlüsselauflösung, D235 vorgeschlagen und nicht abgeschlossen. Der größte ungelöste
   Strukturpunkt.

**Zur dritten Fassung:** sie ist möglich, aber der Anker hat sich bewegt. Nach D258 muss sie
denselben Spec-Stand lesen wie die Go-Fassung — das ist `1109b89`, **nicht** der jetzige. Wer
gegen den reparierten Stand baut, misst die Reparatur und nicht die Häufung. Beides ist zulässig,
aber es sind zwei verschiedene Versuche, und die Wahl gehört ins Register.

## Offen

- **`UNPARSABLE_V` entsteht bei `ratify@1` nicht.** Lage 2 behält dort `UNSUPPORTED_RATIFICATION`,
  weil D276 nur den Kandidatenfilter beschlossen hat. Im Prompt ausdrücklich so beauftragt,
  benannter Rückstand, kein stiller.
- **`LINKED` hängt an genau einem Test** (D278). Gebunden, aber dünn.
- **Die Mutantenmatrix ist unvollständig:** 28 von 42 Zustandspaaren gefahren. Für `SUPERSEDED`
  sind alle sechs Ziele gefahren, für die übrigen mindestens eines. Die fehlenden vierzehn sind
  Mutationen **nach** `SUPERSEDED`, `EXPIRED`, `EQUIVOCATION_FLAGGED` und `ACTIVE`.
- **Sechs Kandidaten für Prüfregel 52 und folgende.** Erstens: wird eine Projektkopie aus einem
  gelieferten Diff rekonstruiert, geht ein `sha256sum -c` der Quelldateien als zweiter Job in den
  Block (aus `00af`). Zweitens: im Merge-Block steht `git push` vor `git branch -d` (aus `00ag`).
  Drittens: wer eine Form vorschreibt, benennt ihren tragenden Teil (aus D276). Viertens: ein
  Anzahl-Assert in einem Splice wird im Wegwerfbaum abgelesen, nicht gerechnet. Fünftens: ein
  Bericht, der den Diff als geliefert bezeichnet, ohne ihn zu enthalten, ist keine Lieferung.
  Sechstens: wo zwei Pfade gekoppelt geprüft werden, braucht jeder zusätzlich einen Träger, der
  den Wert behauptet.
- **Anhang C ist gegen Generatordrift nur teilweise gesichert.** Für C.1 gibt es
  `test_tv1_core_bytes_match_spec` mit getipptem Hex; für C.13 gibt es nichts, was den Spec-Text
  an `vectors_01.json` bindet. Gegen einen Prüfer spricht D233.
- **`cbor_canon.decode` ist tolerant und bleibt es.**
- **`tools/register_index.py` indiziert keine Anhangsverweise.** Ein eigener Lauf, klein.
- **`FOREIGN_LIFECYCLE` hat keinen Vektor und kann keinen bekommen**, solange die Vektoren
  zustandslos gelesen werden (D263). Nach D268 liegt er als einziger Punkt außerhalb der
  selbstenthaltenen Gültigkeit.
- **`EPOCH_FORK` hat keinen Produktivträger** (D138, D176, bewusst).
- **Die Gliederung von `pruefregeln.md` ab Regel 37** (D249).
- **Wurzel-Markdowns tragen Backslashes.** Zuletzt siebzehn gezählt; die Zahl ist nicht
  nachgemessen.
- **Die Kampagne mit mutierten Claims** ist beschlossen und ungebaut (D258).
- **N09 ist beobachtet, nicht durchgesetzt** (D119, D246). **N10 ist teilgemessen** (D246).
- **`00z-anhangsform-prompt.md` trägt fünf um eins zu hohe Zeilenangaben.** Bewusst nicht
  berichtigt (D232).
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
- **Wie weit die Regierbarkeitsprüfung reicht** (D200). Zurückgestellt — **nicht vorher
  aufmachen**.
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
Die zweite Prüfklasse für Verweisrichtigkeit (D233, mit Zahlen verworfen). Die Föderationsstimme
(D235), der Ausschlussmechanismus (D236). Die Zuordnung von Pflichten über Stichworte (D242, mit
Zahlen verworfen). Die MUSS-Extraktion selbst (D246). Die Wahl Vektor statt Sondierwelt für
`01 §5.3` (D250). Der Lookahead in der gedruckten nuc-Regex (D255). Reihenfolge und Umfang der
Zweitimplementierung (D256, D258, D259). Die Abdeckung des Fehlerkanals durch Anhang C (D257).
Der Vergleichsgegenstand der Kanonizitätsprüfung (D261). Der Vorrang der Fehlerklassen (D262).
Der Code für den falschen `J.tag` auf `core/*` (D263). Die Feld-Konsistenz auf `core/*` (D264).
Die Gesamtordnung der Fehlerklassen (D265). Die Codes für Feldsatz-Verstöße (D266). Der zwölfte
Reject-Code (D267). Der Umfang einer Fassung ohne Speicher (D268). Die Hex-Schnittstelle des
Auftrags (D269). Die Arity der Eingabe (D270). Die Lesart von Indefinite-Length und doppelten
Keys (D271). Der Rückstand von D266 im Code (D272). Die restlichen sechs Befundabschnitte (D273).
Die Geltung der `v`-Kanonizität in der Auszählung (D274). **Der Ort und die Verdrängung von
`NON_CANONICAL_V` (D275). Die vier Lagen und `UNPARSABLE_V` (D276). Ihre Reihenfolge (D277). Der
Träger für `superseded` und die Löschung von `State.MALFORMED` (D278).**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht.
