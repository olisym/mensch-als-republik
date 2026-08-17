# Sitzungsstart: Einlesepfad und Anwendung (MaR)

## Kontext

Wir arbeiten an **Mensch als Republik (MaR)**, einem dezentralen Koordinationsprotokoll.
Python-Referenzimplementierung, Branch-per-Lauf, selbst gehostete Gitea-Instanz
(`git.h.error13.de`).

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Implementierungs-Prompts und führst die Abnahmen. Du
schreibst keinen Produktivcode.

**Arbeitsweise:**
- Design vor Code. Alle Forks und Zahlen stehen fest, **bevor** ein Prompt geschrieben wird.
- Die Spec ist normative Wahrheit. Der committete Gitea-Stand ist die Quelle für Dateien.
- Ehrliche Trade-off-Analyse statt Zustimmung. Widersprich, wenn etwas nicht trägt.
- Direkte, sparsame Sprache. Deutsch mit englischen Fachbegriffen.
- Minimale Abhängigkeiten: nur `cbor2` und `cryptography`. Unter `dev` zusätzlich `pytest` und
  `hypothesis`. Kein `float`, kein `fractions` im Produktivcode. `now` ist immer Parameter.
- Shell-Befehle als **ein** Copy-Block, fish. **Ein Job pro Zeile, `and` am Zeilenanfang** — nie
  `;`, und **innerhalb einer Pipe steht nie ein `and`**. Merke: `and` hinter einer Pipe prüft den
  Status des letzten Pipeglieds, nicht den des ersten.
- **Spec-Dateien werden als Download geliefert**, nicht als Copy-Block. Der Shell-Block setzt
  voraus, dass die Datei bereits im Repo-Wurzelverzeichnis liegt.
- **Hash-Test als erster Job.** `test (sha256sum datei | cut -d' ' -f1) = <hash>` hält die Kette
  an, wenn die Grundlage eine andere ist. Ein `sha256sum` allein prüft nichts, es druckt nur.
- **Bei neuen Dateien `git add` vor `make check`**, sonst danach. `check_tree.py` schlägt bei
  unversionierten Quelldateien fehl.
- `git add` mit expliziten Pfaden, nie `-A`.
- Keine Escapes in Spec-Dateien. Bytes als `h'ff'`.
- **Ein Implementierungslauf endet mit einem Commit auf einem benannten Branch.**

⚠ **Dateien nie manuell editieren.** Spec-Dateien kommen vollständig von Claude. Vor einer
Ersetzung mitten in einer Datei per `sha256sum` abgleichen — **und den vollständigen zu
ersetzenden Absatz als Anker nennen**, nicht die eine Zeile, an der es sich festmachen lässt.

⚠ **Das Projektwissen ist nicht die Quelle für Dateien.** Frag nach dem Repo-Stand. Stimmt der
`sha256sum` einer Projektkopie mit dem Repo überein, darf sie als Grundlage dienen — sonst nicht.

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`. Zuletzt lag `main` auf dem Merge von
`impl/verweise`. Register **D1–D129**. **474 Tests**, dazu **elf Eigenschaftstests** unter
`MAR_HYPOTHESIS=voll`. `make check-all` sind **zwei** pytest-Läufe, also zwei Endzeilen.
`check_specs.py` führt **39** Spec-Dateien.

- **01** Atom, Verifier, elf Reject-Codes, acht Zustände.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II: `membership`, `settlement`, `verdict_status`, `resolve_policy`.
- **04** Governance: Epochenkette, Kopfzahl-Auszählung, Ratifizierung.
- **Werkzeugschicht** (`werkzeuge.md`): Autorschaft mit persistenter Spitze und Redo, Simulation,
  Eigenschaftstests. Die Kettenfortführung existiert **einmal**, in `tools/autor.py`.

**Neu in der letzten Sitzung:** D124–D129.

- **D124** Persönliche Rotation ist **nicht** identitätserhaltend. Wer den Schlüssel verliert,
  verliert den Trust-Score und baut ihn sozial neu auf. Werkzeug, kein Layer.
- **D125** Nukleus-Rotation gilt erst mit **Gegenzeichnung** des Nachfolgers (TUF-Form).
- **D126** `key_mode` unterscheidet die Signaturform, nicht die Kardinalität.
- **D127** Die Naht liegt **unter** der Kettenfortführung: zwei Rückhalte, ein Testsatz.
- **D128** Halt bei abgefangener Ausnahme; `BaseException`; der Halt klebt am Objekt, nicht am
  Rückhalt.
- **D129** `gabeln` fasst den dauerhaften Zustand nicht an.

## Das Aufnahmekriterium

Aus `08 §3`, vor jedem neuen Mechanismus:

> **Senkt er die Kosten dafür, festzustellen, wer was gesagt hat — oder verteilt er Macht?**
> Senken: Protokoll. Verteilen: Policy. Keines von beidem: Werkzeug.

Die dritte Spalte hat inzwischen ein eigenes Dach: `werkzeuge.md`. Was dort landet, bekommt keine
Zahl im Dateinamen, keine Golden Anchors und keinen Layer — bleibt aber normativ.

## Prüfregeln

Die neun aus den Vorsitzungen gelten unverändert: **vor dem Schreiben rechnen**, **Standprüfung**,
**Feldinventur**, **Zugehörigkeitsliste am Datentyp**, **Ausgänge aufzählen**, **Monotonie
stufenweise**, **Abhängigkeitssatz bei Reihenfolgeänderungen**, **Parallelenprüfung**,
**Begründungsprüfung**. Dazu **Leserprüfung** (10), **Geschwisterformel** (11) und **zwei Läufe,
eine Variable** (12).

Neu:

13. **Neustart als Annahme (D128).** Modelliert ein Test einen Neustart, wird gefragt, ob dieselbe
    Ursache auch **ohne** Neustart eintreten kann. Wenn ja, ist der Weiterlauf ein eigener Vektor
    und keine Variante. Die Absturzaufzählung konnte B-1 strukturell nicht sehen, weil jeder ihrer
    Läufe nach dem Bruch ein frisches Objekt baute.
14. **Zählregel.** Eine Aufzählung von Fundstellen wird **gegrept, nicht gelesen**. D119 nannte
    zuerst einen Erzeuger, es waren drei. D127 nannte vier Kettenfortführungen, es waren fünf.
    Beide Male stimmte die Begründung und die Zahl nicht.
15. **Literaturprüfung vor der Entscheidung.** Bei jedem Fork, der außerhalb von MaR seit Jahren
    bearbeitet wird, zuerst nachsehen, was dort gefunden wurde. D124 (did:plc, Keybase, CONIKS,
    Nostr, SSB), D125 (TUF), D127 (Test-Doubles, ALICE, ARIES) sind so entschieden worden — und in
    zwei Fällen billiger und schärfer, als eine eigene Analyse geworden wäre.

## Was die letzte Sitzung gelehrt hat

**Der Befund lag im Produktivcode, gefunden über die Frage, was der Test *nicht* tut.** Das ist die
Umkehrung der Vorsitzung, wo vier von vier Befunden in Tests lagen. Beide Male half dieselbe
Bewegung: die Prüfung selbst als Text lesen und nach ihren Lücken fragen.

**Zwei Befunde entstanden erst, nachdem der Mechanismus existierte.** Die Ausnahmeklasse und die
Erholung über `wiederaufnehmen` waren vor dem Halt nicht formulierbar. Das ist die gewöhnliche
Reihenfolge und kein Versäumnis.

**Das Werkzeug hat mehrfach richtig gehandelt:** `except BaseException` mit Kommentar statt
stillschweigend, `HarterBruch` korrekt von `BaseException` abgeleitet, den Grep-Rest in `welt.py`
gemeldet statt still ausgedehnt, `Teilnehmer.seed` als ungenutzt erkannt und entfernt.

**Ein Commit ist ausgefallen**, weil nach der Zustimmung direkt weitergearbeitet wurde. Der
Hash-Test hat es zwei Züge später gefangen. Deshalb steht er jetzt als Arbeitsweise oben.

## Offen

- **D121 — Einlesepfad**, der nie wirft, plus unsigniertes Bündelformat. `store_laden` in
  `tools/sim/welt.py` liest heute fremde Bytes mit `claim_from_bytes`.
- **Ausgang 5 / Selbst-Equivocation.** Zwei eigene Claims auf dieselbe Spitze. Entsteht in zwei
  getrennten Stores und ist erst bei der Vereinigung sichtbar — also eine Frage an D121.
- **Der Sicherungsblob** mit Seed und Spitze (D120), beschrieben und ungebaut.
- **`00a-rotate-key`.** D125 und D126 stehen; offen bleiben der Effektivpunkt der
  Governance-Rotation (uhrfrei formulieren) und die Frage, ob ein Nukleus statt „einer genügt" eine
  Schwelle verlangen können soll (`00 §4`, Verfassungsknopf).
- **B-4** — Zwillingsbuchführung in `welten()` zieht kein Budget ab. Wer eine Eigenschaft mit
  `erlaube_ueberzeichnung = False` **und** `erlaube_equivocation = True` schreibt, repariert es
  zuerst.
- **`03-prompt.md`-Verweise im Paketcode** — vier Stellen unter `mensch_als_republik/profiles/`
  und `policy.py` zeigen auf eine Prompt-Datei. `03-profiles.md` ist vermutlich der richtige Ort.
  Kleiner eigener Durchgang, danach ist auch `03-prompt.md` löschbar.
- **Gleichstand bei `kante_claim_id`** — `test_groups.py:196` und `test_pagerank_groups.py:22`
  tragen den Fall, der Bruch über `sorted(...)[0]` ist von nichts geprüft.
- **Der Grenzwertvektor `now = t_exp`** in Layer 01 ist seit D119 baubar und weiterhin ungebaut.
- **Die Eigenschaftstests zu `INV-04.7`/`INV-04.8`** prüfen eine schwächere Aussage als sie
  scheinen (D117).
- **`02d-purpose`** (D56), **VR-04.1** (D26), **Zeugenquorum für Fristen** (D100).
- **`04 §7.2` Föderation** nicht durchgerechnet.
- **Ein dritter Scope nur für Schlichtung** — Fork, nicht entschieden.
- **Aufräumen im Repo** — Branches mit stehengebliebenen `voraus`-Zählern. Die Prompt-Dateien im
  Wurzelverzeichnis sind teilweise erledigt; vor jedem weiteren Löschen prüfen, ob Code oder Spec
  die Datei referenziert.

## Der nächste Schritt

**Erst D121, dann die Anwendung.**

D121 ist der letzte Baustein, der zwischen dem Bestand und vier Menschen mit eigenen Schlüsseln
steht: solange fremde Bytes nur über `claim_from_bytes` hereinkommen, umgeht jeder Empfang die elf
Reject-Codes aus `01 Anhang B`. Der Beschluss steht bereits — eine Funktion, die nie wirft und
entweder einen Claim oder einen Reject-Code liefert, Kanonizitätsprüfung im selben `try` wie das
Dekodieren (D83), und ein **unsigniertes** Bündel aus Claim-Bytes plus einer Map
`object-hash → Objektbytes`, Duplikate harmlos, Import idempotent, dem Container wird nie geglaubt.

Zu klären vor dem Prompt: ob Ausgang 5 aus D120 dort seinen Ort findet, und wie sich der
Einlesepfad zu `store_laden` und zur Zustellung in der Simulation verhält.

**Danach die Anwendung.** Vier Menschen erzeugen eigene Schlüssel, ein Genesis trägt ihre Namen
statt der Seeds `0x11×32` ff., und jemand geht die erste Obligation ein, die er erfüllen will. Der
Grund steht in `08 §2.2` — eine Aussage wird nicht dadurch überprüfbar, dass sie signiert ist,
sondern dadurch, dass sie mit anderem Signierten **kollidieren kann**. Ein weiterer Spec-Layer
erhöht die Kollisionsdichte um null.

Der Gerätewechsel ist dabei **kein** Rotationsfall: er ist Migration von Seed und Spitze (D120,
D124), ein Schreiber, ein Ort, kein Protokollmechanismus.

Erst danach `05`. Dessen zwei bekannte Baustellen bleiben: **Über-Commitment als Stufe-3-Auslöser**
(D40, mit D118 scharf) und die **Beta-Reputation** mit dem Moral-Licensing-Problem, gegen das
Layer 02s Flussmodell immun ist und `05` es nicht wäre.
