# Sitzungsstart: 00am (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, selbst gehostete Gitea-Instanz (`git.h.error13.de`). Das lokale
Arbeitsverzeichnis ist `~/mensch-als-republik`, daneben `~/mar-go` mit der unabhängigen
Zweitimplementierung von Layer 01 in Go — mit Remote, und **seit `00al` mit eingefrorener
Spec-Kopie und Textanker** unter `spec/STAND.md`.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 62, im
Volltext, mit stabilen Nummern, in elf Abschnitten entlang des Arbeitsbogens. Die Nummern stehen
darin **nicht** in Reihenfolge. Wer eine Regel sucht, sucht den Zeitpunkt, an dem sie greift.

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird. Seit D300 kennt der Index auch Anhangsverweise.

Was in `00al` am meisten getragen hat:

- **Die Projektkopie wird ausgepackt und gefahren.** Aus `/tmp/mar-context.xml` lässt sich der
  ganze Baum rekonstruieren — geschnitten am `file`-Tag, die Newline hinter dem öffnenden und vor
  dem schliessenden Tag gehören nicht zum Inhalt. `cbor2`, `cryptography`, `pytest` und
  `hypothesis` nachinstallieren, dann den Bestand fahren und die bekannte Testzahl reproduzieren:
  damit ist der Baum geeicht (Prüfregel 51). In `00al` hat er jede einzelne Abnahme getragen,
  dazu zwei Prototypen und den kompletten Kampagnenvergleich auf der Referenzseite.
  **Vorsicht bei Eigenschaften der Datei selbst:** das Auspackskript hängt jeder Datei eine
  Schluss-Newline an.
- **Der Blob-Hash aus dem Diff ist der Anker der Rekonstruktion.** `git hash-object` auf die
  nachgebaute Datei gegen die `index`-Zeile des Diffs. In `00al` fünfmal getroffen, viermal davon
  bei einer Abnahme; danach misst man die Fassung statt ihrer Beschreibung.
- **Golden Numbers gehören nicht in den Prompt**, sondern in die Abnahme. In `00al` haben sie
  viermal exakt getroffen und einmal eine Berichtigung ausgelöst.
- **Der Bericht ist nie die Abnahme, auch nicht der eigene** (Prüfregel 56).
- **Der Sitzungsstart ist eine Hypothese, keine Messung.** Prüfregel 27 gilt auch für diese Datei,
  und ebenso für jeden Posten ihrer offenen Liste (D301). In `00al` nannte sie den Stand vor ihrer
  eigenen Übergabe und einen Anker, der nirgends stand.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`,
  `ruff`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.

### Shell

- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und
  eine Pipe auf `tail`, `cat`, `tee` oder `grep -q` sind die nützlichen Ausnahmen.
- **Sichtbar und geprüft zugleich geht über `tee`.** `make check 2>&1 | tee /tmp/x.txt | tail -3`,
  danach `grep -q '^787 passed' /tmp/x.txt`. Eine Umleitung in eine Datei **und** eine Pipe gehen
  in fish nicht zugleich; `tee` löst beides.
- **`grep` ohne `-E` kennt kein `|` als Alternative.** **`grep -c` liefert bei null Treffern
  Status 1**; eine Zählzeile, die null ergeben *darf*, geht auf `| cat`.
- **`diff a b > datei` bricht die Kette**, weil `diff` bei Unterschieden Status 1 liefert.
- **Ein Glob ohne Treffer bricht die Kette**, auch vor einem `rm -f`. Fish meldet
  `No matches for wildcard` und führt den Job gar nicht erst aus; das `-f` schützt vor fehlenden
  Dateien, nicht vor einem leeren Muster. Zum Aufräumen deshalb
  `find /tmp -maxdepth 1 -name 'splice-*.py' -delete`, das bei null Treffern still bleibt. In
  `00al` hat es den Schlussblock der Sitzung gekostet.
- **Eine lange Ausgabe passt nicht in jedes Konsolenfenster.** In `00al` war eine Diagnoseliste
  nicht zurückzukopieren. Diagnoseskripte **aggregieren** deshalb und schreiben die volle Liste in
  eine Datei; ein `| cut -c1-150` am Aufruf verhindert zusätzlich den Umbruch.
- **`go` liegt nicht im `PATH`.** Die Toolchain steht unter `~/sdk/go/bin/go`.
- **Die Werkzeuge unter `tools/` laufen nur als Modul.** `python -m tools.gitter`, nicht
  `python tools/gitter.py`.
- **Im Merge-Block steht `git push` vor `git branch -d`** (Prüfregel 58).
- **Neue Dateien kommen nach dem Splice, nicht davor.** `splice_run.py` verlangt einen sauberen
  Arbeitsbaum und scheitert schon an einer unverfolgten Datei.
- **Mehrere Hashes prüft ein `printf` mit wiederholtem Format**, Ausgabe in `sha256sum -c`.
- **`set -l` und verschachtelte Kommandosubstitution gehören nicht in einen Copy-Block.**
- **Keine Ausgabe heisst: der Block ist nicht gelaufen.**
- **Jeder Block trägt Marken.** Vor jedem Abschnitt ein `echo "== NAME =="`, am Ende ein
  `echo "== FERTIG =="`.
- **`string`-Kommandos in einer `and`-Kette sind eine Falle.**
- **Kommandosubstitution in doppelten Anführungszeichen braucht `$`.**
- **Spec-Dateien, Prompts und Skripte als Download**, nicht als Copy-Block. **Eine Datei, die
  erzeugt und nicht ausgeliefert wurde, existiert für Oli nicht** — in `00al` einmal passiert,
  bei einer korrigierten Zweitfassung unter gleichem Namen. Der Hash-Test hätte es gefangen; der
  Zug war trotzdem verloren.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet`.
- **Prosa bricht bei 100 Zeichen; Tabellenzeilen und Codeblöcke sind ausgenommen** (D222). Für
  Python gibt es **keine** Zeilenlängenregel (D205). Diese Datei ist **nicht** ausgenommen.
  **Zeichen zählen, nicht Bytes.**
- **Eine Regex, die in einen Prompt oder eine Spec-Datei soll, geht nicht.** Regexänderungen
  werden in Prosa beauftragt.

### Die Zitiergrammatik — geschlossen

Seit D232 gibt es keinen offenen Teil. Vier Teile: der Dateiname mit oder ohne `.md`; die
Kurzform `NN`/`NNx` über `LAYER_FILES`; die Bereichsform `NAME §A–§B` (D228, kein Leerraum um den
Strich); die Anhangsnummer als Grossbuchstabe mit Punkt vor der Ziffernfolge (D230). Dazu die
Backtick-Toleranz (D231). Alles andere in `.py` ist ein Befund (D227); in `.md` bleibt der bare
Verweis zulässig.

**Ein Verweis auf einen Abschnitt derselben Datei braucht die Dateinamensform**, nicht die
Kurzform: `02b-abnahme §B.4`, nicht `02b §B.4` (D301).

**Prüfregel 47:** ein Verweis und ein Inline-Code-Span werden nicht über die Zeilengrenze
getrennt. In `00al` einmal beim Schreiben eines Registereintrags passiert und vor dem Splice
gefangen — `01 §2` am Zeilenende ist der typische Fall.

**Die Grenze, die bleibt:** die Prüfung sichert, dass das Ziel **existiert**, nicht dass es
**stimmt** (D229, D233). Daraus folgt D250: ein Anhang wird **angehängt, nicht eingeschoben**.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt. Eine **Ersetzung** ist eine Löschung
  plus eine Einfügung; nach Prüfregel 48 werden die randgleichen Zeilen abgezogen.
- **`grep -c '^+'` auf einen unified diff zählt die `+++`-Kopfzeile mit.** In `00al` war genau
  diese Eins der Beweis, dass ein Diff exakt einem benannten Commit entspricht.
- **Ein eigener Print-Separator ist keine Messung.** Eine Bindestrichlinie im Registerauszug kam
  in `00al` aus dem eigenen Skript und wäre beinahe als Trennerkonvention in einen Splice
  gewandert.
- **Aus einer Zeilennummer folgt kein Abschnitt.**
- **Zählvorschriften:** Registerköpfe `grep -c '^### D' 07-decisions.md`; Prüfregeln
  `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`; Branches `git branch -a | wc -l` — die Zahl
  schliesst `origin/main` und `origin/HEAD` ein, drei heisst also ein lokaler Branch.
- **Die Projektkopie wird nach jedem Push nachgezogen** (D224, Prüfregel 43), mit fünf Kaltzahlen
  im `--header-text`, Aufruf über
  `npx --yes repomix --header-text "..." -o /tmp/mar-context.xml`. **Das `-o` gehört dazu.** Der
  npm-Hinweis zeigt `argv` ungequotet; ob der Header in der Datei steht, sagt erst ein `grep`.
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position, **40**
  vor jeder Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung gegen den
  Prompt, **43** vor jeder Zahl aus der Kopie, **44** vor jeder abgeleiteten Anzahl, **46** vor
  jeder Zeilenangabe, **49** vor jeder Rücknahmeprobe, **50** vor jedem Kriterium aus einem
  Modell, **51** vor jedem Prüfer, der eine Menge misst, **53** vor jeder Mutantenkampagne, **59**
  vor jeder rekonstruierten Fassung, **60** vor jeder Meldung über eine Probe, **61** vor jeder
  Bewertung einer Abweichung zwischen zwei Fassungen, **62** vor jeder Probe, die eine Menge
  verkleinert. **28**: die Welt im Prompt ist Feld für Feld die gemessene Welt.

### Splices

Ein Splice ist ein Skript mit `assert`, dass der Anker genau einmal vorkommt. Gefahren mit
`.venv/bin/python tools/splice_run.py /tmp/splice-*.py` (D225). **Die Meldung `AssertionError`
gefolgt von `zweiter Lauf gescheitert` ist die Erfolgsmeldung.**

- **Das Skript liegt in `/tmp`.** `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Das Skript wird erzeugt, nicht getippt.** Der Anker wird aus der Zieldatei **gelesen**.
- **Ein Skript mit mehreren Paaren rechnet erst alles und schreibt dann.**
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42). In `00al` hat
  genau das gefehlt: ein Einschub mitten in einen Absatz hängte sich an eine Zeile mit 96 Zeichen
  und erzeugte 109. Der Einschubtext für sich war kurz genug. Der Harness fing es und setzte
  zurück. **Der belastbare Assert misst jede Zeile der neuen Fassung, die in der alten nicht
  vorkommt** — er ist damit automatisch so nachsichtig wie D222, weil Tabellenzeilen unverändert
  bleiben.
- **Ein Einschub in einen Fliesstext beginnt mit einem Zeilenumbruch**, nicht mit einem
  Leerzeichen, sonst wächst die Ankerzeile.
- **Das Anhängen an das Dateiende wird über `rstrip` normalisiert** und ist damit unabhängig davon,
  wie die Zieldatei endet; deshalb lässt sich der Zielhash vorher rechnen. Der Zweitlauf scheitert
  dann am `endswith`-Assert, nicht am Anker.
- **Ein Nachtrag an einen bestehenden Eintrag erhöht die Registerzahl nicht** — der Assert prüft
  vorher und nachher dieselbe Zahl.
- **Quellhash vor dem Schreiben, Zielhash nach dem Rechnen.**
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. Vor der Testzahl `.hypothesis` und `__pycache__`
löschen (Prüfregel 19). Prüfregel 40: der Kopf wird gemessen, nicht aus dieser Zeile abgeschrieben.

Nach `00al`: **787 Tests** plus Eigenschaftstests. Register **D1–D308**, Prüfregeln **1–62** in
elf Abschnitten. **Drei Branches**. Keine offenen Läufe. Der Stand ist `f63e54d`.

- **00** Nukleus, Genesis, Verfassung. `§7` nimmt die Föderationsstimme seit D235 aus.
- **01** Atom, Verifier, **zwölf Reject-Codes**, **sieben** Klassifikationszustände. `§3` trägt
  seit D270 den Arity-Satz. `§6` Punkt 4 führt seit D292 die drei `core/*`-Bedingungen einzeln.
  `§B.2` nennt seit D292 die Mängel, die `NON_CANONICAL_ENCODING` aufheben, **abschliessend**, und
  stellt die Wahl unter mehreren wahren Codes ausdrücklich frei. Der Absatz zur Feldtabelle je
  Version trägt **seit D308 zwei weitere Sätze**: unter fremder Version gilt kein Code, dessen
  Aussage eine Feldbedeutung aus `01 §2` voraussetzt, und die Ausnahme verlangt eine als uint
  lesbare `version`. Anhang C trägt **sechzehn** Abschnitte.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II. `§1.3` ist seit D276 die normative Form für jedes Lesen von `v`.
- **04** Governance. `§2.3` trägt seit D274 den Kanonizitätssatz, seit D276 die vier Lagen und
  seit D277 ihre Reihenfolge.
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py`, `tools/check_tree.py`,
  `tools/splice_run.py`, `tools/korpus.py`, `tools/verdikt.py`, `tools/gitter.py`, **neu
  `tools/paare.py`**.
- **Die Kampagne steht über beide Stufen.** `korpus.py` liefert Anhang C als **40** Hexzeilen.
  `gitter.py` liefert **2502** Einzelmutanten in drei Familien: 2438 in A und B, **64 in der
  neuen Familie C** (D303), die nicht-kanonisch kodiert und `NON_CANONICAL_ENCODING` erreicht.
  Damit sind **elf der zwölf Codes** über das Gitter erreichbar; nur `FOREIGN_LIFECYCLE` nicht.
  `paare.py` liefert **16958** Paarmutanten der Stufe 2 (D305, D306): 85 in der Vorrangprobe,
  2059 in Klasse eins, 4378 in Klasse zwei, 10436 in Klasse drei.
- **Go-Fassung**: `~/mar-go`, `main` bei `4ec54cd`, Remote unter `git.h.error13.de/oli/mar-go`.
  Die Spec-Kopie liegt auf dem eingefrorenen Anker `79b73a2` und nennt ihn in `spec/STAND.md`
  samt Blob-Hash (D302). **Sie trägt den D308-Satz absichtlich nicht.** Gebaut mit
  `~/sdk/go/bin/go build -o /tmp/margo .`, gefahren über stdin.

### Was `00al` entschieden hat

- **D302** — der Anker der Zweitfassung wird als Text verkörpert, nicht nur als Dateiinhalt.
- **D303** — Familie C: nicht-kanonische Kodierung auf der unveränderten Saat, fünf Operatoren,
  keine Kombination mit Inhaltsmutationen.
- **D304** — Abnahme der Familie C; Prüfregel 62.
- **D305** — der Zuschnitt der Stufe 2 folgt der Aussagekraft: Klassen eins bis drei vollständig,
  Klasse vier ersetzt durch eine benannte Vorrangprobe, Tripel zurückgestellt.
- **D306** — Berichtigung von D305: die Zahlen zu Klasse zwei und vier waren falsch gezählt; die
  Vorrangprobe erwartet einen abgeleiteten Code; doppelte Drahtfolgen werden verworfen.
- **D307** — Abnahme der Stufe 2; die Deduplikation lässt die Klassenzuordnung wohldefiniert.
- **D308** — Ergebnis der Kampagne und zwei Spec-Lücken; mit zwei Nachträgen.

## Was `00al` gelehrt hat

**Der Ertrag einer Zweitfassung liegt nicht in ihren Fehlern.** Über 2502 Einzel- und 16958
Paarmutanten gab es **null Abweichungen auf Stufe eins** und 512 auf Stufe zwei, jede davon ein
Nichtbefund unter `01 §B.2`. Gefunden wurden trotzdem zwei Lücken — beide dort, wo beide Fassungen
**übereinstimmen** und der Text es nicht verlangt. Das ist Prüfregel 61 in der Gegenrichtung, und
es ist der eigentliche Grund, zwei Fassungen zu vergleichen: eine Übereinstimmung ohne normative
Grundlage ist die Stelle, an der eine dritte Fassung auseinanderläuft.

**Die Nullprobe zur eigenen Reparatur fand den zweiten Fund.** Der Satz, der D308 schliessen
sollte, wurde gegen die Referenz geprüft, und 176 Mutanten schienen ihn zu widerlegen. Sie taten
es nicht — sie zeigten die fehlende Bedingung. Ohne diese Probe wäre eine halbe Norm im Text
gelandet.

**Die eigene Klassifikation veraltet zwischen zwei Messungen.** Eine Zahl aus der ersten Messung
(16943) war richtig; die zweite Messung schnitt anders und lieferte 39964, und beide standen
nebeneinander im selben Registereintrag. Das Werkzeug fand es. **Zwei Messungen desselben
Gegenstands gehören gegeneinander gehalten, bevor die zweite eine Entscheidung trägt.**

**Der Stopp des Werkzeugs war der wertvollste Zug der Sitzung.** Es meldete drei Widersprüche
zwischen Prompt, Register und Messung, statt einen davon aufzulösen. Zwei waren Fehler des
Supervisors. Ein Prompt, der das Melden ausdrücklich verlangt, bekommt es auch.

**Nach zwei Anläufen am selben Symptom wird die Schicht gewechselt.** Sechs Zeilen, in denen die
Zweitfassung anders wählte, waren nach `01 §B.2` unter keinen Umständen ein Befund. Der dritte
Anlauf wäre der Kreisel gewesen; der Schichtwechsel führte auf die Versionsfrage und damit auf
den Fund.

**Ein Assert, der den Einschub misst, misst nicht das Ergebnis.** Prüfregel 42 in ihrer teuersten
Form: der Text war kurz genug, die entstehende Zeile nicht.

## Der nächste Schritt

Die Kampagne hat ihren Zweck erfüllt, und weitere Mutanten liefern abnehmenden Ertrag — das ist
die Warnung aus D298, inzwischen zweimal bestätigt. Vorschlag in dieser Reihenfolge:

1. **Die drei kleinen Rückstände aus `00al` in einem Lauf.** Ein Test, der in
   `tests/test_paare.py` die Klassenzuordnung an die Einzelverdikte bindet; die fünf privaten
   Namen in `tools/gitter.py` öffnen, die `tools/paare.py` importiert; der Operator
   `feldkopf_breiter` mit dem Schritt von Additional Information 26 auf 27, was `t` und `t_exp`
   erreichbar macht. Alle drei sind benannt, klein und unabhängig voneinander.
2. **Danach die Frage, ob eine dritte Fassung mehr trägt als eine dritte Mutantenstufe.** D308
   liefert das Argument dafür: die Lücken lagen dort, wo zwei Fassungen sich einig waren. Eine
   dritte Fassung gegen den **präzisierten** Text wäre die Probe darauf, ob die Präzisierung
   reicht. Der Anker aus D302 steht bereit.
3. **Tripel bleiben zurückgestellt** (D305 Beschluss 4), solange Stufe 2 keinen Befund erzeugt hat.

## Offen

**In `00al` gemessen:**

- **`tools/paare.py` importiert fünf private Namen aus `tools/gitter.py`** — `_SEED_NAMES`,
  `_SIG_KEY`, `_author_sk`, `_clone`, `_sign_a`. Angenommen mit Begründung (D307): der Bruch wäre
  laut, und die Gegenmassnahme berührte die Datei, deren Unberührtheit das Abnahmekriterium war.
- **Kein Test bindet die Klassenzuordnung in `tests/test_paare.py`.** Extern für alle 16873
  Klassenzeilen nachgerechnet, keine Abweichung (D307).
- **`feldkopf_breiter` greift nicht auf `t` und `t_exp`**, weil beide Additional Information 26
  tragen und der Operator dort aussetzt. Der Schritt 26 auf 27 ergäbe zwölf weitere Zeilen (D304).
- **3490 der 16958 Paarmutanten tragen eine fremde Version** und messen im Wesentlichen nur die
  Versionsprüfung (D308).
- **Sechs Zeilen mit wahrer Expiry-Inkohärenz** wählt die Zweitfassung anders als die übrigen 288.
  Beide Codes sind wahr, `01 §B.2` stellt frei; ungeklärt bleibt, woran der Unterschied hängt.
- **Die Werkzeuge unter `tools/` sind über den Dateipfad nicht aufrufbar**, nur als Modul.
- **`test_b2_list_is_derived_from_register_text` leitet über eine Zeichenfolge ab**, nicht über
  die Grammatik (D300).
- **`FOREIGN_LIFECYCLE` ist auch vom Gitter unerreichbar**, weil es einen Speicher braucht (D268).

**Weiterhin offen, in `00al` nicht neu gemessen:**

- **Anhang C ist gegen Generatordrift nur teilweise gesichert.** Für C.1 gibt es
  `test_tv1_core_bytes_match_spec` mit getipptem Hex; für C.13 bis C.15 gibt es nichts, was den
  Spec-Text an `vectors_01.json` bindet. Gegen einen Prüfer spricht D233. **Die andere Achse ist
  seit D295 geschlossen**: Datei gegen Generator.
- **`UNPARSABLE_V` entsteht bei `ratify@1` nicht.** Benannter Rückstand aus D276.
- **`cbor_canon.decode` ist tolerant und bleibt es.**
- **`FOREIGN_LIFECYCLE` hat keinen Vektor und kann keinen bekommen** (D263, D268).
- **`EPOCH_FORK` hat keinen Produktivträger** (D138, D176, bestätigt in D281).
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173).
- **Zwei Registerverweise zeigen ins Leere**, `03 §5.1` und `03 §11`. Bewusst nicht nachgezogen.
- **Die `einlesen-a-*`-Dateien behaupten, NV2 trage keine Drahtbytes.** Seit D291 falsch, bewusst
  nicht nachgezogen.
- **Ob `tests/profiles/test_credit.py` die einzige Python-Datei ohne Schluss-Newline ist, lässt
  sich aus der Projektkopie nicht messen.**
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
Die zweite Prüfklasse für Verweisrichtigkeit (D233). Der Föderations-Fork (D234, D235, D236). Die
Zuordnung von Pflichten über Stichworte (D242). Die MUSS-Extraktion (D246). Die Wahl Vektor statt
Sondierwelt für `01 §5.3` (D250). Der Lookahead in der nuc-Regex (D255). Reihenfolge und Umfang
der Zweitimplementierung (D256, D258, D259). Die Abdeckung des Fehlerkanals durch Anhang C (D257).
Der Vergleichsgegenstand der Kanonizitätsprüfung (D261). Der Vorrang der Fehlerklassen (D262,
D265, D292, D299). Der Code für den falschen `J.tag` auf `core/*` (D263). Die Feld-Konsistenz auf
`core/*` (D264). Die Codes für Feldsatz-Verstösse (D266). Der zwölfte Reject-Code (D267). Der
Umfang einer Fassung ohne Speicher (D268). Die Hex-Schnittstelle (D269). Die Arity der Eingabe
(D270). Indefinite-Length und doppelte Keys (D271). Der Rückstand von D266 im Code (D272). Die
restlichen sechs Befundabschnitte (D273). Die `v`-Kanonizität in der Auszählung (D274). Ort und
Verdrängung von `NON_CANONICAL_V` (D275). Die vier Lagen und `UNPARSABLE_V` (D276, D277). Der
Träger für `superseded` (D278). Die Bindung der Reject-Codewerte (D279). Die Vektoren für die
Feldtabelle (D280). Die Vermerkskampagne (D281). Die Prüfregeln 52 bis 59 (D282). Die überlebenden
Erzeugerstellen (D283, D284, D285). Die Zustandsmatrix (D286). Die zehn Doppelerzeuger (D287). Die
Gliederung (D288). Die Bauform der Mutation (D289). Der Anker der Kampagne (D290). Der zweite
Mangel in NV2 (D291). Die Vorrangliste und `§6` Punkt 4 (D292). Ort und Schnitt der Kampagne
(D293). Der Nachzug der Go-Fassung (D294). Die Bindung der Vektordatei (D295). Prüfregel 60
(D296). Die Operatorenmenge (D297, D298). Der erste Kampagnenlauf (D299). Die Anhangsverweise im
Index (D300). Der Kleinkram (D301). **Die Textform des Ankers (D302). Familie C und ihre Abnahme
(D303, D304). Der Zuschnitt der Stufe 2 und seine Berichtigung (D305, D306). Die Abnahme der
Stufe 2 (D307). Das Kampagnenergebnis und die Versionsausnahme (D308).**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht.
