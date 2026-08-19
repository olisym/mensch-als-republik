# Werkzeug-Prompt: Herleitung der Kalibrierung aus dem Genesis (D147)

## Branch und Basis

Branch `impl/kalibrierung`, Basis ist der Commit, der diese Datei einführt. Ein Commit am Ende,
kein Merge.

## Normative Grundlage

- `07-decisions.md` D147 — Beschluss, Begründung und die verworfenen Alternativen.
- `02-trust-flow.md §8.1` — die fünf Lagen als Tabelle. Sie ist die Abnahmegrundlage.
- `00-nucleus-genesis-constitution.md §4` Schlüssel 9 und `§4.0` — Feldbelegung
  `{0: C₀, 1: γ_num, 2: γ_den, 3: D}` und die Wohlgeformtheitsbedingungen.
- `07-decisions.md` D145 — dieselbe Bindungsprüfung in `decide`, als Vorbild für Ort und
  Fehlerart.

## Auftrag

**1. `resolve_trust_params` in `mensch_als_republik/trust/params.py`.**

Die Funktion nimmt keyword-only `scope: bytes`, `genesis_obj: dict` und
`out_of_band: TrustParams | None = None` und liefert `TrustParams`. Ihr Verhalten ist die
Tabelle in `02 §8.1`; die fünf Lagen werden von dort abgelesen und nicht aus diesem Prompt
abgeschrieben.

Die Bindungsprüfung ist wörtlich die aus `decide`:
`SHA-256(DOM_NUC_GEN ‖ cbor_canon.encode(genesis_obj)) == scope`, sonst `ValueError`. Sie steht
**vor** jedem Zugriff auf ein Feld des Genesis.

Ein vorhandener Schlüssel 9, der keine Map mit den vier erwarteten Schlüsseln und
Integer-Werten ist, ist formwidrig und ergibt `ValueError` — nicht ein stilles Ausweichen auf
`out_of_band`. Die Wohlgeformtheit der Werte selbst prüft `TrustParams.__post_init__` bereits;
sie wird **nicht** ein zweites Mal implementiert.

**2. Der Vergleich in der dritten Lage.** Sind Schlüssel 9 und `out_of_band` beide vorhanden,
entscheidet Gleichheit der vier Werte. Bei Abweichung `ValueError`, dessen Meldung sich von der
Bindungsmeldung unterscheidet — nach D146 muss ein Test die beiden trennen können.

**3. Tests.** Je ein Fall für alle fünf Lagen aus `02 §8.1`, plus der formwidrige Schlüssel 9.
Die erwarteten `TrustParams` werden aus dem jeweiligen Genesis-Objekt **abgeleitet**, nicht als
Literal getippt. Jeder `pytest.raises(ValueError)` trägt ein `match`, das die Meldungen
auseinanderhält.

**Rücknahmeprobe** an der dritten Lage, weil sie der eigentliche Defektfall ist: den Vergleich
versuchsweise entfernen, sodass ein vorhandener Schlüssel 9 stillschweigend gewinnt oder
stillschweigend verliert. Der Test muss rot werden. Im Bericht steht, welches `D` in diesem
Zustand für die Rechnung gegolten hätte — die Zahl, nicht nur „Test rot". Danach wieder
einsetzen.

**4. Eine Feststellung, kein Umbau.** Gegrept und im Bericht genannt: tragen die Genesis-Objekte
in `tools/example_nucleus.py` und `tools/sim/szenario.py` einen Schlüssel 9, und stimmt er mit
den `TrustParams` überein, die dort als Literal stehen (`C0=100, gamma_num=1, gamma_den=2,
D=100`)? Beide Antworten sind zulässig und beide sind zu melden.

- Stimmen sie überein oder fehlt Schlüssel 9 überall: nichts tun.
- Weicht irgendwo etwas ab: **melden, nicht reparieren.** Eine Abweichung im Beispielnukleus
  wäre ein Befund über die Golden Anchors und gehört ins Register, nicht in diesen Lauf.

## Nicht-Ziele

- **`derive`, `trust`, `rank`, `capacity` und `RelaxParams` bleiben unverändert.** Sie nehmen
  weiterhin `TrustParams` bzw. `RelaxParams` entgegen und kennen kein Genesis. Das ist der Kern
  von D147 und keine Vereinfachung.
- **`α` und `K` werden nicht hergeleitet.** Sie stehen nicht im Genesis.
- **`TrustParams.__post_init__` bleibt unverändert.** Die doppelte Formulierung der
  Wohlgeformtheit gegenüber `00 §4.0` ist in D147 notiert und bewusst nicht zusammengelegt.
- **`anchor_set` (Schlüssel 3) bleibt ungebunden.** Benannte Grenze in D147.
- **Kein Aufrufer wird umgestellt.** Weder die Werkzeuge noch die Tests bekommen den neuen Weg;
  Auftrag 4 ist eine Messung, kein Umbau.
- **Kein `D >= C₀`-Vermerk.** Offen in D147.

## Abnahmekriterien

- `make check` grün. Die Testzahl vorher wird festgehalten und im Bericht genannt; sie steigt um
  die Zahl der neuen Testfunktionen und um nichts sonst.
- `make check-all` grün, `python tools/check_specs.py` grün.
- Die sechs Fälle sind vorhanden und jeder `raises` trägt ein `match`.
- Das Ergebnis der Rücknahmeprobe steht mit der Zahl im Bericht.
- Die Feststellung aus Auftrag 4 steht im Bericht, mit dem Grep-Ergebnis und nicht als
  Einschätzung.

Widerspricht eine Messung diesem Prompt, gilt die Messung. Melden, nicht anpassen.
