"""Teilnehmer, Verzeichnisse, Zustellung (sim-prompt.md §2)."""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

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


@dataclass
class Teilnehmer:
    """Ein Beobachter mit eigenem Verzeichnis, Schlüssel und Inbox."""

    name: str
    path: Path
    seed: bytes
    _sk: Ed25519PrivateKey = field(repr=False)
    pub: bytes = field(repr=False)

    @classmethod
    def anlegen(cls, root: Path, name: str, seed: bytes, now: int) -> Teilnehmer:
        path = root / name
        inbox = path / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        (path / "key.bin").write_bytes(seed)
        (path / "now").write_text(str(now), encoding="ascii")
        sk = Ed25519PrivateKey.from_private_bytes(seed)
        pub = sk.public_key().public_bytes_raw()
        h_prev = id_genesis_anchor(pub)
        (path / "h_prev").write_text(h_prev.hex(), encoding="ascii")
        return cls(name=name, path=path, seed=seed, _sk=sk, pub=pub)

    def read_now(self) -> int:
        return int((self.path / "now").read_text(encoding="ascii").strip())

    def write_now(self, now: int) -> None:
        (self.path / "now").write_text(str(now), encoding="ascii")

    def read_h_prev(self) -> bytes:
        return bytes.fromhex((self.path / "h_prev").read_text(encoding="ascii").strip())

    def write_h_prev(self, h_prev: bytes) -> None:
        (self.path / "h_prev").write_text(h_prev.hex(), encoding="ascii")

    def inbox_path(self, cid: bytes) -> Path:
        return self.path / "inbox" / f"{cid.hex()}.cbor"

    def hat_claim(self, cid: bytes) -> bool:
        return self.inbox_path(cid).is_file()

    def claim_einlegen(self, claim: Claim) -> None:
        cid = claim_id(claim)
        self.inbox_path(cid).write_bytes(signed_bytes(claim))

    def claim_signieren(
        self,
        *,
        p: str,
        J: tuple[int, bytes],
        t: int,
        v: bytes | None = None,
        N: bytes | None = None,
        t_exp: int | None = None,
        kette_fortschreiben: bool = True,
    ) -> Claim:
        h_prev = self.read_h_prev()
        signed = build_signed(
            self._sk,
            J=J,
            p=p,
            t=t,
            h_prev=h_prev,
            v=v,
            N=N,
            t_exp=t_exp,
        )
        self.claim_einlegen(signed)
        if kette_fortschreiben:
            self.write_h_prev(claim_id(signed))
        return signed

    def store_laden(self) -> InMemoryStore:
        store = InMemoryStore()
        inbox = self.path / "inbox"
        for path in sorted(inbox.glob("*.cbor")):
            store.add(claim_from_bytes(path.read_bytes()))
        return store


@dataclass
class Welt:
    """Weltpfad mit benannten Teilnehmern — kein gemeinsamer Store."""

    root: Path
    teilnehmer: dict[str, Teilnehmer] = field(default_factory=dict)

    @classmethod
    def anlegen(cls, root: Path) -> Welt:
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True, exist_ok=True)
        return cls(root=root)

    def teilnehmer_anlegen(self, name: str, seed: bytes, now: int) -> Teilnehmer:
        tp = Teilnehmer.anlegen(self.root, name, seed, now)
        self.teilnehmer[name] = tp
        return tp

    def zustellen(
        self,
        von: str,
        an: str | list[str],
        *,
        nur: list[bytes] | None = None,
    ) -> int:
        """Kopiert fehlende Claims aus von/inbox nach an/inbox; gibt Anzahl zurück."""
        quelle = self.teilnehmer[von]
        ziele = list(self.teilnehmer) if an == "alle" else ([an] if isinstance(an, str) else an)
        kopiert = 0
        for ziel_name in ziele:
            if ziel_name == von:
                continue
            ziel = self.teilnehmer[ziel_name]
            paths = sorted((quelle.path / "inbox").glob("*.cbor"))
            if nur is not None:
                allowed = {cid.hex() for cid in nur}
                paths = [p for p in paths if p.stem in allowed]
            for path in paths:
                cid_hex = path.stem
                if ziel.hat_claim(bytes.fromhex(cid_hex)):
                    continue
                ziel.inbox_path(bytes.fromhex(cid_hex)).write_bytes(path.read_bytes())
                kopiert += 1
        return kopiert
