# YEP Format Sample (copy/paste)

This file is a **sample YEP** you can copy into a new proposal folder.

Suggested workflow:

1. Create a folder under `doc/proposals/draft/` named like `YEP-CORE-0001-some-slug/`.
2. Copy this file into that folder as `README.md`.
3. Edit the content, open a PR, discuss.
4. When accepted, move the proposal folder to `approved/`.

---

# YEP-CORE-0001-sample-slug

## Metadata

- **Title:** Sample proposal title
- **Area:** CORE | SEC | CLI | ETC | TRG-<target> | LNG-<lang>
- **Status:** Draft | Approved | Rejected
- **Authors:** <name(s)>
- **Created:** YYYY-MM-DD
- **Last updated:** YYYY-MM-DD
- **Tracking:** <issue link(s)> / <PR link(s)>

## Summary

1–3 sentences describing the change and why it matters.

## Motivation / Problem

What problem are we solving?

- Who is impacted (users, contributors, targets)?
- What is broken or missing today?
- What constraints matter (backwards compatibility, DX, simplicity, security)?

## Goals

- Goal 1
- Goal 2

## Non-goals

- Non-goal 1
- Non-goal 2

## Background (current behavior)

Describe today’s behavior with concrete examples.

Example:

- Reflector extracts vars: only top-level string assignments.
- Local wrapper uses next function’s arg names to bind previous outputs.

## Proposal

Describe the proposed change precisely.

### User-facing behavior

- CLI changes (commands/flags/output)
- Config changes (`.yep/project.toml`)
- Generated wrapper changes (if relevant)

### Technical design

- New/changed data model(s)
- New/changed interfaces (reflectors/targets)
- Migration strategy (if needed)

### Example

Provide at least one example showing the desired experience.

## Alternatives considered

List at least 1–3 alternatives and why they were not chosen.

- Alternative A — pros/cons
- Alternative B — pros/cons

## Tradeoffs / Risks

- Risk 1 (and mitigation)
- Risk 2 (and mitigation)

## Compatibility

- Backwards compatibility: yes/no (explain)
- Breaking changes: yes/no (explain)
- Versioning notes (if relevant)

## Security considerations

- Any new attack surface?
- Secret handling changes?
- Execution/sandbox implications?

## Observability / Operability

- Logging changes?
- Debuggability?
- How will failures be diagnosed?

## Implementation plan

Concrete, checkable steps.

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Testing plan

- Unit tests to add/change
- Example projects to validate
- Manual verification steps (if needed)

## Decision

When the proposal is decided, record:

- **Decision:** Approved | Rejected
- **Decision date:** YYYY-MM-DD
- **Decision makers:** <names/team>
- **Rationale:** 2–6 bullets summarizing why

## Appendix

Optional details, references, links, and extended examples.
