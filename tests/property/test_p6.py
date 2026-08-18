"""P-6 — Zeitgrenze (werkzeuge.md §4.2, 01 §6).

Ein Claim ist zeitlich gültig gdw. ``now ≤ t_exp``. Über zufällige ``t_exp``
und ``now`` beiderseits der Grenze, mit ``now = t_exp`` als ausdrücklich
erzeugtem Fall. Bis ``tools/sim/scenarios/s6.json`` war die Regel nirgends
als Zusicherung geprüft.
"""

from __future__ import annotations

from hypothesis import given, strategies as st

from mensch_als_republik.atom import claim_id
from mensch_als_republik.index import classify_all
from mensch_als_republik.verifier import State

from tests.property.welten import EX, _SEEDS, _Signer, _nuc, _vouch_v, speicher


@st.composite
def _t_exp_und_now(draw: st.DrawFn) -> tuple[int, int]:
    t_exp = draw(st.integers(min_value=2, max_value=10_000))
    lage = draw(st.sampled_from(("equal", "below", "above")))
    if lage == "equal":
        now = t_exp
    elif lage == "below":
        now = draw(st.integers(min_value=0, max_value=t_exp))
    else:
        now = draw(st.integers(min_value=t_exp + 1, max_value=t_exp + 10_000))
    return t_exp, now


@given(_t_exp_und_now())
def test_p6_temporally_valid_iff_now_le_t_exp(grenzen: tuple[int, int]) -> None:
    t_exp, now = grenzen
    anna = _Signer(_SEEDS[0])
    bruno = _Signer(_SEEDS[1])
    claim = anna.claim(
        p=_nuc(EX.N_res, "vouch"),
        J=(1, bruno.pub),
        v=_vouch_v(1),
        N=EX.N_res,
        t_exp=t_exp,
    )
    result = classify_all(speicher(claim), now)
    state = result[claim_id(claim)].state
    if now <= t_exp:
        assert state is State.ACTIVE
    else:
        assert state is State.EXPIRED
