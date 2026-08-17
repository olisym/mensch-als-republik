# Nachlauf: Halt bei abgefangener Ausnahme (D128)

Branch: **`impl/autor`**, derselbe wie zuvor. Kein neuer Branch, ein weiterer Commit.
Grundlage ist `8a38121`; nichts davon wird zurückgenommen.

Zwei Befunde aus der Abnahme, beide in D128 entschieden. Der Bestand außerhalb von
`tools/autor.py` und `tests/test_autor.py` bleibt unangetastet; die 426 bestehenden Tests dürfen
sich nicht bewegen.

## B-1 — `signieren` hält nicht an, wenn ein Schreibvorgang wirft

**Die Lage.** `signieren` kapselt die vier Schreibvorgänge nicht. Wirft einer von ihnen und fängt
der Aufrufer die Ausnahme, bleibt `_zustand` auf `NORMAL` und `_h_prev` steht je nach Abbruchstelle
auf dem alten Wert. Der nächste `signieren`-Aufruf baut dann einen zweiten Claim auf **dasselbe
`h_prev`** — Selbst-Equivocation, beweisbar und dauerhaft.

`DateiRueckhalt` wirft `OSError` bei vollem Datenträger, bei `EACCES`, bei einer schreibgeschützt
neu eingehängten Partition. Das sind Lagen der Welt und keine Abstürze.

**Die Reparatur.** Die Folge ab `redo_schreiben` in ein `try` fassen. Bei **jeder** Ausnahme:

- `_zustand = Kettenzustand.ANGEHALTEN`
- `_h_prev = None` — damit ein versehentlicher Weiterlauf keine Kette bauen **kann**, statt es
  nur nicht zu dürfen
- `_grund` benennt den abgebrochenen Schritt
- die Ausnahme wird **weitergeworfen**, unverändert. Der Aufrufer muss sie sehen; das Modul
  schluckt nichts.

Einheitlich für alle vier Schritte, auch für `redo_schliessen` (D128, Beschluss 3). Bricht der
letzte ab, ist die Lage sachlich unbedenklich — der Halt kostet dort ein `wiederaufnehmen` und
nichts sonst, weil die Wiederaufnahme idempotent ist. Eine Fallunterscheidung nach Schritt wäre
eine Behauptung darüber, was der abgebrochene Schritt bereits bewirkt hat, und die kann das Objekt
nicht prüfen.

`build_signed` steht **außerhalb** des `try`: es schreibt nichts, und eine Ausnahme dort ist ein
Programmierfehler nach D92 und keine Lage der Welt.

**Der Test.** Ein neuer Vektor, parametrisiert über dieselben `k = 1..4` und beide Rückhalte. Er
unterscheidet sich vom bestehenden `test_absturzaufzaehlung` in **genau einer** Größe: der
gebrochene `Autor` wird weiterbenutzt, statt einen frischen zu bauen.

Für jedes `k`:

1. Aufbau wie bisher: zwei Claims, dann der dritte mit Bruch bei `k`.
2. `Bruch` abfangen.
3. **Derselbe** `Autor`, zweiter `signieren`-Aufruf mit anderem `t` ⇒ `KetteAngehalten`.
4. Weder Ausgang noch Rückhalt haben sich durch Schritt 3 verändert.
5. Ein frischer `Autor` über demselben Rückhalt und Ausgang nimmt wieder auf und schreibt weiter,
   und die Kette bleibt forkfrei — der Halt ist eine Sperre am Objekt und keine Beschädigung des
   dauerhaften Zustands.

Schritt 5 ist der Teil, der zeigt, dass die Reparatur nichts kaputtmacht. Ohne ihn belegte der
Test nur, dass etwas verweigert wird.

## B-2 — Der Halt klebt nicht, und das ist richtig

**Die Lage.** Der vorige Prompt verlangte „nach `ANGEHALTEN` bleibt jeder weitere Aufruf
`ANGEHALTEN`". Die Umsetzung leitet den Zustand bei jedem `wiederaufnehmen` neu ab. Für den fremden
Redo hält das, weil der Redo offen bleibt; für Ausgang 4 heilt der Halt, sobald der fehlende Claim
nachgeliefert ist.

**Die Abweichung ist richtig und wird normativ** (D128, Beschluss 1). Ausgang 4 sagt „der Ausgang
kennt die Spitze nicht" — eine Aussage über den Ausgang, nicht über die Kette. Am Code ist nichts
zu ändern.

**Zwei Tests** machen die Entscheidung sichtbar, statt sie stillschweigend zu lassen:

- **Heilung:** Zustand `ANGEHALTEN` über Ausgang 4 herstellen, den fehlenden Claim in denselben
  Ausgang nachliefern, erneut `wiederaufnehmen` ⇒ `NORMAL` mit der Spitze als `h_prev`, und
  `signieren` läuft wieder.
- **Keine Heilung:** der bestehende `test_fremder_redo_haelt_an` bekommt eine Zeile, die zeigt,
  dass auch ein gefüllter Ausgang daran nichts ändert — solange der Redo offen ist, bleibt es
  `ANGEHALTEN`.

Beide zusammen sind „zwei Läufe, eine Variable": derselbe Halt, einmal heilbar und einmal nicht,
und der Unterschied ist genau, ob die Ursache sich von selbst ändern kann.

## Kleinigkeit ohne Befundcharakter

`test_oberflaeche_gibt_weder_seed_noch_schluessel_noch_spitze` ruft `wiederaufnehmen()` innerhalb
der Schleife über die öffentlichen Namen tatsächlich auf. Folgenlos, weil die Operation idempotent
ist — aber das ist Glück und nicht Absicht. Eine Zeile in den Docstring, die festhält, dass die
Prüfung auf der Idempotenz von `wiederaufnehmen` ruht und dass die Spitze nur über
`Wiederaufnahme.h_prev` sichtbar ist, damit niemand den Test später für stärker hält, als er ist.

## Was nicht Teil dieses Laufs ist

- Jede Änderung an `mensch_als_republik/`, `tools/example_nucleus.py`, `tests/helpers.py`,
  `tools/sim/`.
- Der Umzug der drei bestehenden Kettenfortführungen. Eigener Lauf.
- Ausgang 5 aus D120, der Einlesepfad (D121), der Sicherungsblob.
- Jede Änderung an bestehenden Zusicherungen in `tests/test_autor.py`. Ergänzen ja, umschreiben
  nein — wird eine bestehende Zusicherung durch die Reparatur falsch, ist das ein Befund und
  gehört gemeldet.

## Rückfragen

An den Spec-Supervisor, nicht ins eigene Fenster. Insbesondere, wenn der Halt aus Schritt 3 einen
bestehenden Test rot macht, oder wenn sich der gebrochene `Autor` nicht weiterbenutzen lässt, ohne
den Zählinjektor umzubauen.

## Abschluss

```
make check
git add tools/autor.py tests/test_autor.py
git commit
```

`git add` **nach** `make check`: beide Dateien sind bereits versioniert, es entsteht keine neue.
Erwartet: 450 + rund zehn neue Tests, alle grün.
