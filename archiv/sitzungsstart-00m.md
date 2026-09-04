# Sitzungsstart: 00m (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 31, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu sind **30** (Nullprobe, D192) und **31** (der Vergleichspunkt ist der
Prompt-Commit, D196).

Was in der Praxis am häufigsten gebraucht wird:

- **Design vor Code, Modulcode vor Prompt.** In dieser Sitzung hat viermal erst das Lesen des
  Moduls den Zuschnitt sichtbar gemacht. `decide` prüft Verfassung und Zielverfassung
  **asymmetrisch** — das stand in keinem Register und war der ganze Ertrag der letzten Runde.
- **Der Bericht des Werkzeugs ist nie die Abnahme.** Geprüft wird der Diff. In dieser Sitzung
  waren beide Berichte zutreffend und beide Läufe defektfrei; der einzige Defekt lag im
  Abnahmekriterium des Supervisors.
- **Messen statt vermuten, und selbst messen.** Der Supervisor hat beide Läufe in einem eigenen
  Baum nachgebaut, die volle Reihe und jede Probe unabhängig gefahren. Das hat zweimal Sicherheit
  gegeben, die kein Bericht gibt. Die Projektkopie lässt sich per `sha256sum` gegen den Commit
  prüfen und dann lesen, statt Dateien anzufordern (Prüfregel 26).
- **Literatur vor Bauen.** D194 hat die Form der Lösung aus RFC 8914 übernommen — Diagnose ist ein
  getrenntes, additives Feld, das die Verarbeitung nicht verändern darf. D195 und D197 haben
  python-tuf 2669 aufgeschlagen und dabei gefunden, dass die dort offene Frage in MaR nicht offen
  ist. Bei jedem Fork, den andere seit Jahren bearbeiten, zuerst nachsehen.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt — auch dir
  selbst. Diese Sitzung hat eine Zusage aus dem eigenen Baum nachgemessen und berichtigt (D193)
  und einen gemeldeten Produktivbefund als Messfehler des Supervisors entlarvt (D192).
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`, `ruff`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende ist
  die nützliche Ausnahme.
- **Spec-Dateien und Splice-Skripte als Download**, nicht als Copy-Block. Werkzeug-Prompts als
  Datei, wenn sie lang sind.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet -- <datei>`.
- Bei neuen Dateien `git add` **vor** `make check`, sonst meldet `check_tree.py` unversionierte
  Quelldateien. Explizite Pfade, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. Zeilen brechen bei 100 Zeichen — das gilt für
  **Spec-Dateien**; für Python gibt es keine Zeilenlängenregel, `pyproject.toml` setzt kein
  `line-length` und wählt nur `F401` und `F811`.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Zählvorschriften, die tragen:**
  - Registerköpfe: `grep -c '^### D' 07-decisions.md`.
  - Prüfregeln: `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`.
  - Branches: `git branch -a | wc -l`.
- **Prüfregel 26:** der Hash-Abgleich einer Projektkopie gilt für den Commit, an dem er gemacht
  wurde. In dieser Sitzung war die Kopie bei `2aef81d` byte-genau; danach waren alle Diffs
  bekannt, deshalb blieb sie bis zum Ende brauchbar.
- **Prüfregel 27:** vor jedem Verweis in einem Prompt die Stelle aufschlagen.
- **Prüfregel 28:** die Welt im Prompt ist Feld für Feld die gemessene Welt.
- **Prüfregel 30, neu:** eine Variantenwelt wird zuerst mit unverändertem Feld gebaut und gegen
  die Referenzwelt nachgewiesen, bei Claims claim-ID-genau.
- **Prüfregel 31, neu:** der Vergleichspunkt eines Laufs ist der Prompt-Commit. Wenn der Hash beim
  Schreiben des Prompts noch nicht feststeht, lässt der Prompt das Werkzeug ihn beim Start
  festhalten (`set BASIS (git rev-parse HEAD)`) — das spart eine Runde und ist regelkonform.

### Splices

Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher trocken gegen eine
Kopie gelaufen. Diese Sitzung hat vier Splice-Läufe gefahren, alle sauber.

- **Jeder Splice läuft trocken gegen den Stand nach dem vorigen**, nicht gegen die Projektkopie.
- **Ein zweiter Lauf desselben Skripts muss scheitern.** Das ist die billigste Negativprüfung und
  hat in dieser Sitzung viermal gehalten.
- **Nur die neuen Zeilen auf Länge prüfen, nicht die ganze Datei.** Der Altbestand führt Zeilen
  über 100 Zeichen — `07-decisions.md` und `04-governance.md` beide. Eine Ganzdateiprüfung im
  Splice bricht am Altbestand ab; genau das ist beim ersten Trockenlauf zu D192 passiert.
- **Blöcke werden ersetzt, nicht Teilstrings geflickt.**
- Umlaute schreiben, nicht Umschrift.
- Die Splice-Skripte danach aus dem Wurzelverzeichnis **löschen**.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`.

Zum Ende dieser Sitzung: `main` bei `225eb4d`, gepusht. **576 Tests**. Register **D1–D199**,
Prüfregeln **1–31**. **Drei Branches** (`main`, `origin/HEAD`, `origin/main`) — keine Lauf- und
keine Altbranches mehr. Keine offenen Läufe.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys` in
  `mensch_als_republik/keys.py`.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A; `is_nuc_name` in `predicates.py` ist ihre einzige Implementierung.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung, Genesis-Bindung in `decide`,
  `§4.5` Kettenauflösung. **`§3.5` trägt seit D198 die Subjektregel.**
- **Fassade** (`mensch_als_republik/resolve.py`): `resolve_state` und `NucleusState`, seit D183.
- **Kettenbauer** (`tests/kettenwelt.py`): baut aus Identitäten, Wurzelschlüsseln und einer Folge
  von Verfassungen eine fertige Kette. Seit D190/D191, Docstring berichtigt in D193.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests.

**Neu in dieser Sitzung:** D192 bis D199, zwei Läufe (`00k`, `00l`), Prüfregeln 30 und 31, die
Subjektregel in `04 §3.5`, `tests/governance/test_vermerk_subjekte.py`, drei neue Tests in
`tests/test_kettenwelt.py`, und der vollständige Branch-Aufräumzug.

- **D192** — Der gemeldete Produktivbefund zur dreiepochigen Ratifizierung war eine verunreinigte
  Welt. `Identity` ist eine fortlaufende Autorenkette; zwei Welten aus denselben Objekten sind
  nicht dieselbe Welt. Der Widerspruch in der Diagnose löste sich auf: `_unsupported` und die
  Zitatschleife in `verify_ratification` sind zwei Pfade, ein Stimm-Subjekt bedeutet
  `cid not in tally.yes`. Daraus Prüfregel 30.
- **D193** — Berichtigung an D191: die Vorbedingung im Docstring des Kettenbauers war falsch. Es
  zählt **Teilnehmerschaft**, nicht Autorisierung. Gemessen: A ratifiziert unter einer Epoche, die
  nur B autorisiert, und die Kette läuft durch.
- **D194** — Die Ratifizierung gibt die Vermerke der Auszählung weiter, wenn diese `UNEVALUABLE`
  ist. Form nach RFC 8914: additiv, der grobe Vermerk bleibt, die Verarbeitung ändert sich nicht.
- **D195** — Prüffall: fehlende Zwischenverfassung, Kette hält bei Epoche 1.
- **D196** — Abnahme `00k`. Der einzige Defekt lag im Abnahmekriterium. Daraus Prüfregel 31.
- **D197** — Die **untaugliche** Zwischenverfassung sperrt anders als die fehlende: die Kette
  rückt in sie ein und sie regiert. Das ist der zweite Fall aus D190, neu formuliert.
- **D198** — Das Subjekt eines Auszählungsvermerks benennt das zurückgewiesene Objekt. Drei
  Stellen in `decide` berichtigt; Genesis-Fehler adressieren den Scope.
- **D199** — Abnahme `00l`, kein Defekt.

## Was diese Sitzung gelehrt hat

**Ein gemeldeter Produktivbefund kann ein Messfehler des Bauapparats sein.** Der erste offene
Punkt der Vorsitzung war als möglicher Defekt notiert. Er verschwand im ersten Messwert, sobald
die Variantenwelt eine Nullprobe bekam. Ohne diese Probe hätte die Sitzung Stunden in `decide`
gesucht, wo nichts war.

**Zwei richtige Lesarten können wie ein Widerspruch aussehen.** Beide Diagnosen der Vorsitzung
waren zutreffend; sie gehörten zu verschiedenen Codepfaden. Wer einen Widerspruch findet, sollte
zuerst prüfen, ob beide Seiten von derselben Stelle reden.

**Eine Probe belegt mehr als den Code, den sie prüft.** In `00l` trafen alle drei Rücknahmen nur
die neuen Tests. Damit ist am Artefakt vorgeführt, dass die drei Vermerksubjekte vorher von nichts
gehalten wurden — dieselbe Form wie Probe A in `00j`.

**Ein Test kann die Art prüfen und die Adresse nie.** Die vorhandenen Vektortests gehen über einen
`_kinds`-Helfer. Alle drei Subjekte umzustellen lief mit 576 grün durch. Wo ein Helfer ein Feld
wegabstrahiert, ist dieses Feld unbewacht, und niemand merkt es.

**Eine falsche Adresse ist schlechter als keine.** Der Kern von D194 und D198. Einer fehlenden
Adresse folgt der Beobachter nicht; einer falschen folgt er.

## Der nächste Schritt

**Der Fork aus D197: soll `decide` die Zielverfassung auf Inhalt prüfen, bevor sie Übergangsziel
wird?** Heute wird von ihr nur Vorhandensein, Hash und Schwelle geprüft. Eine Verfassung ohne
`participants` ist damit ein zulässiges Ziel; die Kette rückt in sie ein, sie liefert
`authorized_keys`, und erst der **nächste** Übergang scheitert. Gemessen und als Test festgehalten
in `test_kettenwelt_unusable_middle_constitution_governs`.

Das ist eine echte Gabel, kein Nachzug. Für das Prüfen spricht, dass ein Nukleus sonst in einen
Zustand rückt, aus dem er nie wieder herauskommt, und dass nichts an der Policy- oder
Schlüsselschicht das anzeigt. Dagegen spricht, dass die Prüfung dieselbe Sperre nur früher setzt —
und dass sie eine Verfassung ablehnt, die eine spätere Fassung des Protokolls vielleicht lesen
kann. python-tuf 2669 stellt die verwandte Frage und hat sie nicht entschieden.

**Vorgehen:** `04 §3.5` und `§4.1` sind gelesen und aktuell; die Welt existiert als Test. Zuerst
die Gegenprobe messen — was passiert, wenn die Prüfung eingebaut wird, welche Epoche erreicht die
Kette dann, wie viele Tests fallen. Dann eine Position, dann erst ein Prompt. Der Ausgang ist
offen; „nein, und zwar aus benanntem Grund" ist ein zulässiges Ergebnis und wäre ebenso zu
registrieren.

**Der billige Nachzug daneben:** `check_resolved_chain` hat in `example-nucleus.md` keinen
Abschnitt (D189). Ein Splice, keine Entscheidung, kein Lauf. Er hängt an nichts.

## Offen

- **Prüft `decide` die Zielverfassung auf Inhalt?** (D197). Erster Punkt, siehe oben.
- **Weitergabe der Auszählungsvermerke im auswertbaren Fall** (D194). Heute wird nur bei
  `UNEVALUABLE` weitergegeben. Scheitert eine Ratifizierung bei `PASSED`, `FAILED` oder `PENDING`,
  bleibt der Beobachter ohne Adresse. RFC 8914 lässt sein Feld ausdrücklich auch bei fehlerfreien
  Antworten zu; die Literatur zielt auf die breite Fassung.
- **`check_resolved_chain` hat in `example-nucleus.md` keinen Abschnitt** (D189).
- **Die Form der Vermerke ist außerhalb von `04 §3.5` nicht festgehalten** (D173). D198 hat den
  einen Ort besetzt; `00`, `01`, `02` und `03` bleiben unbestimmt.
- **Vergleiche gegen `dedupe_sort` sind für die Reihenfolge zirkulär** (D196). Inhaltlich tragen
  sie. Wer die Ordnung prüfen will, braucht einen eigenen Ort dafür.
- **Vier `Finding`-Klassen, vier `dedupe_sort`** (D183): strukturell identisch, nur im `kind`-Enum
  verschieden. Nicht anfassen, ohne die Frage zu stellen, ob die Enums je zusammengeführt werden.
  D191 hat die Trennung gebraucht; sie ist der Grund, warum ein Vertauschen von `policy_findings`
  und `key_findings` auffällt.
- **Eine dritte `ruff`-Gruppe** — `ARG` hätte den toten `now`-Parameter aus `00j` maschinell
  gefangen. D182 hat den Linter bewusst auf `F401` und `F811` festgelegt; eine dritte Gruppe
  braucht denselben Nachweis: erst die Zahl der Funde im Baum messen, dann entscheiden. **Die
  Zeilenlängenfrage für Python gehört mit hierher** und wird nicht nebenbei beantwortet.
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173).
- **Die Sondierwelt in `test_benennung.py` erzeugt keine Vermerke** (D173).
- **`is_nuc_predicate` und `is_core_predicate` fangen `VerifierError`, `is_nuc_name` fängt
  `Exception`** (D181): drei Funktionen nebeneinander, zwei Fangbreiten.
- **Eine Schwelle für Autoritätslisten** — mit D166 zurückgestellt. Wird für `root_keys`,
  `nucleus_keys` und `arbitration.arbitrators` **zugleich** beantwortet oder gar nicht.
- **Darf ein Amendment ein deklariertes Prädikat weglassen?** Gehört an `04 §5` (D167).
- **Der Beispielnukleus kann Epoche-1- von Epoche-2-Policy nicht unterscheiden** (D169). Von D188
  negativ beantwortet: die Fassade löst das nicht. Ob es je gelöst werden soll, ist offen.
- **`genesis[4]` und die Auszählung**: `GV-24` führt ein Genesis, dessen deklarierte Verfassung in
  der Auszählung nirgends vorkommt.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut.
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
- **`example-nucleus.md`** unvollständig.
- **Braucht der Node eine eigene Beschreibung?** D180 sagt ausdrücklich nein und benennt ihn nur.
  Wenn diese Antwort einmal nicht mehr trägt, wird sie hier fällig.
- **Layer 05.** Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf), die Beta-Reputation
  mit dem Moral-Licensing-Problem — und seit D178 die Frage, ob wiederholtes Stimmen auf
  unveröffentlichte Vorschläge eine Folge tragen soll.

**Erledigt und nicht wieder aufzumachen:** der Ratifizierer-Knopf im Kettenbauer wird **nicht**
mehr gebraucht. Er war für den Fall vorgesehen, dass der Ratifizierer die Auflösung verändert;
D192 hat gemessen, dass er es nicht tut. Ebenso ist der Branch-Aufräumpunkt abgeschlossen: alle
Lauf- und Altbranches sind lokal und auf Gitea gelöscht, gemessen als Vorfahren von `main`.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.
