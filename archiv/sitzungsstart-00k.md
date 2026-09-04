# Sitzungsstart: 00k (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 29, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu ist keine; **28 wurde geschärft** (D191) und endet jetzt nicht mehr beim
Konstruieren der Welt, sondern beim vollständigen Übertragen in den Prompt.

Was in der Praxis am häufigsten gebraucht wird:

- **Design vor Code.** Alle Forks und Zahlen stehen fest, bevor ein Prompt geschrieben wird.
  **Modulcode vor Prompt.** In dieser Sitzung hat dreimal erst das Lesen des Moduls den
  eigentlichen Zuschnitt sichtbar gemacht.
- **Der Bericht des Werkzeugs ist nie die Abnahme.** Geprüft wird der Diff. Diese Sitzung hat drei
  Defekte in einem Lauf gefunden, den das Werkzeug zutreffend beschrieben hatte, und keiner davon
  wäre durch einen Test oder ein Abnahmekriterium gefallen.
- **Literatur vor Bauen.** D190 hat die Form der Prüfwelt von `python-tuf` übernommen und zwei
  Prüffälle gleich mit. Bei jedem Fork, den andere seit Jahren bearbeiten, zuerst nachsehen.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt — auch dir
  selbst. Diese Sitzung hat eine Behauptung aus dem eigenen Register (D186 über `vote`)
  nachgemessen und berichtigt.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`, `ruff`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende ist
  die nützliche Ausnahme.
- **Spec-Dateien und Splice-Skripte als Download**, nicht als Copy-Block. Werkzeug-Prompts als
  Copy-Box.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet -- <datei>`.
- Bei neuen Dateien `git add` **vor** `make check`, sonst meldet `check_tree.py` unversionierte
  Quelldateien. Explizite Pfade, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. Zeilen brechen bei 100 Zeichen.
  `check_specs.py` prüft Escapes, Steuerzeichen, D-Nummern und hängende D-Verweise — **keine
  Zeilenlängen**.
- **Der Vergleichspunkt eines Laufs ist der Prompt-Commit.** Register-Eintrag vor dem Prompt, dann
  nennt der Prompt den Registercommit als Basis. Das hat in dieser Sitzung viermal getragen.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt und nie aus einer selbstgebauten
  Zählvorschrift. Diese Sitzung hat 64 Zeilen gemeldet, wo 63 standen: die Trennung des
  eingefügten Blocks an Zeilenumbrüchen zählte das leere Element vor dem führenden Umbruch mit.
  Die Vorschrift ist in den späteren Splices berichtigt — das erste Element wird abgeschnitten.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Zählvorschriften, die tragen:**
  - Registerköpfe: `grep -c '^### D' 07-decisions.md`. Die Regex-Prüfung im Splice zählt
    `^### D([0-9]+) — ` und liegt um **zwei** darunter (`D5a`, `D16 / D22`).
  - Prüfregeln: `grep -cE '^\*\*[0-9]+\.' pruefregeln.md` → **29**.
- **Prüfregel 26:** der Hash-Abgleich einer Projektkopie gilt für den Commit, an dem er gemacht
  wurde. In dieser Sitzung war die Kopie bei `3d6a18d` byte-genau; danach waren alle Diffs
  bekannt, deshalb blieb sie bis zum Ende brauchbar.
- **Prüfregel 27:** vor jedem Verweis in einem Prompt die Stelle aufschlagen.
- **Prüfregel 28, geschärft:** die Welt im Prompt ist Feld für Feld die gemessene Welt.
- Claude darf Messungen selbst fahren. Diese Sitzung hat jeden Lauf zusätzlich lokal nachgebaut
  und laufen lassen, bevor gemergt wurde — das hat zweimal Sicherheit gegeben, die der Bericht
  allein nicht gibt.

### Splices

Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher trocken gegen eine
Kopie gelaufen. Diese Sitzung hat sechs Splice-Läufe gefahren.

- **Jeder Splice läuft trocken gegen den Stand nach dem vorigen**, nicht gegen die Projektkopie.
- **Ein anhängender Splice braucht eine eigene Negativprüfung**: eine Marke, die vorher fehlt und
  nachher steht. Ans Register wird über eine Regex-Prüfung angehängt: der letzte Registerkopf muss
  der erwartete sein.
- **Blöcke werden ersetzt, nicht Teilstrings geflickt.** Die Schärfung von Prüfregel 28 hat den
  Wortlaut der ganzen Regel als Anker genommen.
- **Zeilenlängen nach dem Trockenlauf prüfen**, nur die neuen Zeilen, in Zeichen. Ein angehängter
  Satz, der in der Zeile des alten Schlusssatzes weiterläuft, erzeugt eine zu lange Zeile — genau
  das ist beim ersten Trockenlauf zu D191 passiert.
- Umlaute schreiben, nicht Umschrift. Eine erste Fassung des D185-Skripts war in Umschrift und
  wurde verworfen.
- Die Splice-Skripte danach aus dem Wurzelverzeichnis **löschen**.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`.

Zum Ende dieser Sitzung: `main` bei `1fd3dfe`, gepusht. **571 Tests**. Register **D1–D191**,
Prüfregeln **1–29**. Keine offenen Läufe. Die Branchzahl ist zu messen: zu Sitzungsbeginn fünf,
dazu die drei Lauf-Branches `impl/00h-fassadentests`, `impl/00i-kettenpruefung` und
`impl/00j-kettenwelt`, die nicht gelöscht wurden.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys` in
  `mensch_als_republik/keys.py`.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A; `is_nuc_name` in `predicates.py` ist ihre einzige Implementierung.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung, Genesis-Bindung in `decide`,
  `§4.5` Kettenauflösung.
- **Fassade** (`mensch_als_republik/resolve.py`): `resolve_state` und `NucleusState`, seit D183.
  Seit D188 mit einem Aufrufer ausserhalb der Tests.
- **Kettenbauer** (`tests/kettenwelt.py`): baut aus Identitäten, Wurzelschlüsseln und einer Folge
  von Verfassungen eine fertige Kette. Seit D190/D191.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests.

**Neu in dieser Sitzung:** D185 bis D191, drei Läufe (`00h`, `00i`, `00j`), Prüfregel 28 geschärft,
`tests/kettenwelt.py` und `tests/test_kettenwelt.py`, `check_resolved_chain` im Beispielnukleus,
`RUFF :=` im Makefile.

- **D185** — Berichtigung an D184: der Fassadentest war nicht zirkulär, sondern **reglos**. Keine
  Verfassung der Governance-Fixtures führt `nucleus_keys`, alle drei Policies sind gleich, der
  Vergleichsaufruf liefert unter der falschen Verfassung dasselbe.
- **D186** — Zurückgestellt gewesen: eine Kettenwelt, in der die Verfassung den Schlüsselsatz
  bewegt. Von D190 beantwortet.
- **D187** — Abnahme `00h`. Probe B hat die Reglosigkeit am Artefakt bestätigt.
- **D188** — Der Beispielnukleus führt die Kette vor (`check_resolved_chain`), ohne umgestellt zu
  werden. **D169 ist damit negativ beantwortet:** `resolve_state` löst die Ununterscheidbarkeit von
  Epoche-1- und Epoche-2-Policy nicht, es verschiebt sie. Die beiden Verfassungen des
  Beispielnukleus unterscheiden sich in genau einem Feld, `participants`.
- **D189** — Abnahme `00i`.
- **D190** — Die Welt entsteht in `tests/`, nach dem Vorbild des `RepositorySimulator` aus
  `python-tuf`: ein Bauer im Speicher, nichts von Hand festgeschrieben. Der Beispielnukleus
  scheidet aus, weil `threshold_class` nur bei reiner `participants`-Änderung `membership`
  liefert und `build()` genau das prüft. Berichtigung an D186: `vote` nimmt seit jeher ein
  `scope`-Argument.
- **D191** — Abnahme `00j`, Schärfung von Prüfregel 28.

## Was diese Sitzung gelehrt hat

**Eine Probe kann mehr belegen als den Code, den sie prüft.** Probe A in `00j` hat in
`resolve_state` die Verfassung der geltenden Epoche gegen die des Genesis getauscht. Rot wurde
**nur** `tests/test_kettenwelt.py`; `tests/test_resolve.py` und `tests/test_example_nucleus.py`
blieben grün. Damit ist die Reglosigkeit der beiden älteren Prüfschichten nicht mehr eine Messung
des Supervisors, sondern am Artefakt vorgeführt.

**Ein reglos gebauter Test ist schlimmer als ein zirkulärer.** D184 hatte den Fassadentest als
zirkulär notiert. Die Nachmessung ergab, dass seine Behauptung in dieser Welt für jede beliebige
Verfassung wahr ist. Ein Umbau des Vergleichsaufrufs ändert daran nichts — es braucht eine andere
Welt.

**Der Prompt hat eine Welt vorgeschrieben, die es nicht geben kann.** Die Feldliste für `00j`
liess `irrevocable_predicates` weg. Ohne `vote@1` und `ratify@1` ist keine Auszählung evaluierbar
(`04 §3.5`, `GV-27`, `GV-31`) — die Kette wäre nie vorgerückt. Die Sondierwelt der Designrunde
hatte beide Einträge; sie gingen beim Abschreiben verloren. Daraus die Schärfung von Prüfregel 28.

**Ein toter Parameter ist ein Defekt, den kein Test sieht.** `now` stand in der Signatur des
Bauers und kam im Rumpf nicht vor, während die Tests den Wert daneben als Literal tippten. `ruff`
fängt das mit F401 und F811 nicht.

**Zwei Namen vom Werkzeug, beide richtig, beide gemeldet.** Prüfregel 29 zielt auf Namen in
Messkriterien, nicht auf Namen in Aufträgen. Deshalb ist daraus keine Regel geworden.

## Der nächste Schritt

**Die Ratifizierung in der dreiepochigen Welt — möglicher Produktivbefund.** Gemessen an einer
Welt mit drei Verfassungen (C1 ohne `nucleus_keys`, C2 mit `[B]`, C3 mit `[C]`, sonst identisch,
`irrevocable_predicates` überall mit `vote@1` und `ratify@1`):

- Ratifiziert **A** beide Übergänge, löst die Kette auf **Epoche 3** auf, `authorized_keys` ist
  Cs Schlüssel, alle Vermerklisten leer. Der Ratifizierer muss also **nicht** in
  `authorized_keys` stehen — `verify_ratification` prüft `ratify.I not in participants`.
- Ratifiziert **B** den zweiten Übergang, hält die Kette bei **Epoche 1** mit zwei
  `UNSUPPORTED_RATIFICATION`. Die beiden Welten sind bis auf den Autor eines Claims aus dem
  **zweiten** Übergang gleich, und trotzdem fällt auch der **erste**.

Das ist der Punkt, an dem diese Sitzung abgebrochen hat (Kreiselregel: zwei Anläufe am selben
Symptom, danach Schichtwechsel). Ungeklärt geblieben ist ausserdem ein Widerspruch in der eigenen
Diagnose: der Subjektabgleich löste die beiden Vermerke auf `vote@1`-Claims auf, während
`_unsupported` in `mensch_als_republik/governance/epoch.py` `claim_id(ratify)` als Subjekt setzt.
Eine der beiden Lesarten ist falsch.

**Vorgehen:** `04 §4.1` im Volltext lesen, `verify_ratification` vollständig lesen — nicht nur bis
Zeile 128 —, dann die Welt neu bauen und den Subjektabgleich sauber führen. Erst danach eine
Position. Es kann eine richtige Sperre sein, ein Diagnosefehler des Supervisors oder ein Defekt im
Produktivcode. Das Reproduktionsskript lag in `/tmp/w3.py` und ist nach einem Neustart weg; es ist
aus dem Kettenbauer in zwanzig Zeilen neu geschrieben.

**Der einfache der beiden D190-Fälle ist reif.** Fehlt die mittlere Verfassung, während die erste
und die dritte bekannt sind, hält die Kette bei Epoche 1 mit `TALLY_UNEVALUABLE` — das MaR-
Gegenstück zu `python-tuf` Nr. 2669, eine unbrauchbare Zwischenversion sperrt alle späteren
gültigen. Gemessen, ein Test, ein kurzer Lauf. Er hängt nicht am offenen Punkt oben.

**Der zweite D190-Fall ist neu zu formulieren.** Er war als „ein Schlüssel, den erst die neue
Epoche autorisiert" gedacht. Da der Ratifizierer nicht in `authorized_keys` stehen muss, trifft
diese Formulierung nicht. Was der Fall in MaR heisst, ist nach der Klärung oben zu entscheiden.

## Aufräumen

- **Drei Lauf-Branches dieser Sitzung** sind nicht gelöscht: `impl/00h-fassadentests`,
  `impl/00i-kettenpruefung`, `impl/00j-kettenwelt`. Alle drei sind als Fast-Forward in `main`
  enthalten, `git branch -d` sollte sie annehmen. Tier 1.
- **Vier ältere Branches** bleiben weiter liegen: `impl/02-trust-flow`, `impl/authoring`,
  `impl/autor`, `spec/02-vouch-weight-and-sybil-fix`. Gemessen in `00g`: `main..origin/<branch>`
  ist bei allen vieren leer, `git branch -D` ist gefahrlos, die Gegenstücke auf Gitea gehören
  mitgelöscht. Tier 1.
- **`ruff ARG`** — die Regelgruppe für ungenutzte Argumente hätte den `now`-Defekt maschinell
  gefangen. D182 hat den Linter bewusst auf F401 und F811 festgelegt; eine dritte Gruppe braucht
  denselben Nachweis: erst die Zahl der Funde im Baum messen, dann entscheiden.

## Offen

- **Die Ratifizierung in der dreiepochigen Welt** (siehe oben). Erster Punkt.
- **`check_resolved_chain` hat in `example-nucleus.md` keinen Abschnitt** (D189). Kurzer
  Spec-Nachzug.
- **Der zweite Fall aus D190** ist neu zu formulieren.
- **Der Ratifizierer-Knopf im Kettenbauer** — in `00j` ausdrücklich draussen gelassen, wird
  gebraucht, sobald der Punkt oben geklärt ist.
- **Vier `Finding`-Klassen, vier `dedupe_sort`** (D183): in `findings.py`,
  `governance/findings.py`, `profiles/findings.py`, `trust/findings.py`, strukturell identisch,
  nur im `kind`-Enum verschieden. Nicht anfassen, ohne die Frage zu stellen, ob die vier Enums je
  zusammengeführt werden sollen. D191 hat die Trennung gerade wieder gebraucht: sie ist der Grund,
  warum ein Vertauschen von `policy_findings` und `key_findings` überhaupt auffällt.
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173).
- **Die Sondierwelt in `test_benennung.py` erzeugt keine Vermerke** (D173).
- **`00` hält die Form seiner Vermerke nirgends fest** (D173).
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

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.
