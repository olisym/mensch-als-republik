# 00a-nachtrag — Nachbesserung nach der Abnahme von `0c3f9ad`

## Branch und Basis

`impl/00a-rotate-key`, Basis `0c3f9ad` zuzüglich des Spec-Commits, der diese Datei einführt.
Ein Commit am Ende, kein Merge, kein Push. Der bestehende Lauf wird **nicht** zurückgenommen.

## Was abgenommen ist

`_on_author_chain`, `_earliest_on_chain`, die Zyklusprüfung und die Rücknahmeprobe zu Auftrag 1
sind in Ordnung und werden nicht angefasst. Die vier Punkte unten sind Nachbesserungen, drei
davon gehen auf Fehler im ersten Prompt zurück.

## Auftrag 1 — Der Protokoll-Boden ohne Policy (D156)

`is_irrevocable(predicate, policy)` in `mensch_als_republik/policy.py` gibt heute `False`
zurück, sobald `policy is None` ist. Das widerspricht `01 §5.4.1` („fehlt das Verfassungsobjekt
lokal, gilt der Sicherheits-Default aus `00 §5.2`") und dem Anker `P-D`.

Bei `policy is None` wird gegen `PROTOCOL_IRREVOCABLE` geprüft. Die übrigen Bedingungen bleiben:
`nuc:`-Präfix, Profilname nach dem letzten Schrägstrich. D73 und D91 bleiben unberührt.

Ein Test belegt, dass ein `core/revoke@1` auf eine `obligation@1` **ohne** Policy den Zustand
nicht auf `REVOKED` bringt.

**Rücknahmeprobe (Prüfregel 23):** die ungeschützte Seite ist der `policy is None`-Pfad. Ein
Test, der eine Policy übergibt, sieht die Regression nicht — er lief vorher grün und läuft
nachher grün. Die Probe nimmt die Reparatur zurück und belegt, dass der neue policy-freie Test
rot wird und ein bestehender Test mit Policy grün bleibt. Beide Namen in den Bericht.

**Melden, nicht anpassen:** jeden Bestandstest, der rot wird, weil er bisher darauf beruhte,
dass ohne Policy ein Widerruf wirkt. Das wäre ein Befund über den Bestand, kein Anlass für eine
Teständerung.

## Auftrag 2 — `keys.py` reicht die Policy durch statt sie zu erfinden (D156)

`resolve_current_key` bekommt einen weiteren Schlüsselwortparameter:

```
policy: NucleusPolicy | None = None
```

Er wird unverändert an `classify_all` gereicht. Die Konstruktion `NucleusPolicy(scope=scope)`
innerhalb der Funktion entfällt ersatzlos — nach Auftrag 1 trägt der Boden auch ohne Policy, und
eine Funktion, die keine Verfassung kennt, erfindet keine.

Dieselbe Naht wie `membership` in `03 §4`, das `policy` ebenfalls durchreicht.

Ein Test belegt, dass die Kettenauflösung ohne übergebene Policy dasselbe Ergebnis liefert wie
mit einer Policy, deren Verfassung zu `scope` gehört.

## Auftrag 3 — Die `03`-Anker wieder binden (D157)

`03-golden-anchors.md` trägt in `P-A` bis `P-E` jetzt `{obligation@1, rotate-ack@1,
rotate-key@1}`. Die Tests, die im vorigen Lauf auf einen Vergleich gegen `PROTOCOL_IRREVOCABLE`
umgestellt wurden, vergleichen wieder gegen die **ausgeschriebenen Werte der Ankerdatei**.

Der Grund ist `P-B`: er ist der einzige Vektor, der D58 und D70 gleichzeitig stellt. Gegen die
Konstante verglichen prüft er die Konstante gegen sich selbst und ist tot.

Ein Vergleich gegen `PROTOCOL_IRREVOCABLE` ist überall dort weiterhin richtig, wo der Boden
**als Boden** geprüft wird und nicht als Ankerwert — diese Stellen bleiben, wie sie sind.

## Auftrag 4 — Testlage 11 neu konstruieren (D155 a)

`test_two_complete_rotates_incomparable_without_link` misst nicht, was er behauptet. Die Lücke
lag unmittelbar vor `R_b`, also wurde `R_b` `PENDING` und war nie eine zweite vollständige
Rotation. Der Zweig `earliest is None` in `_head_from` ist damit von keinem Test betreten.

`_predecessor_known_and_valid` prüft genau **einen** Schritt zurück. Die Lücke gehört daher
mindestens zwei Glieder vor `R_b`:

```
Kette von K:   R_a  →  c1  →  c2  →  R_b
Im Store:      R_a,          c2,     R_b        (c1 fehlt)
```

Dann ist `R_b` `ACTIVE`, weil sein direkter Vorgänger `c2` bekannt ist, während der
Rückwärtslauf ab `R_b` bei `c1` abbricht und `R_a` nie erreicht. Beide Rotationen sind
vollständig und unvergleichbar; erwartet wird die leere Menge für diese Wurzel.

Der Test hält ausdrücklich fest, dass beide Rotationen `ACTIVE` sind — sonst misst er wieder den
`PENDING`-Fall, ohne dass es auffällt.

## Auftrag 5 — Testlage 6 auf die Quittung umbauen (D158)

Der Vektor „Ack als `core/revoke@1`" ist nicht konstruierbar: ein Widerruf auf einen fremden
Claim wirft `FOREIGN_LIFECYCLE`. Der tragende Vektor ist ein `nuc:N/receipt@1` von `K_n` mit
`J = [claim-ref, claim_id(R)]`. Er erfüllt alle vier Bedingungen aus D152 und unterscheidet sich
einzig im Prädikatnamen.

Erwartet: die Rotation bleibt unvollständig, der Kopf bleibt die Wurzel. Der Test heißt
entsprechend um.

## Nicht-Ziele

- **Keine Änderung an `03-golden-anchors.md`**; die Datei ist im Spec-Commit bereits nachgezogen.
- **Keine Änderung an `01a-policy-prompt.md` oder `03-prompt.md`.** Beide tragen eine
  Hinweiszeile und behalten ihre alten Zahlen mit Absicht (D157).
- Keine Änderung an `_on_author_chain`, `_earliest_on_chain` oder der Zyklusprüfung.
- Kein `nucleus_keys`, keine Epochenkette, kein Layer 04 (D151).
- Keine weitere Erweiterung von `PROTOCOL_IRREVOCABLE`.
- Nicht in Angriff nehmen: dass die Equivocation-Prüfung nur equivozierte **Rotationen** sieht
  und nicht eine an anderer Stelle gespaltene Autorenkette. Das ist notiert und offen.

## Abnahmekriterien

- `make check-all` grün, Testzahl vor und nach dem Lauf.
- Beide Namen aus der Rücknahmeprobe zu Auftrag 1 im Bericht.
- Auftrag 4 belegt im Bericht, dass beide Rotationen `ACTIVE` sind und das Ergebnis für diese
  Wurzel leer ist.
- Widerspricht eine Messung diesem Prompt, wird sie gemeldet. Keine Erwartungswerte nachziehen.

## Abschluss

Ein Commit auf `impl/00a-rotate-key`. Der Bericht nennt den Commit, `make check-all`, die
Rücknahmeprobe und jede unterbestimmte Stelle.
