# Mensch als Republik (MaR)

**Can mutual assurance and collective decision-making work without a central authority —
no court, no platform, no admin key?**

Mensch als Republik (MaR — a working title; renaming is planned but hasn't happened yet, see
the decision register) is a protocol under active development that tries to answer that
question by building the thing and measuring what breaks, instead of arguing about it in the
abstract.

This repository is the English entry point. The project's actual working language is German —
the specifications, the decision register, and the day-to-day process are written in German
and will stay that way. This file, along with `CONTRIBUTING.md` and `docs/METHOD.md`, is
written directly for an English-reading audience, not translated from anything.

## The question, more precisely

Most systems that coordinate people rely on either a trusted center — a court, a platform
operator, a custodian holding funds — or a single dominant chain of consensus. MaR asks
whether claims, obligations, and governance can instead be built to be checkable because they
can **contradict each other**, not because an authority signed off on them. A claim nobody can
ever be proven wrong about isn't more trustworthy for it — it's just unfalsifiable.

The project is also deliberately built to survive its own author. One explicit goal is to
resist forgotten decisions, silent drift, and normativity that creeps in unexamined over a
multi-year timeline. The mechanism for that isn't discipline — it's a decision register that
turns every normative choice, and the reasoning behind it, into a permanent, citable, checkable
record.

## What exists today

- A layered specification (Layers 00–08): genesis and constitution, a claim/atom layer with a
  formally verified rejection-code system, trust-flow and governance layers, a scope and
  purpose layer that defines its own admission criteria.
- A Python reference implementation, with **797 automated tests** and a decision register of
  **more than 320 entries**, each with a named justification.
- Layer 01 (the claim/atom layer) has been through an exhaustive mutation-testing campaign:
  over **19,000 generated mutants**, single and paired, across three structural families. Not
  one surviving mutant turned up anything that reading, reasoning, or a rollback probe hadn't
  already found. That's treated as evidence the layer has been read out, not as proof of
  correctness — the distinction matters, and it's recorded as one.
- A second, independent implementation in Go, built against a frozen copy of the specification
  without access to the Python code, specifically as a check on whether the specification
  itself is complete and unambiguous. It has already found spec defects the first
  implementation's own test suite could not surface.
- An active scenario phase: rather than continuing to harden a single layer, the project is
  now running deliberately adversarial comparative scenarios (for example: a shared fund with
  a named custodian vs. a mutual-obligation model with none) to see where the protocol's
  guarantees actually hold and where they don't. Findings from this phase go straight into the
  register; the scenario code itself is throwaway.

## What does *not* exist yet

No real application. The register (D237) is explicit that a real test needs real people with a
genuine shared concern — not a simulation, not volunteers doing a favor. Waiting for that is
treated as a legitimate state; pretending otherwise is not. Making the project visible — this
repository included — is part of how those people might eventually turn up.

## Repository layout

- `00` – `08`, plus lettered sub-specifications: the layered specification, in German.
- `07-decisions.md`: the decision register. Large by design — it is the point of the project,
  not overhead to be trimmed. `tools/register_index.py` gives you structured lookup by entry
  number, so you don't have to read the whole thing at once.
- `pruefregeln.md`: the accumulated review rules the project holds itself to.
- `mensch_als_republik/`, `tests/`, `tools/`: the Python reference implementation, its test
  suite, and the tooling that enforces the review discipline (spec linting, mutation
  campaigns, register consistency checks).
- `go/`: the independent Go implementation. It's deliberately pinned to a frozen snapshot of
  the specification — the register explains why that pin, not the repository split, is what
  actually keeps the two implementations independent.

## License

Code is licensed under **Apache-2.0** (`LICENSE`). The specification, the decision register,
and other prose documents are licensed under **CC-BY-4.0** (`LICENSE-SPEC`). Both choices, and
the reasoning behind them, are recorded in the register.

## Getting involved

This is currently a one-person project, but it isn't built ad hoc — every change is checked
against the specification, not just against what compiles. See `docs/METHOD.md` for how that
actually works day to day.
If you're working on related problems — decentralized coordination, protocols hardened by
contradiction rather than authority, or you think you might be one of the people the register
(D237) is waiting for — open an issue, or see `CONTRIBUTING.md`.
