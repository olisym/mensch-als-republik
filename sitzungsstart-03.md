# Sitzungsstart: Layer 03 schreiben (MaR)

## Kontext

Wir arbeiten an **Mensch als Republik (MaR)**, einem dezentralen Koordinationsprotokoll.
Ich baue die Python-Referenzimplementierung, Branch-per-Layer auf einer selbst gehosteten
Gitea-Instanz (`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, und schreibst eng gefasste Implementierungs-Prompts. Du schreibst keinen
Produktivcode.

**Arbeitsweise:**
- Design vor Code. Alle Forks und Golden Numbers stehen fest, **bevor** ein Prompt geschrieben
  wird.
- Die Spec ist normative Wahrheit. Der committete Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich mir, wenn etwas nicht trägt.
- Direkte, sparsame Sprache ohne diplomatische Weichzeichnung.
- Deutsch mit englischen Fachbegriffen. Implementierung in Python.
- Minimale Abhängigkeiten: nur `cbor2` (canonical=True) und `cryptography`. Kein networkx,
  kein `fractions`, kein `float`. `now` ist immer Parameter, nie Systemuhr.
- Shell-Befehle als **ein** zusammenhängender Copy-Block, fish-Shell, kein Heredoc. Nur trennen,
  wenn ein Zwischenergebnis geprüft werden muss — dann kurz begründen. Keine eingebetteten
  Zeilenumbrüche in `git commit -m`; nimm zwei `-m`.

⚠️ **Dateien nie manuell editieren.** Spec-Dateien kommen entweder vollständig von dir oder über
ein Patch-Skript, das an eine Datei anhängt. Wenn du einen Abschnitt **mitten** in einer Datei
ersetzt, liefere die ganze Datei — und gleiche vorher per `sha256sum` ab, dass du vom
Branch-HEAD ausgehst und nicht vom Projektwissen.

⚠️ **Das Projektwissen ist nicht die Quelle für Dateien.** Es kann ältere Stände tragen als der
Branch-HEAD. Frag nach den Dateien aus dem Repo, statt aus dem Projektwissen zu arbeiten.

## Stand

**Layer 01, 01a, 02a und 02b sind auf `main`, gemergt und gepusht.** `make check` grün in drei
Blöcken: Arbeitsbaum ohne unversionierte Quelldateien, **achtzehn** Spec-Dateien sauber,
Register **D1–D76** lückenlos, **235 Tests**.

**Layer 01 (Atom + Verifier)** — eingefroren. Paket `mensch_als_republik/` mit `atom.py`,
`cbor_canon.py`, `domains.py`, `errors.py`, `policy.py`, `predicates.py`, `verifier.py`. Elf
Reject-Codes, acht Zustände, `classify(claim, store, now, policy=None)`, `ClaimStore`-Protocol.

**Layer 01a (Policy-Override)** — neu in dieser Runde. `NucleusPolicy(scope, declared)` mit
Normalisierung im Konstruktor: Boden `obligation@1` (D70), Negativliste `vouch@1` (D58),
Core-Filter (D71). `PolicyNote(code, predicate)` als Diagnose. Scope-Fehlpaarung wirft
`ValueError` (D73). Der Resolver aus Genesis und Verfassung fehlt noch — er kommt mit `03`.

**Layer 02** — vollständig, beide Sichten. `trust()` (Max-Flow/Min-Cut, Dinic) und `rank()`
(sub-stochastisches `P`, exakte Integer-Rekursion), geteilte Ableitung über `derive()`.

**Werkzeuge:** `make test`, `make check-specs`, `make check-tree`, `make check`. Testlauf immer
`.venv/bin/python -m pytest -q` bzw. `make test`.

### Was diese Runde gelehrt hat

**Der teuerste Fund war kein Spec-Fehler.** Die gesamte Layer-02b-Implementierung — elf Dateien
— lag unversioniert im Arbeitsbaum, während ein Merge-Commit auf `main` sie zu enthalten
behauptete. Alle Testläufe liefen gegen den Arbeitsbaum; ein `git clean -fd` hätte die Schicht
gelöscht. Gefunden nicht durch Nachdenken, sondern durch die **Diskrepanz zwischen zwei
Darstellungen desselben Zustands**: `git diff --stat` zeigte drei Dateien mehr als erwartet.
Dieselbe Mechanik hatte kurz zuvor die fest verdrahtete `SPECS`-Liste in `check_specs.py`
aufgedeckt (dreizehn gelistete gegen sechzehn vorhandene Dateien).

Konsequenz: `tools/check_tree.py` bricht `make check` bei unversionierten Quelldateien ab, und
`SPECS` kommt aus einem Glob. Ein frischer Clone von `main` ist nachweislich grün.

**D75 ergänzt D54.** D54 lehrte: ein zweites Testprofil mit unbequemen Zahlen, weil runde Werte
Fehlerklassen verstecken. In `01a` gab es einen Fall, den **kein** Testvektor prüfen kann — die
Reihenfolge der drei Normalisierungsregeln ist nur unterscheidbar, wenn die Konstanten
überlappen, und das tun sie heute nicht. Die Ergänzung: **wo ein Fall untestbar ist, weil er
heute unmöglich ist, wird die Unmöglichkeit zugesichert, nicht die Semantik getestet.**

**Zwei der drei Abnahmebefunde waren Fehler in meinem Prompt**, nicht in der Ausführung — wie
schon bei `02b`. Beide lagen in Formulierungen: eine Diagnose ohne Subjekt (D74), eine
Testtabelle, die eine Frage nicht stellen konnte (D75). Der Lauf selbst war beim ersten Versuch
grün, mit einer berechtigten Rückfrage.

## Aufgabe dieser Sitzung

**`03-profiles.md` vollständig neu schreiben.** Die Datei wird **ersetzt, nicht gepatcht**: drei
ihrer Abschnitte sind durch `00` überholt, zwei widersprechen sich intern, und
`submit-arbitration@1` fehlt ganz. Ein Anhänge-Patch erzeugte eine Datei mit zwei Meinungen.

Die fünfzehn Forks sind **entschieden** und stehen als D55–D69 im Register, Abschnitt K.
Nichts davon wird neu aufgemacht — deine Aufgabe ist, sie in normativen Spec-Text zu gießen.
Dazu die Änderungsliste in Abschnitt M, die pro Abschnitt sagt, was hineingehört.

Danach, in dieser Reihenfolge und nicht vorgezogen:

1. `03-golden-anchors.md` — drei CBOR-Byte-Vektoren für die `v`-Kodierungen (D55), drei
   Konjunktionstabellen (D60, D63, D67), und das **Gegenprofil**: eine zweite Verfassung, die
   fünf Defaults des kanonischen Beispiels aus `00 §3.1` verletzt (Register Abschnitt L).
2. `03-prompt.md`.

**Bestandsanker, an die `03` bindet** — beide schon gerechnet, nicht neu erfinden:

```
constitution_hash = 890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e
N                 = 65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557
```

## Eigener kleiner Auftrag

**Lehnt `cbor_canon.decode` nicht-kanonische Kodierungen ab?** D37 verlangt kanonisches CBOR für
`v`; falls die Prüfung nur beim Core greift und nicht beim `v`-Payload, ist die Anforderung
nicht durchgesetzt. Das berührt `03` direkt, weil dort drei neue `v`-Kodierungen entstehen und
`§5.1` des Anker-Dokuments Byte-Vektoren dagegen setzt. Ein Aufruf klärt es — sag mir, ob es
ein Befund ist, bevor wir die Anker schreiben.

(In der letzten Runde war der entsprechende Auftrag `trust()` mit leerem Ankerset. Kein Befund:
`OVERCOMMITTED_AUTHOR` erscheint ankerunabhängig, INV-8 hält. Der Vektor aus
`02b-golden-anchors.md §11` ist damit **fällig**, nicht offen, und gehört nach
`tests/trust/test_invariants.py`.)

## Ausdrücklich vertagt — nicht in `03` hineinziehen

- **`02c-purpose`** — Vouch-`v` Key `1` (Zweck-Tag). Layer-02-Semantik, braucht einen
  `purpose`-Parameter in `trust()`/`rank()` und einen erweiterten Gruppenschlüssel (D56).
- **`00a-rotate-key`** — `resolve_current_key` und `rotate-key@1`. `03` nimmt
  `authorized_keys` als Parameter (D62).
- **Der Kompositionspfad aus `04 §3`** (`vote_mode = 0`): Mitgliedschaft ohne einzelnen
  `grant-membership`-Autor. `03` wertet nur den claim-basierten Pfad (D62).
- **Atomarer Tausch** (`03 §3.4`) — Anwendungsschicht, Adaptor-Signaturen.

## Offen, aber nicht blockierend

- **`t_exp is None` bindet Budget unbegrenzt** (Layer 02). Konservativ, aber `02 §6.2` macht
  `t_exp` in Budget-Scopes zur Pflicht — ein eigenes Finding wäre ehrlicher.
- **INV-8-Vektor fehlt** (Layer 02a): geflaggter Autor, dessen Wegfall eine fremde Kante unter
  die Granularitätsgrenze drückt.
- **`TP-BOOT`-Eigenschaftstest** (Layer 02a) wurde verschoben. Nicht streichen: er ist die
  einzige Prüfung der Kalibrierungs-Ungleichung, und `§7` der Anchors zeigt, dass sie
  optimistisch ist (nominell 48 Einheiten, real 36).
- **Zwei offene `02b`-Vektoren**: `PR-INV-9` mit verbundenem zweitem Anker; `α` in nicht
  gekürzter Form.
- **Ist `Σ n_budget > D` im Sinne von `05 §4` terminal oder kurierbar?** (Policy)
- **`example-nucleus.md` anlegen:** `D = 100`, `C₀ ≤ 100`, `k_slash` niedrig mit Begründung aus
  Abschnitt F des Registers. Wird mit `03` dringender, weil `unit_ref` und die
  Irrevocable-Markierung dort landen.
- **Zweiter Spec-Durchgang für `05`, `06`, `04`, `00`, `VISION`** gemäß Änderungsliste G. Neu
  dazu: `05 §3` braucht das Vokabular `BINDING`/`ATTRIBUTED_OPINION` (D68) und Über-Commitment
  als Stufe-3-Auslöser mit Gruppenmaxima-Prüfung (D40).
- **Ziel v1 ist `01`–`04`.** `05` und `06` fügen keinen Mechanismus hinzu, ohne den die anderen
  nicht laufen. Ein fertiges `01`–`04` mit einem echten `example-nucleus` und Menschen, die
  tatsächlich Claims signieren, ist mehr wert als sechs vollständige Specs ohne Nutzer.

---

**Fang an, indem du das Register liest — Abschnitte K (D55–D69), L (Golden-Anchor-Maßstab),
M (Änderungsliste `03`) und N/O (D70–D76) —, dazu `03-profiles.md` im Bestand, `00 §5` und `§7`,
sowie `01 §5.4` in der neuen Fassung. Dann sag mir, ob die fünfzehn Entscheidungen zusammen
eine widerspruchsfreie Datei ergeben, bevor du sie schreibst. Wenn zwei davon kollidieren, ist
das jetzt der Moment — nicht beim Rechnen der Anker.**
