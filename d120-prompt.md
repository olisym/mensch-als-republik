# Implementierungslauf: Autorenkette mit Persistenz (D120, D122, D127)

Branch: `impl/autor`. Ein Commit am Ende, nie „gestaged, nicht committet".

## Was dieser Lauf tut

Er baut **ein neues Modul** `tools/autor.py` und **eine neue Testdatei** `tests/test_autor.py`.

Er ändert **nichts** am Bestand. `tools/example_nucleus.py`, `tests/helpers.py` und
`tools/sim/welt.py` bleiben unangetastet — deren Umzug auf das neue Modul ist ein eigener Lauf.
Die 426 bestehenden Tests müssen unverändert grün bleiben; wird auch nur einer rot, ist das ein
Befund und kein Anlass, ihn anzupassen.

Es entstehen **keine neuen Golden Anchors** und keine neuen Zahlen in Ankerdateien. Die Referenz
für jede Prüfung ist der ungestörte Lauf derselben Eingabe (D127, „zwei Läufe, eine Variable").

## Warum

`_Author.claim` (`example_nucleus.py`), `Identity._append` (`tests/helpers.py`) und
`Teilnehmer.claim_signieren` (`tools/sim/welt.py`) führen die Kettenspitze je selbst fort. Alle
drei rücken sie bei der Konstruktion vor, unabhängig davon, ob der Claim je gespeichert oder
ausgesandt wird. In einem Prozess harmlos, für ein dauerhaftes Werkzeug nicht: ein Absturz
zwischen Aussenden und Spitze-Festschreiben erzeugt einen zweiten Claim auf dasselbe `h_prev` —
Equivocation gegen sich selbst, beweisbar und dauerhaft.

D120 legt die Ordnung fest, D127 den Ort. Dieses Modul ist beides zusammen.

## Ort und Abhängigkeiten

`tools/autor.py`. `pythonpath = ["."]` in `pyproject.toml` macht `tools.autor` importierbar, wie
bei `tools.sim`. Nur `cbor2`, `cryptography` und die Standardbibliothek. Kein `float`, kein
`fractions`. Kein Aufruf einer Systemuhr: `t` ist überall Parameter.

Aus dem Paket verwendet werden ausschließlich `mensch_als_republik.atom`:
`Claim`, `build_signed`, `claim_id`, `claim_from_bytes`, `id_genesis_anchor`, `signed_bytes`.
Das Modul **rechnet keine Core-Bytes und baut keinen Claim von Hand**; jeder Claim entsteht über
`build_signed` (D122).

## 1. Die zwei Ports

Zwei `typing.Protocol`. Beide sind bewusst dumm — sie tragen **keine** Protokollsemantik und
rechnen insbesondere **nie** `h_prev` (D127, Beschluss 1).

```
class Rueckhalt(Protocol):
    def spitze_lesen(self) -> bytes | None: ...
    def spitze_schreiben(self, h_prev: bytes) -> None: ...
    def redo_lesen(self) -> bytes | None: ...
    def redo_schreiben(self, signiert: bytes) -> None: ...
    def redo_schliessen(self) -> None: ...

class Ausgang(Protocol):
    def kennt(self, cid: bytes) -> bool: ...
    def aufnehmen(self, claim: Claim) -> None: ...
```

`spitze_lesen` und `redo_lesen` liefern `None`, wenn nichts da ist. `redo_schliessen` auf einen
bereits geschlossenen Redo ist erlaubt und tut nichts.

Zwei Implementierungen von `Rueckhalt`:

- **`SpeicherRueckhalt`** — zwei Attribute, sonst nichts.
- **`DateiRueckhalt(pfad: Path)`** — zwei Dateien: `spitze` (Hex, ASCII) und `redo` (rohe Bytes).
  Jeder Schreibvorgang: in eine Temporärdatei im **selben** Verzeichnis schreiben, `flush`,
  `os.fsync` auf den Dateideskriptor, `os.replace` auf den Zielnamen, dann `os.fsync` auf den
  Verzeichnisdeskriptor. `redo_schliessen` ist `unlink` (fehlertolerant, wenn nicht vorhanden)
  gefolgt von `fsync` des Verzeichnisses.

  Der Modul-Docstring benennt die drei vorausgesetzten Persistenzeigenschaften — atomares
  `os.replace`, `fsync` der Datei vor dem Rename, `fsync` des Verzeichnisses danach — und
  vermerkt, dass sie **nicht geprüft** sind (D127, getragene Grenze).

Eine Implementierung von `Ausgang` genügt für diesen Lauf: **`StoreAusgang`**, ein dünner Adapter
über `mensch_als_republik.verifier.InMemoryStore`. Falls `InMemoryStore` keine Abfrage nach
`claim_id` anbietet, halte an und frage nach — das ist eine Spec-Lücke und keine Gelegenheit, im
Paket etwas hinzuzufügen.

## 2. Der Zustand

```
class Kettenzustand(Enum):
    GENESIS       # nichts vorhanden, h_prev = id_genesis_anchor(pub)
    NORMAL        # Spitze gesetzt und im Ausgang bekannt
    FORTGESETZT   # ein offener Redo wurde abgeschlossen
    ANGEHALTEN    # es darf nicht weitergeschrieben werden

@dataclass(frozen=True, slots=True)
class Wiederaufnahme:
    zustand: Kettenzustand
    h_prev: bytes | None      # None genau dann, wenn ANGEHALTEN
    grund: str | None         # gesetzt genau dann, wenn ANGEHALTEN
```

## 3. `Autor`

```
class Autor:
    def __init__(self, seed: bytes, rueckhalt: Rueckhalt, ausgang: Ausgang) -> None
    pub: bytes
    def wiederaufnehmen(self) -> Wiederaufnahme
    def signieren(self, *, p, J, t, v=None, N=None, t_exp=None) -> Claim
```

**`__init__` fasst den Rückhalt nicht an.** Es leitet nur `pub` ab. Wer `signieren` aufruft, ohne
vorher `wiederaufnehmen` aufgerufen zu haben, bekommt einen `RuntimeError` — ein Programmierfehler
nach D92, keine Lage der Welt.

**Oberflächenregel (D122).** `Autor` gibt weder den Schlüssel noch die Spitze heraus. Öffentlich
sind genau `pub`, `wiederaufnehmen`, `signieren`. Kein `h_prev`-Attribut, kein Getter, keine
Property. Der Zustand wird über den Rückgabewert von `wiederaufnehmen` sichtbar und sonst nirgends.

**Nicht in diesem Lauf:** eine Operation, die signiert **ohne** die Spitze fortzuschreiben. Die
Simulation braucht sie, um absichtlich zu equivozieren; sie entsteht mit dem Umzug von `welt.py`
und trägt dann einen eigenen Namen. Baue sie hier nicht, auch nicht als Flag.

### `wiederaufnehmen()`

Die Reihenfolge ist normativ (D127, Beschluss 3): **erst der Redo, dann die Spitze.**

```
redo = rueckhalt.redo_lesen()
wenn redo vorhanden:
    claim = claim_from_bytes(redo)
    wenn claim.I != self.pub                -> ANGEHALTEN, grund benannt
    cid = claim_id(claim)
    wenn nicht ausgang.kennt(cid): ausgang.aufnehmen(claim)
    rueckhalt.spitze_schreiben(cid)
    rueckhalt.redo_schliessen()
    -> FORTGESETZT, h_prev = cid

spitze = rueckhalt.spitze_lesen()
wenn spitze ist None                        -> GENESIS, h_prev = id_genesis_anchor(pub)
wenn nicht ausgang.kennt(spitze)            -> ANGEHALTEN, grund benannt
sonst                                       -> NORMAL, h_prev = spitze
```

Wirft `claim_from_bytes` auf den eigenen Redo, ist das ein Programmierfehler und **kein**
Reject-Code: eigene Bytes sind keine Lage der Welt (D121, Abgrenzung zu D92). Fange die Ausnahme
nicht ab.

`wiederaufnehmen` ist **idempotent**: ein zweiter Aufruf direkt danach liefert denselben Zustand
bis auf `FORTGESETZT`, das beim zweiten Mal zu `NORMAL` wird, und dieselbe `h_prev`. Nach
`ANGEHALTEN` bleibt jeder weitere Aufruf `ANGEHALTEN`.

### `signieren()`

Vier Schreibvorgänge, in genau dieser Reihenfolge (D120):

```
1. signed = build_signed(sk, J=J, p=p, t=t, h_prev=<aktuelle Spitze>, v=v, N=N, t_exp=t_exp)
2. rueckhalt.redo_schreiben(signed_bytes(signed))
3. ausgang.aufnehmen(signed)
4. rueckhalt.spitze_schreiben(claim_id(signed))
5. rueckhalt.redo_schliessen()
```

Schritt 1 schreibt nichts und ist nach einem Absturz folgenlos. Die interne Spitze wird **erst
nach Schritt 4** vorgerückt.

Ist der Zustand `ANGEHALTEN`, wirft `signieren` `KetteAngehalten` (im Modul definiert) und schreibt
nichts. **Anhalten, nicht warnen:** Weiterschreiben ist genau der Fehler, den die Prüfung erkannt
hat.

## 4. Tests — `tests/test_autor.py`

### 4.1 Vertragstest über beide Rückhalte

Eine `pytest.fixture(params=...)`, die `SpeicherRueckhalt` und `DateiRueckhalt(tmp_path)` liefert.
**Jeder** Test dieser Datei läuft über beide. Kein Test darf einen Rückhalt bevorzugen.

Mindestens:

- Genesis: frischer Rückhalt ⇒ `GENESIS`, `h_prev == id_genesis_anchor(pub)`.
- Drei Claims hintereinander: jedes `h_prev` ist die `claim_id` des Vorgängers; alle drei im
  Ausgang; die Spitze ist die letzte `claim_id`.
- Neustart: ein zweiter `Autor` über **demselben** Rückhalt und Ausgang nimmt mit `NORMAL` auf und
  hängt an derselben Stelle an wie der erste es getan hätte.
- Ausgang 4: Spitze gesetzt, Ausgang kennt sie nicht ⇒ `ANGEHALTEN`; `signieren` wirft und
  schreibt nichts.
- Fremder Redo: ein Redo mit `claim.I != pub` ⇒ `ANGEHALTEN`.
- `signieren` vor `wiederaufnehmen` ⇒ `RuntimeError`.

### 4.2 Absturzaufzählung

Ein Testhelfer, der **beide** Ports umhüllt und einen gemeinsamen Zähler über alle
Schreiboperationen führt (`redo_schreiben`, `aufnehmen`, `spitze_schreiben`, `redo_schliessen`);
beim k-ten Aufruf wirft er `Bruch`. Lesende Operationen zählen nicht.

Für `k` in `1..4` und zusätzlich den ungestörten Lauf:

1. Aufbau: ein Autor, zwei bereits geschriebene Claims, dann der dritte mit Bruch bei `k`.
2. Neuer Autor über demselben Rückhalt und Ausgang, `wiederaufnehmen()`.
3. Prüfungen — alle gegen den **ungestörten** Lauf derselben Eingabe:
   - Der Ausgang enthält entweder genau die zwei Vorgänger oder genau die zwei plus den dritten,
     und der dritte ist **byteweise identisch** mit dem des ungestörten Laufs.
   - Keine zwei Claims mit `I == pub` tragen dasselbe `h_prev`.
   - Die Spitze ist die `claim_id` des letzten Claims der Kette im Ausgang.
   - Ein zweites `wiederaufnehmen()` ändert weder Ausgang noch Spitze.
   - Nach der Wiederaufnahme lässt sich weiterschreiben, und der Folge-Claim hängt an der
     richtigen Spitze.

Erwartet — als Tabelle im Test dokumentiert, nicht als Zufallsbefund:

| k | gebrochen bei | Zustand danach | Claim im Ausgang |
|---|---|---|---|
| 1 | Redo schreiben | `GENESIS`/`NORMAL` | nein |
| 2 | Aussenden | `FORTGESETZT` | ja |
| 3 | Spitze schreiben | `FORTGESETZT` | ja |
| 4 | Redo schließen | `FORTGESETZT` | ja |
| – | ungestört | `NORMAL` | ja |

Bei `k = 1` gilt zusätzlich: ein erneutes `signieren` mit **demselben** `t` und denselben Feldern
erzeugt einen byteweise identischen Claim. Das ist die Idempotenz aus D120, und sie folgt daraus,
dass Ed25519 deterministisch signiert.

### 4.3 Oberflächenregel

Ein Test, der die öffentliche Fläche **ableitet** statt sie aufzuzählen: iteriere über alle
Attributnamen von `Autor`, die nicht mit `_` beginnen, und stelle sicher, dass keiner davon —
gelesen oder ohne Argumente aufgerufen — den Seed, den privaten Schlüssel oder die aktuelle Spitze
zurückgibt. Eine feste Liste erlaubter Namen im Test wäre dieselbe Schwäche wie die, die der Test
prüft (D122).

## 5. Was ausdrücklich nicht Teil dieses Laufs ist

- Jede Änderung an `mensch_als_republik/`.
- Jede Änderung an `tools/example_nucleus.py`, `tests/helpers.py`, `tools/sim/`.
- Ausgang 5 aus D120 (zwei eigene Claims auf dieselbe Spitze). Vertagt in D127, mit Begründung.
- Ein Einlesepfad für fremde Bytes (D121).
- Ein Sicherungsblob mit Seed und Spitze.
- Prüfungen gegen echte Dateisystem-Absturzzustände. `DateiRueckhalt` trägt seine Annahmen als
  benannte Grenze; er belegt sie nicht.

## 6. Rückfragen

Jede Rückfrage geht an den Spec-Supervisor, nicht in das eigene Fenster. Sie sind Kandidaten für
den Entscheidungsregister und keine Ermessensfragen. Insbesondere:

- wenn `InMemoryStore` keine Abfrage nach `claim_id` anbietet,
- wenn `signed_bytes` nicht das liefert, was `claim_from_bytes` wieder einliest,
- wenn eine der vier Schreiboperationen sich nicht sinnvoll zählen lässt,
- wenn ein bestehender Test rot wird.

## 7. Abschluss

```
git add tools/autor.py tests/test_autor.py
make check
git commit
```

`git add` **vor** `make check`: `check_tree.py` schlägt bei unversionierten Quelldateien fehl, und
zwei neue Dateien sind zwangsläufig unversioniert. Erwartet: 426 + die neuen Tests, alle grün,
Spec-Linter unverändert.
