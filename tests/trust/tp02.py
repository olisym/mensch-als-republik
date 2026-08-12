"""Testprofil TP-02 (02-golden-anchors.md §1-§2): gamma=1/2, C0=16, D=4."""

from __future__ import annotations

from mensch_als_republik.atom import Claim
from mensch_als_republik.trust import TrustParams
from mensch_als_republik.verifier import InMemoryStore

from tests.helpers import Identity, scope_id, store_with

NOW = 1000
T_EXP = 5000
PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)
SCOPE = scope_id("TP-02")

VARIANTS = ("A", "B", "C", "D", "E", "E0", "F")


def _mesh(g1: Identity, g2: Identity, g3: Identity, n: int, scope: bytes, t_exp: int) -> list[Claim]:
    pairs = [(g1, g2), (g2, g1), (g1, g3), (g3, g1), (g2, g3), (g3, g2)]
    return [a.vouch(b, n=n, scope=scope, t=1, t_exp=t_exp) for a, b in pairs]


class Graph:
    def __init__(self, identities: dict[str, Identity], claims: list[Claim], scope: bytes) -> None:
        self.identities = identities
        self.claims = claims
        self.scope = scope

    def __getattr__(self, name: str) -> Identity:
        try:
            return self.identities[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def store(self, *extra: Claim) -> InMemoryStore:
        return store_with(*self.claims, *extra)


def build(variant: str, *, label_suffix: str = "", scope: bytes = SCOPE, t_exp: int = T_EXP) -> Graph:
    """Frische Identitäten je Aufruf; label_suffix hält Schlüssel über Varianten hinweg getrennt."""
    suf = label_suffix or variant
    ALICE = Identity(f"ALICE-{suf}")
    BOB = Identity(f"BOB-{suf}")
    CAROL = Identity(f"CAROL-{suf}")
    g1 = Identity(f"g1-{suf}")
    g2 = Identity(f"g2-{suf}")
    g3 = Identity(f"g3-{suf}")
    EVE = Identity(f"EVE-{suf}")

    claims = [
        ALICE.vouch(BOB, n=4, scope=scope, t=1, t_exp=t_exp),
        BOB.vouch(CAROL, n=4, scope=scope, t=1, t_exp=t_exp),
    ]

    if variant == "A":
        claims += [CAROL.vouch(g, n=4, scope=scope, t=1, t_exp=t_exp) for g in (g1, g2, g3)]
    elif variant == "B":
        claims += [CAROL.vouch(g, n=1, scope=scope, t=1, t_exp=t_exp) for g in (g1, g2, g3)]
    elif variant == "C":
        claims += [CAROL.vouch(g, n=1, scope=scope, t=1, t_exp=t_exp) for g in (g1, g2, g3)]
        claims += _mesh(g1, g2, g3, 2, scope, t_exp)
    elif variant == "D":
        claims += [CAROL.vouch(g, n=1, scope=scope, t=1, t_exp=t_exp) for g in (g1, g2, g3)]
        claims += _mesh(g1, g2, g3, 4, scope, t_exp)
    elif variant == "E":
        claims += [CAROL.vouch(g1, n=4, scope=scope, t=1, t_exp=t_exp)]
        claims += _mesh(g1, g2, g3, 2, scope, t_exp)
    elif variant == "E0":
        claims += [CAROL.vouch(g1, n=4, scope=scope, t=1, t_exp=t_exp)]
    elif variant == "F":
        claims += [
            CAROL.vouch(g1, n=2, scope=scope, t=1, t_exp=t_exp),
            CAROL.vouch(g2, n=1, scope=scope, t=1, t_exp=t_exp),
            CAROL.vouch(g3, n=1, scope=scope, t=1, t_exp=t_exp),
        ]
        claims += _mesh(g1, g2, g3, 2, scope, t_exp)
    else:
        raise ValueError(f"unknown variant {variant!r}")

    identities = {
        "ALICE": ALICE,
        "BOB": BOB,
        "CAROL": CAROL,
        "g1": g1,
        "g2": g2,
        "g3": g3,
        "EVE": EVE,
    }
    return Graph(identities, claims, scope)


def build_A_prime(*, scope: bytes = SCOPE, t_exp: int = T_EXP) -> Graph:
    """T-02.1b: eigener Graph, Rumpf ALICE->BOB + ALICE->{g1,g2,g3} je n=4."""
    ALICE = Identity("ALICE-Ap")
    BOB = Identity("BOB-Ap")
    g1 = Identity("g1-Ap")
    g2 = Identity("g2-Ap")
    g3 = Identity("g3-Ap")

    claims = [
        ALICE.vouch(BOB, n=4, scope=scope, t=1, t_exp=t_exp),
        ALICE.vouch(g1, n=4, scope=scope, t=1, t_exp=t_exp),
        ALICE.vouch(g2, n=4, scope=scope, t=1, t_exp=t_exp),
        ALICE.vouch(g3, n=4, scope=scope, t=1, t_exp=t_exp),
    ]
    identities = {"ALICE": ALICE, "BOB": BOB, "g1": g1, "g2": g2, "g3": g3}
    return Graph(identities, claims, scope)
