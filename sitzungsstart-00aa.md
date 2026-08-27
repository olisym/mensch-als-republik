# Sitzungsstart: 00aa (MaR)

Die Buchstabenreihe `00u` bis `00z` ist erschöpft; verdoppelt läuft sie weiter, ohne mit den
Schichtpräfixen zu kollidieren. `check_specs.py` nimmt `sitzungsstart-*.md` über einen Glob aus,
der Name ist ihm gleich.

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
die Nummer. Neu ist **46**: Zeilennummern und Zeilenzahlen aus der Projektkopie sind um eins zu
hoch (D232).

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird.

Was in der letzten Sitzung am meisten getragen hat:

- **Die Klassen zählen, bevor man sie behandelt.** Der Sitzungsstart `00z` beschrieb die
  Anhangsform als *eine* Form. Gemessen waren es drei Referenten in einer Schreibweise: ein
  Anhangsabschnitt, ein Anhang als Ganzes und ein Axiom aus einer Liste. Erst diese Trennung hat
  die Entscheidung möglich gemacht, und sie hat eine vorher bezogene Position gekippt.
- **Eine Form gegen die Regex halten, nicht gegen das Auge.** Der eine Verweis, den D230 als
  Ertrag nannte, war selbst nicht qualifiziert — der Backtick stand zwischen Namen und
  Paragraphenzeichen. Daraus wurde D231 und eine Berichtigung im nächsten Eintrag.
- **Der Fork, den man beim Prompt-Schreiben bemerkt, ist ein Registereintrag.** Beim Ableiten des
  Überschriften-Zuwachses fiel auf, dass der Kommentar über `LAYER_FILES` durch die Änderung
  falsch wird. Das kam als Punkt in den Prompt, nicht nebenbei in den Diff.
- **Der Prompt verlangt den vollständigen Diff** (D225). Damit fallen Abnahme und Merge in eine
  Runde. Unberührt bleibt: **der Bericht ist nie die Abnahme**, geprüft wird der Diff.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`, `ruff`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und
  eine Pipe auf `tail` oder `python3` sind die nützlichen Ausnahmen. Nach Regel 39 sichert eine
  Zeile, die nur ausgibt, nichts: `test (git branch --show-current) = main` statt der Ausgabe.
- **Ein Wächter, der nur prüft, sagt nicht, was zu tun ist.** Nach einem Lauf steht der Baum auf
  dem Lauf-Branch; der Block bricht dann an der ersten Zeile ab und tut nichts. In den
  Merge-Block gehört `git checkout main` **vor** den Wächter, nicht statt seiner.
- **Kommandosubstitution in doppelten Anführungszeichen braucht `$`** — fish liest `"(cmd)"`
  wörtlich, `"$(cmd)"` führt aus.
- **Spec-Dateien und Splice-Skripte als Download**, nicht als Copy-Block. Werkzeug-Prompts als
  Datei. Downloads landen in `~/Downloads` — der Kopierschritt nach `/tmp` gehört in den Block.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet` — aber nur für
  Dateien, die unverändert sein **müssen**.
- Bei neuen Dateien `git add` **vor** `make check`. Explizite Pfade, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. **Prosa bricht bei 100 Zeichen; Tabellenzeilen
  und Codeblöcke sind ausgenommen, und `make check-specs` prüft es** (D222). Für Python gibt es
  **keine** Zeilenlängenregel; D205 hat das mit Zahlen entschieden und nicht wieder aufzumachen.
- **Ein Prompt im Wurzelverzeichnis wird von `check_specs.py` mitgeprüft.** Wer darin einen
  kaputten Verweis als Literal zitiert, macht die eigene Datei rot; nach D210 wird die Nummer
  ohne Paragraphenzeichen genannt. Ausgenommen sind `07-decisions.md` und `sitzungsstart-*.md` —
  diese Datei darf frei zitieren, aber **nicht** von der Zeilenlänge.
- **Eine Regex, die in einen Prompt oder eine Spec-Datei soll, geht nicht.** Escapes sind dort ein
  eigener Befund. Regexänderungen werden in Prosa beauftragt: welche Zeichenklasse, an welcher
  Stelle, optional oder nicht. `00v` und `00z` haben so funktioniert.

### Die Zitiergrammatik — geschlossen, vier Teile

Seit D232 gibt es keinen offenen Teil mehr. Die Grammatik kennt:

1. **Den Dateinamen**, mit oder ohne `.md` — `02a-maxflow-prompt.md §2.7`. Injektiv von selbst.
2. **Die Kurzform** `NN` und `NNx` über `LAYER_FILES`. Dreizehn Einträge, **geschlossen**.
3. **Die Bereichsform** `NAME §A–§B` (D228). Bindet beide Nummern an denselben Namen.
   Halbgeviertstrich und Bindestrich sind zulässig, Leerraum um den Strich **nicht**.
4. **Die Anhangsnummer** (D230): ein einzelner Großbuchstabe mit Punkt vor der Ziffernfolge, in
   Überschriften wie in Verweisen. `§Anhang C` als Wortform gehört **nicht** dazu und wird in
   Prosa geschrieben; ein Axiom aus einer Liste auch nicht.

Dazu **zwei Schreibweisen des Namens** (D231): ein schließender Backtick zwischen Namen und
Paragraphenzeichen wird toleriert. `` `01 §1` `` und `` `01` §1 `` sind derselbe Verweis. Der
Bestand schreibt überwiegend die erste Form; `00-nucleus-genesis-constitution.md` führt elf
qualifizierte Verweise, alle elf in Backticks.

Alles andere in `.py` ist ein Befund (D227). Ein Kurzform-Name ohne Tabelleneintrag ist ein
Befund (D219); ein fehlender **Dateistamm** ist keiner (D221). In `.md` bleibt der bare Verweis
zulässig, weil dort der Selbstverweis der Normalfall ist.

**Die Grenze, die bleibt:** die Prüfung sichert, dass das Ziel **existiert**, nicht dass es
**stimmt**. Ein Verweis auf einen vorhandenen, aber sachlich falschen Abschnitt bleibt grün.
`example-nucleus.md` ist der erste gemessene Fall.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt, und auch nicht aus dem Netto-Zuwachs
  eines Trockenlaufs abgeleitet: eine **Ersetzung** ist eine Löschung plus eine Einfügung. In
  `00z` wurde `8 0` angekündigt, wo `9 1` stand, weil eine nachgezogene Zeile mitzählte.
- **Prüfregel 46: aus der Projektkopie kommt alles um eins zu hoch.** Jeder der Dateikörper im
  Archiv beginnt mit einem Zeilenumbruch hinter dem Dateitag. Vor jeder absoluten Zeilenangabe
  die führende Leerzeile abziehen; im Prompt bleibt der Ankertext maßgeblich.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Zählvorschriften, die tragen:**
  - Registerköpfe: `grep -c '^### D' 07-decisions.md`.
  - Prüfregeln: `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`.
  - Branches: `git branch -a | wc -l`.
  - Abschnitte je Datei: `grep -n '^## ' <datei>`.
- **Die Projektkopie wird nach jedem Push nachgezogen** (D224, Prüfregel 43). Der Baustein hängt
  hinter jedem `git push`, schreibt nach `/tmp`, trägt fünf Kaltzahlen im `--header-text` und
  zählt gepackte gegen versionierte Dateien. Aufruf über `npx --yes repomix`.
- **Der Wächter meldet einen Überschuss von eins**, und das ist erklärt: die lokale Konfigdatei
  unter `.claude/` wird gepackt, obwohl git sie ignoriert. Kein Befund, nicht zu untersuchen.
- **Die Kopie ist byte-treu, mit einer Ausnahme:** leere Dateien und Dateien ohne Schluss-Newline
  lassen sich aus dem Archiv nicht exakt rekonstruieren. Wer die Kopie gegen `main` prüft, prüft
  mit `sha256sum -c` je Datei — ein Gesamthash kann eine Teilhypothese nicht widerlegen.
- **Verworfen für die Kopie:** `--compress`, `--remove-comments`, `--remove-empty-lines`,
  `--output-show-line-numbers`, `--no-file-summary`. Begründungen in D224; nicht wieder aufmachen.
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position,
  **40** vor jeder Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung,
  **43** vor jeder Zahl aus der Kopie, **44** vor jeder abgeleiteten Anzahl, **46** vor jeder
  Zeilenangabe.
- **Prüfregel 28**: die Welt im Prompt ist Feld für Feld die gemessene Welt.

### Splices

Ein Splice ist ein Skript mit `assert`, dass der Anker genau einmal vorkommt. Gefahren wird er mit
`python3 tools/splice_run.py /tmp/splice-dNNN.py` (D225). Der Harness verlangt einen sauberen
Baum, erzwingt das Scheitern des zweiten Laufs, prüft die Zeilenlänge am Ergebnis und setzt bei
jedem Fehlschlag zurück.

- **Das Skript liegt in `/tmp`, nicht im Wurzelverzeichnis** — sonst meldet der Harness den Baum
  als unsauber. `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Zwei Dateien in einem Skript**, wenn beide in denselben Commit gehören. Der Harness verlangt
  vor jedem Lauf einen sauberen Baum; zwei Skripte hintereinander scheitern am zweiten.
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42).
- **Tabellenzeilen sind von der 100-Zeichen-Grenze ausgenommen** (D222).
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.** Wer einen Docstring
  zitiert, schreibt ihn ohne die Anführungszeichen.
- **Was der Harness nicht fängt** (D226): einen Splice, der eine zu lange Zeile entfernt und eine
  andere einsetzt, und eine unversionierte Datei, die ein gescheiterter Splice angelegt hat.
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`.

**Der Kopf ist nicht `c3b07f5`.** Das ist der Stand nach D232; der Übergabe-Commit dieser Datei
liegt darüber. Prüfregel 40 — der Kopf wird gemessen, nicht aus dieser Zeile abgeschrieben.

**597 Tests.** Register **D1–D232**, Prüfregeln **1–46**. **Drei Branches** (`main`,
`origin/HEAD`, `origin/main`). Keine offenen Läufe.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
  `§10` nennt beide Vermerke mit ihren Subjekten (D212).
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A. Die Axiome A1 bis A3 stehen in `§1`, nicht in einem Anhang.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`. `§10` nennt die
  sechs Vermerke mit ihren Subjekten.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`. `§6.1`
  führt seit D212 die Subjekttabelle mit vierzehn Arten.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung, `§3.5` mit der Subjektregel
  (D198), `§4.1` mit Bedingung 6 (D200), `§4.5` mit der berichtigten Vermerksgrenze (D203).
- **Fassade** (`mensch_als_republik/resolve.py`): `resolve_state` und `NucleusState`.
- **Kettenbauer** (`tests/kettenwelt.py`), **Werkzeugschicht** (`werkzeuge.md`).
- **Linter**: `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py` (Verweisprüfung über Python
  seit D215, Dateinamensform seit D221, Zeilenlänge seit D222, Bereichsform seit D228, Befund für
  bare Verweise seit D227, Anhangsnummer seit D230, Backtick-Toleranz seit D231),
  `tools/check_tree.py`, `tools/splice_run.py`.

**Neu in der letzten Sitzung:** D230 bis D232, ein Lauf mit zwei Commits, Prüfregel 46, die in
allen vier Teilen geschlossene Zitiergrammatik.

- **D230** — Die Anhangsform wird auf Großbuchstabe, Punkt, Zahl beschränkt und geprüft. Gemessen:
  29 Vorkommen der Schreibweise, davon zwölf echte Verweise in drei Referentenklassen, drei davon
  ins Leere zeigend. Verworfen: die Form in `.md` verbieten, gar nicht prüfen, die Wortform
  mittragen, `check_bare_refs` auf Buchstaben erweitern.
- **D231** — Der schließende Backtick zwischen Namen und Paragraphenzeichen wird toleriert. Elf
  Stellen in sieben Dateien, alle grün, keine angefasst. Enthält die Berichtigung zu D230: der
  Ertrag der Anhangserweiterung allein war null, nicht eins.
- **D232** — Abnahme `00z`. Ein Defekt aus dem Prompt (Code-Span als Auszeichnung gelesen), der
  Versatz der Projektkopie, Prüfregel 46.

## Was die letzte Sitzung gelehrt hat

**Eine Position, die vor der Messung bezogen wird, hält selten.** Zweimal in einer Sitzung: erst
die Empfehlung, die Anhangsform gar nicht zu prüfen — gefallen, als die drei Referentenklassen
gemessen waren. Dann der Ertrag von „einem Verweis" — gefallen, als die Backtick-Stellung geprüft
war. Beide Male war die Korrektur billig, weil sie vor dem Lauf kam.

**Ein Fehler, der sich in Differenzen weghebt, hält lange.** Der Zeilenversatz der Projektkopie
war seit D224 in jeder Messung, aber der Zuwachs stimmte immer, und nur der Zuwachs war je ein
Kriterium. Sichtbar wurde er erst, als eine absolute Zeilennummer in einen Prompt ging.

**Backticks in einem Prompt sind mehrdeutig.** Ein Code-Span markiert Text als Literal *des
Prompts* — er sagt nicht, ob die Zeichen in die Zieldatei sollen. In `00z` hat das Werkzeug sie
folgerichtig als Auszeichnung gelesen, und der Verweis landete ohne Backticks im Bestand.
Kandidat für eine Prüfregel, nicht entschieden: wer literalen Text beauftragt, nennt die
Zeichen, die hinein sollen, ausdrücklich.

**Das Werkzeug hat wieder gemeldet statt angepasst.** Fünf verschobene Zeilennummern, nach
Inhalt getroffen, in einem eigenen Abschnitt berichtet. Der Supervisor war auch in dieser Sitzung
die häufigere Fehlerquelle.

## Der nächste Schritt

**Vorschlag: `example-nucleus.md`.** Er ist der einzige offene Punkt, der zugleich gemessen,
klein und abschließbar ist — und er führt die Arbeit vom Prüfer zurück in die Spec. Zwei Dinge
liegen dort: die Kapazitätsformel zitiert `02 §2` (Graphmodell), gemeint ist `02 §3`
beziehungsweise `02a §2.2`; und die Datei ist seit D202 unvollständig, wobei `§5.1` steht.

Der erste Fall ist der erste gemessene Beleg für die Grenze aus D229: formal gültig, sachlich
falsch, grün. Die Frage, die dabei zu benennen und **nicht** beiläufig zu entscheiden ist: gibt
es eine billige zweite Prüfklasse, oder bleibt die Richtigkeit eines Verweises Sache des Lesers?
Die ehrliche Erwartung ist das Zweite — dann ist der Lauf eine Korrektur und kein Werkzeugbau.

Andere Kandidaten, falls die Sitzung anders laufen soll: die elf Absätze mit Stummelzeilen
(D223, reine Hygiene, ein eigener Lauf), `04 §7.2` Föderation (nie durchgerechnet, substanziell),
`SUBGRANULAR_VOUCH.subject` (D173, ungeprüft).

**Nach vier Sitzungen an der Zitierkonvention ist das Meta-Thema erschöpft.** Wer den nächsten
Schritt wieder dort sucht, sollte einen benannten Grund haben.

## Offen

- **`example-nucleus.md` zitiert für die Kapazitätsformel den falschen Abschnitt** — genannt ist
  `02 §2`, gemeint ist `02 §3` beziehungsweise `02a §2.2`. Formal gültig, deshalb grün. Der erste
  gemessene Fall der Grenze aus D229. Siehe oben.
- **`00z-anhangsform-prompt.md` trägt fünf um eins zu hohe Zeilenangaben.** Bewusst nicht
  berichtigt (D232): die Datei beschreibt einen vergangenen Lauf.
- **Der Verweis in `02b-abnahme.md` auf B.4 bleibt bar und ungeprüft.** In `.md` ist das der
  Normalfall; ein Selbstverweis wird nicht mit dem eigenen Dateinamen qualifiziert.
- **`tests/profiles/test_credit.py` ist die einzige Python-Datei ohne Schluss-Newline.** `ruff`
  fängt das im aktuellen Regelsatz nicht. Kosmetisch; eine eigene Entscheidung wert, wenn jemand
  die Regel `W292` einschalten will.
- **`.claude/settings.local.json` landet in der Projektkopie**, obwohl git sie ignoriert. Erklärt
  den Überschuss von eins beim Wächter. Harmlos, aber eine lokale Konfigdatei hat in einer
  Messgrundlage nichts zu suchen.
- **Die Sitzungsstart-Datei ist ein monolithisches Rewrite** (D218). Vorgeschlagen ist eine
  eigene, nur per Splice editierte Datei für die offene Liste. Nicht entschieden.
- **Es gibt keine Kontextdatei für das Werkzeug** (D218). Fork mit benanntem Gegenargument.
- **Das Register ist ein Fünftel der Projektkopie** (D224, entschärft mit D225). Beobachtung ohne
  Dringlichkeit; eine Teilung nach Ären müsste zuerst gegen `tools/register_index.py` gemessen
  werden.
- **Die Verweisprüfung kann Listenpunkte nicht von Unterabschnitten unterscheiden** (D209).
- **Der Harness vergleicht Zeilenzahlen, er identifiziert Zeilen nicht** (D226).
- **Zwei Registerverweise zeigen ins Leere**, `03 §5.1` und `03 §11`. Bewusst nicht nachgezogen:
  das Register beschreibt vergangene Stände.
- **Elf Absätze führen Stummelzeilen** (D223). Nebenwirkung von `00w`, benannt und nicht
  repariert. Glätten ist ein eigener Lauf.
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173).
- **Die Sondierwelt in `test_benennung.py` erzeugt keine Vermerke** (D173).
- **Wie weit die Regierbarkeitsprüfung reicht** (D200). Zurückgestellt, bis ein Fall sie erzwingt
  — **nicht vorher aufmachen**.
- **`RATIFY_WITH_EXPIRY` und der Zeugenpfad tragen die Weitergaberegel ungeprüft** (D203).
- **Vergleiche gegen `dedupe_sort` sind für die Reihenfolge zirkulär** (D196).
- **Vier `Finding`-Klassen, drei `dedupe_sort`** (D183, Zählung mit D207 berichtigt): das vierte
  gehört `PolicyNote` in `policy.py`, einer fünften Vermerksfamilie mit anderer Feldform, deren
  Trennung `03 §1.2` begründet. Nicht anfassen, ohne die Frage zu stellen, ob die Enums je
  zusammengeführt werden.
- **Eine Schwelle für Autoritätslisten** — mit D166 zurückgestellt. Wird für `root_keys`,
  `nucleus_keys` und `arbitration.arbitrators` **zugleich** beantwortet oder gar nicht.
- **Darf ein Amendment ein deklariertes Prädikat weglassen?** Gehört an `04 §5` (D167).
- **Der Beispielnukleus kann Epoche-1- von Epoche-2-Policy nicht unterscheiden** (D169). Von D188
  negativ beantwortet, in `§5.1` seit D202 ausdrücklich benannt.
- **`genesis[4]` und die Auszählung**: `GV-24` führt ein Genesis, dessen deklarierte Verfassung in
  der Auszählung nirgends vorkommt.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut. Solange er fehlt,
  verlassen Vermerke ihren Erzeugungskontext nur über die Weitergabegrenze aus D203.
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
- **`04 §7.2` Föderation** nicht durchgerechnet.
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **Braucht der Node eine eigene Beschreibung?** D180 sagt ausdrücklich nein.
- **Layer 05.** Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf), die Beta-Reputation
  mit dem Moral-Licensing-Problem — und seit D178 die Frage, ob wiederholtes Stimmen auf
  unveröffentlichte Vorschläge eine Folge tragen soll.

**Erledigt und nicht wieder aufzumachen:** die Zeilenlängenfrage für Python ist mit D205 verneint.
Die Frage nach einer dritten `ruff`-Gruppe ist mit `ARG` beantwortet. Der Fork aus D197 ist mit
D200 entschieden. Die Formfrage für `Finding.subject` ist mit D207 entschieden. Ein
Übersichtsdokument über die Schichten ist mit D209 verworfen. Die Fangbreite der Prädikatprüfer
ist mit D213 entschieden. Die Löschung von `is_nuc_predicate` ist mit D216 vollzogen. Teil A der
Zitierkonvention ist mit D219 und `00u` erledigt, Frage 1 mit D221 und `00v`, Frage 2 mit D227 und
den vier Tranchen aus `00y`. Die Zeilenlänge ist mit D222 und `00w` geprüft. Das Nachziehverfahren
steht mit D224. Das Temp-Verzeichnis für Splices ist mit D225 abgeschafft. Die Bereichsform ist
mit D228 entschieden, ein eigener Test für `tools/` mit D229 verworfen. **Die Anhangsform ist mit
D230 entschieden, die Backtick-Form mit D231, und `00z` ist mit D232 abgenommen. Die
Zitiergrammatik ist geschlossen.**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.
