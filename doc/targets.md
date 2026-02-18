# yep targets

This document is intentionally speculative. It outlines the kinds of “targets” yep could support and how targets change the workflow from local prototyping to production-grade execution.

Roadmap note: the categories and examples below are **directional**, not commitments. The goal is to communicate design intent and integration surface area, not to promise timelines.

## What is a target?
A **target** is an execution backend that can take a reflected pipeline model (steps + topology + variables) and:

- generate runnable artifacts (wrappers, manifests, DAGs, job specs)
- run the pipeline on a platform (locally, on a cluster, or via a control plane)
- optionally provide platform-specific semantics (caching, retries, scheduling, scaling, observability)

The pipeline declaration stays in a general-purpose language; targets decide how that declaration is materialized.

## Why targets matter
With only a `local` target, a pipeline engine looks like “a structured script runner”.

With multiple targets, the paradigm shifts:

- **Prototype locally** using the same declaration you’ll later operationalize.
- **Promote to a platform** by switching targets rather than rewriting the pipeline definition in a separate system.
- **Let the platform do the heavy lifting** (distributed compute, scheduling, retries, secrets, scaling), while the declaration remains focused on topology and step contracts.

## Target families (candidate taxonomy)

### 1) Developer / local targets
Good for tight iteration loops.

- **local** (already implemented): runs step functions in-process.
- **venv/poetry-managed local**: ensures dependencies/env are reproducible.
- **docker local**: runs pipeline in a container for parity with CI/prod.

### 2) Batch / job-runner targets
Good for non-interactive runs with retries and logs.

- **Kubernetes Job / CronJob**: each pipeline run becomes a Job; scheduled runs become CronJobs.
- **Nomad job**: similar semantics for HashiCorp Nomad.
- **Slurm / PBS / HTCondor**: HPC-style submission for compute-heavy workloads.
- **Serverless batch**: map steps or runs to AWS Batch / Google Cloud Batch.

### 3) Data engineering / distributed compute targets
Good for large datasets and distributed execution.

- **Spark / Databricks**: pipeline maps to one or more Spark jobs; steps may become stages, notebooks, or job tasks.
- **Jupyter / IPython notebooks**: generate parameterized notebooks for exploratory data work and reproducible runs.
- **Dask / Ray**: step functions become distributed tasks/actors.
- **Flink / Beam**: (longer-term) for streaming or unified batch+streaming.

Design pressure these targets introduce:

- step boundaries become serialization/materialization boundaries (datasets, tables, object storage)
- topology and lineage become first-class (DAGs, metadata)
- execution semantics depend on platform (lazy vs eager, checkpointing)

### 4) Workflow orchestrator targets
Good for scheduling, dependency management, and operations.

- **Airflow**: generate a DAG that calls into step containers/jobs.
- **Dagster / Prefect / Temporal**: model steps as ops/activities with retries, resources, and observability.
- **Argo Workflows**: generate workflow YAML, each step as a container.

These targets tend to separate:

- *control plane*: orchestrator schedules and monitors
- *data plane*: workers execute steps

### 5) DevOps / automation targets
Good when “pipeline steps” are idempotent automation tasks.

- **SSH / remote-exec**: run steps against fleets of machines.
- **Ansible**: generate playbooks/roles or call modules.
- **Terraform / Pulumi**: pipeline drives infra changes, with explicit plan/apply stages.
- **GitHub Actions / GitLab CI**: generate CI workflows from the pipeline topology.

Typical semantics here:

- approvals and environment promotion (dev → staging → prod)
- idempotency and drift detection
- secrets and policy enforcement

### 6) Service / microservice fleet targets (Kubernetes-centric)
Good when the “pipeline” is a deployable topology of services.

- **Kubernetes Deployments/Services/Ingress**: steps define services; edges define dependencies, routing, or initialization order.
- **Helm / Kustomize**: generate/compose deployment artifacts.
- **Service mesh integration**: optional layer for traffic policy and observability.

Here the target is less about “run once” and more about “materialize and manage a living system”:

- deploy on demand
- scale components independently
- rollouts/rollbacks
- health checks and SLO monitoring hooks

### 7) Agentic workflow targets
Good when the pipeline includes **LLM-driven decisions**, tool use, and human-in-the-loop steps.

These targets are less about pure dataflow and more about orchestrating:

- prompts and model calls
- tool invocations (APIs, RPA, browsers)
- memory/state
- approvals and handoffs
- event triggers and long-running conversations

Candidate platforms/tools:

- n8n
- Zapier
- Make (Integromat)
- Pipedream
- Node-RED
- Flowise
- Dify
- LangChain (runnables)
- LangGraph
- LlamaIndex (agents/workflows)
- Semantic Kernel
- Microsoft Copilot Studio (where applicable)

Target design pressure here:

- step contracts may include unstructured I/O (text, JSON, tool results)
- execution often needs durable state and resumability
- reproducibility and audit logs become first-class concerns

### 8) Experimental (UI prototyping / visual flows)
Good when you want a **clickable flow UI** for demos, basic automation, or rapid UX iteration.

This category assumes the UI can implement/accept a **predefined topology** (often a linear chain in the simplest case) and provide an execution experience such as:

- tap/click to run step-by-step
- show intermediate results
- edit parameters interactively
- export/share a run configuration

How it can map to execution:

- **Client-side execution**: run steps locally inside the app (useful for mobile/offline or lightweight automation).
- **Client + server**: UI renders the flow, but execution happens on a backend; the target generates a thin server-side runner and an API contract.
- **UI as a facade**: UI is only a visualizer/controller for another target (e.g., a Kubernetes Job or a CI workflow).

Candidate engines/wrapper ideas:

- Flutter UI that renders a linear pipeline and runs local steps (or calls a backend runner)
- Web UI built on node/edge graph libraries (e.g., React Flow-style editor) for visualizing and triggering runs
- Blockly-style “blocks” UI for beginner-friendly automation
- Static HTML report + controls for step replay (run IDs, params, outputs)

Subcategory: **Logical apps (connected component blocks)**

This is a “Zapier/n8n/KNIME-like” direction focused on turning a pipeline into a **descriptive set of connected blocks** that users can browse, configure, and connect.

Key ideas:

- A palette of reusable blocks (inputs, transforms, actions, sinks).
- Some blocks are generated or exported from yep declarations (e.g., a well-tested function/module becomes a draggable “step block”).
- Blocks can expose their metadata (params, defaults, retries/timeouts, resource class) and validate wiring based on declared contracts.
- The resulting connected flow can be executed locally (for prototyping) or deployed behind an API/worker runner (for shared/team usage).

This overlaps with the “Agentic workflow targets” category, but the emphasis here is **UI-first composition** and reusable building blocks, not necessarily LLM/agent orchestration.

These targets are intentionally labeled experimental because they tend to push yep toward product/UX concerns (state, persistence, auth) that may be out of scope for the minimal engine, but they can be very powerful for adoption and prototyping.

## Cross-cutting target capabilities (future)
Regardless of family, mature targets often converge on similar features:

- **Packaging**: how code and dependencies are shipped (wheel, container image, artifact store)
- **Secrets/config**: how vars map to env vars, secret stores, config maps
- **Observability**: logs, metrics, traces; stable run IDs and step IDs
- **Caching/materialization**: when step outputs are persisted and reused
- **Retries/timeouts**: platform-native vs engine-managed
- **Concurrency/scaling**: per-step parallelism, fan-out/fan-in

## Target implementation methods (metadata layers)
As targets get more capable, they need more information than “here is a list of steps”. Examples: dependencies, parallelization strategy, resources (CPU/memory/GPU), timeouts, retries, caching/materialization, and error-handling policies.

The guiding idea is to **add a metadata layer without abandoning GP languages**. Below are several ways to do it; different languages and targets will naturally prefer different mechanisms.

### 1) Structured comments / docstrings
Embed machine-readable metadata in comments or docstrings and let reflectors parse it.

- Python: docstring blocks (YAML/JSON/TOML snippets) or tagged lines, e.g. `yep: retries=3 timeout=30s`.
- Go/Rust: line/block comments using tags.

Pros: lowest friction, no runtime dependency.
Cons: parsing conventions must be defined; limited validation.

### 2) Decorators (Python) / Annotations (Java) / Attributes (Rust)
Attach metadata directly to step functions/classes via language-native mechanisms.

- Python: `@yep.step(retries=3, timeout="30s", resources={...})`
- Java: `@Step(retries = 3, timeout = "PT30S")`
- Rust: `#[yep(step, retries = 3, timeout = "30s")]`

Pros: explicit, type-checkable in some languages, reflector-friendly.
Cons: requires a small yep runtime library per language.

### 3) Typed step wrappers (Step objects)
Instead of treating steps as bare functions, wrap them in a small typed object that carries metadata.

Examples:

- Python: `Step(fn=read_file, name="read_file", resources=..., retries=...)`
- Java: builder pattern: `Step.of("readFile", this::readFile).withRetries(3)`

Pros: strong structure, easy validation, supports richer topology.
Cons: declaration becomes slightly more “framework-y”.

### 4) Sidecar metadata files (per step or per pipeline)
Keep the pipeline declared in code, but allow optional sidecar files that provide target-specific overlays.

- `word_count.py` plus `word_count.yep.toml`
- or `steps/read_file.yep.json` alongside the module

Pros: clean separation; different targets can have different overlays.
Cons: reintroduces an extra file; needs merge rules.

### 5) Naming and signature conventions
Encode intent in stable conventions that reflectors/targets can interpret.

Examples:

- `read_*` steps are I/O-bound; `train_*` steps need GPU.
- return types / parameter types imply data contracts and materialization.
- reserved parameter names like `ctx`, `spark`, `session`, `logger`.

Pros: minimal ceremony.
Cons: implicit and easy to drift; hard to enforce.

### 6) Explicit dependency / topology API
Add a small API to declare edges and advanced topology when inference is insufficient.

Examples:

- `a >> b >> c` style chaining operators
- `fanout(step, items).map(worker).gather(reducer)`
- `depends_on(step_b, step_a)`

Pros: unlocks non-linear graphs while keeping step logic in code.
Cons: requires design of a compact “topology vocabulary”.

### 7) Target overlays (policy objects)
Let targets apply defaults/policies without annotating every step.

- a “profile”: dev vs prod
- per-target policy: retry rules, default timeouts, resource classes
- environment-level policies: secrets mapping, image registry, scheduling queues

Pros: keeps declarations clean; operational teams can own policies.
Cons: must be predictable and explainable (avoid “magic”).

In practice, yep will likely support a mix: light inference for the happy path, plus one or two explicit metadata mechanisms that scale to production.

## Practical note for the current repo
Today, yep registers a single target: Python `local`. The folder structure and factories already suggest the extension mechanism:

- add a new target class under `src/yep/targets/<lang>/...`
- register it in the targets factory
- teach it to generate wrappers/artifacts and to execute them

As new targets are added, the same pipeline declaration should remain usable, but the wrapper/artifact generation will become increasingly platform-specific.

# Integration (future)
This is a **planned** area: integrate yep with existing workflow/pipeline engines and CI/CD platforms.

This category has strong functional overlap with “native targets” (both execute DAGs), so the intent is to treat these as **special adapter targets**:

- yep remains the place where pipeline topology and step contracts are expressed (in general-purpose code)
- the integration target translates that into the external engine’s concepts (DAG, job, workflow, pipeline, stages)
- execution, scheduling, UI, and operations can then be delegated to the external system

## Candidate integration roadmap (non-committal)
Below is a deliberately broad list (30+) of possible integrations to consider over time:

### Existing pipeline / workflow engines
- KNIME
- Apache NiFi
- Apache Airflow
- Argo Workflows
- Tekton Pipelines
- Prefect
- Dagster
- Luigi
- Flyte
- Temporal
- Netflix Metaflow
- Kubeflow Pipelines
- AWS Step Functions
- Google Cloud Workflows
- Azure Data Factory
- Apache Oozie
- Azkaban

### Data/ML platform orchestration
- Databricks Workflows (Jobs)
- AWS Glue Workflows
- Google Cloud Dataflow (Apache Beam runner)
- Apache Beam (portable pipeline)
- Apache Flink (job graph)
- Apache Spark (job/stage abstraction)
- MLflow Projects
- Amazon SageMaker Pipelines
- Vertex AI Pipelines

### DevOps / CI/CD and automation platforms
- Azure DevOps Pipelines
- GitHub Actions
- GitLab CI/CD
- Jenkins
- CircleCI
- Travis CI
- Bitbucket Pipelines
- TeamCity
- Bamboo
- Buildkite
- Drone CI
- GoCD
- Concourse CI
- Spinnaker
- Argo CD
- Flux CD
- Harness
- Octopus Deploy
- Rundeck

Notes:

- Some items above overlap in scope (engine vs managed offering vs underlying runtime). That’s fine at this stage; this list is meant to capture the landscape.
- Integrations can range from “generate spec files” (DAG/YAML) to “call an API to register and trigger runs”.

## Roadmap framing
As yep grows, expect the target landscape to evolve in stages:

- Start with a small number of “native” targets that exercise the core abstractions.
- Add adapters for widely-used platforms where it’s valuable to reuse their schedulers, UIs, and operational maturity.
- Refine the pipeline model to support richer topologies and platform-specific semantics without losing the “declaration in GP code” principle.

