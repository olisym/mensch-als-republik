# Lauf B `impl/sim-tuer` — eine Tür pro Sprache in der Simulation

## Branch und Basis

Branch: `impl/sim-tuer`.

Basis ist der Commit, der diese Datei einführt. Er heißt hier **PROMPT-COMMIT** und wird
abgeleitet, nicht getippt:

    git log --format=%H -1 -- sim-tuer-prompt.md

Der Vergleichspunkt der Abnahme ist dieser Commit.

## Normative Grundlage

- `07-decisions.md` D132 — fremde Bytes gehen an keiner Stelle durch `claim_from_bytes`; dem
  Container wird nie geglaubt.
- `07-decisions.md` D138 — Zuschnitt dieses Laufs, `read_claim` ohne Store, `hat_claim` liest den
  Inhalt.
- `07-decisions.md` D131 — `read_claim` wirft nie; „wirft nie" ist eine bewiesene Eigenschaft.
- `07-decisions.md` D133 — ein Beobachter hält genau das, wofür `read_claim` einen `Claim`
  geliefert hat.
- `07-decisions.md` D120 — Weiterschreiben ist der erkannte Fehler; `wiederaufnehmen` hält an,
  wenn die Spitze nicht im Ausgang liegt.
- `werkzeuge.md §3.1` — Teilnehmer, Verzeichnisse, Zustellung.

Berührte Datei: `tools/sim/welt.py`. Dazu ein neuer Test.

## Auftrag

### A — `store_laden` über `read_claim`

`tools/sim/welt.py:86` ist der einzige Verstoß gegen D132 im Produktivcode. Ersetzt wird

    store.add(claim_from_bytes(path.read_bytes()))

durch einen Aufruf von `read_claim(path.read_bytes())` **ohne** zweites Argument. Liefert er einen
`Claim`, wird er aufgenommen; liefert er einen `ErrorCode`, wird die Datei **übersprungen**.

Kein `try`, kein `except` — `read_claim` wirft nach D131 nicht, und ein `except` hier machte aus
einer bewiesenen Eigenschaft eine vermutete.

Der Store wird nicht durchgereicht. D138 begründet es: `structural_check` benutzt ihn nur für
`_check_foreign_lifecycle`, und ein beim Laden halbfertiger Store bände `FOREIGN_LIFECYCLE` an die
Hex-Sortierung der Dateinamen. Derselbe Claim wäre je nach Ladereihenfolge Reject oder nicht.

Der Import von `claim_from_bytes` in Zeile 9 fällt weg.

### B — `hat_claim` liest den Inhalt

Heute:

    return self.inbox_path(cid).is_file()

Künftig lokalisiert der Name nur noch die Datei; die Antwort kommt aus dem Inhalt. `hat_claim(cid)`
ist wahr genau dann, wenn die Datei existiert, `read_claim` auf ihren Bytes einen `Claim` liefert
und `claim_id` dieses Claims gleich `cid` ist. Jeder andere Fall ist falsch: fehlende Datei,
`ErrorCode`, abweichende Id.

`Teilnehmer.kennt` bleibt der dünne Durchgriff auf `hat_claim` und wird nicht eigens angepasst —
er erbt die Prüfung. Genau darum geht es: `kennt` ist der `Ausgang.kennt`-Port, den
`Autor.wiederaufnehmen` befragt.

### C — `claim_einlegen` bleibt

Es schreibt eigene Bytes eines eigenen `Claim`-Objekts unter die selbst gerechnete `claim_id`.
Keine fremden Bytes, keine Änderung.

## Ausdrückliche Nicht-Ziele

- **Kein Bündelformat.** D138 hat den Zuschnitt korrigiert: die Inbox *ist* das Bündel aus D121.
- **`zustellen` wird nicht angefasst.** Es kopiert unvertraute Bytes zwischen unvertrauten
  Verzeichnissen; die Grenze liegt beim Lesen. Ein Erkenner an der Kopierstelle wäre der verteilte
  Erkenner, gegen den D132 geschrieben ist. Dass `zustellen` durch B teurer wird, ist erwartet.
- **Kein Cache, kein Index** über `hat_claim`. Ein Index wäre wieder etwas, dem geglaubt wird.
- **Keine Meldung übersprungener Claims** aus `store_laden` — kein Zähler, kein Protokoll, kein
  zweiter Rückgabewert. D138 stellt das ausdrücklich zurück.
- **`tools/autor.py` bleibt unberührt.** Sein `claim_from_bytes` liest den **eigenen** Redo und ist
  nach D92 und D132 legitim.
- **`read_claim` und `structural_check` werden nicht geändert.** Der `store`-Parameter bleibt, wo
  er ist.
- Keine Tests in `tests/test_atom.py`, `tests/test_verifier.py`, `tests/trust/test_coupling.py` —
  deren `claim_from_bytes`-Aufrufe dekodieren Vektor-Hex aus der Spec, also eigene Bytes.
- Keine Änderung an `tools/sim/szenario.py`, `anzeige.py`, `__init__.py`.

## Abnahmekriterien

1. `make check-all` grün, mit vorher gelöschtem `.hypothesis/`. Beide Endzeilen melden. Erwartung
   vor dem Lauf: 491 und 14, danach höher um die neuen Tests — die Zahl wird gegriffen, nicht
   geschätzt.

2. **Regressionstest zu B, neu.** Es gibt heute keinen Test, in dem Dateiname und Inhalt
   auseinanderfallen; `tests/test_sim.py` berührt weder `inbox_path` noch `fromhex`. Der neue Test
   legt zwei Claims `A` und `B` an, schreibt **`A`s Bytes unter `B`s Dateinamen** und behauptet:

   - `hat_claim(cid_B)` ist falsch — der Name lügt,
   - `hat_claim(cid_A)` ist falsch, solange keine Datei unter `A`s Namen liegt,
   - `store_laden()` enthält `A` und nicht `B` — der Inhalt gewinnt.

   Die dritte Zeile ist die eigentliche Aussage und darf nicht fehlen: sie trennt „der Name wird
   nicht geglaubt" von „die Datei wird verworfen".

3. **Rücknahmeprobe.** `hat_claim` auf `is_file()` zurücksetzen und bestätigen, dass der Test aus 2
   **rot** wird. Welche Behauptung fällt, mit Namen melden. Danach die Rücknahme verwerfen.

4. **Zweiter Test zu A:** eine abgeschnittene oder sonst unlesbare Datei in der Inbox wird von
   `store_laden` übersprungen, ohne dass etwas geworfen wird, und die übrigen Claims sind
   vollständig geladen. Das ist die Totalitätsaussage aus D131 an ihrem ersten Produktivaufrufer.

5. Null Treffer für

       grep -rn "claim_from_bytes" tools/sim

   Trefferzahl melden.

6. `read_claim` hat danach mindestens einen Produktivaufrufer. Melden, welchen:

       grep -rn "read_claim" tools mensch_als_republik

7. `python tools/check_specs.py` sauber.

## Abschluss

Ein Commit auf `impl/sim-tuer`. Kein Merge, kein Push.

Was nicht in diesem Prompt steht, wird gemeldet und nicht gebaut. Widerspricht eine Messung dem
Prompt: melden, nicht anpassen. Rückfragen gehen an den Supervisor, nicht ins
Implementierer-Fenster — sie sind Kandidaten für Spec-Lücken.
