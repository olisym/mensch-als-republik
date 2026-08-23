# Sitzungsstart: 00p (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 36, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu sind **32** (wo eine Prüfung sitzt, ist eine eigene Gabel, D200), **33** (der
Prompt wird gegen den Spec-Satz gelesen, D201), **34** (eine Probe, die eine Prüfung entfernt,
belegt nicht ihren Ort, D201), **35** (eine Grenze auf zwei Schichten braucht auf jeder einen
Wächter, D203) und **36** (Erkennung oder Adresse, D205).

Was in dieser Sitzung am meisten getragen hat:

- **Selbst messen, im eigenen Baum.** Der Supervisor hat die Projektkopie entpackt, lauffähig
  gemacht und jeden Lauf vollständig nachgebaut, bevor ein Prompt entstand. Alle Abnahmezahlen,
  alle Rotmengen und alle Weltzustände in den Prompts waren vorher gemessen, nicht geschätzt. Das
  hat dreimal einen Prompt gerettet und einmal einen Defekt gefunden, den kein Bericht zeigte.
- **Der Bericht des Werkzeugs ist nie die Abnahme.** Vier Läufe, vier zutreffende Berichte, ein
  Defekt — und der lag im Prompt des Supervisors, nicht im Lauf. Gefunden wurde er beim Lesen des
  Diffs gegen den Spec-Satz, nicht beim Lesen des Berichts.
- **Die Spec hat oft schon geantwortet.** Zweimal hat eine Messung wie ein Loch ausgesehen und war
  eine benannte Grenze: `§4.5` hatte die weite Fassung von D194 längst entschieden. Vor jeder
  Diagnose den Abschnitt aufschlagen, der zuständig ist.
- **Literatur vor Bauen.** D200 hat python-tuf aufgeschlagen und dort den Präzedenzfall gefunden
  (Schritt 1.3 im Client-Workflow, GHSA-f8mr-jv2c-v8mg) — und zugleich den Grund, seine
  Signaturfassung **nicht** zu übernehmen, weil das Bedrohungsmodell sich nicht überträgt.
- **Widersprich dir selbst, sobald die Messung es verlangt.** In dieser Sitzung zweimal: die weite
  Fassung von D194 zurückgenommen (D203) und die angekündigte Wirkung der `ARG`-Reparatur
  berichtigt (D205, Prüfregel 36).
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: `cbor2` und `cryptography`, unter `dev` `pytest`, `hypothesis`, `ruff`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe**; `sha256sum -c` am Pipe-Ende und
  eine Pipe auf `tail` sind die nützlichen Ausnahmen.
- **Spec-Dateien und Splice-Skripte als Download**, nicht als Copy-Block. Werkzeug-Prompts als
  Datei, wenn sie lang sind.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet -- <datei>`.
- Bei neuen Dateien `git add` **vor** `make check`. Explizite Pfade, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. Zeilen brechen bei 100 Zeichen — das gilt für
  **Spec-Dateien und Prompt-Dateien im Wurzelverzeichnis**. Für Python gibt es **keine**
  Zeilenlängenregel; D205 hat das mit Zahlen entschieden und nicht wieder aufzumachen.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie geschätzt.
- **Zeichen zählen, nicht Bytes.** `awk length` zählt Bytes und meldet bei Umlauten falsch.
- **Zählvorschriften, die tragen:**
  - Registerköpfe: `grep -c '^### D' 07-decisions.md`.
  - Prüfregeln: `grep -cE '^\*\*[0-9]+\.' pruefregeln.md`.
  - Branches: `git branch -a | wc -l`.
- **Prüfregel 26 in der Praxis dieser Sitzung.** Die Projektkopie ließ sich vollständig entpacken
  und gegen ein Manifest aus 200 Prüfsummen halten. Sechs Abweichungen, alle erklärt: fünf leere
  `__init__.py`, denen der Extraktor einen Zeilenumbruch angehängt hatte, und
  `tests/profiles/test_credit.py`,
  das ohne abschließenden Zeilenumbruch endet. Danach war die Kopie für den ganzen Commit gültig
  und ersetzte jede Dateianforderung.
- **Der eigene Baum ist die stärkste Messung.** `pip install cbor2 cryptography pytest hypothesis
  ruff`, dann läuft die volle Reihe. Jede Rotmenge, jeder Weltzustand und jede Variante lässt sich
  vorher fahren. Das kostet den Operator keinen Zug.
- **Prüfregel 27**: vor jedem Verweis in einem Prompt die Stelle aufschlagen. **Prüfregel 33**:
  und dann den Satz danebenlegen, den der Prompt umsetzt — der Verweis kann stimmen und die
  Anweisung daneben liegen.
- **Prüfregel 28**: die Welt im Prompt ist Feld für Feld die gemessene Welt.
- **Prüfregel 30**: eine Variantenwelt sichert ihre eigene Voraussetzung. Das Werkzeug hat das in
  `00n` besser gemacht als der Entwurf: ein Helfer mit `assert fremd.pub not in
  C1["participants"]` statt einer stillschweigenden Annahme.

### Splices

Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher trocken gegen eine
Kopie gelaufen. Diese Sitzung hat sechs Splice-Läufe gefahren, alle sauber.

- **Jeder Splice läuft trocken gegen den Stand nach dem vorigen**, nicht gegen die Projektkopie.
- **Ein zweiter Lauf desselben Skripts muss scheitern.** Sechsmal gehalten.
- **Nur die neuen Zeilen auf Länge prüfen, nicht die ganze Datei.** Der Altbestand führt Zeilen
  über 100 Zeichen.
- **Blöcke werden ersetzt, nicht Teilstrings geflickt.** In dieser Sitzung wurde ein Absatz in
  `§4.5` vollständig ersetzt, weil seine Begründung nicht mehr galt.
- Umlaute schreiben, nicht Umschrift. Die Splice-Skripte danach löschen.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Die Zahlen ablesen, nicht schätzen. `pytest` liegt im venv —
`.venv/bin/python -m pytest -q`.

Zum Ende dieser Sitzung: `main` bei `827b597`, gepusht. **587 Tests**. Register **D1–D206**,
Prüfregeln **1–36**. **Drei Branches** (`main`, `origin/HEAD`, `origin/main`). Keine offenen Läufe.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys`.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`. Prädikat-Grammatik in
  `§2.2` und Anhang A.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung, `§3.5` mit der Subjektregel
  (D198). **`§4.1` trägt seit D200 die Bedingung 6**, **`§4.5` seit D203 die berichtigte
  Vermerksgrenze.**
- **Fassade** (`mensch_als_republik/resolve.py`): `resolve_state` und `NucleusState`.
- **Kettenbauer** (`tests/kettenwelt.py`), **Werkzeugschicht** (`werkzeuge.md`).
- **Linter**: `ruff` mit `ARG`, `F401`, `F811` (D205). `check-lint` ruft `ruff check` ohne eigene
  Select-Liste, die Gruppe aus `pyproject.toml` greift unmittelbar.

**Neu in dieser Sitzung:** D200 bis D206, drei Läufe (`00m` mit Nachlauf, `00n`, `00o`),
Prüfregeln 32 bis 36, Bedingung 6 in `04 §4.1`, die berichtigte Vermerksgrenze in `§4.5`,
Abschnitt `§5.1` in `example-nucleus.md`, `tests/governance/test_regierbarkeit.py`,
`tests/governance/test_vermerkweitergabe.py`, die dritte `ruff`-Gruppe.

- **D200** — Eine Zielverfassung, die keine Auszählung tragen kann, wird nicht Epochenverfassung.
  Geprüft am Übergang (`§4.1`), nicht in der Auszählung (`§3.5`), weil letzteres `UNEVALUABLE`
  meldete, wo `PASSED` gemessen ist. Enge Fassung: `participants` und die beiden
  Unwiderruflichkeiten. Ein Helfer `constitution_governable`, von beiden Seiten benutzt.
- **D201** — Abnahme `00m`. Der einzige Defekt lag im Prompt: der ValueError-Wächter stand hinter
  den Bedingungen 1 bis 5, wo die Spec ihn an keine Bedingung knüpft. Daraus Prüfregeln 33 und 34.
- **D202** — Der aufgelöste Zustand des Beispielnukleus hat einen Abschnitt. Die Reglosigkeit des
  Schlüsselsatzes wird darin benannt statt überspielt. Schließt D189.
- **D203** — Die Auszählungsvermerke gehen mit, wenn keine Epoche entsteht, und nur dann. Die weite
  Fassung wurde gemessen und **zurückgenommen**: `§4.5` hatte sie längst entschieden. Daraus
  Prüfregel 35.
- **D204** — Abnahme `00n`, kein Defekt.
- **D205** — `ARG` ja, Zeilenlänge nein, beides mit Zahlen. Drei `ARG`-Funde, null im
  Produktivcode; zwei davon deckten auf, dass `test_bootstrap_rows` fünf Ankerspalten führt und
  zwei prüft. Daraus Prüfregel 36.
- **D206** — Abnahme `00o`, kein Defekt.

## Was diese Sitzung gelehrt hat

**Wo eine Prüfung sitzt, entscheidet, was sie behauptet.** Bei D200 kosteten alle drei Varianten
genau einen Test. Die Zahl half nicht. Die Wahl fiel erst, als die erzeugten Vermerke nebeneinander
lagen: zwei Varianten meldeten `UNEVALUABLE`, wo `PASSED` gemessen war. Kosten entscheiden eine
Gabel nur, wenn sie sich unterscheiden.

**Ein Verweis kann stimmen und die Anweisung daneben liegen.** Prüfregel 27 prüft den Verweis. Der
Prompt zu `00m` zitierte `§4.1` korrekt und schrieb den Wächter trotzdem an eine Stelle, die die
Spec nicht nennt. Das Werkzeug setzte den Prompt korrekt um. Gefunden wurde es erst beim Lesen des
Diffs gegen den Spec-Satz.

**Eine Grenze kann von zwei Schichten gehalten werden.** Der erste Grenztest zu D203 blieb grün,
als die Weitergabe versuchsweise auf den tragenden Pfad gelegt wurde — `resolve_epoch` liest die
Vermerke dort gar nicht. Wer eine Grenze prüft, misst zuerst, wie viele Stellen sie halten.

**Nicht jede neue Behauptung ist ein Wächter.** Die `ARG`-Reparatur wurde als neuer Wächter
angekündigt und ist keiner: mit und ohne sie fallen bei falschem `n` dieselben fünf Fälle. Was sie
bewacht, ist etwas anderes — die Übertragung der Ankertabelle in den Test. Beides ist zulässig,
aber es ist nicht dasselbe, und der Registereintrag sagt welches.

**Gemeldete Unvollständigkeit ist billiger als eine unvollständige Messung.** Das Werkzeug konnte
zwei Proben in `00o` nur gegen eine Datei fahren und hat das gesagt. Der Supervisor hat sie
nachgefahren. Hätte das Werkzeug geschwiegen, wäre die Lücke unbemerkt in die Abnahme gegangen.

## Der nächste Schritt

**Die Form der Vermerke außerhalb von `04 §3.5`** (D173). D198 hat den Subjektbegriff an einem Ort
normativ festgehalten: das Subjekt benennt das zurückgewiesene Objekt. D200 und D203 haben ihn
zweimal angewandt und dabei zweimal gefunden, dass er trägt. In `00`, `01`, `02` und `03` ist er
**nicht** festgehalten — dort gibt es Vermerksarten, deren Subjekttyp nur aus dem Code hervorgeht.

Das ist der Punkt, an dem `08 §2.2` hängt: Vermerke sollen kollidieren können, und zwei Vermerke
kollidieren nur, wenn ihre Subjekte vom selben Typ sind und dieselbe Sache benennen. D172 hat genau
das schon einmal entschieden — derselbe Vermerkstyp mit verschiedenem Subjekttyp ist die falsche
Kollision.

**Vorgehen, und zwar messen vor entscheiden.** Zuerst eine Bestandsaufnahme im eigenen Baum: je
Layer die Zahl der Vermerksarten, und für jede, ob die Spec ihren Subjekttyp nennt. Erst wenn die
Zahlen liegen, ist zu entscheiden, ob das Layer für Layer geht oder ob ein gemeinsamer Abschnitt
die richtige Form ist. Der Ausgang ist offen; „ein Abschnitt je Layer, aus benanntem Grund" ist
ebenso zulässig wie ein gemeinsamer Ort.

**Der billige Nachzug daneben:** `is_nuc_predicate` und `is_core_predicate` fangen `VerifierError`,
`is_nuc_name` fängt `Exception` (D181). Drei Funktionen nebeneinander, zwei Fangbreiten. Messbar —
welche Ausnahmen können dort überhaupt austreten — und danach eine Entscheidung, kein Ermessen.

## Offen

- **Die Form der Vermerke ist außerhalb von `04 §3.5` nicht festgehalten** (D173). Erster Punkt.
- **`is_nuc_predicate` und `is_core_predicate` fangen `VerifierError`, `is_nuc_name` fängt
  `Exception`** (D181).
- **Wie weit die Regierbarkeitsprüfung reicht** (D200). Die vollständige Fassung prüfte auch die
  beiden erreichbaren Schwellenklassen, `membership` und die Klasse aus `genesis[5]`. Sie ist
  konstruierbar und kostet dasselbe, braucht aber `genesis_obj` als zweiten Parameter in `§4.1`.
  Zurückgestellt, bis ein Fall sie erzwingt — **nicht vorher aufmachen**.
- **`RATIFY_WITH_EXPIRY` und der Zeugenpfad tragen die Weitergaberegel ungeprüft** (D203). Von
  fünf Pfaden ohne Folgeepoche halten Prüffälle drei. Bewusste Wahl aus Verhältnismässigkeit.
- **Vergleiche gegen `dedupe_sort` sind für die Reihenfolge zirkulär** (D196).
- **Vier `Finding`-Klassen, vier `dedupe_sort`** (D183): strukturell identisch, nur im `kind`-Enum
  verschieden. Nicht anfassen, ohne die Frage zu stellen, ob die Enums je zusammengeführt werden.
  D191 und D200 haben die Trennung gebraucht.
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173).
- **Die Sondierwelt in `test_benennung.py` erzeugt keine Vermerke** (D173).
- **Eine Schwelle für Autoritätslisten** — mit D166 zurückgestellt. Wird für `root_keys`,
  `nucleus_keys` und `arbitration.arbitrators` **zugleich** beantwortet oder gar nicht.
- **Darf ein Amendment ein deklariertes Prädikat weglassen?** Gehört an `04 §5` (D167).
- **Der Beispielnukleus kann Epoche-1- von Epoche-2-Policy nicht unterscheiden** (D169). Von D188
  negativ beantwortet, in `§5.1` seit D202 ausdrücklich benannt. Ob es je gelöst werden soll, ist
  offen.
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
- **`example-nucleus.md`** weiterhin unvollständig, aber `§5.1` steht seit D202.
- **Braucht der Node eine eigene Beschreibung?** D180 sagt ausdrücklich nein.
- **Layer 05.** Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf), die Beta-Reputation
  mit dem Moral-Licensing-Problem — und seit D178 die Frage, ob wiederholtes Stimmen auf
  unveröffentlichte Vorschläge eine Folge tragen soll.

**Erledigt und nicht wieder aufzumachen:** die Zeilenlängenfrage für Python ist mit D205 verneint,
mit Zahlen, und bleibt es, solange die Zahlen so liegen. Die Frage nach einer dritten
`ruff`-Gruppe ist mit `ARG` beantwortet; eine vierte bräuchte denselben Nachweis von vorn.
`check_resolved_chain` hat seit D202 seinen Abschnitt. Der Fork aus D197 ist mit D200 entschieden.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.
