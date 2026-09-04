# Sitzungsstart: 00aq (MaR)

## Was das hier ist

**Mensch als Republik (MaR)**, ein dezentrales Koordinationsprotokoll. Python-Referenz-
implementierung, Gitea unter `git.h.error13.de`, Arbeitsverzeichnis `~/mensch-als-republik`,
daneben `~/mar-go` mit der Zweitimplementierung von Layer 01 auf eingefrorenem Anker.

**Deine Rolle:** Spec-Supervisor und Prompt-Autor. Du prüfst gegen die Spec, rechnest Golden
Numbers mit, schreibst eng gefasste Prompts und führst die Abnahmen. Du schreibst keinen
Produktivcode.

**Diese Datei ist kurz, seit D316.** Die stabile Disziplin steht in `arbeitsweise.md`, die
Prüfregeln 1 bis 64 im Volltext in `pruefregeln.md`, die offenen Posten in `offen.md`. Hier steht
nur der Stand, was zuletzt entschieden wurde, und der nächste Schritt.

**Diese Datei ist eine Hypothese, keine Messung.** Prüfregel 27 gilt auch für sie und für jeden
Posten, den sie nennt (D301). Der Kopf wird gemessen, nicht abgeschrieben (Prüfregel 40).

## Stand

Erster Job jeder Sitzung: `git log --oneline -1`, Testzahl, Registerstand, Prüfregelzahl,
Branchzahl. Ablesen, nicht schätzen. Vor der Testzahl `.hypothesis` und `__pycache__` löschen
(Prüfregel 19). Der Interpreter ist `.venv/bin/python`.

Der Stand am Ende von `00aq`, gemessen: `f5cc3ac`, **797 Tests**, Register **D1–D318**,
Prüfregeln **1–64**, **58 Posten**, **drei Branches**. In der Wurzel liegen 32 Markdown-Dateien,
davon 29 gebunden.

`.venv/bin/python tools/stand.py <testausgabe>` liefert die sechs Zahlen in einer Zeile, geeignet
als Kopftext der Projektkopie (D318). Die Testzahl wird daraus gelesen, nie getippt.

Die Ausgangslage war `34e1dba`, 315 Registereinträge, 27 Wurzeldateien.

### Die Schichten

- **00** Nukleus, Genesis, Verfassung. `00 §4.2` empfiehlt Governance und Substanz in getrennte
  Scopes — Obligationen gehören **nicht** in den Scope, dessen `participants` abgestimmt werden.
- **01** Atom, Verifier, **zwölf Reject-Codes**, **sieben** Klassifikationszustände. Anhang C
  trägt **sechzehn** Abschnitte. Seit D308 die Versionsausnahme.
- **02** Trust-Flow, Max-Flow und PageRank, Budget `Σ n ≤ D`, Kapazität `⌊C₀γ^d⌋`.
- **03** Profile II. `03 §3.1` Preisblindheit, `03 §3.2` Trägerwert extern, `03 §3.3` Kredit.
- **04** Governance. Ein Vorschlag besteht aus Scope, Vorgängerepoche und Verfassungshash.
- **08** Zweck und Geltungsbereich. `08 §3` trägt das Aufnahmekriterium und die Prüftabelle.

### Der Bestand

`tools/`: `autor.py`, `check_specs.py`, `check_tree.py`, `example_nucleus.py`, `gitter.py`,
`korpus.py`, `offen.py`, `paare.py`, `register_index.py`, `splice_run.py`, `stand.py`,
`szenario_absicherung.py`, `verdikt.py`, dazu `sim/`.

`offen.py` prüft die Nummerierung von `offen.md` und läuft in `make check`; `stand.py` gibt die
sechs Kaltzahlen aus. Beide sind neu seit `00aq`.

**`tools/sim/` ist der Simulationsrahmen** — getrennte Beobachter, getrennte Uhren und Schlüssel,
ein Verzeichnis je Teilnehmer mit Inbox, deklarative Szenarien in JSON mit den Schritten `claim`,
`zustellen`, `uhr`, `zeige` und `erwarte`, sechs Szenarien, eigene Tests. **Jeder weitere
Szenariolauf setzt darauf auf** (Prüfregel 63).

**Die Mutantenkampagne steht über beide Stufen.** `gitter.py` liefert **2511** Einzelmutanten in
drei Familien (1174 in A, 1264 in B, 73 in C); `paare.py` **16958** Paarmutanten (85 Vorrangprobe,
2059 / 4378 / 10436 in den Klassen). Elf der zwölf Reject-Codes sind erreichbar. Über 19469
Mutanten hat sie **keinen einzigen Befund** aus einem Verdikt-Unterschied getragen. Layer 01 ist
damit ausgelesen.

## Was zuletzt entschieden wurde

- **D309, D310** — die drei Rückstände aus `00al`. Berichtigung von D304: neun Zeilen, nicht zwölf.
- **D311** — Moduswechsel in den Anwendungsabschnitt; der Prototypmodus.
- **D312** — Abnahme von Stufe A; zwei Fehler im eigenen Prompt; Prüfregel 63.
- **D313** — zwei Vorarbeiten zur Risikoteilung, und wohin eine Versicherung gehört.
- **D314, D315** — Bindungsregel und Archiv; Prüfregel 64.
- **D316** — die Übergabedatei zerfällt; `offen.md` wird nummeriert und fortgeschrieben; die
  Arbeitsteilung mit dem Werkzeug wird verbindlich. Schliesst den Posten aus D218.
- **D317** — der Repositoriumsname wird `symbolon`; umbenannt wird später.
- **D318** — der Kopf der Projektkopie trägt sechs Zahlen; die Postenzahl kommt hinzu, die Zahl
  der Wurzeldateien nicht. Dazu die Abnahme des Werkzeuglaufs und ein Defekt, der vor dem Merge
  behoben wurde.

## Der nächste Schritt

Der Abschnitt heisst **Öffnung** und steht in `offen.md` als O51 bis O58. Die Vorarbeit ist
getan: O50 ist erledigt, die beiden Werkzeuge stehen. Was bleibt, ist der Weg nach draussen.

1. **O58** — die beiden Implementierungen in ein Repositorium. Die Go-Fassung wird zu `go/` im
   Hauptbaum, mit erhaltener Historie. Der Python-Baum wird **nicht** umgebaut. Tier 1, eigener
   Lauf, und D302 bleibt: die eingefrorene Spec-Kopie ist der Mechanismus der Unabhängigkeit,
   nicht die Repositoriumsgrenze.
2. **O51** Lizenz. Ohne sie ist „open source" eine Behauptung, und eine Förderlinie verlangt eine.
3. **O52** öffentlicher Spiegel, **O53** englische Schale — README, LICENSE, CONTRIBUTING und ein
   Dokument zur Methode. Neu geschrieben, nicht übersetzt. Die Werkstatt bleibt deutsch.
4. **O57** Förderantrag.
5. **O54** normative Sprache und **O55** Umbenennung als eigener Abschnitt, mit eigenem
   Registereintrag, **nach** der Öffnung.

Die Prompt-Dateien dieses Laufs bleiben vorerst in der Wurzel und werden als ungebunden gemeldet.
Das ist die Erinnerung, sie mit der nächsten Übergabe zu archivieren.

Die inhaltliche Arbeit bleibt daneben liegen: Stufe B beginnt als Spec-Arbeit (D313), die drei
Befunde ohne Ort aus D312 werden durch das Aufnahmekriterium aus `08 §3` geschickt. Sie stehen als
O1, O2 und O3 in `offen.md` und sind nicht dringend.

**Die Anwendung mit echten Menschen bleibt zurückgestellt.** `08 §2.2` verlangt vier Menschen mit
einem echten gemeinsamen Anliegen. Warten ist ein zulässiger Zustand; so tun als ob nicht. Die
Öffnung ist der Grund, warum aus dem Warten etwas werden kann.
