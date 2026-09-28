# Cooling Fluid Discovery — Project Specification

Version 0.3 — after red-team cycle 2 · 28 September 2026

## 01. Purpose and delivery contract

Build a reproducible research system that discovers and evaluates candidate cooling fluids through measured data, chemical representations, thermodynamic calculations, predictive machine learning and sequential experiment selection. The proposed first application is fluorine-free, electrically insulating, two-phase immersion cooling. This application is a research hypothesis requiring confirmation in the first epic; the software shall support other explicitly versioned application profiles.

The intended outcome is a defensible decision about candidate fluids and the usefulness of the discovery process. A negative feasibility result is a valid research outcome. A working application, an accurate model, a useful experimental selection policy and a qualified commercial fluid are different deliverables.

The final specification is intended for subsequent Jira decomposition and AWF execution. Logical IDs beginning FDE are proposed planning identifiers, not existing Jira issue keys. This document does not create tickets, authorize purchases, commission experiments, install software, modify AWF or authorize a merge.

Three completion levels apply:

1. **Engineering completion:** the data-to-decision workflow runs reproducibly and satisfies its software acceptance tests.
2. **Research completion:** the declared benchmark and prospective evaluation are performed and their results reported, including inconclusive or negative results.
3. **Candidate qualification:** a specific physical formulation and batch meets an agreed application profile in appropriate physical testing. This is not implied by either of the first two levels.

The owner chooses the application and resource envelope. A chemistry lead reviews chemical plausibility and interpretation; a thermal/electrical lead defines system tests; an experimental partner executes agreed measurements; AWF implementation and review roles govern software delivery. These are responsibilities to assign, not people already engaged.

## 02. Scope, assumptions and exclusions

The core release includes source ingestion, evidence normalization, molecular identity, property models, physical baselines, screening, experiment selection, experimental result intake and decision reports. Mathematica is the primary research interface and orchestration language. Python adapters provide specialist libraries where they add measured value.

Start with commercially accessible pure compounds. Introduce binary formulations through a separately validated mixture model; a component's properties must not be treated as the properties of its blend. Keep optional chemical-family exploration separate from purchasable-candidate delivery.

The initial system does not require new molecule synthesis, autonomous laboratory hardware, an RL generator, a bespoke CUDA kernel, a new quantum chemistry engine, a multi-tenant web application, or a production data-center trial. Those are contingent extensions. It will not treat a lookup function, a language-model answer or a molecular orbital calculation as a complete coolant qualification.

Working assumptions: the owner prefers a Mathematica-led implementation; a local licensed Wolfram runtime can be arranged; some public measurements are usable; external calculations and laboratory work will have finite budgets. None of these establishes access to a particular machine, licence, laboratory, compound or dataset. Hardware discovered in other projects is not allocated to this project by default.

Research lanes are PURE (known compounds), MIX (binary formulations), NOVEL (unmade structures) and SYSTEM (fluid/pressure/equipment co-design). PURE is the initial implementation path. Activating another lane requires its own profile and evidence. Single-phase cooling is a distinct lane/profile, not a silent relaxation of the two-phase objective.

The **minimum useful release (MUR)** is a reproducible pure-fluid research run: ingest a curated measurement panel, construct a leakage-audited benchmark for at least two usable endpoints, compare simple/physical/ML models, produce an evidence-labelled shortlist and export a proposed next batch. It requires neither external quantum software nor successful fluid discovery. A thin vertical slice precedes broad engine integration.

Planning limits for that slice are up to 10,000 unique candidate structures, up to 100,000 normalized observations, a reference panel initially targeting 20–40 substances, and at most 20 optional detailed calculation requests. These are sizing assumptions and caps for initial test design, not assertions of data availability, adequate training sample size or an authorized purchase. Increase them only through a documented capacity decision. The reference panel can be smaller when the coverage report explains why; it cannot support a stronger statistical claim merely by definition.

MIX schemas and rejection behavior are core. Mixture prediction, mixture optimization, NOVEL synthesis and SYSTEM co-design are contingent capabilities. The baseline release must clearly report a disabled lane rather than simulate its availability.

## 03. Initial application profile

Create a machine-readable, versioned profile before candidate optimization. Each constraint must carry a property identifier, condition set, numerical threshold or categorical rule, unit, evidence requirement, test method reference, rationale and decision owner. Mark proposed values distinctly from agreed values.

| Profile item | Initial proposal | Evidence needed to freeze it |
|---|---|---|
| Application | Two-phase immersion cooling of electronics | Equipment boundary, immersion arrangement and use case |
| Chemistry policy | No intentionally included fluorine-containing component | Structure policy plus physical composition evidence for tested batches |
| Boiling envelope | Explore 45–55 °C at 101,325 Pa | Thermal-system requirement; this is a proposed research window, not a claim of universal compatibility |
| Electrical performance | Separate breakdown strength, resistivity, permittivity and dielectric loss requirements | Methods, frequency where relevant, temperature, purity and ageing conditions |
| Fire behavior | Seek a fluid acceptable for the agreed operating and fault conditions | Named tests and acceptance criteria; no-flash observation alone is insufficient |
| Thermal performance | Compare useful heat removal and operating margin with a reference fluid in a defined rig | Geometry, heat flux, surface, pressure and uncertainty |
| Material compatibility | Relevant metals, seals, polymers, boards and surface treatments | Exposure conditions, endpoints and allowable changes |
| Lifecycle | Stability, contamination tolerance, vapor loss and composition drift | Defined ageing protocol and sampling plan |
| Practicality | Purchasability, purity, usable quantity and cost | Dated supplier information and acquisition estimates |

Do not optimize a single generic cooling score before these boundaries exist. Critical heat flux and heat-transfer coefficients depend on the surface and apparatus; model them only with the required system inputs. A high latent heat alone does not prove a superior coolant.

Every hard constraint evaluates to PASS, FAIL or UNKNOWN. UNKNOWN is retained as an explicit evidence gap and cannot count as a qualified pass. Predictions may support ranking but physical evidence is required for properties designated experimental by the profile. Screening profiles and qualification profiles remain distinguishable.

A profile has `status = RESEARCH_DRAFT | RESEARCH_FROZEN | CAMPAIGN_READY | QUALIFICATION_READY`. These are project data states, not AWF lifecycle states. RESEARCH_FROZEN permits offline analysis with explicitly recorded unknowns. CAMPAIGN_READY requires named tests, required sample amounts, laboratory capacity, costs, operating bounds and a signed-off experimental design for the proposed actions. QUALIFICATION_READY means that the specification of qualification is complete, not that any fluid has passed it.

Fields that must be resolved before qualification work are electrical thresholds and measurement frequency, permissible flame behavior under named methods, ageing duration/cycles, allowed material changes, acceptable composition drift, thermal performance margin and reference rig. At least one independently sourced reference fluid must be characterized in the actual apparatus before comparative candidate claims. Where a thermal limit is not yet justified, the responsible task is to establish it; inventing a numerical value does not close the task.

The initial no-fluorine search policy is deliberately stricter than an unspecified PFAS exclusion. It is a structural search definition, not an analytical guarantee that a sample contains zero fluorine or a complete environmental assessment. A sample-level claim requires an agreed analytical method and reporting limit. Other chemical families are excluded only by a versioned chemistry rationale, not by assuming that all non-fluorinated compounds are acceptable.

## 04. Questions and hypotheses

H1 — A usable region exists within the selected chemistry, operating envelope and practical constraints. Test with a structured feasibility map and reference compounds before a large search.

H2 — Structure- and condition-aware models improve property predictions over simple and physical baselines on genuinely held-out chemical groups. Evaluate each property and the resulting constrained ranking.

H3 — Sequential selection produces better experimental decisions than fixed screening and random selection for the same resource budget. Evaluate cumulative cost, confirmed feasible candidates and useful trade-offs.

H4 — Physical models or calculations improve predictions in the target domain enough to justify their cost. Compare data-only, physics-only and combined models under matching information budgets.

H5 — Binary formulation search offers improvement beyond the pure-fluid frontier while respecting phase behavior and composition stability. This hypothesis is conditional on completing mixture-specific validation.

Record a hypothesis as supported, unsupported or inconclusive within the tested domain. Software ticket completion must not depend on obtaining a positive scientific finding. Retain failed experiments and rejected candidates with their reasons.

## 05. Architecture and language boundary

Use a modular local research application, with batch operation as a first-class mode. Mathematica notebooks are interactive views over version-controlled Wolfram Language packages; hidden notebook state must not be necessary to reproduce a run.

| Component | Proposed implementation | Contract |
|---|---|---|
| Research interface | Mathematica notebooks | Browse evidence, choose profiles, inspect decisions, launch named workflows |
| Workflow and policy logic | Wolfram Language packages | Validate input snapshots, invoke adapters, apply constraints, build reports |
| Evidence store | Immutable source files plus normalized JSON records and manifests | Preserve provenance and append new versions |
| Feature pipeline | Wolfram chemistry functions; optional Python chemistry adapter | Versioned molecular identity and feature definitions |
| Predictive models | Wolfram baselines; Python adapter for advanced models | Same prediction envelope and evaluation harness |
| Thermodynamic/quantum adapters | External executable or Python integration | Explicit capabilities, inputs, units, errors and method provenance |
| Experiment policy | Wolfram implementation or BoTorch adapter | Select from eligible candidates under resource constraints |
| Reporting | Markdown and JSON; notebook views | Candidate evidence, benchmark outcomes, proposed experiments and decisions |

The first release uses one authoritative copy of each function: orchestration and profile logic in Wolfram Language; optional specialist algorithms behind adapters. Do not duplicate a complete Python and Wolfram implementation of every model.

Documented Wolfram capabilities relevant to implementation include Molecule, MoleculeModify, MoleculeValue, ChemicalData, Predict, ExternalEvaluate, RunProcess, VerificationTest and TestReport. Availability and behavior must be tested on the pinned installation. Proposed project APIs are separate from these vendor functions.

Use subprocess argument arrays and structured input files; do not interpolate molecule strings into shell commands. A worker has a unique run directory, finite time budget and cancellation behavior. Adapter output is validated before entering the evidence store.

### Proposed repository structure and ownership

| Path | Responsibility | Initial owner stream |
|---|---|---|
| `src/wolfram/FDE/` | Profile, data, feature, screening and reporting packages | Assigned per module; one writer |
| `notebooks/` | Thin research views and walkthrough | Interface stream |
| `python/fde_adapters/` | Specialist models, solver adapters and process bridges | Modeling/adapter stream |
| `schemas/` | Project envelopes and schema migrations | Contract owner |
| `profiles/` | Versioned research/application/metric definitions | Science/profile owner |
| `fixtures/` | Small independently checked examples and negative cases | Owning module + reviewer |
| `tests/wolfram/`, `tests/python/`, `tests/integration/` | Module and cross-runtime verification | Owning module |
| `data/manifests/` | Immutable input references and normalized snapshot manifests | Evidence stream |
| `evidence/` | Bounded review/verification reports; no uncontrolled raw data | Ticket-specific owner |
| `docs/` | Methods, runbooks, decisions and report templates | Ticket-specific owner |

Managed AWF paths are outside ordinary product-edit scope. Large raw datasets, calculation outputs, model weights, sample images and instrument files belong in an agreed artifact store with immutable hash references and backup policy; the project repository stores manifests and small permitted fixtures. A database/server deployment is not required for the first release.

### Component interface contract

The following names are proposed **project operations**, not Wolfram built-ins or claimed implemented commands: `ingest_source`, `normalize_observations`, `resolve_identity`, `compute_features`, `fit_baseline`, `train_model`, `predict_properties`, `calculate_properties`, `screen_candidates`, `propose_actions`, `ingest_results` and `render_report`. Provide a single batch dispatcher and thin notebook wrappers over these operations. Pin the operation version independently of the document version.

Every request carries `schema_version`, `operation`, `request_id`, `input_manifest`, `profile_id` when applicable, `parameters`, and `resource_envelope_id` for resource-consuming work. Every response carries `schema_version`, `request_id`, `status`, `output_manifest`, `errors`, `warnings`, `provenance` and `usage`. Allowed operation states are SUCCESS, PARTIAL, FAILED, BLOCKED, CANCELLED and UNKNOWN_OUTCOME. SUCCESS requires all mandatory requested outputs; PARTIAL is never silently promoted. Error records include code, locus, retry classification and relevant evidence.

Prediction items have their own status: VALID, OUT_OF_DOMAIN, UNSUPPORTED, FAILED or MISSING_INPUT. A VALID item supplies property, candidate/condition IDs, value, unit, method and provenance. A failed/unsupported item must not contain a usable numeric estimate. An interval records bounds, nominal level, calibration population and method; absence of an interval is represented explicitly. Constraint states remain PASS/FAIL/UNKNOWN and are not operation statuses.

Request/response schemas reject unknown fields for stable interfaces, nonfinite numbers, malformed identities, incompatible units and invalid condition combinations. Large outputs are manifest-referenced. Treat data deserialization as data parsing; never evaluate Wolfram expressions or untrusted Python pickles from external sources. Use reviewed model serialization mechanisms and provenance checks.

Select one supported Wolfram version and one Python environment in E01 and record their versions. Do not require unverified cross-platform parity: choose a primary execution platform, test it, and document secondary-platform claims only after their tests run. The Python wrapper must propagate an unavailable Wolfram runtime or a failing Wolfram test to a failing required check; it cannot replace it with a skip or mock.

Cross-runtime golden fixtures cover °C/K, kPa/Pa, gauge/absolute pressure rejection, cP/Pa·s, molar/mass conversion, null values, censoring, component permutations, unsupported chemistry and a failed external process. Compare numeric values within declared unit-aware tolerances and categorical states exactly.

## 06. Evidence and data model

Keep source material, observed measurements, derived values, simulation outputs and model predictions as different entity types. The system must be able to answer where every number came from and under which conditions it applies.

| Entity | Required fields |
|---|---|
| SourceRecord | source_id, title, URL/DOI or supplied-file reference, retrieval date, file hash, extraction locator, access/reuse notes |
| Substance | substance_id, original identity, normalized structure, stereochemistry/isotope policy, identifiers, identity status, normalization version |
| Formulation | formulation_id, component identities, fractions, fraction basis, composition uncertainty, preparation metadata |
| Sample | sample_id, substance/formulation reference, batch, purity, water/contamination evidence, preparation and storage metadata |
| Observation | observation_id, sample/substance reference, property, value or bound, units, conditions, method, uncertainty, source, evidence class |
| Calculation | calculation_id, structure/geometry, engine and version, model chemistry/parameters, convergence, conditions, result, input/output hashes |
| DatasetSnapshot | snapshot_id, observation IDs, exclusions, normalization version, source hashes, created timestamp |
| ModelArtifact | model_id, training snapshot, feature schema, split, hyperparameters, environment, metrics, domain limits, artifact hash |
| Prediction | prediction_id, candidate, property, conditions, mean/interval, uncertainty method, model/calculation IDs, applicability status |
| ExperimentProposal | proposal_id, candidates, measurements, conditions, rationale, expected cost, dependencies, profile/model IDs |
| ExperimentResult | result_id, proposal/sample links, raw files, observations, calibration/control outcomes, deviations |
| Decision | decision_id, profile, evidence references, constraint states, rank rationale, unresolved gaps, actor and timestamp |

Use SI internally while retaining original values and units. Preserve pressure basis, temperature scale, composition basis, phase, test frequency and method. Unknown conditions stay unknown. Store a censored value as a bound; do not silently replace it with its threshold.

The same paper may be represented in several databases. Resolve shared provenance before counting independent observations. Keep conflicting measurements separately until an explicit reconciliation rule is applied; record both the rule and the retained uncertainty.

Priority sources are NIST Chemistry WebBook, NIST ThermoML and traceable primary measurements. ChemicalData is a convenience for discovery and cross-checking, not a substitute for source-level provenance when a value affects a decision. Supplier data require identity, purity, method and date checks.

### Normative measurement and identity semantics

Observation `value_kind` is EXACT, INTERVAL, LEFT_CENSORED, RIGHT_CENSORED, CATEGORICAL or MISSING. EXACT requires a finite value; INTERVAL requires ordered bounds; censoring requires its bound and direction; MISSING requires a reason and forbids a numeric placeholder. Measurement uncertainty records type (standard/expanded/confidence interval), magnitude/bounds, coverage factor or level where known, and estimation method. Unspecified uncertainty is not zero.

Condition records contain absolute temperature, absolute pressure, phase and property-specific fields. Electrical endpoints additionally require test frequency where relevant, electrode/geometry and method, plus sample conditioning. Thermal apparatus endpoints require rig/surface identifiers. `saturation_temperature`, `bubble_temperature` and `dew_temperature` are different property IDs. `dynamic_viscosity` and `kinematic_viscosity` are different property IDs; conversion requires a matched density measurement/estimate with lineage. Mass-to-molar conversion requires the correct composition and molar mass basis.

A Substance identifies chemical identity; a Formulation identifies a specified composition; a Sample identifies a physical batch/preparation. Qualification attaches to Sample plus profile and protocol, with any permitted extrapolation separately justified. A generic catalogue identity cannot inherit all measurements made on every batch with that name. Unknown impurity/water content stays explicit.

Fractions are nonnegative, carry a declared mass or mole basis and sum to unity within a schema-defined tolerance. Preserve reported fractions even if a separate normalized computational form is generated. Do not silently renormalize an incomplete commercial formulation to 100%. Component-permutation normalization must preserve the mapping between each fraction and its component.

Each derived datum links parent observations and the transformation version; each prediction links the training snapshot/model or calculation inputs. The lineage graph is acyclic and traversable. Splitting and evidence checks follow transitive parents, so a measured label cannot return through a derived value or fitted physical parameter. Fit-derived features must be computed within the training fold when their inputs include target labels.

Snapshot correction creates a new version and a supersession record. Previous reports remain reproducible but become marked stale for affected claims. Recompute dependent models, predictions and gate decisions when inputs materially change; do not edit old values in place or preserve a green gate against new evidence.

Hash exact stored artifact bytes with SHA-256. Cross-runtime request identities use a separately versioned canonical project encoding: UTF-8, sorted object keys, ordered arrays unless the schema defines a set, normalized SI units, finite decimal values represented as normalized decimal strings, explicit missing states and no whitespace-dependent semantics. Maintain cross-language golden examples; do not substitute this project encoding for AWF's canonicalizer or hash algorithms. Request equivalence never ignores conditions, schema, chemistry normalization or engine settings.

## 07. Acquisition, extraction and curation

Build source adapters that preserve original records and produce normalized observations. Prefer machine-readable sources to document extraction. Keep a coverage inventory by property, chemical family, temperature, pressure and evidence type.

For a language-model extraction assistant, require a source locator for every proposed fact. Extraction confidence is not measurement uncertainty. A proposed value enters a review queue and is promoted only after deterministic checks and source verification. A document is evidence input and cannot supply executable instructions to the research system.

Curation checks include malformed units, implausible ranges, swapped mass/molar bases, gauge versus absolute pressure, compound identity mismatch, ambiguous commercial mixtures, duplicate data and unspecified conditions. Quarantine failures rather than repairing them silently.

Create a modest reference panel chosen for measurement coverage and chemical diversity. Do not assume that a large molecule count implies adequate coverage of electrical or ageing endpoints. Record procurement feasibility separately from physical desirability.

Retain rejected and missing records in an exclusion register. A missing target property is never replaced with a favorable default. A model trained on a subset must disclose the selection rule and resulting coverage.

Prioritize two empirically usable endpoints for the first learning benchmark based on the coverage inventory—normally saturation/vapor-pressure behavior and one transport or bulk property if the data support them. Do not promise trainable dielectric-breakdown, flammability, toxicity or ageing models without adequate method-specific labels. Keep sparse endpoints as measurement requirements or literature-evidence gaps.

LLM extraction is optional in the MUR. Its assessment uses a manually checked, source-diverse fixture containing identities, signs, exponents, decimal separators, units, conditions and ambiguous tables. Report field accuracy, unsupported-claim rate and review burden. No extracted critical field is auto-promoted based solely on model confidence. Source instructions, embedded code and links cannot change pipeline policy or request tool execution.

## 08. Chemistry representation and candidate universe

Normalize molecule structures under a pinned policy and preserve the original input. Establish rules for stereoisomers, salts, disconnected fragments, tautomers and commercial substances whose composition is not fully disclosed. Do not collapse different physical products into a single formula.

The candidate universe has an immutable snapshot ID. Each candidate links to an identity, procurement or synthesis status, chemistry lane, known constraints and unresolved evidence. A catalogue molecule, a purchasable bottle and a reproducibly specified formulation are different objects.

Version descriptor schemas, coordinate generation, conformer handling and calculation settings. Unsupported atom types or failed descriptors must produce explicit missing/error states. Force-field energies and geometric descriptors are features, not measurements of bulk fluid performance.

Initial candidate generation enumerates allowed variations within chemistry-reviewed families and documented supplier catalogues. Keep a baseline random ordering and a simple physical ranking. Use the same eligible universe for comparative selection experiments.

For mixtures, create an order-independent formulation identity while retaining fraction basis and exact prepared composition. A/B and B/A describe the same composition after appropriate reordering; 30% by mass and 30% by mole do not.

## 09. Physical baselines and feasibility analysis

Construct a feasibility map before building a sophisticated generator. Compare observed property combinations in the target region, highlight unsupported extrapolations, and identify constraints for which no credible measurement path exists.

Pure-fluid baseline calculations include unit-checked vapor-pressure fits within their validity range, saturation-temperature calculation at an explicit pressure, simple property correlations and reference-data comparisons. Report model range and fitting uncertainty. For a vapor-pressure fit, a numerical root outside the validated range is an extrapolation, not an established boiling point.

Mixture work requires phase-equilibrium calculations and empirical checks. An ideal-mixture calculation may be a baseline but cannot qualify a blend. Distinguish bubble and dew conditions, liquid and vapor compositions, liquid-liquid separation, temperature glide and composition change during evaporation or loss.

Treat thermal conductivity, viscosity, heat capacity, surface tension, density and latent heat as condition-dependent quantities. Do not infer electrical breakdown from dielectric constant, or flame behavior from a molecular structural flag. An absent fluorine atom does not establish acceptable toxicity, environmental fate or materials compatibility.

Candidate feasibility reports must show all constraints, including unknowns. When no feasible region has been demonstrated, the report must identify which assumptions would need investigation; it must not automatically change the target to obtain a positive result.

The initial mixture scope is identification, exchange, provenance and unsupported-request handling. Enabling MIX requires a separate validation panel of pure endpoints and binary equilibrium data. Check component-permutation invariance, exact pure-component limits, fraction-basis conversions, conservation and single/two-liquid-phase behavior. Evaporation/cycling evidence must address the vapor path and residual liquid, not only the initially prepared blend. Absence of these results leaves MIX_DISABLED or MIX_RESEARCH_ONLY.

Use a two-phase-specific system comparison. Before rig tests, promising thermophysical properties are screening evidence only. If the chosen profile yields no credible candidates, deliver a bounded infeasibility/knowledge-gap report and a ranked list of assumptions worth testing. A move to elevated pressure or single-phase operation is a new profile and separate hypothesis, never retrospective success on the original target.

## 10. Models, uncertainty and applicability

Train property-specific baselines before multi-task or molecular graph models. Compare a constant/nearest-reference baseline, a transparent structure-property model where supported, and random-forest or Gaussian-process models. Neural models are conditional extensions justified by data coverage and benchmark results.

Include measurement conditions explicitly. A temperature-dependent property model must not mix observations from different conditions as if they were repeated labels. Preserve simulated versus experimental fidelity; simulated data can support training only under an explicit experiment and cannot become experimental validation labels.

Report point error, uncertainty calibration, interval width, domain coverage and performance near decision thresholds. Evaluate uncertainty under withheld chemical families. A confident out-of-domain prediction is not a reason to promote a candidate.

For joint constraints, avoid multiplying marginal probabilities unless independence is supported. Multi-task models may learn cross-property dependence; they still require calibration and complete reporting of unavailable endpoints. Missing evidence remains a distinct issue from predictive variance.

Optional physics-assisted models can learn residual errors around a physical baseline. Compare this against a data-only model using the same training information. Store every model's property coverage, supported chemistry, condition domain and abstention rule.

For initial benchmark promotion, freeze a `metric_contract` before revealing holdout labels. It contains the endpoint and scale, primary loss, group weighting, baseline selection rule, decision tolerance, uncertainty target, minimum effective test size and treatment of missing/censored labels. Default comparisons use MAE for saturation temperature and density, and absolute log error for positive viscosity/vapor-pressure endpoints. Choose the primary endpoint on training/coverage information, not holdout performance.

**Proposed research thresholds:** require at least 30 independent held-out substance/family groups for an endpoint-level comparative claim; fewer groups yields exploratory evidence only. Require at least 10% reduction in the predeclared primary loss versus the strongest baseline selected on development data, and a paired group-bootstrap 95% interval whose lower bound for relative improvement is greater than zero. Use at least 1,000 group resamples and retain the seed. This is a promotion rule, not a promised attainable accuracy or a universal sample-size theorem. Zero baseline loss makes relative improvement undefined; retain the baseline and report the model comparison accordingly.

Independently of relative gain, a model used to resolve a two-sided temperature window of width W must achieve held-out MAE no greater than W/4. For the proposed 10 K exploration window this is 2.5 K. Absolute requirements for other endpoints must be justified and frozen from decision sensitivity before promotion. A model failing this criterion may still support broad prioritization under an explicitly weaker use, but cannot be presented as resolving that narrow window.

For nominal 90% prediction intervals, report group-weighted coverage and its confidence interval, median width and threshold-region coverage. Proposed usability check: the coverage interval contains 0.90, observed coverage is at least 0.80, and interval width meets the frozen decision-tolerance rule. Passing a broad coverage interval with uninformatively wide predictions is insufficient. A finite-sample interval claim is limited to its calibration domain; abstention remains required outside it. Conservative bounds and uncalibrated intervals must be labelled as such.

For a provisional temperature-window screen, require the calibrated prediction interval to fall inside the window; overlapping intervals are UNKNOWN. This does not replace measured evidence for qualification. Treat ordinal synthetic-accessibility scores as rankings, not synthesis probabilities or supplier quotations.

Global accuracy is insufficient when the useful region is narrow. Define a threshold-neighborhood from the profile and development data before holdout access, then report local error, interval width, false-pass/false-reject rates and sample/group counts there. If that neighborhood is too sparsely measured, the model remains unvalidated for boundary decisions even if its global promotion criteria pass. Report joint feasibility only for the subset with supported joint evidence; label it `modeled_subset_feasibility`, never full qualification probability.

An applicability rule includes chemical-feature distance or coverage, property and condition domain, supported atom types and model training lineage. Choose cutoffs on training/calibration data. Compare any multi-task model against independent property models under the same labels; learning dependence is a hypothesis, not an automatic cure for false positives. Pretrained models require training-data overlap disclosure where knowable; unknowable overlap limits novelty/holdout claims.

## 11. Benchmark and leakage controls

Freeze training, calibration and holdout assignments before final model selection. Group repeated measurements and related identities so the holdout does not merely contain another temperature from a training molecule. Include a chemical-family challenge split in addition to an interpolation assessment.

Use training-only preprocessing and hyperparameter selection. Keep final holdout labels unavailable to the selection workflow until predictions and candidate rankings have been committed. Record all model attempts and selection decisions.

Evaluate each property, the constraints that consume it and the downstream ranking. Report sample counts, independent chemical-group counts, error distributions, subgroup failures and uncertainty. Compare against physical and simple statistical baselines. Report intervals around performance differences.

For sequential-policy testing, use a replay dataset whose hidden measurements are revealed only when the policy requests them. Equalize starting data, candidate universe, available measurements and resource budget across policies. Replay cannot validate properties absent from the hidden dataset or establish a discovery of new chemistry.

Prospective performance is assessed separately using experiments conducted after policy selection. A small pilot may establish feasibility without supporting a claim of superiority.

Assign observation lineage groups before splitting: all repeated observations from the same substance/sample lineage, source republications and explicitly linked duplicates travel together. Evaluate a substance-disjoint split and a separate family-disjoint challenge. For acyclic chemistry, define family/grouping rules from functional groups, connectivity/branching and homology; do not use an empty ring scaffold as a meaningful family label. Record connected-group sizes and report when grouping leaves too few independent groups. Do not weaken grouping just to meet a sample-count target.

Keep train, calibration, development and final challenge roles distinguishable. Hyperparameter tuning, missing-feature treatment, descriptor selection, transform fitting and uncertainty calibration cannot access final challenge labels. Censored targets require an appropriate declared loss/likelihood or exclusion from that endpoint's point-error metric with explicit coverage reporting. Do not treat censoring thresholds as exact labels.

The replay policy test starts with a frozen candidate pool and measured hidden outcomes. Missing or censored outcomes restrict the supported endpoint; do not fill the replay oracle with the model being evaluated. Compare each policy on the same paired starting splits and budgets, using 30 paired replay initializations where coverage permits. Such repeated seeds estimate policy variability within that finite panel, not 30 independent laboratory discoveries. Report performance after each resource increment and include failed/unsuccessful actions in cost.

The default replay primary endpoint is confirmed feasible-candidate count at the terminal budget for an explicitly modelable subset of the full profile. Predeclare its minimum useful gain; proposed default is 20% relative gain over the strongest development-selected baseline with a positive paired 95% interval. If baseline count is zero, relative gain is undefined: use a predeclared absolute gain threshold and report both counts. Ties and zero discoveries are informative outcomes. Any Pareto/hypervolume endpoint is secondary unless it was selected and scaled before evaluation; its reference point must not move after outcomes appear.

Before a prospective comparative trial, perform a power/precision assessment using pilot variability, feasible event rates, the minimum worthwhile gain and actual costs. If the available budget cannot discriminate the desired effect, classify the work as a discovery/measurement pilot and prohibit a superiority claim. Adaptive arms must be evaluated under a predeclared trial design; repeated within-candidate measurements do not substitute for independent candidate-level evidence.

Holdout manifests are read-only to the modeling/selection jobs. The evaluation runner can resolve hidden labels but returns them only according to the frozen protocol. Persist the committed prediction hash and the reveal event. Development evaluators and final challenge evaluators are separate entry points. Audit descendants as well as direct observations for leakage. A source correction invalidates affected split assumptions and produces a new benchmark version.

Policy comparisons report both `subset_feasible_count` and `fully_qualified_count` where the latter is actually measurable. A replay with only boiling/viscosity labels must never report a fully qualified coolant count. Failed measurement requests, absent labels and censored results follow the frozen oracle rules; dropping difficult candidates after selection is forbidden. Report known reporting/availability bias in any complete-case replay panel.

## 12. External calculations and compute control

Use external calculations when their expected decision value warrants their cost. Each engine declares supported properties, chemistry, methods, operating systems, required licences and validated domains. Record failures and nonconvergence as failures.

COSMO-RS is a candidate for liquid/mixture thermodynamics. Its fast pure-property predictor and its thermodynamic calculations are distinct capabilities. Parameterization and supported chemistry must be checked independently. PySCF/GPU4PySCF is an optional electronic-structure route; a successful energy calculation does not establish a fluid property.

The Wolfram QuantumChemistry paclet may be investigated, but it is not a mandatory dependency for the minimum useful release. Pin and benchmark any adopted package. Do not assume that one engine's output format or quantum method is compatible with another engine's parametrization.

Every job records a request, budget, environment, inputs, engine settings, result status and raw output references. Cache only results produced under matching conditions and settings. Support cancellation, checkpointing where the engine supports it and bounded retries for transient failures. Do not retry deterministic unsupported-method errors.

Start without custom CUDA. GPU usage must be justified by a representative CPU/GPU comparison including transfer overhead, numerical differences, memory use and supported methods. Absence of a GPU must not block the data-ingestion and baseline workflow.

Adapter capability probing is read-only and returns an availability status before submission. Jobs run only an allowlisted, pinned executable/library with a reviewed argument schema. The request specifies maximum wall time, memory, supported concurrency and estimated charge. Each external calculation has a new output directory and stored stdout/stderr references with sensitive fields redacted where necessary.

The cache key includes normalized identity, stereochemistry/conformer ensemble, geometry, phase/temperature/pressure/composition, calculation type, method/basis, parameter-set hash, engine/dependency version and the project schema/canonicalization version. A change to any relevant element produces a new request. Cache reuse cannot turn a failed or unvalidated result into a validated one.

For external jobs, distinguish prepared, submitted, running, completed, failed, cancelled and unknown states. A timeout of the client is not proof that the job stopped. Recover by querying the same job identity; do not submit a duplicate until nonexecution/termination is established. Reservation and actual research charges remain recorded even when no scientifically usable result returns. No external purchasing or laboratory submission is automated in the MUR.

## 13. Screening and constrained ranking

Screen in layers: identity/chemistry checks; observed hard failures; low-cost estimates; applicability checks; detailed calculations; proposed measurements. Every filter records its version and reason. Preserve candidates eliminated by uncertain predictions for later audit, separate from candidates with measured disqualifications.

The output contains a Pareto set over selected objectives, explicit hard-constraint states, uncertainty and evidence gaps. A large value on one objective cannot offset a hard failure. A prediction interval crossing a threshold does not count as a confirmed pass.

Distinguish a candidate suitable for additional evidence gathering from a candidate qualified for the application. The system may recommend testing an uncertain candidate if that experiment is feasible and informative. Ranking must explain the applicable profile and why a candidate was included, excluded or deferred.

Maintain a fixed baseline ranking for policy comparisons. An empty shortlist is a legitimate result with diagnostic evidence. Do not alter filters, reference points or objective weights after seeing outcomes without creating a new declared experiment.

Use three separate lists: measured hard failures, evidence-eligible candidates for bounded investigation, and candidates whose required qualification evidence is complete. For the investigation list, missing hard-endpoint data generates a required test action rather than a qualified pass. Direct measured failures cannot be overridden by a favorable model. Known assay/procurement infeasibility removes an action from the selectable set with a reason.

Keep a measurement ladder per candidate: (1) identity/composition and existing evidence; (2) a feasible test for a critical disqualifying condition; (3) targeted uncertain thermophysical properties; (4) qualified rig/material/lifecycle work. The scientific lead may alter the ladder with a recorded reason when information value justifies it. The optimizer cannot avoid an essential unmodeled constraint merely because predicting viscosity is cheaper.

## 14. Experiment-selection policy

The selection action is a candidate or formulation, a measurement or calculation, specified conditions and an evaluation fidelity. Its cost includes procurement, preparation, instrument time, analysis, compute and relevant setup costs. The policy selects useful actions rather than ranking molecules alone.

Begin with constrained Bayesian optimization or a transparent uncertainty/diversity policy. Compare against random eligible selection, a fixed physics-based shortlist and greedy predicted improvement. Prefer a small number of well-defined objectives. Unknown, experimentally required constraints remain explicit.

Select a batch under the agreed resource envelope. Account for shared preparation, instrument availability, pending measurements and duplicates. Where a full cost-aware multi-fidelity acquisition is too complex, implement and document a simpler policy first; do not claim an algorithm that was not implemented.

Each recommendation records model/profile versions, information available at selection time, estimated cost, rationale and rejected alternatives. Update only after experimental results are validated. Retain a replayable decision history and a controlled response to delayed or failed experiments.

Implement an action ledger separate from the AWF model-run ledger. `action_key` binds candidate/sample lineage, property/test, condition set, fidelity and protocol version; intentional replicates add a replicate identifier. State transitions are PROPOSED → RESERVED → SUBMITTED → RUNNING → COMPLETED, with FAILED/CANCELLED/UNKNOWN_OUTCOME branches and reconciliation events. A uniqueness check blocks accidental duplicate active actions. Exactly one writer updates the ledger through an atomic transaction or compare-and-swap equivalent.

Before admission, reserve the conservative expected charge and required shared setup/resource capacity. At settlement, record actual cost and reclaim only demonstrably unused reservation; unknown cost remains unresolved, not zero. Track policy-attributed comparison cost separately from actual invoiced campaign cost. Pending outcomes condition batch choice or are excluded conservatively; the implementation must disclose which policy it uses.

The first policy supports one test family/fidelity with fixed validated cost estimates and a finite candidate pool. Cost-aware multi-property and multi-fidelity selection is an extension after that policy is verified. An engine may use an explicit staged rule for disqualifying tests and Bayesian selection within the remaining pool; it must not claim general optimal value-of-information behavior from a heuristic ratio.

For every proposed batch, validate sum of reservations plus unresolved liabilities against the remaining envelope, prerequisites, instrument/resource slots, duplicate keys and eligible sample availability. Test changed budgets, pending failures, a late result and an empty action set. No feasible action produces a reasoned BLOCKED/STOP report rather than an infinite selection loop.

## 15. Laboratory interface and physical evidence

Define a laboratory interface before prospective work. The experiment request must specify sample identity, required quantity, preparation and conditioning, measurement methods, conditions, controls, uncertainty requirements, raw-data return format and stopping conditions. Chemical handling and apparatus operation remain with the experimental partner under its established procedures.

Begin with reference measurements and repeatability checks. Candidate testing should proceed from inexpensive disqualifying measurements to more demanding thermal, electrical and materials evaluations. Include reference fluids and blanks where meaningful; randomize or block measurement order to reduce drift and batch confounding.

For two-phase testing, record heater geometry and surface history, fluid charge, pressure, temperatures, heat input, heat losses, fluid level and boiling regime. Evaluate heat removal and operating margin in the defined apparatus. A boiling point or calorimetry result alone does not validate a heat-transfer advantage.

For compatibility, test actual relevant material grades and record immersion, vapor and condensate exposure where applicable. Track extracted contaminants, deposits and changes in electrical and thermal performance after exposure. For blends, analyze prepared and post-cycle composition.

Reject or quarantine results with ambiguous sample mapping, failed controls, missing method context or unreadable raw data. Preserve deviations; do not delete an inconvenient result. Publish qualified outcomes only for the tested samples and profile.

A first pilot may use a small candidate batch (illustratively 6–12, plus the controls and repeats dictated by the laboratory protocol). Its purpose is to establish measurement feasibility, model error and candidate behavior. The exact batch is chosen from cost/capacity evidence; the number alone does not justify an efficacy claim. If no laboratory is available, ship an honest offline release and an experiment-ready exchange package, leaving physical outcomes pending.

Resolve the protocol before requesting tests: endpoint-specific repeat count, independent batches where relevant, calibrated instrument range, uncertainty budget, detection/reporting limits, conditioning, blinding/randomization where feasible, control acceptance limits, and treatment of nonconvergence or sample loss. Predefine stopping conditions for the apparatus and which results remain usable after a deviation. Record physical preparation and instrument settings with each result.

The trial design must state whether experimental arms share newly acquired observations. Default comparison: identical initial information, then separate policy histories until the predeclared analysis point; common controls may be shared according to a fixed rule. If measurements are physically shared to save money, retain each arm's information-access timestamps and assigned counterfactual cost under the frozen rule. Report actual aggregate expenditure separately. Do not count shared measurements as independent replications.

A chemistry/experimental specialist must review the prospective protocol and the adequacy of its endpoints. A statistical specialist must review any claim of policy superiority, including adaptive allocation, stopping rules, clustered outcomes, multiple endpoints and missing results. Bootstrap over repeated seeds in a finite replay is not the confidence interval for an adaptive prospective campaign.

Physical-experiment tickets have two deliverables: a versioned request/protocol package and, after execution, validated observations plus analysis. Merging the request package does not close the physical measurement obligation. Record that obligation as a separate dependent ticket or owner-closure condition so the workflow cannot confuse a code merge with a laboratory result.

## 16. Gates, budgets and stop rules

Research gates are decisions about evidence and scope; they are separate from AWF's software lifecycle gates. The following dependency order removes circular setup prerequisites.

| Gate | Required evidence | Outcome and permitted next step |
|---|---|---|
| G0A Planning baseline | Research profile, role responsibilities, AWF 1.9.1 source pin, initial requirements and explicit unknowns | Begin the runtime/contract skeleton and laboratory feasibility planning |
| G0B Runtime readiness | Headless fixture, initial schema contracts, observed runtime/licence and AWF adoption/conformance evidence for the target project | Dispatch dependent implementation under the actual authorized mode |
| G1 Data/feasibility | Coverage report, curated panel, physical baselines and documented conflicts/gaps | Build endpoint models with sufficient data; commission only separately ready measurements; stop or narrow unsupported lanes |
| G2 Endpoint/model promotion | Frozen metric contract, valid grouped tests, useful accuracy/calibration and benchmark evidence | Enable only validated endpoint/domain predictions in screening; weak models remain exploratory |
| G3 Policy/campaign readiness | Fair replay evidence or a declared pilot-only decision, CAMPAIGN_READY profile, laboratory protocol and resource envelope | Begin the bounded prospective campaign or pilot under its stated claim limits |
| G4 Prospective evidence | Controlled observations, actual costs, deviations and the predeclared analysis | Candidate-specific development, inconclusive continuation proposal, or research stop |
| G5 Research handoff | Reproducible outputs, traceability, independent implementation review and open-decision register | Close the delivered research milestone; product qualification remains separately scoped |

G0B requires the AWF state and mode appropriate to the actual action. Missing remote rules do not block local adoption; live modes retain the prerequisites in AWF's runbooks. No scientific gate permits bypassing a workflow boundary.

Create two resource records: (a) AWF model-run/token/monetary accounting, governed by the installed workflow; (b) research compute, procurement, preparation, instrument and analysis budgets. Units, reservation estimates, actual charges, failed work and currency/date for quotations remain explicit. A null research budget means NOT_AUTHORIZED_FOR_SPEND; a zero budget prohibits spend. Do not infer AWF 1.9.2 token-only behavior for 1.9.1.

Milestone M0 is a bounded feasibility and runtime spike. M1 is the offline minimum useful release. M2 adds warranted external calculations and validated sequential selection. M3 is the separately resourced laboratory pilot/comparison. M4 is a decision package. Optional synthesis, RL, learned potentials and equipment deployment are outside those commitments unless a later milestone is explicitly accepted.

Stop or narrow a lane if critical measurements cannot be obtained, evidence indicates conflicting requirements, promoted models do not improve the declared decision, or the remaining campaign exceeds its resource envelope. Record a STOP_DOMAIN, INCONCLUSIVE or CONTINUE decision with the tested domain and remaining uncertainty. Do not describe a bounded unsuccessful search as proof that no coolant exists. Stop optional complexity when the simple baseline is already the better supported decision rule.

No calendar or monetary estimate is represented as a quote. E00/E10 must obtain workload timings, procurement/measurement lead times and quotations before committing milestone dates or expenditure.

## 17. Requirements and verification catalogue

The requirements below are normative for the proposed software/research system. Their acceptance criteria verify behavior and evidence production; they do not demand a favorable scientific result. Each requirement belongs to an epic and must be linked to one or more implementation or research tickets.

### FDE-E00 — Profile, ownership and AWF baseline

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-GOV-001 | Freeze an explicit application profile | Profile records every hard constraint, units, conditions, evidence rule and decision owner; proposed values are distinguishable. |
| FDE-GOV-002 | Verify the controlling AWF | Target-project conformance references the inspected 1.9.1 commit/manifest, actual installation state and revision-3 schema; it does not claim live readiness from documentation. |
| FDE-GOV-003 | Separate engineering and scientific outcomes | A negative or inconclusive research fixture closes with an honest research outcome and cannot be labeled qualified fluid. |
| FDE-GOV-004 | Record responsibilities and resource limits | Responsibility and resource records identify accountable roles and unresolved assignments; expenditure-dependent actions require a defined envelope. |

### FDE-E01 — Runtime, contracts and reproducible skeleton

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-RUN-001 | Run core workflows without notebook state | A fresh headless process executes the pinned fixture and produces its expected outputs without opening a notebook. |
| FDE-RUN-002 | Validate all inter-component contracts | Malformed, missing-version and wrong-unit payloads are rejected with machine-readable reason codes. |
| FDE-RUN-003 | Capture execution provenance | Each completed run links its code, configuration, data, dependencies and outputs through verifiable hashes. |
| FDE-RUN-004 | Separate optional capability availability | Missing external software produces an unavailable-capability result while the offline core fixture remains runnable. |
| FDE-RUN-005 | Implement cross-runtime operation envelopes | Golden request/response fixtures agree across Wolfram and Python, reject malformed/status-inconsistent payloads and propagate required-check failures. |

### FDE-E02 — Source acquisition and measurement curation

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-DATA-001 | Preserve source provenance | Every accepted observation resolves to an original source record and locator; untraceable inputs are quarantined. |
| FDE-DATA-002 | Preserve measurement semantics | Fixtures distinguish pressure basis, temperature, frequency, phase, composition basis, uncertainty and censoring. |
| FDE-DATA-003 | Deduplicate without destroying conflicting evidence | Republished measurements are grouped; disagreeing observations remain individually addressable with reconciliation history. |
| FDE-DATA-004 | Keep evidence classes separate | Measured, derived, simulated, predicted and extracted-unverified records cannot be silently interchanged. |
| FDE-DATA-005 | Review machine-extracted evidence | An extraction without a verifiable locator or with wrong units cannot enter the accepted training snapshot. |
| FDE-DATA-006 | Audit data coverage and exclusions | Report independent identities and sources by property/condition/family, with every excluded record and reason retained. |
| FDE-DATA-007 | Preserve transitive lineage and corrections | A corrected or derived observation updates dependent-staleness reports; seeded target-derived features and republished labels cannot leak into the holdout. |

### FDE-E03 — Chemical identity and descriptor pipeline

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-CHEM-001 | Version chemical normalization | Stereo, salt, tautomer, fragment and ambiguous-product fixtures follow the declared policy and retain original identities. |
| FDE-CHEM-002 | Represent samples and formulations | Component ordering is canonicalized; mass and mole fractions remain distinguishable; sample batches retain separate identities. |
| FDE-CHEM-003 | Version descriptors and capabilities | Feature schemas and tool versions are fixed; unsupported structures and failed calculations yield explicit nonnumeric states. |
| FDE-CHEM-004 | Freeze eligible candidate universes | Candidate snapshots contain availability/novelty status and provenance; comparisons use the same declared universe. |

### FDE-E04 — Thermodynamic baselines and feasibility

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-PHYS-001 | Implement a physical reference baseline | Reference calculations reproduce independently specified fixtures within declared tolerances and label out-of-range evaluations. |
| FDE-PHYS-002 | Evaluate the feasible region | Report constraint conflicts, missing evidence and observed trade-offs without silently relaxing the target. |
| FDE-PHYS-003 | Model mixture phase behavior explicitly | Core schemas/rejection fixtures distinguish mixtures correctly; enabling the conditional MIX lane additionally requires validated bubble/dew, composition and phase checks. |
| FDE-PHYS-004 | Preserve system-dependent endpoints | Thermal and electrical performance records include required rig/method context; unsupported proxy substitutions are rejected. |

### FDE-E05 — Benchmark and split infrastructure

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-VAL-001 | Prevent correlated-label leakage | Split audit detects overlap in substances, measurement groups and protected chemical families according to the declared test. |
| FDE-VAL-002 | Freeze information available to evaluation | Predictions and rankings are committed before holdout disclosure; post-disclosure changes require a new evaluation version. |
| FDE-VAL-003 | Compare valid baselines | The predeclared metric contract, grouped evaluation and uncertainty meet section 10 promotion rules or return a bounded negative/inconclusive decision. |
| FDE-VAL-004 | Replay sequential policies honestly | Replay reveals only requested hidden observations and charges specified costs; unavailable endpoints remain unavailable. |
| FDE-VAL-005 | Report inconclusive evaluations | Insufficient coverage or precision yields INCONCLUSIVE with reasons rather than a numerical pass by default. |

### FDE-E06 — Predictive models and uncertainty

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-ML-001 | Train reproducible baseline property models | Training runs produce model artifacts, model cards, selected hyperparameters and reproducible evaluation outputs. |
| FDE-ML-002 | Condition predictions on physical context | Requests with unsupported temperature/pressure/phase return an explicit applicability result rather than unqualified values. |
| FDE-ML-003 | Calibrate uncertainty and abstention | Report interval coverage and width on declared chemical-group holdouts and demonstrate abstention on out-of-domain fixtures. |
| FDE-ML-004 | Handle joint constraints and missing properties | Correlated-property fixtures cannot be evaluated by an undeclared independence assumption; unavailable endpoints remain unknown. |
| FDE-ML-005 | Compare physics-assisted learning fairly | An ablation separates the effect of extra information from the effect of the learning method and reports negative results. |

### FDE-E07 — External calculation adapters

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-SIM-001 | Declare engine capabilities and requirements | Adapter reports supported chemistry/methods/versions and required runtime/licence; unsupported requests fail before expensive execution. |
| FDE-SIM-002 | Validate calculations against references | Each enabled property/method has a reference comparison and convergence checks; single-molecule energy is not relabeled as a liquid property. |
| FDE-SIM-003 | Bound computation and handle failures | Timeout, nonconvergence, cancellation and deterministic unsupported-method fixtures terminate visibly without unbounded retries. |
| FDE-SIM-004 | Avoid invalid cross-engine reuse | Cache and interoperability checks reject mismatched method, geometry, temperature, parameterization or engine version. |

### FDE-E08 — Constraint screening and candidate dossiers

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-SCR-001 | Evaluate hard constraints without compensation | One hard failure cannot be offset by favorable objectives; an unknown hard endpoint cannot count as a confirmed pass. |
| FDE-SCR-002 | Maintain traceable screening decisions | Every included, rejected and deferred candidate has profile/filter versions, reasons and evidence references. |
| FDE-SCR-003 | Generate interpretable trade-off sets | Report objective directions, conditions, uncertainty and nondominated candidates; empty feasible sets remain valid outputs. |
| FDE-SCR-004 | Separate exploration from qualification | A candidate proposed for learning is visibly distinguished from one with sufficient physical evidence for the profile. |

### FDE-E09 — Sequential experiment selection

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-AL-001 | Select measurement actions under cost | A proposal identifies candidate, test, conditions, fidelity, prerequisites and estimated resource consumption. |
| FDE-AL-002 | Compare sequential selection policies | Run equal-information/equal-budget comparisons against random, fixed physical ranking and greedy alternatives. |
| FDE-AL-003 | Respect batching and pending work | Pending or completed equivalent actions are not accidentally purchased twice; setup and availability constraints are enforced. |
| FDE-AL-004 | Reproduce the selection history | A decision can be regenerated from its recorded information snapshot, seed, policy, profile and pending-action state. |
| FDE-AL-005 | Account for actions and unknown outcomes | Duplicate active actions are rejected, unknown submissions are reconciled without resubmission and reservations/actual charges remain consistent under interruption. |

### FDE-E10 — Laboratory protocol and result exchange

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-LAB-001 | Specify executable measurement requests | Requests contain sample IDs, methods, conditions, controls, quantities, raw-data requirements and return schemas. |
| FDE-LAB-002 | Validate experimental intake | Unknown sample IDs, failed controls and missing raw-data references are quarantined with visible reason codes. |
| FDE-LAB-003 | Characterize relevant failure mechanisms | Protocols cover thermal/electrical performance, relevant materials exposure and composition changes for the activated lane. |
| FDE-LAB-004 | Preserve protocol deviations and outcomes | Failed or deviating tests remain in the experiment register; inclusion/exclusion decisions are explicit. |

### FDE-E11 — Prospective experimental campaign

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-EXP-001 | Freeze prospective comparison design | Campaign protocol freezes endpoints, information sharing, budget and a power/precision assessment; an underpowered pilot is labelled exploratory. |
| FDE-EXP-002 | Track actual experiment resources | Report costs, failures, elapsed time and completed measurements for every arm, including unsuccessful procurement. |
| FDE-EXP-003 | Evaluate prospective scientific outcomes | Final campaign report distinguishes discovery, improvement, no demonstrated advantage and inconclusive results. |

### FDE-E12 — Research decisions and reporting

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-REP-001 | Produce candidate evidence dossiers | Each dossier resolves every material claim to measured, calculated or predicted evidence with conditions and gaps. |
| FDE-REP-002 | Produce gate decisions with rationale | A gate report states pass/stop/inconclusive, evidence, applicable scope and unresolved dependencies. |
| FDE-REP-003 | Create reproducible research exports | Markdown and JSON outputs agree on candidate IDs, constraints, metrics and scientific status. |

### FDE-E13 — Conditional advanced methods

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-EXT-001 | Gate generative and RL extensions | An extension proposal names the validated scorer, bounded chemistry/action space, baseline and experimental validation plan. |
| FDE-EXT-002 | Gate learned simulation extensions | An ML-potential/custom-acceleration proposal identifies a measured bottleneck, domain, reference checks and cost-benefit test. |

### FDE-E14 — Reproducible release and handoff

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-REL-001 | Package independent rerun evidence | A second clean environment runs the declared reference workflow from pinned inputs and records agreement or documented limitations. |
| FDE-REL-002 | Complete requirements-to-evidence traceability | Every core requirement maps to tickets, artifacts and verification evidence or a visible blocked/deferred disposition. |
| FDE-REL-003 | Prepare AWF handoff without bypassing approval | Handoff identifies actual instruction baseline, revision-specific review evidence and owner merge status without manufacturing authorization. |
| FDE-REL-004 | Verify artifact recovery and scientific claims | A restored decision resolves its required artifacts/hashes; missing physical evidence or inaccessible dependencies cannot be presented as a qualified or publicly reproducible result. |


## 18. Proposed Jira epic structure

| Epic | Deliverable | Dependencies | Gate |
|---|---|---|---|
| FDE-E00 | Profile, ownership and AWF baseline | None | G0 |
| FDE-E01 | Runtime, contracts and reproducible skeleton | FDE-E00 | G0 |
| FDE-E02 | Source acquisition and measurement curation | FDE-E01 | G1 |
| FDE-E03 | Chemical identity and descriptor pipeline | FDE-E01 | G1 |
| FDE-E04 | Thermodynamic baselines and feasibility | FDE-E02, FDE-E03 | G1 |
| FDE-E05 | Benchmark and split infrastructure | FDE-E02, FDE-E03 | G2 |
| FDE-E06 | Predictive models and uncertainty | FDE-E04, FDE-E05 | G2 |
| FDE-E07 | External calculation adapters | FDE-E01, FDE-E03, FDE-E04 | G2 |
| FDE-E08 | Constraint screening and candidate dossiers | FDE-E04, FDE-E06 | G2 |
| FDE-E09 | Sequential experiment selection | FDE-E05, FDE-E08 | G3 |
| FDE-E10 | Laboratory protocol and result exchange | FDE-E00, FDE-E01 | G3 |
| FDE-E11 | Prospective experimental campaign | FDE-E09, FDE-E10 | G4 |
| FDE-E12 | Research decisions and reporting | FDE-E08, FDE-E11 | G5 |
| FDE-E13 | Conditional advanced methods | FDE-E06, FDE-E09 | EXTENSION |
| FDE-E14 | Reproducible release and handoff | FDE-E12 | G5 |

Use these epic IDs as stable external references when creating Jira issues. Preserve the reference in issue metadata or a consistent description field. Dependencies are logical prerequisites, not assumed Jira workflow transitions. Detailed work items must be small enough for one accountable worker and an independent review.

Parallel work is appropriate only after shared contracts are frozen. Evidence ingestion and chemistry features can proceed independently once identities and observation envelopes are agreed. Laboratory protocol design may proceed alongside modeling; actual campaign execution depends on its evidence and resource gates. Avoid assigning multiple workers ownership of the same mutable schema.

E07 is an optional capability provider and is deliberately not an unconditional prerequisite of E08. Baseline screening and the MUR can use measured data and promoted models without COSMO-RS or quantum chemistry. A ticket that requests an external property adds the exact validated adapter ticket as its dependency. E13 is excluded from core release acceptance. E10's protocol/interface work may start after G0A and the relevant schemas; it need not wait for AI success.

## 19. Ticket and AWF 1.9.1 execution contract

The requested compatibility baseline is [jkinlay/agentic-workflow-framework](https://github.com/jkinlay/agentic-workflow-framework), **1.9.1**, at repository-recorded source commit `e7d80a691e2ae0a0b55e54f4e5e91e95e5ca7fe5`. The retrieved `MANIFEST.json` hashes to `d10a180af0109ffda59f70d925dd934c8fb78d9a8016d7ca39086d715f1194bd`. The repository's later upgrade-fixture index identifies that source as its 1.9.1 reference. This is a pinned compatibility target, not a claim that 1.9.1 is the latest release. Inspection also observed a 1.9.2 published release and main documenting 1.9.3; their behavior is not imported into this specification.

The actual 1.9.1 specification, AGENTS instructions, ticket schema/template, lifecycle, native coordination, adoption, routing, operating configuration and review/closeout runbooks were read. The former v1.41 overlay is superseded for this task. Retrieval and local hashing establish inspected source identity, not successful AWF installation, project adoption or live qualification.

**Contract generation must use the retrieved revision-3 schema.** Its fields are `schema_version`, `contract_id`, `contract_version`, `created_at`, `project_id`, `repository_id`, `issue_id`, `ticket`, `requirements_hash`, `policy_hash`, `objective`, `acceptance_criteria`, `dependencies`, `branch_origin_sha`, `target_base_branch`, `scope`, `validation`, `risk_flags`, `specialist_domains`, `disposition`, `risk_tier`, `tier_justification`, `closure_standard`, `owner_closure_required` and `corrects`. The schema's historical `$id` contains AWF 1.2; that is not permission to alter it or set the schema revision to 1.9.1.

Every acceptance criterion supplies `id`, `text` and `validation`. Scope contains expected paths, allowed adjacent paths, protected interfaces, forbidden changes, governance-change authorization and evidence paths. Validation declares actual commands, cases, resources, justified non-applicability and any tested platform distinction. Runtime contracts must not contain placeholder UUIDs, repository IDs, SHAs, hash values or Jira keys. Draft planning records stay distinct from executable contracts.

Dependencies in the AWF contract carry observed issue identity, `kind` from `code | deployment | migration | environment`, `direction: requires`, satisfaction and evidence. They are ticket dependencies; an epic being present does not prove its deliverable is available. Map laboratory/resource dependencies to environment records tied to actual evidence and retain scientific prerequisite details in the project record. A READY contract requires satisfied dependencies with evidence.

Use risk Tier 2 for uncertain/scientific-decision, schema, orchestration or resource-accounting work unless the installed policy and actual paths support a less restrictive classification. Tier 1 eligibility is derived under reviewed configuration. Freeze `closure_standard` (FULL or DECLARED_LIMITATIONS) before review; a nonpositive research result can satisfy a FULL analysis contract, but an unexecuted laboratory test cannot. Explicitly attributed limitations are required for DECLARED_LIMITATIONS.

AWF publication sequence is worker completion, scoped branch push and draft PR, observed branch/PR identities, current validation and requirements, observed draft clearance, critic review of the actual head, required specialist review, final gate, then owner authorization. READY_FOR_CRITIC and READY_FOR_OWNER_AUTHORIZATION are different states. Changed heads or bases invalidate affected evidence under the controlling policy. Do not adopt the later publisher-commit shortcut without a version-specific change.

Only the controller mirrors Jira lifecycle events. Worker start maps to In Progress; PR readiness to In Review; owner-requested changes or changed review head to In Progress; confirmed merge and valid closeout to Done, subject to owner-closure requirements. BLOCK/PARK do not trigger Jira status writes. Never transition Epics. Read before and after writes; mismatches or unknown outcomes stop further writes to that ticket without reissuing the action. The reference adapter itself is not evidence that live Jira writing is enabled.

Native planning defaults to three implementation streams with an independent reviewer per stream, inside the configured ceiling and actual host capacity. Do not assume all those agents exist. Keep one writer per ticket/path, explicit resource leases and separate reviewer contexts. Runtime choices come from accepted project configuration, not model names hard-coded in this specification.

Reserve protected run budgets before dispatch and settle observed usage. AWF 1.9.1 has effective monetary ceilings when configured; unknown actual cost is not zero. If the chosen host cannot supply/enforce required accounting, report that mode unavailable and use an allowed reference/manual mode or a separately reviewed workflow upgrade. Do not disable the constraint to make the project run.

The normal amendment cap is governed by the installed policy; the inspected default is three. At the cap, present unresolved findings for the prescribed owner disposition; do not silently extend cycles or weaken closure. Serious findings must name a criterion or mandatory boundary. This document's three specification self-review cycles are drafting work, not independent AWF critic approvals, and do not consume a future implementation ticket's amendment allowance.

FDE adoption must preserve managed AWF bytes and project instructions through the supported mechanism, map real GitHub/Jira identities, supply a Wolfram-capable project test command and record actual INSTALLED/CONFIGURED/ACTIVE state. A fresh project may remain Jira-disabled with provisional local IDs. No ticket or this document grants merge authority, live adapter enrollment or approval to modify governance.

## 20. Reproducibility, quality and operational behavior

Pin runtime and dependency versions and preserve an environment manifest for every benchmark and release. Separate an offline deterministic fixture suite from network-dependent integrations and physical experiments. A mock adapter proves orchestration behavior only.

Use content-addressed run manifests, fixed random seeds where applicable and explicit numerical tolerances. Where engines are nondeterministic, test scientific agreement within declared tolerances rather than promising identical floating-point bytes. Record hardware and backend when results depend on them.

Test failures deliberately: invalid units, duplicate identities, ambiguous mixtures, missing conditions, censored observations, unsupported chemistry, unavailable licence, nonconvergence, timeout, empty shortlist, interrupted batch and missing evidence. Ensure errors are visible and cannot be promoted to scientific success.

Keep API credentials out of reports, repositories and generated command strings. Limit external transmissions to necessary inputs under the project's data policy. Log action identity and timestamps without exposing secrets.

The first release should be operable by a second researcher from the documentation and pinned inputs. Include startup, normal operation, failure recovery, schema migration, rerun and deactivation instructions.

Require three explicit verification layers: (a) deterministic software fixtures, (b) scientific golden/reference comparisons with provenance and tolerances, and (c) live licensed/data/laboratory integrations where the release claims them. Store counts for discovered/executed tests, declared skips, unavailable capabilities and unevaluable files. Required unexecuted work cannot pass. AWF's local/CI parity requirements apply to the actual selected checks; a valid platform distinction needs its required regression evidence.

Acceptance failure injections include Celsius interpreted as Kelvin; absolute/gauge confusion; duplicate-source leakage; a target-derived descriptor; mixture composition reversal; missing dielectric frequency; failed solvent parameterization; a point estimate with a wide interval; an unobserved action result; invalid sample/batch mapping; changed profile after ranking; and a revised source that should invalidate a report. Use independently specified expectations rather than tests that merely duplicate the implementation.

Every run manifest lists artifact role, relative/controlled location, byte size, SHA-256, schema, producer, dependencies and retention/access class. Validate references at report generation and at release. Restoration from backup must recover at least one complete historical decision and its inputs; inaccessible licensed data require a documented access dependency, not a claim of public reproducibility.

Before scaling, benchmark ingestion, feature generation and prediction on the declared MUR workload, measuring wall time, peak RAM, output size and failure counts on the selected host. Set explicit thresholds in E01 after the first capability measurement and before choosing optimizations; report hardware with results. Failure to meet a performance target must not change scientific outputs silently. Do not train a molecular foundation model or build a new scheduler to solve an unmeasured bottleneck.

## 21. Decisions, risks and unresolved dependencies

| ID | Decision or risk | Owner role | Required resolution |
|---|---|---|---|
| D01 | Application and chemistry boundaries remain proposed | Project owner + chemistry/thermal leads | Freeze research profile; resolve campaign/qualification fields before dependent actions |
| D02 | Target-project AWF adoption not yet performed | Project owner + workflow controller | Use the inspected 1.9.1 source pin; verify target installation, configured policy and mode |
| D03 | Wolfram runtime and CI licence unverified | Engineering lead | Demonstrate headless execution on selected environment |
| D04 | Critical data may be sparse or biased | Data/science lead | Coverage audit and explicit experiment-backed gaps |
| D05 | Laboratory access and test costs unverified | Experimental lead | Obtain feasible measurement plan and capacity |
| D06 | Low boiling, electrical and fire constraints may conflict | Chemistry/thermal leads | Feasibility evidence and lane decision |
| D07 | Molecular novelty may exceed model domain | Modeling lead | Abstention and targeted evidence strategy |
| D08 | Mixture fractionation may erase predicted benefits | Thermodynamics lead | Composition and cycling evaluation |
| D09 | External engine licensing and methods may constrain scale | Engineering/science leads | Capability/cost benchmark and fallback |
| D10 | Experimental failures could bias the observed dataset | Experimental/modeling leads | Retain failure outcomes and selection histories |

Unresolved decisions block only their dependent work. Schema design and an offline fixture workflow can proceed while laboratory procurement is unresolved. Do not convert missing information into invented operating limits, prices or available resources.

## 22. Deliverables and release acceptance

Deliver versioned profiles, source and measurement catalogues, chemistry/feature schemas, physics baselines, benchmark datasets and splits, model artifacts/cards, external-engine adapters, candidate dossiers, selection histories, experiment exchange formats, prospective results and a final research decision report.

The release package must contain the implementation revision, environment manifest, input snapshot hashes, commands needed to reproduce the reference run, generated outputs, verification evidence, known limitations and issue traceability. It must explicitly state which capabilities were tested with real data, mocks, simulations or laboratory measurements.

A release can be accepted as an engineering research tool without declaring a successful fluid discovery. If no candidate meets the target, the final report must identify evidence-backed reasons, remaining uncertainties and whether further work has a justified objective.

## 23. Evidence basis and source register

Primary sources were checked on 28 September 2026. Documentation is a capability reference, not evidence of an installed runtime or successful execution. Standards and vendor documentation must be pinned again for the implementation baseline. Requirements, budgets and thresholds proposed in this specification are project design decisions unless explicitly identified as source facts.

| Source | Reference and use |
|---|---|
| S01 | [Wolfram molecular computation](https://reference.wolfram.com/language/guide/MolecularStructureAndComputation.html): molecule representation and structural operations |
| S02 | [MoleculeValue](https://reference.wolfram.com/language/ref/MoleculeValue.html): documented computed descriptors |
| S03 | [ChemicalData](https://reference.wolfram.com/language/ref/ChemicalData.html): lookup capability |
| S04 | [Predict](https://reference.wolfram.com/language/ref/Predict.html): baseline learning algorithms |
| S05 | [Python external evaluation](https://reference.wolfram.com/language/ref/externalevaluationsystem/Python.html) and [RunProcess](https://reference.wolfram.com/language/ref/RunProcess.html): external integration |
| S06 | [WolframScript](https://reference.wolfram.com/language/ref/program/wolframscript.html), [VerificationTest](https://reference.wolfram.com/language/ref/VerificationTest.html), [TestReport](https://reference.wolfram.com/language/ref/TestReport.html): headless execution and tests |
| S07 | [QuantumChemistry paclet](https://resources.wolframcloud.com/PacletRepository/resources/WolframChemistry/QuantumChemistry/): optional electronic-structure investigation |
| S08 | [NIST Chemistry WebBook](https://webbook.nist.gov/chemistry/): reference-property discovery |
| S09 | [NIST ThermoML](https://www.nist.gov/mml/acmd/trc/thermoml): structured experimental-property archive |
| S10 | [SCM pure-property predictor](https://www.scm.com/doc/COSMO-RS/Property_Prediction.html): property-specific limitations and supported chemistry |
| S11 | [COSMO-RS properties](https://www.scm.com/doc/COSMO-RS/Properties.html): phase/mixture calculations |
| S12 | [GPU4PySCF](https://pyscf.org/user/gpu.html): optional accelerated electronic structure |
| S13 | [BoTorch multi-objective documentation](https://botorch.org/docs/multi_objective) and [NEHVI paper](https://arxiv.org/abs/2105.08195): selection-policy implementation references |
| S14 | [GATE preprint](https://arxiv.org/html/2510.23371v2): related single-phase screening research; not two-phase product qualification |
| S15 | [OCP immersion project](https://www.opencompute.org/wiki/Cooling_Environments/Immersion): identify and obtain applicable dated specifications |
| S16 | [AWF 1.9.1 source](https://github.com/jkinlay/agentic-workflow-framework/tree/e7d80a691e2ae0a0b55e54f4e5e91e95e5ca7fe5): actual contracts and runbooks; source manifest independently hashed locally as recorded in section 19 |

Source-informed cautions: the fast SCM predictor has chemistry/domain limitations and errors that can exceed a narrow target window; its support cannot be generalized to all elements. The quantum paclet is an optional package requiring its own validation. GATE's example is single-phase screening with limited selected validation. These observations motivate benchmarking, explicit capability checks and physical evidence requirements; they do not imply that any chosen model will meet this project's accuracy goals.

## 24. Specification status

Version 0.3 incorporates red-team cycles 1 and 2. Interfaces, measurement semantics, leakage controls and resource recovery have been rewritten. The final review will test Jira/AWF decomposition, dependency completeness, scope realism and internal consistency.
