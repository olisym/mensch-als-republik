# Lauf `00s` — eine Fangbreite für drei Prädikatprüfer

## Branch und Basis

Branch: `impl/00s`. Basis ist der Commit, der **diese Datei** enthält — der Branchpunkt von
`impl/00s` gegen `main`. Ein Commit auf dem Branch, kein Merge, kein Push.

## Normative Grundlage

- **D213** in `07-decisions.md` — im selben Commit wie dieser Prompt. Er entscheidet den Fall
  vollständig; dieser Prompt setzt ihn um und erfindet nichts dazu.
- `01-claim-atom.md` Anhang B: „falscher Feldtyp" fällt unter `MALFORMED_CBOR`.
- D181 — die breite Fangweite von `is_nuc_name` steht dort mit Begründung. Sie wird verengt,
  ihr **Verhalten** bleibt unverändert.

## Der Auftrag

Alles in `mensch_als_republik/predicates.py` und `tests/test_predicates.py`. Keine andere
Produktivdatei wird angefasst.

**1. Die Wache.** `parse_predicate` prüft als erstes, ob `p` ein `str` ist, und wirft sonst
`MalformedCbor`. Der Import kommt aus `mensch_als_republik.errors`, alphabetisch einsortiert.

**2. Die Verengung.** `is_nuc_name` fängt `VerifierError` statt `Exception`. Damit tragen alle
drei Prüfer dieselbe Fangbreite.

**3. Die Zeiger.** Der Docstring von `parse_predicate` nennt die Wache und D213. Der Docstring
von `is_nuc_name` nennt D213 zusätzlich zu D181.

**4. Die Prüffälle.** Vier Formen für ein `p`, das kein `str` ist:

```
b"nuc:x/vouch@1"        None        7        ["nuc:x/vouch@1"]
```

Daraus zwei parametrisierte Prüffälle, acht Prüfpunkte:

- `parse_predicate` wirft für jede der vier Formen `MalformedCbor`.
- Für einen Claim, dessen `p` durch jede der vier Formen ersetzt ist, liefern
  `is_core_predicate`, `is_nuc_predicate` und `is_nuc_name` jeweils `False`.

Der Claim wird aus dem vorhandenen `_claim`-Helfer gebaut und sein `p` mit `dataclasses.replace`
ersetzt — dieselbe Bauform wie in `test_nuc_name_bytes_p_returns_false`.

## Ausdrückliche Nicht-Ziele

- **`is_nuc_predicate` wird nicht gelöscht**, obwohl sie null Aufrufstellen hat. Die Löschung ist
  vorgeschlagen und nicht entschieden (D213).
- **Kein Eingriff in `verifier.py`.** Die dortige Typprüfung bleibt, wie sie ist; die Wache ist
  eine zweite Tür, kein Ersatz.
- **Keine neue Fehlerklasse und kein neuer Reject-Code.** Es bleiben elf.
- **Kein Eingriff an `resolve_scope` oder `check_scope_binding`.** Sie erben die Wache über
  `parse_predicate`; ihre eigene Form ändert sich nicht.
- **Keine Spec-Datei wird angefasst.**
- Kein sonstiges Refactoring in `predicates.py`. Fällt etwas auf: melden, nicht bauen.

## Abnahmekriterien

1. `make check` grün. `ruff` ohne Befund.
2. Testzahl **597**. Vorher sind es 589; acht Prüfpunkte kommen dazu.
3. `test_nuc_name_bytes_p_returns_false` bleibt **grün** und wird nicht angefasst.
4. **Rücknahmeprobe A — die Wache muss zählen.** Die Wache aus `parse_predicate` entfernen, die
   Verengung stehen lassen, Reihe fahren. Erwartet: **9 rot, 588 grün**, und zwar genau

   ```
   test_parse_predicate_...            vier Parameter
   test_praedikatpruefer_...           vier Parameter
   test_nuc_name_bytes_p_returns_false
   ```

   Die letzte Zeile ist der Beleg: ohne Wache verliert die verengte Fangweite ihr Netz. Fehlt sie
   in der Rotmenge, ist die Verengung nicht angekommen. Danach zurücknehmen.
5. **Rücknahmeprobe B — die Verengung darf nicht zählen.** Die Verengung zurücknehmen
   (`except Exception`), die Wache stehen lassen, Reihe fahren. Erwartet: **597 grün**. Wird hier
   etwas rot, ändert die Verengung Verhalten und D213 ist widerlegt — dann **melden und
   anhalten**, nicht anpassen. Danach zurücknehmen.
6. Beide Proben werden im Bericht **wörtlich** mit ihrer Zeile aus `pytest` wiedergegeben.

## Abschluss

Ein Commit auf `impl/00s`. Kein Merge, kein Push, keine Änderung an `main`.
