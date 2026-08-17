# Werkzeug: Autorschaft, Nachlauf — Implementierungsprompt

Register: D117, D119, D122. Branch: `impl/authoring`, derselbe wie der erste Lauf.
Voraussetzung: Commit `8667671` ist der Ausgangspunkt.

## 1. Auftrag

Fünf Punkte. Die ersten beiden reparieren Befunde der Abnahme, die übrigen drei schließen
die Lücke, die dabei sichtbar wurde. Es ist derselbe Gegenstand.

## 2. Befund A — der Feldtest ist zirkulär

`tests/test_atom.py` prüft heute `set(Claim.__dataclass_fields__)` gegen die im Test
aufgeschriebene Menge `CLAIM_FIELDS`, und `test_build_signed_sets_every_field_when_all_optionals_given`
vergleicht gegen ein handaufgezähltes `expected`.

Beide melden, dass `Claim` sich geändert hat. Keiner stellt sicher, dass `build_signed` ein
neues Feld **durchreicht**. Wer ein Feld hinzufügt und beide Aufzählungen nachzieht, hat zwei
grüne Tests und ein totes Feld — genau die Fehlerklasse, gegen die D122 gebaut wurde.

**Auftrag:** ein Test, der die erwarteten Parameter aus der Signatur ableitet statt aus einer
Liste:

```python
felder = set(Claim.__dataclass_fields__) - {"version", "I", "sigma"}
params = set(inspect.signature(build_signed).parameters) - {"sk"}
assert felder == params
```

Die drei Ausnahmen bekommen je einen Kommentar mit ihrem Grund: `version` ist fest, `I` wird
aus `sk` abgeleitet, `sigma` entsteht beim Signieren. Jedes weitere Feld muss ein Parameter
sein, sonst rot.

`CLAIM_FIELDS` und `test_claim_dataclass_fields_are_exactly_these` bleiben bestehen — als
Alarm auf Änderungen an `Claim` sind sie richtig, nur nicht als Vollständigkeitsprüfung.

`test_build_signed_sets_every_field_when_all_optionals_given` bleibt unverändert.

## 3. Befund B — ein Test trägt den falschen Namen

`test_no_vouch_without_texp_outside_budget_set` erzeugt zwei Identitäten aus demselben Label,
also Selbst-Equivocation. `EQUIVOCATION_FLAGGED` liegt nicht in `BUDGET_STATES`; der Claim
scheitert an `_in_budget_set`, bevor `t_exp` gelesen wird. Geprüft wird der triviale Fall.

**Auftrag, zwei Teile:**

1. Umbenennen in `test_no_vouch_without_texp_on_flagged_author`. Der Test ist richtig, sein
   Name ist es nicht.
2. Neuer Test `test_no_vouch_without_texp_on_expired_vouch`: ein Vouch **mit** `t_exp < NOW`.
   Zu prüfen ist, dass weder ein `VOUCH_WITHOUT_TEXP` fällt noch eine Gruppe für ihn entsteht.

Der zweite Fall ist der einzige, bei dem der Ort des Vermerks falsch sein könnte: der Claim
trägt sein `t_exp` und verlässt das Budget-Set trotzdem — über den Zweig in `_in_budget_set`,
den dessen Docstring als von Layer 01 unabhängig begründet.

## 4. `welten.py` — die `t_exp`-Dimension

Heute übergibt keine Aufrufstelle in `welten()` ein `t_exp`. Jeder erzeugte Vouch trägt
`None`. Zwei Folgen: der Vermerk ist in allen Eigenschaftstests gesättigt und unterscheidet
nichts mehr, und der Budget-Set-Austritt über die Uhr wird generativ nie erreicht.

**Auftrag:** je Vouch wird `t_exp` gezogen, mit Gewichtung **4 : 4 : 1**:

- **abwesend** — `t_exp = None`
- **künftig** — `t_exp > welt.now`
- **vergangen** — `t_exp < welt.now`

Gezogen wird **je Vouch**, nicht je Welt: eine Ziehung je Welt korrelierte den Ablauf über
alle Kanten, und die interessanten Mischgraphen entstünden nie.

Die Ziehung steht **nach** der `n`-Ziehung und außerhalb des Überzeichnungspfads, damit die
Struktur, an der `find()` in `test_p3a` schrumpft, unverändert bleibt.

`now = t_exp` wird **nicht** gezogen. Der Grenzwert gehört `test_p6.py`, wo er ausdrücklich
gezogen wird; ihn hier einzustreuen verteilte dieselbe Aussage auf zwei Orte.

**Stimmen bekommen kein `t_exp`.** `04` kennt keins an `vote@1`, und dieser Lauf macht keine
Governance-Frage auf.

### 4.1 Die Buchhaltung muss mit

Das ist die eigentliche Arbeit. `welten()` führt `remaining[author_i] -= n`. Diese Rechnung
kennt `t_exp` nicht. Ein abgelaufener Vouch fällt aus dem Budget-Set, `remaining` hat ihn aber
abgezogen — der Generator hält das Budget für ausgeschöpft, während `derive()` es frei sieht.

Folge bei `erlaube_ueberzeichnung=True`: `Σ n_budget` wird nur über die nicht abgelaufenen
Vouches gerechnet und rutscht unter `D`. `_p3a_verletzt` findet dann seltener eine Verletzung,
und `test_p3a_finds_overcommit_violation` wird flaky — nicht falsch, sondern unzuverlässig,
und das ist schlimmer.

**Auftrag:** ein Vouch mit vergangenem `t_exp` zieht **nichts** von `remaining` ab. Damit
stimmt der Generator wieder mit `derive()` überein.

## 5. Vorbild-Nachzug

`tests/test_policy.py` und die Profil-Tests unter `tests/profiles/` setzen `t_exp` an ihren
Vouch-Bauten. Nicht aus Korrektheit — der Vermerk ist wirkungslos und die Läufe bleiben grün —,
sondern weil eine Fixture eine Vorlage ist: wer sie liest, baut den nächsten Vouch so nach.

`t_exp` liegt dort jeweils weit jenseits des zugehörigen `now` und nie gleich `now`.

## 6. Der Test auf die neue Dimension

Ein Eigenschaftstest, der belegt, dass der Austritt aus dem Budget-Set über die Uhr generativ
**erreicht** wird — sonst ist die neue Dimension selbst unbewacht und Punkt 4 wäre folgenlos.

Vorschlag: über `find()` eine Welt suchen, in der mindestens ein Vouch ein `t_exp < welt.now`
trägt und in `build_groups` keine Gruppe erzeugt. Findet der Lauf keine, ist **das** der
Befund.

## 7. Verbotene Konstrukte

- Ein festes `t_exp` für alle Vouches in `welten()`. Das ersetzte eine Lücke durch eine andere.
- `now = t_exp` in `welten()`.
- `t_exp` an Stimmen.
- Eine Änderung an `build_signed`, `Claim`, `groups.py` oder `findings.py`. Der erste Lauf hat
  dort das Richtige gebaut; dieser Lauf fasst nur Tests und Generator an.
- Eine Anpassung einer Eigenschaft P-1 bis P-6, um sie grün zu halten. Siehe §8.
- `git add -A`.

## 8. Abnahmekriterium

- **423 Tests grün**, plus die neuen aus §3 und §6.
- Keine Ankerdatei ändert sich.
- `make check` und `make check-all` grün.
- **`make check-all` fünfmal hintereinander**, alle fünf grün. Das prüft, ob `test_p3a` unter
  der neuen Dimension stabil bleibt; ein einzelner grüner Lauf sagt darüber nichts.

**Bricht eine Eigenschaft P-1 bis P-6, ist das ein Halt und eine Rückfrage, keine Reparatur.**
Erwartet wird, dass keine bricht: alle vier vergleichen zwei Läufe über demselben `welt.now`,
und ein abgelaufener Vouch fehlt in beiden gleichermaßen. Bricht dennoch eine, dann hat sie
stillschweigend vorausgesetzt, dass jeder erzeugte Vouch im Budget-Set liegt — und diese
Voraussetzung steht nirgends. Das wäre ein Befund über die Eigenschaft, nicht über den
Generator.

## 9. Abschluss

Commit auf `impl/authoring`, `git add` mit expliziten Pfaden. Rückfragen gehen ins
Spec-Gespräch zurück.
