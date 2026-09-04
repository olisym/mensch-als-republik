# Sitzungsstart: 00c (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 26, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu seit der letzten Sitzung sind **26** (aus D169) und ein **Zusatz zu 18** (aus
D165); beide betreffen den Supervisor, nicht das Werkzeug.

Was in der Praxis am häufigsten gebraucht wird:

- **Design vor Code.** Alle Forks und Zahlen stehen fest, bevor ein Prompt geschrieben wird.
  **Modulcode vor Prompt** — alle betroffenen Quellen lesen, bevor ein Prompt entsteht.
- **Der Bericht des Werkzeugs ist nie die Abnahme.** Geprüft wird der Diff.
- Die Spec ist normative Wahrheit, das Register ist die oberste Instanz. Der committete
  Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt — auch dir
  selbst aus der vorigen Runde. In dieser Sitzung ist das zweimal nötig gewesen und beide Male
  billig geblieben, weil es früh kam.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: nur `cbor2` und `cryptography`, unter `dev` `pytest` und `hypothesis`.
  Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. Ein Job pro Zeile, `and` am Zeilenanfang, nie `;`.
  Glob-Argumente **quoten** — `--include="*.py"`, sonst expandiert fish sie vorher und `grep`
  bricht ab. **Nie `and` innerhalb einer Pipe:** eine Pipe auf `tail` oder `cat` hält die Kette am
  Leben, verschluckt aber den roten Status. Das trifft vor allem **leere** Ergebnisse, und die
  sind oft der Befund.
- **Spec-Dateien als Download**, nicht als Copy-Block. Werkzeug-Prompts als Copy-Box oder, wenn
  lang, als Datei im Wurzelverzeichnis.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet -- <datei>`.
- Bei neuen Dateien `git add` **vor** `make check` / `check_specs.py`, sonst danach. `git add`
  mit expliziten Pfaden, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. Zeilen brechen bei 100 Zeichen; Tabellenzeilen
  sind ausgenommen, ein Umbruch zerstört sie.
- **Der Vergleichspunkt eines Laufs ist der Prompt-Commit.** Ein Prompt kann den Commit, der ihn
  enthält, nicht nennen — er nennt den Branchpunkt (`git merge-base main <branch>`). Spec-Nachzug
  gehört **vor** den Lauf auf `main`, damit „die Spec steht" im Prompt erfüllbar ist.
- Claude darf `sha256sum` einer Projektkopie selbst rechnen und sie dann lesen statt anfordern.
  **Prüfregel 26:** dieser Abgleich gilt für den Commit, an dem er gemacht wurde. Jeder Merge, der
  eine Datei anfasst, entwertet ihn — die Kopie sieht danach unverändert lesbar aus.

### Messen

- **Zeilenzahlen mit `git diff --numstat`**, nie mit selbstgebautem `grep`. `grep -c "^+[^+]"`
  zählt hinzugefügte **Leerzeilen** nicht mit; in dieser Sitzung hat das eine Erwartung um zwölf
  Zeilen verfehlt.
- Vor jeder Zahl in einem Prompt: **ist sie gemessen, und ist die Messung noch gültig?**
- Eine Auffälligkeit an einer Stelle ist erst ein Befund, wenn die Nachbarstellen dieselbe
  Erwartung erfüllen (Prüfregel 8). D171 ist der Fall, in dem das gefehlt hat.

### Splices

Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher trocken gegen eine
Kopie gelaufen. Diese Sitzung hat acht Splices gefahren, alle im ersten Zug grün — bis auf einen,
der an der eigenen Längenprüfung hängenblieb und genau dafür da war.

- **Jeder Splice läuft trocken gegen den Stand nach dem vorigen**, nicht gegen die Projektkopie.
  Eine Kette `dry` → `dry2` → `dry3` kostet nichts.
- **Ans Register wird über eine Regex-Prüfung angehängt**: der letzte Registerkopf muss der
  erwartete sein. Kein Zitat, keine Erinnerung.
- **Blöcke werden ersetzt, nicht Teilstrings geflickt.**
- **Zeilenlängen nach dem Trockenlauf prüfen**, nur die *neuen* Zeilen, Tabellenzeilen
  ausgenommen.
- Umlaute schreiben, nicht Umschrift.
- Die Splice-Skripte danach aus dem Wurzelverzeichnis **löschen**. Liegen sie herum, verrauschen
  sie jeden `grep --include="*.py"`.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl. Die
Zahlen ablesen, nicht schätzen.

Zum Ende der letzten Sitzung: **542 Tests** plus **14** Eigenschaftstests unter `voll`, kalt auf
`main` gemessen. Register **D1–D171**. Prüfregeln **1–26**. Keine offenen Läufe, keine offenen
Branches.

- **00** Nukleus, Genesis, Verfassung. Seit `00a`/`00b`: `resolve_current_key` und
  `resolve_authorized_keys` in `mensch_als_republik/keys.py`, Vermerke in
  `mensch_als_republik/findings.py`.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy` — seit `03b`
  mit `constitution_hash` als Parameter.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung, Genesis-Bindung in `decide`.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests.

**Neu in der letzten Sitzung:** D161 bis D171, `mensch_als_republik/findings.py`,
`resolve_authorized_keys`, `tests/nucleus/test_anchor.py`, der Vektor `P-H`, Prüfregel 26 und der
Zusatz zu 18.

- **D161** — `resolve_authorized_keys` mit der Verfassung als **Parameter**, nicht aus der
  Epochenkette hergeleitet. Rückgabe `KeyResolution(keys, findings)`. Dieselbe Naht wie
  `resolve_policy` und `membership`.
- **D162** — Eine Spaltung der Autorenkette an **beliebiger** Stelle entwertet die Wurzel, nicht
  nur eine an einer Rotation. Der Diebstahl zeigt sich zuerst an gewöhnlichen Akten.
- **D163** — Ein gesetztes `nucleus_keys` fällt **nie** auf `genesis.root_keys` zurück. Sonst
  holte ein einziges formwidriges Byte die abgesetzten Wurzelschlüssel zurück.
- **D164** — Die lokal unbekannte Verfassung ist nicht „die Verfassung nennt kein Feld".
  Genesis-Rückfall **mit** Vermerk.
- **D165** — Abnahme `00b`. Dazu die Berichtigung, dass mein neuer `§6.4`-Satz enger war als
  der abgelöste: die Prüfung gilt für jedes Kettenglied, nicht nur für den Anker.
- **D166** — Autoritätslisten tragen **keine** Schwelle. Die Frage war falsch gestellt: es gibt
  drei solche Listen, und sie wird für alle drei zugleich beantwortet oder gar nicht. TUF
  entscheidet andersherum, und das steht im Eintrag.
- **D167** — Die Auflösungskette in `03 §1.2` hatte keinen Epochenschritt. `genesis[4]` bindet
  die Epoche 1; welche Fassung gilt, ist Parameter. `CONSTITUTION_HASH_MISMATCH` entfällt.
- **D168** — Ein Auflöser prüft, was er liest. `resolve_policy` prüft `genesis[4]` nicht mehr,
  weil es ihn nicht mehr liest. `P-E` und `P-G` nachgezogen.
- **D169** — Abnahme `03b`, dazu Prüfregel 26.
- **D170** — Die Prompt-Verweise im Paketcode, gemessen: sieben statt vier, fünf davon richtig.
- **D171** — Berichtigung zu D170: es gibt keine `INV-04`-Lücke. **Keine** Layer-Datei nennt ihre
  Invarianten; sie stehen in den `*-golden-anchors.md`. Die Trennung ist getragen und jetzt
  aufgeschrieben.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.

## Das Aufnahmekriterium

Aus `08 §3`, vor jedem neuen Mechanismus:

> **Senkt er die Kosten dafür, festzustellen, wer was gesagt hat — oder verteilt er Macht?**
> Senken: Protokoll. Verteilen: Policy. Keines von beidem: Werkzeug.

Die **Bestandstabelle** darunter ist mehr wert als das Kriterium allein. In D150 hat sie die
Entscheidung getragen, in D166 die Zurückstellung: es gibt keinen Nukleus, der die Schwelle
verlangt, und ein Mechanismus ohne Kollisionsdichte ist Spezifikationstiefe.

## Was die letzte Sitzung gelehrt hat

**Der Supervisor war siebenmal die Fehlerquelle, das Werkzeug null mal — dritte Sitzung in
Folge.** Zwei zu enge Sätze in der Spec, zwei falsch gemessene Zeilenzahlen, eine abgelaufene
Zählung, eine Aufzählung, die einen Fall mitriss, und ein Fehlschluss aus einer ungeprüften
Parallele. Das Werkzeug hat jeden Fall gemessen und gemeldet statt still zu reparieren.

**Der teuerste Fehlertyp war die abgelaufene Messung, nicht die falsche.** Eine falsche Zahl fällt
auf. Eine Zahl, die einmal richtig war, sieht richtig aus und bleibt es, bis jemand neu misst.
Prüfregel 26 kommt daher, und sie gilt auch für die offene Liste unten: „vier Stellen" stand
dort seit Monaten und waren sieben.

**Ein Satz, der einen älteren ersetzt, erbt dessen Geltungsbereich nicht von selbst.** Zweimal
passiert: `§6.4` Schritt 3 verlor beim Umschreiben die Kette, und eine Prompt-Aufzählung riss
einen Fall mit, für den sie nicht gedacht war. Der Zusatz zu Prüfregel 18 kommt daher.

**Ein Registereintrag, der einen Zug später widerlegt wird, ist billig.** D170 hat den nächsten
Schritt benannt, und der Versuch, ihn zu beginnen, hat den Fehler sofort gefunden. Teuer wäre die
umgekehrte Reihenfolge gewesen.

**Zufällige Harmlosigkeit ist keine Richtigkeit.** Der Defekt in `check_anchor_resolution` war
nicht messbar, weil beide Verfassungen des Beispielnukleus in `irrevocable_predicates`
übereinstimmen. Er war trotzdem falsch, und er stand ausgerechnet in dem Vektor, der die zwei
Epochen trennen soll.

## Der nächste Schritt

**Drei Docstring-Zeiger als Beifang** (D171). Sie brauchen keinen eigenen Lauf, sondern reiten
beim nächsten mit:

- `profiles/payload.py` → `03 §1.3` statt `03-prompt.md §3.1`
- `governance/findings.py` → `04-golden-anchors.md §8` statt `04-prompt.md §2`
- `mensch_als_republik/findings.py` → eine Zitatzeile für `dedupe_sort`, die heute fehlt

**Der erste eigene Kandidat ist der Gleichstand bei `kante_claim_id`.** Der Bruch über
`sorted(...)[0]` ist von nichts geprüft; ein Gleichstand ist konstruierbar, und ob er stabil
bricht, weiß heute niemand. Kleiner Lauf, klares Abnahmekriterium, und er kann die drei Zeiger
tragen.

**Vor jedem Prompt zu lesen:** die Quellen, die er anfasst, im Volltext — und vorher prüfen, ob
der Hashabgleich für sie noch gilt.

## Offen

- **Gleichstand bei `kante_claim_id`** — der Bruch über `sorted(...)[0]` ist ungeprüft.
- **Drei Docstring-Zeiger** (D171), Beifang des nächsten Laufs.
- **Eine Schwelle für Autoritätslisten** — mit D166 zurückgestellt, nicht erledigt. Wird für
  `root_keys`, `nucleus_keys` und `arbitration.arbitrators` **zugleich** beantwortet oder gar
  nicht. Anlass wäre der erste Nukleus mit mehr als einem Halter, der Diebstahl fürchtet.
- **Darf ein Amendment ein deklariertes Prädikat weglassen?** Heute entschützt es damit
  Bestandsclaims, unsichtbar bis zum Widerruf. Gehört an `04 §5` (D167).
- **Der Beispielnukleus kann Epoche-1- von Epoche-2-Policy nicht unterscheiden**, weil
  `constitution_2` in `irrevocable_predicates` mit `constitution_gov` übereinstimmt. Der
  Epochenschritt wird deshalb nur von `P-H` gemessen (D169). Ein zweiter Messpunkt bewegte die
  dokumentierten Hashes in `example-nucleus.md`.
- **Die Epochenkette bleibt ungebaut** (D161). Wer eine veraltete Verfassung übergibt, bekommt
  einen veralteten Anker.
- **`genesis[4]` und die Auszählung**: `GV-24` führt weiterhin ein Genesis, dessen deklarierte
  Verfassung in der Auszählung nirgends vorkommt.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut.
- **`D >= C₀` ist ein SHOULD** in `00 §4.0` und `02 §8` und wird nirgends geprüft (D147).
- **`anchor_set` (`genesis[3]`) bleibt ungebunden** (D147).
- **`TrustParams.__post_init__` und `00 §4.0`** prüfen dieselbe Wohlgeformtheit zweimal (D147).
- **`disjoint_paths` bewegt sich nicht** (bleibt `1` in allen gemessenen Fällen).
- **`make check` steigt in `.venv` ab:** `find . -name __pycache__ -type d -exec rm -rf {} +`
  ohne `-not -path "./.venv/*"`.
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
  liegen bleiben. Zahl beim Sitzungsstart ablesen.
- **Layer 05.** Über-Commitment als Stufe-3-Auslöser (D40, mit D118 scharf) und die
  Beta-Reputation mit dem Moral-Licensing-Problem.
- **Die Anwendung.** Wartet auf Menschen. Siehe oben.
