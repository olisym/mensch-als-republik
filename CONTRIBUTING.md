# Contributing

## Welcome

Thanks for reading this. Mensch als Republik is still small and its process is a little
unusual, but if you've made it this far, you're already the kind of person the project hopes
to find — most people who show up to a project like this do so in good faith, and that's the
assumption this document starts from.

## What kind of project this is

This is currently one person's work, checked against a written specification rather than built
ad hoc. That process is described in `docs/METHOD.md` — worth a look before you invest much
time, mostly so a review built for catching drift over years doesn't feel like an odd wall to
hit on your first pull request.

This is also the maintainer's first public open-source project. If something about how this
works feels unclear, or you don't know where to start, say so — figuring that out together is
part of the point, not an inconvenience. Response times may be slow while that's being worked
out; that's not a reflection of how welcome you are.

There's no backlog of "good first issues" yet, and a pull request that adds a feature will
probably need a conversation first, not because it's unwelcome, but because every change here
goes through that same review process.

## The fastest way to help right now

The most valuable contribution isn't code — it's finding a defect in the specification itself.
`01-claim-atom.md` and its neighbors are dense, and an outside reader who spots a
contradiction, an unhandled case, or an ambiguous rule is doing exactly the kind of thing this
project is built to reward. Open an issue. You don't need to have a fix, and you don't need to
know the codebase.

An independent implementation is even more valuable, and it doesn't need to be complete. The
project's own Go implementation (`go/`) was built specifically as a check on the specification
text, without looking at the Python code — and it found real spec defects in one pass just by
being read closely by someone implementing it fresh. If you try to implement any layer from
the spec alone and get stuck, that's a finding, not a failure on your part. Say so in an issue.

## If you want to submit code

Small, well-scoped fixes to the Python reference implementation are welcome, especially ones
that come with a failing test first. Larger changes should start as an issue or a discussion,
not a pull request — the review here includes deriving expected values from source data rather
than typing them, and in some cases a rollback probe showing that a regression test actually
regresses. That's a heavier bar than most projects ask for, and it's worth agreeing on scope
before you write code against it.

## If you think you might be one of the people this is waiting for

The register (D237) is explicit that a real application of this protocol needs real people
with a genuine shared concern — not volunteers doing a favor, not a simulation. If that's you,
open an issue and say so directly. That's not a smaller contribution than code; it's the one
the project is actually waiting for.

## License

Code contributions are accepted under **Apache-2.0**. Contributions to the specification,
documentation, or decision register are accepted under **CC-BY-4.0**. By opening a pull
request you're agreeing your contribution is offered under the license that already covers the
file you're changing.

Thank you for reading this far. Most people who do are exactly the kind of people worth
building something with.
