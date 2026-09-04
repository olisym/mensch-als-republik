# Korrektur-Prompt — Layer 04c

Ausgangsstand `impl/04b-korrektur`, Commit `5714bbc`. Eine Umschichtung, keine neue Bedingung.

## 1. `threshold_for` teilen (D113)

`threshold_for()` wird ersetzt durch zwei Funktionen:

```
threshold_class(old_obj, new_obj, genesis_obj) -> str
applied_threshold(old_obj, new_obj, klass)     -> tuple[int, int]
```

`threshold_class` trägt die Ableitung aus `04 §3.4`: unterscheiden sich beide Verfassungen
ausschließlich in `participants`, ist die Klasse `membership`, sonst der Name zu `genesis[5]`.

`applied_threshold` liest `old_obj["thresholds"][klass]` und `new_obj["thresholds"][klass]` und
gibt `ratio_max` zurück. Sie coerciert nicht; sie bekommt bereits validierte Integer-Paare.

## 2. `decide()` umbauen

Genau eine Klassenbestimmung. Der heute inline eingesetzte Vergleich der beiden `_rest`-Objekte
entfällt ersatzlos:

1. `klass = threshold_class(...)`
2. `_is_ratio` auf `thresholds[klass]` beider Verfassungen — Verletzung ergibt
   `MALFORMED_THRESHOLD`
3. `threshold = applied_threshold(..., klass)`

Das `try/except (KeyError, TypeError, IndexError)` um den Aufruf **entfällt**: nach Schritt 2 kann
nichts mehr werfen. Unerreichbarer Code, der einen Fehlerfall vortäuscht, ist schlechter als
keiner.

Fehlt `thresholds` oder `klass` darin, greift weiterhin die bestehende Prüfung vor `_is_ratio`.

## 3. Tests

**Keine neuen Vektoren.** Erwartete Testzahl: **387, unverändert.** Steigt sie, ist etwas
Zusätzliches passiert; fällt sie, wurde ein Test entfernt. Beides ist meldepflichtig.

Bestehende Tests dürfen `threshold_for` importieren; dann sind sie auf die beiden neuen Funktionen
umzustellen.

## 4. Abnahme

Branch `impl/04c-korrektur`. `make check` grün in drei Blöcken, committen vor dem Melden,
`git add` mit expliziten Pfaden.
