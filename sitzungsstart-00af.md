# Sitzungsstart: 00af (MaR)

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
eine Position bezogen wird.

Was in `00ad` und `00ae` am meisten getragen hat:

- **Die Abnahme läuft über Zielhashes, nicht über gelesenen Diff.** Wird eine Änderung lokal gegen
  eine vollständige Kopie des Bestands gerechnet und dort mit der echten `check_specs.py` geprüft,
  belegt ein `sha256sum -c` der Ergebnisdateien byteweise, dass im Repo genau das entsteht, was
  geprüft wurde. Voraussetzung: die Projektkopie ist hash-gleich mit dem Repo, und die Prüfung
  läuft über **alle** Wurzel-`.md`. In `00ae` sind so vier Registereinträge und sieben
  Spec-Schnitte ohne einen einzigen gelesenen Diff abgenommen worden.
- **Die Projektkopie wird an einzelnen Dateien verankert, nicht am Archivhash.** `/tmp` überlebt
  keinen Neustart, und der Hash der XML-Datei sagt ohnehin nichts über das Repo. Vier aus der
  Kopie extrahierte Dateien, von Oli mit `sha256sum -c` geprüft, sind der billige und scharfe
  Test — und sie eichen zugleich die Extraktion. Geschnitten wird am `file`-Tag, wobei das
  Newline direkt hinter dem öffnenden Tag und das vor dem schließenden nicht zum Inhalt gehören;
  wer so extrahiert und den Hash prüft, hat korrekte Zeilennummern und Prüfregel 46 greift nicht.
- **Golden Numbers gehören nicht in den Prompt.** In `00ae` habe ich beide neuen Vektoren selbst
  gerechnet und die Werte zurückgehalten; der Prompt fixierte nur die Welt Feld für Feld,
  Zeitstempel eingeschlossen. Die Übereinstimmung war dadurch eine unabhängige Messung und nicht
  die Rückgabe der eigenen Eingabe.
- **Die Rücknahmeprobe des Werkzeugs wird selbst geeicht.** Ich habe den Lauf lokal ohne die
  beiden handgeschriebenen Tests nachgebaut und Schritt 1 zurückgenommen: kein Test wird rot.
  Damit war die Trägermengen-Behauptung des Werkzeugs gemessen statt geglaubt (Prüfregeln 49, 51).
- **Fremde Artefakte werden nachgerechnet, nicht gelesen.**
- **Der Sitzungsstart ist eine Hypothese, keine Messung.** Der Übergabe-Commit dieser Datei liegt
  über dem hier genannten Stand.
- **Diagnoseläufe geben Zahlen aus, keine rohen Trefferlisten.**
- **Der Bericht ist nie die Abnahme, auch nicht der eigene.**
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`, `ruff`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.

### Shell

- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und
  eine Pipe auf `tail` oder `awk` sind die nützlichen Ausnahmen. Nach Regel 39 sichert eine Zeile,
  die nur ausgibt, nichts: `test (git branch --show-current) = main` statt der Ausgabe.
- **`set -l` und verschachtelte Kommandosubstitution gehören nicht in einen Copy-Block.** In
  `00ae` ist ein Block mit `set -l branches (count (git branch -a))` **ohne eine einzige
  Ausgabezeile** verworfen worden — nicht abgebrochen, sondern gar nicht erst gestartet. Zahlen
  für den `--header-text` werden aus einer vorherigen Ausgabe abgelesen und als Literal
  eingesetzt.
- **Keine Ausgabe heißt: der Block ist nicht gelaufen.** Eine abgebrochene Kette hinterlässt
  immer die Marken bis zur Bruchstelle.
- **Jeder Block trägt Marken.** Vor jedem Abschnitt ein `echo "== NAME =="`, am Ende ein
  `echo "== FERTIG =="`.
- **`string`-Kommandos in einer `and`-Kette sind eine Falle.** `string trim`, `string match` und
  `string replace` geben Exit-Status 1 zurück, wenn sie nichts zu tun hatten. Als Wächter ist das
  nutzbar; als Zwischenschritt bricht es die Kette. `wc -l` liefert mit `count` oder `grep -c`
  eine Zahl ohne Leerraum.
- **Ein Wächter, der nur prüft, sagt nicht, was zu tun ist.** In den Merge-Block gehört
  `git checkout main` **vor** den Wächter, nicht statt seiner. `git branch -d` statt `-D`.
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
Klartext genannt. `01 §C.11` dagegen löst auf und wird von den Generator-Kommentaren benutzt.

**Befund-Dateien sind zitierfähig.** `00ad-fragen-befund.md` trägt siebzehn nummerierte
Überschriften; `00ad-fragen-befund §5` löst auf und wird in D264 so benutzt.

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
Fehlschlag zurück.

- **Das Skript liegt in `/tmp`.** `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Das Skript wird erzeugt, nicht getippt.** Anker und Ersetzung je als `repr`. Mehrere
  Anker-Paare in einer Liste sind billiger als mehrere Skripte; in `00ae` liefen sieben Schnitte
  in einem Lauf.
- **Quellhash vor dem Schreiben, Zielhash nach dem Rechnen.**
- **Ein Anker am Dateiende braucht `endswith`.** Der Anker wird aus der Kopie **abgelesen**.
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42).
- **Mehrere Dateien in einem Skript**, wenn sie in denselben Commit gehören.
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`. Prüfregel 40: der Kopf wird gemessen, nicht aus dieser Zeile
abgeschrieben.

Nach `00ae`: **622 Tests** plus Eigenschaftstests. Register **D1–D264**, Prüfregeln **1–51**.
**Drei Branches**. Keine offenen Läufe. Der Stand nach D264 und dem Vektorlauf ist `3d2cba7`.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A. **Anhang C trägt seit D263 und D264 zwölf Abschnitte**: C.1 bis C.4
  positiv, C.5 bis C.7 negativ, C.8 Byte-Vektoren, C.9 TV5, C.10 die acht Vektoren NV4 bis NV11,
  C.11 TV6 und NV12.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung.
- **Fassade** (`mensch_als_republik/resolve.py`), **Kettenbauer** (`tests/kettenwelt.py`),
  **Werkzeugschicht** (`werkzeuge.md`), **Linter** `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py`, `tools/check_tree.py`,
  `tools/splice_run.py`.

### Was `00ae` entschieden hat

- **D261** — `01 §3` verglich den dekodierten **Core** mit den empfangenen Bytes. Der Core ist die
  Map ohne `σ`; wörtlich befolgt lehnt die Regel jeden signierten Claim ab. Verglichen wird jetzt
  die dekodierte Map. `01 §6` Punkt 2 trug dieselbe Zuschreibung und wurde mitgezogen.
- **D262** — BV2 berief sich auf eine Prüfreihenfolge „2b vor 2c", die es nur in den Kommentaren
  von `verifier.py` gab und der die Einleitung von C.8 widerspricht. Normiert wird jetzt der
  **Vorrang**, nicht die Reihenfolge: `NON_CANONICAL_ENCODING` behauptet, es gebe eine gültige
  kanonische Kodierung desselben Inhalts; trägt der Inhalt einen Mangel, den keine Kodierung
  behebt, ist der Code `MALFORMED_CBOR`. Die Regel steht in `Anhang B.2`.
- **D263** — `J.tag != claim-ref` auf `core/*` ist `MALFORMED_CBOR`, nicht `FOREIGN_LIFECYCLE`.
  `ziel.I == C.I` wird nur geprüft, wenn der Ziel-Claim lokal bekannt ist, und entfällt sonst
  ersatzlos. Ein zwölfter Fehlercode wurde benannt und verworfen.
- **D264** — auf `core/*` entfällt die Feld-Konsistenz `t < t_exp` mitsamt dem Feld. Begründung
  aus `01 §5.3` selbst: ein Reject wirkt wie der Ablauf, nämlich zugunsten von Über-Vertrauen.
  **Hier korrigiert die Zweitimplementierung die Referenz**, zum ersten Mal.
- **Ein Werkzeug-Lauf**: die Punkt-7-Ausnahme in `verifier.py`, TV6 und NV12 in `Anhang C.11`,
  622 statt 617 Tests.

### Das zweite Arbeitsverzeichnis

`~/mar-go` ist ein eigenes Git-Repo **ohne Remote**, Commit `365df9b` auf `main`, 2039 Zeilen,
eigenes deterministisches CBOR ohne Bibliothek. Go liegt in `~/.local/go` (1.27.0) und ist
**nicht im PATH**; Aufruf über `~/.local/go/bin/go`.

Der Hash der beschnittenen Spec, gegen die gebaut wurde:

```
b16251fc02d07c8761a0583fe77ddadd6a6f59e6b7167d889231733170cc051a
```

**Die Fragenliste liegt seit `00ae` im Repo** als `00ad-fragen-befund.md`, Kopf plus siebzehn
unveränderte Einträge, 332 Zeilen. Entschieden sind drei: `§1` (D261), `§2` (D263), `§5` (D264).
`§4` ist zur Hälfte entschieden — D262 hat die Überschneidung von Kodierungs- und Inhaltsmangel
geregelt, die vorgeschlagene Gesamtordnung der zehn Fehlerklassen nicht.

## Was `00ae` gelehrt hat

**Derselbe Defekttyp kam zweimal vor, und beim zweiten Mal war er schneller zu sehen.** `01 §3`
verlangte etwas, das keine Fassung leisten kann; `01 §6` Punkt 4 verlangt mit `ziel.I == C.I`
dasselbe für den zustandslosen Fall. Beide Male hat der Text eine Bedingung normiert, ohne zu
sagen, unter welcher Voraussetzung sie prüfbar ist. Das ist ein Suchmuster für die restlichen
Layer, kein Einzelfall.

**Ein Vektor kann die wörtliche Lesart ausschließen, aber keinen Textdefekt anzeigen.** Eine
Fassung, die `01 §3` wörtlich befolgt, fällt an jedem positiven Vektor durch — sichtbar wird der
Defekt trotzdem nicht, weil jede bestehende Fassung den Text schon repariert hat. Sichtbar wurde
er allein dadurch, dass eine zweite Fassung ihre Abweichung **aufgeschrieben** hat.

**Der Vorrang ist billiger zu normieren als die Reihenfolge.** Eine Schrittfolge bände jede fremde
Fassung an einen Ablauf und entschiede keinen einzigen Ausgang zusätzlich. Die inhaltliche Regel
entscheidet dieselben Fälle und bleibt an jedem einzelnen Claim prüfbar.

**Die Branch-Disziplin ist ausgefallen, und niemand hat es gemerkt.** Prompt-Commit `7c34985` und
Implementierungs-Commit `3d2cba7` liegen beide auf `main`; `lauf/00ae-c11` hat nie existiert. Die
Abnahme trug trotzdem, weil sie auf dem Diff und auf nachgerechneten Zahlen stand und nicht auf
der Branch-Form. Die Ursache ist ungemessen — der Block, der den Branch anlegen sollte, ist nie
zurückgekommen.

**Ein Copy-Block kann verworfen werden, ohne zu starten.** Kein `echo`, keine Fehlermeldung, nichts.
Der Unterschied zum Kettenabbruch ist die fehlende erste Marke.

## Der nächste Schritt

1. **`00ad-fragen-befund §4`** — die vorgeschlagene Ordnung der zehn Fehlerklassen. D262 hat ein
   Stück davon entschieden; die Frage ist, ob der Rest überhaupt normiert werden soll oder ob die
   Vorrangregel genügt und die Liste als Befund stehen bleibt.
2. **`00ad-fragen-befund §7`** — Extra-Keys, fehlende Pflichtfelder, falsche Längen. Der Eintrag
   liest `MALFORMED_CBOR` sehr weit; `Anhang B.2` deckt das nicht ausdrücklich. Vermutlich der
   größte der verbliebenen Brocken.
3. **Die restlichen elf Einträge**, einzeln geprüft und einzeln entschieden: `§3`, `§6`, `§8` bis
   `§17`.
4. **Die Gliederung von `pruefregeln.md`** (D249).

**Nicht vergessen:** eine dritte Fassung ist möglich, aber der Anker hat sich bewegt. Nach D258
muss sie denselben Spec-Stand lesen wie die Go-Fassung — das ist `1109b89` beziehungsweise die
daraus beschnittene Datei, **nicht** der jetzige. Wer gegen den reparierten Stand baut, misst die
Reparatur und nicht die Häufung. Beides ist zulässig, aber es sind zwei verschiedene Versuche, und
die Wahl gehört ins Register.

## Offen

- **Dreizehn unbehandelte Einträge in `00ad-fragen-befund.md`**, dazu `§4` zur Hälfte.
- **`FOREIGN_LIFECYCLE` hat keinen Vektor und kann keinen bekommen**, solange die Vektoren
  zustandslos gelesen werden: nach D263 verlangt der Code einen bekannten Ziel-Claim. Ein Vektor
  dafür braucht eine Weltbeschreibung, nicht nur Bytes.
- **Der Lauf-Branch ist in `00ae` nicht entstanden**; Ursache ungemessen.
- **Die Gliederung von `pruefregeln.md` ab Regel 37** (D249).
- **Ein Kandidat ohne Nummer** (D249): eine neu formulierte Norm wird vor dem Commit gegen die
  offenen Befunde derselben Sitzung gehalten.
- **Siebzehn Wurzel-Markdowns tragen Backslashes**, obwohl die Anweisung keine vorsieht.
- **Die Kampagne mit mutierten Claims** ist beschlossen und ungebaut (D258).
- **N09 ist beobachtet, nicht durchgesetzt** (D119, D246).
- **N10 ist teilgemessen** (D246).
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
- **`EPOCH_FORK` hat keinen Produktivträger** (D138, D176, bewusst).
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
**Der Vergleichsgegenstand der Kanonizitätsprüfung (D261). Der Vorrang der Fehlerklassen gegen
eine normierte Prüfreihenfolge (D262). Der Code für den falschen `J.tag` auf `core/*` und die
Voraussetzung von `FOREIGN_LIFECYCLE` (D263). Die Feld-Konsistenz auf `core/*` (D264).**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht.
