"""v lesen: typ-normativ, bedeutungsblind (03-profiles.md §1.3, D77/D83)."""

from __future__ import annotations

from mensch_als_republik import cbor_canon
from mensch_als_republik.profiles.findings import ProfileFinding


def read_v(v: bytes | None) -> tuple[dict | None, tuple[ProfileFinding, ...]]:
    """Dekodiert ``v`` und prüft Kanonizität; Subjekt setzt der Aufrufer (03-prompt.md §3.1).

    Reihenfolge ist normativ (D83): ``decode`` und ``is_canonical`` im selben ``try``.
    """
    if v is None:
        return None, ()
    try:
        obj = cbor_canon.decode(v)
        canonical = cbor_canon.is_canonical(v)
    except Exception:
        return None, (ProfileFinding.UNPARSABLE_V,)
    if not canonical:
        return None, (ProfileFinding.NON_CANONICAL_V,)
    if not isinstance(obj, dict):
        return None, (ProfileFinding.UNPARSABLE_V,)
    return obj, ()
