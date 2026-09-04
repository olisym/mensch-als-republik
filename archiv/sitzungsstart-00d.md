# Sitzungsstart: 00d (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 27, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu ist **27** (aus D173). Sie steht neben **26** und **22**: alle drei richten sich
an den Supervisor, keine an das Werkzeug.

Was in der Praxis am häufigsten gebraucht wird:

- **Design vor Code.** Alle Forks und Zahlen stehen fest, bevor ein Prompt geschrieben wird.
  **Modulcode vor Prompt** — alle betroffenen Quellen lesen, bevor ein Prompt entsteht.
- **Der Bericht des Werkzeugs ist nie die Abnahme.** Geprüft wird der Diff. In dieser Sitzung war
  der Bericht in jeder Zelle zutreffend, und der Defekt stand trotzdem im Diff.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt — auch dir
  selbst aus der vorigen Runde. Diese Sitzung hat zweimal einen eigenen Entwurf zurückgenommen,
  beide Male vor dem Splice, beide Male billig.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: nur `cbor2` und `cryptography`, unter `dev` `pytest` und `hypothesis`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten**. **Nie `and` innerhalb einer Pipe** — eine Pipe auf `tail` hält die
  Kette am Leben, verschluckt aber den roten Status. Eine Ausnahme ist nützlich: `sha256sum -c`
  am Ende einer Pipe druckt `FAILED` je Datei, dort ist der Statusverlust unschädlich.
- **Spec-Dateien als Download**, nicht als Copy-Block. Werkzeug-Prompts als Copy-Box oder, wenn
  lang, als Datei im Wurzelverzeichnis.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet -- <datei>`.
- Bei neuen Dateien `git add` **vor** `make check` / `check_specs.py`, sonst danach. `git add`
  mit expliziten Pfaden, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. Zeilen brechen bei 100 Zeichen; Tabellenzeilen
  sind ausgenommen.
- **Der Vergleichspunkt eines Laufs ist der Prompt-Commit.** Ein Prompt kann den Commit, der ihn
  enthält, nicht nennen — er nennt den Branchpunkt (`git merge-base main <branch>`). Spec-Nachzug
  gehört **vor** den Lauf auf `main`, damit „die Spec steht" im Prompt erfüllbar ist. In dieser
  Sitzung ist das so gelaufen und hat getragen.
- Claude darf `sha256sum` einer Projektkopie selbst rechnen und sie dann lesen statt anfordern.
  **Prüfregel 26:** dieser Abgleich gilt für den Commit, an dem er gemacht wurde.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie mit selbstgebautem `grep`.
- Vor jeder Zahl in einem Prompt: **ist sie gemessen, und ist die Messung noch gültig?**
- **Prüfregel 27:** vor jedem Verweis in einem Prompt die Stelle **aufschlagen**. Auch wenn er
  aus dem eigenen Register stammt.
- Eine Auffälligkeit an einer Stelle ist erst ein Befund, wenn die Nachbarstellen dieselbe
  Erwartung erfüllen (Prüfregel 8). Diese Sitzung hat sie zweimal gebraucht: einmal richtig
  angewandt (fünf Stellen, zwei Regeln) und einmal versäumt (`00` und `04` nicht gegrept).

### Splices

Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher trocken gegen eine
Kopie gelaufen. Diese Sitzung hat zwei Splice-Läufe mit zusammen sechs Ankern gefahren, alle im
ersten Zug grün.

- **Jeder Splice läuft trocken gegen den Stand nach dem vorigen**, nicht gegen die Projektkopie.
- **Ans Register wird über eine Regex-Prüfung angehängt**: der letzte Registerkopf muss der
  erwartete sein. Das fängt auch eine veraltete Projektkopie.
- **Blöcke werden ersetzt, nicht Teilstrings geflickt.**
- **Zeilenlängen nach dem Trockenlauf prüfen**, nur die *neuen* Zeilen. Tabellenzeilen sind
  ausgenommen.
- Umlaute schreiben, nicht Umschrift.
- Die Splice-Skripte danach aus dem Wurzelverzeichnis **löschen**.
- Ein zweiter Lauf desselben Skripts muss an der Ankerprüfung scheitern, bevor etwas geschrieben
  wird. Das ist getestet und hat gehalten.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl. Die
Zahlen ablesen, nicht schätzen. `pytest` liegt im venv — `.venv/bin/python -m pytest -q`, das
System-Python hat es nicht.

Zum Ende dieser Sitzung: `main` bei `8a3c730`. **544 Tests** plus **14** Eigenschaftstests unter
`voll`. Register **D1–D173**, Prüfregeln **1–27**. Keine offenen Läufe, keine offenen Branches.

- **00** Nukleus, Genesis, Verfassung. `resolve_current_key` und `resolve_authorized_keys` in
  `mensch_als_republik/keys.py`, Vermerke in `mensch_als_republik/findings.py`.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim` — und seit dieser Sitzung
  `§4.1`, die Benennungsregel.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung, Genesis-Bindung in `decide`.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests.

**Neu in dieser Sitzung:** D172, D173, `01 §4.1`, Anwendungssätze in `02 §3.1` und `03 §6`,
`tests/trust/test_benennung.py`, ein Vektor in `tests/trust/test_groups.py`, Prüfregel 27.

- **D172** — Die Ordnung der `claim_id` **benennt**, sie **entscheidet nicht**. Fünf Stellen im
  Paket wählen aus gleichwertigen Claims einen aus, und sie zerfallen in zwei Regeln. Die
  Trennlinie ist die **Vertauschungsprobe**: ersetzt man den benannten Claim durch einen anderen
  der Kandidatenmenge, ist das Ergebnis byte-gleich, das benannte Feld ausgenommen. Hält sie, gilt
  die kleinste `claim_id`. Hält sie nicht, darf keine **abgeleitete** Ordnung wählen, sondern nur
  eine **deklarierte** — Verfassung oder Governance-Akt; sonst fällt die Aussage weg.
- **D173** — Abnahme `00c`, dazu die Berichtigung zu D171 und Prüfregel 27.

## Warum die Probe strukturell ist und nicht semantisch

Der erste Entwurf hätte als Kriterium gehabt, ob die Kandidaten „dasselbe sagen". Das verlangt
vom Atom ein Urteil über **Bedeutung** und bricht `01 §1 A2`. In `04 §3.1` geht der Satz durch, weil
er Prosa über einen benannten Fall ist; an der Basis wäre er ein Leitsatzbruch gewesen.

Die Literatur hat den Ersatz geliefert (Prüfregel 15). CRDT: das Multi-Value-Register behält alle
nebenläufigen Werte, das LWW-Register kollabiert sie über eine willkürliche Totalordnung und
verliert still Schreibvorgänge. Der gangbare Mittelweg ist ein mehrwertiger Zustand mit **einem**
willkürlich gewählten *angezeigten* Wert. Ethereums Fork-Choice bricht Gleichgewicht über die
höhere Blockwurzel und kann sich das nur leisten, weil eine getrennte Finalisierungsschicht den
Kopf revidiert; diese Schicht gibt es hier nicht. `did:plc` löst konkurrierende Operationen über
den **Index im deklarierten** Rotationsschlüssel-Array auf, nie über den Inhaltshash — und
braucht dafür zusätzlich ein Zeitfenster und ein zentrales Verzeichnis.

Die Mahlbarkeit trägt die Regel: die `claim_id`-Ordnung ist ein Nebenprodukt des Hashes, und wer
einen Schlüssel hält, mahlt, bis seiner der kleinere ist. Auf der Benennungsseite gewinnt er einen
Namen; auf der Entscheidungsseite gewänne er Autorität durch Rechenzeit.

## Das Aufnahmekriterium

Aus `08 §3`, vor jedem neuen Mechanismus:

> **Senkt er die Kosten dafür, festzustellen, wer was gesagt hat — oder verteilt er Macht?**
> Senken: Protokoll. Verteilen: Policy. Keines von beidem: Werkzeug.

Die **Bestandstabelle** darunter ist mehr wert als das Kriterium allein. D172 ist der Fall, in dem
kein neuer Mechanismus entstand: zwei laufende wurden aufgeschrieben. Ein Vermerk, der auf zwei
ehrlichen Knoten verschiedene Claims nennt, ist eine falsche Kollision — deshalb Protokoll.

## Was diese Sitzung gelehrt hat

**Der Supervisor war die Fehlerquelle, das Werkzeug nicht — vierte Sitzung in Folge.** Zwei
Fehler, beide vor oder im Prompt: ein semantisches Kriterium an der Basis, das A2 gebrochen hätte,
und ein Abschnittsverweis, der die Aussage nicht trägt.

**Ein Verweis, der einmal aufgeschrieben wurde, wird nicht mehr nachgemessen.**
`04-golden-anchors.md §8` hat vier Stationen durchlaufen: D170, D171, den `00c`-Prompt, den Lauf.
An keiner hat jemand die Datei aufgeschlagen. Das ist Prüfregel 27, und der Unterschied zu 26 ist,
dass dieser Verweis **nie** richtig war: kein Verfallsdatum, sondern eine Behauptung ohne Prüfung.

**Die Nachfrage des Operators hat den teureren der beiden Fehler gefunden.** „Vielleicht lohnt es
sich, noch einmal die Literatur zu vergleichen" kam, bevor ein Splice lief. Der Entwurf war
schlüssig zu lesen und trotzdem falsch — Schlüssigkeit ist kein Prüfmittel an der Basis.

**Eine Rücknahmeprobe kann zwei Tests unterscheiden.** Der Vektor prüft den Wert, die
Vertauschungsprobe die Norm. Bei `tied[-1]` wird der eine rot und der andere bleibt grün; bei
einer Sortierung nach `claim_id` umgekehrt. Wären beide in beiden Zeilen rot geworden, prüften sie
dasselbe, und eine der beiden Dateien wäre wertlos gewesen.

## Der nächste Schritt

**`resolve_authorized_keys` hat weiterhin keinen Produktivträger.** Das ist die größte benannte
Lücke von v1 und steht seit D160 unverändert: `03 §4` bekommt `authorized_keys` als externen
Parameter, und wer eine veraltete Menge übergibt, bekommt ein veraltetes Ergebnis. Rechenbar,
aber ohne Wirkung.

Der Anschluss hängt an der **Epochenkette** (D161): heute wird die Verfassung übergeben, nicht
hergeleitet. Beides ist ein Lauf oder zwei, und die Reihenfolge ist ein Fork, der vor dem ersten
Prompt zu entscheiden ist.

**Zwei kleine Kandidaten**, die als Beifang mitreiten können:

- `00` hält die Form seiner Vermerke nirgends fest. Die drei Schwestermodule zitieren ihre eigene
  Schicht (`02a §5`, `03-profiles.md §6`, `04-prompt.md §2`); nur das Nukleus-Modul kann das
  nicht.
- Der zweite Messpunkt für `SUBGRANULAR_VOUCH.subject` fehlt.

**Vor jedem Prompt zu lesen:** die Quellen, die er anfasst, im Volltext — und vorher prüfen, ob
der Hashabgleich für sie noch gilt. **Und jeden Verweis aufschlagen.**

## Offen

- **`resolve_authorized_keys` ohne Produktivträger** (D160) und **die ungebaute Epochenkette**
  (D161). Zusammen die größte Lücke.
- **`00` hält die Form seiner Vermerke nirgends fest** (D173).
- **`SUBGRANULAR_VOUCH.subject` ist ungeprüft** (D173): die Gleichstandsgruppe sitzt am Anker,
  dort wird `cap` nie null.
- **Die Sondierwelt in `test_benennung.py` erzeugt keine Vermerke** (D173). Der Vermerksvergleich
  läuft leer, und er vergleicht als Menge, nicht als Folge — Reihenfolge und Vielfachheit fallen
  weg. Bei leerer Menge folgenlos.
- **Eine Schwelle für Autoritätslisten** — mit D166 zurückgestellt, nicht erledigt. Wird für
  `root_keys`, `nucleus_keys` und `arbitration.arbitrators` **zugleich** beantwortet oder gar
  nicht.
- **Darf ein Amendment ein deklariertes Prädikat weglassen?** Heute entschützt es damit
  Bestandsclaims, unsichtbar bis zum Widerruf. Gehört an `04 §5` (D167).
- **Der Beispielnukleus kann Epoche-1- von Epoche-2-Policy nicht unterscheiden**, weil
  `constitution_2` in `irrevocable_predicates` mit `constitution_gov` übereinstimmt (D169).
- **`genesis[4]` und die Auszählung**: `GV-24` führt weiterhin ein Genesis, dessen deklarierte
  Verfassung in der Auszählung nirgends vorkommt.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut.
- **`D >= C₀` ist ein SHOULD** in `00 §4.0` und `02 §8` und wird nirgends geprüft (D147).
- **`anchor_set` (`genesis[3]`) bleibt ungebunden** (D147).
- **`TrustParams.__post_init__` und `00 §4.0`** prüfen dieselbe Wohlgeformtheit zweimal (D147).
- **`disjoint_paths` bewegt sich nicht** (bleibt `1` in allen gemessenen Fällen).
- **`make check` steigt in `.venv` ab:** `find . -name __pycache__ -type d -exec rm -rf {} +`
  ohne `-not -path "./.venv/*"`. Gehört mit einer Messung vorher und nachher gefahren.
- **Ausgang 5 / Selbst-Equivocation** — entschieden, aber der Ort ist offen (D127).
- **`FOREIGN_LIFECYCLE` hat keinen Produktivträger mehr** (D138, bewusst).
- **Meldung übersprungener Claims aus `store_laden`** — von D138 zurückgestellt.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** prüfen eine schwächere Aussage als sie
  scheinen (D117). Der Vorbehalt steht in `04-golden-anchors.md §8`.
- **Dreifache Kantensumme in `test_deckenelastizitaet.py`** (D142, notiert, nicht blockierend).
- **`02d-purpose`** (D56), **VR-04.1** (D26), **Zeugenquorum für Fristen** (D100).
- **`04 §7.2` Föderation** nicht durchgerechnet.
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **`example-nucleus.md`** unvollständig.
- **Gemergte Branches** liegen auf `main` auf. Löschung ist Tier 1 und schadet nichts, solange sie
  liegen bleiben. Zahl beim Sitzungsstart ablesen; zuletzt 71 plus `00c-benennung`.
- **Layer 05.** Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf) und die
  Beta-Reputation mit dem Moral-Licensing-Problem.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.
