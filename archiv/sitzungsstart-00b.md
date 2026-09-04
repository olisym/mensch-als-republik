# Sitzungsstart: 00b (MaR)

## Kontext

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

## Arbeitsweise

Die dauerhafte Anweisung gilt. **Die Prüfregeln stehen in `pruefregeln.md`** — 1 bis 25, im
Volltext, mit stabilen Nummern. Diese Datei wiederholt sie nicht. Wer eine Regel zitiert, zitiert
die Nummer. Neu seit der letzten Sitzung sind 24 und 25; beide kommen aus D160 und beide betreffen
den Supervisor, nicht das Werkzeug.

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
  **nie `and` innerhalb einer Pipe**. Eine Pipe auf `cat` oder `tail` hält die Kette am Leben, wo
  ein Zwischenschritt rot werden darf — sie maskiert aber auch einen roten Status. Wo der Status
  zählt (`check_specs.py`), in eine Datei umleiten und danach `tail` aufrufen, statt zu pipen.
- **Spec-Dateien als Download**, nicht als Copy-Block. Werkzeug-Prompts als Copy-Box oder, wenn
  lang, als Datei im Wurzelverzeichnis.
- **Hash-Test als erster Job.** Bei Ersetzungen zusätzlich `git diff --quiet -- <datei>`.
- Bei neuen Dateien `git add` **vor** `make check` / `check_specs.py`, sonst danach. `git add`
  mit expliziten Pfaden, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`. Zeilen brechen bei 100 Zeichen.
- **Der Vergleichspunkt eines Laufs ist der Prompt-Commit.** Liegt eine Spec-Änderung auf
  demselben Branch wie der Lauf, ist der Vergleichspunkt der Spec-Commit — sonst erscheinen
  nachgezogene Anker als Werkzeugarbeit.
- Claude darf `sha256sum` einer Projektkopie selbst rechnen und sie dann lesen statt anfordern.
  **Achtung:** die Projektkopien hinken dem Repo nach. Der Hashabgleich zu Sitzungsbeginn sagt,
  welche Dateien lesbar sind und welche angefordert werden müssen.

### Splices

Splices als Skript mit `assert`, dass der Anker genau einmal vorkommt, vorher trocken gegen eine
Kopie gelaufen. Die letzte Sitzung hat fünf Splices in Folge gefahren, alle im ersten Zug grün.
Was dafür gesorgt hat:

- **Jeder Splice läuft trocken gegen den Stand nach dem vorigen**, nicht gegen die Projektkopie.
  Eine Kette `dry` → `dry2` → `dry3` kostet nichts und fängt jeden Anker, den ein früherer
  Splice bereits verschoben hat.
- **Ans Register wird über eine Regex-Prüfung angehängt**, nicht über einen Prosa-Anker: der
  letzte Registerkopf muss der erwartete sein. Kein Zitat, keine Erinnerung.
- **Blöcke werden ersetzt, nicht Teilstrings geflickt.** Wo ein ganzer Registerschwanz neu
  geschrieben wird, ist `replace_to_end` ab der ersten Überschrift die billigste Form.
- **Zeilenlängen nach dem Trockenlauf prüfen**, und zwar nur die *neuen* Zeilen — der Bestand
  überlange Tabellenzeilen, gegen die jede naive Prüfung rauscht.
- Umlaute schreiben, nicht Umschrift. Ein Block in `ae`/`ue` fällt im Register sofort auf und
  kostet einen zusätzlichen Splice.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`.

**`main` liegt auf `a624b83`**, gepusht. Keine offenen Läufe. **526 Tests** plus **14**
Eigenschaftstests, kalt gemessen. Register **D1–D160**. Prüfregeln **1–25**. Die Zahlen beim
Sitzungsstart ablesen, nicht schätzen.

- **00** Nukleus, Genesis, Verfassung; seit `00a` mit `resolve_current_key` in
  `mensch_als_republik/keys.py` — dem ersten Produktivcode dieser Schicht.
- **01** Atom, Verifier, elf Reject-Codes, acht Zustände, `read_claim`.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`,
  `resolve_trust_params` als Herleitungsort der Kalibrierung.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung, Genesis-Bindung in `decide`.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests.

**Neu in der letzten Sitzung:** D150 bis D160, `mensch_als_republik/keys.py`,
`tests/nucleus/test_rotate_key.py`, `00 §5.4`, ein neu geschriebenes `00 §6.4`, Prüfregeln 24
und 25.

- **D150** — Die Governance-Rotation hatte keinen Träger. `00 §6.2` verlangte eine Payload, die
  weder das Vorschlagsobjekt (drei Felder) noch die Verfassung (vier Felder) aufnehmen konnte.
  Beschluss: fünftes normatives Verfassungsfeld `nucleus_keys`. Es **ersetzt** den Anker der
  Key-Chain, statt mit einem Kettenende verglichen zu werden — damit löst sich der Effektivpunkt
  aus `§6.4` Schritt 3 ersatzlos auf. `nucleus_keys = []` legt die Nukleus-Autorität still.
- **D151** — Zuschnitt: `00a` baut die Kette mit dem Anker als Parameter, `00b` den Anker selbst.
- **D152** — Die Gegenzeichnung ist `nuc:N/rotate-ack@1`, vierteilig nach dem Muster von D63.
- **D153** — `rotate-key@1` und `rotate-ack@1` sind Protokoll-Default irrevocable.
- **D154** — „Erster vollständiger Rotate" heißt: erster in der Autorenkette. Der aufgelöste
  Kopf kann unter Wissenszuwachs **zurückspringen**; dieselbe Klasse wie nachträglich entdeckte
  Equivocation. Ein defektes Kettenglied blockiert nichts.
- **D155** — Vier Belegungen: unvergleichbare Rotationen liefern keinen Kopf, der Zustand muss
  `ACTIVE` sein, `EXPIRED` zählt bei den Rotationsprädikaten mit, Zyklen liefern keinen Kopf.
- **D156** — Der Protokoll-Boden galt nur mit Policy. `is_irrevocable(p, None)` gab `False`
  zurück, bevor es irgendetwas prüfte — das Schulden-Lösch-Loch aus D57 eine Ebene höher.
- **D157** — Die `03`-Anker zur wirksamen Menge werden nachgezogen, die Tests nicht von ihnen
  gelöst. Erteilte Prompt-Dateien behalten ihre Zahlen und bekommen eine Hinweiszeile.
- **D158** — Berichtigung von D152s Begründung: der Widerrufsvektor ist wegen
  `FOREIGN_LIFECYCLE` nicht konstruierbar, der tragende Vektor ist die Quittung aus D63.
- **D159** — M-5, C-1 und C-9 aus `01a` sind abgelöst; D156 trägt aus `00 §5.2`, nicht aus
  `01 §5.4.1`.
- **D160** — Abschluss `00a`, dazu die Prüfregeln 24 und 25.

**Die Anwendung bleibt ausdrücklich zurückgestellt.** Es gibt keine vier Menschen mit einem echten
gemeinsamen Anliegen, und `08 §2.2` verlangt genau das. Warten ist ein zulässiger Zustand; so tun
als ob nicht. Das ist ein benannter Zustand, kein Versäumnis — und keine Aufforderung, in der
nächsten Sitzung eine Gelegenheit zu erfinden.

## Das Aufnahmekriterium

Aus `08 §3`, vor jedem neuen Mechanismus:

> **Senkt er die Kosten dafür, festzustellen, wer was gesagt hat — oder verteilt er Macht?**
> Senken: Protokoll. Verteilen: Policy. Keines von beidem: Werkzeug.

Die **Bestandstabelle** darunter ist mehr wert als das Kriterium allein: sie führt bereits
„Schwellenwerte, Arbitratorenlisten, Ressourcengrenzen" unter Policy. In D150 hat genau diese
Zeile die Entscheidung getragen — `arbitration.arbitrators` ist eine Autoritätsliste in der
Verfassung, `nucleus_keys` ist dieselbe Bauform.

## Was die letzte Sitzung gelehrt hat

**Der Supervisor war fünfmal die Fehlerquelle, das Werkzeug null mal.** Ein unerfüllbares
Nicht-Ziel, zwei Begründungen, die den Beschluss nicht trugen, eine mehrdeutig beschriebene
Testlage und ein `classify_all`-Aufruf ohne Policy im Prompt. Das Werkzeug hat jeden Fall
gemeldet statt still zu reparieren — auch den, den es umgehen musste, um den Auftrag überhaupt
auszuführen. Das ist die Bedingung, unter der ein falscher Prompt billig bleibt, keine Erlaubnis,
ihn falsch zu schreiben.

**Zwei Begründungen trugen nicht, beide Beschlüsse schon.** Das ist Prüfregel 25 und der
teuerste Fehlertyp dieser Sitzung: eine ungeprüfte Begründung sieht aus wie eine geprüfte und
fällt erst auf, wenn eine Messung widerspricht. Beide Male stand die richtige Stelle einen
Absatz weiter.

**Ein rotes `make check-all` war der beste Ausgang des Laufs.** Die drei roten Bestandstests aus
`01a` waren kein Kollateralschaden, sondern die Stelle, an der D156 auf eine ältere Entscheidung
traf. Hätte das Werkzeug sie angepasst, wäre der Konflikt unsichtbar geblieben.

**Ein Vektor mit zwei Ausschlussgründen misst keinen davon.** Der Gegenvektor zu D159 lief zuerst
über `vouch@1` — nicht im Boden **und** trust-gewährend. Heute wirkt nur der erste Grund, aber
der Test bliebe grün, wenn sich das änderte. Dieselbe Klasse wie Prüfregel 23.

**Der Vergleichspunkt eines Laufs kann der Spec-Commit sein.** Lag die Spec-Änderung auf dem
Implementierungs-Branch, zeigt ein Diff gegen den älteren Stand nachgezogene Anker als
Werkzeugarbeit. Beim Anfordern des Diffs die Basis nennen.

## Der nächste Schritt

**`00b`.** Zwei Grenzen aus D160 und eine offene Frage, in dieser Reihenfolge zu entscheiden.

Was feststeht:
- Der Anker ist die Menge `nucleus_keys` aus der Verfassung der **jüngsten ratifizierten Epoche**,
  sonst `genesis.root_keys` (D150). Die Epochenkette ist über `predecessor` total geordnet und
  uhrfrei; es wird kein Effektivpunkt verglichen.
- `resolve_current_key` nimmt den Anker als Parameter und behält ihn (D151). Der Herleitungsort
  ist ein eigener Ort, dieselbe Naht wie `resolve_policy` und `resolve_trust_params`.

Was offen ist und vor dem Prompt entschieden werden muss:
1. **Wer `authorized_keys` füllt.** `03 §4` bekommt die Menge weiterhin von außen; kein
   Produktivpfad verbindet sie mit der Kette (D160). Der Anschluss ist die eigentliche Wirkung
   von `00b` — ohne ihn ist auch `00a` folgenlos.
2. **Ob eine außerhalb der Rotationen gespaltene Autorenkette die Wurzel entwertet.** `§6.4`
   Schritt 3 sagt „die Kette", `§6.3` definiert nur den Rotationsfall. Heute sieht `_head_from`
   nur equivozierte Rotationen.
3. **Die Wohlgeformtheit von `nucleus_keys`.** `00 §5.4` hält fest, dass die leere Liste die
   Autorität stilllegt. Was ein nicht-`bytes32`-Eintrag tut, ist nicht entschieden — Kandidat
   für dieselbe Bewegung wie D70 und D37: der defekte Eintrag fällt weg, nicht die Aussage.

**Vor dem Prompt zu lesen:** `00 §5.4` und `§6.4` im Volltext, `governance/epoch.py` (welche
Funktion die jüngste ratifizierte Epoche liefert — und ob es sie gibt), `profiles/membership.py`
und `03 §4` für die Naht, `keys.py` im Volltext.

## Offen

- **`00b`** — siehe oben. Punkte 1 bis 3.
- **Eine Schwelle für `nucleus_keys`.** D126 ließ offen, ob ein Nukleus statt „einer genügt"
  ein `k`-von-`n` verlangen können soll; D149 verortete die Frage in der Verfassung. Seit
  D150 gibt es dort das Feld, an dem die Schwelle hinge. Erster Kandidat bleibt
  `example-nucleus.md` mit seiner 1-von-2-Autorität.
- **47 gemergte Branches** liegen auf `main` auf. Löschung ist Tier 1 und schadet nichts, solange
  sie liegen bleiben.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut.
- **`genesis[4]` ist an die Epochenkette nicht gebunden.** `GV-24` führt ein Genesis, dessen
  deklarierte Verfassung in der Auszählung nirgends vorkommt.
- **`D >= C₀` ist ein SHOULD** in `00 §4.0` und `02 §8` und wird nirgends geprüft (D147).
- **`anchor_set` (`genesis[3]`) bleibt ungebunden**, als benannte Grenze nach TUFs Trennung
  zwischen Trust Anchor und abgeleitetem Parameter (D147).
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
