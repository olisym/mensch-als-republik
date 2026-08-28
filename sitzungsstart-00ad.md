# Sitzungsstart: 00ad (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`). Das
lokale Arbeitsverzeichnis ist `~/mensch-als-republik`.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 50, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer.

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird.

Was in `00ab` und `00ac` am meisten getragen hat:

- **Die Abnahme läuft über Zielhashes, nicht über gelesenen Diff.** Wird eine Änderung lokal gegen
  eine vollständige Kopie des Bestands gerechnet und dort mit der echten `check_specs.py` geprüft,
  dann belegt ein `sha256sum -c` der Ergebnisdateien byteweise, dass im Repo genau das entsteht,
  was geprüft wurde. Voraussetzung: die Projektkopie ist hash-gleich mit dem Repo, und die Prüfung
  läuft über **alle** Wurzel-`.md`, weil `check_specs.py` Verweise sonst nicht auflösen kann. In
  `00ac` sind so drei Splices ohne einen einzigen gelesenen Diff abgenommen worden.
- **Der Sitzungsstart ist eine Hypothese, keine Messung.** Der Übergabe-Commit dieser Datei liegt
  über dem hier genannten Stand.
- **Diagnoseläufe geben Zahlen aus, keine rohen Trefferlisten.** Die Liste gehört in eine Datei,
  die Zahl in die Antwort.
- **Vor jeder Position gegen fremden Code: die Trägermenge zählen** (D245, Prüfregel 49). In `00ac`
  hat genau das eine Frage beantwortet, die zwei Sitzungen offen stand.
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
  `string replace` geben Exit-Status 1 zurück, wenn sie nichts zu tun hatten. Kommandosubstitution
  entfernt Whitespace bereits selbst.
- **Ein Wächter, der nur prüft, sagt nicht, was zu tun ist.** In den Merge-Block gehört
  `git checkout main` **vor** den Wächter, nicht statt seiner. `git branch -d` statt `-D`.
- **Kommandosubstitution in doppelten Anführungszeichen braucht `$`** — fish liest `"(cmd)"`
  wörtlich, `"$(cmd)"` führt aus.
- **Spec-Dateien und Splice-Skripte als Download**, nicht als Copy-Block. Downloads landen in
  `~/Downloads` — der Kopierschritt nach `/tmp` gehört in den Block.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet`.
- Bei neuen Dateien `git add` **vor** `make check`. Explizite Pfade, nie `-A`.
- **Prosa bricht bei 100 Zeichen; Tabellenzeilen und Codeblöcke sind ausgenommen** (D222). Für
  Python gibt es **keine** Zeilenlängenregel; D205 hat das mit Zahlen entschieden. Diese Datei ist
  **nicht** von der Zeilenlänge ausgenommen.
- **Eine Regex, die in einen Prompt oder eine Spec-Datei soll, geht nicht.** Regexänderungen
  werden in Prosa beauftragt: welche Zeichenklasse, an welcher Stelle, optional oder nicht. In
  `00ac` sind so drei Proben beauftragt worden, ohne ein einziges Muster zu schreiben.

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
- **Verworfen für die Kopie:** `--compress`, `--remove-comments`, `--remove-empty-lines`,
  `--output-show-line-numbers`, `--no-file-summary`. Begründungen in D224.
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position,
  **40** vor jeder Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung,
  **43** vor jeder Zahl aus der Kopie, **44** vor jeder abgeleiteten Anzahl, **46** vor jeder
  Zeilenangabe, **49** vor jeder Rücknahmeprobe, **50** vor jedem Kriterium aus einem Modell.
  **28**: die Welt im Prompt ist Feld für Feld die gemessene Welt.

### Splices

Ein Splice ist ein Skript mit `assert`, dass der Anker genau einmal vorkommt. Gefahren mit
`python3 tools/splice_run.py /tmp/splice-*.py` (D225). Der Harness verlangt einen sauberen Baum,
erzwingt das Scheitern des zweiten Laufs, prüft die Zeilenlänge am Ergebnis und setzt bei jedem
Fehlschlag zurück.

- **Das Skript liegt in `/tmp`.** `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Das Skript wird erzeugt, nicht getippt.** Anker und Ersetzung je als `repr`.
- **Quellhash vor dem Schreiben, Zielhash nach dem Rechnen.** Ein Skript, das beide prüft, kann
  auf einem falschen Stand nichts anrichten und macht die Abnahme zu einem `sha256sum -c`.
- **Ein Anker am Dateiende braucht `endswith`, nicht nur `count == 1`.** In `00ac` zeigte ein
  Registeranker auf das Ende des vorletzten Eintrags; `count == 1` war erfüllt, und der neue
  Eintrag wäre vor seinen Vorgänger gerutscht. Der `endswith`-Assert hat es gefangen. Wer an ein
  Dateiende anhängt, prüft, dass der Anker das Dateiende **ist**.
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42) — aber er prüft
  auch nur den **eingesetzten** Text auf Form. Ein Verbot von Backslashes über die ganze Datei
  scheitert an Bestand: `01-claim-atom.md` trägt in Zeile 55 ein maskiertes Sternchen.
- **Mehrere Dateien in einem Skript**, wenn sie in denselben Commit gehören.
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`. Prüfregel 40: der Kopf wird gemessen, nicht aus dieser Zeile
abgeschrieben.

Nach `00ac`: **601 Tests** plus 14 Eigenschaftstests. Register **D1–D254**, Prüfregeln **1–50**.
**Drei Branches**. Keine offenen Läufe. Der Stand nach D254 ist `06c5f75`.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
  `§7` zählt vier Nukleus-Akte auf; die Föderationsstimme ist ausdrücklich keiner.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A. Die Axiome A1 bis A3 stehen in `§1`. **Anhang C trägt seit D250 neun
  Abschnitte**: C.1 bis C.4 positiv, C.5 bis C.7 negativ, C.8 Byte-Vektoren, C.9 TV5.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung. `§7.2` trägt den benannten
  Föderationsschlüssel, `§8` die Selbstblockade als getragene Grenze.
- **Fassade** (`mensch_als_republik/resolve.py`), **Kettenbauer** (`tests/kettenwelt.py`),
  **Werkzeugschicht** (`werkzeuge.md`), **Linter** `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py`, `tools/check_tree.py`,
  `tools/splice_run.py`.

**Neu in `00ac`:** D249 bis D254, drei Splices und ein Werkzeug-Lauf. Punkt 1 und Punkt 3 aus
`00ab` sind geschlossen.

- **D249** — die drei Normen aus `00ab` bekommen die Nummern 47 bis 49. Ohne Nummer ist eine Regel
  in einem Prompt nicht zitierbar, und was nicht zitierbar ist, wirkt nicht.
- **D250** — TV5 als `01 §C.9`: ein `core/revoke@1` mit gesetztem `t_exp`. Vektor statt
  Sondierwelt, weil Anhang C das einzige Artefakt ist, das eine Zweitimplementierung sehen wird.
  Ziel ist TV1 und damit ein bereits widerrufener Claim: der Vektor trägt eine Eigenschaft und
  ändert in keinem Store einen Zustand.
- **D251** — die in D248 beschlossene Löschung ist zurückgenommen. Beide Lookaheads spiegeln die
  gedruckten Regexe aus Anhang A; die redundante Bedingung in `resolve_scope` spiegelt die zwei
  MUSS aus `01 §2.2` Regel 3. **Das ist das neue Kriterium für toten Code: spiegelt er einen
  normativen Satz, ist Löschen ein Verlust, kein Gewinn.**
- **D252** — Befund an Anhang A: der Lookahead in der gedruckten nuc-Regex kann an seiner Stelle
  nichts ausschließen. Null Unterschiede über 200000 Kandidaten. Textfrage, offen.
- **D253, D254** — N02 ist geprüft. Vier Zellen: Lookahead entfernt allein grün, Reihenfolge
  getauscht allein grün, beides zusammen rot. D254 korrigiert die Zahl der roten Tests von einem
  auf vier.

## Was `00ac` gelehrt hat

**Die geschlossene Neutralisierung hat eine zwei Sitzungen alte Frage beantwortet.** N02 galt als
unbestimmt, weil die Einzelprobe grün blieb. Sobald beide Träger — das Lookahead und die
Zweigreihenfolge in `parse_predicate` — zusammen neutralisiert wurden, färbten sich vier Tests
rot. Prüfregel 49 hat innerhalb einer Sitzung nach ihrer Aufnahme ihren ersten Fall entschieden.

**Toter Code ist nicht automatisch Streichmaterial.** D248 hatte die Löschung beschlossen, bevor
gemessen war, dass beide Lookaheads wörtlich in Anhang A stehen. Die Frage ist nicht „läuft diese
Zeile", sondern „spiegelt sie einen Satz, der normativ ist". Der Befund aus D248 blieb richtig,
sein Beschluss nicht.

**Ein Modell des Codes trägt nur, was es nachbildet.** Die Vorhersage „genau ein roter Test" kam
aus einem Modell von `resolve_scope` mit drei Fällen; die Datei hat achtzehn Tests, und drei der
vier roten behaupten über `parse_predicate` statt über die Auflösung. Die Richtung stimmte, die
Zahl nicht. Daraus Prüfregel 50: ein Kriterium aus einem Modell ist eine untere Schranke.

**Das Werkzeug hat gemeldet statt angepasst**, und die Meldung war der Grund, den Punkt
nachzurechnen. Der Prompt hatte die Erwartung zu eng gefasst; ohne die Meldung wäre der Fehler in
D253 stehen geblieben.

## Der nächste Schritt

1. **Layer 01 in einer zweiten Sprache**, gegen Anhang C und die bestehenden Golden Anchors.
   Kanonische CBOR-Kodierung, Signaturprüfung, elf Reject-Codes, acht Zustände. Seit D250 trägt
   Anhang C mit TV5 auch die `t_exp`-Pflicht aus `01 §5.3`. Cursor-Credits liegen bereit. Jede
   Abweichung und jede Rückfrage ist eine Mehrdeutigkeit der Spec, die sich von allein meldet.
   D237 hält fest: das ist der beste verfügbare Ersatz für die fehlende Außenprüfung, und er
   ersetzt sie nicht. **Vor dem Prompt gehört eine Vorentscheidung ins Register**: welche Sprache,
   welcher Umfang, und woran genau die fremde Implementierung gemessen wird.
2. **D252 entscheiden.** Der wirkungslose Lookahead in der gedruckten nuc-Regex wird gestrichen
   oder als Spiegelung der Zeile darüber ausdrücklich behalten. Ein Splice, kein Lauf.
3. **Die Gliederung von `pruefregeln.md`.** Die angekündigte Ordnung nach dem Zeitpunkt, an dem
   eine Regel greift, ist ab Nummer 37 faktisch die Ordnung ihrer Entstehung; 38, 39, 40, 43 und
   46 stehen unter einer Überschrift über Tests und handeln nicht von Tests. Umsortieren würde
   Nummern brechen — die Frage ist, ob die Überschriften nachgezogen werden.

## Offen

- **D252**: der Lookahead in der gedruckten nuc-Regex von Anhang A.
- **Die Gliederung von `pruefregeln.md` ab Regel 37** (D249).
- **Ein Kandidat ohne Nummer** (D249): eine neu formulierte Norm wird vor dem Commit gegen die
  offenen Befunde derselben Sitzung gehalten. Einziger Anlass ist D248.
- **Siebzehn Wurzel-Markdowns tragen Backslashes**, obwohl die Anweisung keine vorsieht.
  Ungeprüft, ob das je eine Rolle spielt; `check_specs.py` beanstandet es nicht.
- **N09 ist beobachtet, nicht durchgesetzt** (D119, D246). Der Vermerk bleibt ohne Wirkung auf den
  Fluss; so beschlossen.
- **N10 ist teilgemessen** (D246). Drei Erzeugungsstellen für `INVALID_V_TYPE` in `credit.py`, eine
  Teststelle. `verdict.py` erzeugt den Vermerk nirgends.
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
  scheinen (D117). Der Vorbehalt steht in `04-golden-anchors.md §8`. Dieselbe Klasse wie D247,
  das mit D250 geschlossen ist — hier bleibt sie offen.
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
aus D243. **Die Nummerierung der Prüfregeln 47 bis 50 (D249, D254). Die Wahl Vektor statt
Sondierwelt für `01 §5.3` (D250). Die Löschung der beiden Lookaheads und der redundanten Bedingung
in `predicates.py` (D251, ausdrücklich zurückgenommen). Der Zustand von N02 und N07 (D250, D253,
D254).**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht.
