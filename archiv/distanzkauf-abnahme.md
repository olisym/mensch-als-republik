# Abnahme: Charakterisierungstest Distanzkauf (D141)

Branch `impl/distanzkauf`, Prompt-Commit `57e9153`, Lauf `11f57a8`, Nachlauf `da8b424`.
Grundlage: `distanzkauf-prompt.md`, `07-decisions.md` D139/D141, `02-trust-flow.md §4`.

## Was der Test festhält

Eine Kante minimaler Kapazität von einem seed-nahen Knoten `p` hebt die Knotendecke eines
seed-fernen Grenzknotens `h` und gibt damit bereits vorhandenen ehrlichen Fluss frei. Drei
Fälle: ohne Angriff, auf der Schwelle, eine Einheit darunter. Gemessene Werte deckungsgleich
mit der Tabelle in D141, nichts geglättet.

Der dritte Fall trägt die Isolierung. Ohne ihn könnte der Test von etwas anderem als dem
`E⁺`-Filter grün gehalten werden: eine Einheit unter der Schwelle ist wirkungslos, genau auf
der Schwelle vervierfacht dieselbe Kante den Fluss.

## Geprüft am Diff, nicht am Bericht

- `git diff 57e9153 -- mensch_als_republik` ist **leer**. Der Distanzkauf ist nicht repariert,
  nicht abgemildert, nicht erkannt — der Test charakterisiert eine offene Schwäche.
- Keine getippte Kapazitäts- oder Distanzzahl. Alle Erwartungen laufen über
  `capacity(PARAMS, d)`; `N_A_TO_P` fällt aus dem Budget `D`, `D_H_OHNE` aus der Kettenlänge.
- Die Schwelle für `n` wird aus dem **unangegriffenen** Graphen gerechnet. Damit hängt der
  Erwartungswert nicht von dem Zustand ab, den er bewerten soll.
- 493 → 496 Tests, `make check-all` kalt grün.

## Befund im Nachlauf

Der erste Lauf prüfte `d_h == d_p + 1` — eine Aussage über die Lage von `h` **relativ zu `p`**,
nicht darüber, dass `h` sich bewegt hat. Eine Topologie, in der `h` ohnehin bei `d = 2` liegt,
hätte den Test grün gelassen, obwohl der Angriff nichts bewirkt. Ebenso fehlte die Bedingung,
dass `p` überhaupt seed-näher sitzt als `h` — ohne sie gibt es keinen Distanzgewinn zu kaufen.

Nachgetragen wurden `d_h < D_H_OHNE` und `d_p < D_H_OHNE - 1`. Rücknahmeprobe: `D_H_OHNE`
testweise auf `2` gesetzt, erste Behauptung rot.

**Vorbehalt.** Diese Probe verstellt eine Konstante, nicht die Topologie. Sie belegt, dass die
Behauptung `D_H_OHNE` liest, nicht dass sie eine echte Topologieänderung fängt. Das trägt hier,
weil die Behauptung eine strikte Ungleichung gegen eine abgeleitete Konstante ist. Wer die
Topologie je parametrisiert, braucht eine schärfere Probe.

## Rückfragen des Werkzeugs

Drei, alle berechtigt, zwei davon Fehler im Prompt:

1. **Abnahmekriterium 3 nannte die falsche Basis.** `71a8720` statt `57e9153` — der
   Vergleichspunkt eines Laufs ist der Prompt-Commit. Das Werkzeug hat gemeldet statt zu
   rebasen.
2. **`derive` ist nicht re-exportiert.** Der Prompt sagte „aus `mensch_als_republik.trust`".
   Import aus dem Untermodul ist richtig; ein Re-Export wäre ein Nicht-Ziel gewesen.
3. **Rücknahmeprobe 2 färbt auch Fall 3 rot.** Erwartet: ohne Distanzdecay fällt die Schwelle,
   und ein abgeleitetes `n` rutscht auf `0`. Dass daraus `INVALID_VOUCH_WEIGHT` wird, bestätigt
   beiläufig, dass `n` gerechnet und nicht getippt ist. Fall 3 wird nicht dagegen isoliert —
   eine Probe, die nur trifft, was sie treffen soll, wäre die schwächere Probe.

## Stand

Damit ist die Aussage aus D139/D141 zum ersten Mal **gemessen** statt aufgeschrieben. Entsteht
je ein Mechanismus gegen den Distanzkauf, wird genau dieser Test rot — die Rücknahmeprobe im
Voraus für den offenen Fork aus D140.
