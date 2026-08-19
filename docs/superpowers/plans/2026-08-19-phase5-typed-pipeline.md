# Phase 5 Typed Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Build a typed, end-to-end order transformation pipeline whose function boundaries validate Pandera input and output schemas at runtime.

**Architecture:** Keep the Phase-4 `OrderSchema` as the trusted input contract, add a stricter `EnrichedOrderSchema` for transformation output, and use `@pa.check_types(lazy=True)` on the transformation boundary. Keep batch input validation/reporting separate from internal typed transformations, then orchestrate ingestion → validation → enrichment → persistence in `pipeline.py`.

**Tech Stack:** Python 3.10+, pandas 2.x, Pandera 0.32.1, pytest 8.x, JupyterLab 4.x.

**Spec:** `docs/00_roadmap.md` Phase 5 and the cumulative learning-repository requirements established in Phases 1–4.

## Global Constraints

- Preserve all earlier notebooks and their historical behavior.
- Keep `pandera[pandas]==0.32.1` pinned for reproducibility.
- Use `pandera.pandas as pa` for pandas-facing Pandera APIs.
- Use `pandera.typing.DataFrame[Schema]` annotations on typed dataframe function boundaries.
- Use `@pa.check_types(lazy=True)` to validate transformation inputs and outputs at runtime.
- Invalid source data is an expected data-quality outcome and must produce reports rather than trusted output.
- Output-schema violations are programmer/transform defects and must raise rather than be converted into ordinary source-data failures.
- Generated clean data and reports remain ignored by Git.
- Phase 5 must include code, tests, notebook, lesson, challenge, interview questions, solutions, examples, and updated README/roadmap.

---

### Task 1: Freeze the Phase-4 educational schema

**Files:**
- Modify: `src/pandera_lab/schemas/history.py`
- Modify: `src/pandera_lab/schemas/__init__.py`
- Modify: `notebooks/04_business_rules.ipynb`

**Interfaces:**
- Produces: `Phase4OrderSchema`, equivalent to the schema taught at the end of Phase 4.

- [x] Add `Phase4OrderSchema` with the Phase-4 custom and dataframe checks.
- [x] Export it from `pandera_lab.schemas`.
- [x] Make Notebook 04 import `Phase4OrderSchema as OrderSchema`.
- [x] Verify Notebook 02/03/04 each reference their frozen phase schema.

### Task 2: Add a semantic output schema

**Files:**
- Create: `src/pandera_lab/schemas/analytics.py`
- Modify: `src/pandera_lab/business_rules.py`
- Modify: `src/pandera_lab/schemas/__init__.py`
- Test: `tests/test_phase5_typed_pipeline.py`

**Interfaces:**
- Consumes: `OrderSchema`, existing order business-rule helpers.
- Produces: `EnrichedOrderSchema` with `gross_amount`, `discount_amount`, `net_amount`, `order_month`, and `is_discounted`.

- [x] Write tests for valid enriched output and semantic mismatches.
- [x] Add reusable expected-value helpers for derived analytics columns.
- [x] Define `EnrichedOrderSchema(OrderSchema)` with `strict=True` and dataframe-level checks for all derived fields.
- [x] Verify a correct enriched frame passes and incorrect derived values fail.

### Task 3: Add the typed transformation boundary

**Files:**
- Create: `src/pandera_lab/transformations.py`
- Modify: `src/pandera_lab/__init__.py`
- Test: `tests/test_phase5_typed_pipeline.py`

**Interfaces:**
- Produces: `enrich_orders(df: DataFrame[OrderSchema]) -> DataFrame[EnrichedOrderSchema]`.

- [x] Write tests showing invalid input is rejected before a trusted result is produced.
- [x] Write tests showing valid raw-text-compatible input is coerced and enriched.
- [x] Implement `@pa.check_types(lazy=True)` on `enrich_orders`.
- [x] Ensure the transformation returns a new dataframe and does not mutate the caller's columns.
- [x] Verify output columns and derived values.

### Task 4: Add end-to-end pipeline orchestration

**Files:**
- Create: `src/pandera_lab/pipeline.py`
- Modify: `src/pandera_lab/__init__.py`
- Create: `examples/phase5_run_pipeline.py`
- Test: `tests/test_phase5_typed_pipeline.py`

**Interfaces:**
- Produces: `PipelineResult` and `run_order_pipeline(input_path, output_path, report_dir)`.

- [x] Write a valid-pipeline integration test that writes a trusted enriched CSV.
- [x] Write an invalid-pipeline integration test that writes detailed/summary reports and no trusted output.
- [x] Implement stale-artifact cleanup so current run state cannot be confused with a previous run.
- [x] Keep transformation contract failures uncaught so programming defects fail loudly.
- [x] Add a runnable example for both valid and invalid batches.

### Task 5: Build the educational Phase-5 layer

**Files:**
- Create: `docs/05_typed_pipeline.md`
- Create: `notebooks/05_typed_pipeline.ipynb`
- Create: `challenges/05_typed_pipeline.md`
- Create: `interview/05_typed_pipeline.md`
- Create: `solutions/07_phase5_reference.md`
- Create: `solutions/08_interview_phase5_answers.md`
- Create: `PHASE_5.md`
- Modify: `README.md`
- Modify: `START_HERE.md`
- Modify: `docs/00_roadmap.md`
- Modify: `pyproject.toml`

**Interfaces:**
- Teaches: manual validation vs typed decorators, input/output contracts, trusted transformations, pipeline orchestration, and source-data failures vs code-contract failures.

- [x] Create a problem-driven lesson with architecture diagrams and failure semantics.
- [x] Create an executable notebook that demonstrates valid input, invalid input, broken output, valid pipeline, and invalid pipeline.
- [x] Add challenge and interview material with separate reference answers.
- [x] Update repository navigation and project version to `0.5.0`.

### Task 6: Verification and packaging

**Files:**
- Verify all Python source/test/example files.
- Verify all five notebooks.
- Verify ZIP contents and hashes.

- [x] Run Python compile/AST checks across the repository.
- [x] Run notebook JSON validation and historical-schema import scans.
- [x] Run `pytest` if Pandera is available; otherwise record the dependency/runtime blocker explicitly.
- [x] Check for TODO/TBD placeholders, cache files, and accidental generated reports/clean data.
- [x] Build `pandera-data-quality-lab-phase5.zip` and verify archive integrity.


## Verification note

The implementation environment did not have Pandera installed, and network/DNS access prevented installing `pandera[pandas]==0.32.1`. The full pytest command was still executed and stopped during collection with `ModuleNotFoundError: No module named 'pandera'`. Static Python compilation, AST checks, notebook JSON/Python-cell parsing, historical-schema checks, pure business-rule runtime checks, and ZIP integrity checks were used as the available local verification layers. Run `python -m pip install -r requirements.txt && pytest` in a normal connected project environment before publishing the repository.
