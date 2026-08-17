"""Autorenkette: Vertrag über beide Rückhalte, Absturzaufzählung, Oberfläche (D120, D122, D127)."""

from __future__ import annotations

from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mensch_als_republik.atom import (
    Claim,
    build_signed,
    claim_id,
    id_genesis_anchor,
    signed_bytes,
)
from mensch_als_republik.verifier import InMemoryStore
from tools.autor import (
    Autor,
    DateiRueckhalt,
    KetteAngehalten,
    Kettenzustand,
    Rueckhalt,
    SpeicherRueckhalt,
    StoreAusgang,
)

SEED = b"\x11" * 32
SUBJECT = b"\x22" * 32
P = "core/revoke@1"
J: tuple[int, bytes] = (1, SUBJECT)


@pytest.fixture(params=["speicher", "datei"])
def rueckhalt(request: pytest.FixtureRequest, tmp_path: Path) -> Rueckhalt:
    if request.param == "speicher":
        return SpeicherRueckhalt()
    return DateiRueckhalt(tmp_path)


@pytest.fixture
def store() -> InMemoryStore:
    return InMemoryStore()


@pytest.fixture
def ausgang(store: InMemoryStore) -> StoreAusgang:
    return StoreAusgang(store)


def test_genesis(rueckhalt: Rueckhalt, ausgang: StoreAusgang) -> None:
    autor = Autor(SEED, rueckhalt, ausgang)
    w = autor.wiederaufnehmen()
    assert w.zustand is Kettenzustand.GENESIS
    assert w.h_prev == id_genesis_anchor(autor.pub)
    assert w.grund is None


def test_drei_claims_hintereinander(
    rueckhalt: Rueckhalt, ausgang: StoreAusgang, store: InMemoryStore
) -> None:
    autor = Autor(SEED, rueckhalt, ausgang)
    autor.wiederaufnehmen()
    c1 = autor.signieren(p=P, J=J, t=1)
    c2 = autor.signieren(p=P, J=J, t=2)
    c3 = autor.signieren(p=P, J=J, t=3)
    assert c1.h_prev == id_genesis_anchor(autor.pub)
    assert c2.h_prev == claim_id(c1)
    assert c3.h_prev == claim_id(c2)
    assert store.get(claim_id(c1)) is not None
    assert store.get(claim_id(c2)) is not None
    assert store.get(claim_id(c3)) is not None
    assert rueckhalt.spitze_lesen() == claim_id(c3)


def test_neustart_nimmt_normal_auf(
    rueckhalt: Rueckhalt, ausgang: StoreAusgang
) -> None:
    erster = Autor(SEED, rueckhalt, ausgang)
    erster.wiederaufnehmen()
    erster.signieren(p=P, J=J, t=1)
    c2 = erster.signieren(p=P, J=J, t=2)
    zweiter = Autor(SEED, rueckhalt, ausgang)
    w = zweiter.wiederaufnehmen()
    assert w.zustand is Kettenzustand.NORMAL
    assert w.h_prev == claim_id(c2)
    c3 = zweiter.signieren(p=P, J=J, t=3)
    assert c3.h_prev == claim_id(c2)


def test_spitze_unbekannt_haelt_an(
    rueckhalt: Rueckhalt, ausgang: StoreAusgang
) -> None:
    autor = Autor(SEED, rueckhalt, ausgang)
    autor.wiederaufnehmen()
    c1 = autor.signieren(p=P, J=J, t=1)
    spitze = rueckhalt.spitze_lesen()
    leer_store = InMemoryStore()
    leer = StoreAusgang(leer_store)
    neu = Autor(SEED, rueckhalt, leer)
    w = neu.wiederaufnehmen()
    assert w.zustand is Kettenzustand.ANGEHALTEN
    assert w.h_prev is None
    assert w.grund is not None
    with pytest.raises(KetteAngehalten):
        neu.signieren(p=P, J=J, t=2)
    assert leer_store.all_claims() == []
    assert rueckhalt.redo_lesen() is None
    assert rueckhalt.spitze_lesen() == spitze == claim_id(c1)


def test_fremder_redo_haelt_an(
    rueckhalt: Rueckhalt, ausgang: StoreAusgang
) -> None:
    fremd_sk = Ed25519PrivateKey.from_private_bytes(b"\x22" * 32)
    fremd = build_signed(
        fremd_sk,
        J=J,
        p=P,
        t=1,
        h_prev=id_genesis_anchor(fremd_sk.public_key().public_bytes_raw()),
    )
    rueckhalt.redo_schreiben(signed_bytes(fremd))
    autor = Autor(SEED, rueckhalt, ausgang)
    w = autor.wiederaufnehmen()
    assert w.zustand is Kettenzustand.ANGEHALTEN
    assert w.h_prev is None
    assert w.grund is not None
    w2 = autor.wiederaufnehmen()
    assert w2.zustand is Kettenzustand.ANGEHALTEN


def test_signieren_ohne_wiederaufnehmen(
    rueckhalt: Rueckhalt, ausgang: StoreAusgang
) -> None:
    autor = Autor(SEED, rueckhalt, ausgang)
    with pytest.raises(RuntimeError):
        autor.signieren(p=P, J=J, t=1)


class Bruch(Exception):
    """Absturz am k-ten Schreibvorgang (D127)."""


class _ZaehlRueckhalt:
    def __init__(self, innen: Rueckhalt, zaehler: list[int], bei: int | None) -> None:
        self._innen = innen
        self._zaehler = zaehler
        self._bei = bei

    def spitze_lesen(self) -> bytes | None:
        return self._innen.spitze_lesen()

    def redo_lesen(self) -> bytes | None:
        return self._innen.redo_lesen()

    def spitze_schreiben(self, h_prev: bytes) -> None:
        self._treffen()
        self._innen.spitze_schreiben(h_prev)

    def redo_schreiben(self, signiert: bytes) -> None:
        self._treffen()
        self._innen.redo_schreiben(signiert)

    def redo_schliessen(self) -> None:
        self._treffen()
        self._innen.redo_schliessen()

    def _treffen(self) -> None:
        self._zaehler[0] += 1
        if self._bei is not None and self._zaehler[0] == self._bei:
            raise Bruch()


class _ZaehlAusgang:
    def __init__(self, innen: StoreAusgang, zaehler: list[int], bei: int | None) -> None:
        self._innen = innen
        self._zaehler = zaehler
        self._bei = bei

    def kennt(self, cid: bytes) -> bool:
        return self._innen.kennt(cid)

    def aufnehmen(self, claim: Claim) -> None:
        self._zaehler[0] += 1
        if self._bei is not None and self._zaehler[0] == self._bei:
            raise Bruch()
        self._innen.aufnehmen(claim)


# k | gebrochen bei     | Zustand danach    | Claim im Ausgang
# 1 | Redo schreiben    | GENESIS/NORMAL    | nein
# 2 | Aussenden         | FORTGESETZT       | ja
# 3 | Spitze schreiben  | FORTGESETZT       | ja
# 4 | Redo schließen    | FORTGESETZT       | ja
# – | ungestört         | NORMAL            | ja


@pytest.mark.parametrize("k", [1, 2, 3, 4, None], ids=["k1", "k2", "k3", "k4", "ungestoert"])
def test_absturzaufzaehlung(
    rueckhalt: Rueckhalt,
    ausgang: StoreAusgang,
    store: InMemoryStore,
    tmp_path: Path,
    k: int | None,
) -> None:
    if isinstance(rueckhalt, DateiRueckhalt):
        ref_pfad = tmp_path / "ungestoert"
        ref_pfad.mkdir()
        ref_r: Rueckhalt = DateiRueckhalt(ref_pfad)
    else:
        ref_r = SpeicherRueckhalt()
    ref_store = InMemoryStore()
    ref_a = StoreAusgang(ref_store)
    ref = Autor(SEED, ref_r, ref_a)
    ref.wiederaufnehmen()
    c1_ref = ref.signieren(p=P, J=J, t=1)
    c2_ref = ref.signieren(p=P, J=J, t=2)
    c3_ref = ref.signieren(p=P, J=J, t=3)

    autor = Autor(SEED, rueckhalt, ausgang)
    autor.wiederaufnehmen()
    autor.signieren(p=P, J=J, t=1)
    autor.signieren(p=P, J=J, t=2)

    zaehler = [0]
    z_r = _ZaehlRueckhalt(rueckhalt, zaehler, k)
    z_a = _ZaehlAusgang(ausgang, zaehler, k)
    bruch = Autor(SEED, z_r, z_a)
    bruch.wiederaufnehmen()
    try:
        bruch.signieren(p=P, J=J, t=3)
    except Bruch:
        assert k is not None
    else:
        assert k is None

    neu = Autor(SEED, rueckhalt, ausgang)
    w = neu.wiederaufnehmen()
    pub = neu.pub
    eigene = [c for c in store.all_claims() if c.I == pub]
    got = {signed_bytes(c) for c in eigene}
    zwei = {signed_bytes(c1_ref), signed_bytes(c2_ref)}
    drei = zwei | {signed_bytes(c3_ref)}
    if k == 1:
        assert w.zustand is Kettenzustand.NORMAL
        assert got == zwei
    elif k is None:
        assert w.zustand is Kettenzustand.NORMAL
        assert got == drei
    else:
        assert w.zustand is Kettenzustand.FORTGESETZT
        assert got == drei

    gesehen: set[bytes] = set()
    for c in eigene:
        assert c.h_prev not in gesehen
        gesehen.add(c.h_prev)

    by_prev = {c.h_prev: c for c in eigene}
    cur = id_genesis_anchor(pub)
    last = None
    while cur in by_prev:
        last = by_prev[cur]
        cur = claim_id(last)
    assert last is not None
    assert rueckhalt.spitze_lesen() == claim_id(last)

    ids_vorher = {claim_id(c) for c in store.all_claims()}
    spitze_vorher = rueckhalt.spitze_lesen()
    w2 = neu.wiederaufnehmen()
    assert w2.h_prev == w.h_prev
    assert {claim_id(c) for c in store.all_claims()} == ids_vorher
    assert rueckhalt.spitze_lesen() == spitze_vorher
    assert w2.zustand is Kettenzustand.NORMAL

    if k == 1:
        erneut = neu.signieren(p=P, J=J, t=3)
        assert signed_bytes(erneut) == signed_bytes(c3_ref)
        folge = neu.signieren(p=P, J=J, t=4)
        assert folge.h_prev == claim_id(erneut)
    else:
        folge = neu.signieren(p=P, J=J, t=4)
        assert folge.h_prev == w.h_prev


def test_oberflaeche_gibt_weder_seed_noch_schluessel_noch_spitze(
    rueckhalt: Rueckhalt, ausgang: StoreAusgang
) -> None:
    autor = Autor(SEED, rueckhalt, ausgang)
    w = autor.wiederaufnehmen()
    spitze = w.h_prev
    for name in dir(autor):
        if name.startswith("_"):
            continue
        wert = getattr(autor, name)
        if callable(wert):
            try:
                wert = wert()
            except TypeError:
                continue
        assert wert != SEED
        assert not isinstance(wert, Ed25519PrivateKey)
        assert wert != spitze
