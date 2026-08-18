# Prompt: Einlesepfad Lauf A — Nachlauf (Abnahmedefekte A-1, A-2)

Branch: `impl/einlesen`, weiter auf `65b457e`. Kein neuer Branch, kein Merge.

Grundlage: `einlesen-a-abnahme.md` §2. Nur Tests, kein Produktivcode.

Rückfragen gehen an den Supervisor.

## 1. A-1 — Die Parametrisierung verankern

`_reject_vectors_with_wire()` in `tests/test_verifier.py` liefert heute vier Einträge. Fällt sie
auf null, meldet `pytest` einen Skip und keinen Fehler.

Zu bauen: ein eigener Test, der die **Ausnahme** festhält statt der Summe. Die Vektoren mit
`expect_reject`, aber ohne `wire_bytes` und ohne `signed_bytes`, sind genau `{"NV2"}`.

Die Zahl der parametrisierten Fälle wird **nicht** getippt. Geprüft wird, daß kein Vektor still
aus der Ableitung fällt.

## 2. A-2 — BV3 an seine Bedeutung binden

Vorbild ist `test_nv2_reserializes_to_tv1_core`, das direkt darunter steht.

Zu bauen, gegen `_vec("BV3")["wire_bytes"]` und `_vec("TV1")["signed_bytes"]`:

- `cbor_canon.reserialize(bv3) == tv1_signed`
- `len(bv3) == len(tv1_signed) + 1` — die indefinite-length-Form kostet ein Byte (`h'bf'` und
  `h'ff'` statt eines Map-Headers)

Damit prüft der Generator sich gegen den Vektor, den er erzeugt. Ein Fehler in der Schleife in
`gen.py` — falsche Schlüsselreihenfolge, `core_map` statt `signed_map` — fällt auf, statt still in
die committete JSON zu wandern.

## 3. Eine Feststellung, kein Test

`grep -rn 'raise VerifierError' mensch_als_republik/` ausführen und das Ergebnis in den
Commit-Text schreiben. `read_claim` liest `exc.code`; die Basisklasse `VerifierError` trägt kein
`code`-Klassenattribut, die elf Unterklassen tragen es. Eine Fundstelle wäre ein Bruch der
Totalität an genau der Funktion, die nie werfen soll.

Erwartung: keine Fundstelle. Ergibt der Grep etwas, **nicht reparieren** — melden.

## 4. Ausdrücklich nicht

- Kein Produktivcode. `verifier.py`, `atom.py`, `cbor_canon.py` bleiben unangetastet.
- `welten.py` bleibt unangetastet. Das `t_exp`-Problem und B-4 sind ein eigener Lauf.
- Keine Änderung an `gen.py` oder `vectors_01.json`. A-2 prüft den Bestand, es korrigiert ihn
  nicht. Schlägt einer der beiden Tests fehl, ist das ein Befund und wird gemeldet, nicht
  weggerechnet.

## 5. Abnahmekriterien

1. `make check-all` grün, zwei pytest-Endzeilen. 486 → 489, Eigenschaftstests bleiben bei 13.
2. `python -m tools.check_specs` sauber.
3. `git diff --stat 65b457e` zeigt genau eine geänderte Datei: `tests/test_verifier.py`.
4. Ein Commit auf `impl/einlesen`. Kein Merge.

Im Commit-Text: Testzahl vorher/nachher und das Grep-Ergebnis aus §3.
