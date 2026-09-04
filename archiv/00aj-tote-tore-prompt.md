# 00aj — Tote Tore streichen, drei Träger bauen

## Branch und Basis

Branch `00aj-tote-tore`, Basis ist der Splice-Commit auf diesem Branch (Anhang `01 §C.15`,
Register D283-D285). Ein Commit am Ende, kein Merge.

## Normative Grundlage

- **D283** — zwei nie erreichte Erzeugerstellen sind unerreichbar und werden gestrichen, drei
  bekommen Träger.
- **D284** — `resolve_scope` auf `core/*` ist ein Aufruferfehler, kein Reject.
- **D285** — NV31, zwölfter negativer Vektor, Anhang `01 §C.15`.
- `01 §3` Regel 1 (Top-Level ist eine CBOR-Map mit uint-Keys), `01 §2.2` Regel 3 und Regel 4,
  `01 §2.3` (ein `core/*`-Claim ist kontextfrei), `01 §6` Punkt 4.

## Auftrag

### 1. Das zweite Versionstor streichen

In `mensch_als_republik/verifier.py`, in `structural_check`, den Block hinter dem Aufbau des
Claims entfernen: den Kommentar `# 1: version`, die Bedingung auf `claim.version` und den
zugehörigen `raise`. Das Versionstor vor der Feldtypprüfung bleibt unverändert.

### 2. Das Formtor unter `nuc:` streichen

In `mensch_als_republik/predicates.py`, in `parse_predicate`:

- Der Zweig für die Alias-Kodierung wird unbedingt. Nach dem Test auf die kanonische Kodierung
  folgt kein zweiter Test mehr, sondern direkt der Rückgabewert mit `scope_alias`.
- Der abschließende `raise` innerhalb des `nuc:`-Zweigs entfällt.
- Die Regex-Konstante für die Alias-Form entfällt ersatzlos.

Die Regex für die kanonische Form bleibt: sie unterscheidet Hex-Scope von Alias-Scope. Die
Grammatik-Regex für `nuc:`-Prädikate bleibt unverändert; sie trägt die Alias-Bedingung bereits als
Lookahead.

### 3. `resolve_scope` auf `core/*`

In `mensch_als_republik/predicates.py`, in `resolve_scope`: der Zweig für den Namensraum `core`
wirft `ValueError` statt der bisherigen Reject-Klasse. Die Meldung benennt, dass ein
`core/*`-Claim keinen Scope hat. Die beiden übrigen Würfe in dieser Funktion bleiben unverändert.

Träger in `tests/test_predicates.py`: ein `core/revoke@1`-Claim, an `resolve_scope` übergeben,
erwartet `ValueError`.

### 4. Zwei Sondierwelten für `FOREIGN_LIFECYCLE`

In `tests/test_verifier.py`. Eine Welt, zwei Einstiege. Die Welt Feld für Feld:

- Zwei Identitäten aus `tests/helpers.py`.
- Die erste bürgt für die zweite: `vouch` mit `n=1`, Scope aus `scope_id`, `t=1000`, kein `t_exp`.
- Die zweite widerruft diesen Claim: `revoke` auf das Ziel, `t=1001`. Der Widerruf ist damit
  fremd-bezüglich.
- Der Store enthält beide Claims.

Zwei Tests:

- `classify` auf den Widerruf mit diesem Store wirft `ForeignLifecycle`.
- `classify_all` aus `mensch_als_republik/index.py` mit diesem Store und `now = 1500` wirft
  `ForeignLifecycle`.

Beide Tore sind eigenständig; jedes braucht seinen eigenen Test.

### 5. NV31

In `tests/vectors/gen.py`: ein zwölfter negativer Vektor `NV31`. Seine Drahtbytes sind die
kanonische CBOR-Kodierung einer **Liste**, die die Werte der signierten TV1-Map in aufsteigender
Key-Reihenfolge enthält. Der Wert wird aus der bereits im Modul vorhandenen signierten TV1-Map
abgeleitet, nicht getippt. Erwarteter Code: `MALFORMED_CBOR`. Der Eintrag steht am Ende der
Vektorliste, hinter NV30, mit einem Kommentar, der `01 §C.15` und D285 nennt.

Danach `tests/vectors/vectors_01.json` neu erzeugen. Bestehende Vektoren dürfen sich dabei nicht
ändern.

## Nicht-Ziele

- **Keine Änderung an `01-claim-atom.md` und `07-decisions.md`.** Beide sind mit dem Splice-Commit
  fertig; der Anhangsabschnitt `01 §C.15` existiert bereits.
- **Keine Änderung an `mensch_als_republik/errors.py`.** Kein neuer Reject-Code, keine Umbenennung,
  keine Änderung an der Aufzählung.
- **Keine Änderung an bestehenden Vektoren**, keine Umnummerierung, keine Änderung an `TV1`.
- **Die zehn toten Doppelerzeuger von Vermerken aus D281 bleiben unangetastet.** Sie gehören nicht
  in diesen Lauf.
- **Kein Aufräumen daneben.** Wer beim Lesen weitere unerreichbare Zweige findet, meldet sie und
  streicht sie nicht.
- **Keine getippten Bytes.** Weder für NV31 noch für einen Erwartungswert. Wo eine Erwartung
  gebraucht wird, wird sie abgeleitet.
- **Kein Merge, kein Push auf `main`.**

## Abnahmekriterien

1. `make check` läuft durch. Die Testzahl ist **658**.
2. `python3 tools/check_specs.py` meldet alle Spec-Dateien sauber und `Register: D1–D285`.
3. Die neu erzeugten Drahtbytes von NV31 sind **299 Byte** lang und dekodieren zu einer Liste mit
   **zehn** Elementen.
4. `git diff` gegen den Branchpunkt zeigt Änderungen ausschließlich in
   `mensch_als_republik/verifier.py`, `mensch_als_republik/predicates.py`,
   `tests/test_predicates.py`, `tests/test_verifier.py`, `tests/vectors/gen.py` und
   `tests/vectors/vectors_01.json`.
5. In `tests/vectors/vectors_01.json` unterscheidet sich gegenüber dem Branchpunkt genau ein
   Vektoreintrag: der neue. Kein bestehender Eintrag ändert sich.

## Rücknahmeproben

Vier Proben. Jede: die genannte Stelle zurücknehmen, **nur** den genannten Test fahren, rot
bestätigen, Stelle wiederherstellen. Wird eine Probe grün, ist der Träger stumm — das ist ein
Befund und wird gemeldet, nicht umgangen.

1. **`resolve_scope`**: den `core`-Zweig samt `raise` entfernen. Der Träger aus Auftrag 3 wird rot.
2. **`classify`**: das `FOREIGN_LIFECYCLE`-Tor in `mensch_als_republik/verifier.py` entfernen. Der
   erste Test aus Auftrag 4 wird rot, der zweite bleibt grün.
3. **`classify_all`**: das `FOREIGN_LIFECYCLE`-Tor in `mensch_als_republik/index.py` entfernen. Der
   zweite Test aus Auftrag 4 wird rot, der erste bleibt grün.
4. **NV31**: **beide** Tore zugleich entfernen — den Test auf „Top-Level ist eine Map" **und** die
   Schleife, die die Keys auf `int` prüft. Der Vektortest für NV31 wird rot. Wird nur eines der
   beiden Tore entfernt, bleibt er grün; das ist gemessen und kein Fehler, sondern der Grund für
   die Zwei-Tor-Probe.

Für die beiden gestrichenen Tore aus Auftrag 1 und 2 gibt es keine Rücknahmeprobe: sie sind
unerreichbar, ein Test kann sie nicht sehen. Ihr Kriterium ist, dass der Bestand nach der
Streichung vollständig grün bleibt.

## Abschluss

Ein Commit auf `00aj-tote-tore`. Im Bericht: die Testzahl, die Ausgabe von `check_specs.py`, die
Länge der NV31-Bytes, das Ergebnis jeder der vier Rücknahmeproben und der **vollständige**
`git diff` gegen den Branchpunkt — nicht nur `--numstat`.
