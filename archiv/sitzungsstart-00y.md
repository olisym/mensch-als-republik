# Sitzungsstart: 00y (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`). Das
lokale Arbeitsverzeichnis ist `~/mensch-als-republik`.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 43, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu sind **42** (der Assert eines Splices prüft das Ergebnis, D223) und **43**
(zwischen Merge und Nachzug ist die Projektkopie kalter Kaffee, D224).

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird. Der Index findet nur **qualifizierte** Namen: ein Eintrag, der
`§6.1` schreibt statt `03 §6.1`, taucht dort nie auf.

Was in der letzten Sitzung am meisten getragen hat:

- **Die Variante vollständig bauen, bevor der Prompt entsteht.** Vier Läufe, vier Abnahmen ohne
  Überraschung — jede Zahl im Prompt war vorher auf der Projektkopie gerechnet. Das kostet den
  Operator keinen Zug.
- **Eine Messung schliesst einen Fork öfter, als sie ihn eröffnet.** Die vermutete Zweideutigkeit
  der `02a`-Namen war keine: die Abnahme-Dateien führen keine nummerierten Überschriften und
  konnten nie Zitierziel sein (D219). Erst messen, dann Position.
- **Wer eine Klasse repariert, misst zuerst ihre Grösse — und zwar mit derselben Regex, die
  später prüft.** D220 hat 185 präfixlose Verweise gezählt, weil es dateinamensqualifizierte
  mitgezählt hat; wirklich bar sind 73. D221 hat das berichtigt.
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
- **Spec-Dateien und Splice-Skripte als Download**, nicht als Copy-Block. Werkzeug-Prompts als
  Datei.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet` — aber nur für
  Dateien, die unverändert sein **müssen**.
- Bei neuen Dateien `git add` **vor** `make check`. Explizite Pfade, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. **Prosa bricht bei 100 Zeichen; Tabellenzeilen
  und Codeblöcke sind ausgenommen, und `make check-specs` prüft es** (D222). Für Python gibt es
  **keine** Zeilenlängenregel; D205 hat das mit Zahlen entschieden und nicht wieder aufzumachen.
- **Ein Prompt im Wurzelverzeichnis wird von `check_specs.py` mitgeprüft** — seit D221 auch auf
  Verweise der Dateinamensform. Wer darin einen kaputten Verweis als Literal zitiert, macht die
  eigene Datei rot; nach D210 wird die Nummer ohne Paragraphenzeichen genannt. Ausgenommen sind
  `07-decisions.md` und `sitzungsstart-*.md` — diese Datei darf frei zitieren, aber **nicht** von
  der Zeilenlänge.

### Die Zitiergrammatik

Seit D221 sind **zwei** Namensformen zulässig, und `check_specs.py` prüft beide:

1. **Der Dateiname**, mit oder ohne `.md` — `02a-maxflow-prompt.md §2.7`. Injektiv von selbst,
   ohne Tabelleneintrag.
2. **Die Kurzform** `NN` und `NNx` über `LAYER_FILES`. Dreizehn Einträge, **geschlossen**. Wer
   einen vierzehnten braucht, hat Form 1 übersehen.

Ein Kurzform-Name ohne Tabelleneintrag ist ein Befund (D219). Ein fehlender **Dateistamm** ist
keiner (D221) — die Verweise auf gelöschte Prompt-Dateien stehen in Umzugstabellen, die den Namen
erwähnen statt ihn zu benutzen. Der Preis ist benannt: ein vertippter Dateiname fällt durch.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt. In der letzten Sitzung zweimal
  gerissen, beide Male vom Supervisor, einmal committet.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Auch Dateizahlen werden gezählt, nicht von Hand aufsummiert.** D222 nannte 13 Dateien;
  gemessen waren es 11.
- **Zählvorschriften, die tragen:**
  - Registerköpfe: `grep -c '^### D' 07-decisions.md`.
  - Prüfregeln: `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`.
  - Branches: `git branch -a | wc -l`.
  - Abschnitte je Datei: `grep -n '^## ' <datei>`.
- **Die Projektkopie wird nach jedem Push nachgezogen** (D224, Prüfregel 43). Der repomix-Baustein
  hängt hinter jedem `git push`, schreibt nach `/tmp`, trägt fünf Kaltzahlen im `--header-text`
  und zählt gepackte gegen versionierte Dateien. Wer vor dem Nachzug eine Zahl aus der Kopie
  nennt, sagt dazu, dass sie hinter `main` liegt.
- **Verworfen für die Kopie:** `--compress`, `--remove-comments`, `--remove-empty-lines`,
  `--output-show-line-numbers`, `--no-file-summary`. Begründungen in D224; nicht wieder aufmachen.
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position,
  **40** vor jeder Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung,
  **43** vor jeder Zahl aus der Kopie.
- **Prüfregel 28**: die Welt im Prompt ist Feld für Feld die gemessene Welt.

### Splices

Ein Splice ist ein Skript mit `assert`, dass der Anker genau einmal vorkommt. Gefahren wird er mit
`python3 tools/splice_run.py /tmp/splice-dNNN.py` (D225). Der Harness verlangt einen sauberen
Baum, erzwingt das Scheitern des zweiten Laufs, prüft die Zeilenlänge am Ergebnis und setzt bei
jedem Fehlschlag zurück. Temp-Verzeichnis und Trockenlauf gegen eine Kopie sind entfallen — Git
ist der Rollback.

- **Ein zweiter Lauf desselben Skripts muss scheitern.** Ohne wirksamen Anker gibt es keinen
  Splice.
- **Der Assert prüft das Ergebnis, nicht den eingesetzten Text** (Prüfregel 42).
- **Tabellenzeilen sind von der 100-Zeichen-Grenze ausgenommen** (D222).
- **Was der Harness nicht fängt** (D226): einen Splice, der eine zu lange Zeile entfernt und eine
  andere einsetzt, und eine unversionierte Datei, die ein gescheiterter Splice angelegt hat.
- **Blöcke werden ersetzt, nicht Teilstrings geflickt.** Wer in eine Datei mit Abschnittsstruktur
  einfügt, ersetzt den Ankerblock samt Überschrift.
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`.

**Der Kopf ist nicht `75bf695`.** Das ist der Stand nach D226; der Übergabe-Commit dieser Datei
liegt darüber. Prüfregel 40 — der Kopf wird gemessen, nicht aus dieser Zeile abgeschrieben.

**597 Tests.** Register **D1–D226**, Prüfregeln **1–43**. **Drei Branches** (`main`,
`origin/HEAD`, `origin/main`). Keine offenen Läufe.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
  `§10` nennt beide Vermerke mit ihren Subjekten (D212) und ist seit D215 der Anker für alle
  drei Docstrings in `mensch_als_republik/findings.py`.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A. `parse_predicate` trägt seit D213 eine Typwache. **`is_nuc_predicate` ist
  mit D216 gelöscht.**
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`. `§10` nennt die
  sechs Vermerke mit ihren Subjekten.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`. `§6.1`
  führt seit D212 die Subjekttabelle mit vierzehn Arten.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung, `§3.5` mit der Subjektregel
  (D198), `§4.1` mit Bedingung 6 (D200) und der dritten Lage, `§4.5` mit der berichtigten
  Vermerksgrenze (D203).
- **Fassade** (`mensch_als_republik/resolve.py`): `resolve_state` und `NucleusState`.
- **Kettenbauer** (`tests/kettenwelt.py`), **Werkzeugschicht** (`werkzeuge.md`).
- **Linter**: `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py` (Verweisprüfung über Python
  seit D215, Dateinamensform seit D221, Zeilenlänge seit D222), `tools/check_tree.py`,
  `tools/splice_run.py` (seit D225).

**Neu in der letzten Sitzung:** D219 bis D226, vier Läufe (`00u`, `00v`, `00w`, `00x`),
Prüfregeln 42 und 43, `tools/splice_run.py`, drei geschlossene offene Punkte.

- **D219** — Die Buchstabennamen sind gebunden. `LAYER_FILES` führt `01a`, `02a`, `02b`, `04a`;
  ein Kurzform-Name ohne Eintrag ist ein Befund. Verworfen: eine Datei umbenennen, und die Regex
  aus den Tabellenschlüsseln bauen.
- **D220** — Teil B vermessen, keine Position. Fünf Namensformen im Umlauf. **Die Zahlen dieses
  Eintrags sind mit D221 berichtigt.**
- **D221** — Zwei Namensformen, der Dateiname bindet sich selbst. Ein fehlender Dateistamm ist
  kein Befund. Vier tote Zeiger benannt und mit `00v` berichtigt. Verworfen: die Anhangs-Zielform
  mitbauen, weil sie heute null Wirkung hätte.
- **D222** — Die 100-Zeichen-Grenze gilt für Prosa, nicht für Tabellenzeilen. Gemessen: 268 von
  27194 Zeilen über 100, davon 244 Tabellenzeilen. Verworfen: semantische Umbrüche, die Grenze
  streichen, eine höhere Grenze für Tabellen.
- **D223** — Abnahme `00w`, kein Defekt. Die Stummelzeilen sind benannt und bleiben. Daraus
  Prüfregel 42.
- **D224** — Die Projektkopie wird nach jedem Push nachgezogen. Verworfen: Lesezugriff des
  Supervisors aufs Repository über einen Spiegel. Daraus Prüfregel 43.
- **D225** — Zwei Änderungen am Takt: der Prompt verlangt den vollständigen Diff, und Splices
  laufen über einen Harness. Zurückgenommen: die Sorge, das Register mache den Nachzug teuer.
- **D226** — Abnahme `00x`, kein Defekt. Zwei Grenzen des Harness benannt.

## Was die letzte Sitzung gelehrt hat

**Zwei falsche Zahlen, beide von Hand, beide vom Supervisor.** Eine erwartete `numstat`-Zeile und
eine Dateizahl, die schon committet war und einen Berichtigungs-Commit gekostet hat. Prüfregel 1
stand die ganze Zeit da. Eine Zahl, die in einem Satz steht, ist eine Behauptung — auch wenn sie
klein aussieht.

**Eine Messung mit derselben Regex, die später prüft.** D220 hat präfixlose Verweise gezählt und
dabei dateinamensqualifizierte mitgenommen, weil die Messregex das Wort vor dem
Paragraphenzeichen nicht als Namen las. Dieselbe Lücke ist in derselben Sitzung zweimal
aufgetreten. Wer eine Klasse zählt, zählt sie mit dem Werkzeug, das sie später erkennt.

**Der Anteil ohne den Nenner klingt nach Knappheit.** „Das Register ist 22 Prozent der Kopie" war
richtig und irreführend; die Kopie hat 2,15 MB gegen 30 MB Grenze. D225 hat die Sorge
zurückgenommen.

**Ein zu enges Abnahmekriterium erzeugt eine Nebenwirkung, die man benennen muss.** `00w` durfte
je Befund genau eine Zeile löschen, damit der Diff Wort für Wort prüfbar blieb. Das hat 17
Stummelzeilen erzeugt. Der Preis war richtig gewählt und gehört ins Register, nicht in eine
spätere Entdeckung.

## Der nächste Schritt

**Frage 2 der Zitiergrammatik** (D220, D221). Frage 1 ist entschieden und gebaut. Die Prüfung
erfasst 187 von 260 Paragraphenverweisen in Python.

Offen ist, was ein **barer** Verweis bedeutet. 73 stehen noch in `.py`, davon treffen 62
Überschriften in mehr als einer Layer-Datei — eine Heuristik über die Nummer gibt es nicht. Drei
Lesarten stehen zur Wahl, und keine ist bezogen:

1. **Fortsetzung im Modulkontext** — der Verweis erbt das zuletzt im selben Modul genannte
   Präfix. Deckt die sechs, die heute in keiner Layer-Datei treffen; die zeigen alle auf
   `02a-maxflow-prompt.md`.
2. **Die eigene Schicht** — abgeleitet aus dem Paketverzeichnis. Gemessen in D220 und schwach:
   98 gedeckt, 18 widerlegt, 69 in Dateien ohne Schichtverzeichnis.
3. **Unzulässig** — jeder Verweis wird qualifiziert. 73 Stellen, und die Grammatik ist geschlossen.

**Der erste Griff ist eine Messung, keine Position**, und sie kostet den Operator keinen Zug: die
73 Fundstellen einzeln im Kontext ansehen und je Stelle prüfen, welche Lesart sie trägt. Lesart 1
ist mechanisch entscheidbar — ein vorher genanntes Präfix im selben Modul gibt es oder nicht.
Lesart 2 ist es nicht. Erst wenn feststeht, wie viele der 73 jede Lesart erklärt, hat die Position
Boden.

Dazu gehört die **Anhangs-Zielform**: `01-claim-atom.md` führt fünfzehn Anhangsüberschriften, und
Verweise wie `§B.2` gibt es. Sie sind heute alle bar, weshalb D221 die Zielform vertagt hat. Wer
Frage 2 entscheidet, entscheidet sie mit.

## Offen

- **Die Sitzungsstart-Datei ist ein monolithisches Rewrite** (D218). Vorgeschlagen ist eine
  eigene, nur per Splice editierte Datei für die offene Liste. Nicht entschieden.
- **Es gibt keine Kontextdatei für das Werkzeug** (D218). Fork mit benanntem Gegenargument.
- **Das Register ist ein Fünftel der Projektkopie** (D224, entschärft mit D225). Beobachtung ohne
  Dringlichkeit; eine Teilung nach Ären müsste zuerst gegen `tools/register_index.py` gemessen
  werden.
- **Frage 2 der Zitiergrammatik ist offen** (D220, D221). Zahlen oben.
- **73 von 260 Paragraphenverweisen in Python sind ungeprüft** (D221). Geprüft werden 187.
- **Die Verweisprüfung kann Listenpunkte nicht von Unterabschnitten unterscheiden** (D209).
- **Der Harness vergleicht Zeilenzahlen, er identifiziert Zeilen nicht** (D226). Ein Splice, der
  eine zu lange Zeile entfernt und eine andere einsetzt, läuft durch.
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
Zitierkonvention ist mit D219 und `00u` erledigt, Frage 1 der Grammatik mit D221 und `00v`. Die
Zeilenlänge ist mit D222 und `00w` geprüft. Das Nachziehverfahren steht mit D224. Das
Temp-Verzeichnis für Splices ist mit D225 abgeschafft.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.
