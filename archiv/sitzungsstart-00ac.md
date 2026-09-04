# Sitzungsstart: 00ac (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`). Das
lokale Arbeitsverzeichnis ist `~/mensch-als-republik`.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 46, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer.

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird.

Was in `00ab` am meisten getragen hat:

- **Die Abnahme läuft über Zielhashes, nicht über gelesenen Diff.** Wird eine Änderung lokal gegen
  eine vollständige Kopie des Bestands gerechnet und dort mit der echten `check_specs.py` geprüft,
  dann belegt ein `sha256sum -c` der Ergebnisdateien byteweise, dass im Repo genau das entsteht,
  was geprüft wurde. Das hat in `00ab` 260 Diff-Zeilen im Kanal gespart und ist strenger als
  Augenschein. Voraussetzung: die Projektkopie ist hash-gleich mit dem Repo, und die Prüfung
  läuft über **alle** Wurzel-`.md`, weil `check_specs.py` Verweise sonst nicht auflösen kann.
- **Der Sitzungsstart ist eine Hypothese, keine Messung** — zum zweiten Mal in Folge bestätigt.
  Die siebzehn Stummelzeilen waren vierzehn. Die MUSS-Aufgabe umfasste 24 Marker, daraus vierzehn
  Kennungen und am Ende zwölf Pflichten. Beide Male hat das Messen die Aufgabe verändert, bevor
  eine Zeile geschrieben war.
- **Diagnoseläufe geben Zahlen aus, keine rohen Trefferlisten.** Ein Lauf über kurze Zeilen hat in
  `00ab` mehr als 500 Zeilen in den Kanal gespült für ein Ergebnis, das die Aufgabe nicht
  verändert hat. Die Liste gehört in eine Datei, die Zahl in die Antwort.
- **Vor jeder Position gegen fremden Code: die Trägermenge zählen.** Vier Module prüfen dieselbe
  Genesis-Bindung, acht Stellen dieselbe Scope-Gleichheit. Wer eine davon anfasst und daraus
  schließt, hat die Stelle gemessen und nicht die Pflicht (D245).
- **Der Bericht ist nie die Abnahme, auch nicht der eigene.** Bei reinen Registeranhängen genügt
  `numstat` plus die Asserts; bei Ersetzungen mitten in Layer-Dateien der Zielhash oder der
  vollständige Diff (D225).
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`, `ruff`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten** — ein leerer Glob bricht die Zeile ab, `find -name` ist der sichere
  Ersatz. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und eine Pipe auf `tail`
  oder `awk` sind die nützlichen Ausnahmen. Nach Regel 39 sichert eine Zeile, die nur ausgibt,
  nichts: `test (git branch --show-current) = main` statt der Ausgabe.
- **Jeder Block trägt Marken.** Vor jedem Abschnitt ein `echo "== NAME =="`, am Ende ein
  `echo "== FERTIG =="`. Fehlt die Schlussmarke in der zurückkopierten Ausgabe, ist die Kette
  abgebrochen — unabhängig davon, ob die letzte sichtbare Zeile erfolgreich aussieht. Ohne Marken
  ist ein stiller Abbruch nicht von einem vollständigen Lauf zu unterscheiden, und beide Male, wo
  das in `00ab` passiert ist, war die letzte sichtbare Zeile ein Erfolg. Die Marken stehen mit
  `and` in der Kette, damit sie mit ihr abbrechen.
- **`string`-Kommandos in einer `and`-Kette sind eine Falle.** `string trim`, `string match` und
  `string replace` geben Exit-Status 1 zurück, wenn sie nichts zu tun hatten — kein Fehler, nur
  keine Änderung. In einer Kette bricht das alles Folgende ab. Genau daran ist der Nachzug der
  Projektkopie in `00ab` zweimal gescheitert: `wc -l` liefert unter Linux keine führenden
  Leerzeichen, `string trim` hatte nichts zu tun und meldete 1. Meist braucht man es nicht —
  Kommandosubstitution entfernt Whitespace bereits selbst.
- **Ein Wächter, der nur prüft, sagt nicht, was zu tun ist.** In den Merge-Block gehört
  `git checkout main` **vor** den Wächter, nicht statt seiner. `git branch -d` statt `-D`, damit
  die Löschung scheitert, wenn doch etwas ungemergt ist.
- **Kommandosubstitution in doppelten Anführungszeichen braucht `$`** — fish liest `"(cmd)"`
  wörtlich, `"$(cmd)"` führt aus.
- **Spec-Dateien und Splice-Skripte als Download**, nicht als Copy-Block. Downloads landen in
  `~/Downloads` — der Kopierschritt nach `/tmp` gehört in den Block.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet`.
- Bei neuen Dateien `git add` **vor** `make check`. Explizite Pfade, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. **Prosa bricht bei 100 Zeichen; Tabellenzeilen
  und Codeblöcke sind ausgenommen** (D222). Für Python gibt es **keine** Zeilenlängenregel; D205
  hat das mit Zahlen entschieden und nicht wieder aufzumachen. Diese Datei darf frei zitieren,
  aber sie ist **nicht** von der Zeilenlänge ausgenommen.
- **Eine Regex, die in einen Prompt oder eine Spec-Datei soll, geht nicht.** Regexänderungen
  werden in Prosa beauftragt: welche Zeichenklasse, an welcher Stelle, optional oder nicht.

### Die Zitiergrammatik — geschlossen, mit einer neuen Umbruchpflicht

Seit D232 gibt es keinen offenen Teil. Vier Teile: der Dateiname mit oder ohne `.md`; die
Kurzform `NN`/`NNx` über `LAYER_FILES` (dreizehn Einträge, geschlossen); die Bereichsform
`NAME §A–§B` (D228, kein Leerraum um den Strich); die Anhangsnummer als Großbuchstabe mit Punkt
vor der Ziffernfolge (D230). Dazu die Backtick-Toleranz zwischen Namen und Paragraphenzeichen
(D231). Alles andere in `.py` ist ein Befund (D227); in `.md` bleibt der bare Verweis zulässig.

**Neu mit D239: ein Verweis und ein Inline-Code-Span werden nicht über die Zeilengrenze
getrennt.** `SECTION_REF` verlangt den Namen unmittelbar vor dem Paragraphenzeichen; ein Umbruch
dazwischen macht den Verweis unsichtbar, nicht falsch — die Prüfung bleibt grün und sieht ihn
nicht mehr. Gemessen wäre das in `00ab` zweimal passiert. Wer Prosa umbricht, behandelt beide als
ein Wort.

**Die Grenze, die bleibt:** die Prüfung sichert, dass das Ziel **existiert**, nicht dass es
**stimmt** (D229, mit Zahlen bestätigt in D233). Gemessene Fehlerrate an der einzigen vollständig
geprüften Datei: zwei von 25.

**Ein Anhang ohne Ziffer ist kein Verweis.** `01 §A` matcht `SECTION_REF` nicht, weil hinter dem
Paragraphenzeichen eine Ziffernfolge stehen muss. Anhänge werden im Klartext genannt.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt. Eine **Ersetzung** ist eine Löschung
  plus eine Einfügung. **Nach D244 werden die randgleichen Zeilen abgezogen:** git zieht Zeilen,
  die am oberen oder unteren Rand eines Blocks unverändert bleiben, nicht in den Hunk. Ohne diesen
  Abzug ist die Erwartung systematisch zu hoch — in `00ab` um 32 Zeilen auf beiden Seiten.
- **`tools/check_specs.py` zählt eine Zeile mehr als `wc -l`**, weil es die Umbrüche plus eins
  rechnet. Kein Widerspruch, nur zwei Zählweisen.
- **Prüfregel 46: aus der Projektkopie kommt jede absolute Zeilenangabe um eins zu hoch.** Wer
  eine Datei sauber aus dem Archiv extrahiert (den Zeilenumbruch hinter dem Dateitag konsumieren)
  und den Hash gegen das Repo prüft, hat korrekte Zeilennummern.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Aus einer Zeilennummer folgt kein Abschnitt.** In `00ab` waren neun von vierzehn geschlossenen
  Abschnittsangaben falsch. Die Zuordnung wird gegen die Überschriften gerechnet, immer.
- **Zählvorschriften:** Registerköpfe `grep -c '^### D' 07-decisions.md`; Prüfregeln
  `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`; Branches `git branch -a | wc -l`; Abschnitte je Datei
  `grep -n '^## ' <datei>`.
- **Die Projektkopie wird nach jedem Push nachgezogen** (D224, Prüfregel 43), mit fünf Kaltzahlen
  im `--header-text`, Aufruf über
  `npx --yes repomix --header-text "..." -o /tmp/mar-context.xml`. **Das `-o` gehört dazu**:
  ohne es schreibt repomix `repomix-output.xml` in den Arbeitsbaum, und `check_tree.py` meldet
  sie. `.gitignore` nimmt sie bewusst **nicht** auf, damit der Wächter anschlägt.
- **Die fünf Kaltzahlen werden ausgelesen, nicht abgetippt.** Ein Header, der die Zahlen falsch
  trägt, ist schlimmer als keiner. Der Nachzug steht am Kettenende und ist deshalb der erste
  Verlierer jedes stillen Abbruchs; ein `echo` des Headers **vor** dem Aufruf zeigt, ob die Kette
  so weit gekommen ist.
- **Verworfen für die Kopie:** `--compress`, `--remove-comments`, `--remove-empty-lines`,
  `--output-show-line-numbers`, `--no-file-summary`. Begründungen in D224; nicht wieder aufmachen.
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position,
  **40** vor jeder Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung,
  **43** vor jeder Zahl aus der Kopie, **44** vor jeder abgeleiteten Anzahl, **46** vor jeder
  Zeilenangabe. **28**: die Welt im Prompt ist Feld für Feld die gemessene Welt.

### Splices

Ein Splice ist ein Skript mit `assert`, dass der Anker genau einmal vorkommt. Gefahren mit
`python3 tools/splice_run.py /tmp/splice-*.py` (D225). Der Harness verlangt einen sauberen Baum,
erzwingt das Scheitern des zweiten Laufs, prüft die Zeilenlänge am Ergebnis und setzt bei jedem
Fehlschlag zurück.

- **Das Skript liegt in `/tmp`.** `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Das Skript wird erzeugt, nicht getippt.** In `00ab` sind vierzehn Blockersetzungen aus dem
  gemessenen Ist-Zustand generiert worden, Anker und Ersetzung je als `repr` der Zeilenliste. Ein
  getippter Anker ist ein Tippfehler in Wartestellung; der Eindeutigkeits-Assert hat genau so
  einen gefangen (Einrückung zwei statt drei Leerzeichen).
- **Ein Assert auf den Kontext** gehört dazu, wenn das Skript nur auf einem bestimmten Branch
  laufen darf — etwa die Existenz einer Datei, die erst der Merge bringt.
- **Mehrere Dateien in einem Skript**, wenn sie in denselben Commit gehören.
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42). Bewährt: im
  Trockenlauf gegen Kopien in `/tmp` die Zeilenlänge, die Verweisauflösung und `check_specs.py`
  vollständig durchrechnen, bevor die Datei ausgeliefert wird.
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`. Prüfregel 40: der Kopf wird gemessen, nicht aus dieser Zeile
abgeschrieben; der Übergabe-Commit dieser Datei liegt über dem hier genannten Stand.

Nach `00ab`: **597 Tests** plus 14 Eigenschaftstests. Register **D1–D248**, Prüfregeln **1–46**.
**Drei Branches**. Keine offenen Läufe. Der Stand nach D248 ist `2f32a60`.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
  `§7` zählt vier Nukleus-Akte auf; die Föderationsstimme ist ausdrücklich keiner.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A. Die Axiome A1 bis A3 stehen in `§1`.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung. `§7.2` trägt den benannten
  Föderationsschlüssel, `§8` die Selbstblockade als getragene Grenze.
- **Fassade** (`mensch_als_republik/resolve.py`), **Kettenbauer** (`tests/kettenwelt.py`),
  **Werkzeugschicht** (`werkzeuge.md`), **Linter** `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py`, `tools/check_tree.py`,
  `tools/splice_run.py`.

**Neu in `00ab`:** D238 bis D248, vier Splices und zwei Werkzeug-Läufe. Punkt 1 und Punkt 2 aus
D237 sind geschlossen.

- **D238 bis D241** — der Reflow. Vierzehn Blöcke geglättet, drei ausdrücklich nicht: zweimal ist
  die kurze Zeile ein Absatzschluss, einmal ergibt der Umbruch den Ist-Zustand. Dazu zwei
  vorbestehende Defekte, die der Reflow offengelegt hat: eine Silbentrennung über den Umbruch in
  `06 §10` und zwei Kopfangaben ohne trennende Leerzeile in `02-golden-anchors.md`.
- **D242** — die Menge der markierten Pflichten und das Verfahren. Die Zuordnung über Stichworte
  ist mit Zahlen verworfen: 133 Treffer auf ein Allerweltswort belegen nichts.
- **D243** — die RFC-2119-Marker sind keine Landkarte der Normativität. `05` und `08` tragen
  keinen einzigen, `02` vier bei durchweg normativem Inhalt.
- **D244** — die `numstat`-Erwartung zieht randgleiche Zeilen ab.
- **D245** — die Rücknahmeprobe misst die Stelle, nicht die Pflicht, solange Träger redundant sind.
- **D246** — Abnahme: zwölf Pflichten, zehn geprüft, eine unbestimmt, eine ungeprüft.
- **D247, D248** — die zwei echten Befunde mit ihrer jeweiligen Reparatur, beide offen.

## Was `00ab` gelehrt hat

**Eine Frage nach Testabdeckung hat eine Eigenschaft der Codebasis freigelegt.** Dieselbe
Bindungsprüfung steht an vier Stellen, dieselbe Scope-Gleichheit an acht. Das ist kein Defekt —
`04 §3.5` verlangt die Prüfung vor jedem Feldzugriff, und jeder Einstiegspunkt muss sie selbst
leisten. Aber es macht jede Messung an einer Einzelstelle wertlos, und das war vorher nicht
gewusst.

**Die eigene Regel wurde beim Schreiben nicht angewandt.** D245 fordert die geschlossene
Trägermenge, und im selben Eintrag blieb N02 mit einer von zwei Stellen stehen. Der Fehler ist in
D248 benannt und die Probe ausdrücklich offen. Kandidat für eine Prüfregel: eine neu formulierte
Norm wird vor dem Commit gegen die offenen Befunde derselben Sitzung gehalten.

**Drei Normen dieser Sitzung haben keine Prüfregelnummer.** D239, D244 und D245 sind als Norm
formuliert, aber `pruefregeln.md` steht unverändert bei 46. Das ist die billigste Arbeit der
nächsten Sitzung und der wahrscheinlichste Verlust, wenn sie unterbleibt.

## Der nächste Schritt

1. **Die drei Normen als Prüfregeln 47 bis 49 aufnehmen.** Ein Splice, kein Werkzeug-Lauf. Die
   Texte stehen fertig in D239, D244 und D245.
2. **Layer 01 in einer zweiten Sprache**, gegen die bestehenden Golden Anchors. Kanonische
   CBOR-Kodierung, Signaturprüfung, elf Reject-Codes, acht Zustände. Cursor-Credits liegen bereit.
   Jede Abweichung und jede Rückfrage ist eine Mehrdeutigkeit der Spec, die sich von allein meldet.
   D237 hält fest: das ist der beste verfügbare Ersatz für die fehlende Außenprüfung, und er
   ersetzt sie nicht.
3. **Die zwei Reparaturen aus D247 und D248**, ein Lauf. Ein `core/*`-Vektor mit abgelaufenem
   `t_exp` samt Test, die Löschung des toten Lookaheads und der redundanten Bedingung, und die
   offene Probe zu N02 mit geschlossener Trägermenge. Innenarbeit; sie ersetzt Punkt 2 nicht.

## Offen

- **Die drei Normen ohne Prüfregelnummer** (D239, D244, D245).
- **N02 ist unbestimmt** (D248). Die Probe hat die Lookaheads getroffen, nicht die Reihenfolge in
  `parse_predicate`. Ausdrücklich ungemessen.
- **N07 ist ungeprüft** (D247). Der Test klassifiziert einen Vektor ohne `t_exp`.
- **N09 ist beobachtet, nicht durchgesetzt** (D119, D246). Der Vermerk bleibt ohne Wirkung auf den
  Fluss; so beschlossen.
- **N10 ist teilgemessen** (D246). Drei Erzeugungsstellen für `INVALID_V_TYPE` in `credit.py`, eine
  Teststelle. `verdict.py` erzeugt den Vermerk nirgends — ob dort ein `v` mit deklariertem Typ
  vorkommt und einen Träger braucht, ist ungeprüft.
- **Die Zweitimplementierung von Layer 01** (D237).
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
  scheinen (D117). Der Vorbehalt steht in `04-golden-anchors.md §8`. Dieselbe Klasse wie D247.
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
Ausschlussmechanismus (D236). **Der Reflow der Stummelzeilen (D238). Die Zuordnung von Pflichten
über Stichworte (D242, mit Zahlen verworfen). Die MUSS-Extraktion selbst (D246) — mit der Grenze
aus D243.**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht.
