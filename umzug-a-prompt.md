# Umzugslauf A: `gabeln` und die drei Speicher-Kettenfortführungen (D127, D129)

Branch: `impl/umzug-a`. Ein Commit am Ende.

## Was dieser Lauf tut

1. Ergänzt `tools/autor.py` um die Operation `gabeln`.
2. Zieht `tests/helpers.py`, `tools/example_nucleus.py` und `tests/property/welten.py` auf
   `tools.autor.Autor` um.

`tools/sim/welt.py` und `tools/sim/szenario.py` bleiben **unangetastet** — Lauf B.

**Dies ist eine reine Refaktorierung.** Kein Claim darf sich um ein Byte ändern. Jede Abweichung
in einer `claim_id`, einem Anker oder einer Findings-Liste ist ein **Befund** und kein Anlass,
eine Erwartung anzupassen.

## 1. `gabeln` in `tools/autor.py`

```
def gabeln(self, *, p, J, t, v=None, N=None, t_exp=None) -> Claim
```

Gleiche Argumente wie `signieren`. Verhalten:

- dieselben Wächter wie `signieren`: kein vorheriges `wiederaufnehmen` ⇒ `RuntimeError`,
  Zustand `ANGEHALTEN` ⇒ `KetteAngehalten` (D128).
- signiert über die **aktuelle** Spitze,
- ruft `ausgang.aufnehmen(signed)`,
- **schreibt weder Redo noch Spitze** und rückt `_h_prev` **nicht** vor.

Der letzte Punkt trägt die Operation allein und gehört als Begründung in den Docstring (D129):
schriebe `gabeln` einen Redo, machte ein späteres `wiederaufnehmen` den absichtlichen Fork zur
echten Spitze — der Zwilling würde still zum Hauptzweig. Schriebe es die Spitze, wäre es kein Fork.

Da `gabeln` den Rückhalt nicht berührt, ist ein Abbruch in `ausgang.aufnehmen` folgenlos für die
Kette; ein `try` mit Halt wie in `signieren` ist hier **nicht** nötig und soll nicht eingebaut
werden. Der Docstring hält fest, warum.

**Tests** in `tests/test_autor.py`, über beide Rückhalte:

- `gabeln` nach zwei Claims: der gegabelte Claim trägt dasselbe `h_prev` wie der nächste reguläre;
  beide liegen im Ausgang; Spitze und Redo sind unverändert.
- Nach `gabeln` legt `signieren` regulär an derselben Stelle an, und ein anschließendes
  `wiederaufnehmen` liefert die Spitze des **regulären** Claims, nicht die des gegabelten.
  Das ist der Test, der die Begründung prüft und nicht nur die Wirkung.
- `gabeln` ohne vorheriges `wiederaufnehmen` ⇒ `RuntimeError`; im Zustand `ANGEHALTEN` ⇒
  `KetteAngehalten`, und der Ausgang bleibt unverändert.

## 2. Umzug — allgemeine Auflage

Die vier öffentlichen Oberflächen bleiben **identisch**: `Identity` (mit `vouch`, `vouch_raw`,
`claim`, `revoke`, `supersede`, `pub`, `label`), `_Author` (mit `claim`, `vouch`, `pub`), `_Signer`
(mit `claim`, `pub`). Keine Signatur, kein Argumentname, keine Voreinstellung ändert sich. Die 26
Testdateien, die sie benutzen, dürfen **nicht** angefasst werden.

Aus jeder der drei Dateien verschwinden `build_signed`, `id_genesis_anchor`, `_h_prev` und die
Ed25519-Konstruktion. Jede Klasse hält stattdessen einen `Autor` über `SpeicherRueckhalt` und
einen **privaten** `StoreAusgang(InMemoryStore())`, dessen Inhalt niemand liest, und ruft
`wiederaufnehmen()` einmal im Konstruktor.

Der Wegwerf-Ausgang ist Absicht: `Identity.vouch()` legt heute nichts ab, und die Tests wählen mit
`store_with(...)` selbst, was ein Beobachter kennt — darin liegt ihre Kraft, etwa für
`pending`-Fälle. Ein Ausgang, dessen `kennt` lügt, wäre die schlechtere Wahl: der Port trüge eine
Unwahrheit für einen Zweck, den er nicht hat.

### 2.1 `tests/helpers.py`

`Identity._append` wird ein Aufruf von `autor.signieren`. Alles andere bleibt.

### 2.2 `tools/example_nucleus.py`

`_Author.claim` wird ein Aufruf von `autor.signieren`. `_Author` bleibt der Feldtyp in beiden
Dataclasses (Zeilen 185–188 und 409–412) und der Parametertyp in `_vote` und `_accept`; an diesen
Stellen ändert sich nichts.

### 2.3 `tests/property/welten.py`

`_Signer.claim` behält seinen Parameter `kette_fortschreiben` — er ist hier ein Argument des
Generators und keine Signieroberfläche — und verzweigt:

```
kette_fortschreiben=True   -> autor.signieren(...)
kette_fortschreiben=False  -> autor.gabeln(...)
```

Der Zähler `self._t` bleibt bei `_Signer` und wird wie bisher vor jedem Claim erhöht; `t` geht als
Parameter an `signieren` bzw. `gabeln` (D129).

Achte auf die Reihenfolge im Zwillingsfall: der **erste** Claim wird mit
`kette_fortschreiben=False` erzeugt, also gegabelt, und der **zweite** hängt regulär an. Das ist
die bestehende Semantik und bleibt es.

## 3. Abnahmekriterien

Zwei abgeleitete Kriterien statt einer Aufzählung (D129):

```
grep -rn "_h_prev" tools/ tests/          # nur Fundstellen in tools/autor.py
grep -rn "build_signed\|id_genesis_anchor" tests/helpers.py tools/example_nucleus.py tests/property/welten.py
```

Der zweite Befehl muss leer bleiben. Findet der erste etwas außerhalb von `tools/autor.py`, ist
der Umzug unvollständig.

Dazu:

- `make check-all` grün — **zwei** pytest-Läufe, also zwei Endzeilen: 468 + die neuen
  `gabeln`-Tests, und elf Eigenschaftstests unter `MAR_HYPOTHESIS=voll`.
- `git diff main --stat` zeigt **genau vier** geänderte Dateien: `tools/autor.py`,
  `tests/test_autor.py`, `tests/helpers.py`, `tools/example_nucleus.py`, `tests/property/welten.py`
  — also fünf. Steht dort eine sechste, ist eine Oberfläche gebrochen worden.

## 4. Was nicht Teil dieses Laufs ist

- `tools/sim/welt.py`, `tools/sim/szenario.py`, `tools/sim/scenarios/*.json`. Lauf B.
- **B-4**: die Zwillingsbuchführung in `welten()` zieht kein Budget ab. Bekannter offener Befund,
  wird hier **nicht** repariert (D129) — sonst weiß die Abnahme bei einer Ankerabweichung nicht,
  welche der beiden Änderungen sie bewegt hat.
- Jede Änderung an `mensch_als_republik/`.
- Jede Änderung an einer der 26 Testdateien, die `Identity` oder `store_with` benutzen.

## 5. Rückfragen

An den Spec-Supervisor. Insbesondere:

- wenn eine `claim_id`, ein Anker oder eine Findings-Liste sich bewegt,
- wenn eine der drei Oberflächen sich nicht erhalten lässt, ohne `Autor` zu erweitern,
- wenn `wiederaufnehmen()` im Konstruktor eine bestehende Erwartung an die Konstruktionskosten
  bricht (etwa in einer Hypothesis-Strategie, die viele `_Signer` baut).

## 6. Abschluss

```
make check-all
git add tools/autor.py tests/test_autor.py tests/helpers.py tools/example_nucleus.py tests/property/welten.py
git commit
```

`git add` nach `make check-all`: alle fünf Dateien sind bereits versioniert, es entsteht keine
neue.
