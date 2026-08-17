# Sitzungsstart: nach der Werkzeugschicht (MaR)

## Kontext

Wir arbeiten an **Mensch als Republik (MaR)**, einem dezentralen Koordinationsprotokoll.
Python-Referenzimplementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz
(`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

**Arbeitsweise:**
- Design vor Code. Alle Forks und Zahlen stehen fest, **bevor** ein Prompt geschrieben wird.
- Die Spec ist normative Wahrheit. Der committete Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: nur `cbor2` und `cryptography`. Unter `dev` zusätzlich `pytest` und
  `hypothesis`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish, kein Heredoc, verbunden mit **`and`** und nicht mit
  `;` — eine rote Prüfung muss die Kette anhalten.
- **Spec-Dateien werden als Download geliefert**, nicht als Copy-Block. Der Shell-Block setzt
  voraus, dass die Datei bereits im Repo-Wurzelverzeichnis liegt.
- **Bei neuen Dateien `git add` vor `make check`**, sonst danach. `check_tree.py` schlägt bei
  unversionierten Quelldateien fehl, und eine neue Datei ist zwangsläufig unversioniert.
- `git add` mit expliziten Pfaden, nie `-A`. `git stash push` mit Pfad greift nur bei getrackten
  Dateien — für Unversioniertes ist der Branchwechsel ohnehin unschädlich.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`.
- **Ein Implementierungslauf endet mit einem Commit auf einem benannten Branch**, nie mit
  "gestaged, nicht committet".

⚠️ **Dateien nie manuell editieren.** Spec-Dateien kommen vollständig von Claude. Vor einer
Ersetzung mitten in einer Datei per `sha256sum` abgleichen — **und den vollständigen zu
ersetzenden Absatz als Anker nennen**, nicht die eine Zeile, an der es sich festmachen lässt.
Ein halber Anker hat in der letzten Sitzung einen normativen Satz gelöscht.

⚠️ **Das Projektwissen ist nicht die Quelle für Dateien.** Frag nach dem Repo-Stand.

## Stand

`main` = `38ea020`. Register **D1–D123**. **426 Tests**, dazu **elf Eigenschaftstests** unter
`MAR_HYPOTHESIS=voll`. `make check` prüft Baum, Specs, Tests; `make check-all` zusätzlich
`tests/property` unter dem vollen Profil — **zwei** pytest-Läufe, also zwei Endzeilen.

- **01** Atom, Verifier, elf Reject-Codes, acht Zustände.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung.
- **Werkzeugschicht Autorschaft** (D119, D122): `build_signed` im Paket, fünf Autoren-Helfer auf
  einem Kodierweg, `VOUCH_WITHOUT_TEXP`, `t_exp` an allen Erzeugerstellen und im Generator.

**Werkzeuge:** `tools/example_nucleus.py`, `tools/sim` (S1–S6), `tests/property` (P-1 bis P-6).

## Das Aufnahmekriterium

Aus `08 §3`, vor jedem neuen Mechanismus:

> **Senkt er die Kosten dafür, festzustellen, wer was gesagt hat — oder verteilt er Macht?**
> Senken: Protokoll. Verteilen: Policy. Keines von beidem: Werkzeug.

Die dritte Spalte ist neu. Sie hat die ganze letzte Sitzung getragen: ein Wallet erzeugt Claims
überhaupt erst, senkt also nichts und verteilt nichts. Kein Layer, keine Golden Anchors, keine
Zahl im Dateinamen.

## Prüfregeln

Die sieben aus der Vorsitzung gelten unverändert: **vor dem Schreiben rechnen**, **Standprüfung**,
**Feldinventur**, **Zugehörigkeitsliste am Datentyp**, **Ausgänge aufzählen**, **Monotonie
stufenweise**, **Abhängigkeitssatz bei Reihenfolgeänderungen**. Dazu **Parallelenprüfung** und
**Begründungsprüfung**.

Neu aus der letzten Sitzung:

10. **Leserprüfung (D119).** Trägt ein normativer Satz eine Pflicht an den *Autor* von Claims,
    wird bei seiner Formulierung benannt, welche Funktion die Erfüllung liest. Gibt es keine, ist
    der Satz auf SOLL zurückzunehmen oder mit einem Vermerk zu versehen. Die Feldinventur fragt
    nach dem Leser eines Feldes; diese Regel nach dem Leser einer Pflicht. `02 §6.2` hat zwei
    Layer überdauert, weil seine einzige Wirkung war, dass ein wohlerzogener Autor etwas
    hinschreibt.
11. **Geschwisterformel.** Ein Verbot, das mit "an welcher Stelle auch immer" endet, fängt
    Geschwister, die eine Aufzählung nicht kennt. Billiger als eine vollständige Liste. Der
    Schnitt in D122 nannte einen Helfer; das Verbot hat fünf gefunden.
12. **Zwei Läufe, eine Variable.** Um zu zeigen, dass ein Mechanismus erreicht wird oder
    wirkungslos ist, zwei Läufe über derselben Menge vergleichen, die sich in genau einer Größe
    unterscheiden. Eine Bedingung zu prüfen, die auch andere Ursachen erfüllen könnten, ist
    schwächer — und liest sich gleich.

## Was die letzte Sitzung gelehrt hat

**Vier von vier Befunden lagen in Tests, nicht im Produktivcode.** Der zirkuläre Feldtest, der
falsch benannte Equivocation-Test, das zu grobe Prädikat, die Zwillingsbuchführung. Der
Produktivcode war beide Läufe lang richtig.

**Zwei Befunde lagen in Prüfungen, die Claude selbst als Abnahmekriterium formuliert hatte.** Ein
Abnahmekriterium ist keine Prüfung, sondern ein Text, und Texte haben Lücken derselben Art wie
Code.

**Das Werkzeug hat viermal richtig gehandelt**, wo es hätte raten können: es hat den Grenzwert
`t_exp = 5000` in `s6` erkannt und stehengelassen, vier weitere Erzeugerstellen gemeldet statt
still ausgedehnt, und die Geschwisterformel korrekt auf fünf Helfer angewandt.

## Offen

- **B-4** — Zwillingsbuchführung in `welten()` zieht kein Budget ab. Wirksam nur bei
  `erlaube_ueberzeichnung=False` **und** `erlaube_equivocation=True`, was heute keine Eigenschaft
  benutzt. Wer eine schreibt, repariert es zuerst.
- **Gleichstand bei `kante_claim_id`** — `test_groups.py:196` und `test_pagerank_groups.py:22`
  tragen den Fall, der Bruch über `sorted(...)[0]` ist von nichts geprüft. Nächster `02`-Durchgang.
- **Der Grenzwertvektor `now = t_exp`** in Layer 01 ist jetzt **baubar** (D119 gab `t_exp` an die
  Erzeuger) und weiterhin ungebaut.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** prüfen eine schwächere Aussage als sie
  scheinen (D117).
- **`02d-purpose`** (D56), **VR-04.1** (D26), **Zeugenquorum für Fristen** (D100).
- **`04 §7.2` Föderation** nicht durchgerechnet.
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **Aufräumen im Repo** — 41 Branches mit teils stehengebliebenen `voraus`-Zählern, und die
  Prompt-Dateien im Wurzelverzeichnis. Vor dem Löschen: prüfen, welche Prompts von Code oder
  Spec referenziert werden. `fuzz-prompt.md` ist es (Docstrings in `tests/property/`), und das
  heißt, dass die Definition von P-1 bis P-6 heute nur in einem Prompt steht.

## Der nächste Schritt

**Nicht Layer 05.** Der ist: vier Menschen erzeugen eigene Schlüssel, ein Genesis trägt ihre
Namen statt der Seeds `0x11×32` ff., und jemand geht die erste Obligation ein, die er erfüllen
will. Der Grund steht in `08 §2.2` — eine Aussage wird nicht dadurch überprüfbar, dass sie
signiert ist, sondern dadurch, dass sie mit anderem Signierten **kollidieren kann**. Ein weiterer
Spec-Layer erhöht die Kollisionsdichte um null.

Dafür sind D119 bis D123 die Grundlage, und drei Dinge fehlen, **in dieser Reihenfolge**:

1. **`00a-rotate-key` / D62** (`resolve_current_key`). Nach D123 ist ein zweites Gerät eine
   **Rotation**, keine Delegation — der einzige Weg, der einen Schreiber und eine Kette erhält.
   Der Fall tritt beim ersten Gerätewechsel ein, also vor dem ersten echten Nukleus, nicht danach.
2. **D120** — Persistenz der Kettenspitze und Core-Redo-Log. Fünf Ausgänge aus dem Zustand der
   Spitze, drei davon anhaltend. Ed25519 signiert deterministisch, deshalb ist die Wiederaufnahme
   idempotent.
3. **D121** — Einlesepfad, der nie wirft, plus unsigniertes Bündelformat.

Erst danach `05`. Dessen zwei bekannte Baustellen bleiben: **Über-Commitment als
Stufe-3-Auslöser** (D40, mit D118 scharf) und die **Beta-Reputation** mit dem
Moral-Licensing-Problem, gegen das Layer 02s Flussmodell immun ist und `05` es nicht wäre.
