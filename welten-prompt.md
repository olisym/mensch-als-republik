# Lauf `impl/welten` — Buchführung des Weltgenerators

## Branch und Basis

Branch: `impl/welten`.

Basis ist der Commit, der diese Datei einführt. Er heißt hier **PROMPT-COMMIT** und wird zu Beginn
des Laufs abgeleitet, nicht getippt:

    git log --format=%H -1 -- welten-prompt.md

Der Vergleichspunkt der Abnahme ist dieser Commit, nicht der Branchpunkt der Spec-Reihe.

## Normative Grundlage

- `07-decisions.md` D133 — `welten()` erzeugt in der Voreinstellung strukturell gültige Claims;
  vierte Lage `"grenze"`.
- `07-decisions.md` D134 samt Nachtrag — die Budgetbuchführung ist gruppenweise und wird über
  **lebende Mitglieder** formuliert, nicht über den ersten Claim einer Gruppe.
- `07-decisions.md` D135 — `EQUIVOCATION_FLAGGED` gehört ins Budget-Set.
- `07-decisions.md` D136 — Umlenkungstabelle für Verweise auf gelöschte Prompt-Dateien.
- `01-claim-atom.md §6.7` — `INCOHERENT_EXPIRY` gdw. `t` und `t_exp` vorhanden und `t >= t_exp`.
- `01-claim-atom.md §6` — zeitlich gültig gdw. `now <= t_exp`.
- `02 §3.1` — `n_budget = max n` über die Mitglieder einer Gruppe, `Σ_J n_budget <= D` über die
  Gruppen. Maximum innerhalb, Summe darüber.
- `werkzeuge.md §4.1`, `§4.2` — der Generator und die sechs Eigenschaften.

Einzige berührte Datei für A bis D: `tests/property/welten.py`. E berührt zusätzlich die in der
Tabelle genannten Testdateien und `tools/sim/`.

## Auftrag

### A — Das nächste `t` sichtbar machen (D133)

`_Signer` bekommt eine Eigenschaft `naechstes_t`, die das `t` liefert, das der **nächste**
`claim()`-Aufruf verwenden wird. Heute zählt `claim()` den Zähler innerhalb der Methode hoch; der
Aufrufer kennt das `t` erst hinterher und kann deshalb keine Untergrenze setzen.

Die Lage `"vergangen"` zieht danach

    t_exp aus [naechstes_t + 1, now - 1]

Ableitung: `01 §6` fordert `t < t_exp`, also `t_exp >= t + 1`, mit `t = naechstes_t`.

Keine feste Untergrenze wie `min_value=100` — sie hielte nur, solange keine Welt mehr als hundert
Claims je Identität baut, und diese Schranke stünde nirgends. Kein `assume`. Wird der Bereich
jemals leer, ist das ein Befund und wird gemeldet, nicht weggefiltert.

### B — Vierte Lage `"grenze"` (D133)

`_T_EXP_LAGEN` bekommt die Lage `"grenze"` mit `t_exp = now`. Gewichtung `4 : 4 : 1 : 1` in der
Reihenfolge abwesend, künftig, vergangen, grenze — also zehn Einträge.

`"grenze"` liegt auf der **lebenden** Seite: `_in_budget_set` prüft `now <= claim.t_exp`, und
`01 §6` sagt dasselbe. Der Punkt schließt den Grenzwertvektor `now = t_exp`, den D119 als „baubar
und ungebaut" führt; er war ungebaut, weil der Erzeuger ihn nicht ziehen konnte.

### C — Buchführung über lebende Mitglieder (D134 samt Nachtrag)

Die heutige Form `remaining[author] -= n` je Claim wird ersetzt durch:

    lebend(t_exp)      := t_exp is None oder t_exp >= now
    gruppe[(a, s)]     := max n über die lebenden Mitglieder der Gruppe (a, s)
    verbraucht[a]      := Summe über s von gruppe[(a, s)]
    Schranke           := verbraucht[a] <= D            (nur bei erlaube_ueberzeichnung = False)

Obergrenze für ein neues **lebendes** Mitglied der Gruppe `(a, s)`:

    n <= gruppe[(a, s)] + (D - verbraucht[a])

Ableitung: nach dem Einfügen zahlt die Gruppe `max(gruppe, n)`, die Änderung an `verbraucht[a]`
ist also `max(0, n - gruppe)`. Die Schranke `verbraucht[a] - gruppe + max(gruppe, n) <= D` ergibt
umgestellt genau die Zeile oben.

Ein **nicht lebendes** Mitglied zieht `n` aus `[1, D]` und ändert die Buchführung nicht. Das ist
der Kern des Nachtrags zu D134: ein abgelaufenes Mitglied trägt null, gleich an welcher Stelle es
gezogen wurde — und ein lebender Zwilling hinter einem abgelaufenen Ersten trägt `n2`, obwohl die
alte Form dort nichts gebucht hat.

Weiter:

- Das Tor `if not erlaube_ueberzeichnung and remaining[author_i] < 1: continue` **entfällt**. Ein
  Autor auf `verbraucht = D` darf weiter bürgen: abgelaufen, oder lebend mit `n <= gruppe[(a, s)]`.
  Bliebe das Tor stehen, gingen genau die Welten verloren, für die D134 gebaut wird.
- Ist die Obergrenze für ein lebendes Mitglied null, wird der Claim **übersprungen**. Nicht: still
  auf abgelaufen umbiegen. Null tritt genau dann ein, wenn `gruppe[(a, s)] = 0` und
  `verbraucht[a] = D`.
- Bei `erlaube_ueberzeichnung = True` bleibt `n` aus `[1, D]` unverändert; dort gibt es keine
  Schranke einzuhalten.

### D — Ziehen vor Bauen

Pro Schleifendurchlauf werden **alle** Ziehungen abgeschlossen, bevor der erste Claim gebaut wird:
Autor, Empfänger, Zwilling ja/nein, beide Lagen, beide `t_exp`, beide `n`.

Das ist keine Stilfrage. `t_exp` hängt jetzt von `t` ab und `n` von `t_exp`; beide `t`-Werte sind
über `naechstes_t` vorher bekannt (`naechstes_t + 1` für den Ersten, `naechstes_t + 2` für den
Zwilling). Heute ist die Reihenfolge gemischt: `twin` fällt vor dem Bau des Ersten, `lage2`
danach — das trägt unter den neuen Abhängigkeiten nicht mehr.

Zwei Folgen:

- Kann kein lebender Zwilling gebaut werden, entsteht **kein** Zwilling, und der Erste wird mit
  `kette_fortschreiben=True` gebaut. Kein unbeantworteter Fork, der die nächste Signatur desselben
  Autors ungewollt zur Equivocation macht.
- Die Konstruktion `n2 = n - 1` beziehungsweise `min(d_budget, n + 1)` samt Nachbesserung
  **entfällt**. `n2` wird nach derselben Regel gezogen wie `n`. Equivocation entsteht aus `gabeln`
  plus `signieren` über demselben `h_prev` — `_is_in_equivocation_pair` prüft das Paar über den
  Store —, nicht aus abweichendem Gewicht. Kein Test setzt auf `n2 != n` auf; der einzige Test auf
  Zwillinge, `test_p3b_finds_equivocation_passed_to_pending`, arbeitet über Stimmen.

Die Ziehungsreihenfolge ändert damit den Ziehungsstrom von hypothesis und den erzeugten
Weltkorpus. Golden Anchors hängen nicht daran — `tests/trust/test_anchors.py` und die
PageRank-Anker fahren eigene Fixtures. Aber eine bisher grüne Eigenschaft kann auf neu
erreichbaren Welten rot werden. **Das wäre ein Befund und kein Grund zum Zurückdrehen.** Melden.

### E — Verweise umlenken (D136)

Achtzehn Docstring-Zitate zeigen auf die gelöschten Dateien `fuzz-prompt.md` und `sim-prompt.md`.
Sie werden nach dieser Tabelle ersetzt:

| Zitat im Code            | Ziel                |
|--------------------------|---------------------|
| `fuzz-prompt.md §2`      | `werkzeuge.md §4.1` |
| `fuzz-prompt.md §3`      | `werkzeuge.md §4.2` |
| `fuzz-prompt.md §7`      | `werkzeuge.md §2.4` |
| `sim-prompt.md` (ohne §) | `werkzeuge.md §3`   |
| `sim-prompt.md §2`       | `werkzeuge.md §3.1` |
| `sim-prompt.md §3`       | `werkzeuge.md §3.2` |
| `sim-prompt.md §6`       | `werkzeuge.md §3.3` |

Beigefügte Zusätze bleiben unverändert: `02 §7`, `01 §6`, `INV-04.3`, `P-1`. Passt ein Zitat nicht
in die Tabelle, wird es gemeldet und nicht geraten.

## Ausdrückliche Nicht-Ziele

- `tools/autor.py` wird nicht angefasst. `Autor` kennt `t` nicht; es ist Parameter von `signieren`
  und `gabeln`, und der Zähler bleibt nach D129 beim Weltgenerator.
- Kein Produktivcode unter `mensch_als_republik/`.
- Kein dritter Schalter für strukturell ungültige Claims. D133 nennt die Fähigkeit als fehlend;
  sie ist nicht Auftrag dieses Laufs.
- `test_read_claim.py` wird nicht repariert. Sein Ablehnungszweig lebt heute von den zwei Claims
  mit `INCOHERENT_EXPIRY` und ist nach A leer. Das ist erwartet und gehört in die Abnahme, nicht
  in diesen Lauf.
- Golden Anchors werden nicht bewegt — weder in `02-golden-anchors.md` noch in
  `tests/trust/test_anchors.py`. Widerspricht eine Messung dem Prompt: melden, nicht anpassen.
- Keine neuen Eigenschaftstests außer dem einen zu D134 aus Kriterium 2.
- Die Stimmen-Zweige bleiben inhaltlich unverändert; Stimmen tragen kein `t_exp`.

## Abnahmekriterien

1. `make check-all` grün. Zwei pytest-Läufe, also zwei Endzeilen — beide melden. Testzahl vor und
   nach dem Lauf gegriffen, nicht geschätzt.

2. Ein neuer Eigenschaftstest zu D134, der die Buchführung **nicht nachbaut**. Er rechnet mit
   Layer 02s eigener Gruppenbildung:

       classifications = classify_all(store, welt.now)
       groups, _ = build_groups(store.all_claims(), classifications, EX.N_res, D, welt.now)

   und behauptet **beides** (Wirkungsprüfung — die Summe allein reicht nicht, weil die Wirkung nie
   dort liegt, wo die Zahl entsteht):

   - je Autor `Σ group.n_budget <= D`,
   - `derive(...).findings` enthält kein `OVERCOMMITTED_AUTHOR`.

   Gefahren unter `welten(erlaube_ueberzeichnung=False, erlaube_equivocation=True)` — genau der
   Kombination, für die der Nachtrag zu D134 geschrieben ist.

3. **Rücknahmeprobe.** Die Buchführung aus C auf die alte Form zurücknehmen (`remaining[a] -= n`
   je Claim, Ablaufprüfung je Claim) und bestätigen, dass der Test aus 2 **rot** wird. Ergebnis
   melden, dann die Rücknahme verwerfen. Ein Regressionstest, der die Regression nicht sieht, ist
   keiner.

4. `test_t_exp.py::test_finds_budget_exit_via_clock` findet weiterhin eine Welt. Nach C bekommen
   Gruppen häufiger mehrere Mitglieder, und `set(groups_a) < set(groups_b)` verlangt, dass eine
   Gruppe **vollständig** abläuft. Findet `find` keine Welt mehr, ist das ein Befund und wird
   gemeldet — nicht durch Zurückdrehen der Ziehungsreihenfolge behoben.

5. Null Treffer für

       grep -rnE "fuzz-prompt|sim-prompt" tests tools

   Trefferzahl melden.

6. Kein neues `assume` in `welten.py`. Zahl greifen und melden.

7. Die Gewichtung in `_T_EXP_LAGEN` wird gegriffen, nicht geschätzt: 4 abwesend, 4 künftig,
   1 vergangen, 1 grenze.

8. `python tools/check_specs.py` sauber.

## Abschluss

Ein Commit auf `impl/welten`. Kein Merge, kein Push, kein Aufräumen fremder Baustellen.

Was nicht in diesem Prompt steht, wird gemeldet und nicht gebaut. Rückfragen gehen an den
Supervisor, nicht ins Implementierer-Fenster — sie sind Kandidaten für Spec-Lücken.
