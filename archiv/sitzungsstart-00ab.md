# Sitzungsstart: 00ab (MaR)

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

Was in der letzten Sitzung am meisten getragen hat:

- **Der Sitzungsstart ist eine Hypothese, keine Messung.** Er nannte `04 §7.2` „nie
  durchgerechnet"; gelesen war der Abschnitt bewusst dünn und trug stattdessen einen
  Autorisierungsweg, den keine Schicht einlöst. Er nannte einen falschen Verweis in
  `example-nucleus.md`; gemessen waren es zwei. Beide Male hat das Lesen die Aufgabe verändert,
  bevor eine Zeile geschrieben wurde.
- **Die Klassen zählen, bevor man sie behandelt.** Vier Vorkommen von `02 §2` in einer Datei, drei
  davon richtig. Eine Ersetzung über die Datei wäre falsch gewesen; der Befund war zeilengenau.
- **Vor dem Verwerfen einer Idee die Falsch-Positiv-Rate messen.** Die Frage nach einer zweiten
  Prüfklasse für Verweisrichtigkeit war mit D229 verworfen und wurde durch einen zweiten Fund
  wieder aufgemacht. Statt sie erneut zu verwerfen, wurde die vorgeschlagene Probe gegen die eine
  Datei mit bekannter Wahrheit gehalten: 48 Prozent Blindquote, 50 Prozent Präzision. Erst diese
  Zahl hat die Frage geschlossen.
- **Bei Forks, die außerhalb seit Jahrzehnten bearbeitet werden, zuerst nachsehen.** Die
  Föderationsfrage hat drei getrennte Literaturstränge (SPKI/SDSI, byzantinische Reconfiguration,
  Gruppenschlüsselprotokolle). Die Recherche hat die Entscheidung nicht ersetzt, aber sie hat
  einen Unmöglichkeitsgrund geliefert, den MaR aus sich heraus nicht herstellen kann.
- **Der Bericht ist nie die Abnahme, auch nicht der eigene.** Bei reinen Registeranhängen genügt
  `numstat` plus die Asserts; bei Ersetzungen mitten in Layer-Dateien wird der vollständige Diff
  gelesen (D225).
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`, `ruff`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und
  eine Pipe auf `tail`, `awk` oder `python3` sind die nützlichen Ausnahmen. Nach Regel 39 sichert
  eine Zeile, die nur ausgibt, nichts: `test (git branch --show-current) = main` statt der Ausgabe.
- **Ein Wächter, der nur prüft, sagt nicht, was zu tun ist.** In den Merge-Block gehört
  `git checkout main` **vor** den Wächter, nicht statt seiner.
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

### Die Zitiergrammatik — geschlossen

Seit D232 gibt es keinen offenen Teil. Vier Teile: der Dateiname mit oder ohne `.md`; die
Kurzform `NN`/`NNx` über `LAYER_FILES` (dreizehn Einträge, geschlossen); die Bereichsform
`NAME §A–§B` (D228, kein Leerraum um den Strich); die Anhangsnummer als Großbuchstabe mit Punkt
vor der Ziffernfolge (D230). Dazu die Backtick-Toleranz zwischen Namen und Paragraphenzeichen
(D231). Alles andere in `.py` ist ein Befund (D227); in `.md` bleibt der bare Verweis zulässig.

**Die Grenze, die bleibt:** die Prüfung sichert, dass das Ziel **existiert**, nicht dass es
**stimmt** (D229, mit Zahlen bestätigt in D233). Ein Verweis auf einen vorhandenen, aber sachlich
falschen Abschnitt bleibt grün. Gemessene Fehlerrate an der einzigen vollständig geprüften Datei:
zwei von 25.

**Die Regex im Kopf behalten, wenn Fremdzitate in eine Datei sollen:** `SECTION_REF` verlangt den
Namen unmittelbar vor dem Paragraphenzeichen und die Ziffer unmittelbar dahinter. Gesetzesstellen
in der Form mit Leerzeichen nach dem Paragraphenzeichen werden nicht als Verweis gelesen.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt. Eine **Ersetzung** ist eine Löschung
  plus eine Einfügung.
- **Prüfregel 46: aus der Projektkopie kommt jede absolute Zeilenangabe um eins zu hoch.** Wer
  eine Datei sauber aus dem Archiv extrahiert (den Zeilenumbruch hinter dem Dateitag konsumieren)
  und den Hash gegen das Repo prüft, hat korrekte Zeilennummern — das ist der billigere Weg als
  das Abziehen im Kopf.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Zählvorschriften:** Registerköpfe `grep -c '^### D' 07-decisions.md`; Prüfregeln
  `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`; Branches `git branch -a | wc -l`; Abschnitte je Datei
  `grep -n '^## ' <datei>`.
- **Die Projektkopie wird nach jedem Push nachgezogen** (D224, Prüfregel 43), mit fünf Kaltzahlen
  im `--header-text`, Aufruf über `npx --yes repomix`. Der Wächter meldet einen Überschuss von
  eins: `.claude/settings.local.json` wird gepackt, obwohl git sie ignoriert. Kein Befund.
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
- **Mehrere Dateien in einem Skript**, wenn sie in denselben Commit gehören. Fünf Ersetzungen über
  drei Dateien haben in `00aa` in einem Lauf funktioniert.
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42). Bewährt hat sich
  zusätzlich, im Trockenlauf gegen Kopien in `/tmp` die Zeilenlänge und die Verweisauflösung mit
  der echten `SECTION_REF` nachzurechnen, bevor die Datei ausgeliefert wird.
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`. Prüfregel 40: der Kopf wird gemessen, nicht aus dieser Zeile
abgeschrieben; der Übergabe-Commit dieser Datei liegt über dem hier genannten Stand.

Nach `00aa`: **597 Tests** plus 14 Eigenschaftstests. Register **D1–D237**, Prüfregeln **1–46**.
**Drei Branches**. Keine offenen Läufe. Der Stand nach D237 ist `6bd811d`.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
  `§7` zählt seit `00aa` **vier** Nukleus-Akte auf; die Föderationsstimme ist ausdrücklich keiner.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A. Die Axiome A1 bis A3 stehen in `§1`.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung. `§7.2` trägt seit `00aa`
  den benannten Föderationsschlüssel, `§8` die Selbstblockade als getragene Grenze.
- **Fassade** (`mensch_als_republik/resolve.py`), **Kettenbauer** (`tests/kettenwelt.py`),
  **Werkzeugschicht** (`werkzeuge.md`), **Linter** `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py`, `tools/check_tree.py`,
  `tools/splice_run.py`.

**Neu in der letzten Sitzung:** D233 bis D237, sechs Läufe, zwei geschlossene Punkte der offenen
Liste und eine Grundsatzfrage, die vorher nicht gestellt war.

- **D233** — Zwei sachlich falsche Verweise in `example-nucleus.md`, nicht einer. Die zweite
  Prüfklasse für Verweisrichtigkeit ist mit Zahlen verworfen: 48 Prozent Blindquote.
- **D234** — Befund: die Föderationsstimme trägt keinen Autorisierungsweg. Kein Registereintrag
  über D1 bis D233 nennt die Föderation; die Frage war nie gestellt.
- **D235** — `participants` einer Föderation benennt einen eigenen Schlüssel des Kindes, nicht
  seinen aufgelösten Nukleus-Schlüssel. Der abgelöste Schlüssel bleibt stimmfähig, und das ist
  nicht schließbar: die Gegenmaßnahme verlangt Konsens, den MaR nach `08 §2.3` nicht hat.
- **D236** — Kein Ausschlussmechanismus, kein Stimmverbot, keine Schlichtung als Ausweg. Exit ist
  die Antwort; ein Genesis braucht niemandes Zustimmung. Mit Literaturtabelle nach dem Muster
  von D124 und der Kennzeichnung, welche Quellen selbst gelesen wurden.
- **D237** — Reifegrad und die beschlossene Reihenfolge der nächsten Arbeit.

## Was die letzte Sitzung gelehrt hat

**Eine Frage nach Verweishygiene hat eine Grundsatzeigenschaft freigelegt.** Jede Autoritätsliste
in MaR ist ein Bearer-Recht: `participants`, `root_keys` und `arbitration.arbitrators` werden
byte-weise verglichen, keine wird aufgelöst. Wer die Bytes hält, hat die Befugnis, bis die Liste
geändert ist — und wer in der Liste steht, stimmt über seine eigene Streichung mit. Die Föderation
war nur der Ort, an dem das zuerst weh tat.

**Zweimal ist eine Position gekippt, beide Male vor dem Lauf und deshalb billig.** Erst die
Neigung, `participants` byte-fest zu lassen und die Kosten nur zu benennen — gefallen, als die
Sicherheitsseite gerechnet war. Dann die Empfehlung des Rechercheberichts, einen
Nachfolge-Mechanismus zu bauen — gefallen, weil er die Blockade nicht umgeht, solange der
Nachfolgebeschluss derselben Auszählung unterliegt. Kandidat für eine Prüfregel, nicht
entschieden: er liegt sehr nah an 41 und verdient vielleicht nur ein Beispiel dort.

**Der zweite Kandidat aus `00z` steht weiter offen:** wer literalen Text beauftragt, nennt die
Zeichen, die hinein sollen, ausdrücklich — Backticks in einem Prompt sind mehrdeutig.

## Der nächste Schritt

Die Reihenfolge steht mit D237 fest.

1. **Die siebzehn Stummelzeilen glätten** (D223). Gemessen aus `git show e98b7f2`: siebzehn
   eingefügte Zeilen unter 40 Zeichen in neun `.md`-Dateien — `00-nucleus-genesis-constitution.md`
   (2), `01-claim-atom.md` (4), `02-golden-anchors.md` (1), `04-governance.md` (2),
   `06-services.md` (3), `07-decisions.md` (1), `example-nucleus.md` (1),
   `genesis-bindung-prompt.md` (1), `werkzeuge.md` (2). Die Treffer in `tools/check_specs.py` sind
   neuer Code aus demselben Commit und keine Stummel. Zwei Fälle brauchen eigene Prüfung: eine
   Blockquote-Fortsetzung in `01-claim-atom.md` und eine eingerückte Zeile, die in einem Codeblock
   stehen könnte. **Bedingung aus D223:** der Splice muss je Absatz belegen, dass die Wortfolge
   unverändert bleibt — Vergleich nach Normalisierung des Umbruchs, nicht Augenschein.
2. **Die MUSS-Aussagen gegen ihre Prüfer messen.** Eine endliche, mechanisch aufzählbare Menge;
   jede Aussage hat entweder einen Test oder ist ein Befund.
3. **Layer 01 in einer zweiten Sprache**, gegen die bestehenden Golden Anchors. Kanonische
   CBOR-Kodierung, Signaturprüfung, elf Reject-Codes, acht Zustände. Cursor-Credits liegen bereit.
   Jede Abweichung und jede Rückfrage ist eine Mehrdeutigkeit der Spec, die sich von allein meldet.

## Offen

- **Der Reflow der siebzehn Zeilen** (D223, D237). Siehe oben, Menge gemessen.
- **Die MUSS-Extraktion** (D237). Noch kein Verfahren festgelegt.
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
Prüfklasse für Verweisrichtigkeit (D233, mit Zahlen verworfen). **Die Föderationsstimme (D235),
der Ausschlussmechanismus (D236) — und `04 §7.2` ist damit aus der offenen Liste.**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. D237 hält aber fest, dass die letzten Läufe überwiegend das Werkzeug geschärft haben
und nicht das Werk — die Zweitimplementierung ist der beste verfügbare Ersatz für die fehlende
Außenprüfung, und sie ersetzt sie nicht.
