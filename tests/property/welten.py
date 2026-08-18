"""hypothesis-Strategien: Welten mit getrennten Beobachtern (werkzeuge.md §4.1)."""

from __future__ import annotations

from dataclasses import dataclass

from hypothesis import strategies as st

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import Claim, claim_id
from mensch_als_republik.governance import decide
from mensch_als_republik.index import classify_all
from mensch_als_republik.policy import NucleusPolicy
from mensch_als_republik.trust.derive import derive
from mensch_als_republik.trust.flow import trust
from mensch_als_republik.trust.params import TrustParams
from mensch_als_republik.verifier import InMemoryStore
from tools.autor import Autor, SpeicherRueckhalt, StoreAusgang
from tools.example_nucleus import build

EX = build()
GOV_POLICY = NucleusPolicy(
    EX.N_gov, declared=EX.constitution_gov["irrevocable_predicates"]
)

# Seeds 0x11… aus example-nucleus.md §2, fortgesetzt für bis zu sechs Identitäten.
_SEEDS = tuple(bytes([0x11 + i] * 32) for i in range(6))

# t_exp je Vouch, Gewichtung 4 : 4 : 1 : 1 — abwesend : künftig : vergangen : grenze.
_T_EXP_LAGEN = (
    "abwesend",
    "abwesend",
    "abwesend",
    "abwesend",
    "künftig",
    "künftig",
    "künftig",
    "künftig",
    "vergangen",
    "grenze",
)


@dataclass(frozen=True, slots=True)
class Welt:
    """Eine zufällige Welt: Identitäten, Anker, Claims, Zustellplan (werkzeuge.md §4.1)."""

    pubs: tuple[bytes, ...]
    anchors: frozenset[bytes]
    params: TrustParams
    vouches: tuple[Claim, ...]
    votes: tuple[Claim, ...]
    delivery: tuple[frozenset[int], ...]
    now: int

    @property
    def claims(self) -> tuple[Claim, ...]:
        return self.vouches + self.votes


class _Signer:
    """Autorenkette; ``kette_fortschreiben=False`` ruft ``gabeln`` (werkzeuge.md §2.4)."""

    def __init__(self, seed: bytes) -> None:
        self._autor = Autor(seed, SpeicherRueckhalt(), StoreAusgang(InMemoryStore()))
        self.pub = self._autor.pub
        self._autor.wiederaufnehmen()
        self._t = 0

    @property
    def naechstes_t(self) -> int:
        """t, das der naechste claim()-Aufruf verwenden wird (D133)."""
        return self._t + 1

    def claim(
        self,
        *,
        p: str,
        J: tuple[int, bytes],
        v: bytes | None = None,
        N: bytes | None = None,
        t_exp: int | None = None,
        kette_fortschreiben: bool = True,
    ) -> Claim:
        self._t += 1
        if kette_fortschreiben:
            return self._autor.signieren(
                p=p, J=J, t=self._t, v=v, N=N, t_exp=t_exp
            )
        return self._autor.gabeln(p=p, J=J, t=self._t, v=v, N=N, t_exp=t_exp)


def speicher(*claims: Claim) -> InMemoryStore:
    """Store in der gegebenen Einfügereihenfolge."""
    store = InMemoryStore()
    for claim in claims:
        store.add(claim)
    return store


def _nuc(scope: bytes, name: str) -> str:
    return f"nuc:{scope.hex()}/{name}@1"


def _vouch_v(n: int) -> bytes:
    return cbor_canon.encode({0: n})


def _vote_v(choice: int) -> bytes:
    return cbor_canon.encode({0: choice})


@st.composite
def welten(
    draw: st.DrawFn,
    *,
    erlaube_ueberzeichnung: bool = False,
    erlaube_equivocation: bool = False,
) -> Welt:
    """Baut eine Welt. Beide Schalter einzeln setzbar, Voreinstellung False."""
    n_ids = draw(st.integers(min_value=3, max_value=6))
    signers = tuple(_Signer(_SEEDS[i]) for i in range(n_ids))
    pubs = tuple(s.pub for s in signers)
    n_anchors = draw(st.integers(min_value=1, max_value=2))
    anchor_idx = draw(
        st.lists(
            st.integers(min_value=0, max_value=n_ids - 1),
            min_size=n_anchors,
            max_size=n_anchors,
            unique=True,
        )
    )
    anchors = frozenset(pubs[i] for i in anchor_idx)
    c0 = draw(st.sampled_from((16, 100)))
    d_budget = draw(st.sampled_from((16, 100)))
    gamma = draw(st.sampled_from(((1, 2), (2, 3))))
    params = TrustParams(C0=c0, gamma_num=gamma[0], gamma_den=gamma[1], D=d_budget)

    now = 1000
    n_vouches = draw(st.integers(min_value=0, max_value=12))
    gruppe: dict[tuple[int, int], int] = {}
    verbraucht: dict[int, int] = {i: 0 for i in range(n_ids)}
    vouches: list[Claim] = []

    def _t_exp(lage: str, t: int) -> int | None:
        if lage == "abwesend":
            return None
        if lage == "künftig":
            return draw(st.integers(min_value=now + 1, max_value=now + 10_000))
        if lage == "grenze":
            return now
        return draw(st.integers(min_value=t + 1, max_value=now - 1))

    def _lebend(t_exp: int | None) -> bool:
        return t_exp is None or t_exp >= now

    def _buche(a: int, s: int, n: int) -> None:
        alt = gruppe.get((a, s), 0)
        neu = max(alt, n)
        verbraucht[a] += neu - alt
        gruppe[(a, s)] = neu

    def _n_lebend(a: int, s: int) -> int | None:
        if erlaube_ueberzeichnung:
            return draw(st.integers(min_value=1, max_value=d_budget))
        obere = gruppe.get((a, s), 0) + (d_budget - verbraucht[a])
        if obere < 1:
            return None
        return draw(st.integers(min_value=1, max_value=obere))

    def _n_tot() -> int:
        return draw(st.integers(min_value=1, max_value=d_budget))

    for _ in range(n_vouches):
        author_i = draw(st.integers(min_value=0, max_value=n_ids - 1))
        subject_i = draw(
            st.integers(min_value=0, max_value=n_ids - 1).filter(lambda j, a=author_i: j != a)
        )
        want_twin = erlaube_equivocation and draw(st.booleans())
        t1 = signers[author_i].naechstes_t
        lage1 = draw(st.sampled_from(_T_EXP_LAGEN))
        t_exp1 = _t_exp(lage1, t1)
        t_exp2: int | None = None
        if want_twin:
            lage2 = draw(st.sampled_from(_T_EXP_LAGEN))
            t_exp2 = _t_exp(lage2, t1 + 1)

        if _lebend(t_exp1):
            n1 = _n_lebend(author_i, subject_i)
            if n1 is None:
                continue
        else:
            n1 = _n_tot()

        n2: int | None = None
        build_twin = want_twin
        if want_twin:
            if _lebend(t_exp2):
                if erlaube_ueberzeichnung:
                    n2 = draw(st.integers(min_value=1, max_value=d_budget))
                else:
                    if _lebend(t_exp1):
                        alt = gruppe.get((author_i, subject_i), 0)
                        grp = max(alt, n1)
                        verbr = verbraucht[author_i] - alt + grp
                    else:
                        grp = gruppe.get((author_i, subject_i), 0)
                        verbr = verbraucht[author_i]
                    obere2 = grp + (d_budget - verbr)
                    if obere2 < 1:
                        build_twin = False
                    else:
                        n2 = draw(st.integers(min_value=1, max_value=obere2))
            else:
                n2 = _n_tot()

        first = signers[author_i].claim(
            p=_nuc(EX.N_res, "vouch"),
            J=(1, pubs[subject_i]),
            v=_vouch_v(n1),
            N=EX.N_res,
            t_exp=t_exp1,
            kette_fortschreiben=not build_twin,
        )
        vouches.append(first)
        if _lebend(t_exp1):
            _buche(author_i, subject_i, n1)
        if build_twin:
            assert n2 is not None
            vouches.append(
                signers[author_i].claim(
                    p=_nuc(EX.N_res, "vouch"),
                    J=(1, pubs[subject_i]),
                    v=_vouch_v(n2),
                    N=EX.N_res,
                    t_exp=t_exp2,
                )
            )
            if _lebend(t_exp2):
                _buche(author_i, subject_i, n2)

    votes: list[Claim] = []
    if draw(st.booleans()):
        # Stimmen nur der Gründer (0x11–0x13) auf den einen Vorschlag des Beispielnukleus.
        for author_i in range(min(3, n_ids)):
            if not draw(st.booleans()):
                continue
            choice = draw(st.integers(min_value=0, max_value=1))
            twin = erlaube_equivocation and draw(st.booleans())
            first = signers[author_i].claim(
                p=_nuc(EX.N_gov, "vote"),
                J=(3, EX.proposal.proposal_hash),
                v=_vote_v(choice),
                N=EX.N_gov,
                kette_fortschreiben=not twin,
            )
            votes.append(first)
            if twin:
                votes.append(
                    signers[author_i].claim(
                        p=_nuc(EX.N_gov, "vote"),
                        J=(3, EX.proposal.proposal_hash),
                        v=_vote_v(1 - choice),
                        N=EX.N_gov,
                    )
                )

    claims = vouches + votes
    n_claims = len(claims)
    if n_claims == 0:
        delivery = tuple(frozenset() for _ in range(n_ids))
    else:
        delivery = tuple(
            draw(
                st.frozensets(
                    st.integers(min_value=0, max_value=n_claims - 1),
                    max_size=n_claims,
                )
            )
            for _ in range(n_ids)
        )
    return Welt(
        pubs=pubs,
        anchors=anchors,
        params=params,
        vouches=tuple(vouches),
        votes=tuple(votes),
        delivery=delivery,
        now=now,
    )


def _sorted_pairs(mapping: dict[bytes, int]) -> list[list[object]]:
    return [[k, mapping[k]] for k in sorted(mapping)]


def _findings_bytes(findings: tuple) -> list[list[object]]:
    return [[f.kind.value, f.subject] for f in findings]


def fingerprint_derive(store: InMemoryStore, welt: Welt) -> bytes:
    """Byte-Identität von ``derive`` (werkzeuge.md §4.2 P-1)."""
    result = derive(
        store,
        anchors=welt.anchors,
        scope=EX.N_res,
        now=welt.now,
        params=welt.params,
    )
    payload = {
        0: _sorted_pairs(result.bfs.distance),
        1: _sorted_pairs(result.bfs.node_capacity),
        2: [
            [e.author, e.subject, e.cap, e.claim_id, e.n_kante]
            for e in result.bfs.edges
        ],
        3: _findings_bytes(result.findings),
    }
    return cbor_canon.encode(payload)


def fingerprint_trust(store: InMemoryStore, welt: Welt) -> bytes:
    """Byte-Identität von ``trust`` (werkzeuge.md §4.2 P-1)."""
    targets = frozenset(p for p in welt.pubs if p not in welt.anchors)
    result = trust(
        store,
        anchors=welt.anchors,
        targets=targets,
        scope=EX.N_res,
        now=welt.now,
        params=welt.params,
    )
    payload = {
        0: result.value,
        1: result.disjoint_paths,
        2: list(result.cut),
        3: _findings_bytes(result.findings),
    }
    return cbor_canon.encode(payload)


def fingerprint_decide(store: InMemoryStore, welt: Welt) -> bytes:
    """Byte-Identität von ``decide`` (werkzeuge.md §4.2 P-1)."""
    result = decide(
        store,
        epoch=EX.epoch_1,
        proposal=EX.proposal,
        genesis_obj=EX.genesis_gov,
        constitution_obj=EX.constitution_gov,
        target_constitution_obj=EX.constitution_2,
        known_proposals={EX.proposal.proposal_hash: EX.proposal},
        now=welt.now,
        policy=GOV_POLICY,
    )
    participants = (
        sorted(result.participants) if result.participants is not None else None
    )
    payload = {
        0: result.state.value,
        1: list(result.yes),
        2: list(result.no),
        3: participants,
        4: list(result.threshold) if result.threshold is not None else None,
        5: _findings_bytes(result.findings),
    }
    return cbor_canon.encode(payload)


def fingerprint_classify(store: InMemoryStore, welt: Welt) -> bytes:
    """Byte-Identität von ``classify_all`` (werkzeuge.md §4.2 P-1)."""
    result = classify_all(store, welt.now)
    payload = [
        [cid, result[cid].state.value, result[cid].trust_usable]
        for cid in sorted(result)
    ]
    return cbor_canon.encode(payload)


def kapazitaeten(store: InMemoryStore, welt: Welt) -> dict[bytes, int]:
    """C(x) für jede Identität; unerreichbar = 0. Nur Paketrechnung."""
    result = derive(
        store,
        anchors=welt.anchors,
        scope=EX.N_res,
        now=welt.now,
        params=welt.params,
    )
    return {p: result.bfs.node_capacity.get(p, 0) for p in welt.pubs}


def flusswerte(store: InMemoryStore, welt: Welt) -> dict[bytes, int]:
    """trust()-Wert je Nicht-Anker. Nur Paketrechnung."""
    values: dict[bytes, int] = {}
    for pub in welt.pubs:
        if pub in welt.anchors:
            continue
        values[pub] = trust(
            store,
            anchors=welt.anchors,
            targets=frozenset({pub}),
            scope=EX.N_res,
            now=welt.now,
            params=welt.params,
        ).value
    return values


def hoeheres_vertrauen(teil: InMemoryStore, voll: InMemoryStore, welt: Welt) -> bool:
    """True gdw. die Teilmenge irgendwo streng höheres Vertrauen zeigt (02 §7, D118)."""
    k_teil = kapazitaeten(teil, welt)
    k_voll = kapazitaeten(voll, welt)
    if any(k_teil[p] > k_voll[p] for p in welt.pubs):
        return True
    f_teil = flusswerte(teil, welt)
    f_voll = flusswerte(voll, welt)
    return any(f_teil[p] > f_voll[p] for p in f_teil)


def auszaehlung(store: InMemoryStore, welt: Welt):
    """``decide`` gegen den Aufnahmevorschlag des Beispielnukleus."""
    return decide(
        store,
        epoch=EX.epoch_1,
        proposal=EX.proposal,
        genesis_obj=EX.genesis_gov,
        constitution_obj=EX.constitution_gov,
        target_constitution_obj=EX.constitution_2,
        known_proposals={EX.proposal.proposal_hash: EX.proposal},
        now=welt.now,
        policy=GOV_POLICY,
    )


def teilmengen(claims: tuple[Claim, ...], welt: Welt) -> list[tuple[Claim, ...]]:
    """Zustellplan plus Leave-one-out — die Teilmengen, gegen die Monotonie gehalten wird."""
    seen: set[tuple[bytes, ...]] = set()
    out: list[tuple[Claim, ...]] = []
    for indices in welt.delivery:
        subset = tuple(claims[i] for i in sorted(indices) if i < len(claims))
        key = tuple(sorted(claim_id(c) for c in subset))
        if key not in seen:
            seen.add(key)
            out.append(subset)
    for i in range(len(claims)):
        subset = tuple(c for j, c in enumerate(claims) if j != i)
        key = tuple(sorted(claim_id(c) for c in subset))
        if key not in seen:
            seen.add(key)
            out.append(subset)
    return out
