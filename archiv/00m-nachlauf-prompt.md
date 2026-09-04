# Nachlauf 00m — der Wächter für das Zielobjekt steht zu spät

## Befund

`04-governance.md §4.1`, Absatz „Das Zielobjekt gehört zur Auszählung":

> Ist `tally.state` nicht `UNEVALUABLE` und trägt das gereichte Zielobjekt nicht den Hash
> `proposal.constitution_hash`, ist das ein **`ValueError`** wie in Bedingung 0.

Umgesetzt ist der Wächter hinter den Bedingungen 1 bis 5. Trägt der `ratify@1` nicht, kehrt
`verify_ratification` mit `UNSUPPORTED_RATIFICATION` zurück und prüft das Zielobjekt nie. Ein
Aufruferfehler erscheint dann als Lage der Welt — genau das, was Bedingung 0 verhindert.

Der Defekt liegt im Prompt zu `00m`, nicht im Lauf. Dort stand „nach allen Bedingungen 1 bis 5",
und das Werkzeug hat es korrekt umgesetzt. Die Spec ist richtig; der Code war enger.

## Branch und Basis

Weiter auf `impl/00m-regierbarkeit`, kein neuer Branch.

```
set BASIS (git rev-parse HEAD)
echo $BASIS
```

## Auftrag

### 1. Den Wächter verschieben

In `mensch_als_republik/governance/verify_ratification` — Datei
`mensch_als_republik/governance/epoch.py` — wandert der Block

```
    if (
        target_constitution_obj is None
        or constitution_hash(target_constitution_obj) != proposal.constitution_hash
    ):
        raise ValueError("target_constitution_obj does not match proposal")
```

von seiner jetzigen Stelle an die Stelle unmittelbar **nach** dem Block
`if tally.participants is None:` und unmittelbar **vor** der Zeile
`participants = tally.participants`.

Nur verschieben. Der Wortlaut bleibt unverändert.

Der Regierbarkeitsblock (Bedingung 6) bleibt, wo er ist: unmittelbar vor der Konstruktion der
Folgeepoche, nach allen Bedingungen 1 bis 5. Nur der ValueError-Wächter zieht nach vorn.

### 2. Ein Prüffall, der die Stelle hält

Neu in `tests/governance/test_regierbarkeit.py`:
`test_mismatched_target_with_unsupported_ratify`.

Die Welt ist die aus `test_mismatched_target_object_raises` mit einer Änderung: der `ratify@1`
zitiert **keine** Stimme und erreicht die Schwelle deshalb nicht. Er würde ohne den Wächter mit
`UNSUPPORTED_RATIFICATION` zurückkehren.

Geprüft wird:

```
tally.state is TallyState.PASSED
verify_ratification(..., target_constitution_obj=C1, ...) wirft ValueError
```

Gegen den heutigen Stand des Branches ist dieser Fall rot, und zwar mit „DID NOT RAISE
ValueError". Wird er grün, ohne dass Auftrag 1 ausgeführt wurde, ist die Welt falsch gebaut —
dann melden, nicht anpassen.

## Nicht-Ziele

- **Keine Änderung an `04-governance.md`**, `07-decisions.md` oder `pruefregeln.md`.
- **Keine Änderung an Bedingung 6**, an `constitution_governable` oder an `decide`.
- **Keine weiteren Aufrufstellen** und keine Signaturänderung.
- **Keine Umbenennung** bestehender Prüffälle.
- Kein Aufräumen daneben.

## Abnahmekriterien

1. `make check` grün.
2. Testzahl **583**, gemessen mit `.venv/bin/python -m pytest -q`. Basis sind 582.
3. `git diff --numstat $BASIS` nennt **genau zwei** Dateien:
   `mensch_als_republik/governance/epoch.py` und `tests/governance/test_regierbarkeit.py`.
4. Zwei Rücknahmeproben, jede einzeln gefahren und danach zurückgenommen.

**Probe E** — den Wächter an die alte Stelle zurückschieben, also wieder hinter Bedingung 5.
Erwartet rot, **genau einer**: `test_mismatched_target_with_unsupported_ratify`. Der ältere
`test_mismatched_target_object_raises` bleibt **grün**. Das ist der eigentliche Beleg des
Nachlaufs: der vorhandene Prüffall hat die Stelle nie gehalten, nur die Prüfung selbst.

**Probe F** — den Wächter ganz entfernen. Erwartet rot, **genau zwei**:
`test_mismatched_target_with_unsupported_ratify` und `test_mismatched_target_object_raises`.

## Abschluss

**Ein** Commit auf `impl/00m-regierbarkeit`. **Kein** Merge, **kein** Push.

Der Bericht nennt `$BASIS`, den Commit-Hash, `git diff --numstat $BASIS`, die Testzahl und für
beide Proben die tatsächlich rote Menge.

Widerspricht eine Messung diesem Prompt, wird sie **gemeldet**. Kein Wert wird nachgezogen.
