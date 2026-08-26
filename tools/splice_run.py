#!/usr/bin/env python3
"""Harness für Splice-Skripte: ein Aufruf statt neun Zeilen (D225).

Lässt den Splice im Arbeitsverzeichnis laufen, erzwingt das Scheitern des
zweiten Laufs, prüft am Ergebnis die Zeilenlänge (D222, Prüfregel 42) und
setzt bei Fehlschlag mit ``git checkout --`` zurück. Committet nicht.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from check_specs import check_line_length

ROOT = Path(__file__).resolve().parent.parent


def restore() -> None:
    """``git checkout --`` auf die Pfade aus ``git diff --name-only`` (D225)."""
    listed = subprocess.run(
        ["git", "diff", "--name-only"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    paths = [p for p in listed.stdout.splitlines() if p]
    if not paths:
        return
    subprocess.run(["git", "checkout", "--", *paths], cwd=ROOT, check=True)
    print("zurückgesetzt: " + ", ".join(paths))


def main() -> int:
    if len(sys.argv) != 2:
        print("Aufruf: splice_run.py <skript>")
        return 1
    script = Path(sys.argv[1]).resolve()

    porcelain = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    if porcelain.stdout:
        print("Arbeitsbaum nicht sauber.")
        print(porcelain.stdout, end="")
        return 1

    first = subprocess.run([sys.executable, str(script)], cwd=ROOT)
    if first.returncode != 0:
        print("erster Lauf gescheitert.")
        restore()
        return 1

    second = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    combined = (second.stdout or "") + (second.stderr or "")
    lines = combined.splitlines()
    if lines:
        print(lines[-1])
    if second.returncode == 0:
        print("zweiter Lauf ist durchgelaufen.")
        restore()
        return 1

    numstat = subprocess.run(
        ["git", "diff", "--numstat"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    print(numstat.stdout, end="")
    rows = [ln for ln in numstat.stdout.splitlines() if ln]
    if not rows:
        print("keine Datei geändert.")
        restore()
        return 1

    added = 0
    deleted = 0
    md_abort = False
    for row in rows:
        ins, outs, path = row.split("\t", 2)
        added += int(ins) if ins != "-" else 0
        deleted += int(outs) if outs != "-" else 0
        if not path.endswith(".md"):
            continue
        work_path = ROOT / path
        if not work_path.exists():
            continue
        work_hits = check_line_length(work_path.read_text(encoding="utf-8"))
        shown = subprocess.run(
            ["git", "show", f"HEAD:{path}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        base_text = shown.stdout if shown.returncode == 0 else ""
        base_hits = check_line_length(base_text)
        if len(work_hits) > len(base_hits):
            md_abort = True
            print(path)
            known = set(base_hits)
            for hit in work_hits:
                if hit not in known:
                    print(f"  {hit}")
    if md_abort:
        restore()
        return 1

    n = len(rows)
    noun = "Datei" if n == 1 else "Dateien"
    print(f"ok  {n} {noun}, +{added} −{deleted}")
    print("zweiter Lauf gescheitert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
