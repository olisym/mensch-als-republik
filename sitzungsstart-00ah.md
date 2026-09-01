# Sitzungsstart: 00ah (MaR)

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

Was in `00ag` am meisten getragen hat:

- **Die Projektkopie wird nicht nur gelesen, sie wird ausgepackt und gefahren.** Aus
  `/tmp/mar-context.xml` lässt sich der ganze Baum rekonstruieren — geschnitten am `file`-Tag,
  Newline hinter dem öffnenden und vor dem schließenden Tag gehören nicht zum Inhalt, die
  Schluss-Newline wird wieder angehängt. Der ausgepackte Baum hat in `00ag` **dieselben 626
  Tests grün** geliefert wie Olis venv. Damit ist er geeicht (Prüfregel 51), und der Supervisor
  kann selbst messen statt zu fragen: Mutanten bauen, Codes ablesen, Nullproben fahren. Das war
  der größte einzelne Gewinn der Sitzung. `cbor2` und `cryptography` nachinstallieren.
- **Vier bis fünf Dateien aus der Kopie, von Oli mit `sha256sum -c` geprüft, verankern sie.**
  Der Archivhash taugt nicht; der `--header-text` kann eine Sitzung alt sein. In `00ag` enthielt
  die Kopie bereits `sitzungsstart-00ag.md`, während ihr Header noch den Commit davor nannte.
- **Ein Vektor mit zwei wahren Codes bindet nichts.** Beim Entwurf von NV14 bis NV19 sind zwei
  Entwürfe daran gescheitert: der Fremdkey-Vektor, wenn ein Dritter anhängt, trägt auch
  `BAD_SIGNATURE`; der Doppel-Key-Vektor mit zweimal demselben Wert trägt auch
  `NON_CANONICAL_ENCODING`, weil last-wins genau TV1 ergibt. Beide wurden umgebaut, bis genau
  ein Code eine wahre Aussage trägt. **Vor jedem Vektor: welche Codes sind hier noch wahr?**
- **Golden Numbers gehören nicht in den Prompt.** Auf zwei Wegen gerechnet — einmal aus
  `vectors_01.json`, einmal aus den Seeds mit reinem `cbor2` und `cryptography` ohne eine Zeile
  Repo-Code — und zurückgehalten. Der Prompt fixierte die Welten Feld für Feld. Die sechs
  Vektoren des Werkzeugs waren byte-gleich; das war eine Messung und nicht die Rückgabe der
  eigenen Eingabe.
- **Vor dem Prompt eine Nullprobe.** Die Codeänderung ohne die neuen Tests lokal nachgebaut:
  626 grün, vorher wie nachher, und alle Mutanten kippen. Damit war gemessen statt vermutet,
  dass der Bestand blind ist, und die fünf Rücknahmeproben des Laufs waren vorab geeicht
  (Prüfregeln 49, 51).
- **Der Bericht ist nie die Abnahme, auch nicht der eigene.**
- **Der Sitzungsstart ist eine Hypothese, keine Messung.** Der Übergabe-Commit dieser Datei
  liegt über dem hier genannten Stand.
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
- **Im Merge-Block steht `git push` vor `git branch -d`.** In `00ag` stand es dahinter, und der
  Block ist an der Löschung abgebrochen: `-d` prüft gegen den **Upstream**, nicht gegen HEAD, und
  ein lokal gemergter Branch gilt als unzusammengeführt, solange `main` nicht gepusht ist. Der
  Wächter war richtig, er stand nur zu früh.
- **Sichtbar und geprüft zugleich geht über eine Datei.** `pytest -q > /tmp/x.txt`, dann
  `tail -1 /tmp/x.txt`, dann `grep -q '^632 passed' /tmp/x.txt`: ein Lauf, eine Ausgabe, ein
  Wächter. Eine Pipe würde eines von beidem fressen.
- **Mehrere Hashes prüft ein `printf` mit wiederholtem Format.** Ein Formatstring aus zwei
  Platzhaltern und Zeilenumbruch, dahinter die Paare aus Hash und Dateiname, die Ausgabe in
  `sha256sum -c`: eine Zeile, ein Wächter, kein Heredoc. `~/Downloads/...` wird darin expandiert.
- **`set -l` und verschachtelte Kommandosubstitution gehören nicht in einen Copy-Block.** Zahlen
  für den `--header-text` werden aus einer vorherigen Ausgabe abgelesen und als Literal
  eingesetzt; ein Wächter über `test (grep -c ...) = <zahl>` sichert das Literal.
- **Keine Ausgabe heißt: der Block ist nicht gelaufen.** Eine abgebrochene Kette hinterlässt
  immer die Marken bis zur Bruchstelle.
- **Jeder Block trägt Marken.** Vor jedem Abschnitt ein `echo "== NAME =="`, am Ende ein
  `echo "== FERTIG =="`.
- **`string`-Kommandos in einer `and`-Kette sind eine Falle.** `string trim`, `string match` und
  `string replace` geben Exit-Status 1 zurück, wenn sie nichts zu tun hatten. Kommandosubstitution
  entfernt Leerraum ohnehin selbst.
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
erzeugt** — im Prompt zu `01 §C.13` stand deshalb „Anhang C.13" in Prosa. Erst nach dem Lauf ist
`01 §C.13` zitierfähig.

**Befund-Dateien sind zitierfähig.** `00ad-fragen-befund §12` löst auf und wird in D273 so
benutzt.

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
  Anker-Paare in einer Liste sind billiger als mehrere Skripte.
- **Der Anker am Dateiende wird aus der Kopie abgelesen, nicht getippt.** In `00ag` hat einmal
  `text[-160:]` als Anker gedient; das ist robust und spart die Fehlerquelle Abschrift.
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42). Ein Assert auf
  eine erwartete **Anzahl** im Ergebnis — etwa 274 Registerköpfe — fängt mehr als eine
  Anwesenheitsprüfung.
- **Quellhash vor dem Schreiben, Zielhash nach dem Rechnen.** Die Abnahme eines reinen
  Textschnitts liegt vollständig im Zielhash; Commit und Merge dürfen im selben Block stehen.
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`. Vor der Testzahl `.hypothesis` und `__pycache__` löschen
(Prüfregel 19). Prüfregel 40: der Kopf wird gemessen, nicht aus dieser Zeile abgeschrieben.

Nach `00ag`: **632 Tests** plus Eigenschaftstests. Register **D1–D274**, Prüfregeln **1–51**.
**Drei Branches**. Keine offenen Läufe. Der Stand nach D274 ist `5370785`.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
- **01** Atom, Verifier, **zwölf Reject-Codes**, acht Zustände, `read_claim`. Prädikat-Grammatik
  in `§2.2` und Anhang A. `§3` trägt seit D270 den Arity-Satz. **Anhang C trägt seit D272
  vierzehn Abschnitte**: C.1 bis C.4 positiv, C.5 bis C.7 negativ, C.8 Byte-Vektoren, C.9 TV5,
  C.10 die acht Vektoren NV4 bis NV11, C.11 TV6 und NV12, C.12 NV13, C.13 NV14 bis NV19.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung. `§2.3` trägt seit D274 den
  Kanonizitätssatz für `v` — **im Text, noch nicht im Code**.
- **Fassade** (`mensch_als_republik/resolve.py`), **Kettenbauer** (`tests/kettenwelt.py`),
  **Werkzeugschicht** (`werkzeuge.md`), **Linter** `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py`, `tools/check_tree.py`,
  `tools/splice_run.py`.

### Was `00ag` entschieden hat

- **D269** — die Hex-Schnittstelle des Go-Auftrags ist keine Norm. Aber die Zusage „je
  Eingabezeile genau eine Ausgabezeile" zwingt den Harness, auch dort einen Reject-Code
  auszugeben, wo gar keine Bytefolge entstanden ist. Das ist der falsche Satz aus D265. Folge nur
  für den nächsten Auftrag: Transportfehler und Verdikt getrennt ausgeben.
- **D270** — die empfangenen Bytes sind die Kodierung **genau eines** CBOR-Items. Restbytes sind
  `MALFORMED_CBOR`. Offen war nicht der Code, sondern was die Eingabe ist: ohne den Satz durfte
  ein Verifizierer einen angehängten zweiten Claim ebenso gut verarbeiten wie verwerfen — und die
  Fassung verwarf ihn stillschweigend als „nicht-kanonisch".
- **D271** — `00ad-fragen-befund §10` und `§11` ändern keine Norm. Doppelte Keys sind über D262
  entschieden, semantische Schlüsselgleichheit ist maßgeblich.
- **D272** — **D266 war Text ohne Code.** Fünf gemessene Ausgänge der Referenzfassung wichen vom
  geltenden Text ab. Der schärfste: jeder Dritte konnte an einen gültigen Claim beliebige
  uint-Felder anhängen, das Ergebnis war gültig, die Signatur verifizierte, und die `claim_id`
  blieb dieselbe. Dazu `version` und `t` als CBOR `true` oder als negative Zahl — angenommen,
  weil `bool` in Python eine Unterklasse von `int` ist und `True == 1`.
- **D273** — `00ad-fragen-befund §12` bis `§17` ändern keine Norm. **Damit ist der Befund
  abgearbeitet**: siebzehn Abschnitte, geschlossen von D261 bis D273, elf davon ohne
  Normänderung.
- **D274** — die Kanonizität von `v` gilt auch in der Auszählung. `01 §7.1` setzt die Anforderung
  dort durch, wo `v` gelesen wird, und nennt für `vouch@1` zwei Stellen; `vote@1` und `ratify@1`
  sind zwei weitere, und `04` sagte dazu nichts. Der Satz steht jetzt in `04 §2.3`, der Code
  fehlt.

## Was `00ag` gelehrt hat

**Der teuerste Defekttyp ist nicht die offene Frage, sondern der geschlossene Beschluss ohne
Lauf.** D266 ist im Juni entschieden, in drei Abschnitte von `01` gefahren und nie gebaut worden;
niemand hat danach gefragt, weil die Spec sauber aussah und die Tests grün waren. Gefunden wurde
es nur, weil eine andere Frage — `00ad-fragen-befund §10` — dazu zwang, die Fassung gegen den
Text zu messen statt gegen sich selbst. **Das Suchmuster für die übrigen Layer:** welcher
Registereintrag hat Verifiziererverhalten beschlossen und taucht in keinem Commit-Betreff und in
keinem Test auf? Das ist mechanisch messbar und der erste Kandidat für einen kleinen Prüfer.

**`isinstance(x, int)` ist kein Test auf uint.** `bool` ist Unterklasse von `int`, und `True == 1`
passiert damit auch jeden Wertvergleich gegen `1`. Der richtige Griff ist `type(x) is int` — und
er stand schon in `governance/tally.py`, wo `_is_yes_choice` ihn seit jeher benutzt. Eine
Konstruktion, die an einer Stelle im Baum richtig ist und an einer anderen fehlt, ist ein
Suchmuster und keine Einzelheit.

**Ein Träger, den es schon gibt, wird nicht noch einmal bestellt.** Schritt 3 des Prompts verlangte
je Vektor einen Test; `tests/test_verifier.py::test_read_claim_reject_vectors` parametrisiert seit
jeher über alle Vektoren mit `expect_reject` und hatte die sechs neuen automatisch aufgenommen.
Ergebnis: +12 statt +6, zurückgenommen vor dem Merge. Prüfregel 27 gilt auch für Testdateien —
**vor jedem verlangten Träger nachsehen, ob er schon existiert.**

**Der Supervisor kann selbst messen.** Der ausgepackte Baum aus der Projektkopie hat in dieser
Sitzung sieben Mutanten, zwei unabhängige Golden-Number-Wege, eine Nullprobe und drei
Befundmessungen getragen, ohne einen einzigen Zug an Oli. Das verschiebt die Grenze zwischen
„fragen" und „nachrechnen" deutlich. Voraussetzung bleibt die Eichung: erst den Bestand fahren
und die bekannte Testzahl reproduzieren, dann messen.

## Der nächste Schritt

1. **Der Lauf aus D274.** `governance/tally.py` und `governance/epoch.py` auf die Form von
   `profiles/payload.py::read_v` ziehen: dekodieren und `is_canonical` im selben `try` (D83),
   Vermerk `NON_CANONICAL_V` in den Governance-Vermerken, defekter Teil fällt weg, nie ein
   Reject, nie der Abwesend-Default. Vorher messen, wie die Ausschlusslogik in `tally.py` mit
   zwei Stimmen desselben Autors auf denselben Vorschlag umgeht — das entscheidet, ob der Lauf
   einen zweiten Träger braucht.
2. **Die Suche nach Text ohne Lauf.** Beschlüsse über Verifizierer- oder Auszählungsverhalten,
   deren D-Nummer in keinem Test und keinem Commit-Betreff vorkommt. D272 war der erste Fund
   dieser Art; ob es der einzige ist, weiß niemand.
3. **Die Gliederung von `pruefregeln.md`** ab Regel 37 (D249), zusammen mit den beiden
   Kandidaten für Regel 52.
4. **Der Föderations-Fork D234.** Dreiweg-Widerspruch zwischen `00 §7`, `04 §7.2` und `04 §3.1`
   zur Schlüsselauflösung, D235 vorgeschlagen und nicht abgeschlossen. Der größte ungelöste
   Strukturpunkt.

**Zur dritten Fassung:** sie ist möglich, aber der Anker hat sich bewegt. Nach D258 muss sie
denselben Spec-Stand lesen wie die Go-Fassung — das ist `1109b89` beziehungsweise die daraus
beschnittene Datei, **nicht** der jetzige. Wer gegen den reparierten Stand baut, misst die
Reparatur und nicht die Häufung. Beides ist zulässig, aber es sind zwei verschiedene Versuche, und
die Wahl gehört ins Register. Seit D268 ist sagbar, **was** sie bauen soll; seit D272 ist bekannt,
dass auch die Referenz Fehler dieser Art trägt.

## Offen

- **Der Codeteil von D274.** `04 §2.3` verlangt die Kanonizitätsprüfung von `v`, `tally.py` und
  `epoch.py` machen sie nicht. Benannter Rückstand, kein stiller.
- **Zwei Kandidaten für Prüfregel 52.** Erstens: wird eine Projektkopie aus einem gelieferten
  Diff rekonstruiert, geht ein `sha256sum -c` der **Quelldateien** als zweiter Job in den Block
  (aus `00af`). Zweitens: im Merge-Block steht `git push` vor `git branch -d` (aus `00ag`, dort
  einmal gebrochen).
- **Anhang C ist gegen Generatordrift nur teilweise gesichert.** Für C.1 gibt es
  `test_tv1_core_bytes_match_spec` mit getipptem Hex; für C.13 gibt es nichts, was den Spec-Text
  an `vectors_01.json` bindet. Ändert sich `gen.py`, wandert die Vektordatei mit und der Anhang
  veraltet still. Der billige Weg wäre ein Prüfer, der die Hexblöcke aus `01-claim-atom.md` liest
  und gegen die Vektordatei hält — beidseitig abgeleitet, nichts getippt. Gegen ihn spricht D233,
  wo eine zweite Prüfklasse mit Zahlen verworfen wurde. Nicht entschieden.
- **`cbor_canon.decode` ist tolerant und bleibt es.** Der Umschlag ist seit D272 streng, `v`
  wird an vier Stellen mit dem toleranten Dekoder gelesen; zwei davon prüfen `is_canonical` und
  fangen damit auch doppelte Keys und Restbytes, zwei nicht (das ist D274).
- **`tools/register_index.py` indiziert keine Anhangsverweise.** `01 §B.2` und `01 §C.10` fallen
  durch, obwohl `check_specs.py` sie prüft. Ein eigener Lauf, klein.
- **`FOREIGN_LIFECYCLE` hat keinen Vektor und kann keinen bekommen**, solange die Vektoren
  zustandslos gelesen werden (D263). Nach D268 liegt er als einziger Punkt außerhalb der
  selbstenthaltenen Gültigkeit.
- **Die Gliederung von `pruefregeln.md` ab Regel 37** (D249).
- **Wurzel-Markdowns tragen Backslashes**, obwohl die Anweisung keine vorsieht. Zuletzt sind
  siebzehn gezählt worden; seither sind Dateien hinzugekommen, die Zahl ist nicht nachgemessen.
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
Voraussetzung von `FOREIGN_LIFECYCLE` (D263). Die Feld-Konsistenz auf `core/*` (D264). Die
Gesamtordnung der Fehlerklassen (D265). Die Codes für Feldsatz-Verstöße und die Geltung der
Feldtabelle je Version (D266). Der zwölfte Reject-Code (D267). Der Umfang einer Fassung ohne
Speicher (D268). **Die Hex-Schnittstelle des Auftrags (D269). Die Arity der Eingabe (D270). Die
Lesart von Indefinite-Length und doppelten Keys (D271). Der Rückstand von D266 im Code (D272).
Die restlichen sechs Befundabschnitte (D273). Die Geltung der `v`-Kanonizität in der Auszählung
(D274).**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht.
