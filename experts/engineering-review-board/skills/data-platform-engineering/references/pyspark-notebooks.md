# PySpark Notebook Evidence Baseline

Load this reference for PySpark SQL, DataFrame, execution-plan, tuning, or
Structured Streaming work whose target repository may use notebooks. It records
the public Apache Spark baseline only; it does not establish a target
repository's runtime, managed-notebook behavior, cluster topology, data access,
or performance.

## Evidence Record

| Field | Persisted evidence |
| --- | --- |
| Retrieval date and time | 2026-07-31, 23:13–23:14 UTC. |
| Source authority | Primary documentation and release notes published by the Apache Spark Project at `spark.apache.org`. No vendor documentation, blog, benchmark, or search-result summary is authority for the claims below. |
| Current-version disposition | At retrieval, the official [`latest` PySpark overview](https://spark.apache.org/docs/latest/api/python/index.html) identified itself as **PySpark 4.2.0**, dated 2026-07-11. The official `latest` SQL-tuning and streaming-overview URLs also identified their pages as Spark 4.2.0. “Current” means current at that retrieval time only. |
| Exact applicable upstream version | **Apache Spark 4.2.0 / PySpark 4.2.0**. Use the version-pinned citations in this reference for that baseline. The [Apache Spark 4.2.0 release note](https://spark.apache.org/releases/spark-release-4-2-0.html) is the release authority. |
| Exact revision disposition | The retrieved official pages disclose release version `4.2.0`, not an immutable documentation build revision or Git commit. No SHA is inferred. The `/docs/4.2.0/` URLs pin this reference to the disclosed release; they do not prove the target runtime revision. |
| Target-runtime disposition | **Unresolved.** No target-repository configuration, lockfile, image, cluster policy, session output, or runtime metadata was supplied or executed for this record. Do not treat 4.2.0 as the deployed version until target evidence confirms it. |
| Managed-runtime disposition | **Unresolved.** This record makes no claim about a vendor, notebook UI, cell magic, filesystem mount, catalog, display helper, job scheduler, autoscaling policy, Spark Connect endpoint, or library distribution. |
| Method and safety boundary | Public-document retrieval and static repository documentation only. No notebook was opened or run; no cell, UDF, cluster code, package install, data access, credential access, query, or cluster operation was performed. |

## What the Apache Baseline Establishes

Use these claims only after confirming that the target uses a compatible Spark
and PySpark runtime.

| Concern | Verified Apache 4.2.0 evidence | Practical boundary |
| --- | --- | --- |
| SQL and DataFrames | [Spark SQL, DataFrames and Datasets Guide](https://spark.apache.org/docs/4.2.0/sql-programming-guide.html) defines a DataFrame as a Dataset organized into named columns, identifies the DataFrame API as available in Python, and says SQL and Dataset expressions share the execution engine. [PySpark Overview](https://spark.apache.org/docs/4.2.0/api/python/index.html) identifies PySpark as Spark's Python API and includes Spark SQL and DataFrames. | SQL text and DataFrame expressions do not by themselves prove identical target plans, connector pushdown, output, permissions, or data semantics. Establish those from the target's code, schemas, runtime configuration, and bounded validation. |
| Execution plans | [`DataFrame.explain`](https://spark.apache.org/docs/4.2.0/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.explain.html) prints plans for debugging; its `simple`, `extended`, `codegen`, `cost`, and `formatted` modes have distinct outputs. The SQL [`EXPLAIN`](https://spark.apache.org/docs/4.2.0/sql-ref-syntax-qry-explain.html) reference defines physical, parsed, analyzed, optimized, cost, codegen, and formatted-plan output. | A documented explain mode is not a captured plan. Do not claim a scan, exchange, join strategy, predicate pushdown, cost estimate, or runtime statistic without a sanitized target-runtime artifact. |
| Tuning | The [performance-tuning guide](https://spark.apache.org/docs/4.2.0/sql-performance-tuning.html) covers caching, partitioning, statistics, join strategy, and AQE. It states that inaccurate or missing statistics can produce poor plans; it documents `EXPLAIN COST` / `DataFrame.explain(mode="cost")`, runtime statistics in the SQL UI, join hints, and configuration defaults including `spark.sql.shuffle.partitions=200` for this release. It also says AQE is enabled by default since Spark 3.2.0 and can be controlled with `spark.sql.adaptive.enabled`. | Published defaults are a comparison point, not a recommendation or proof of effective values. Target session configuration, administrator defaults, data layout, connector behavior, statistics, workload concurrency, resource limits, and AQE decisions can change the observed result. A hint is not guaranteed to select the hinted strategy. |
| Structured Streaming model | The [Structured Streaming overview](https://spark.apache.org/docs/4.2.0/streaming/index.html) describes the default micro-batch engine and the continuous-processing alternative. The [DataFrame/Dataset streaming API guide](https://spark.apache.org/docs/4.2.0/streaming/apis-on-dataframes-and-datasets.html) documents `readStream`, sources, source-specific fault-tolerance status, and checkpoint-related behavior. | Do not generalize an engine-level guarantee to an unverified source, sink, checkpoint location, trigger, state store, or recovery procedure. The API guide explicitly labels the socket source as testing-only and not end-to-end fault tolerant. |
| Streaming recovery and latency tradeoffs | The [streaming performance guide](https://spark.apache.org/docs/4.2.0/streaming/performance-tips.html) documents asynchronous progress tracking and its limitations, including its initial support only for stateless Kafka-sink queries and lack of end-to-end exactly-once processing. It also documents continuous processing as experimental, at-least-once, limited to supported operations/sources/sinks, and dependent on sufficient cluster cores. | Never enable, disable, or migrate a streaming setting from this reference alone. Check the actual query shape, source and sink compatibility, checkpoint contents and retention, Spark version, and a recovery test plan first. |

## Required Target Evidence Before Making a Runtime Claim

Collect only the evidence authorized for the target repository and environment;
do not infer it from notebook prose or an upstream version.

1. **Version and distribution:** recorded Spark version, PySpark package version,
   Python and Java versions, distribution/build identity, and whether the session
   is classic Spark or Spark Connect. Compare them to the 4.2.0 baseline; treat a
   mismatch as an evidence gap until the matching official documentation is
   consulted.
2. **Execution context:** source-controlled notebook/job definition, dependency
   declarations, session and cluster configuration, enabled extensions, catalog
   and connector versions, and relevant administrator or policy constraints.
3. **Data contract:** input and output schema, row grain, keys, time-zone and
   null rules, source/sink semantics, expected volume, skew, file layout, and
   safe representative fixtures. A notebook's rendered result is not sufficient
   contract evidence.
4. **Streaming contract, when applicable:** checkpoint ownership and durability,
   query identity, source offsets, sink commit semantics, trigger, state-store
   behavior, restart procedure, retention, duplicates, late data, and replay or
   backfill policy.
5. **Performance evidence, when applicable:** sanitized plan artifacts, relevant
    statistics, measured workload and concurrency, executor and driver resources,
    effective Spark configuration, stage/task metrics, and a before/after
    comparison with the same workload.

## Implementation and Notebook Operating Guide

Use this guide after the target runtime and data contract are known. It is a
review and implementation checklist, not permission to run a notebook, submit a
job, inspect data, or alter a cluster.

### Discover the Runtime Before Changing Behavior

Identify the source-controlled entry point and the declared or observed (when
authorized) Spark/PySpark, Python, Java, distribution, connector, and
classic-versus-Connect versions. Also establish effective session settings,
dependency declarations, execution identity, input/output locations, and the
target's approved job or notebook lifecycle. Do not infer any of these from a
file extension, a rendered cell result, a generic `latest` page, or a managed
notebook product assumption.

Treat notebook parameters, widgets, environment values, file paths, SQL text,
and data as untrusted inputs until the target validates and authorizes them.
Treat a notebook, UDF, dependency hook, or pasted cell from an untrusted source
as executable code, not as data or a safe test fixture. Never run it merely to
understand it; use repository review and isolated, explicitly authorized
execution procedures when execution is necessary.

### Make Transformations Reproducible

- Define input and output contracts before transformations: named columns,
  explicit data types, nullable fields, grain, keys, time-zone rules, malformed
  record policy, and schema-evolution behavior. Prefer an explicit schema at
  ingestion and explicit casts or projections at contract boundaries over
  inference from representative data.
- Keep transformations deterministic from declared inputs and parameters. Avoid
  cell-order dependencies, ambient temporary views, hidden session settings, and
  mutable driver globals as transformation inputs. Put reusable transformation
  functions in ordinary source modules when that makes them independently
  testable; notebooks should orchestrate and present approved work rather than
  become the only definition of business logic.
- Test extracted transformations with small, explicit-schema fixtures covering
  nulls, duplicates, late or malformed records, key and grain changes, and
  expected output schema as well as rows. Local unit tests establish
  transformation semantics, not connector, optimizer, cluster, or sink behavior;
  use a separately authorized integration or representative-cluster check for
  those claims.
- Prefer Spark SQL expressions and documented built-in functions when they state
  the required behavior. Introduce a Python UDF only when a built-in cannot meet
  the contract and its serialization, optimizer visibility, type/null behavior,
  failure handling, and performance cost are acceptable. Keep UDF code small,
  deterministic, explicitly typed at the boundary, tested with hostile and
  ordinary input values, and subject to the same untrusted-code and dependency
  controls as any other executable code.

### Reason About Lazy Execution and Distributed Work

DataFrame and SQL construction describes a logical computation; an action or
streaming query start is where work may be triggered. Do not confuse a notebook
display, a successful expression definition, or a local test with a completed
distributed computation. Before changing performance-sensitive behavior, state
the intended action, input size/layout, output contract, and accepted resource
and latency bounds.

Use a captured, sanitized target plan only to support the plan facts it actually
shows. Compare logical and physical plan changes, relevant statistics, exchanges,
and runtime stage/task evidence before attributing a result to a join, pushdown,
partition, or AQE decision. The upstream `explain` modes in the evidence baseline
describe available diagnostics; they do not make an uncaptured plan factual.

- Select partition counts and layouts from measured input size, file layout,
  downstream parallelism, and cluster resources. Repartitioning, coalescing, and
  changing a shuffle setting are behavior and cost changes, not formatting.
- Treat joins, aggregations, sorts, windows, distinct operations, and explicit
  repartitioning as potential shuffle boundaries. Investigate a suspected skew
  with distribution and stage evidence; define the skew key and the correctness
  of any salting, filtering, aggregation, or layout change before applying it.
- Keep data on executors. Do not use unbounded `collect`, `toPandas`, iterator
  materialization, large exception messages, or verbose samples as routine
  notebook diagnostics. Bound and sanitize any authorized sample, aggregate,
  schema, or metric sent to the driver, and account for driver memory separately
  from executor capacity.
- Cache or persist only after identifying the reused computation, storage level,
  capacity impact, owner, invalidation condition, and measurement. Unpersist
  temporary caches in an approved cleanup path; never assume a restart, run-all,
  or session end removes the intended cache or leaves no competing state.

### Writes, Retries, and Structured Streaming

Treat every write, merge, external call, checkpoint change, and query start/stop
as a side effect. Before an authorized execution, define destination ownership,
schema compatibility, commit/visibility semantics, duplicate and partial-write
handling, retry classification and bounds, idempotency key or equivalent, and
the operator's repair or rollback procedure. A retry is safe only when the
specific source, sink, and write operation establish that safety; do not infer
idempotency from a notebook rerun or a Spark engine label.

For Structured Streaming, additionally define query identity, source offsets,
checkpoint location and exclusive ownership, trigger, watermark and late-data
policy, state-store growth and retention, sink commit behavior, stop/restart
procedure, and replay/backfill policy. Test failure and recovery only against
authorized disposable inputs and outputs. Do not delete, share, relocate, or
reuse a checkpoint to make a query start, and do not treat a running query or a
single micro-batch as proof of end-to-end delivery semantics.

### Credential, Package, and Cluster Boundaries

- Obtain data access through the target's approved identity and secret-reference
  mechanism. Do not embed credentials in notebooks, UDFs, parameters, paths,
  SQL, logs, screenshots, plans, or test fixtures; do not print or retrieve them
  to prove access.
- Do not install packages, mutate a notebook-scoped environment, change cluster
  libraries, or alter Spark/session configuration as an exploratory workaround.
  Make dependency and package changes source-controlled, reproducible, reviewed
  under target policy, and separately assess registry, lockfile, install-hook,
  and provenance risk when material.
- Cluster commands, job submissions, restarts, cache eviction, stream controls,
  and data access require explicit target authority and its bounded operating
  procedure. Static code review, a task packet, and this reference do not grant
  that authority.
- Keep plans, logs, metrics, screenshots, and cluster evidence sanitized and
  minimally scoped. They can demonstrate only the captured runtime, workload,
  identity, and configuration context; they do not establish production
  representativeness without the comparison in the next section.

## Notebook, Restart, and Run-All Limits

Notebook behavior is conditional on the target platform. Until its documentation,
configuration, and approved observations are available, mark every item in this
section **unresolved** rather than assuming a particular managed runtime.

- **Cell order and hidden state:** A successful individual cell does not prove a
  clean, ordered, reproducible notebook execution. Imports, variables, temporary
  views, cached data, session configuration, and externally persisted state may
  survive or be absent depending on the platform and lifecycle.
- **Restart:** Do not assume what a kernel, driver, Spark session, cluster, or job
  restart clears, preserves, reattaches, retries, or bills. In particular, do not
  assume a restart preserves streaming checkpoint compatibility, state, or
  partially written output. Identify the target's restart semantics and prove
  recovery against a disposable, authorized fixture before relying on it.
- **Run all:** “Run all” is an execution affordance, not a correctness or
  deployment guarantee. It may not reproduce a scheduled-job environment,
  parameterization, dependency resolution, user identity, concurrency, trigger,
  cluster shape, or prior external side effects. It must not be used as the sole
  evidence for SQL correctness, streaming recovery, or performance.
- **Stateful and side-effecting cells:** Treat table writes, cache changes,
  streaming query starts/stops, checkpoints, external calls, and package or
  session changes as stateful operations. Their safety, idempotency, and cleanup
  are target-specific and unverified here.
- **Vendor helpers:** Do not introduce or rely on magics, widgets, display APIs,
  filesystem helpers, secret utilities, or platform-specific scheduling APIs
  unless source-controlled target evidence establishes the vendor and supported
  behavior.

## Representative-Cluster Limits

This reference has no representative-cluster evidence. It cannot support a
claim that a local session, default notebook cluster, or development pool
represents production.

Before calling a plan or tuning result representative, establish the comparison
dimensions that materially affect it: Spark and connector distribution,
effective configuration, executor count/cores/memory/disk, driver resources,
autoscaling and dynamic allocation, worker type/architecture, network and
storage locality, concurrent workload, input volume and file sizes, data skew,
statistics freshness, cache state, source/sink throughput, and relevant
security/governance controls. Document any mismatch and limit the conclusion to
the environment actually measured.

The Spark tuning guide's documented defaults and optimization features are not
substitutes for this evidence. The streaming guide's continuous-mode core
requirement is a concrete example: enough parallel cluster cores are required
for its long-running tasks to make progress, but the necessary count depends on
the query's source partitions and is therefore not inferable here.

## Uncertainty Register and Handoff

| Status | Boundary | Required resolution before a stronger claim |
| --- | --- | --- |
| Confirmed upstream | Apache Spark/PySpark 4.2.0 documentation facts cited above. | None; retain the version-pinned citation with the claim. |
| Unresolved target runtime | Exact deployed Spark/PySpark/build/Python/Java and classic-versus-Connect mode. | Authorized target configuration or runtime metadata; use the matching version's official docs. |
| Unresolved managed platform | Vendor, notebook lifecycle, restart, run-all, identity, filesystem, and scheduler behavior. | Target platform documentation plus source-controlled configuration and an authorized, bounded validation plan. |
| Unresolved recovery | Checkpoint compatibility, source replay, sink idempotency/commit behavior, state recovery, and partial-write handling. | Query-specific contract and authorized recovery exercise; do not restart or run a stream merely to fill this gap. |
| Unresolved performance | Plan, statistics, resource allocation, data layout/skew, concurrency, and production representativeness. | Sanitized representative-cluster measurements and comparable workload evidence. |

When a task needs to execute a notebook or inspect a real cluster, obtain
target-repository authority and use its approved, bounded validation procedure.
This reference itself authorizes no execution, package installation, data access,
or platform action.

## Source Index

All sources below are official Apache Spark sources retrieved on 2026-07-31.
Version-pinned links are preferred for claims; `latest` was consulted only to
record the current-version disposition at retrieval.

1. [PySpark Overview — 4.2.0](https://spark.apache.org/docs/4.2.0/api/python/index.html)
   and [latest at retrieval](https://spark.apache.org/docs/latest/api/python/index.html)
2. [Spark Release 4.2.0](https://spark.apache.org/releases/spark-release-4-2-0.html)
3. [Spark SQL, DataFrames and Datasets Guide — 4.2.0](https://spark.apache.org/docs/4.2.0/sql-programming-guide.html)
4. [`pyspark.sql.DataFrame.explain` — 4.2.0](https://spark.apache.org/docs/4.2.0/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.explain.html)
5. [SQL `EXPLAIN` — 4.2.0](https://spark.apache.org/docs/4.2.0/sql-ref-syntax-qry-explain.html)
6. [Performance Tuning — 4.2.0](https://spark.apache.org/docs/4.2.0/sql-performance-tuning.html)
7. [Structured Streaming Overview — 4.2.0](https://spark.apache.org/docs/4.2.0/streaming/index.html)
8. [Structured Streaming: APIs on DataFrames and Datasets — 4.2.0](https://spark.apache.org/docs/4.2.0/streaming/apis-on-dataframes-and-datasets.html)
9. [Structured Streaming: Performance Tips — 4.2.0](https://spark.apache.org/docs/4.2.0/streaming/performance-tips.html)
