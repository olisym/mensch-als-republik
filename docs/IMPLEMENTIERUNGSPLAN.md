# Implementierungsplan — Mensch als Republik (Referenz-Python)

Modell: **Cursor codet, Claude supervidiert.** Du fährst jeden Schritt in Cursor, sammelst das
Ergebnis ein und bringst es zu Claude zur Qualitätskontrolle gegen die Spec. Erst wenn ein Schritt
„grün" ist (Tests + Claude-Review), geht es weiter.

Die **Spec (`00`–`06`) ist die Wahrheit.** Die Test-Vektoren in den Specs sind die Akzeptanz-Tests
des Codes — Code und Spec sind mechanisch gekoppelt.

---

## Arbeitsrhythmus (für jeden Schritt gleich)

1. **Branch** anlegen: `git switch -c impl/<schritt>` (von `main`).
2. **Prompt** aus diesem Plan (bzw. den separaten Prompt-Dateien) in Cursor geben.
3. Cursor arbeiten lassen; in **kleinen Commits** sichern.
4. **Grün-Check lokal:** `pytest` läuft durch.
5. **Rückmeldung an Claude** einsammeln (siehe „Was Claude als Rückmeldung erwartet").
6. Claude reviewt gegen Spec → „grün" oder „Nacharbeit mit Punkt X".
7. Bei grün: Branch nach `main` mergen (`--no-ff` oder Merge Request in Gitea), pushen.
8. Nächster Schritt auf frischem Branch.

**Regel:** Nie zwei Schichten gleichzeitig offen. Nie direkt auf `main` codieren.

---

## Was Claude als Rückmeldung erwartet (nach jedem Schritt)

Kopiere Claude genau das — daraus mache ich die Qualitätskontrolle:

- **`pytest`-Ausgabe** (voll, inkl. Anzahl passed/failed).
- **`git diff --stat`** des Branches (welche Dateien, wie groß) — grober Umfang.
- **Die neuen/geänderten Dateien** selbst (die relevanten `.py`), oder das Repo im Projekt.
- **Jede Cursor-Rückfrage** wörtlich, falls Cursor innegehalten hat.
- **Ein Satz „Auffälligkeiten"**: irgendwas, das sich komisch angefühlt hat (Cursor hat etwas
  erfunden, eine Datei umgebaut, die es nicht sollte, o. Ä.).

Ich prüfe dann: (a) stimmen die Vektoren byte-genau? (b) hält der Code die Schichtgrenze (kein
neues Atom-Feld, keine Wall-Clock-Ordnung, keine Bedeutung im Kern)? (c) sind positive **und**
negative Tests pro Fehlerklasse da? (d) ist etwas subtil falsch, das grün ist, aber die Spec
verletzt? Ergebnis: „merge" oder „ein konkreter Nacharbeits-Prompt".

---

## Die Schritte

### Schritt 0 — Repo-Gerüst (klein, einmalig)
- Branch `impl/00-scaffold`.
- Ziel: `pyproject.toml` (Deps: `cbor2`, `cryptography`, `pytest`), Paket `mensch_als_republik/`,
  `tests/`, `docs/prompts/` (lege die Cursor-Prompts dort ab). `README` mit „so läuft pytest".
- **Kein** Protokoll-Code. Nur Struktur, damit `pytest` grün (leer) startet.
- Rückmeldung: `pytest` läuft (0 Tests ok), `git diff --stat`.
- *Optional* — wenn dir das zu kleinteilig ist, in Schritt 1 mit reinziehen.

### Schritt 1 — Schicht 01: Atom + Verifizierer  ← **Start hier**
- Branch `impl/01-atom`.
- Prompt: **`docs/prompts/01-atom.md`** (die fertige Datei `cursor-prompt-01-atom.md`).
- Akzeptanz: `gen.py` reproduziert Anhang C **byte-genau**; alle Fehlerklassen aus Anhang B mit
  positivem+negativem Test; Zustandsmaschine korrekt (`pending`/`active`/`revoked`/
  `equivocation_flagged`). Keine Änderung an `trust_flow.py`.
- Das ist der **wichtigste** Schritt — hier steht oder fällt die Kopplung Spec↔Code. Nimm dir Zeit;
  erst `cbor_canon`+`atom`+`gen.py` grün, dann der Verifizierer.

### Schritt 2 — Schicht 02: Trust-Flow (+ bekannten Bug fixen)
- Branch `impl/02-trust-flow`.
- Claude liefert vorab den **Prompt `02-trust-flow.md`**. Inhalt grob: Aktiv-Set aus Atom (§6),
  Graphaufbau pro `(N, π)`, Knoten-Splitting (Advogato), **Max-Flow/Min-Cut** als harte Sicht,
  **PageRank** als weiche Relaxation, `t_exp`-lokal + `pending`-Kanten (die frischen 02-Edits).
  Enthält den **Fix** des `parse_vouch_predicate`-Doppeldefinition-Bugs (die zweite Definition
  referenziert ein nicht existierendes `_VOUCH_PREDICATE_RE`).
- Akzeptanz: der **Sybil-Bound aus §4** wird durch einen Test bezeugt (Fluss in die Sybil-Region
  ≤ Summe der ehrlichen Grenzkapazitäten, unabhängig von der Sybil-Zahl); Monotonie unter fehlenden
  Kanten; „Neuling ≈ 0".

### Schritt 3 — Schicht 00/03: Nukleus-Fundament + Profile
- Branch `impl/03-profiles`.
- Prompt `03-profiles.md`: `resolve_scope`, Genesis/Verfassung als content-adressierte Objekte,
  `resolve_current_key` (00 §6.4), die Profile `vouch`/`accept-rules`/`vouch`/`verdict`/
  `obligation`/`receipt`/`grant-membership` als **Interpretation** über dem Atom. Akzeptanz gegen
  das geteilte Beispiel-Nukleus (00 §3.1) und die 06-Akteure.
- Wichtig: `obligation@1` **irrevocable** (Pflicht-Policy, 03 §3.3.3) mit Test.

### Schritt 4 — Schicht 04/05: Governance + Enforcement
- Branch `impl/04-governance`.
- Prompt `04-governance.md`: Vorschlag/Stimme/Auszählung, zweck-gescopte gewichtete Tally +
  Snapshot-Determinismus, Schwellenklassen; Enforcement-Leiter als Zustands-/Cure-Logik.

### Schritt 5 — Schicht 06: Dienste
- Branch `impl/06-services`.
- Prompt `06-services.md`: `service-announce`/`timestamp`/`validation` als Profile, und vor allem
  **VR-06.1** (mechanischer Falsch-Validierungs-Slash) mit den Vektoren SV1–SV3 + NV06. Akzeptanz:
  `{NV06, NV1}` wird als self-contained Falsch-Validierungs-Beweis erkannt.

### Schritt 6 — Integration & Transport-Profil (optional, später)
- Ende-zu-Ende-Szenario über alle Schichten; danach das Reticulum/LXMF-Transport-Profil als
  separater, klar abgetrennter Layer (nie im Kern).

---

## Leitplanken, die für ALLE Schritte gelten (gib sie Cursor mit)

- Die **Spec gewinnt** bei jedem Konflikt; nicht eigenmächtig abweichen, sondern **stoppen und
  fragen**. Rückfragen bringst du zu Claude.
- **Kein neues Atom-Feld**, keine Key-Rotation/Delegation im Kern.
- **Keine Wall-Clock-Ordnung** — Ordnung kommt aus `h_prev`. `now` ist immer ein Parameter.
- **Kein globaler Zustand/Konsens** — alles per-Verifizierer, per-Sicht.
- Kleine, reine Funktionen; Tests neben jedem Modul; positive **und** negative Fälle.
- Eine Schicht pro Branch; kleine Commits; erst grün + Review, dann merge.

---

## Merksatz für den Start des frischen Chats

Gib dem neuen Chat: (1) diesen Plan, (2) die Specs `00`–`06`, (3) `cursor-prompt-01-atom.md`,
(4) „wir starten Schritt 1". Claude hält die Specs **nicht** automatisch aktuell — die jeweils
committete Fassung aus dem Repo ist maßgeblich und muss sichtbar sein.
