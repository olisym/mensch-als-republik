# Werkzeug: Autorschaft — Implementierungsprompt

Register: D119, D122. Branch: `impl/authoring`.

## 1. Auftrag

Drei Dinge, die dieselbe Funktion anfassen und deshalb in einem Lauf gehören:

- **A** — eine Bauform für signierte Claims im Paket, die kein Feld verlieren kann (D122).
- **B** — `_Author` in `tools/example_nucleus.py` auf Schlüsselhaltung und Kettenspitze
  reduzieren; Bau und Signatur kommen aus dem Paket (D122).
- **C** — der Vermerk `VOUCH_WITHOUT_TEXP` und `t_exp` an allen drei Erzeugerstellen (D119).

**Nicht in diesem Lauf:** Persistenz der Kettenspitze, Redo-Log, Einlesepfad für fremde Bytes,
Bündelformat. Diese hängen an D120 und D121 und bekommen einen eigenen Lauf.

## 2. Teil A — `build_signed` in `mensch_als_republik/atom.py`

```python
def build_signed(
    sk: Ed25519PrivateKey,
    *,
    J: tuple[int, bytes],
    p: str,
    t: int,
    h_prev: bytes,
    v: bytes | None = None,
    N: bytes | None = None,
    t_exp: int | None = None,
) -> Claim: ...
```

- `I` wird aus `sk` abgeleitet (`sk.public_key().public_bytes_raw()`) und ist **kein**
  Parameter. Ein Schlüssel, der nicht zu einem übergebenen `I` gehört, ist damit nicht
  darstellbar — die Zugehörigkeit entfällt, statt geprüft zu werden.
- `version` ist `1`.
- Der Ablauf ist: unsignierten `Claim` bauen, dann
  `dataclasses.replace(unsigned, sigma=sign(sk, unsigned))`. **Keine** Handaufzählung der
  Felder bei der zweiten Konstruktion.
- Keine Vorgabe, keine Ergänzung, keine Prüfung über das hinaus, was `Claim.__post_init__`
  bereits tut. Die Funktion ist dünn.

Ort ist `atom.py` und keine neue Datei: `sign()` und `core_bytes()` stehen dort bereits, und ein
eigenes Modul mit einer Funktion importierte ohnehin alles aus `atom`.

## 3. Teil B — `_Author` im Beispielnukleus

`_Author` behält genau zwei Aufgaben: den Schlüssel halten und die Kettenspitze führen.

- `_Author.claim(...)` ruft `build_signed(...)` und setzt danach `self._h_prev = claim_id(...)`.
  Die Doppelkonstruktion in `_Author` entfällt vollständig.
- `_Author.claim(...)` bekommt `t_exp: int | None = None` durchgereicht.
- `_Author.vouch(...)` bekommt `t_exp: int` als **Pflicht-Keyword** — ohne Default. Ein Vouch
  ohne Ablaufzeit ist nach `02 §6.2` in einem Scope mit Budgetregel spec-widrig, und jeder Scope
  trägt sie heute (D119). Die Pflicht findet zugleich alle Aufrufstellen.

## 4. Teil C — der Vermerk

`mensch_als_republik/trust/findings.py`:

```python
VOUCH_WITHOUT_TEXP = "VOUCH_WITHOUT_TEXP"
```

`mensch_als_republik/trust/groups.py`, in der Schleife von `build_groups`, **nach** dem
erfolgreichen `_decode_weight` und **vor** der Aufnahme in `members`:

- Ist `c.t_exp is None`, wird `Finding(kind=TrustFinding.VOUCH_WITHOUT_TEXP, subject=cid)`
  angehängt.
- **Ohne Wirkung.** Der Vouch geht danach unverändert in `members`, trägt sein `n_budget` und
  sein `n_kante`. Kein `continue`, kein Ausschluss.

Begründung für die Wirkungslosigkeit: `02 §3.1` legt fest, dass kein Akt außer der Uhr Budget
freigibt. Ein Ausschluss gäbe Budget frei, das gebunden gehört — die gefährliche Richtung.
Diagnose verschieden, Wirkung gleich (D94).

## 5. Teil D — die drei Erzeugerstellen

Alle drei setzen `t_exp` weit jenseits ihres jeweiligen `now`:

1. `tools/example_nucleus.py` — Vorgabe `t_exp = NOW + 1000000`.
2. die Fixtures unter `tests/`, die Vouches bauen.
3. `tools/sim/scenarios/` — die sechs Szenarien.

`t_exp` darf an keiner dieser Stellen gleich dem jeweiligen `now` sein. Der Grenzwert
`now = t_exp` ist einem eigenen Vektor vorbehalten und gehört nicht in eine Fixture, die etwas
anderes prüft.

Sämtliche `_eq`-Zusicherungen in `tools/example_nucleus.py` müssen unverändert durchlaufen. Alle
`DOC_`-Konstanten bleiben byte-identisch: keine von ihnen ist eine `claim_id`.

## 6. Neue Tests

- **Feldabdeckung.** Ein Test vergleicht `set(Claim.__dataclass_fields__)` gegen eine im Test
  aufgeschriebene Menge und schlägt fehl, sobald `Claim` ein Feld gewinnt oder verliert. Ein
  zweiter Test ruft `build_signed` mit **allen** optionalen Feldern belegt und prüft jedes
  einzelne im Ergebnis. Die Aufzählung steht im Test, die Vollständigkeitsprüfung kommt aus
  `__dataclass_fields__` — nicht umgekehrt.
- **Signatur und Identität.** `verify_sig(build_signed(sk, ...))` ist wahr, und `I` des Ergebnisses
  gleicht `sk.public_key().public_bytes_raw()`.
- **Determinismus.** Zweimal `build_signed` mit denselben Argumenten liefert byte-gleiche
  `signed_bytes` (RFC 8032).
- **Vermerk feuert.** Ein Vouch ohne `t_exp` in einem Scope erzeugt genau ein
  `VOUCH_WITHOUT_TEXP` mit seiner `claim_id` als Subjekt.
- **Vermerk ist wirkungslos.** Zwei sonst gleiche Läufe, einer mit `t_exp`, einer ohne, liefern
  identische `n_budget`, `n_kante` und identische Kapazitäten; sie unterscheiden sich allein in
  der Finding-Menge.
- **Kein Vermerk bei defektem `v`.** Ein Vouch ohne `t_exp`, dessen `v` nicht dekodierbar ist,
  erzeugt `UNPARSABLE_VOUCH_PAYLOAD` und **kein** `VOUCH_WITHOUT_TEXP`.
- **Kein Vermerk außerhalb des Budget-Sets.** Ein Vouch ohne `t_exp`, der `_in_budget_set` nicht
  besteht, erzeugt keinen Vermerk.

## 7. Verbotene Konstrukte

- Ein Feld in `TrustParams` für die Budgetregel.
- Ein Ausschluss des Vouch aus Budget-Set, Kantensatz oder Gruppe wegen fehlendem `t_exp`.
- Ein Default für `t_exp` in `build_signed`, in `Claim` oder in `_Author.claim`.
- Eine Handaufzählung der Felder beim Signieren, an welcher Stelle auch immer.
- Eine Änderung an `Claim`, `core_map`, `signed_map`, `claim_id` oder `sign_preimage`.
- `git add -A`.

## 8. Abnahmekriterium

- Die 415 bestehenden Tests laufen grün, mit **genau einer** erlaubten Abweichung: die gewählte
  `kante_claim_id` darf bei zwei aktiven Vouches derselben Gruppe mit gleichem `n` umspringen,
  weil der Gleichstand über die `claim_id` gebrochen wird und `t_exp` diese ändert. `n_kante`,
  Kapazitäten und Flüsse bleiben unverändert. Jede andere Abweichung ist ein Halt.
- Die neuen Tests aus §6 laufen grün.
- `make check` und `make check-all` grün.
- Kein Wert in `02-golden-anchors.md`, `02b-golden-anchors.md`, `03-golden-anchors.md` oder
  `04-golden-anchors.md` ändert sich.

## 9. Abschluss und Rückfragen

Der Lauf endet mit einem **Commit auf `impl/authoring`**, nicht mit einem Bericht über gestagete
Pfade. `git add` mit expliziten Pfaden.

Rückfragen gehen in das Spec-Gespräch zurück und werden nicht im Implementierungsfenster
entschieden. Insbesondere: findet sich eine vierte Stelle, die Vouches erzeugt, ist das eine
Rückfrage und keine stille Erweiterung — die Dreizahl ist Teil des Beschlusses.
