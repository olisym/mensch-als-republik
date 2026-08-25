# Sitzungsstart: 00u (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`). Das
lokale Arbeitsverzeichnis ist `~/mensch-als-republik`.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 41, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu ist **41**: die Vorabvariante ist Erwartungsquelle, nicht Vorbild (D217).

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird. Der Index findet nur **qualifizierte** Namen: ein Eintrag, der
`§6.1` schreibt statt `03 §6.1`, taucht dort nie auf.

Was in dieser Sitzung am meisten getragen hat:

- **Die Variante vollständig bauen, bevor der Prompt entsteht.** Für `00t` standen Testzahl,
  Grep-Zählungen, beide Probenausgaben und fünf Zeilenmengen fest, bevor das Werkzeug lief. Die
  Abnahme war eine Prüfung und keine Entdeckung. Das kostet den Operator keinen Zug, weil die
  Projektkopie mit `pip install cbor2 cryptography pytest hypothesis ruff` die volle Reihe fährt.
- **Aber die Variante bindet das Werkzeug nicht.** In `00t` war die Variante an einer Stelle
  schlechter als der Prompt: sie zählte alle Python-Befunde als einen, der Prompt verlangte die
  Zählung je Datei. Die vier Zeilen Abweichung waren die Reparatur, nicht der Preis. Prüfregel 41.
- **Wer eine Defektklasse repariert, zählt zuerst ihre Vorkommen.** D212 benannte zwei
  Docstring-Zeiger in `mensch_als_republik/findings.py`; es waren drei. Der dritte zeigte für die
  halbe Aussage richtig und ist deshalb durch dieselbe Durchsicht gefallen.
- **Eine Prüfung schlägt einen Registereintrag.** Die drei Zeiger waren berichtigt und blieben
  ungeprüft, bis `check_specs.py` über Python lief. Jetzt fängt sie jeden Zeiger auf einen
  gelöschten oder umnummerierten Abschnitt — die kleinere Klasse, aber die maschinelle.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`, `ruff`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und
  eine Pipe auf `tail` sind die nützlichen Ausnahmen. Nach Regel 39 sichert eine Zeile, die nur
  ausgibt, nichts: `test (git branch --show-current) = main` statt der blossen Ausgabe.
- **Spec-Dateien und Splice-Skripte als Download**, nicht als Copy-Block. Werkzeug-Prompts als
  Datei.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet` — aber nur für
  Dateien, die unverändert sein **müssen**.
- Bei neuen Dateien `git add` **vor** `make check`. Explizite Pfade, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. Zeilen brechen bei 100 Zeichen — das gilt für
  **Spec-Dateien und Prompt-Dateien im Wurzelverzeichnis**, ist aber **ungeprüft**; es hält nur,
  weil jeder Splice es selbst assertet. Für Python gibt es **keine** Zeilenlängenregel; D205 hat
  das mit Zahlen entschieden und nicht wieder aufzumachen.
- **Ein Prompt im Wurzelverzeichnis wird von `check_specs.py` mitgeprüft.** Wer darin einen
  kaputten Verweis als Literal zitiert, macht die eigene Datei rot; nach D210 wird die Nummer
  ohne Paragraphenzeichen genannt. Ausgenommen sind `07-decisions.md` und `sitzungsstart-*.md` —
  diese Datei darf frei zitieren.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Zählvorschriften, die tragen:**
  - Registerköpfe: `grep -c '^### D' 07-decisions.md`.
  - Prüfregeln: `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`.
  - Branches: `git branch -a | wc -l`.
  - Abschnitte je Datei: `grep -n '^## ' <datei>`.
- **Der eigene Baum ist die stärkste Messung** — aber nur, wenn er auf dem Commit steht, über den
  geredet wird. Wächst `main` während der Sitzung, wächst die Kopie nicht mit. Die Kopie nach
  jedem Merge nachziehen, auch bei Code, den das Werkzeug geschrieben hat.
- **Die Kopie wird am Sitzungsende erzeugt, nicht am Anfang.** Nach dem letzten Push ein
  repomix-Lauf mit `--header-text`, der Commit, Testzahl, Registerstand und Prüfregelzahl trägt.
  Der Lauf gehört hinter einen Abgleich von `HEAD` gegen `origin/main` — eine Kopie von einem
  ungepushten Stand kann niemand nachprüfen. Die erzeugte Datei bleibt aus dem Repository: eine
  committete Ableitung ist der nächste stille Drift-Kandidat (D218).
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position,
  **40** vor jeder Erwartung an einen Kopfstand, **41** vor jeder Bewertung einer Abweichung.
- **Prüfregel 28**: die Welt im Prompt ist Feld für Feld die gemessene Welt.

### Splices

Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher trocken gegen eine
Kopie gelaufen. Diese Sitzung hat zwei Splice-Läufe gefahren, beide sauber.

- **Jeder Splice läuft trocken gegen den Stand nach dem vorigen**, nicht gegen die Projektkopie.
- **Ein zweiter Lauf desselben Skripts muss scheitern.** Beide Male gehalten.
- **Nur die neuen Zeilen auf Länge prüfen, nicht die ganze Datei.** Der Altbestand führt Zeilen
  über 100 Zeichen. **Tabellenzeilen nicht ausnehmen.**
- **Blöcke werden ersetzt, nicht Teilstrings geflickt.** Wer in eine Datei mit Abschnittsstruktur
  einfügt, ersetzt den Ankerblock samt Überschrift — ein Split am Anker und Neuzusammenbau
  zerlegt den Abschnitt darüber. In dieser Sitzung einmal beim ersten Anlauf passiert.
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`.

**Der Kopf ist nicht `43b984c`.** Das ist der letzte inhaltliche Commit; der Übergabe-Commit
dieser Datei liegt darüber. Prüfregel 40 — der Kopf wird gemessen, nicht aus dieser Zeile
abgeschrieben.

**597 Tests.** Register **D1–D217**, Prüfregeln **1–41**. **Drei Branches** (`main`,
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
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py` (**seit D215 mit
  Verweisprüfung über Python**), `tools/check_tree.py`.

**Neu in dieser Sitzung:** D215 bis D217, ein Lauf (`00t`), Prüfregel 41,
`00t-zeiger-prompt.md`, die Python-Verweisprüfung in `check_specs.py`.

- **D215** — Die Zeiger im Code werden geprüft, nicht nur berichtigt. Drei Docstrings in
  `mensch_als_republik/findings.py` nennen jetzt `00 §10`; der Zwilling in
  `governance/findings.py` bleibt, weil er in der eigenen Schicht zeigt. `check_section_refs`
  läuft zusätzlich über alle `.py` ohne `.venv`. Verworfen: `00 §5.4` daneben stehen lassen,
  und `check_escapes` mitlaufen lassen.
- **D216** — `is_nuc_predicate` gelöscht. Null Produktiv-Aufrufstellen; die einzige Aufrufstelle
  prüfte die Funktion auf eine Eigenschaft ihrer selbst. Verworfen: behalten wegen D213,
  behalten wegen Symmetrie zu `is_core_predicate` (das acht Aufrufstellen hat), und den Lauf
  nicht anfassen, weil `00s` eine Runde alt ist.
- **D217** — Abnahme `00t`, kein Defekt. Die Abweichung von vier Zeilen war die Reparatur eines
  Fehlers in der Vorabvariante. Daraus Prüfregel 41.

## Was diese Sitzung gelehrt hat

**Der Supervisor bleibt die Fehlerquelle, aber die Asymmetrie hat einen zweiten Ausgang.**
Bisher galt: das Werkzeug führt aus, der Prompt ist der Defekt. In `00t` war der Prompt richtig
und die Variante daneben falsch — und weil abgenommen wird, was der Prompt sagt, hat das
Werkzeug die Variante korrigiert. Eine Abweichung ist deshalb kein Verdacht, sondern eine Frage
in zwei Richtungen.

**Eine Klasse repariert man an ihrer Zählung, nicht an ihren Fundstellen.** D212 hat zwei von
drei erwischt, weil es zwei gefunden hatte.

**Nicht jeder Eingriff kann eine rote Probe haben, und das gehört in den Prompt.** `00t` hatte
vier Eingriffe und zwei Proben. Die beiden anderen sind im Prompt ausdrücklich als probenlos
benannt worden, mit Begründung — sonst hätte das Werkzeug eine erfunden.

## Der nächste Schritt

**Die Zitierkonvention injektiv machen** (D209). Gemessen auf `43b984c`, und die Messung teilt
den Fork in zwei sehr ungleiche Hälften:

**A — die Buchstabenpräfixe. Klein und abschliessbar.** 31 Verweise der Form `NNx §Y` in
`.md` und `.py` zusammen, verteilt auf fünfzehn Dateien, mit genau vier benutzten Namen:

| Name | Verweise | beanspruchende Dateien |
|---|---|---|
| `02a` | 24 | `02a-abnahme.md`, `02a-maxflow-prompt.md` |
| `01a` | 3 | `01a-nachtrag-prompt.md`, `01a-policy-prompt.md` |
| `04a` | 2 | `04a-korrektur-prompt.md` — **eindeutig** |
| `02b` | 2 | `02b-abnahme.md`, `02b-golden-anchors.md` |

Drei zweideutige Namen, sechs Dateien. `04a` ist bereits injektiv. Der erste Griff ist die
Frage, welche der beiden `02a`-Dateien die vierundzwanzig Verweise meinen — eine Messung, keine
Position. Danach zwei Wege: eine Datei umbenennen, oder eine Zuordnungstabelle wie `LAYER_FILES`,
die den Zitiernamen an genau eine Datei bindet und die Prüfung darauf ausweitet. Erst messen.

**B — die präfixlosen Verweise in Python. Gross und nicht nebenbei zu lösen.** 260
Paragraphenverweise in `.py`, davon **201 ohne Ziffernpräfix**, über siebzig Dateien. Die neue
Prüfung erfasst 59 von 260. Eine Zuordnung Verzeichnis auf Schicht wäre der billige Weg und
trägt nicht: `mensch_als_republik/policy.py` nennt `00 §3` und daneben die Prompt-Datei der
Schicht 04. B braucht eine eigene Position, bevor irgendwer anfängt, und ist kein Nachmittag.

A zuerst. B bleibt offen und ist ausdrücklich kein Anhängsel von A.

## Offen

- **Die Sitzungsstart-Datei ist ein monolithisches Rewrite** (D218). Vorgeschlagen ist eine
  eigene, nur per Splice editierte Datei für die offene Liste. Nicht entschieden.
- **Es gibt keine Kontextdatei für das Werkzeug** (D218). Fork mit benanntem Gegenargument.
- **Die Projektkopie hat kein erzwungenes Nachziehverfahren** (D218). Das Verfahren steht oben
  unter „Messen"; nichts prüft, ob es eingehalten wurde.
- **Die Zitierkonvention ist nicht injektiv** (D209). Teil A ist der nächste Schritt, Teil B
  offen. Zahlen oben.
- **201 von 260 Paragraphenverweisen in Python sind ungeprüft** (D217).
- **Die Verweisprüfung kann Listenpunkte nicht von Unterabschnitten unterscheiden** (D209).
- **Zwei Registerverweise zeigen ins Leere**, `03 §5.1` und `03 §11`. Bewusst nicht nachgezogen:
  das Register beschreibt vergangene Stände.
- **Die 100-Zeichen-Regel ist ungeprüft.** Sie hält nur, weil jeder Splice sie selbst assertet.
  Eine Prüfung dafür ist ein eigener Fork und nicht aufgemacht.
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
ist mit D213 entschieden. Die Löschung von `is_nuc_predicate` ist mit D216 vollzogen; wer sie
zurückholt, braucht einen Produktiv-Aufrufer, den D216 nicht gemessen hat. Die beiden
Docstring-Zeiger aus D212 und der dritte, den D212 übersah, sind mit D215 erledigt.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.
