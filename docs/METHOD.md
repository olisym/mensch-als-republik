# Method

This describes how the project is actually built, day to day — not as a pitch, as a
description you can check against the decision register and the commit history.

## The core discipline

Nothing here counts as done because it compiles or passes its own tests. It counts as done
because it's been checked against the written specification, and because the decision behind
it — including the reasoning, not just the outcome — is recorded permanently in
`07-decisions.md`. The register is deliberately large. That's the point: a decision that lives
only in a commit message or a chat log is effectively lost within a year, on a project meant
to run for several.

## Golden numbers, not typed values

Expected values in tests and specs are derived from an independent source — a cryptographic
vector file, a signature, a table already in the specification — rather than typed in by hand.
A typed expected value looks identical to a derived one right up until the underlying rule
changes and nobody notices, because the test still passes against the stale number that was
typed alongside it.

## Rollback probes

Where a fix produces a regression test, the fix is reverted once, on purpose, specifically to
confirm the new test actually turns red. A regression test that can't be shown to fail when the
regression is reintroduced isn't verified to be testing anything at all.

## What mutation testing actually told us

Layer 01 went through an exhaustive mutation campaign: over 19,000 generated mutants, single
and paired, across three structural families of the rejection-code logic. It found zero new
defects. Every defect this project has ever found came from reading the specification closely,
reasoning about an edge case, or a rollback probe — never from a mutant surviving a test suite.
That's worth stating plainly instead of citing the mutant count as if it were the discovery
method: the campaign's actual result was confidence that the existing tests do their job, not a
bug-finding technique that paid off.

## A second implementation as a spec debugger

The Go implementation in `go/` was built against a frozen snapshot of the specification,
deliberately without reference to the Python code. The goal wasn't a second production
implementation — it was to find out whether the specification itself was complete and
unambiguous enough for someone to build from cold. It found real defects in the specification
text in a single pass that the Python test suite, however thorough, could not have surfaced,
because a test suite can't tell you a rule was underspecified if the only implementation
reading it made the same silent assumption the spec's author did.

## Acceptance means reading the diff

A tool's own report of what it did — even an accurate one — is never the basis for accepting a
change. The actual diff gets read, and the delivered code gets reconstructed and re-run
independently before anything is accepted. This project's history includes several cases where
an accurate report from an implementing tool still described code that, on inspection, had a
defect the report hadn't mentioned because the tool hadn't been asked to check for it.

## Division of labor

One person makes every substantive decision, executes every shell command, and is the only
human in the process. A large language model (Claude, from Anthropic) acts as a
specification supervisor: it reviews proposed changes against the written spec, derives golden
numbers independently, writes the register entries and the tightly-scoped prompts that
implementation work is done against, and conducts the acceptance review described above. It
writes no code that ends up in the repository. A separate coding tool does the actual
implementation work, strictly against those prompts.

The reason for the split isn't ceremony. Keeping "what should be built and why" separate from
"build it" is what makes the acceptance step meaningful — the same party that decided the spec
also checks the result against it, and neither role is the one holding the keyboard while the
code gets written.

## Where this comes from

Every claim above is checkable: `07-decisions.md` for the reasoning behind normative choices,
`pruefregeln.md` for the accumulated review rules, and the commit history for whether the
practice actually holds up over time rather than just being described well once.
