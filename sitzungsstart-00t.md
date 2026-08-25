# Sitzungsstart: 00t (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 40, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu ist **40**: der erwartete Kopf des nächsten Blocks wird abgeleitet, nicht erinnert
(D214).

`python3 tools/register_index.py "04 §4.1"` nennt die Registereinträge, die einen Abschnitt
entschieden haben. Das ist Prüfregel 38 in ausführbarer Form und der billigste erste Griff, bevor
eine Position bezogen wird. **Neu gelernt: der Index findet nur qualifizierte Namen.** Ein
Registereintrag, der `§6.1` schreibt statt `03 §6.1`, taucht dort nie auf. Wer einen Eintrag
verfasst, schreibt die Datei mit — sonst schreibt er ihn für niemanden.

Was in dieser Sitzung am meisten getragen hat:

- **Die Variante vollständig bauen, bevor der Prompt entsteht.** Für `00s` stand die Rotmenge
  (9 rot, 588 grün, mit Namen) und die Testzahl (597) fest, bevor das Werkzeug lief. Die Abnahme
  war dann eine Prüfung und keine Entdeckung. Das kostet den Operator keinen einzigen Zug, weil
  die Projektkopie mit `pip install cbor2 cryptography pytest hypothesis ruff` die volle Reihe
  fährt.
- **Einen Textdefekt löst man aus seiner Herkunft, nicht aus dem Code.** `03 §6` nannte zweimal
  denselben Vermerk. Der Code gab keine Antwort darauf, welcher Name gemeint war — `03-prompt.md`
  Zeile 82 gab sie: dort stand `CONSTITUTION_HASH_MISMATCH`, und D167 hat ihn ersatzlos gestrichen.
  Die Reparatur war eine Streichung, keine Ersetzung. Ohne den Ursprungssatz wäre die falsche
  Antwort plausibel gewesen.
- **Eine Probe, die grün bleiben muss, kann die Aussage selbst sein** — aber nur neben einer
  roten. In `00s` belegt Probe A die Kopplung (ohne Wache verliert die Verengung ihr Netz), und
  Probe B belegt, dass die Verengung kein Verhalten ändert. Einzeln wäre B wertlos.
- **Der Bericht des Werkzeugs war zutreffend, der Diff hat trotzdem gezählt.** `00s` meldete
  `6 -2`, die Vorabmessung ergab `5 -1`. Die Differenz waren die zwei Docstring-Zeilen — plausibel,
  aber erst der Diff hat es zur Abnahme gemacht.
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
- Wer über einen kaputten Verweis schreibt, nennt seine Nummer ohne Paragraphenzeichen (D210).
  Ausgenommen sind `07-decisions.md` und `sitzungsstart-*.md` — diese Datei darf frei zitieren.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Zählvorschriften, die tragen:**
  - Registerköpfe: `grep -c '^### D' 07-decisions.md`.
  - Prüfregeln: `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`.
  - Branches: `git branch -a | wc -l`.
  - Abschnitte je Datei: `grep -n '^## ' <datei>`.
- **Der eigene Baum ist die stärkste Messung** — aber nur, wenn er auf dem Commit steht, über den
  geredet wird. Wächst `main` während der Sitzung, wächst die Kopie nicht mit; jede Zahl, die
  danach an einen Commit geheftet wird, ist neu zu messen. Die Kopie nach jedem Merge nachziehen,
  auch bei Code, den das Werkzeug geschrieben hat — der Diff aus `git show` reicht dafür.
- **Prüfregel 27** vor jedem Verweis, **33** für den Satz daneben, **38** vor der Position,
  **40** vor jeder Erwartung an einen Kopfstand.
- **Prüfregel 28**: die Welt im Prompt ist Feld für Feld die gemessene Welt.

### Splices

Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher trocken gegen eine
Kopie gelaufen. Diese Sitzung hat drei Splice-Läufe gefahren, alle sauber.

- **Jeder Splice läuft trocken gegen den Stand nach dem vorigen**, nicht gegen die Projektkopie.
- **Ein zweiter Lauf desselben Skripts muss scheitern.** Dreimal gehalten, jedes Mal am Hash-Test.
- **Nur die neuen Zeilen auf Länge prüfen, nicht die ganze Datei.** Der Altbestand führt Zeilen
  über 100 Zeichen. **Tabellenzeilen nicht ausnehmen.**
- **Blöcke werden ersetzt, nicht Teilstrings geflickt.**
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`.

Zum Ende dieser Sitzung: `main` bei `8c2f90f`, gepusht. **597 Tests**. Register **D1–D214**,
Prüfregeln **1–40**. **Drei Branches** (`main`, `origin/HEAD`, `origin/main`). Keine offenen Läufe.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
  **Neu: `§10` nennt beide Vermerke mit ihren Subjekten** (D212).
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A. **`parse_predicate` trägt seit D213 eine Typwache.**
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`. `§10` nennt die
  sechs Vermerke mit ihren Subjekten.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`. **`§6.1`
  führt seit D212 die Subjekttabelle mit vierzehn Arten.**
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung, `§3.5` mit der Subjektregel
  (D198), `§4.1` mit Bedingung 6 (D200) und der dritten Lage, `§4.5` mit der berichtigten
  Vermerksgrenze (D203).
- **Fassade** (`mensch_als_republik/resolve.py`): `resolve_state` und `NucleusState`.
- **Kettenbauer** (`tests/kettenwelt.py`), **Werkzeugschicht** (`werkzeuge.md`).
- **Linter**: `ruff` mit `ARG`, `F401`, `F811` (D205).
- **Werkzeuge**: `tools/register_index.py`, `tools/check_specs.py` (mit Verweisprüfung),
  `tools/check_tree.py`.

**Neu in dieser Sitzung:** D212 bis D214, ein Lauf (`00s`), Prüfregel 40, `00 §10`, die
Subjekttabelle in `03 §6.1`, `00s-fangbreite-prompt.md`, acht Prüfpunkte in
`tests/test_predicates.py`.

- **D212** — Die Vermerkssubjekte von `03` und `00`. Der Doppeleintrag in `03 §6` war ein
  Streichungsrest aus D167, keine falsche Namenswahl. Verworfen: eine dritte Spalte (die längste
  Tabellenzeile misst 92 Zeichen) und ein Halbsatz in `00 §6.4`.
- **D213** — Die Fangbreite wird an der Wurzel geschlossen. `parse_predicate` wirft für ein
  nicht-`str` `p` jetzt `MalformedCbor`; danach tragen alle drei Prädikatprüfer dieselbe
  Fangbreite. Verworfen: `is_nuc_name` allein verengen (kippt einen Prüffall aus D181) und alle
  drei auf `Exception` verbreitern (verschluckt Programmierfehler).
- **D214** — Abnahme `00s`, kein Defekt im Lauf. Der Fehler lag zweimal in der Erwartung des
  Supervisors. Daraus Prüfregel 40.

## Was diese Sitzung gelehrt hat

**Der Supervisor bleibt die konstante Fehlerquelle, und zwar an einer neuen Stelle.** Nicht die
Position war diesmal falsch und nicht der Verweis, sondern der behauptete Kopfstand: zweimal ein
Hash geheftet, der nie galt, weil der vorige Block etwas anderes hinterlassen hatte als der zuletzt
gesehene Zustand. Beide Male stand der Baum richtig. Prüfregel 40 ist die Antwort.

**Die vollständig gebaute Variante ist die billigste Abnahme.** Die Rotmenge aus Probe A stand mit
Namen im Prompt, bevor das Werkzeug lief, und traf exakt. Wer die Erwartung erst nach dem Bericht
formuliert, prüft den Bericht.

**Ein Registereintrag ohne Dateipräfix ist für den Index unsichtbar.** `§6.1` findet
`register_index.py` nicht, `03 §6.1` schon. Das ist keine Formalie: der Index ist das Werkzeug
gegen genau die Wiederholung, die diese Sitzungen dreimal gekostet hat.

## Der nächste Schritt

**Ein Lauf `00t`, der drei kleine offene Punkte zusammenzieht.** Alle drei stehen unter „reist beim
nächsten Lauf mit, der die Datei ohnehin anfasst" — getrennt kosten sie drei Läufe, gebündelt
einen. Zuerst messen, dann entscheiden, dann Register, dann Prompt:

1. **Die zwei Docstring-Zeiger in `mensch_als_republik/findings.py`** (D212). Der Modul-Docstring
   nennt `00 §5.4` für eine Aussage, die dort nicht steht; `dedupe_sort` nennt `04-prompt.md §2`
   schichtübergreifend. Seit D212 gibt es mit `00 §10` den wahren Anker für beides. Reine
   Zeigerkorrektur, keine Rücknahmeprobe möglich — die Abnahme ist der Diff.
2. **Die doppelte Formenliste in `tests/test_predicates.py`** (D214). Die vier Formen stehen
   zweimal als Literal, einmal je `parametrize`. Eine Modulkonstante behebt es. Rücknahmeprobe:
   eine fünfte Form ergänzen und prüfen, dass beide Prüffälle sie sehen.
3. **`is_nuc_predicate` löschen oder behalten** (D213). Null Aufrufstellen im Paket, in `tools/`,
   in den Tests, in keiner Spec-Datei. Vorgeschlagen war die Löschung; **entschieden ist nichts**.
   Seit D213 wird die Funktion mitgeprüft, die Asymmetrie ist also nicht mehr das Argument. Die
   Entscheidung braucht eine Position, bevor der Prompt entsteht.

**Der grössere Fork danach: die Zitierkonvention injektiv machen** (D209). `03` und `04`
bezeichnen je vier Dateien, `01a` zwei; Verweise mit Buchstabenpräfix sind deshalb **ungeprüft**.
Erster Griff ist eine Messung: wie viele Verweise tragen ein Buchstabenpräfix, und welche Datei
beansprucht welchen Zitiernamen. Erst danach eine Position. Das ist kein Nachmittag, aber es
hebt einen ganzen Verweisbestand aus dem Ungeprüften.

## Offen

- **Zwei Docstring-Zeiger in `mensch_als_republik/findings.py`** (D212). Erster Punkt.
- **Doppelte Formenliste in `tests/test_predicates.py`** (D214).
- **Löschung von `is_nuc_predicate`** — vorgeschlagen, nicht entschieden (D213).
- **Die Zitierkonvention ist nicht injektiv** (D209). Verweise mit Buchstabenpräfix ungeprüft.
- **Die Verweisprüfung kann Listenpunkte nicht von Unterabschnitten unterscheiden** (D209).
- **Zwei Registerverweise zeigen ins Leere**, `03 §5.1` und `03 §11`. Bewusst nicht nachgezogen:
  das Register beschreibt vergangene Stände.
- **Die 100-Zeichen-Regel ist ungeprüft.** Sie hält nur, weil jeder Splice sie selbst assertet.
  Eine Prüfung dafür ist ein eigener Fork und nicht aufgemacht.
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173). Der Rest von D173 ist erledigt: die Spec
  trägt die Subjekte in `00 §10`, `02 §10` und `03 §6.1`.
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
ist mit D213 entschieden, mit gebauter und gemessener Variante; wer sie wieder aufmacht, braucht
einen Aufrufer, den D213 nicht gemessen hat.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.
