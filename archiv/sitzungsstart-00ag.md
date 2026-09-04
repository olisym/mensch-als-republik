# Sitzungsstart: 00ag (MaR)

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

Was in `00ae` und `00af` am meisten getragen hat:

- **Die Abnahme läuft über Zielhashes, nicht über gelesenen Diff.** Wird eine Änderung lokal gegen
  eine vollständige Kopie des Bestands gerechnet und dort mit der echten `check_specs.py` geprüft,
  belegt ein `sha256sum -c` der Ergebnisdateien byteweise, dass im Repo genau das entsteht, was
  geprüft wurde. Voraussetzung: die Kopie ist hash-gleich mit dem Repo, und die Prüfung läuft über
  **alle** Wurzel-`.md`. In `00af` sind so drei Splices mit vier Registereinträgen abgenommen
  worden, keiner davon über einen gelesenen Diff.
- **Ist die Kopie veraltet, wird sie rekonstruiert und der Quellhash mitgeliefert.** Nach dem
  Werkzeuglauf war der Repo-Stand um C.12 voraus; der Abschnitt ließ sich aus dem gelieferten Diff
  in die Kopie einsetzen. Der Beleg ist ein `sha256sum -c` der **Quelldateien** als zweiter Job im
  Block: stimmt die Rekonstruktion nicht, bricht die Kette ab, bevor etwas geschrieben wird. Das
  spart den Nachzug der Projektkopie mitten in der Sitzung.
- **Die Projektkopie wird an einzelnen Dateien verankert, nicht am Archivhash.** Vier aus der
  Kopie extrahierte Dateien, von Oli mit `sha256sum -c` geprüft, sind der billige und scharfe
  Test — und sie eichen zugleich die Extraktion. Geschnitten wird am `file`-Tag, wobei das
  Newline direkt hinter dem öffnenden Tag und das vor dem schließenden nicht zum Inhalt gehören;
  wer so extrahiert und den Hash prüft, hat korrekte Zeilennummern und Prüfregel 46 greift nicht.
- **Golden Numbers gehören nicht in den Prompt.** In `00af` habe ich NV13 auf zwei Wegen selbst
  gerechnet — mit einem an NV5 geeichten eigenen Rechner und getrennt über den Generator — und
  beide Werte zurückgehalten; der Prompt fixierte nur die Welt Feld für Feld, Zeitstempel
  eingeschlossen. Die Übereinstimmung war dadurch eine Messung und nicht die Rückgabe der eigenen
  Eingabe.
- **Vor dem Prompt eine Nullprobe.** Die Codeänderung ohne die neuen Tests lokal nachgebaut: 622
  grün, vorher wie nachher. Damit war gemessen statt vermutet, dass der Bestand blind ist und die
  neuen Träger die **gesamte** Trägermenge sind — und die Rücknahmeprobe des Werkzeugs war
  vorab geeicht (Prüfregeln 49, 51).
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
  eine Pipe auf `tail`, `awk` oder `grep -q` sind die nützlichen Ausnahmen. Nach Regel 39 sichert
  eine Zeile, die nur ausgibt, nichts: `test (git branch --show-current) = main` statt der Ausgabe.
- **Mehrere Hashes prüft ein `printf` mit wiederholtem Format.** Ein Formatstring aus zwei
  Platzhaltern und Zeilenumbruch, dahinter die Paare aus Hash und Dateiname, die Ausgabe in
  `sha256sum -c`: eine Zeile, ein Wächter, kein Heredoc.
- **`set -l` und verschachtelte Kommandosubstitution gehören nicht in einen Copy-Block.** In
  `00ae` ist ein Block mit `set -l branches (count (git branch -a))` **ohne eine einzige
  Ausgabezeile** verworfen worden. Zahlen für den `--header-text` werden aus einer vorherigen
  Ausgabe abgelesen und als Literal eingesetzt; ein Wächter über `grep -qx` sichert das Literal.
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
Klartext genannt. `01 §C.12` dagegen löst auf und wird von den Generator-Kommentaren benutzt.

**Befund-Dateien sind zitierfähig.** `00ad-fragen-befund.md` trägt siebzehn nummerierte
Überschriften; `00ad-fragen-befund §5` löst auf und wird in D264 so benutzt.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt, und in einem Wegwerf-Repo gerechnet.
  Eine **Ersetzung** ist eine Löschung plus eine Einfügung; nach Prüfregel 48 werden die
  randgleichen Zeilen abgezogen.
- **`tools/check_specs.py` zählt eine Zeile mehr als `wc -l`.** Der Unterschied zu `git diff` bei
  einer neuen Datei ist derselbe und kein Befund.
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
  Anker-Paare in einer Liste sind billiger als mehrere Skripte.
- **Quellhash vor dem Schreiben, Zielhash nach dem Rechnen.**
- **Ein Anker am Dateiende braucht `endswith`.** Der Anker wird aus der Kopie **abgelesen**.
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42).
- **Mehrere Dateien in einem Skript**, wenn sie in denselben Commit gehören.
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.
- **Ein reiner Textschnitt ohne Werkzeuglauf darf Commit und Merge im selben Block tragen.** Die
  Abnahme liegt vollständig im Zielhash; der Nachzug der Projektkopie kommt getrennt danach.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`. Prüfregel 40: der Kopf wird gemessen, nicht aus dieser Zeile
abgeschrieben.

Nach `00af`: **626 Tests** plus Eigenschaftstests. Register **D1–D268**, Prüfregeln **1–51**.
**Drei Branches**. Keine offenen Läufe. Der Stand nach D268 ist `78e20e5`.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
- **01** Atom, Verifier, **zwölf Reject-Codes**, acht Zustände, `read_claim`. Prädikat-Grammatik
  in `§2.2` und Anhang A. **Anhang C trägt seit D267 dreizehn Abschnitte**: C.1 bis C.4 positiv,
  C.5 bis C.7 negativ, C.8 Byte-Vektoren, C.9 TV5, C.10 die acht Vektoren NV4 bis NV11, C.11 TV6
  und NV12, C.12 NV13.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung.
- **Fassade** (`mensch_als_republik/resolve.py`), **Kettenbauer** (`tests/kettenwelt.py`),
  **Werkzeugschicht** (`werkzeuge.md`), **Linter** `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py`, `tools/check_tree.py`,
  `tools/splice_run.py`.

### Was `00af` entschieden hat

- **D265** — keine Gesamtordnung der Fehlerklassen. `01 §B.1` kennt genau einen Reject-Zustand,
  `malformed`; die zwölf Codes sind Gründe. Tragen mehrere Codes eine wahre Aussage über dieselbe
  Bytefolge, ist die Wahl frei. Normativ bleibt allein **das Verbot des falschen Satzes** aus
  D262, und es gilt für alle Klassen. Die Vektoren binden nur, soweit sie stellen: C.10 trägt acht
  Vektoren mit je genau einem Mangel, BV2 ist der einzige mit zweien.
- **D266** — Feldsatz-Verstöße sind `MALFORMED_CBOR`: fehlendes Pflichtfeld, Key außerhalb der
  Feldtabelle, falsche Byte- oder Array-Länge. Dazu: **die Feldtabelle gilt je Version.** Bei
  nicht unterstützter Version wird nicht mehr gegen `01 §2` geprüft — der Satz wäre falsch.
- **D267** — zwölfter Code `INVALID_PREDICATE` für Formverstöße unter `nuc:`.
  `UNKNOWN_NAMESPACE` ist auf seinen Wortlaut zurückgeschnitten: weder `core/`- noch
  `nuc:`-Präfix. Ein Werkzeuglauf hat ihn gebaut, mit NV13 in `01 §C.12`.
- **D268** — `00ad-fragen-befund §3` ändert keine Norm; die Lesart des Befunds ist die der Spec.
  Benannt wird der Umfang: **selbstenthaltene Gültigkeit** sind die Punkte 1 bis 7 aus `01 §6`
  ohne den bedingten Konjunkt `ziel.I == C.I`. Wissen kann das Urteil nur verengen.

## Was `00af` gelehrt hat

**Eine Regel, die in derselben Sitzung entsteht, kann in derselben Sitzung dreimal arbeiten.** Das
Verbot des falschen Satzes hat nach D265 die Versionsklausel in D266 entschieden und den ganzen
Fork in D267. Es hat dabei zweimal gegen die billigere Antwort entschieden — die Ordnung wäre
teurer gewesen, der zwölfte Code war es. Beides ist dieselbe Prüfung: **trägt die Bytefolge die
Aussage, die der Code macht?**

**Der Defekttyp „normative Tabelle ohne Code" ist der vierte Fund derselben Art.** `01 §2`
(Feldsatz, D266) und Anhang A (Grammatik, D267) sind normativ überschrieben, und ihre Verletzung
hatte keinen Reject-Grund. Vorher: `01 §3` (D261) und `01 §6` Punkt 4 (D263), dort eine Bedingung
ohne genannte Voraussetzung. Das Suchmuster für die restlichen Layer lautet: **wo steht „normativ"
über etwas, das keine Folge hat?**

**Ein Ausdruck, der dreimal getragen hat und nirgends definiert ist, ist eine Schuld.**
„Zustandslose Stufe von Layer 01" hat seit D256 Umfang und Abnahme der Go-Fassung bezeichnet, ohne
dass irgendwo stünde, welche Punkte dazugehören. D268 hat ihn benannt — und das ging erst, seit
D263 den letzten unbedingten Speicherzugriff bedingt gemacht hat. Definierbarkeit war hier das
Ergebnis einer früheren Entscheidung, nicht ihre Voraussetzung.

**Die Nullprobe vor dem Prompt kostet einen lokalen Testlauf und ersetzt eine Glaubensfrage.** Der
Bestand war für `INVALID_PREDICATE` vollständig blind. Hätte das Werkzeug nur zwei rote Tests
gemeldet, wäre ohne Eichung nicht zu sagen gewesen, ob der Bericht falsch ist oder der Bestand.

## Der nächste Schritt

1. **`00ad-fragen-befund §8`** — Hex-Zeilen als Auftrag-Schnittstelle, ausdrücklich nicht Spec.
   Vermutlich ohne Registerfolge; dann als solches festhalten und weiter.
2. **`00ad-fragen-befund §9` bis `§11`** — Trailing-Bytes, Indefinite-Length und Break, doppelte
   Map-Keys semantisch gegen kodiert. Alle drei liegen an `01 §3` und `01 §B.2` und sind nach
   D262 und D266 vermutlich schon entschieden; zu prüfen ist, ob der Text es hergibt.
3. **`00ad-fragen-befund §12` bis `§17`** — `N` auf `core/*`, Alias gegen 64-Hex, Profilregeln,
   Signatur-Preimage, Genesis-Anker, kanonische Map-Sortierung.
4. **Die Gliederung von `pruefregeln.md`** (D249).

**Nicht vergessen:** eine dritte Fassung ist möglich, aber der Anker hat sich bewegt. Nach D258
muss sie denselben Spec-Stand lesen wie die Go-Fassung — das ist `1109b89` beziehungsweise die
daraus beschnittene Datei, **nicht** der jetzige. Wer gegen den reparierten Stand baut, misst die
Reparatur und nicht die Häufung. Beides ist zulässig, aber es sind zwei verschiedene Versuche, und
die Wahl gehört ins Register. Seit D268 ist immerhin sagbar, **was** sie bauen soll.

## Offen

- **Zehn unbehandelte Einträge in `00ad-fragen-befund.md`**: `§8` bis `§17`. Die Liste der zehn
  Fehlerklassen in `§4` bleibt Befund und wird nicht Norm (D265).
- **Ein Kandidat für Prüfregel 52**: wird eine Projektkopie aus einem gelieferten Diff
  rekonstruiert, geht ein `sha256sum -c` der **Quelldateien** als zweiter Job in den Block. Er hat
  in `00af` getragen, ist aber nur einmal gelaufen.
- **`tools/register_index.py` indiziert keine Anhangsverweise.** `01 §B.2` und `01 §C.10` fallen
  durch, obwohl `check_specs.py` sie prüft. Prüfregel 38 in ausführbarer Form ist damit schmaler
  als die Verweisprüfung — ein eigener Lauf, klein.
- **`FOREIGN_LIFECYCLE` hat keinen Vektor und kann keinen bekommen**, solange die Vektoren
  zustandslos gelesen werden: nach D263 verlangt der Code einen bekannten Ziel-Claim. Nach D268
  liegt er als einziger Punkt außerhalb der selbstenthaltenen Gültigkeit.
- **Elf der zwölf Codes tragen einen Vektor.** Die Abdeckung aus D257 ist mit NV13 nachgezogen.
- **Die Gliederung von `pruefregeln.md` ab Regel 37** (D249).
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
Der Vergleichsgegenstand der Kanonizitätsprüfung (D261). Der Vorrang der Fehlerklassen gegen eine
normierte Prüfreihenfolge (D262). Der Code für den falschen `J.tag` auf `core/*` und die
Voraussetzung von `FOREIGN_LIFECYCLE` (D263). Die Feld-Konsistenz auf `core/*` (D264).
**Die Gesamtordnung der Fehlerklassen (D265). Die Codes für Feldsatz-Verstöße und die Geltung der
Feldtabelle je Version (D266). Der zwölfte Reject-Code (D267). Der Umfang einer Fassung ohne
Speicher (D268).**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht.
