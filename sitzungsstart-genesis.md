# Sitzungsstart: Genesis (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 23, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer.

Was in der Praxis am häufigsten gebraucht wird:

- **Design vor Code.** Alle Forks und Zahlen stehen fest, bevor ein Prompt geschrieben wird.
  **Modulcode vor Prompt** — alle betroffenen Quellen lesen, bevor ein Prompt entsteht.
- **Der Bericht des Werkzeugs ist nie die Abnahme.** Geprüft wird der Diff.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt — auch dir
  selbst aus der vorigen Runde.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: nur `cbor2` und `cryptography`, unter `dev` `pytest` und `hypothesis`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`,
  **nie `and` innerhalb einer Pipe**. `grep -c` mit Ergebnis null gibt Status 1 und bricht die
  Kette — das ist nutzbar, muss aber angesagt werden. Eine Pipe auf `cat` oder `tail` hält die
  Kette am Leben, wo ein Zwischenschritt rot werden darf.
- **Spec-Dateien als Download**, nicht als Copy-Block. Werkzeug-Prompts als Copy-Box oder, wenn
  lang, als Datei.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet -- <datei>`.
- Bei neuen Dateien `git add` **vor** `make check` / `check_specs.py`, sonst danach. `git add`
  mit expliziten Pfaden, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. Zeilen brechen bei 100 Zeichen.
- **Der Vergleichspunkt eines Laufs ist der Prompt-Commit.**
- Claude darf `sha256sum` einer Projektkopie selbst rechnen und sie dann lesen statt anfordern.
  **Achtung:** die Projektkopien hinken dem Repo nach. Der Hashabgleich zu Sitzungsbeginn sagt,
  welche Dateien lesbar sind und welche angefordert werden müssen.

### Splices

Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher trocken gegen die
Projektkopie gelaufen. Zwei Bauformen haben sich in der letzten Sitzung bewährt und zwei sind
gescheitert:

- **Anhängen ans Register braucht keinen Prosa-Anker.** Die tragende Vorbedingung ist, welcher
  Registereintrag zuletzt steht; `append_after_last_entry(path, "D149", text)` prüft sie per
  Regex über die Ueberschriftenzeilen des Registers und kommt ohne Zitat aus. Ein
  Prosa-Endanker prüft nur, ob der Autor
  einen Satz richtig erinnert — er ist zweimal gescheitert.
- **Absätze werden als Block ersetzt, nicht als Teilstring geflickt.** Drei Anläufe an einem
  Zeilenumbruch waren einer zu viel; die Blockersetzung mit fertig umbrochenem Ersatztext geht
  im ersten Zug.
- **Eine selbst getippte Ankerzeile prüft den Anker nicht.** Wer für den Trockenlauf die
  Schlusszeile der Datei von Hand nachbaut, testet seine Erinnerung gegen sich selbst.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`.

**`main` liegt auf `0ca0fd9`**, gepusht (der Commit dieser Datei kommt darüber). Keine offenen
Läufe. **508 Tests**, dazu die Eigenschaftstests unter `MAR_HYPOTHESIS=voll`. Register
**D1–D149**. Die Zahlen beim Sitzungsstart ablesen, nicht schätzen.

- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`, seit D147 mit
  `resolve_trust_params` als Herleitungsort der Kalibrierung.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung; seit D145 mit
  Genesis-Bindung in `decide`.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests.

**Neu in der letzten Sitzung:** D145 bis D149, `tests/governance/test_genesis_bindung.py`,
`tests/trust/test_kalibrierung.py`, `resolve_trust_params`, `02 §8.1`, Prüfregeln 22 und 23.

- **D145** — `decide` las `genesis_obj[5]` und `[6]`, ohne die Bindung an `epoch.scope`
  nachzurechnen. `04 §3` nennt den allgemeinen Satz („Objektidentitäten vor jedem Zugriff auf
  ihren Inhalt"), die Aufzählung darunter führt nur die Verfassungen, und der Code folgte der
  Aufzählung — Prüfregel 18. Beschluss: `ValueError`, Begründung aus `03 §1.2`. `GV-24` und
  `GV-29` konstruierten eine nach dem Beschluss unmögliche Lage; Konstruktion geändert,
  Erwartungswerte nicht.
- **D146** — Prüfregel 22 (ein Bezeichner im Prompt ist ein Zitat), dazu ein dritter Beleg für
  Regel 14 und deren Zusatz: ein Limit, das exakt erreicht wird, ist ein Nulltreffer.
- **D147** — Herleitung der Kalibrierung. `TrustParams` war feldgleich mit `genesis[9]`, ohne
  Abgleich, obwohl D35 Unveränderlichkeit von `D` verlangt. `resolve_trust_params` trägt die
  Bindungsprüfung; `derive`, `trust` und `rank` bleiben parametrisiert — dieselbe Naht wie
  `resolve_policy` in `03 §1.2`. Fünf Lagen als Tabelle in `02 §8.1`.
- **D148** — Prüfregel 23: die Rücknahmeprobe setzt an der ungeschützten Seite an.
- **D149** — Design-Runde `00a`. Die Schwellenfrage war bereits in `00 §7` verortet; Literatur-
  tabelle im Eintrag, damit TUF, TAP 8, did:plc und die Soft-Fail-Debatte nicht erneut gesucht
  werden. Verweiskorrektur in `00 §7` mitgenommen.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.

## Das Aufnahmekriterium

Aus `08 §3`, vor jedem neuen Mechanismus:

> **Senkt er die Kosten dafür, festzustellen, wer was gesagt hat — oder verteilt er Macht?**
> Senken: Protokoll. Verteilen: Policy. Keines von beidem: Werkzeug.

Die **Bestandstabelle** darunter ist mehr wert als das Kriterium allein: sie führt bereits
„Schwellenwerte, Arbitratorenlisten, Ressourcengrenzen" unter Policy. In der letzten Sitzung hätte
ein Blick in die Tabelle eine lange Herleitung erspart.

## Was die letzte Sitzung gelehrt hat

**Der Supervisor war fünfmal die Fehlerquelle, das Werkzeug null mal.** `passed()` statt
`reached()`; ein Importeur von `_tally`, es waren zwei; eine Rücknahmeprobe an der hashgebundenen
statt der ungeschützten Seite; ein Endanker aus dem eigenen Entwurf rekonstruiert; drei Anläufe
an einem Zeilenumbruch. Jedes Mal hat das Werkzeug korrekt gemeldet statt still zu reparieren.
Das ist die Bedingung, unter der ein falscher Prompt billig bleibt — keine Erlaubnis, ihn falsch
zu schreiben.

**Die teuerste Stelle war keine davon.** `00 §7` beantwortet die Frage, ob eine Autoritätsschwelle
ins Protokoll gehört, in einem Absatz — und der Supervisor hat sie über eine `08 §3`-Prüfung und
drei Literaturrecherchen neu hergeleitet, obwohl `§6` und `§7` als gelesen geführt wurden.
Prüfregel 22 deckt Bezeichner ab, nicht übersprungene Abschnitte. **Ob das eine eigene Regel
braucht, ist offen und beim nächsten Vorfall zu entscheiden** — zweimal derselbe Fehlertyp war
bisher das Kriterium.

**Rot ersetzt das Lesen nicht.** Die Rücknahmeprobe zu D147 wurde rot und sah bestätigt aus; die
Meldung nannte einen Bestandsanker, also einen Test, den es vorher schon gab. Die Diagnose stand
in der Meldung.

**Eine Messung, die nicht trifft, ist mehr wert als eine, die bestätigt.** Auftrag 4 zu D147
sollte nur eine Übereinstimmung melden und hat gezeigt, dass `genesis_gov` keinen Schlüssel 9
trägt — `00 §4.2` korrekt gefolgt, ohne dass es je jemand geprüft hatte.

## Der nächste Schritt

**`00a-rotate-key` / D62.** Nach D149 ist der Lauf deutlich kleiner als vor der Design-Runde.

Was feststeht:
- `resolve_current_key(N)` liefert eine **Menge**. `∈` ist für jede Mächtigkeit definiert
  (`00 §7`).
- Jede Rotation ersetzt den Schlüssel **ihres eigenen Autors**. Bei `|root_keys| = 2` gibt es
  zwei parallele Ketten, deren Köpfe beide in der Menge landen. Es ist **keine** Auswahl zwischen
  konkurrierenden Ketten zu treffen; Konkurrenz innerhalb einer Wurzel ist Equivocation und
  gehört Layer 01.
- `J = [identity, K_n]` ist korrekt. Die Gegenzeichnung bleibt ein einzelner Claim.
- Eine Autoritätsschwelle ist ein **Verfassungsknopf**, nicht Teil von `00a` (D149).

Was offen ist und vor dem Prompt entschieden werden muss:
1. **Die Belegung des Gegenzeichnungsprädikats** (D125). `00 §6.1` sagt „ein Claim `C` mit
   `C.I == K_n`, der die `claim_id` des Rotate nennt" — welche Feldbelegung? `J = [claim-ref,
   claim_id(R_n)]` liegt nahe. Ob `C.N` gebunden sein muss, ist offen; ohne Bindung zeichnet
   eine Gegenzeichnung aus Nukleus A eine Rotation in Nukleus B gegen — dieselbe Fehlerform wie
   D63s dritte Bedingung.
2. **Der Effektivpunkt der Governance-Rotation** (`00 §6.4` Schritt 3). Vergleicht heute eine
   Governance-Größe mit einer Position in einer Autorenkette; über `t` ist das nach `01 §5.3`
   verboten. Der uhrfreie Weg — die Rotation nennt den ersetzten Schlüssel oder die `claim_id`
   explizit — ist vorgeschlagen, nicht entschieden.
3. **Was ein defektes Kettenglied tut.** `§6.4` sagt „folge der längsten Kette" und schweigt
   dazu. Die TUF-Referenzimplementierung hatte hier einen realen Betriebsschaden: eine einzige
   ungültige Version blockierte alle folgenden dauerhaft.

**Vor dem Prompt zu lesen:** `parse_grant_membership` in `03`, der Schlüsselpfad in `04 §5`
(Zeile 459), und `00 §6.4` im Volltext. Layer 00 hat **keinen** Produktivcode — `root_keys`,
`key_mode`, `anchor_set`, `vote_mode` und `parent_scope` haben keinen Träger im Paket. `00a` ist
damit der erste Code, der ein Genesis-Feld außerhalb von `[4]`, `[5]`, `[6]` und `[9]` anfasst.

## Offen

- **`00a-rotate-key` / D62**, D125, D126, D149. Siehe oben.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut.
- **`genesis[4]` ist an die Epochenkette nicht gebunden.** `GV-24` führt ein Genesis, dessen
  deklarierte Verfassung in der Auszählung nirgends vorkommt. Aus D145/D147 mitgenommen.
- **`D >= C₀` ist ein SHOULD** in `00 §4.0` und `02 §8` und wird nirgends geprüft (D147).
- **`anchor_set` (`genesis[3]`) bleibt ungebunden**, als benannte Grenze nach TUFs Trennung
  zwischen Trust Anchor und abgeleitetem Parameter (D147).
- **`example-nucleus.md` führt eine 1-von-2-Autorität** — Bruno und Anna dürfen jeder allein als
  der Nukleus handeln. Zulässig nach `00 §7`, und der erste Kandidat für den Verfassungsknopf
  (D149).
- **`TrustParams.__post_init__` und `00 §4.0`** prüfen dieselbe Wohlgeformtheit in eigener
  Formulierung. Heute einig, nicht zusammengelegt (D147).
- **`disjoint_paths` bewegt sich nicht** (bleibt `1` in allen gemessenen Fällen).
- **`make check` steigt in `.venv` ab:** `find . -name __pycache__ -type d -exec rm -rf {} +`
  ohne `-not -path "./.venv/*"`.
- **Ausgang 5 / Selbst-Equivocation.** Entschieden: nicht im Einlesepfad, kein zwölfter
  Reject-Code. Offen bleibt der Ort (D127).
- **`FOREIGN_LIFECYCLE` hat keinen Produktivträger mehr** (D138, bewusst).
- **Meldung übersprungener Claims aus `store_laden`** — von D138 zurückgestellt.
- **`03-prompt.md`-Verweise im Paketcode** — vier Stellen unter `mensch_als_republik/profiles/`
  und `policy.py`. Nach Prüfregel 17 doppelt relevant.
- **Gleichstand bei `kante_claim_id`** — der Bruch über `sorted(...)[0]` ist von nichts geprüft.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** prüfen eine schwächere Aussage als sie
  scheinen (D117).
- **Dreifache Kantensumme in `test_deckenelastizitaet.py`** (D142, notiert, nicht blockierend).
- **`02d-purpose`** (D56), **VR-04.1** (D26), **Zeugenquorum für Fristen** (D100).
- **`04 §7.2` Föderation** nicht durchgerechnet.
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **`example-nucleus.md`** unvollständig.
- **Layer 05.** Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf) und die
  Beta-Reputation mit dem Moral-Licensing-Problem.
- **Die Anwendung.** Wartet auf Menschen. Siehe oben.
