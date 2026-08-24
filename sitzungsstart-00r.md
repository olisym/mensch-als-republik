# Sitzungsstart: 00r (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 39, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu sind **37** (die Basis eines Laufs ist der Commit, der den Prompt enthält, D208),
**38** (eine Position wird erst bezogen, nachdem der zuständige Abschnitt aufgeschlagen ist, D209)
und **39** (eine Ausgabe ist keine Bedingung, D211).

**Neu und sofort nutzbar: `python3 tools/register_index.py "04 §4.1"`** nennt die
Registereinträge, die einen Abschnitt entschieden haben. Ohne Argument eine Übersicht, welche
Abschnitte wie oft entschieden wurden. Das ist Prüfregel 38 in ausführbarer Form und der billigste
erste Griff, bevor eine Position bezogen wird. Grenze: 40 Prozent der Einträge nennen keinen
Abschnitt und tauchen nicht auf.

Was in dieser Sitzung am meisten getragen hat:

- **Nachschlagen, bevor die Position steht.** Vier Positionen bezogen, drei zurückgenommen — jede
  gegen eine Entscheidung, die es schon gab. Prüfregel 27 und 33 greifen erst beim Prompt; die
  Rücknahmen fielen davor an. Genau dafür gibt es jetzt Regel 38 und den Registerindex.
- **Der Bericht des Werkzeugs ist nie die Abnahme — aber seine Weigerung kann die beste Meldung
  sein.** In `00r` hat das Werkzeug einen Widerspruch im Prompt gefunden, ihn benannt und **nicht**
  aufgelöst. Das war richtig und hat einen Fehler des Supervisors sichtbar gemacht.
- **Der eigene Baum muss auf dem Commit stehen, über den geredet wird.** Der Supervisor hat 672
  Verweise „gemessen an `65ab37d`" gemeldet und an einer älteren Kopie gemessen. Richtig waren 704.
  Prüfregel 19, in neuer Kleidung.
- **Messen, was der Fall ist, nicht was plausibel klingt.** Der Verdacht „die Schichten sind zu
  verzahnt" hielt der Messung nicht stand: 74 Importkanten nach unten, 6 zurück, davon fünf aus
  der Fassade. Die Schichten stapeln.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`, `ruff`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und
  eine Pipe auf `tail` sind die nützlichen Ausnahmen. **Und nach Regel 39: eine Zeile, die nur
  ausgibt, sichert nichts.** `test (git branch --show-current) = main` statt der blossen Ausgabe.
- **Spec-Dateien und Splice-Skripte als Download**, nicht als Copy-Block. Werkzeug-Prompts als
  Datei, wenn sie lang sind.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet -- <datei>` — aber nur
  für Dateien, die unverändert sein **müssen**. Steht ein Splice noch ungesichert im Baum, wird
  seine Datei von dieser Prüfung ausgenommen.
- Bei neuen Dateien `git add` **vor** `make check`. Explizite Pfade, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. Zeilen brechen bei 100 Zeichen — das gilt für
  **Spec-Dateien und Prompt-Dateien im Wurzelverzeichnis**, ist aber **ungeprüft**; es hält nur,
  weil jeder Splice es selbst assertet. Für Python gibt es **keine** Zeilenlängenregel; D205 hat
  das mit Zahlen entschieden und nicht wieder aufzumachen.
- **Neu: wer über einen kaputten Verweis schreibt, nennt seine Nummer ohne Paragraphenzeichen**
  (D210). „Der Unterabschnitt 6.7 von `01 §6`" statt der Zitierform. Sonst meldet die
  Verweisprüfung die Erwähnung als Verwendung. Ausgenommen sind nur `07-decisions.md` und
  `sitzungsstart-*.md` — diese Datei darf also frei zitieren.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Zählvorschriften, die tragen:**
  - Registerköpfe: `grep -c '^### D' 07-decisions.md`.
  - Prüfregeln: `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`.
  - Branches: `git branch -a | wc -l`.
  - Abschnitte je Datei: `grep -n '^## ' <datei>`.
- **Der eigene Baum ist die stärkste Messung** — aber nur, wenn er auf dem Commit steht, über den
  geredet wird. Die Projektkopie gegen ein Manifest aus allen Dateien halten, dann `pip install
  cbor2 cryptography pytest hypothesis ruff`, dann läuft die volle Reihe. Jede Rotmenge, jeder
  Weltzustand und jede Variante lässt sich vorher fahren. Das kostet den Operator keinen Zug.
  **Wächst `main` während der Sitzung, wächst die Kopie nicht mit.** Jede Zahl, die danach an
  einen Commit geheftet wird, ist neu zu messen.
- **Varianten baut man, man schätzt sie nicht.** In dieser Sitzung wurden drei Formvarianten
  vollständig gebaut und gemessen. Die Rotmenge war bei allen dieselbe — entschieden hat, was beim
  Bauen auffiel: eine Variante hätte einen `TypeError` in den Produktivpfad gelegt, den die volle
  Reihe nicht sieht.
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position.
- **Prüfregel 28**: die Welt im Prompt ist Feld für Feld die gemessene Welt.

### Splices

Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher trocken gegen eine
Kopie gelaufen. Diese Sitzung hat sieben Splice-Läufe gefahren, alle sauber.

- **Jeder Splice läuft trocken gegen den Stand nach dem vorigen**, nicht gegen die Projektkopie.
  Steht die Kopie hinter `main`, werden die fehlenden Splices zuerst auf eine Arbeitsdatei
  angewandt und der neue darauf.
- **Ein zweiter Lauf desselben Skripts muss scheitern.** Siebenmal gehalten.
- **Nur die neuen Zeilen auf Länge prüfen, nicht die ganze Datei.** Der Altbestand führt Zeilen
  über 100 Zeichen. **Tabellenzeilen nicht ausnehmen** — wer sie ausnimmt, umgeht die Regel statt
  die Tabelle zu kürzen.
- **Blöcke werden ersetzt, nicht Teilstrings geflickt.**
- **Ein Splice, der zwei Dateien anfasst, gehört geteilt, wenn die Dateien zu verschiedenen
  Commits gehören.** In `00r` musste die Prompt-Berichtigung in den Lauf-Commit und der
  Registereintrag danach; das eine Skript war dafür falsch geschnitten.
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`.

Zum Ende dieser Sitzung: `main` bei `d9db6fc`, gepusht. **589 Tests**. Register **D1–D211**,
Prüfregeln **1–39**. **Drei Branches** (`main`, `origin/HEAD`, `origin/main`). Keine offenen Läufe.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`. **Neu: `§10`
  nennt die sechs Vermerke mit ihren Subjekten** (D173).
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`. **`§2.4.4`
  führt seit D207 fünf Lagen statt vier.**
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung, `§3.5` mit der Subjektregel
  (D198), `§4.1` mit Bedingung 6 (D200) und seit D207 mit der dritten Lage, `§4.5` mit der
  berichtigten Vermerksgrenze (D203).
- **Fassade** (`mensch_als_republik/resolve.py`): `resolve_state` und `NucleusState`.
- **Kettenbauer** (`tests/kettenwelt.py`), **Werkzeugschicht** (`werkzeuge.md`).
- **Linter**: `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py` (neu, D209), `tools/check_specs.py` prüft seit D209
  auch Abschnittsverweise, `tools/check_tree.py`.

**Neu in dieser Sitzung:** D207 bis D211, zwei Läufe (`00q`, `00r`), Prüfregeln 37 bis 39,
`02 §10`, die dritte Lage in `04 §4.1` und die vierte in `03 §2.4.4`,
`tests/profiles/test_vermerk_subjekte.py`, zwei Prüffälle, `tools/register_index.py`, die
Verweisprüfung.

- **D207** — Die Vermerkslage ohne eigene Adresse. Drei Formvarianten gebaut und verworfen
  (`subject` optional, Rollenfeld, eigene `kind`); der gemeldete Rollenwechsel war keiner, weil das
  defekte Objekt jeweils ein **Feld** ist und Felder keine eigene Adresse haben. D198 ist
  vollständig. Was fehlte, waren zwei Tabellenzeilen.
- **D208** — Abnahme `00q`, kein Defekt im Lauf; die Basis im Prompt war falsch gesetzt. Daraus
  Prüfregel 37.
- **D209** — Registerindex und Verweisprüfung. Die Diagnose ist gemessen: der Code stapelt, die
  Spec ist konsistent, das Register wächst. Daraus Prüfregel 38.
- **D210** — Die Verweisprüfung unterscheidet Erwähnung nicht von Verwendung. Beispiele werden
  umgeschrieben, keine Abschaltmarke gebaut. Berichtigt drei Zahlen aus D209.
- **D211** — Abnahme `00r`, kein Defekt im Werkzeugcode; der Lauf landete auf `main`, weil eine
  Branchausgabe als Prüfung galt. Daraus Prüfregel 39.

## Was diese Sitzung gelehrt hat

**Die Spec hat dreimal schon geantwortet.** `04 §4.1` hatte die Sammelform mit Kriterium
entschieden, `03 §2.4.4` die Zusammenfassung zweier Lagen begründet, `04a §6` die feinere
Aufschlüsselung ausdrücklich zurückgestellt. Alle drei wurden erst gefunden, nachdem eine Position
schon stand. Das ist der teuerste Fehler dieser Sitzung, dreimal wiederholt.

**Literatur trägt, wenn man die Primärquelle liest.** Der erste Griff war ein Issue-Tracker-Eintrag,
der ein `missing.key`-Feld als Spec-Text ausgab; die JSON:API-Spec kennt es nicht. Erst SARIF
`§3.27.12` und `§3.27.13` in der OASIS-Fassung gaben belastbare Präzedenz — und zugleich den Grund,
sie **nicht** zu übernehmen, weil ein Content-Hash kein Dokumentzeiger ist.

**Eine Variante entscheidet sich beim Bauen, nicht an der Rotmenge.** Drei Varianten, dieselbe
Rotmenge von einem Test. Entschieden hat, dass eine davon `dedupe_sort` zwingt und ohne diesen
Eingriff einen `TypeError` in den Produktivpfad legt, den 587 grüne Tests nicht sehen.

**Eine Prüfung, die Text prüft, trifft den Text, der über sie spricht.** Der `00r`-Prompt
beschrieb kaputte Verweise und wurde von seiner eigenen Prüfung gemeldet. Das ist keine
Kuriosität, sondern die Regel für jede Selbstbeschreibung; die Antwort war, die Beispiele zu
entschärfen statt ein Schlupfloch zu bauen.

**Was das Werkzeug meldet und nicht baut, ist mehr wert als ein sauberer Commit.** `00r` kam
ungebaut zurück, mit einer präzisen Widerspruchsanzeige. Hätte das Werkzeug den Widerspruch selbst
aufgelöst, wäre der Prompt-Defekt unbemerkt geblieben.

## Der nächste Schritt

**D173 zu Ende bringen.** Der Abdeckungsteil ist erledigt, `02 §10` steht. Es fehlen zwei Orte:

- **`03 §6.1`** führt eine Vermerkstabelle mit vierzehn Arten **ohne Subjektspalte**. Die
  allgemeine Regel steht in `§6` und trägt einen Textdefekt: `CONSTITUTION_UNAVAILABLE` ist dort
  in derselben Aufzählung **zweimal** genannt, eine der Nennungen sollte etwas anderes sein.
- **`00 §5.4`** nennt den Subjekttyp für `MALFORMED_NUCLEUS_KEY`, nicht für
  `CONSTITUTION_UNAVAILABLE`. Eine von zwei Arten gedeckt.

Beides zusammen ist ein Splice und ein Commit, kein Werkzeuglauf — sofern der Textdefekt in `§6`
sich aus dem Code auflösen lässt. Zuerst messen, welche Art dort gemeint war.

**Der billige Nachzug daneben:** `is_nuc_predicate` und `is_core_predicate` fangen
`VerifierError`, `is_nuc_name` fängt `Exception` (D181). Drei Funktionen nebeneinander, zwei
Fangbreiten. Messbar — welche Ausnahmen können dort überhaupt austreten — und danach eine
Entscheidung, kein Ermessen.

## Offen

- **`03 §6.1` ohne Subjektspalte und der Doppeleintrag in `03 §6`** (D173). Erster Punkt.
- **`00 §5.4` deckt eine von zwei Vermerksarten** (D173).
- **Die Zitierkonvention ist nicht injektiv** (D209). `03` und `04` bezeichnen je vier Dateien,
  `01a` zwei. Verweise mit Buchstabenpräfix sind deshalb **ungeprüft**. Wer sie prüfen will,
  braucht zuerst eine Entscheidung, welche Datei welchen Zitiernamen führt.
- **Die Verweisprüfung kann Listenpunkte nicht von Unterabschnitten unterscheiden** (D209).
  `01 §6.7` war inhaltlich richtig gemeint und trotzdem ein Befund.
- **Zwei Registerverweise zeigen ins Leere**, `03 §5.1` und `03 §11`. Bewusst nicht nachgezogen:
  das Register beschreibt vergangene Stände.
- **`VISION` in `register_index.py`** stand in keinem Auftrag (D211). Inhaltlich richtig, weil das
  Register `VISION §…` dreimal nennt; bleibt stehen.
- **Die 100-Zeichen-Regel ist ungeprüft.** Sie hält nur, weil jeder Splice sie selbst assertet.
  Eine Prüfung dafür ist ein eigener Fork und nicht aufgemacht.
- **`is_nuc_predicate`/`is_core_predicate` fangen `VerifierError`, `is_nuc_name` fängt
  `Exception`** (D181).
- **Wie weit die Regierbarkeitsprüfung reicht** (D200). Zurückgestellt, bis ein Fall sie erzwingt
  — **nicht vorher aufmachen**.
- **`RATIFY_WITH_EXPIRY` und der Zeugenpfad tragen die Weitergaberegel ungeprüft** (D203).
- **Vergleiche gegen `dedupe_sort` sind für die Reihenfolge zirkulär** (D196).
- **Vier `Finding`-Klassen, drei `dedupe_sort`** (D183, Zählung mit D207 berichtigt): das vierte
  gehört `PolicyNote` in `policy.py`, einer fünften Vermerksfamilie mit anderer Feldform, deren
  Trennung `03 §1.2` begründet. Nicht anfassen, ohne die Frage zu stellen, ob die Enums je
  zusammengeführt werden.
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173).
- **Die Sondierwelt in `test_benennung.py` erzeugt keine Vermerke** (D173).
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
- **`example-nucleus.md`** weiterhin unvollständig, aber `§5.1` steht seit D202.
- **Braucht der Node eine eigene Beschreibung?** D180 sagt ausdrücklich nein.
- **Layer 05.** Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf), die Beta-Reputation
  mit dem Moral-Licensing-Problem — und seit D178 die Frage, ob wiederholtes Stimmen auf
  unveröffentlichte Vorschläge eine Folge tragen soll.

**Erledigt und nicht wieder aufzumachen:** die Zeilenlängenfrage für Python ist mit D205 verneint.
Die Frage nach einer dritten `ruff`-Gruppe ist mit `ARG` beantwortet. Der Fork aus D197 ist mit
D200 entschieden. Die Formfrage für `Finding.subject` ist mit D207 entschieden, mit drei gebauten
Varianten; wer sie wieder aufmacht, braucht einen Fall, den D207 nicht gemessen hat. Ein
Übersichtsdokument über die Schichten ist mit D209 verworfen — der Importgraph ist aus dem Code
in Sekunden zu rechnen.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.
