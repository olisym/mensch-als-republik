"""Simulation — sechs Szenarien mit getrennten Beobachter-Stores (werkzeuge.md §3.3)."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import claim_id, signed_bytes
from tools.sim import run_scenario
from tools.sim.welt import Welt

_SCENARIOS = Path(__file__).resolve().parent.parent / "tools" / "sim" / "scenarios"

_SEED = b"\x11" * 32
_SCOPE = bytes(range(32))
_P = f"nuc:{_SCOPE.hex()}/vouch@1"
_J: tuple[int, bytes] = (1, b"\x22" * 32)
_V = cbor_canon.encode({0: 1})


def _run(name: str) -> None:
    raw = (_SCENARIOS / f"{name}.json").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / f"{name}.json"
        path.write_text(raw.replace("PLACEHOLDER", tmp), encoding="utf-8")
        run_scenario(path)


@pytest.mark.parametrize("name", ["s1", "s2", "s3", "s4", "s5", "s6"])
def test_scenario(name: str) -> None:
    _run(name)


def test_hat_claim_glaubt_dem_dateinamen_nicht(tmp_path: Path) -> None:
    """Dateiname und Inhalt fallen auseinander: der Inhalt gewinnt (D132, D138)."""
    welt = Welt.anlegen(tmp_path / "welt")
    tp = welt.teilnehmer_anlegen("alice", _SEED, now=1000)
    claim_a = tp.claim_signieren(p=_P, J=_J, t=1, v=_V, N=_SCOPE)
    claim_b = tp.claim_signieren(p=_P, J=_J, t=2, v=_V, N=_SCOPE)
    cid_a = claim_id(claim_a)
    cid_b = claim_id(claim_b)
    tp.inbox_path(cid_a).unlink()
    tp.inbox_path(cid_b).write_bytes(signed_bytes(claim_a))

    assert not tp.hat_claim(cid_b)
    assert not tp.hat_claim(cid_a)
    store = tp.store_laden()
    ids = {claim_id(c) for c in store.all_claims()}
    assert cid_a in ids and cid_b not in ids


def test_store_laden_ueberspringt_unlesbare_datei(tmp_path: Path) -> None:
    """Abgeschnittene Inbox-Datei: store_laden wirft nicht, uebrige Claims bleiben (D131)."""
    welt = Welt.anlegen(tmp_path / "welt")
    tp = welt.teilnehmer_anlegen("alice", _SEED, now=1000)
    claim_a = tp.claim_signieren(p=_P, J=_J, t=1, v=_V, N=_SCOPE)
    claim_b = tp.claim_signieren(p=_P, J=_J, t=2, v=_V, N=_SCOPE)
    (tp.path / "inbox" / f"{bytes(32).hex()}.cbor").write_bytes(b"\x00")
    store = tp.store_laden()
    ids = {claim_id(c) for c in store.all_claims()}
    assert ids == {claim_id(claim_a), claim_id(claim_b)}
