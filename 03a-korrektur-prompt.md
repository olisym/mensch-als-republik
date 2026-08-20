# `03a` — Korrekturlauf zur Abnahme

Auftrag an den Implementierer. Normative Quelle: `03-abnahme.md` (Befunde B1–B6), die
nachgezogenen Abschnitte `03-profiles.md §1.2`, `§1.4`, `§2.4.2`, `§2.4.4`, `§3.3.1`, sowie die
neuen Vektoren `P-G`, `SE-13`, `VS-12` bis `VS-14`, `PR-INV-13` in `03-golden-anchors.md`.

Umfang: vier Module, sechs Punkte, sechs neue Tests. **306 bestehende Tests bleiben grün** —
keiner wird angepasst. Wird einer rot, ist das der Beweis, dass eine Korrektur zu weit greift.

---

## 1. `profiles/verdict.py` — Eingangsprüfung (B1, B4)

`settlement()` beginnt mit einer Prüfung auf Prädikat, Scope und Store-Eintrag; `verdict_status()`
hat keine. Ein Verdikt aus Nukleus B, mit `scope = N_A` ausgewertet, wird heute nicht abgewiesen:
`path_i` vergleicht `verdict.I` gegen die Arbitratoren von A, und steht der Autor dort, lautet
die Antwort `BINDING`.

**Der Fall ist nicht exotisch.** Ein anerkannter Schiedsrichter sitzt typischerweise in mehreren
Nuklei — genau dann greift der Fehler.

Vor jedem weiteren Zugriff:

```
verdict ist nuc:{scope}/verdict@1   und   verdict.N == scope   und   im Store
```

sonst `ValueError`. Damit verschwindet auch der `KeyError` aus `by_cid[v_cid]` (B4): zwei
Funktionen, dieselbe Lage, ab jetzt derselbe Fehlertyp.

Die Strecke ist die von `settlement()` — **gleiche Reihenfolge, gleiche Formulierung**. Wenn
beim Bauen auffällt, dass sich die drei Zeilen sinnvoll teilen lassen, ist das eine gute Idee;
wenn nicht, ist die Duplikation von drei Zeilen billiger als eine Abstraktion, die nur zweimal
benutzt wird.

Vektoren: `VS-13` (fremder Scope), `VS-14` (falsches Prädikat), `PR-INV-13`.

## 2. `profiles/verdict.py` — Vermerk bei fremd-gescopter Anklage (B3)

`accusation.N != scope` meldet heute `UNKNOWN_ACCUSATION`. Die Anklage ist **bekannt**; sie
liegt nur im falschen Nukleus. Richtig ist `SCOPE_MISMATCH` (`03 §2.4.4`, Tabelle).

Wirkung unverändert — Pfad (ii) bleibt nicht auswertbar. Nur die Diagnose ändert sich, und die
entscheidet, wo der Betreiber sucht.

Vektor: `VS-12`.

## 3. `profiles/credit.py` — `EXPIRING_OBLIGATION` unbedingt (B2)

Der Vermerk steht heute im `EXPIRED`-Zweig und erscheint damit genau dann, wenn er wertlos ist:
nach dem Erlöschen sagt `EXPIRED` es ohnehin.

```
obligation.t_exp is not None  ⇒  EXPIRING_OBLIGATION, unabhängig vom Zustand
```

Die Stelle ist `_obligation_v_findings` oder gleich daneben — jedenfalls dort, wo die Obligation
**einmal** betrachtet wird, nicht in einem Zustandszweig. `SE-8` bleibt grün und trägt den
Vermerk weiterhin.

Vektor: `SE-13` (aktive Obligation mit `t_exp` in der Zukunft → `OPEN` + `EXPIRING_OBLIGATION`).

## 4. `profiles/policy.py` — defektes Genesis (B6)

Der Scope-Check schützt nicht vor einem Genesis ohne Key `4`: `scope` wird *aus* `genesis_obj`
gerechnet, also passiert jedes Objekt den Vergleich, das der Aufrufer selbst gehasht hat.
`genesis_obj[4]` läuft dann in einen `KeyError`.

Ein Genesis ohne `constitution_hash` ist kein Teilwissen, sondern ein defektes Objekt — dieselbe
Klasse wie der Scope-Fehler, also `ValueError`. Gleiches gilt, wenn der Wert keine `bytes` der
Länge 32 ist.

Ebenfalls zu prüfen: `irrevocable_predicates` muss eine Liste von Strings sein. Ist sie es
nicht, ist das Verfassungsobjekt defekt — **nicht** `ValueError`, sondern Sicherheits-Default
plus `CONSTITUTION_HASH_MISMATCH`? **Nein.** Das Objekt hat den Hash-Vergleich bereits bestanden,
es ist also genau das Objekt, das das Genesis meint. Ein defekter Inhalt darin ist eine
Spec-Lücke — **Rückfrage, nicht entscheiden.**

Vektor: `P-G`.

> **Nachtrag (D167, D168).** `resolve_policy` liest `genesis_obj[4]` nicht mehr und prüft es
> deshalb auch nicht; ein Genesis ohne Key `4` ist kein Fehler dieses Auflösers. `P-G` erwartet
> seit D168 das normale Ergebnis statt `ValueError`. Der Wortlaut oben bleibt stehen, weil
> dieser Prompt erteilt ist; normativ gilt `03-profiles.md §1.2`.

## 5. `profiles/findings.py` — `_dedupe_sort` (B5)

Wird von vier Modulen importiert und trägt einen Unterstrich. Umbenennen in `dedupe_sort`,
Aufrufstellen mit.

---

## 6. Abnahme

1. `make check` grün in allen drei Blöcken.
2. **312 Tests** (306 + 6). Keiner der 306 ist geändert, übersprungen oder angepasst worden.
3. `git diff --stat` zeigt `profiles/verdict.py`, `profiles/credit.py`, `profiles/policy.py`,
   `profiles/findings.py`, die drei importierenden Module (nur Importzeile) und
   `tests/profiles/*`.
4. `git status --short` leer.

## 7. Rückfragen

Der Punkt aus §4 (defekter Inhalt eines hash-korrekten Verfassungsobjekts) ist ausdrücklich
**offen** und geht zurück ins Spec-Gespräch. Alles andere in dieser Datei ist entschieden.
