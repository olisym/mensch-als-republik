# Sitzungsstart: 00z (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`). Das
lokale Arbeitsverzeichnis ist `~/mensch-als-republik`.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 45, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu sind **44** (abgeleitete Zahlen werden gerechnet, nicht aus der eigenen Tabelle
nachgezählt, D229) und **45** (eine Probe darf den Produktivcode nicht formen, D229).

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird. Der Index findet nur **qualifizierte** Namen — seit D227 sind das in
Python alle.

Was in der letzten Sitzung am meisten getragen hat:

- **Die Auflösung vollständig belegen, bevor der Prompt entsteht.** Vier Tranchen, 73 Stellen,
  jede einzeln gegen die Zieldatei geöffnet. Kein Ziel wurde geraten, und keine Abnahme brachte
  eine Überraschung. Das kostet den Operator keinen Zug: die Projektkopie trägt es.
- **Eine Verzeichnisheuristik hätte an vier Stellen falsch gebunden.** `graph.py` meint mit der
  Nummer 4 den Solver in `02a`, `derive.py` den Fluss in `02`. Dieselbe Nummer, dasselbe
  Verzeichnis, verschiedene Ziele. Das ist der Beleg, warum D227 so entschieden hat.
- **Der Fork, den man beim Prompt-Schreiben bemerkt, ist ein Registereintrag.** Die Bereichsform
  fiel beim Vorbereiten von Tranche C auf und wurde zu D228, statt nebenbei entschieden zu
  werden.
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
- **Kommandosubstitution in doppelten Anführungszeichen braucht `$`** — fish liest `"(cmd)"`
  wörtlich, `"$(cmd)"` führt aus. In `00y` einmal gerissen, der Header der Projektkopie trug
  darauf den Klammerausdruck statt des Commits.
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
  ohne Paragraphenzeichen genannt. Das ist in `00y` einmal passiert und beim Trockenlauf
  gefangen worden. Ausgenommen sind `07-decisions.md` und `sitzungsstart-*.md` — diese Datei darf
  frei zitieren, aber **nicht** von der Zeilenlänge.

### Die Zitiergrammatik — geschlossen

Seit D229 gibt es in Python keinen ungeprüften Paragraphenverweis mehr. Die Grammatik hat drei
Bestandteile und keine vierte Klasse:

1. **Der Dateiname**, mit oder ohne `.md` — `02a-maxflow-prompt.md §2.7`. Injektiv von selbst,
   ohne Tabelleneintrag.
2. **Die Kurzform** `NN` und `NNx` über `LAYER_FILES`. Dreizehn Einträge, **geschlossen**. Wer
   einen vierzehnten braucht, hat Form 1 übersehen.
3. **Die Bereichsform** `NAME §A–§B` (D228). Bindet beide Nummern an denselben Namen.
   Halbgeviertstrich und Bindestrich sind zulässig, Leerraum um den Strich **nicht** — dann
   fällt die zweite Nummer als barer Verweis auf, und das ist gewollt.

Alles andere in `.py` ist ein Befund (D227). Ein Kurzform-Name ohne Tabelleneintrag ist ein
Befund (D219); ein fehlender **Dateistamm** ist keiner (D221).

**Die Grenze, die bleibt:** die Prüfung sichert, dass das Ziel **existiert**, nicht dass es
**stimmt**. Ein Verweis auf einen vorhandenen, aber sachlich falschen Abschnitt bleibt grün.
Deshalb ist bei Qualifizierungsläufen der Diff die Abnahme und nicht die grüne Zeile.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt. Auch die Zeilenzahl eines Einschubs,
  den man selbst geschrieben hat, wird gerechnet und nicht nachgezählt (Prüfregel 44).
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
  lassen sich aus dem Archiv nicht exakt rekonstruieren. In `00y` erzeugte das sechs Scheinbefunde
  beim Hash-Abgleich. Wer die Kopie gegen `main` prüft, prüft mit `sha256sum -c` je Datei, nicht
  über einen Aggregat-Hash — ein Gesamthash kann eine Teilhypothese nicht widerlegen.
- **Verworfen für die Kopie:** `--compress`, `--remove-comments`, `--remove-empty-lines`,
  `--output-show-line-numbers`, `--no-file-summary`. Begründungen in D224; nicht wieder aufmachen.
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position,
  **40** vor jeder Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung,
  **43** vor jeder Zahl aus der Kopie, **44** vor jeder abgeleiteten Anzahl.
- **Prüfregel 28**: die Welt im Prompt ist Feld für Feld die gemessene Welt.

### Splices

Ein Splice ist ein Skript mit `assert`, dass der Anker genau einmal vorkommt. Gefahren wird er mit
`python3 tools/splice_run.py /tmp/splice-dNNN.py` (D225). Der Harness verlangt einen sauberen
Baum, erzwingt das Scheitern des zweiten Laufs, prüft die Zeilenlänge am Ergebnis und setzt bei
jedem Fehlschlag zurück.

- **Das Skript liegt in `/tmp`, nicht im Wurzelverzeichnis** — sonst meldet der Harness den Baum
  als unsauber. `ROOT = Path.cwd()`, nicht `Path(__file__).parent`.
- **Ein zweiter Lauf desselben Skripts muss scheitern.**
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42).
- **Tabellenzeilen sind von der 100-Zeichen-Grenze ausgenommen** (D222).
- **Dreifache Anführungszeichen im Einschubtext beenden den Python-String.** Wer einen Docstring
  zitiert, schreibt ihn ohne die Anführungszeichen — Escapes wären in einer Spec-Datei ein
  eigener Befund.
- **Was der Harness nicht fängt** (D226): einen Splice, der eine zu lange Zeile entfernt und eine
  andere einsetzt, und eine unversionierte Datei, die ein gescheiterter Splice angelegt hat.
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`.

**Der Kopf ist nicht `aaec761`.** Das ist der Stand nach D229; der Übergabe-Commit dieser Datei
liegt darüber. Prüfregel 40 — der Kopf wird gemessen, nicht aus dieser Zeile abgeschrieben.

**597 Tests.** Register **D1–D229**, Prüfregeln **1–45**. **Drei Branches** (`main`,
`origin/HEAD`, `origin/main`). Keine offenen Läufe.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
  `§10` nennt beide Vermerke mit ihren Subjekten (D212).
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A.
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
  bare Verweise seit D227), `tools/check_tree.py`, `tools/splice_run.py`.

**Neu in der letzten Sitzung:** D227 bis D229, vier Läufe (Tranchen A bis D), Prüfregeln 44 und
45, die geschlossene Zitiergrammatik.

- **D227** — Bare Paragraphenverweise in Python sind unzulässig. Gemessen: Lesart 1 (Fortsetzung
  im Modulkontext) trug 41 von 73 und band an 6 Stellen falsch, Lesart 2 (Paketverzeichnis) trug
  33 und band an 9 falsch. Verworfen: beide, dazu ein Mapping von Modulthema auf Schicht.
  Berichtigt: die Anhangs-Zielform gehört **nicht** zu Frage 2.
- **D228** — Die Bereichsform bindet beide Nummern an denselben Namen. Verworfen: den Namen
  wiederholen, Bereiche verbieten, den Trennstrich vereinheitlichen.
- **D229** — Die Grammatik ist geschlossen. 121 Dateien, 260 geprüfte Verweise, null bare.
  Entschieden: **kein** eigener Test für `tools/`, weil der bare Befund die Bereichsregel mit
  abdeckt. Benannt: die Prüfung sichert Existenz, nicht Richtigkeit.

## Was die letzte Sitzung gelehrt hat

**Ein Aggregat-Hash kann eine Teilhypothese nicht widerlegen.** Die Vermutung, fünf leere
`__init__.py` erklärten die Abweichung der Projektkopie, wurde gegen einen Gesamthash geprüft, bekam
einen dritten Wert und galt als widerlegt. Sie war richtig — eine sechste Datei wich zusätzlich ab.
Der zu grobe Test hat eine korrekte Aussage verworfen.

**Zwei falsche Dateizahlen in einem Prompt, beide vom Supervisor.** Die Messung lag vor, gezählt
wurde aus der eigenen Tabelle. Das Werkzeug hat beide gemeldet und die Tabelle umgesetzt. Daraus
Prüfregel 44.

**Eine Probe hat Produktivcode erzeugt.** Weil die Rücknahmeprobe eine Regex-Gruppe entfernte,
kam eine Abfrage auf die Gruppenzahl hinzu, die im Produktivpfad konstant wahr war. Die Probe war
falsch konstruiert, nicht der Code unvollständig. Daraus Prüfregel 45.

**„Vollständig gelesen“ ist eine Behauptung wie jede andere.** Der Sitzungsstart `00y` wurde zu
92 Prozent gelesen und als vollständig gemeldet; der Schlussteil mit der offenen Liste fehlte.
Prüfregel 1 gilt auch für die eigene Lektüre: Zeilenzahl messen, dann behaupten.

## Der nächste Schritt

**Die Anhangsform der Zitiergrammatik.** Sie ist der letzte offene Teil und wurde zweimal
verschoben: D221 hat sie zu Frage 2 geschoben, D227 hat berichtigt, dass sie dort nicht hingehört.

Gemessen auf `b49358e` — **die Zahl ist zu Sitzungsbeginn neu zu messen**, seither sind vier
Prompts und drei Registereinträge hinzugekommen: 19 Vorkommen der Form Paragraphenzeichen plus
Großbuchstabe, **sämtlich in Wurzel-`.md`**, keines in `.py`. Sieben in `02b-abnahme.md`, fünf im
Register, drei in `00`, je eines in `00v-grammatik-prompt.md`, `02b-golden-anchors.md` und zwei
Sitzungsstart-Dateien.

Die Forks, die zu benennen sind, bevor eine Position bezogen wird:

- **Wird die Anhangsform überhaupt geprüft?** Die Anhänge tragen keine nummerierten
  Überschriften der Ebene 2–4, auf die `HEADING_NUM` passt. Eine Prüfung bräuchte eine zweite
  Überschriftenquelle — das ist der eigentliche Preis, nicht die Regex.
- **Gilt sie nur für `.md`?** In Python gibt es keinen Fall. Eine Regel ohne Anwendung ist
  vorgezogene Arbeit; eine Regel, die erst bei der ersten Anwendung entsteht, ist zu spät.
- **Ist `§B.2` ein Bereich, ein Abschnitt oder eine Tabellenzeile?** In `02b-abnahme.md` wird die
  Form für Vektoren benutzt, in `00` für Anhangsabschnitte. Das ist zu messen, nicht zu vermuten.

**Der erste Griff ist eine Messung, keine Position.** Sie kostet den Operator keinen Zug: die
Projektkopie trägt alle Wurzel-`.md`.

## Offen

- **Die Anhangsform der Zitiergrammatik ist nicht entschieden** (D221, D227, D229). Zahlen oben.
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
- **`example-nucleus.md` zitiert für die Kapazitätsformel den falschen Abschnitt** — genannt ist
  `02 §2` (Graphmodell), gemeint ist `02 §3` beziehungsweise `02a §2.2`. Formal gültig, deshalb
  grün. Der erste gemessene Fall der Grenze aus D229.
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
- **`example-nucleus.md`** weiterhin unvollständig, aber `§5.1` steht seit D202.
- **Braucht der Node eine eigene Beschreibung?** D180 sagt ausdrücklich nein.
- **Layer 05.** Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf), die Beta-Reputation
  mit dem Moral-Licensing-Problem — und seit D178 die Frage, ob wiederholtes Stimmen auf
  unveröffentlichte Vorschläge eine Folge tragen soll.

**Erledigt und nicht wieder aufzumachen:** die Zeilenlängenfrage für Python ist mit D205 verneint.
Die Frage nach einer dritten `ruff`-Gruppe ist mit `ARG` beantwortet. Der Fork aus D197 ist mit
D200 entschieden. Die Formfrage für `Finding.subject` ist mit D207 entschieden. Ein
Übersichtsdokument über die Schichten ist mit D209 verworfen. Die Fangbreite der Prädikatprüfer
ist mit D213 entschieden. Die Löschung von `is_nuc_predicate` ist mit D216 vollzogen. Teil A der
Zitierkonvention ist mit D219 und `00u` erledigt, Frage 1 der Grammatik mit D221 und `00v`, **Frage
2 mit D227 und den vier Tranchen der Sitzung `00y`**. Die Zeilenlänge ist mit D222 und `00w`
geprüft. Das Nachziehverfahren steht mit D224. Das Temp-Verzeichnis für Splices ist mit D225
abgeschafft. **Die Bereichsform ist mit D228 entschieden, ein eigener Test für `tools/` mit D229
verworfen.**

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.
