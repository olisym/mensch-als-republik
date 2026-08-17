"""Autorenkette mit persistenter Spitze und Redo (D120, D122, D127, D129).

DateiRueckhalt setzt drei Persistenzeigenschaften voraus und prüft sie nicht (D127):
atomares ``os.replace``, ``fsync`` der Datei vor dem Rename, ``fsync`` des Verzeichnisses
danach.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Protocol

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mensch_als_republik.atom import (
    Claim,
    build_signed,
    claim_from_bytes,
    claim_id,
    id_genesis_anchor,
    signed_bytes,
)
from mensch_als_republik.verifier import InMemoryStore


class KetteAngehalten(Exception):
    """Weiterschreiben ist der erkannte Fehler (D120)."""


class Rueckhalt(Protocol):
    def spitze_lesen(self) -> bytes | None: ...

    def spitze_schreiben(self, h_prev: bytes) -> None: ...

    def redo_lesen(self) -> bytes | None: ...

    def redo_schreiben(self, signiert: bytes) -> None: ...

    def redo_schliessen(self) -> None: ...


class Ausgang(Protocol):
    def kennt(self, cid: bytes) -> bool: ...

    def aufnehmen(self, claim: Claim) -> None: ...


class SpeicherRueckhalt:
    """Zwei Attribute, sonst nichts (D127)."""

    def __init__(self) -> None:
        self._spitze: bytes | None = None
        self._redo: bytes | None = None

    def spitze_lesen(self) -> bytes | None:
        return self._spitze

    def spitze_schreiben(self, h_prev: bytes) -> None:
        self._spitze = h_prev

    def redo_lesen(self) -> bytes | None:
        return self._redo

    def redo_schreiben(self, signiert: bytes) -> None:
        self._redo = signiert

    def redo_schliessen(self) -> None:
        self._redo = None


class DateiRueckhalt:
    """Spitze als Hex (ASCII), Redo als rohe Bytes; atomares Schreiben (D127)."""

    def __init__(self, pfad: Path) -> None:
        self._pfad = pfad

    def spitze_lesen(self) -> bytes | None:
        datei = self._pfad / "spitze"
        if not datei.exists():
            return None
        return bytes.fromhex(datei.read_text(encoding="ascii").strip())

    def spitze_schreiben(self, h_prev: bytes) -> None:
        self._atomar_schreiben("spitze", h_prev.hex().encode("ascii"))

    def redo_lesen(self) -> bytes | None:
        datei = self._pfad / "redo"
        if not datei.exists():
            return None
        return datei.read_bytes()

    def redo_schreiben(self, signiert: bytes) -> None:
        self._atomar_schreiben("redo", signiert)

    def redo_schliessen(self) -> None:
        datei = self._pfad / "redo"
        try:
            datei.unlink()
        except FileNotFoundError:
            pass
        self._fsync_verzeichnis()

    def _atomar_schreiben(self, name: str, data: bytes) -> None:
        ziel = self._pfad / name
        tmp = self._pfad / f".{name}.tmp"
        with open(tmp, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, ziel)
        self._fsync_verzeichnis()

    def _fsync_verzeichnis(self) -> None:
        fd = os.open(self._pfad, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


class StoreAusgang:
    """Dünner Adapter über ``InMemoryStore`` (D127)."""

    def __init__(self, store: InMemoryStore) -> None:
        self._store = store

    def kennt(self, cid: bytes) -> bool:
        return self._store.get(cid) is not None

    def aufnehmen(self, claim: Claim) -> None:
        self._store.add(claim)


class Kettenzustand(Enum):
    GENESIS = "GENESIS"
    NORMAL = "NORMAL"
    FORTGESETZT = "FORTGESETZT"
    ANGEHALTEN = "ANGEHALTEN"


@dataclass(frozen=True, slots=True)
class Wiederaufnahme:
    zustand: Kettenzustand
    h_prev: bytes | None
    grund: str | None


class Autor:
    """Eine Autorenkette über Rückhalt und Ausgang (D120, D122, D127, D129)."""

    def __init__(self, seed: bytes, rueckhalt: Rueckhalt, ausgang: Ausgang) -> None:
        self._sk = Ed25519PrivateKey.from_private_bytes(seed)
        self.pub = self._sk.public_key().public_bytes_raw()
        self._rueckhalt = rueckhalt
        self._ausgang = ausgang
        self._h_prev: bytes | None = None
        self._zustand: Kettenzustand | None = None
        self._grund: str | None = None

    def wiederaufnehmen(self) -> Wiederaufnahme:
        redo = self._rueckhalt.redo_lesen()
        if redo is not None:
            claim = claim_from_bytes(redo)
            if claim.I != self.pub:
                self._zustand = Kettenzustand.ANGEHALTEN
                self._h_prev = None
                self._grund = "Redo trägt fremdes I"
                return Wiederaufnahme(Kettenzustand.ANGEHALTEN, None, self._grund)
            cid = claim_id(claim)
            if not self._ausgang.kennt(cid):
                self._ausgang.aufnehmen(claim)
            self._rueckhalt.spitze_schreiben(cid)
            self._rueckhalt.redo_schliessen()
            self._h_prev = cid
            self._zustand = Kettenzustand.FORTGESETZT
            self._grund = None
            return Wiederaufnahme(Kettenzustand.FORTGESETZT, cid, None)

        spitze = self._rueckhalt.spitze_lesen()
        if spitze is None:
            h_prev = id_genesis_anchor(self.pub)
            self._h_prev = h_prev
            self._zustand = Kettenzustand.GENESIS
            self._grund = None
            return Wiederaufnahme(Kettenzustand.GENESIS, h_prev, None)
        if not self._ausgang.kennt(spitze):
            self._zustand = Kettenzustand.ANGEHALTEN
            self._h_prev = None
            self._grund = "Spitze nicht im Ausgang"
            return Wiederaufnahme(Kettenzustand.ANGEHALTEN, None, self._grund)
        self._h_prev = spitze
        self._zustand = Kettenzustand.NORMAL
        self._grund = None
        return Wiederaufnahme(Kettenzustand.NORMAL, spitze, None)

    def signieren(
        self,
        *,
        p: str,
        J: tuple[int, bytes],
        t: int,
        v: bytes | None = None,
        N: bytes | None = None,
        t_exp: int | None = None,
    ) -> Claim:
        if self._zustand is None:
            raise RuntimeError("signieren ohne vorheriges wiederaufnehmen")
        if self._zustand is Kettenzustand.ANGEHALTEN:
            raise KetteAngehalten(self._grund)
        assert self._h_prev is not None
        signed = build_signed(
            self._sk,
            J=J,
            p=p,
            t=t,
            h_prev=self._h_prev,
            v=v,
            N=N,
            t_exp=t_exp,
        )
        schritt = "Redo schreiben"
        try:
            self._rueckhalt.redo_schreiben(signed_bytes(signed))
            schritt = "Aussenden"
            self._ausgang.aufnehmen(signed)
            cid = claim_id(signed)
            schritt = "Spitze schreiben"
            self._rueckhalt.spitze_schreiben(cid)
            self._h_prev = cid
            schritt = "Redo schließen"
            self._rueckhalt.redo_schliessen()
        except BaseException:  # B-3: KeyboardInterrupt erbt von BaseException, nicht Exception
            self._zustand = Kettenzustand.ANGEHALTEN
            self._h_prev = None
            self._grund = schritt
            raise
        self._zustand = Kettenzustand.NORMAL
        return signed

    def gabeln(
        self,
        *,
        p: str,
        J: tuple[int, bytes],
        t: int,
        v: bytes | None = None,
        N: bytes | None = None,
        t_exp: int | None = None,
    ) -> Claim:
        """Signiert über die aktuelle Spitze und sendet aus, ohne Redo oder Spitze
        zu schreiben und ohne ``_h_prev`` vorzurücken (D129).

        Schriebe ``gabeln`` einen Redo, machte ein späteres ``wiederaufnehmen`` den
        absichtlichen Fork zur echten Spitze — der Zwilling würde still zum
        Hauptzweig. Schriebe es die Spitze, wäre es kein Fork.

        Ein Abbruch in ``ausgang.aufnehmen`` ist folgenlos für die Kette, weil
        ``gabeln`` den Rückhalt nicht berührt; ein ``try`` mit Halt wie in
        ``signieren`` ist deshalb nicht nötig.
        """
        if self._zustand is None:
            raise RuntimeError("gabeln ohne vorheriges wiederaufnehmen")
        if self._zustand is Kettenzustand.ANGEHALTEN:
            raise KetteAngehalten(self._grund)
        assert self._h_prev is not None
        signed = build_signed(
            self._sk,
            J=J,
            p=p,
            t=t,
            h_prev=self._h_prev,
            v=v,
            N=N,
            t_exp=t_exp,
        )
        self._ausgang.aufnehmen(signed)
        return signed
