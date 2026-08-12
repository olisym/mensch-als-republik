"""PageRank-Relaxation — die schnelle Sicht von Schicht 02 (02 §5, D45-D53).

Kapazitaetsvergessende Relaxation, **keine** Schranke. Fuer harte Gate-Entscheidungen
verboten (§9). Eigene Oberflaeche (D52): eigenes Modul, eigener Rueckgabetyp -- nicht
`trust`, nicht `TrustResult`, kein zusaetzliches Feld an `TrustResult`. Das ist die einzige
mechanische Durchsetzung der Trennlinie, die es gibt.
"""

from __future__ import annotations

from dataclasses import dataclass

from mensch_als_republik.verifier import ClaimStore

from .derive import derive
from .findings import Finding
from .params import TrustParams


@dataclass(frozen=True, slots=True)
class RelaxParams:
    """SHOULD alpha = 1 - gamma (D48). Abweichung ist erlaubt, aber zu begruenden; die
    Klasse erzwingt sie nicht.

    "Ein Graph, zwei Sichten" gilt nur innerhalb eines Parametersatzes: `base` muss
    denselben `TrustParams` entsprechen, mit dem `trust()` fuer denselben Vergleich laeuft.
    Laeuft `rank()` mit einem anderen `base` als der zugehoerige `trust()`-Aufruf, rechnen
    beide Sichten legitim ueber verschiedenen Graphen -- nichts in dieser Klasse erzwingt
    Gleichheit.
    """

    base: TrustParams  # C0, gamma_num, gamma_den, D -- geteilt mit §4
    alpha_num: int  # a
    alpha_den: int  # b
    rounds: int  # K

    def __post_init__(self) -> None:
        if not (0 < self.alpha_num < self.alpha_den):
            raise ValueError("alpha_num must satisfy 0 < alpha_num < alpha_den")
        if self.rounds < 1:
            raise ValueError("rounds must be >= 1")


@dataclass(frozen=True, slots=True)
class RankingResult:
    """Ein Wert ist das Paar (u, denominator) -- kein Skalar, kein float.

    Vergleiche zwischen zwei Laeufen sind nur bei gleichem denominator und gleichen
    Parametern zulaessig: u fuer verschiedene K oder verschiedene |A| lebt ueber
    verschiedenen Nennern (PR-INV-8, PR-INV-9).
    """

    scores: tuple[tuple[bytes, int], ...]  # (Identitaet, u), sortiert nach Bytes
    denominator: int  # Delta
    mass: int  # sum(u) -- fuer PR-INV-2/3
    findings: tuple[Finding, ...]


def rank(
    store: ClaimStore,
    *,
    anchors: frozenset[bytes],
    scope: bytes,
    now: int,
    params: RelaxParams,
    include_flagged: bool = False,
) -> RankingResult:
    """D45-D47: sub-stochastisches P, exakte Integer-Rekursion, feste Rundenzahl K, u_0 = 0.

    u_{k+1}[J] = a*D*(b*D)**k * [J in A] + (b-a) * Sum_{(I,J) in E+} u_k[I] * n_kante(I,J)
    """
    if not anchors:
        raise ValueError("anchors must not be empty")

    # geteilte Ableitung (D49): dieselbe Ableitungsstufe wie trust() (derive.py), aber ohne
    # Knoten-Split -- §5 hat keine Knotenkapazitaeten (K13). C(x) ist bereits als E+-Filter
    # eingegangen (cap >= 1 in derivation.bfs.edges); n_kante ist das rohe Gruppengewicht,
    # nicht cap -- C(x) geht hier nie als Faktor ein (D49).
    derivation = derive(
        store, anchors=anchors, scope=scope, now=now, params=params.base,
        include_flagged=include_flagged,
    )
    edges = derivation.bfs.edges

    a = params.alpha_num
    b = params.alpha_den
    D = params.base.D
    K = params.rounds
    bD = b * D

    # Knotenmenge des Ergebnisses: A vereinigt mit allen Endpunkten von E+ (§3). Wer nicht
    # darin liegt, erscheint gar nicht -- nicht als 0 (PR-INV-7).
    nodes: set[bytes] = set(anchors)
    incoming: dict[bytes, list[tuple[bytes, int]]] = {}
    for e in edges:
        nodes.add(e.author)
        nodes.add(e.subject)
        incoming.setdefault(e.subject, []).append((e.author, e.n_kante))
    for members in incoming.values():
        members.sort()
    node_list = sorted(nodes)

    u: dict[bytes, int] = {j: 0 for j in node_list}  # u_0 = 0 (D47)
    for k in range(K):
        restart = a * D * (bD**k)
        next_u: dict[bytes, int] = {}
        for j in node_list:
            total = restart if j in anchors else 0
            for i, n in incoming.get(j, ()):
                total += (b - a) * u[i] * n
            next_u[j] = total
        u = next_u

    denominator = len(anchors) * (bD**K)
    scores = tuple(sorted(u.items()))
    mass = sum(value for _, value in scores)

    return RankingResult(
        scores=scores,
        denominator=denominator,
        mass=mass,
        findings=derivation.findings,
    )
