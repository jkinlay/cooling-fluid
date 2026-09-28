# Cooling Fluid Discovery — Project Specification

Version 1.1 · 28 September 2026 · Feasibility-first amendment after external review

## 01. Purpose and current commitment

Determine whether a cooling-fluid discovery project offers a scientifically plausible and economically useful opportunity before building its platform. Version 1.1 supersedes v1.0's recommended build sequence following the user-supplied external red-team review. The original detailed design is retained as a conditional engineering reference.

The immediate planning scope is M0: a bounded desk investigation of application requirements, known chemistry, hazard and deployment constraints, available evidence, buyer value and validation costs. No viable fluid, complete candidate census, customer demand, laboratory engagement or independent professional approval has been established by this specification.

Only after an explicit feasibility decision should the owner authorize an appropriately scoped M1 implementation. M1's default useful artifact is a reproducible evidence-curation and constraint-screening tool. Predictive ML, adaptive experiment selection, external simulation, novel synthesis and a physical campaign require separate evidence and activation; none is required to justify the first desk investigation.

The owner account is `jkinlay`; acceptance of the proposed capacity, study dates and spending limits remains pending. Chemistry and thermal reviewers and experimental providers are unassigned. A role name is not evidence that a person or partner exists. The application and runtime are undecided: two-phase immersion is one hypothesis, and Mathematica is one implementation option.

Keep engineering completion, research findings, commercial validation and physical candidate qualification as separate outcomes. STOP_DOMAIN and INCONCLUSIVE are valid study outcomes. A successful document or software build does not establish a viable market or qualified coolant.

Logical FDE IDs are planning identifiers, not Jira issues. This revision updates repository planning documents; it does not create issues, adopt AWF, authorize purchases/outreach, execute the study or approve a scientific gate. Read section 16 and [M0 study procedures](M0_Feasibility_Study.md) first, then the conditional design and section 19 AWF mapping.


## 02. Scope, assumptions and exclusions

M0 compares three first-class application alternatives: two-phase immersion, single-phase dielectric immersion, and two-phase direct-to-chip. Each has its own fluid-contact boundary, temperature/pressure conditions, fire/electrical constraints and customer/equipment context. None is the default winner. An application switch requires an explicit versioned decision and cannot be reported as success against the former profile.

Research lanes remain PURE (known compounds), MIX (formulations), NOVEL (unmade structures) and SYSTEM (fluid/pressure/equipment co-design). The desk study begins with bounded searches of known purchasable chemistry because these provide the cheapest feasibility evidence. MIX or NOVEL is activated only by a plausible hypothesis and a credible evidence path, not simply because PURE failed.

M0 may use spreadsheets, Mathematica notebooks or short Python scripts for traceable calculations and curation. It requires no application framework, database service, cross-runtime bridge, benchmark infrastructure or AWF installation. If agents execute M0 through AWF, the installed workflow's actual controls still apply; manual study work is not a bypass for governed agent execution.

After G0, the default minimum useful release (MUR/M1) ingests the selected evidence, normalizes identities/conditions/units, preserves provenance, evaluates PASS/FAIL/UNKNOWN constraints, produces candidate dossiers and exports a simple proposed next-measurement list. It can report an empty shortlist or unresolved evidence. It does not require training any model, proving AI superiority, two trainable endpoints, a laboratory campaign or a two-language implementation.

The searched universe and evidence density determine workload sizing. Record raw versus post-filter structures, independent substances, observations by condition and supported endpoints. The former 10,000-candidate/100,000-observation caps and 20–40 reference-panel target are withdrawn as planning requirements. Set measured capacity targets only after M0 and a small vertical slice; do not build distributed ingestion or GPU infrastructure for an unmeasured workload.

Conditional capabilities include ML and benchmark infrastructure (M2_MODEL), sequential-policy experiments (M2_POLICY), action execution/accounting (M2_ACTIONS), external calculations (M2_COMPUTE), funded physical experiments (M3), product qualification (M4) and MIX/NOVEL/SYSTEM extensions (EXT). Mixture identity and rejection behavior are supported when needed; mixture prediction is separately activated. Disabled capabilities must be explicit.

No autonomous laboratory, bespoke CUDA engine, molecular foundation model, multi-tenant application or production data-centre trial is included. Hardware, runtime licences, datasets and laboratories are not assumed available from other projects.


## 03. Application comparison and acceptance profiles

Before optimization, compare the following alternatives using explicit evidence. These are proposed investigation boundaries, not agreed product specifications.

| Profile | Initial question | Required differentiation |
|---|---|---|
| TP_IMMERSION_F0 | Is a fluorine-free dielectric fluid with an exploratory 45–55 °C normal boiling range useful and acceptable for a defined immersion system? | Direct equipment contact; operating/fault fire behavior; electrical and materials evidence; vapour management |
| SP_IMMERSION | Is there an unmet single-phase dielectric-fluid requirement with a credible improvement opportunity? | Operating range, viscosity/pumping losses, thermal performance, fire margin, ageing and materials; no automatic universal boiling threshold |
| TP_DIRECT_CHIP | Is there a useful two-phase cold-plate/closed-loop fluid problem? | Pressure envelope, cold-plate and seal materials, charge size, leakage/fault conditions, OEM requirements; do not inherit immersion requirements silently |

For each profile record the proposed buyer/use case, equipment boundary, operating and fault conditions, hard properties, units, method, threshold rationale, evidence class, measurement uncertainty, owner, and unresolved fields. Preserve the initial TP_IMMERSION_F0 profile even if another profile is selected.

Fire and deployment acceptability is a decision-critical M0 constraint. Maintain distinct entries for chemistry hazard, equipment conformity, applicable jurisdiction/adopted standard edition and clause, OEM procurement requirements, and insurer acceptance. A general reference to NFPA 75/76, an unadopted draft clause, or a vendor statement cannot establish a universal prohibition or acceptance. Record PASS, FAIL or UNKNOWN against the actual application. Unresolved mandatory acceptability prevents a claim of deployability and requires a bounded follow-up rather than broad platform investment.

Other hard requirements include breakdown strength, resistivity, permittivity/loss with conditions; relevant material compatibility; lifecycle stability and composition drift; supply, purity and price; and chemical/environmental constraints. Fluorine-free is a structural policy, not proof of safety, sustainability or regulatory acceptance. PFAS-free and fluorine-free are different claims and require explicit definitions. Sample-level analytical claims require a method and reporting limit.

Every hard constraint evaluates to PASS, FAIL or UNKNOWN. Unknown data cannot be counted as a pass. A measured hard failure cannot be compensated by a desirable thermal property. Distinguish investigated candidates, evidence-eligible candidates and physically qualified batches. Critical heat flux and heat-transfer performance require apparatus and surface context.

Profile states are RESEARCH_DRAFT, RESEARCH_FROZEN, CAMPAIGN_READY and QUALIFICATION_READY. A frozen research profile may explicitly contain bounded unknowns; it is not campaign permission. CAMPAIGN_READY needs named methods, sample amounts, provider capacity, funded limits and a reviewed protocol. QUALIFICATION_READY means the qualification specification is complete, not that a fluid passes it. A physical reference fluid must be characterized in the actual rig before comparative performance claims.

M1 must exercise two intentionally different, explicitly synthetic profile fixtures without changing the screening algorithm: one boiling-window profile and one single-phase temperature/viscosity/fire-constraint profile. Their values are software test inputs, not recommended engineering limits or a second completed research campaign.


## 04. Questions and hypothesis activation

H1 — Does a credible, useful region exist for a specified application, chemistry domain and evidence budget? Investigate through the M0 desk study before software. A bounded unsuccessful search is not a universal impossibility proof. A domain where all candidates have measured hard failures triggers STOP_DOMAIN for that domain/profile.

H2 — Can predictions improve an identified decision involving genuinely missing or costly information? Activate only after documenting the missing endpoint/condition, decision cost, baseline and usable training/evaluation evidence. Reliable existing measurements take precedence. Known purchasable substances may still have valuable evidence gaps; molecular novelty is not a prerequisite for useful prediction.

H3 — Can adaptive selection improve decisions at an equal resource budget? This is optional M2_POLICY research. A usable hidden-outcome panel, independent-unit definition, supported feasibility subset and power/precision assessment are prerequisites. M1 provides transparent fixed prioritization only.

H4 — Can external physical calculations add decision value beyond available evidence and simple baselines? Activate only with an identified gap and bounded cost.

H5 — Can a defined formulation or new-chemistry hypothesis improve the demonstrated frontier? Require a separate rationale, evidence plan and review; creating a new lane does not remove conflicting physical requirements.

Classify each activated hypothesis as supported, unsupported or inconclusive in its tested domain. Software acceptance must not depend on obtaining a favorable scientific finding. Retain failed tests and negative results.


## 05. Architecture and language boundary

This is conditional M1 design. Choose a primary runtime through FDE-RUN-006 after G0; no runtime has been selected. Compare Python core with optional Mathematica notebook client against Wolfram Language core with optional Python specialist adapters. Use a modular local application with reproducible batch operation; notebooks must not hide necessary state.

The bounded comparison implements the same normalization/condition fixture, one chemical-identity operation, one constraint screen and a headless report in both runtimes. Use identical source inputs and expected outputs. Record implementation/review hours, agent iterations, defects, cold-start execution, dependency availability, licensing and CI feasibility on the actual host. Prefer the simpler maintainable option under observed requirements; results on this slice do not establish universal language superiority. Cap the spike before it starts and preserve an inconclusive outcome if evidence is insufficient.

| Component | Proposed implementation | Contract |
|---|---|---|
| Research interface | Optional Mathematica/Jupyter notebooks | Browse evidence, choose profiles, inspect decisions, launch named workflows |
| Workflow and policy logic | Selected primary runtime packages | Validate input snapshots, invoke adapters, apply constraints, build reports |
| Evidence store | Immutable source files plus normalized JSON records and manifests | Preserve provenance and append new versions |
| Feature pipeline | Selected runtime chemistry library; optional adapter | Versioned molecular identity and feature definitions |
| Predictive models | Measured/physical baselines; conditional model adapter | Same prediction envelope and evaluation harness |
| Thermodynamic/quantum adapters | External executable or Python integration | Explicit capabilities, inputs, units, errors and method provenance |
| Experiment policy | Fixed transparent prioritization; conditional adaptive adapter | Select from eligible candidates under resource constraints |
| Reporting | Markdown and JSON; notebook views | Candidate evidence, benchmark outcomes, proposed experiments and decisions |

The first release uses one authoritative implementation of each function in the selected core runtime. A second runtime is optional and must justify its interface and maintenance cost. Keep the comparison prototypes out of the production path after the choice.

Documented Wolfram capabilities relevant to implementation include Molecule, MoleculeModify, MoleculeValue, ChemicalData, Predict, ExternalEvaluate, RunProcess, VerificationTest and TestReport. Availability and behavior must be tested on the pinned installation. Proposed project APIs are separate from these vendor functions.

Use subprocess argument arrays and structured input files; do not interpolate molecule strings into shell commands. A worker has a unique run directory, finite time budget and cancellation behavior. Adapter output is validated before entering the evidence store.

### Proposed repository structure and ownership

| Path | Responsibility | Ownership rule |
|---|---|---|
| `src/fde/` (language-specific layout bound in RUN-006) | Profile, data, feature, screening and reporting packages | Assigned per module; one writer |
| `notebooks/` | Thin research views and walkthrough | Assigned owner in the initial single stream |
| `adapters/` (only enabled integrations) | Specialist models, solver adapters and process bridges | Assigned owner when the integration is enabled |
| `schemas/` | Project envelopes and schema migrations | Contract owner |
| `profiles/` | Versioned research/application/metric definitions | Science/profile owner |
| `fixtures/` | Small independently checked examples and negative cases | Owning module + reviewer |
| `tests/core/`, `tests/integration/` | Module and cross-runtime verification | Owning module |
| `data/manifests/` | Immutable input references and normalized snapshot manifests | Assigned owner in the initial single stream |
| `evidence/` | Bounded review/verification reports; no uncontrolled raw data | Ticket-specific owner |
| `docs/` | Methods, runbooks, decisions and report templates | Ticket-specific owner |

Managed AWF paths are outside ordinary product-edit scope. Large raw datasets, calculation outputs, model weights, sample images and instrument files belong in an agreed artifact store with immutable hash references and backup policy; the project repository stores manifests and small permitted fixtures. A database/server deployment is not required for the first release.

### Component interface contract

The following names are proposed **project operations**, not Wolfram built-ins or claimed implemented commands: `ingest_source`, `normalize_observations`, `resolve_identity`, `compute_features`, `fit_baseline`, `train_model`, `predict_properties`, `calculate_properties`, `screen_candidates`, `propose_actions`, `ingest_results` and `render_report`. Provide one batch entry point for the operations actually included in the approved slice; notebook wrappers and dormant operations are optional. Pin the operation version independently of the document version.

Every request carries `schema_version`, `operation`, `request_id`, `input_manifest`, `profile_id` when applicable, `parameters`, and `resource_envelope_id` for resource-consuming work. Every response carries `schema_version`, `request_id`, `status`, `output_manifest`, `errors`, `warnings`, `provenance` and `usage`. Allowed operation states are SUCCESS, PARTIAL, FAILED, BLOCKED, CANCELLED and UNKNOWN_OUTCOME. SUCCESS requires all mandatory requested outputs; PARTIAL is never silently promoted. Error records include code, locus, retry classification and relevant evidence.

Prediction items have their own status: VALID, OUT_OF_DOMAIN, UNSUPPORTED, FAILED or MISSING_INPUT. A VALID item supplies property, candidate/condition IDs, value, unit, method and provenance. A failed/unsupported item must not contain a usable numeric estimate. An interval records bounds, nominal level, calibration population and method; absence of an interval is represented explicitly. Constraint states remain PASS/FAIL/UNKNOWN and are not operation statuses.

Request/response schemas reject unknown fields for stable interfaces, nonfinite numbers, malformed identities, incompatible units and invalid condition combinations. Large outputs are manifest-referenced. Treat data deserialization as data parsing; never evaluate Wolfram expressions or untrusted Python pickles from external sources. Use reviewed model serialization mechanisms and provenance checks.

Pin the chosen primary runtime and its dependencies in E01. Pin a secondary runtime only for an enabled adapter. Select and test one primary platform before claiming others. Required checks must fail visibly when the selected required runtime is unavailable; an optional disabled Wolfram adapter cannot force a Python-only core to acquire a licence. If Wolfram is selected or required by an enabled capability, demonstrate real licensed headless execution rather than a skip or mock.

Core golden fixtures, with parity checks only across enabled runtime boundaries, cover °C/K, kPa/Pa, gauge/absolute pressure rejection, cP/Pa·s, molar/mass conversion, null values, censoring, component permutations, unsupported chemistry and a failed external process. Compare numeric values within declared unit-aware tolerances and categorical states exactly.

The source tree above is a responsibility map, not an instruction to create every directory. Actual scoped paths and commands are bound after the runtime decision. No optional training, calculation or adaptive-selection operation is required for M1.


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

M1 prioritizes evidence needed to decide constraints; it does not require two trainable endpoints. Before M2_MODEL, identify a specific missing property/condition whose prediction would alter a decision, then audit independent labels, baseline availability and evaluation coverage. Do not promise models for electrical breakdown, fire behavior, toxicity or ageing without adequate method-specific labels. Missing data can justify measurement or a stop decision rather than an ML epic.

LLM extraction is optional in the MUR. Its assessment uses a manually checked, source-diverse fixture containing identities, signs, exponents, decimal separators, units, conditions and ambiguous tables. Report field accuracy, unsupported-claim rate and review burden. No extracted critical field is auto-promoted based solely on model confidence. Source instructions, embedded code and links cannot change pipeline policy or request tool execution.

## 08. Chemistry representation and candidate universe

Normalize molecule structures under a pinned policy and preserve the original input. Establish rules for stereoisomers, salts, disconnected fragments, tautomers and commercial substances whose composition is not fully disclosed. Do not collapse different physical products into a single formula.

The candidate universe has an immutable snapshot ID. Each candidate links to an identity, procurement or synthesis status, chemistry lane, known constraints and unresolved evidence. A catalogue molecule, a purchasable bottle and a reproducibly specified formulation are different objects.

Version descriptor schemas, coordinate generation, conformer handling and calculation settings. Unsupported atom types or failed descriptors must produce explicit missing/error states. Force-field energies and geometric descriptors are features, not measurements of bulk fluid performance.

Initial candidate generation enumerates allowed variations within chemistry-reviewed families and documented supplier catalogues. Keep a baseline random ordering and a simple physical ranking. Use the same eligible universe for comparative selection experiments.

For mixtures, create an order-independent formulation identity while retaining fraction basis and exact prepared composition. A/B and B/A describe the same composition after appropriate reordering; 30% by mass and 30% by mole do not.

Include a first-pass hazard/regulatory register linked to each identity and source date: GHS classification and SDS revision, known incompatibilities/stability hazards, applicable jurisdiction and chemical-registration/restriction evidence, VOC-related requirements, and available GWP/ODP/environmental-fate/aquatic-toxicity evidence. Missing information is UNKNOWN; a classification alone is not a complete application-risk assessment. Do not assume EU rules apply universally or infer legal compliance from catalogue availability. Record authoritative sources and responsible review before procurement.


## 09. Physical baselines and feasibility analysis

Construct the initial feasibility map manually in M0 before platform implementation. FDE-PHYS-002 later verifies that the implemented system reproduces and updates the approved desk evidence; it is not the first feasibility investigation. Compare observed property combinations in the target region, highlight unsupported extrapolations, and identify constraints for which no credible measurement path exists.

Pure-fluid baseline calculations include unit-checked vapor-pressure fits within their validity range, saturation-temperature calculation at an explicit pressure, simple property correlations and reference-data comparisons. Report model range and fitting uncertainty. For a vapor-pressure fit, a numerical root outside the validated range is an extrapolation, not an established boiling point.

Mixture work requires phase-equilibrium calculations and empirical checks. An ideal-mixture calculation may be a baseline but cannot qualify a blend. Distinguish bubble and dew conditions, liquid and vapor compositions, liquid-liquid separation, temperature glide and composition change during evaporation or loss.

Treat thermal conductivity, viscosity, heat capacity, surface tension, density and latent heat as condition-dependent quantities. Do not infer electrical breakdown from dielectric constant, or flame behavior from a molecular structural flag. An absent fluorine atom does not establish acceptable toxicity, environmental fate or materials compatibility.

Candidate feasibility reports must show all constraints, including unknowns. When no feasible region has been demonstrated, the report must identify which assumptions would need investigation; it must not automatically change the target to obtain a positive result.

The initial mixture scope is identification, exchange, provenance and unsupported-request handling. Enabling MIX requires a separate validation panel of pure endpoints and binary equilibrium data. Check component-permutation invariance, exact pure-component limits, fraction-basis conversions, conservation and single/two-liquid-phase behavior. Evaporation/cycling evidence must address the vapor path and residual liquid, not only the initially prepared blend. Absence of these results leaves MIX_DISABLED or MIX_RESEARCH_ONLY.

Use a two-phase-specific system comparison. Before rig tests, promising thermophysical properties are screening evidence only. If the chosen profile yields no credible candidates, deliver a bounded infeasibility/knowledge-gap report and a ranked list of assumptions worth testing. A move to elevated pressure or single-phase operation is a new profile and separate hypothesis, never retrospective success on the original target.

## 10. Conditional models, uncertainty and applicability

This section applies only after M2_MODEL activation; M1 runs without a trained model. Document the missing information, affected decision, strongest available lookup/physical baseline and expected benefit before training. Train property-specific baselines before multi-task or molecular graph models. Compare a constant/nearest-reference baseline, a transparent structure-property model where supported, and random-forest or Gaussian-process models. Neural models are conditional extensions justified by data coverage and benchmark results.

Include measurement conditions explicitly. A temperature-dependent property model must not mix observations from different conditions as if they were repeated labels. Preserve simulated versus experimental fidelity; simulated data can support training only under an explicit experiment and cannot become experimental validation labels.

Report point error, uncertainty calibration, interval width, domain coverage and performance near decision thresholds. Evaluate uncertainty under withheld chemical families. A confident out-of-domain prediction is not a reason to promote a candidate.

For joint constraints, avoid multiplying marginal probabilities unless independence is supported. Multi-task models may learn cross-property dependence; they still require calibration and complete reporting of unavailable endpoints. Missing evidence remains a distinct issue from predictive variance.

Optional physics-assisted models can learn residual errors around a physical baseline. Compare this against a data-only model using the same training information. Store every model's property coverage, supported chemistry, condition domain and abstention rule.

For initial benchmark promotion, freeze a `metric_contract` before revealing holdout labels. It contains the endpoint and scale, primary loss, group weighting, baseline selection rule, decision tolerance, uncertainty target, minimum effective test size and treatment of missing/censored labels. Default comparisons use MAE for saturation temperature and density, and absolute log error for positive viscosity/vapor-pressure endpoints. Choose the primary endpoint on training/coverage information, not holdout performance.

**Decision-specific promotion contract:** freeze the loss, minimum worthwhile decision improvement, threshold neighbourhood, false-pass/false-reject costs and acceptable rates, uncertainty/abstention rule, and required precision before holdout access. Base sample-size requirements on independent units, event rates and the proposed comparison, not a universal count. Compare with the strongest development-selected baseline under matching information. Report effect size and an appropriately clustered interval; insufficient precision is INCONCLUSIVE.

The former W/4 MAE rule, universal 30-group minimum and default 10% improvement threshold are withdrawn. Global MAE remains descriptive but cannot authorize narrow-window decisions. Report errors and confidence intervals near both boundaries, false-pass/false-reject rates, sample counts and abstentions. If local evidence is too sparse or the required decision error cannot be bounded, do not promote the model for that use. Freeze numerical tolerances from application consequences before evaluation; there is no replacement universal constant.

For prediction intervals, freeze the nominal level, maximum useful width, calibration tolerance and minimum precision in the metric contract; report group-weighted and threshold-region coverage with uncertainty. A wide confidence interval that happens to contain the nominal level is not evidence of adequate calibration. Uninformatively wide prediction intervals cannot pass a decision-usability gate. A finite-sample interval claim is limited to its calibration domain; abstention remains required outside it. Conservative bounds and uncalibrated intervals must be labelled as such.

For a provisional temperature-window screen, require the calibrated prediction interval to fall inside the window; overlapping intervals are UNKNOWN. This does not replace measured evidence for qualification. Treat ordinal synthetic-accessibility scores as rankings, not synthesis probabilities or supplier quotations.

Global accuracy is insufficient when the useful region is narrow. Define a threshold-neighborhood from the profile and development data before holdout access, then report local error, interval width, false-pass/false-reject rates and sample/group counts there. If that neighborhood is too sparsely measured, the model remains unvalidated for boundary decisions even if its global promotion criteria pass. Report joint feasibility only for the subset with supported joint evidence; label it `modeled_subset_feasibility`, never full qualification probability.

An applicability rule includes chemical-feature distance or coverage, property and condition domain, supported atom types and model training lineage. Choose cutoffs on training/calibration data. Compare any multi-task model against independent property models under the same labels; learning dependence is a hypothesis, not an automatic cure for false positives. Pretrained models require training-data overlap disclosure where knowable; unknowable overlap limits novelty/holdout claims.

All numerical thresholds in an activated metric contract are **project research policy**, not universal literature limits. The owner/science lead may amend them using development information before final labels or prospective outcomes are revealed; preserve the old contract and justification. Post-result changes begin a new research comparison and cannot retroactively turn a failed preregistered result into a pass.

Any justified minimum count applies to independent test units in the declared comparison, not raw observations: substance-disjoint tests count substances or leakage-linked clusters; family-challenge tests additionally report whole held-out families and their constituent clusters. Do not claim broad unseen-family generalization from a few families regardless of the number of temperature rows. Apply uncertainty to the appropriate cluster level and explicitly limit a sparse family test to its observed cases.

## 11. Conditional benchmark and leakage controls

These controls apply when a model/policy comparison is activated; M1 source deduplication and provenance do not require building the full benchmark harness.

Freeze training, calibration and holdout assignments before final model selection. Group repeated measurements and related identities so the holdout does not merely contain another temperature from a training molecule. Include a chemical-family challenge split in addition to an interpolation assessment.

Use training-only preprocessing and hyperparameter selection. Keep final holdout labels unavailable to the selection workflow until predictions and candidate rankings have been committed. Record all model attempts and selection decisions.

Evaluate each property, the constraints that consume it and the downstream ranking. Report sample counts, independent chemical-group counts, error distributions, subgroup failures and uncertainty. Compare against physical and simple statistical baselines. Report intervals around performance differences.

For sequential-policy testing, use a replay dataset whose hidden measurements are revealed only when the policy requests them. Equalize starting data, candidate universe, available measurements and resource budget across policies. Replay cannot validate properties absent from the hidden dataset or establish a discovery of new chemistry.

Prospective performance is assessed separately using experiments conducted after policy selection. A small pilot may establish feasibility without supporting a claim of superiority.

Assign observation lineage groups before splitting: all repeated observations from the same substance/sample lineage, source republications and explicitly linked duplicates travel together. Evaluate a substance-disjoint split and a separate family-disjoint challenge. For acyclic chemistry, define family/grouping rules from functional groups, connectivity/branching and homology; do not use an empty ring scaffold as a meaningful family label. Record connected-group sizes and report when grouping leaves too few independent groups. Do not weaken grouping just to meet a sample-count target.

Keep train, calibration, development and final challenge roles distinguishable. Hyperparameter tuning, missing-feature treatment, descriptor selection, transform fitting and uncertainty calibration cannot access final challenge labels. Censored targets require an appropriate declared loss/likelihood or exclusion from that endpoint's point-error metric with explicit coverage reporting. Do not treat censoring thresholds as exact labels.

The replay policy test starts with a frozen candidate pool and measured hidden outcomes. Missing or censored outcomes restrict the supported endpoint; do not fill the replay oracle with the model being evaluated. Compare each policy on the same paired starting splits and budgets, using a justified number of paired replay initializations chosen before comparison. Repeated seeds estimate policy variability within the finite panel, not additional independent substances or laboratory discoveries. Report performance after each resource increment and include failed/unsuccessful actions in cost.

The default replay primary endpoint is confirmed feasible-candidate count at the terminal budget for an explicitly modelable subset of the full profile. Predeclare a decision-relevant minimum useful gain and interval procedure; the former default 20% gain threshold is withdrawn. If baseline count is zero, relative gain is undefined: use a predeclared absolute gain threshold and report both counts. Ties and zero discoveries are informative outcomes. Any Pareto/hypervolume endpoint is secondary unless it was selected and scaled before evaluation; its reference point must not move after outcomes appear.

Before a prospective comparative trial, perform a power/precision assessment using pilot variability, feasible event rates, the minimum worthwhile gain and actual costs. If the available budget cannot discriminate the desired effect, classify the work as a discovery/measurement pilot and prohibit a superiority claim. Adaptive arms must be evaluated under a predeclared trial design; repeated within-candidate measurements do not substitute for independent candidate-level evidence.

Holdout manifests are read-only to the modeling/selection jobs. The evaluation runner can resolve hidden labels but returns them only according to the frozen protocol. Persist the committed prediction hash and the reveal event. Development evaluators and final challenge evaluators are separate entry points. Audit descendants as well as direct observations for leakage. A source correction invalidates affected split assumptions and produces a new benchmark version.

Policy comparisons report both `subset_feasible_count` and `fully_qualified_count` where the latter is actually measurable. A replay with only boiling/viscosity labels must never report a fully qualified coolant count. Failed measurement requests, absent labels and censored results follow the frozen oracle rules; dropping difficult candidates after selection is forbidden. Report known reporting/availability bias in any complete-case replay panel.

No fixed pool size, including several hundred candidates, guarantees useful inference. Establish the supported endpoint, usable independent outcomes, likely event rate and minimum worthwhile effect before authorizing a superiority experiment. Sparse data may justify descriptive replay or a measurement pilot only. Integer outcomes can support comparisons, but repeated random seeds cannot create independent chemical evidence. A zero baseline uses the already-specified predeclared absolute-gain rule; never choose the alternative endpoint after inspecting results.


## 12. External calculations and compute control

Use external calculations when their expected decision value warrants their cost. Each engine declares supported properties, chemistry, methods, operating systems, required licences and validated domains. Record failures and nonconvergence as failures.

COSMO-RS is a candidate for liquid/mixture thermodynamics. Its fast pure-property predictor and its thermodynamic calculations are distinct capabilities. Parameterization and supported chemistry must be checked independently. PySCF/GPU4PySCF is an optional electronic-structure route; a successful energy calculation does not establish a fluid property.

The Wolfram QuantumChemistry paclet may be investigated, but it is not a mandatory dependency for the minimum useful release. Pin and benchmark any adopted package. Do not assume that one engine's output format or quantum method is compatible with another engine's parametrization.

Every job records a request, budget, environment, inputs, engine settings, result status and raw output references. Cache only results produced under matching conditions and settings. Support cancellation, checkpointing where the engine supports it and bounded retries for transient failures. Do not retry deterministic unsupported-method errors.

Start without custom CUDA. GPU usage must be justified by a representative CPU/GPU comparison including transfer overhead, numerical differences, memory use and supported methods. Absence of a GPU must not block the data-ingestion and baseline workflow.

Adapter capability probing is read-only and returns an availability status before submission. Jobs run only an allowlisted, pinned executable/library with a reviewed argument schema. The request specifies maximum wall time, memory, supported concurrency and estimated charge. Each external calculation has a new output directory and stored stdout/stderr references with sensitive fields redacted where necessary.

The cache key includes normalized identity, stereochemistry/conformer ensemble, geometry, phase/temperature/pressure/composition, calculation type, method/basis, parameter-set hash, engine/dependency version and the project schema/canonicalization version. A change to any relevant element produces a new request. Cache reuse cannot turn a failed or unvalidated result into a validated one.

For external jobs, distinguish prepared, submitted, running, completed, failed, cancelled and unknown states. A timeout of the client is not proof that the job stopped. Recover by querying the same job identity; do not submit a duplicate until nonexecution/termination is established. Reservation and actual research charges remain recorded even when no scientifically usable result returns. No external purchasing or laboratory submission is automated in the MUR.

All external-engine implementation is M2_COMPUTE or later. It cannot block the desk study or default M1 evidence-screening release.


## 13. Screening and constrained ranking

Screen in layers: identity/chemistry checks; observed hard failures; low-cost estimates; applicability checks; detailed calculations; proposed measurements. Every filter records its version and reason. Preserve candidates eliminated by uncertain predictions for later audit, separate from candidates with measured disqualifications.

The output contains a Pareto set over selected objectives, explicit hard-constraint states, uncertainty and evidence gaps. A large value on one objective cannot offset a hard failure. A prediction interval crossing a threshold does not count as a confirmed pass.

Distinguish a candidate suitable for additional evidence gathering from a candidate qualified for the application. The system may recommend testing an uncertain candidate if that experiment is feasible and informative. Ranking must explain the applicable profile and why a candidate was included, excluded or deferred.

Maintain a fixed baseline ranking for policy comparisons. An empty shortlist is a legitimate result with diagnostic evidence. Do not alter filters, reference points or objective weights after seeing outcomes without creating a new declared experiment.

Use three separate lists: measured hard failures, evidence-eligible candidates for bounded investigation, and candidates whose required qualification evidence is complete. For the investigation list, missing hard-endpoint data generates a required test action rather than a qualified pass. Direct measured failures cannot be overridden by a favorable model. Known assay/procurement infeasibility removes an action from the selectable set with a reason.

Keep a measurement ladder per candidate: (1) identity/composition and existing evidence; (2) a feasible test for a critical disqualifying condition; (3) targeted uncertain thermophysical properties; (4) qualified rig/material/lifecycle work. The scientific lead may alter the ladder with a recorded reason when information value justifies it. The optimizer cannot avoid an essential unmodeled constraint merely because predicting viscosity is cheaper.

Apply the sourced hazard/regulatory and deployment-acceptability register before expensive scoring. A pure identity match or fluorine-free structure cannot override a hazard failure. M1 uses measured/physical evidence and explicit unknowns; model-dependent ranking is disabled until its specific capability is promoted.


## 14. Experiment-selection policy

The selection action is a candidate or formulation, a measurement or calculation, specified conditions and an evaluation fidelity. Its cost includes procurement, preparation, instrument time, analysis, compute and relevant setup costs. The policy selects useful actions rather than ranking molecules alone.

M1 exports a fixed, explainable evidence-gap/measurement-priority list and a simple cost worksheet; it makes no adaptive-superiority claim and cannot submit jobs. After M2_POLICY activation, compare the selected adaptive method against random eligible selection, fixed physical ranking and simple greedy alternatives. Bayesian optimization is an option only if the evidence supports its required model. Prefer a small number of well-defined objectives. Unknown, experimentally required constraints remain explicit.

Select a batch under the agreed resource envelope. Account for shared preparation, instrument availability, pending measurements and duplicates. Where a full cost-aware multi-fidelity acquisition is too complex, implement and document a simpler policy first; do not claim an algorithm that was not implemented.

Each recommendation records model/profile versions, information available at selection time, estimated cost, rationale and rejected alternatives. Update only after experimental results are validated. Retain a replayable decision history and a controlled response to delayed or failed experiments.

Implement an action ledger separate from the AWF model-run ledger. `action_key` binds candidate/sample lineage, property/test, condition set, fidelity and protocol version; intentional replicates add a replicate identifier. State transitions are PROPOSED → RESERVED → SUBMITTED → RUNNING → COMPLETED, with FAILED/CANCELLED/UNKNOWN_OUTCOME branches and reconciliation events. A uniqueness check blocks accidental duplicate active actions. Exactly one writer updates the ledger through an atomic transaction or compare-and-swap equivalent.

Before admission, reserve the conservative expected charge and required shared setup/resource capacity. At settlement, record actual cost and reclaim only demonstrably unused reservation; unknown cost remains unresolved, not zero. Track policy-attributed comparison cost separately from actual invoiced campaign cost. Pending outcomes condition batch choice or are excluded conservatively; the implementation must disclose which policy it uses.

The first policy supports one test family/fidelity with fixed validated cost estimates and a finite candidate pool. Cost-aware multi-property and multi-fidelity selection is an extension after that policy is verified. An engine may use an explicit staged rule for disqualifying tests and Bayesian selection within the remaining pool; it must not claim general optimal value-of-information behavior from a heuristic ratio.

For every proposed batch, validate sum of reservations plus unresolved liabilities against the remaining envelope, prerequisites, instrument/resource slots, duplicate keys and eligible sample availability. Test changed budgets, pending failures, a late result and an empty action set. No feasible action produces a reasoned BLOCKED/STOP report rather than an infinite selection loop.

The transactional ledger and its failure/reconciliation behavior become mandatory before any enabled operation can incur an external liability or dispatch a job, including M2_COMPUTE or M3. Action accounting is M2_ACTIONS engineering and can be enabled independently of M2_POLICY statistical comparisons; it needs no replay panel or successful H3 result. A static M1 proposal export must not be represented as an executable transaction system.


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

## 16. Feasibility gate, capacity and spending limits

The initial M0 study is proposed, not started. Its control template contains a suggested ten-working-day timebox, 40 total research/analysis hours, eight total owner-review hours (four per week) and zero external spend until separately authorized. These are planning assumptions, not observed throughput or accepted commitments. The owner must bind actual start/deadline, availability, hours and spending caps before kickoff. A nominal 29 September–12 October 2026 window is supplied for review only and must be rebased if not accepted. No date implies that external reviewers or laboratories have committed to respond.

| Gate | Required evidence | Permitted outcome |
|---|---|---|
| G0 M0 decision | Three-profile comparison; bounded chemistry/hazard search; value thesis; cost/access status; review register; capacity and stop-rule audit | STOP_DOMAIN; INCONCLUSIVE; CONTINUE_LIMITED_OFFLINE naming specific packages; or CONTINUE for a named M1 scope |
| G0A Implementation scope | Selected research profile, specific useful artifact, accepted resource envelope and runtime-spike cap | Run bounded runtime comparison and bind core contracts |
| G0B Runtime/AWF readiness | Observed selected runtime, required headless checks, actual AWF adoption/mode for governed execution | Dispatch only the approved implementation packages |
| G1 Evidence-screening release | Traceable real-data curation, condition/identity/hazard checks, reproducible PASS/FAIL/UNKNOWN decisions and two-profile software fixture | Accept M1 within its evidence limits; stop/narrow a lane; propose a justified optional capability |
| G2 Model/calculation activation | Specific information gap, meaningful baseline, independent evidence, decision metric/precision contract and bounded resources | Activate only supported M2_MODEL or M2_COMPUTE capabilities |
| G3 Policy/campaign readiness | Supported policy-evaluation design or explicit pilot-only scope; named methods/partner, reviewed protocol and funded limits | Bounded M2_POLICY comparison or M3 campaign, as expressly approved |
| G4 Physical evidence | Controlled measurements, actual costs and predeclared analysis | Candidate development, stop or inconclusive result; no implied product qualification |
| G5 Scoped handoff | Reproducibility, traceability, appropriate review and unresolved decisions | Close the declared increment only |

Apply these precommitted rules at the M0 deadline or earlier cap exhaustion:

1. If every candidate in the declared universe has a documented hard failure, issue STOP_DOMAIN for that profile/domain. Completed software, sunk cost or changing the target silently cannot override it.
2. If decisive evidence is missing, report INCONCLUSIVE, not universal infeasibility. Any extension needs a new dated, capped question and owner decision before further work.
3. Full CONTINUE requires a plausible target/evidence path, an explicit buyer or deliberately chosen research purpose, acceptable next-stage costs/capacity, resolved decision-critical objections and named chemistry/thermal assessments. Missing specialist review cannot masquerade as independent endorsement.
4. CONTINUE_LIMITED_OFFLINE may release only named small packages producing a useful offline artifact despite specified missing lab/reviewer evidence. It cannot release the whole M1 backlog, authorize physical work or claim commercial validation.
5. Missing owner, unaccepted limits, undefined next scope, expired deadline or unresolved mandatory deployment constraints blocks broad implementation. A separately justified offline investigation remains possible only through the limited decision route.

Re-estimate after five working days or 20 research hours, whichever arrives first, and again at the M0 close. Record owner hours/week, pending-review age, actual analysis hours and external response times. Capacity shortfall or review delay triggers scope reduction or INCONCLUSIVE at the cap; it does not silently extend the deadline. M1 dates are estimated only after G0 and the runtime slice.

Keep separate AWF run accounting and research/procurement/laboratory envelopes. Null is not authorized; zero prohibits paid work. Quotations, estimates, scenario assumptions, actual invoices and spending authorization are different records. Obtain two indicative laboratory responses if possible; unavailable responses leave the physical route blocked and need not prevent a clearly useful offline decision. This specification authorizes no external outreach, engagement or purchase.

M0 can be conducted manually with one accountable owner and an attributed decision memo. For any task actually executed through AWF, all installed workflow requirements apply from the start. This phase distinction does not waive AWF rules. Start M1 with one implementation stream; add streams only after measured review capacity and non-overlapping scope support them.

An artifact may satisfy an analysis task even when its scientific result is negative. Capability activation is separate. Scope, metric and profile changes after outcomes require a new version and cannot retroactively convert a failure into a pass.


## 17. Requirements and verification catalogue

Requirements apply only to their expressly accepted increment and scope. The nine E15 desk procedures execute first; all later requirements are conditional and need further bounded ticket acceptance design. No requirement demands a favorable scientific result.

### FDE-E15 — Pre-build feasibility, value and investment decision

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-FEAS-001 | Bind the study mandate, capacity and stop rules | Inspect a control record with a named accountable owner, accepted start/deadline, hours and spend caps, review capacity and rules for STOP_DOMAIN, INCONCLUSIVE and CONTINUE. Confirm every field has explicit owner acceptance and a dated evidence reference. |
| FDE-FEAS-002 | Compare application profiles and acceptance constraints | For each of the three applications, trace temperature/pressure, fluid-contact boundary, electrical and fire requirements to a named source or responsible decision-maker. Record jurisdiction, standard edition/clause where obtained, equipment arrangement, buyer/OEM requirements and insurer status separately. |
| FDE-FEAS-003 | Assemble a bounded candidate and source inventory | Select one included record, one excluded record and one missing-property record; reproduce each from its source locator and retrieval date. Verify identities, original units, measurement conditions and searched scope are retained. |
| FDE-FEAS-004 | Evaluate chemical feasibility and hazards before software | For each candidate-profile pair, record each hard constraint as PASS, FAIL or UNKNOWN with evidence. Include flash-point method, LEL/UEL and autoignition where available, electrical-property conditions, GHS/SDS information, jurisdiction-specific chemical status, VOC/environmental evidence and procurement status. |
| FDE-FEAS-005 | Define buyer value, competition and publication policy | Trace each proposed buyer problem and competitor claim to a dated source, and distinguish a buyer hypothesis from buyer validation. Identify a specific first useful artifact and why it could matter beyond a generic screening platform. |
| FDE-FEAS-006 | Establish laboratory access and indicative cost bounds | For each response retain provider/date, relevant methods, sample amounts, controls, inclusions/exclusions, currency, taxes/shipping/disposal assumptions, rig scope, lead time and validity. Compare both with the proposed first useful artifact. |
| FDE-FEAS-007 | Obtain independent chemistry and thermal assessments | Verify named reviewers, relevant expertise, scope, conflicts/independence, source dossier version and signed/attributed conclusions. Record objections and unresolved evidence separately from document edits. |
| FDE-FEAS-008 | Audit the desk dossier and record dissent | Reproduce an inclusion, exclusion and cost scenario; verify every external finding has an accepted, qualified, rejected or unresolved disposition with reasons and links. Confirm design amendments are not presented as completed experiments. |
| FDE-FEAS-009 | Issue the dated feasibility and investment decision | A CONTINUE identifies the application/profile version, bounded candidate domain, credible evidence path, buyer/research purpose, funded or capped next scope, owner capacity, review status and specific work packages released. The owner signs the exact dossier revision. |

### FDE-E00 — Research mandate, profile and source baseline

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-GOV-001 | Freeze the selected application profile after G0 | Profile matches the dated G0 decision, records every hard constraint/unknown and preserves rejected alternatives; it cannot authorize a broader application. |
| FDE-GOV-003 | Separate engineering and scientific outcomes | A negative or inconclusive research fixture closes with an honest research outcome and cannot be labeled qualified fluid. |
| FDE-GOV-004 | Bind implementation responsibilities and resources | Actual owner/reviewer capacity and separate AWF/research limits are bound to the G0-authorized scope; null budgets cannot authorize paid action. |

### FDE-E01 — Runtime, contracts and target AWF adoption

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-GOV-002 | Verify the controlling AWF | Target-project conformance references the inspected 1.9.1 commit/manifest, actual installation state and revision-3 schema; it does not claim live readiness from documentation. |
| FDE-RUN-001 | Run the selected core without notebook state | A fresh headless process in the selected runtime executes the fixture without a notebook; unavailable required runtimes fail visibly. |
| FDE-RUN-002 | Validate core contracts and profile independence | Malformed units/conditions are rejected; two synthetic application profiles produce their declared different decisions without changing core screening code. |
| FDE-RUN-003 | Capture execution provenance | Each completed run links its code, configuration, data, dependencies and outputs through verifiable hashes. |
| FDE-RUN-004 | Separate optional capability availability | Missing external software produces an unavailable-capability result while the offline core fixture remains runnable. |
| FDE-RUN-005 | Validate enabled operation boundaries | Core golden cases verify request/response semantics; cross-runtime parity is required only for an enabled second-runtime adapter and cannot block a single-runtime core. |
| FDE-RUN-006 | Select the primary runtime from a bounded comparison | Compare identical normalization, chemical-identity, screening and headless-report fixtures in Python and Wolfram; record observed effort, defects, CI/licence feasibility and the justified choice before core implementation. |

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
| FDE-CHEM-003 | Version enabled representations and capabilities | Record the selected identity/feature capabilities and versions; unsupported calculations remain disabled rather than requiring a feature engine for M1. |
| FDE-CHEM-004 | Freeze sourced candidate and hazard eligibility | Snapshots retain availability, hazard/regulatory evidence, applicable profile and UNKNOWN fields; compared policies use the same declared universe. |

### FDE-E04 — Thermodynamic baselines and feasibility

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-PHYS-001 | Implement a physical reference baseline | Reference calculations reproduce independently specified fixtures within declared tolerances and label out-of-range evaluations. |
| FDE-PHYS-002 | Reproduce and update the approved desk feasibility map | The implemented map agrees with the source-reviewed M0 decisions and preserves known hard failures and unknowns; this task is not the first feasibility study. |
| FDE-PHYS-003 | Model mixture phase behavior explicitly | Core schemas/rejection fixtures distinguish mixtures correctly; enabling the conditional MIX lane additionally requires validated bubble/dew, composition and phase checks. |
| FDE-PHYS-004 | Preserve system-dependent endpoints | Thermal and electrical performance records include required rig/method context; unsupported proxy substitutions are rejected. |

### FDE-E05 — Benchmark and split infrastructure

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-VAL-001 | Prevent correlated-label leakage | Split audit detects overlap in substances, measurement groups and protected chemical families according to the declared test. |
| FDE-VAL-002 | Freeze information available to evaluation | Predictions and rankings are committed before holdout disclosure; post-disclosure changes require a new evaluation version. |
| FDE-VAL-003 | Compare decision-relevant baselines | A frozen, endpoint-specific decision/precision contract supports the activated model comparison; unsupported inference yields INCONCLUSIVE without universal sample-size or gain defaults. |
| FDE-VAL-004 | Replay sequential policies honestly | Replay reveals only requested hidden observations and charges specified costs; unavailable endpoints remain unavailable. |
| FDE-VAL-005 | Report inconclusive evaluations | Insufficient coverage or precision yields INCONCLUSIVE with reasons rather than a numerical pass by default. |

### FDE-E06 — Predictive models and uncertainty

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-ML-001 | Justify and train a bounded property model | Before training, record the missing costly information, affected decision, usable labels, baseline and permitted scope; otherwise return MODEL_NOT_JUSTIFIED and do not build the model. |
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
| FDE-SCR-003 | Report measured and supported trade-offs | Objective directions, conditions and provenance are explicit; measured/physical fallback runs without ML, and any model-dependent objective requires separate promotion. |
| FDE-SCR-004 | Separate exploration from qualification | A candidate proposed for learning is visibly distinguished from one with sufficient physical evidence for the profile. |

### FDE-E09 — Sequential experiment selection

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-AL-001 | Export a static next-measurement proposal | A fixed, explainable proposal identifies candidate, evidence gap, test, conditions, prerequisites and cost assumptions; the M1 operation cannot submit jobs or reserve spend. |
| FDE-AL-002 | Evaluate a separately activated sequential policy | Supported outcomes, event rates, independent units and a predeclared precision assessment justify the comparison; missing evidence permits descriptive replay only, not a superiority claim. |
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
| FDE-EXP-001 | Freeze a funded pilot or comparison protocol | Named capacity, methods, resources, controls and claim scope are frozen; a discovery pilot does not depend on a successful policy-superiority result, and comparative claims require the appropriate design. |
| FDE-EXP-002 | Track actual experiment resources | Report costs, failures, elapsed time and completed measurements for every arm, including unsuccessful procurement. |
| FDE-EXP-003 | Evaluate prospective scientific outcomes | Final campaign report distinguishes discovery, improvement, no demonstrated advantage and inconclusive results. |

### FDE-E12 — Research decisions and reporting

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-REP-001 | Produce candidate evidence dossiers | Each dossier resolves every material claim to measured, calculated or predicted evidence with conditions and gaps. |
| FDE-REP-002 | Report scoped gates and limitations | A report states scientific outcome, authorized scope, capability availability and unresolved evidence separately; no unrun benchmark becomes an M1 prerequisite. |
| FDE-REP-003 | Create reproducible research exports | Markdown and JSON outputs agree on candidate IDs, constraints, metrics and scientific status. |

### FDE-E13 — Conditional advanced methods

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-EXT-001 | Gate generative and RL extensions | An extension proposal names the validated scorer, bounded chemistry/action space, baseline and experimental validation plan. |
| FDE-EXT-002 | Gate learned simulation extensions | An ML-potential/custom-acceleration proposal identifies a measured bottleneck, domain, reference checks and cost-benefit test. |

### FDE-E14 — Reproducible release and handoff

| Requirement | Required behavior | Acceptance evidence |
|---|---|---|
| FDE-REL-001 | Package the authorized slice for independent rerun | A second clean environment reruns the chosen core and declared evidence slice; optional disabled models, runtimes and ledgers are not required checks. |
| FDE-REL-002 | Complete requirements-to-evidence traceability | Every requirement applicable to the declared release increment maps to work packages, artifacts and verification evidence; later/disabled capabilities retain explicit planned/blocked status and claim restrictions. |
| FDE-REL-003 | Prepare AWF handoff without bypassing approval | Handoff binds the actual adopted 1.9.1 policy, current candidate review/closeout evidence and owner status; compatibility inspection alone is not installation or authorization. |
| FDE-REL-004 | Verify artifact recovery and scientific claims | A restored decision resolves its required artifacts/hashes; missing physical evidence or inaccessible dependencies cannot be presented as a qualified or publicly reproducible result. |


## 18. Proposed Jira structure and staged commitment

| Epic | Deliverable | Planning references | Gate |
|---|---|---|---|
| FDE-E15 | Pre-build feasibility, value and investment decision | None | G0 |
| FDE-E00 | Research mandate, profile and source baseline | FDE-E15 | G0A |
| FDE-E01 | Runtime, contracts and target AWF adoption | FDE-E00 | G0B |
| FDE-E02 | Source acquisition and measurement curation | FDE-E01 | G1 |
| FDE-E03 | Chemical identity and descriptor pipeline | FDE-E00, FDE-E01, FDE-E02 | G1 |
| FDE-E04 | Thermodynamic baselines and feasibility | FDE-E00, FDE-E02, FDE-E03, FDE-E15 | G1 |
| FDE-E05 | Benchmark and split infrastructure | FDE-E01, FDE-E02, FDE-E03, FDE-E04 | G2 |
| FDE-E06 | Predictive models and uncertainty | FDE-E03, FDE-E04, FDE-E05 | G2 |
| FDE-E07 | External calculation adapters | FDE-E01, FDE-E03, FDE-E04, FDE-E09 | G2 |
| FDE-E08 | Constraint screening and candidate dossiers | FDE-E00, FDE-E01, FDE-E03, FDE-E04 | G1 |
| FDE-E09 | Sequential experiment selection | FDE-E01, FDE-E05, FDE-E08 | G3 |
| FDE-E10 | Laboratory protocol and result exchange | FDE-E00, FDE-E01, FDE-E02, FDE-E03, FDE-E04 | G3 |
| FDE-E11 | Prospective experimental campaign | FDE-E09, FDE-E10 | G4 |
| FDE-E12 | Research decisions and reporting | FDE-E04, FDE-E08 | G5 |
| FDE-E13 | Conditional advanced methods | FDE-E06, FDE-E07, FDE-E09 | EXTENSION |
| FDE-E14 | Reproducible release and handoff | FDE-E01, FDE-E12 | G5 |

E15 is deliberately numbered after the original epics to preserve all original IDs. It executes first. Its nine M0 records have concrete manual procedures and positive/negative/boundary acceptance cases in `M0_Feasibility_Study.md` and the planning JSON. No M0 record depends on runtime, schema, curation-platform or model implementation.

All original work packages are conditional. Their stable IDs are retained for traceability; they are not a commitment to build all of them. In particular, PHYS-002 becomes an implemented check of the already-completed desk feasibility evidence. The initial decision is made by FEAS-004/FEAS-009 with no software prerequisites.

| Increment | Deliverable | Scope |
|---|---|---|
| M0 | Bounded evidence and investment decision | E15 only; desk tools allowed, no platform build |
| M1 | Useful evidence-curation and constraint-screening vertical slice | Approved E00/E01/E02/E03/E04/E08/E12/E14 work plus static AL-001 proposal export |
| M2_MODEL | Decision-justified predictive capability | E05/E06 only after endpoint/data/value and precision gates |
| M2_POLICY | Evaluated sequential policy | AL-002 and relevant replay/benchmark work; supported outcomes required |
| M2_ACTIONS | Transactional action handling | AL-003/004/005; engineering prerequisite for external liabilities, independent of H3 |
| M2_COMPUTE | Warranted external calculations | E07 plus ledger/capability prerequisites |
| M3 | Bounded physical pilot or comparison | E10/E11, ledger, accountable partner and funded protocol |
| M4 | Product qualification | Separately commissioned system, materials, lifecycle and compliance work |
| EXT | Explicitly approved research extension | MIX/NOVEL/SYSTEM, E13 or other scoped investigation |

Use work-package predecessors, activation gates and the signed list of authorized IDs, not blanket whole-epic completion. The graph is a planning dependency graph; none of its records is an AWF READY contract. A small Jira feasibility epic is permissible; wholesale conversion of the later backlog is premature.

After G0, first freeze the selected profile/resources, run the bounded runtime comparison, bind actual paths/commands and AWF readiness, then implement one measured-data-to-decision slice. The same screening implementation must process two synthetic profile fixtures. Do not implement dormant operations merely because they appear in the conditional architecture.

Risk tiers are proposed by consequence, not filename. The M0 source inventory, quote transcription and clerical dossier audit are Tier 1 only while they do not change acceptance rules or adjudicate scientific evidence. Profile, safety, scientific inference, spending/activation and policy changes remain Tier 2. Later tiers are reassessed under actual AWF policy and inspected changes. No blanket Tier 1 exemption applies to documentation.

M1 implementation records still need requirement-specific executable cases and commands before dispatch. Their deferred validation status is explicit; repeating a generic sentence is not executable acceptance. Split L work before dispatch and measure actual delivery/review capacity before parallelism or schedule commitments.


## 19. Ticket and AWF 1.9.1 execution contract

The requested compatibility baseline is [jkinlay/agentic-workflow-framework](https://github.com/jkinlay/agentic-workflow-framework), **1.9.1**, at repository-recorded source commit `e7d80a691e2ae0a0b55e54f4e5e91e95e5ca7fe5`. The retrieved `MANIFEST.json` hashes to `d10a180af0109ffda59f70d925dd934c8fb78d9a8016d7ca39086d715f1194bd`. The repository's later upgrade-fixture index identifies that source as its 1.9.1 reference. This is a pinned compatibility target, not a claim that 1.9.1 is the latest release. Inspection also observed a 1.9.2 published release and main documenting 1.9.3; their behavior is not imported into this specification.

The actual 1.9.1 specification, AGENTS instructions, ticket schema/template, lifecycle, native coordination, adoption, routing, operating configuration and review/closeout runbooks were read. The former v1.41 overlay is superseded for this task. Retrieval and local hashing establish inspected source identity, not successful AWF installation, project adoption or live qualification.

**Contract generation must use the retrieved revision-3 schema.** Its fields are `schema_version`, `contract_id`, `contract_version`, `created_at`, `project_id`, `repository_id`, `issue_id`, `ticket`, `requirements_hash`, `policy_hash`, `objective`, `acceptance_criteria`, `dependencies`, `branch_origin_sha`, `target_base_branch`, `scope`, `validation`, `risk_flags`, `specialist_domains`, `disposition`, `risk_tier`, `tier_justification`, `closure_standard`, `owner_closure_required` and `corrects`. The schema's historical `$id` contains AWF 1.2; that is not permission to alter it or set the schema revision to 1.9.1.

Every acceptance criterion supplies `id`, `text` and `validation`. Scope contains expected paths, allowed adjacent paths, protected interfaces, forbidden changes, governance-change authorization and evidence paths. Validation declares actual commands, cases, resources, justified non-applicability and any tested platform distinction. Runtime contracts must not contain placeholder UUIDs, repository IDs, SHAs, hash values or Jira keys. Draft planning records stay distinct from executable contracts.

Dependencies in the AWF contract carry observed issue identity, `kind` from `code | deployment | migration | environment`, `direction: requires`, satisfaction and evidence. They are ticket dependencies; an epic being present does not prove its deliverable is available. Map laboratory/resource dependencies to environment records tied to actual evidence and retain scientific prerequisite details in the project record. A READY contract requires satisfied dependencies with evidence.

Use risk Tier 2 for uncertain/scientific-decision, schema, orchestration or resource-accounting work unless the installed policy and actual paths support a less restrictive classification. Tier 1 eligibility is derived under reviewed configuration. Freeze `closure_standard` (FULL or DECLARED_LIMITATIONS) before review; a nonpositive research result can satisfy a FULL analysis contract, but an unexecuted laboratory test cannot. Explicitly attributed limitations are required for DECLARED_LIMITATIONS.

AWF publication sequence is worker completion, scoped branch push and draft PR, observed branch/PR identities, current validation and requirements, observed draft clearance, critic review of the actual head, required specialist review, final gate, then owner authorization. READY_FOR_CRITIC and READY_FOR_OWNER_AUTHORIZATION are different states. Changed heads or bases invalidate affected evidence under the controlling policy. Do not adopt the later publisher-commit shortcut without a version-specific change.

Only the controller mirrors Jira lifecycle events. Worker start maps to In Progress; PR readiness to In Review; owner-requested changes or changed review head to In Progress; confirmed merge and valid closeout to Done, subject to owner-closure requirements. BLOCK/PARK do not trigger Jira status writes. Never transition Epics. Read before and after writes; mismatches or unknown outcomes stop further writes to that ticket without reissuing the action. The reference adapter itself is not evidence that live Jira writing is enabled.

The inspected AWF native-planning default describes three implementation streams with an independent reviewer per stream, inside the configured ceiling and actual host capacity. This project proposes one initial stream through the supported project configuration; this document does not itself change that configuration. Do not assume all those agents exist. Keep one writer per ticket/path, explicit resource leases and separate reviewer contexts. Runtime choices come from accepted project configuration, not model names hard-coded in this specification.

Reserve protected run budgets before dispatch and settle observed usage. AWF 1.9.1 has effective monetary ceilings when configured; unknown actual cost is not zero. If the chosen host cannot supply/enforce required accounting, report that mode unavailable and use an allowed reference/manual mode or a separately reviewed workflow upgrade. Do not disable the constraint to make the project run.

The normal amendment cap is governed by the installed policy; the inspected default is three. At the cap, present unresolved findings for the prescribed owner disposition; do not silently extend cycles or weaken closure. Serious findings must name a criterion or mandatory boundary. This document's three specification self-review cycles are drafting work, not independent AWF critic approvals, and do not consume a future implementation ticket's amendment allowance.

FDE adoption must preserve managed AWF bytes and project instructions through the supported mechanism, map real GitHub/Jira identities, supply actual project test commands for the selected required runtime/capabilities and record actual INSTALLED/CONFIGURED/ACTIVE state. A fresh project may remain Jira-disabled with provisional local IDs. No ticket or this document grants merge authority, live adapter enrollment or approval to modify governance.

### Conversion from planning work package to executable contract

| Planning content | AWF destination | Conversion rule |
|---|---|---|
| Logical work-package ID, epic and requirement IDs | Project sidecar plus acceptance-criterion IDs/text | Retain traceability without adding undeclared top-level AWF fields |
| Objective and scope paths | objective; scope.* | Replace proposed paths with inspected paths and bounded adjacent changes |
| Criteria and validation plan | acceptance_criteria; validation.* | Name real commands/cases/resources; determine actual skip or platform policy |
| Work-package predecessors | dependencies | Resolve actual issue IDs/tickets, supported dependency kinds and observed satisfaction evidence |
| Profile, dataset and metric versions | Project manifest; requirements hash | Bind precise input versions through the project's requirements record and AWF canonicalization |
| Proposed tier and scientific review needs | risk_tier, tier_justification, risk_flags, specialist_domains | Validate under installed paths/policy; explicitly configure required scientific specialist domains if absent |
| Closure intention and limitations | closure_standard; owner_closure_required | Freeze before review; retain attribution and apply observed keyword rules |
| Actual repository and issue data | project_id, repository_id, issue_id, ticket, branch_origin_sha, target_base_branch | Obtain from the real target; do not reuse the AWF source repository's numeric ID |
| Trusted configuration and evidence | policy_hash, requirements_hash, contract ID/version/time | Generate through the actual reviewed workflow; no invented hash values |

The revision-3 schema is closed (`additionalProperties: false`). Keep profile IDs, scientific hypotheses, milestone classifications, resource estimates and proposed Jira metadata in project-owned sidecars unless mapped into existing schema fields. A planning JSON file may use null for unbound identities; that does not make it a valid AWF runtime record. The shipped AWF template is also a draft wrapper that requires extraction, filling and semantic validation.

Jira creation must preserve the original issue key returned by the service, parent epic and requirement links; use supported issue/link types from the actual project. Do not invent Jira custom fields, issue IDs, transitions or labels assumed to trigger automation. Creation and lifecycle operation are separate activities. This deliverable performs neither.

Every ready ticket needs an independently executable acceptance procedure and retained evidence paths. For research methods, include a chemistry/thermal/statistical reviewer when its claim requires that expertise. Scientific threshold changes, evaluation policies and laboratory protocols should be Tier 2 even when stored under docs/; nominate a stricter tier rather than relying on path eligibility. A generic code reviewer does not validate a chemical or statistical claim.

Do not hard-code specialist model names from this document. The AWF 1.9.1 routes must be available on the actual host; unavailable configured routes need the workflow's explicit remedy, not silent substitution. Source compatibility is verified here; the target's adopted/modified policy, model availability, resources and trusted identities still require observation.

For pre-adoption foundation work, distinguish authorized local setup from AWF-governed dispatch. E01 can prepare the bounded runtime skeleton and test command using the normal adoption process; it must not claim a dispatched AWF run or ACTIVE state before the corresponding evidence exists. This avoids making the existence of the test command depend on an already-completed adoption.

### Phase-specific application

M0 manual procedures are research planning records, not executable AWF contracts. If converted to agent-dispatched tickets, bind the actual schema, scope, case procedure, resources, reviewer and adopted policy before READY. Later conditional seeds cannot bypass G0 by acquiring Jira keys. The controller must verify both ordinary dependency evidence and the named authorized scope in the feasibility decision.

Use one delivery stream initially. Independent critic/specialist/owner requirements follow the actual adopted policy for each task; available review capacity must be demonstrated rather than inferred from a proposed three-stream chart. A simple source-transcription task may propose Tier 1; an uncertain or consequential scientific/approval change remains Tier 2 even in docs.


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

M0 quality checks are source/decision audits with explicit manual cases; they do not require a software test harness. Package-integrity validation checks these planning artifacts only. M1 validation covers the selected runtime, provenance, units, hazard/constraint decisions, empty/unknown cases and two-profile independence. Full ML leakage/calibration and adaptive-policy tests apply only to activated capabilities.


## 21. Open decisions and factual status

| Decision | Current state | Required resolution and blocking scope |
|---|---|---|
| Study ownership/capacity | `jkinlay` is proposed accountable owner; dates/hours not accepted | Accept M0 control before kickoff; no study completion is claimed |
| Chemistry/application | No profile selected or qualified | M0 comparison and bounded feasibility evidence before broad implementation |
| Fire/deployment acceptability | Applicable methods, clauses, OEM/insurer decisions unresolved | Resolve for the chosen intended deployment; unknowns block deployability claims |
| Buyer/value route | Hypothesis only | One-page thesis; separate public evidence, assumptions and actual buyer validation |
| Laboratory costs/access | No quotes or partner obtained in this amendment | Costed credible path before paid or physical work; offline-only alternative must be explicit |
| Independent science review | No named professional reviews obtained | Chemistry and thermal assessments for full CONTINUE; limited owner-attested offline route is separately labelled |
| Runtime | Undecided | Bounded post-G0 comparison; no mandatory two-runtime core |
| ML/policy utility | Unestablished | Specific evidence gap, baseline and precision case before M2 activation |
| AWF | Source compatibility inspected at 1.9.1; target adoption not performed | Actual conformance/configuration before governed dispatch; no change to AWF itself |
| Repository/Jira | Repository `jkinlay/cooling-fluid`, ID 1393836050; Jira unbound | Bind actual Jira scope if used; never invent issue IDs or policy hashes |
| Publication/IP | Repository observed public on 28 September 2026 | Decide route before adding new candidate/formulation findings; general plans do not establish a patentability verdict |

No automatic visibility change is requested or performed by this amendment. The supplied external review is retained as attributed review material, with its claims qualified in a separate disposition record. Historic v1.0 documents are superseded planning evidence, not current execution instructions.


## 22. Deliverables and acceptance by increment

M0 delivers the study control, three-profile comparison, search-coverage/source register, feasibility and hazard tables, value thesis, quote/cost status, independent-review status, dissent register and dated decision. Missing external evidence must remain visible. Acceptance of a complete INCONCLUSIVE or STOP_DOMAIN report is not permission to build the platform.

M1 delivers only the G0-authorized evidence-screening slice: pinned source/identity/condition data, explicit hazard and hard-constraint states, reproducible dossiers/reports, static next-measurement proposals and rerun instructions. It must preserve measured versus derived/predicted evidence and process two synthetic profiles without algorithm edits. It requires neither two trainable endpoints nor model promotion. Synthetic-only operation is an ENGINEERING_DEMONSTRATOR, not a real-data research outcome.

M2 deliverables are capability-specific and require the corresponding value/data/precision and resource gates. No comparison may claim superiority from unsupported endpoints or repeated seeds treated as new chemistry. M3 requires actual accountable laboratory capacity, methods and funds; M4 qualification is separate.

Every accepted increment lists included and deferred requirement IDs, true prerequisites, actual commands/procedures, executed/unexecuted checks, resources, results and claim limitations. Record package/engineering completion, scientific result, commercial evidence and physical qualification separately.

The document package has structural/hash/dependency validation only. This amendment executes no fluid models, chemistry experiments, runtime comparison, buyer interview, laboratory outreach or AWF adoption. Its review disposition records design changes while scientific/commercial evidence remains pending.


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

Additional primary references used for the design: [molecular RL optimization](https://www.nature.com/articles/s41598-019-47148-x) supports the existence of the optional method, not its value for this project; [liquid ML-potential transferability study](https://pubs.acs.org/jctcce/article/21/12/6096/3693205/Transferability-of-Data-Sets-between-Machine) motivates chemistry-specific validation. No performance claim is transferred from those studies to the proposed cooling application.

AWF primary paths at the pinned commit: `.agentic/SPECIFICATION.md`, `AGENTS.md`, `.agentic/workflow-version.yaml`, `.agentic/templates/ticket-contract.yaml`, `.agentic/schemas/ticket-contract.schema.json`, `.agentic/PROJECT_CONFIG.yaml`, `.agentic/docs/20-NEW-PROJECT-SETUP.md`, `23-TICKET-LIFECYCLE.md`, `24-STREAM-STARTUP.md`, `27-MODEL-ROUTING.md`, `29-OPERATING-CONFIGURATION.md` and `30-REVIEW-TIERS-AND-CLOSEOUT.md`. The evidence appendix records their content hashes. Historical source files are referenced, not adopted into a product repository by this task.

External-review amendment sources checked on 28 September 2026:

| Source | Supported use and limitation |
|---|---|
| S17 [NIOSH ethyl formate](https://www.cdc.gov/niosh/npg/npgd0278.html) | 130 °F boiling point and −4 °F flash point (about 54 °C and −20 °C) refute the review's universal flash-point range; the substance remains flammable and is not recommended as a coolant |
| S18 [ZutaCore architecture explanation](https://blog.zutacore.com/zutacore-blog/two-phase-dlc-not-immersion-liquid-cooling) | Distinguishes direct-to-chip from immersion; vendor performance/market claims are not independent qualification evidence |
| S19 [Schneider Electric, 22 May 2026](https://blog.se.com/datacenter/2026/05/22/pfas-phase-out-liquid-cooling-us-data-center-operators-must-do/) | Industry participant's account of market headwinds; not a verified market census or substitute for current adopted regulation |
| S20 [EPO enabling disclosure guidance](https://www.epo.org/en/legal/guidelines-epc/2026/g_iv_2.html) | Supports claim/disclosure-specific IP assessment; this project has no patentability or freedom-to-operate opinion |

The external review's exact market shares, universal fire-code/insurer conclusions, exhaustive chemical infeasibility and minimum laboratory prices remain unverified claims. Obtain current authoritative jurisdiction-specific requirements and provider evidence in M0; do not promote those assertions into acceptance criteria merely because the review calls them blockers.


## 24. Revision status and next decision

**Version 1.1 — feasibility-first planning baseline.** The appropriate next work is the bounded M0 investigation, subject to accepting its control record. The broad engineering backlog is conditional and is not recommended for bulk dispatch.

The history remains v0.1 → self-review 1 → v0.2 → self-review 2 → v0.3 → self-review 3 → v1.0 → user-supplied external cycle 4 → v1.1. The first three reviews were drafting self-reviews. The identity, credentials and independence of the external reviewer have not been verified; it is not a substitute for the named professional assessments required by G0.

See `reviews/Red_Team_04_External.md` for the supplied review and `reviews/Red_Team_04_Disposition.md` for all 19 findings, accepted changes, qualified/rejected assertions and remaining evidence. Document-level remedies do not close the scientific or commercial questions. Existing v1.0 files/archives are retained as history and clearly superseded by this version.

No Jira tickets or AWF runtime contracts have been created by this revision. Proceed to implementation only after a dated scope-specific CONTINUE decision; preserve STOP_DOMAIN and INCONCLUSIVE as legitimate outcomes.

