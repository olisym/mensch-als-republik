"""Szenariodatei lesen und ausführen (werkzeuge.md §3.2)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import Claim, claim_id
from mensch_als_republik.governance import (
    decide,
    verify_ratification,
)
from mensch_als_republik.policy import NucleusPolicy
from mensch_als_republik.profiles import membership
from mensch_als_republik.trust.derive import derive
from mensch_als_republik.trust.findings import TrustFinding
from mensch_als_republik.trust.params import TrustParams
from mensch_als_republik.verifier import classify

from tools.example_nucleus import ExampleNucleus, build
from tools.sim.anzeige import tabelle
from tools.sim.welt import Welt


@dataclass
class Kontext:
    """Laufzeitkontext eines Szenarios."""

    welt: Welt | None = None
    ex: ExampleNucleus | None = None
    labels: dict[str, Claim] = field(default_factory=dict)


def _seed(byte_val: int) -> bytes:
    return bytes([byte_val] * 32)


NAMEN_SEED = {
    "anna": 0x11,
    "bruno": 0x12,
    "chris": 0x13,
    "dora": 0x14,
}


def _policy(ex: ExampleNucleus, scope: bytes) -> NucleusPolicy:
    if scope == ex.N_gov:
        return NucleusPolicy(ex.N_gov, declared=ex.constitution_gov["irrevocable_predicates"])
    return NucleusPolicy(ex.N_res, declared=ex.constitution_res["irrevocable_predicates"])


def _resolve_bytes(value: str, ex: ExampleNucleus) -> bytes:
    table = {
        "constitution_hash_gov": ex.constitution_hash_gov,
        "constitution_hash_2": ex.constitution_hash_2,
        "constitution_hash_res": ex.constitution_hash_res,
        "N_gov": ex.N_gov,
        "N_res": ex.N_res,
        "proposal_hash": ex.proposal.proposal_hash,
        "epoch_id_1": ex.epoch_1.epoch_id,
        "epoch_id_2": ex.epoch_2.epoch_id,
    }
    if value in table:
        return table[value]
    if len(value) == 64 and all(c in "0123456789abcdef" for c in value):
        return bytes.fromhex(value)
    raise ValueError(f"unknown byte reference: {value!r}")


def _resolve_subject(name: str, ctx: Kontext) -> bytes:
    assert ctx.ex is not None
    mapping = {
        "anna": ctx.ex.anna.pub,
        "bruno": ctx.ex.bruno.pub,
        "chris": ctx.ex.chris.pub,
        "dora": ctx.ex.dora.pub,
    }
    if name not in mapping:
        raise ValueError(f"unknown subject: {name!r}")
    return mapping[name]


def _resolve_j(raw: list[Any], ctx: Kontext) -> tuple[int, bytes]:
    tag = int(raw[0])
    ref = raw[1]
    if isinstance(ref, str):
        return tag, _resolve_bytes(ref, ctx.ex)  # type: ignore[arg-type]
    raise ValueError(f"unsupported J reference: {raw!r}")


def _resolve_scope(name: str, ctx: Kontext) -> bytes:
    assert ctx.ex is not None
    if name in ("gov", "N_gov"):
        return ctx.ex.N_gov
    if name in ("res", "N_res"):
        return ctx.ex.N_res
    raise ValueError(f"unknown scope: {name!r}")


def _constitution_obj(name: str, ctx: Kontext) -> dict:
    assert ctx.ex is not None
    if name in ("gov", "constitution_hash_gov"):
        return ctx.ex.constitution_gov
    if name in ("gov2", "constitution_hash_2"):
        return ctx.ex.constitution_2
    if name in ("res", "constitution_hash_res"):
        return ctx.ex.constitution_res
    raise ValueError(f"unknown constitution: {name!r}")


def _constitution_hash(name: str, ctx: Kontext) -> bytes:
    assert ctx.ex is not None
    if name in ("gov", "constitution_hash_gov"):
        return ctx.ex.constitution_hash_gov
    if name in ("gov2", "constitution_hash_2"):
        return ctx.ex.constitution_hash_2
    if name in ("res", "constitution_hash_res"):
        return ctx.ex.constitution_hash_res
    raise ValueError(f"unknown constitution hash: {name!r}")


def _nuc(scope: bytes, name: str) -> str:
    return f"nuc:{scope.hex()}/{name}@1"


def _schritt_welt(step: dict[str, Any], ctx: Kontext) -> None:
    pfad = Path(step["pfad"])
    ctx.welt = Welt.anlegen(pfad)
    for tp in step["teilnehmer"]:
        name = tp["name"]
        seed = _seed(int(tp["seed"], 16)) if isinstance(tp["seed"], str) else _seed(tp["seed"])
        now = int(tp["now"])
        ctx.welt.teilnehmer_anlegen(name, seed, now)


def _schritt_genesis(step: dict[str, Any], ctx: Kontext) -> None:
    if step.get("quelle") != "beispielnukleus":
        raise ValueError(f"unknown genesis source: {step!r}")
    ctx.ex = build()


def _schritt_claim(step: dict[str, Any], ctx: Kontext) -> None:
    assert ctx.welt is not None and ctx.ex is not None
    autor = ctx.welt.teilnehmer[step["autor"]]
    scope = _resolve_scope(step["scope"], ctx)
    praedikat = step["praedikat"]
    t = int(step.get("t", 1))
    kette_fortschreiben = bool(step.get("kette_fortschreiben", True))
    t_exp = step.get("t_exp")
    if t_exp is not None:
        t_exp = int(t_exp)

    if "J" in step:
        J = _resolve_j(step["J"], ctx)
    elif praedikat == "vouch":
        subj = _resolve_subject(step["subject"], ctx)
        J = (1, subj)
    else:
        raise ValueError(f"claim step needs J: {step!r}")

    v: bytes | None = None
    if praedikat == "vote":
        choice = int(step.get("choice", step.get("v", {}).get("0", 0)))
        v = cbor_canon.encode({0: choice})
    elif praedikat == "vouch":
        n = int(step["n"])
        v = cbor_canon.encode({0: n})
    elif praedikat == "ratify":
        witnesses = [claim_id(ctx.labels[w]) for w in step["witnesses"]]
        v = cbor_canon.encode({0: witnesses})

    p = _nuc(scope, {"accept-rules": "accept-rules", "vote": "vote", "propose": "propose",
                     "ratify": "ratify", "vouch": "vouch"}[praedikat])

    if kette_fortschreiben:
        claim = autor.claim_signieren(p=p, J=J, t=t, v=v, N=scope, t_exp=t_exp)
    else:
        claim = autor.claim_gabeln(p=p, J=J, t=t, v=v, N=scope, t_exp=t_exp)
    if label := step.get("label"):
        ctx.labels[label] = claim


def _schritt_zustellen(step: dict[str, Any], ctx: Kontext) -> None:
    assert ctx.welt is not None
    von = step["von"]
    an = step["an"]
    nur: list[bytes] | None = None
    if labels := step.get("nur"):
        nur = [claim_id(ctx.labels[label]) for label in labels]
    if an == "alle":
        ctx.welt.zustellen(von, "alle", nur=nur)
    elif isinstance(an, list):
        ctx.welt.zustellen(von, an, nur=nur)
    else:
        ctx.welt.zustellen(von, an, nur=nur)


def _schritt_uhr(step: dict[str, Any], ctx: Kontext) -> None:
    assert ctx.welt is not None
    ctx.welt.teilnehmer[step["teilnehmer"]].write_now(int(step["now"]))


def _membership_row(
    ctx: Kontext,
    subject: str,
    constitution: str,
) -> dict[str, str]:
    assert ctx.welt is not None and ctx.ex is not None
    subj = _resolve_subject(subject, ctx)
    ch = _constitution_hash(constitution, ctx)
    obj = _constitution_obj(constitution, ctx)
    row: dict[str, str] = {}
    for name, tp in ctx.welt.teilnehmer.items():
        result = membership(
            tp.store_laden(),
            subject=subj,
            scope=ctx.ex.N_gov,
            constitution_hash=ch,
            now=tp.read_now(),
            authorized_keys=frozenset(),
            constitution_obj=obj,
            policy=_policy(ctx.ex, ctx.ex.N_gov),
        )
        row[name] = result.state.value
    return row


def _tally_row(ctx: Kontext, target: str) -> dict[str, dict[str, Any]]:
    assert ctx.welt is not None and ctx.ex is not None
    if target == "aufnahme":
        epoch = ctx.ex.epoch_1
        proposal = ctx.ex.proposal
        constitution = ctx.ex.constitution_gov
        target_obj = ctx.ex.constitution_2
    else:
        raise ValueError(f"unknown tally target: {target!r}")
    row: dict[str, dict[str, Any]] = {}
    for name, tp in ctx.welt.teilnehmer.items():
        store = tp.store_laden()
        result = decide(
            store,
            epoch=epoch,
            proposal=proposal,
            genesis_obj=ctx.ex.genesis_gov,
            constitution_obj=constitution,
            target_constitution_obj=target_obj,
            known_proposals={proposal.proposal_hash: proposal},
            now=tp.read_now(),
            policy=_policy(ctx.ex, ctx.ex.N_gov),
        )
        row[name] = {
            "state": result.state.value,
            "yes": len(result.yes),
            "no": len(result.no),
        }
    return row


def _trust_row(
    ctx: Kontext,
    subject: str,
    anchors: list[str],
) -> dict[str, dict[str, Any]]:
    assert ctx.welt is not None and ctx.ex is not None
    subj = _resolve_subject(subject, ctx)
    anchor_set = frozenset(_resolve_subject(a, ctx) for a in anchors)
    params = TrustParams(C0=100, gamma_num=1, gamma_den=2, D=100)
    row: dict[str, dict[str, Any]] = {}
    for name, tp in ctx.welt.teilnehmer.items():
        deriv = derive(
            tp.store_laden(),
            anchors=anchor_set,
            scope=ctx.ex.N_res,
            now=tp.read_now(),
            params=params,
        )
        d = deriv.bfs.distance.get(subj)
        c = deriv.bfs.node_capacity.get(subj)
        over_names = sorted(
            name
            for name, tp in ctx.welt.teilnehmer.items()
            if tp.pub
            in {
                f.subject
                for f in deriv.findings
                if f.kind is TrustFinding.OVERCOMMITTED_AUTHOR
            }
        )
        row[name] = {
            "d": d,
            "C": c,
            "edges": len(deriv.bfs.edges),
            "overcommitted": over_names,
        }
    return row


def _classify_row(ctx: Kontext, label: str) -> dict[str, str]:
    assert ctx.welt is not None
    claim = ctx.labels[label]
    row: dict[str, str] = {}
    for name, tp in ctx.welt.teilnehmer.items():
        result = classify(claim, tp.store_laden(), now=tp.read_now())
        row[name] = result.state.value
    return row


def _ratify_row(ctx: Kontext, label: str) -> dict[str, str | None]:
    assert ctx.welt is not None and ctx.ex is not None
    ratify = ctx.labels[label]
    row: dict[str, str | None] = {}
    for name, tp in ctx.welt.teilnehmer.items():
        store = tp.store_laden()
        tally = decide(
            store,
            epoch=ctx.ex.epoch_1,
            proposal=ctx.ex.proposal,
            genesis_obj=ctx.ex.genesis_gov,
            constitution_obj=ctx.ex.constitution_gov,
            target_constitution_obj=ctx.ex.constitution_2,
            known_proposals={ctx.ex.proposal.proposal_hash: ctx.ex.proposal},
            now=tp.read_now(),
            policy=_policy(ctx.ex, ctx.ex.N_gov),
        )
        try:
            result = verify_ratification(
                store,
                ratify=ratify,
                epoch=ctx.ex.epoch_1,
                proposal=ctx.ex.proposal,
                tally=tally,
                target_constitution_obj=ctx.ex.constitution_2,
                now=tp.read_now(),
                policy=_policy(ctx.ex, ctx.ex.N_gov),
            )
        except ValueError:
            row[name] = "ValueError"
            continue
        if result.next_epoch is None:
            kinds = {f.kind.value for f in result.findings}
            row[name] = kinds.pop() if len(kinds) == 1 else str(sorted(kinds))
        else:
            row[name] = result.next_epoch.epoch_id.hex()[:16]
    return row


def _check_erwarte(got: Any, expected: Any, path: str) -> None:
    if isinstance(expected, dict):
        if not isinstance(got, dict):
            raise AssertionError(f"{path}: expected dict, got {got!r}")
        for key, exp in expected.items():
            if key not in got:
                raise AssertionError(f"{path}.{key}: missing in {got!r}")
            _check_erwarte(got[key], exp, f"{path}.{key}")
        return
    if isinstance(expected, list):
        if list(got) != list(expected):
            raise AssertionError(f"{path}: expected {expected!r}, got {got!r}")
        return
    if got != expected:
        raise AssertionError(f"{path}: expected {expected!r}, got {got!r}")


def _schritt_zeige(step: dict[str, Any], ctx: Kontext) -> str | None:
    was = step["was"]
    got: Any
    if was == "membership":
        got = _membership_row(ctx, step["subject"], step["constitution"])
    elif was == "tally":
        got = _tally_row(ctx, step["target"])
    elif was == "trust":
        got = _trust_row(ctx, step["subject"], step.get("anchors", ["anna", "bruno"]))
    elif was == "classify":
        got = _classify_row(ctx, step["claim"])
    elif was == "ratify":
        got = _ratify_row(ctx, step["claim"])
    else:
        raise ValueError(f"unknown zeige was: {was!r}")

    if erwarte := step.get("erwarte"):
        _check_erwarte(got, erwarte, was)

    if step.get("ausgabe", True):
        if was == "membership":
            cols = ["", *got.keys()]
            rows = [(step["subject"], *(got[n] for n in got))]
            return tabelle(f"membership/{step['constitution']}", cols, rows)
        if was == "tally":
            cols = ["", *got.keys()]
            rows = [
                ("state", *(got[n]["state"] for n in got)),
                ("yes", *(str(got[n]["yes"]) for n in got)),
                ("no", *(str(got[n]["no"]) for n in got)),
            ]
            return tabelle(f"tally/{step['target']}", cols, rows)
    return None


def _schritt_erwarte(step: dict[str, Any], ctx: Kontext) -> None:
    fake = {"was": step["was"], **{k: v for k, v in step.items() if k != "art"}}
    fake["ausgabe"] = False
    _schritt_zeige(fake, ctx)


def run_scenario(path: str | Path) -> None:
    """Führt eine JSON-Szenariodatei aus; bricht bei erwarte-Abweichung ab."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    ctx = Kontext()
    for step in data["schritte"]:
        art = step["art"]
        if art == "welt":
            _schritt_welt(step, ctx)
        elif art == "genesis":
            _schritt_genesis(step, ctx)
        elif art == "claim":
            _schritt_claim(step, ctx)
        elif art == "zustellen":
            _schritt_zustellen(step, ctx)
        elif art == "uhr":
            _schritt_uhr(step, ctx)
        elif art == "zeige":
            _schritt_zeige(step, ctx)
        elif art == "erwarte":
            _schritt_erwarte(step, ctx)
        else:
            raise ValueError(f"unknown step art: {art!r}")
