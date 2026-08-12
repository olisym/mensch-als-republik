"""Testprofil TP-02-PR (02b-golden-anchors.md §2): alpha=1/2 (a=1,b=2), K=20.

Baut auf demselben Graphbauer wie tp02.py (02-golden-anchors.md §1-§2) -- Anker PR-1 verlangt
denselben Graphen wie 02a.
"""

from __future__ import annotations

from mensch_als_republik.trust import RelaxParams

from .tp02 import PARAMS

RP = RelaxParams(base=PARAMS, alpha_num=1, alpha_den=2, rounds=20)
DELTA = 8**20

assert DELTA == 1152921504606846976


def mass_bound(denominator: int, anchors_count: int, params: RelaxParams) -> int:
    """Delta - |A|*D^K*(b-a)^K, exakt und ohne Division (D54).

    Delta*(1-alpha)^K = |A|*(bD)^K*(b-a)^K/b^K = |A|*D^K*(b-a)^K -- b^K kuerzt sich
    vollstaendig gegen Delta heraus. `Delta - Delta // 2**K` ist nur fuer alpha=1/2 exakt
    (D54); diese Produktform gilt fuer jedes Profil.
    """
    D = params.base.D
    K = params.rounds
    b_minus_a = params.alpha_den - params.alpha_num
    return denominator - anchors_count * (D**K) * (b_minus_a**K)
