# Applications & positioning (note)

This document captures a product/technical framing for **yep**: what it is today, what it could become, and the key decisions that drive the roadmap.

It is intentionally written as a **project note** (not marketing copy, not an RFC).

## Summary

**yep** is a pipeline engine that infers a runnable pipeline from ordinary source code rather than requiring a separate YAML/DSL definition.

The core thesis is:

> **Pipeline topology should be derived from general-purpose code**, and targets should decide how that topology is materialized and executed.

This is a strong developer-experience idea, but the project’s success depends heavily on choosing a focused “wedge” use case.

## What yep is (today)

At a high level:

```
source code (Python)
      │
      ▼
reflector (AST)
      │
      ▼
pipeline model (tasks + vars)
      │
      ▼
target backend
      │
      ▼
generated wrapper / artifact
      │
      ▼
execution
```

Current implementation scope:

- Python reflector (AST)
- Python local target (wrapper + execution)
- Linear chain inference (source-order functions)

## What’s interesting about the idea

The compelling part is not “yet another runner” — it’s the **code-to-topology** approach.

Many systems split the world into:

```
logic in code
structure in YAML
```

That duplication creates drift. yep’s bet is that topology inference (plus small annotations where needed) can keep pipelines **code-first** without losing structure.

## Strengths

- **Avoids a separate DSL**: the declaration file is just code.
- **Reflection-based discovery**: the engine infers steps/vars from the source.
- **Targets are a strong seam**: the same declared topology can be run locally or compiled into platform-specific artifacts later.

## Risks / constraints

### 1) Crowded ecosystem

Workflow/pipeline engines are a saturated category (Airflow, Prefect, Dagster, Argo, Temporal, etc.). Competing head-on as “a new workflow engine” is hard.

### 2) Linear inference hits a ceiling

Linear chaining is a great on-ramp, but real workflows often need:

- branching / joins
- retries / timeouts
- caching / artifacts
- scheduling
- parallelism
- observability

Without a path to those capabilities, yep risks being perceived as a “structured script runner”.

### 3) Positioning is currently too broad

If yep is described as a generic “pipeline engine”, it’s unclear who it’s for and why it wins.

## Strategic directions (choose one wedge)

### Direction A: code-to-workflow compiler (most aligned)

Position yep as a compiler layer:

```
Python declaration → Airflow DAG / Argo Workflow / Prefect Flow / etc.
```

This turns the target abstraction into the main product surface: the value is “write once, materialize anywhere”.

### Direction B: infrastructure/runbook automation

Treat pipelines as idempotent operational runbooks:

```
provision → deploy → migrate → validate
```

This is often less crowded than data orchestration and can emphasize audits, approvals, and environment promotion.

### Direction C: agent/tool workflows

Use the pipeline model for LLM + tool orchestration.

This is promising but currently noisy/fast-moving; it can be a good target family later, but is risky as the first wedge.

## Near-term product milestones (implementation-oriented)

These milestones are useful regardless of wedge, but the priority/order may change.

1) **Richer topology model**
   - branching and joins
   - explicit dependencies (light annot//ations)

2) **Graph visibility**
   - a command that outputs a wiring report / DOT / Mermaid
   - make the “magic” inspectable

3) **One real external target**
   - generate an artifact for a real engine (e.g., Airflow/Argo)
   - “compiler” framing becomes tangible

## Open question (the one that decides everything)

What motivated the project originally?

Was the primary pain:

1. YAML pipeline definitions are painful / drift from code
2. Existing workflow engines are too heavy for everyday workflows
3. Developers want pipelines to look like normal code (inference/annotations)
4. Something else (specific use case)

The answer determines whether yep should be:

- a focused OSS devtool
- a compiler layer to existing engines
- a runbook/automation product
