# YEP proposals (ADR/RFC-like)

This folder tracks **YEPs**: *YEP Enhancement Proposals*.

A YEP is an architectural decision record / RFC-like document used to propose, discuss, and record concrete changes to yep (engine, CLI, targets, language support, etc.).

The goals:

- Make decisions explicit and reviewable.
- Capture tradeoffs and rejected alternatives.
- Track implementation status and follow-ups.

## Folder layout (lifecycle)

Proposals live in one of these folders:

- `doc/proposals/draft/` — under discussion / not yet accepted.
- `doc/proposals/approved/` — accepted; implementation may be pending or in progress.
- `doc/proposals/rejected/` — not accepted (keep for history).

A proposal moves by **moving its whole folder** to the next lifecycle directory.

## Naming convention

Each proposal is a folder named like:

```
YEP-<AREA>-<NNNN>-<slug>/
```

Where:

- `YEP` literally means **YEP Enhancement Proposal**.
- `<AREA>` is the category (see below).
- `<NNNN>` is a zero-padded integer (e.g. `0001`). It is unique within the repo.
- `<slug>` is a short lowercase-kebab "comment" describing the proposal.
  - Examples: `python-vars`, `java-reflector`, `azure-devops`, `local-target-cache`.

Inside the folder, use one or more markdown files:

- `README.md` — required; the canonical proposal text.
- Optional extra docs (when helpful):
  - `notes.md` (meeting notes)
  - `examples.md`
  - `migration.md`
  - `appendix.md`

### AREA values

Use one of:

- `CORE` — pipeline model, reflection, wrapper generation, engine architecture.
- `SEC` — security/compliance, sandboxing, secret handling.
- `CLI` — command UX, flags, outputs.
- `ETC` — anything else that doesn’t fit the above.
- `TRG-<target>` — a specific target backend (examples: `TRG-local`, `TRG-argo`, `TRG-azure-devops`).
- `LNG-<lang>` — language support / reflectors / runtime libs (examples: `LNG-py`, `LNG-java`).

Notes:

- Prefer **specific** areas for target/language work (`TRG-*`, `LNG-*`) so proposals are easy to find.
- Keep `<target>` / `<lang>` in lowercase-kebab.

### Examples

- `doc/proposals/draft/YEP-CORE-0001-wrapper-vars-schema/README.md`
- `doc/proposals/draft/YEP-CLI-0002-vars-flag-format/README.md`
- `doc/proposals/draft/YEP-TRG-azure-devops-0003-generate-workflow/README.md`
- `doc/proposals/draft/YEP-LNG-py-0004-reflector-metadata/README.md`

## Status and progression

Each proposal must include a **Status** section:

- `Draft` → `Approved` or `Rejected`

If approved, the proposal should also track:

- Implementation issue(s) / PR(s)
- Rollout / migration notes

## Writing guidelines

Keep YEPs short, concrete, and testable:

- Specify the problem and constraints.
- Propose the smallest change that solves the problem.
- Enumerate alternatives and why they’re not chosen.
- Define success criteria and non-goals.

## Template

Use the sample format in `doc/proposals/fmt-sample.md`.
