# Abnahme: Werkzeugschicht Autorschaft

Läufe: `8667671`, `3fe4e27`, `36f1481` auf `impl/authoring`.
Register: D117, D119, D122. Grundlage: `authoring-prompt.md`, `authoring-nachlauf-prompt.md`.

## 1. Ergebnis

Angenommen. 426 Tests grün (415 vor dem Lauf, 8 aus Lauf 1, 3 aus Lauf 2). `make check` und
`make check-all` grün. `test-prop` unter `MAR_HYPOTHESIS=voll` fünfmal hintereinander grün, alle
elf Eigenschaften stabil. Keine Ankerdatei geändert, kein `DOC_`-Wert im Beispielnukleus
verschoben.

## 2. Was gebaut wurde

- `build_signed` in `atom.py`: `I` aus dem Schlüssel abgeleitet, `sigma` über
  `dataclasses.replace`. Sechs Zeilen, keine zweite Prüfung neben `Claim.__post_init__`.
- `VOUCH_WITHOUT_TEXP` in `groups.py`, nach dem Payload-Zweig, ohne eigenes `continue`. Der
  Vouch geht unverändert in `members` und behält `n_budget` und `n_kante`.
- `t_exp` an allen Erzeugerstellen; `welten()` zieht es je Vouch im Verhältnis 4 : 4 : 1.

## 3. Fünf Helferschnitte statt einem

Der Prompt schnitt `_Author`. Gezogen wurden fünf: `_Author`, `Identity` (`tests/helpers.py`),
`_Signer` (`welten.py`), `tests/vectors/gen.py`, `tools/sim/welt.py`. Autorisiert war das durch
eine Zeile in §7 — "eine Handaufzählung der Felder beim Signieren, **an welcher Stelle auch
immer**".

**Das Verbot hat die Arbeit getan, die der Schnitt nicht getan hat.** Die Schnitttabelle in D122
nannte nur `_Author`; ohne diese Formel wären vier zweite Kodierwege stehengeblieben, und der
Feldtest hätte die halbe Fläche bewacht.

**Konsequenz — Geschwisterformel.** Ein Verbot, das mit "an welcher Stelle auch immer" endet,
fängt Geschwister, die eine Aufzählung nicht kennt. Es ist billiger als eine vollständige Liste
und schlägt in die Richtung aus, in die Regel 5 zeigt. Wo ein Prompt eine Stelle nennt, ist zu
fragen, ob die zugehörige Regel ortsunabhängig formuliert werden kann.

## 4. Befunde

### B-1 — der Feldtest war zirkulär (repariert)

`set(Claim.__dataclass_fields__) == CLAIM_FIELDS` meldet Änderungen an `Claim` und stellt nichts
über `build_signed` sicher. Wer ein Feld hinzufügt und beide Aufzählungen nachzieht, hat zwei
grüne Tests und ein totes Feld — die Klasse, gegen die D122 gebaut wurde.

Repariert: die erwarteten Parameter kommen aus `inspect.signature(build_signed)`, abzüglich
`version` (fest), `I` (aus `sk`) und `sigma` (entsteht). Der zirkuläre Test bleibt als Alarm auf
Änderungen an `Claim` — dafür ist er richtig.

### B-2 — ein Test trug den falschen Namen (repariert)

`test_no_vouch_without_texp_outside_budget_set` erzeugte Selbst-Equivocation.
`EQUIVOCATION_FLAGGED` liegt nicht in `BUDGET_STATES`; der Claim scheiterte an `_in_budget_set`,
bevor `t_exp` gelesen wurde. Geprüft wurde der triviale Fall.

Umbenannt in `..._on_flagged_author`. Neu: `..._on_expired_vouch` mit `t_exp < NOW` — der
einzige Fall, in dem der Ort des Vermerks falsch sein könnte, weil der Claim sein `t_exp` trägt
und das Budget-Set trotzdem über die Uhr verlässt.

### B-3 — das Prädikat prüfte zu wenig (repariert)

`_austritt_ueber_uhr` prüfte, ob der Gruppenschlüssel `(I, J)` fehlt. Zu grob in beide
Richtungen: ein fehlender Schlüssel kann auch von defektem `v` kommen, und ein zweiter,
nicht abgelaufener Vouch derselben Gruppe verdeckt den Austritt.

Repariert: zwei Läufe über derselben Claim-Menge, unterschieden allein durch `now`; das Prädikat
verlangt eine echte Teilmenge. Damit hängt die Aussage an der Uhr und an keiner Voreinstellung
von `welten()`.

### B-4 — Zwillingsbuchführung ohne Budgetabzug (getragene Grenze)

Bei `erlaube_equivocation=True` zieht der Zwilling ein eigenes `t_exp2`, ohne `remaining`
anzufassen. Trägt der erste Claim ein vergangenes und der Zwilling ein künftiges `t_exp`, fällt
der erste aus dem Budget-Set, der Zwilling bleibt — abgezogen wurde für keinen. Der Generator
unterschätzt das gebundene Budget.

Wirksam nur bei `erlaube_ueberzeichnung=False` **und** `erlaube_equivocation=True`. Diese
Kombination benutzt heute keine Eigenschaft: P-2 und P-5 setzen beide auf `False`, P-3b prüft
Auszählung und keine Budgets.

**Nicht repariert, mit Grund.** Eine Änderung an der Zwillingsbuchführung verschiebt Ziehungen
und damit die Struktur, an der `find()` in `test_p3a` schrumpft — für einen Fall, den niemand
benutzt. Wer eine Eigenschaft über dieser Kombination schreibt, repariert es zuerst.

## 5. Ablauf ist keine Wissensdimension

Alle vier `welten()`-Eigenschaften vergleichen zwei Läufe über **demselben `welt.now`**: P-1
Reihenfolge, P-2, P-3a und P-5 Teilmenge gegen Vollmenge. Ein abgelaufener Vouch fehlt in beiden
Läufen gleichermaßen. Ablauf verschiebt den Graphen, aber symmetrisch.

Deshalb halten P-1 bis P-6 unter der neuen Dimension, und deshalb ist `t_exp` **nicht** die
dritte Nicht-Monotonie neben D118 und dem fehlenden Widerruf. Jene entstehen, weil ein
*hinzukommender* Claim etwas kippt. Ablauf kommt nicht hinzu — er ist von Anfang an da.

Die Aussage gehört hierher und nicht in den Lauf: sie ist eine über die Eigenschaften, nicht
über diese Implementierung.

## 6. Was offen bleibt

- **B-4**, wie oben.
- **Der Gleichstandsfall** bei `kante_claim_id`: `test_groups.py:196` und
  `test_pagerank_groups.py:22` tragen zwei aktive Vouches derselben Gruppe mit gleichem `n`. Der
  Bruch über `sorted(...)[0]` wurde nie gestört, weil dort schon vorher `t_exp=T_EXP` stand. Kein
  Vektor fehlt; die Reihenfolge ist aber von nichts geprüft. Gehört in den nächsten `02`-Durchgang.
- **D120 und D121** — Persistenz der Kettenspitze, Redo-Log, Einlesepfad, Bündelformat. Nicht
  angefasst, wie im Prompt festgelegt.
