# Sitzungsstart: 00g (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 29, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu ist **29** (aus D184). Sie steht neben **22**, **26**, **27** und **28**: fünf
Regeln, die sich an den Supervisor richten, keine an das Werkzeug.

Was in der Praxis am häufigsten gebraucht wird:

- **Design vor Code.** Alle Forks und Zahlen stehen fest, bevor ein Prompt geschrieben wird.
  **Modulcode vor Prompt** — alle betroffenen Quellen lesen, bevor ein Prompt entsteht. In dieser
  Sitzung hat erst das Lesen der Signaturen den eigentlichen Fork sichtbar gemacht (F6, drei
  verschiedene `Finding`-Typen); die drei zuvor bestätigten Forks waren die leichteren.
- **Der Bericht des Werkzeugs ist nie die Abnahme.** Geprüft wird der Diff. Diese Sitzung hat
  einen Defekt gefunden, den kein Test und kein Prompt-Kriterium gesehen hätte.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt — auch dir
  selbst. Diese Sitzung hat eine eigene Begründung aus D183 nach der Messung zurückgenommen.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis` und —
  seit D182 — `ruff`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende ist
  die nützliche Ausnahme.
- **Spec-Dateien als Download**, nicht als Copy-Block. Werkzeug-Prompts als Copy-Box oder, wenn
  lang, als Datei im Wurzelverzeichnis.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet -- <datei>`.
- Bei neuen Dateien `git add` **vor** `make check`, sonst danach. Explizite Pfade, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. Zeilen brechen bei 100 Zeichen; Tabellenzeilen
  sind ausgenommen. `check_specs.py` prüft Escapes, Steuerzeichen, D-Nummern und hängende
  D-Verweise — **keine Zeilenlängen**.
- **Der Vergleichspunkt eines Laufs ist der Prompt-Commit.** Ein Prompt kann den Commit, der ihn
  enthält, nicht nennen — er nennt den Branchpunkt. Spec-Nachzug gehört **vor** den Lauf auf
  `main`. Läuft ein Branch bereits, wird `main` in ihn gemergt.
- Claude darf `sha256sum` einer Projektkopie selbst rechnen und sie dann lesen statt anfordern.
  **Prüfregel 26:** dieser Abgleich gilt für den Commit, an dem er gemacht wurde. In dieser
  Sitzung war die Projektkopie bei `d75a499` gültig; danach waren alle Diffs bekannt, deshalb
  blieb sie brauchbar.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie mit selbstgebautem `grep`.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Zählvorschriften, die tragen** (die aus `00e` war falsch):
  - Registerköpfe: `grep -c '^### D' 07-decisions.md` → **184**. Die Regex-Prüfung im Splice
    zählt `^### D([0-9]+) — ` und liegt um **zwei** darunter (`D5a`, `D16 / D22`) → **182**.
  - Prüfregeln: `grep -cE '^\*\*[0-9]+\.' pruefregeln.md` → **29**. Die Regeln stehen als
    `**N. Titel.**`, der ganze Satz im Fettdruck. Ein Muster `\*\*[0-9]+\.\*\*` findet **null**.
- Vor jeder Zahl in einem Prompt: **ist sie gemessen, und ist die Messung noch gültig?**
- **Prüfregel 27:** vor jedem Verweis in einem Prompt die Stelle aufschlagen. Diese Sitzung hätte
  sonst `01 §4.1` als Prädikat-Grammatik zitiert; dort steht die Ordnung der `claim_id`. Die
  Grammatik ist `01 §2.2` mit Anhang A. Der falsche Verweis stand in der eigenen Übergabe.
- **Prüfregel 28:** ein Abnahmekriterium behauptet einen Weltzustand. Vor dem Prompt den Zustand
  konstruieren.
- **Prüfregel 29:** ein Grep-Kriterium verbietet Namen. Eng fassen — `def _is_nuc_name` statt
  `_is_nuc_name`.
- **Eine Zusage ist keine Messung.** Und: eine Kette aus mehreren `git log`-Aufrufen ohne Trenner
  liefert bei leerer Ausgabe keine unterscheidbare Aussage. Diese Sitzung hat die Branchdiagnose
  deshalb zweimal fahren müssen.
- Eine Auffälligkeit an einer Stelle ist erst ein Befund, wenn die Nachbarstellen dieselbe
  Erwartung erfüllen (Prüfregel 8).

### Splices

Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher trocken gegen eine
Kopie gelaufen. Diese Sitzung hat vier Splice-Läufe mit zusammen zehn Ankern gefahren, alle im
ersten Zug grün.

- **Jeder Splice läuft trocken gegen den Stand nach dem vorigen**, nicht gegen die Projektkopie.
- **Ein anhängender Splice braucht eine eigene Negativprüfung.** Jeder Anker bekommt eine Marke,
  die nach dem Einfügen im Text steht — bei D184 war es `berichtigt in D184` im Register und das
  Fehlen von `**29.` in `pruefregeln.md`.
- **Ans Register wird über eine Regex-Prüfung angehängt**: der letzte Registerkopf muss der
  erwartete sein.
- **Blöcke werden ersetzt, nicht Teilstrings geflickt.**
- **Zeilenlängen nach dem Trockenlauf prüfen**, nur die *neuen* Zeilen, in Zeichen.
- Umlaute schreiben, nicht Umschrift. Ein Skript in Umschrift wurde in dieser Sitzung verworfen
  und neu geschrieben.
- Die Splice-Skripte danach aus dem Wurzelverzeichnis **löschen**.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`.

Zum Ende dieser Sitzung: `main` bei `ff5a959`, gepusht. **567 Tests**. Register **D1–D184**,
Prüfregeln **1–29**. Keine offenen Läufe. Fünf lokale Branches: `main` plus die vier aus dem
Aufräumen (siehe unten).

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys` in
  `mensch_als_republik/keys.py`.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A; `is_nuc_name` in `predicates.py` ist ihre einzige Implementierung.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung, Genesis-Bindung in `decide`,
  `§4.5` Kettenauflösung.
- **Fassade** (`mensch_als_republik/resolve.py`): `resolve_state` und `NucleusState`, seit D183.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests.

**Neu in dieser Sitzung:** D180 bis D184, Prüfregel 29, `mensch_als_republik/resolve.py` mit
`tests/test_resolve.py`, `is_nuc_name` als einzige Fassung in `predicates.py`, `ruff` mit F401 und
F811 in `make check`, und 71 gelöschte Branches.

- **D180** — Der Aufrufer der Kettenauflösung ist der **Node**. Das steht seit `VISION §5` und
  `06 §2` und wurde hier nur benannt, nicht entschieden. Daraus folgt der Zuschnitt der Fassade:
  soviel, wie ein Node beim Empfang eines fremden Claims braucht. Die Gegenrichtung ist normativ —
  die Bibliothek darf den Node nicht kennen. Kein Pfad, kein Socket, kein Daemon.
- **D181** — `is_nuc_name` einmal, in `predicates.py`, ohne Unterstrich. Vorher sechs
  byte-identische Kopien und ein modulübergreifender Import. `except Exception` bleibt.
- **D182** — `ruff` unter `dev`, mit genau zwei Regeln: F401 und F811. Kein Formatter, kein E501.
- **D183** — Die Fassade `resolve_state`. Rückgabetyp `NucleusState` trägt die Invariante, dass
  Epoche, Verfassungsobjekt, Policy und `authorized_keys` aus derselben Kette stammen. Vermerke
  bleiben in drei getrennten Feldern.
- **D184** — Abnahme `00f`, Berichtigung an D183, Prüfregel 29.

## Was diese Sitzung gelehrt hat

**Das eigene Übergabedokument ist eine Quelle, die man nachmisst.** `00e` führte `_is_nuc_name` als
einen Import über eine Modulgrenze; gemessen waren es sechs Definitionen, 18 Vorkommen in sieben
Dateien. `00e` nannte `01 §4.1` als Benennungsregel; dort steht etwas anderes. `00e` gab eine
Zählvorschrift für die Prüfregeln an, die null liefert. Drei Fehler in einer Datei, die als
Wahrheit weitergereicht wird.

**Ein Abnahmekriterium kann vorschreiben statt messen.** Das Werkzeug hat gemeldet, dass es die
Testnamen nach dem Grep-Kriterium ausgerichtet hat. Daraus Prüfregel 29 — und der Hinweis, dass
das Werkzeug diese Art Rückwirkung sieht und benennt, wenn man es nicht daran hindert.

**Eine Rücknahmeprobe kann die Begründung widerlegen, nicht nur den Code prüfen.** Die Probe zu
D183 lief rot, aber aus einem anderen Grund als vorhergesagt: kein stiller Policy-Wechsel, sondern
ein `ValueError`. Damit war die Begründung des Registereintrags falsch, während die Entscheidung
richtig blieb. Das ist der Wert der Probe jenseits ihres Zwecks.

**Der Linter fängt eine Klasse, die der Supervisor nur durch Lesen fand.** Der tote `Claim`-Import
war der erste Werkzeugdefekt seit mehreren Sitzungen und zugleich der Anlass, ihn künftig
maschinell zu fangen. Die Messung vor der Entscheidung hat 16 Funde ergeben, keinen davon in
`mensch_als_republik/` — die Bibliothek war sauber, die Testschicht nicht.

## Der nächste Schritt

**Der zweite Ort der Verkettung.** D183 begründet sich damit, dass dieselbe Reihenfolge an zwei
Stellen steht. Eine davon ist jetzt `resolve_state`. Die andere ist `_member` in
`tools/example_nucleus.py` (Zeile 466 bis 484), die `resolve_authorized_keys` und `membership`
weiterhin selbst verkettet und `constitution_hash` samt Verfassungsobjekt als Parameter bekommt.
Solange sie das tut, ist der Befund nicht behoben, sondern verdoppelt.

**Zuerst messen, dann fragen.** Vor jeder Positionierung ist zu zählen, welche Stellen in `tools/`
die Verkettung nachbauen und welche davon überhaupt eine Kette haben — `_member` bekommt heute
`constitution_h` und `obj` von außen, und `check_anchor_resolution` prüft absichtlich verschiedene
Verfassungen gegeneinander. Nicht jede Stelle lässt sich umstellen, und eine erzwungene Umstellung
würde einen Test entwerten. **D169** ist dabei zu lesen: der Beispielnukleus kann Epoche-1- von
Epoche-2-Policy nicht unterscheiden. Ob `resolve_state` das löst oder nur verschiebt, ist eine
Messung, keine Meinung.

**Der zweite Kandidat.** Vier `Finding`-Klassen — in `findings.py`, `governance/findings.py`,
`profiles/findings.py`, `trust/findings.py` — sind strukturell identisch und unterscheiden sich nur
im `kind`-Enum; `dedupe_sort` steht dreimal mit gleicher Signatur daneben, ein viertes Mal in
`policy.py` über `PolicyNote`. Derselbe Befund wie D181, aber über vier Schichten. Er ist grösser
als er aussieht: eine Vereinheitlichung koppelt `00`, `02`, `03` und `04` aneinander, und D183 hat
die Trennung gerade erst als Information begründet. Nicht anfassen, ohne die Frage zu stellen, ob
die vier Enums je zusammengeführt werden sollen.

## Aufräumen

- **Vier Branches bleiben liegen**: `impl/02-trust-flow`, `impl/authoring`, `impl/autor`,
  `spec/02-vouch-weight-and-sybil-fix`. `git branch -d` verweigert sie, weil sie nicht mit ihrem
  `origin/`-Gegenstück zusammengeführt sind. **Gemessen:** `main..origin/<branch>` ist bei allen
  vieren leer — auf keinem Remote-Branch liegt Arbeit, die `main` nicht hat. `git branch -D` ist
  damit gefahrlos; die Gegenstücke auf Gitea gehören mitgelöscht. Tier 1.
- **`check-lint` ruft `.venv/bin/ruff` direkt auf**, während alles andere über `PY :=` läuft. Ein
  `RUFF := .venv/bin/ruff` wäre konsistent. Kosmetik, ein Zug.
- Die Ref-Liste der 75 Branches vor der Löschung lag in `/tmp/branches-vor-loeschung.txt` und ist
  nach einem Neustart weg. Kein Verlust — alle gelöschten waren in `main` enthalten.

## Offen

- **`test_resolve_state_authorized_keys_match_direct` ist schwächer als sein Name** (D184): er
  übergibt `policy=state.policy` an den Vergleichsaufruf.
- **`policy_findings` ist von keinem Test berührt** (D184).
- **Vier `Finding`-Klassen, vier `dedupe_sort`** (D183, siehe oben).
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173).
- **Die Sondierwelt in `test_benennung.py` erzeugt keine Vermerke** (D173).
- **`00` hält die Form seiner Vermerke nirgends fest** (D173).
- **`is_nuc_predicate` und `is_core_predicate` fangen `VerifierError`, `is_nuc_name` fängt
  `Exception`** (D181): drei Funktionen nebeneinander, zwei Fangbreiten.
- **Eine Schwelle für Autoritätslisten** — mit D166 zurückgestellt. Wird für `root_keys`,
  `nucleus_keys` und `arbitration.arbitrators` **zugleich** beantwortet oder gar nicht.
- **Darf ein Amendment ein deklariertes Prädikat weglassen?** Gehört an `04 §5` (D167).
- **Der Beispielnukleus kann Epoche-1- von Epoche-2-Policy nicht unterscheiden** (D169).
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
- **Braucht der Node eine eigene Beschreibung?** `06 §2` ordnet ihn ein, `VISION §5` beschreibt
  ihn als Infrastrukturthese. Was fehlt, ist die Frage, ob zwischen beiden etwas Normatives liegt —
  D180 sagt ausdrücklich nein und benennt ihn nur. Wenn diese Antwort einmal nicht mehr trägt,
  wird sie hier fällig.
- **Layer 05.** Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf), die Beta-Reputation
  mit dem Moral-Licensing-Problem — und seit D178 die Frage, ob wiederholtes Stimmen auf
  unveröffentlichte Vorschläge eine Folge tragen soll.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.
