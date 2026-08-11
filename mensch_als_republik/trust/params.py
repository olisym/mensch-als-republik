"""Trust-Flow-Parameter (02a §2.1)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrustParams:
    """γ = gamma_num/gamma_den, C(d) = ⌊C0 · γ^d⌋ (einmal am Ende gerundet, §2.2)."""

    C0: int
    gamma_num: int
    gamma_den: int
    D: int

    def __post_init__(self) -> None:
        if self.C0 <= 0:
            raise ValueError("C0 must be > 0")
        if not (0 < self.gamma_num < self.gamma_den):
            raise ValueError("gamma_num must satisfy 0 < gamma_num < gamma_den")
        if self.D < 1:
            raise ValueError("D must be >= 1")
