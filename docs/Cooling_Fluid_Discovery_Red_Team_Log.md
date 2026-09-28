# Cooling Fluid Discovery — Three-Cycle Red-Team Record

Final specification: v1.0, 28 September 2026.

Process: initial draft; three sequential adversarial self-reviews, each followed by a retained complete rewrite. These are not independent AWF critic reviews or an implementation approval.

# Red-team cycle 1 — scientific feasibility and scope

Input: `revisions/Specification_v0.1.md`. Method: adversarial self-review of the written draft, followed by a substantive rewrite. This is not an independently executed AWF critic review. The user identified the canonical GitHub source and requested version 1.9.1 during drafting; the review incorporates that new evidence.

| Finding | Severity | Attack against the draft | Required correction | Disposition in v0.2 |
|---|---|---|---|---|
| R1-01 | BLOCKER | Sections 19/21 treat canonical AWF as unavailable and refer to an obsolete overlay, despite the newly supplied source. | Pin actual 1.9.1 files, verify the source manifest and replace inferred workflow rules. | Fixed in sections 19, 21, 23. Remaining target-project adoption is a real later dependency. |
| R1-02 | MAJOR | The target profile contains missing electrical/fire/lifecycle limits; a worker could mistake a completed profile file for a usable qualification specification. | Separate research-profile completeness from campaign and qualification readiness; hard missing thresholds block only the corresponding claim/action. | Fixed in sections 03 and 16. |
| R1-03 | MAJOR | G0 requires the environment while the environment epic follows the G0-owning epic, creating ambiguous readiness. | Define a planning baseline followed by runtime readiness; software fixture work must have a noncircular entry route. | Fixed in section 16. |
| R1-04 | MAJOR | Predictive usefulness and policy improvement have no operational pass criteria; nearly any chart could be accepted as progress. | Define pre-result metric contracts, primary endpoints, uncertainty/precision gates and negative/inconclusive outcomes. | Fixed in sections 10, 11, 16. |
| R1-05 | MAJOR | Chemical-family withholding is underdefined for largely acyclic candidate chemistry; repeated temperatures and re-published values can leak. | Specify grouped lineage, acyclic-family handling, train-only transforms and sealed revelation rules. | Fixed in section 11. |
| R1-06 | MAJOR | A laboratory pilot could be represented as proof of AI superiority despite weak power or selectively missing labels. | Separate discovery pilots from a prospective comparative trial; predeclare sample size/precision and failure accounting. | Fixed in sections 11 and 15. |
| R1-07 | MAJOR | The MVP claims pure-first scope but requires substantial mixture implementation, creating scope creep. | Require mixture-aware schemas initially; gate mixture prediction/optimization behind an explicit lane activation. | Fixed in sections 02, 09 and PHYS-003. |
| R1-08 | MAJOR | An attractive point prediction inside a narrow boiling window could receive excessive confidence when model error exceeds the design margin. | Tie accuracy and interval informativeness to the actual decision window; never let prediction satisfy a lab-only endpoint. | Fixed in sections 10 and 13. |
| R1-09 | MINOR | No initial scale limits distinguish a useful vertical slice from a large simulation platform. | Add bounded workload assumptions and incremental delivery milestones, explicitly separate from spending authorization. | Fixed in sections 02 and 16. |

Review conclusion: revise before Jira decomposition. None of these findings establishes physical infeasibility; they expose ways the project could spend resources without answering its declared questions.


---

# Red-team cycle 2 — data integrity, implementation and experimental validity

Input: `revisions/Specification_v0.2.md`. Method: adversarial self-review of interfaces, failure paths and scientific misuse cases. Each correction is incorporated in the next complete draft. No independent agent or live AWF execution is claimed.

| Finding | Severity | Failure scenario | Required correction | Disposition in v0.3 |
|---|---|---|---|---|
| R2-01 | MAJOR | Engineers implement mutually inconsistent Wolfram/Python payloads because the architecture names components but omits executable interface semantics. | Define operations, common envelopes, strict status/value rules, capability discovery and golden parity cases. | Fixed in sections 05/06/20 and new RUN-005. |
| R2-02 | MAJOR | Correct molecular predictions become evidence for a different batch; mass/molar units or upper bounds are silently converted. | Specify observation/sample/condition identity, immutable normalization lineage, censoring representation and batch-specific qualification. | Fixed in section 06 and DATA-007. |
| R2-03 | MAJOR | A simulated label is duplicated into measured data, then re-enters a holdout through a derived property. | Follow transitive label lineage; include source revisions and derived/simulation parents in split audits. | Fixed in sections 06/11. |
| R2-04 | MAJOR | Temperature-error promotion ignores threshold-region errors; impressive global MAE is irrelevant near the proposed target. | Require declared threshold-region reporting and distinguish broad ranking from fine boundary decisions. | Fixed in sections 10/11. |
| R2-05 | MAJOR | A selector double-spends a test or retries an unknown external submission, and caching ignores engine/model changes. | Implement action identities, reservation/settlement, state transitions and recovery without blind retries. | Fixed in sections 12/14 and AL-005. |
| R2-06 | MAJOR | Cheap actions maximize information about easy properties while critical unmodeled constraints never receive measurements. | Include an explicit eligibility/measurement ladder and gate-disqualifying tests; scope policy claims to measured endpoints. | Fixed in sections 13/14. |
| R2-07 | MAJOR | Prospective arms share new observations asymmetrically; adaptive comparisons then claim independent evidence. | Freeze information-sharing, allocation and inference rules; distinguish actual cost from attributed comparison cost. | Fixed in section 15. |
| R2-08 | MAJOR | A required Wolfram test silently skips on a host without a licence and CI goes green. | Require real headless Wolfram CI for core promotion; mock and licensed integration results are separate. | Fixed in sections 05/20. |
| R2-09 | MAJOR | No boundary separates trusted analysis from document instructions, unsafe deserialization or untrusted external executables. | Treat source contents as inert; require reviewed executable adapters, strict parsing and validated artifacts. | Fixed in sections 07/12/20. |
| R2-10 | MAJOR | Raw data links rot or a corrected source silently changes a prior decision. | Immutable manifests, corrections with supersession and invalidation/recomputation of affected evidence. | Fixed in sections 06/20 and REL-004. |
| R2-11 | MINOR | Optional engines block all downstream epics through broad dependency edges. | Make capability-specific dependencies explicit; core screening must run with evidence and baselines alone. | Fixed in sections 05/18. |

Review conclusion: the research logic is now materially clearer. Jira decomposition still needs precise work-package boundaries, scope ownership, external prerequisites and an explicit conversion checklist.


---

# Red-team cycle 3 — Jira/AWF executability and final consistency

Input: `revisions/Specification_v0.3.md`. Method: adversarial self-review of decomposition, dependency order, release scope and exact workflow compatibility, then a final substantive rewrite. This is the third requested review/rewrite cycle; final mechanical QA follows without being represented as an additional independent review.

| Finding | Severity | Failure scenario | Required correction | Disposition in final v1.0 |
|---|---|---|---|---|
| R3-01 | MAJOR | E00 contains actual adoption readiness while E01 needs E00 to begin; an epic-level all-done dependency can create a setup cycle. | Put actual target adoption in E01, leave E00 as the planning baseline and distinguish local setup from governed dispatch. | Fixed in sections 16/18/19 and backlog dependencies. |
| R3-02 | MAJOR | E12/E14 require prospective E11, blocking an offline research release when laboratory access is absent. | Define milestone-specific acceptance; let core reporting/release run without prospective claims. | Fixed in sections 18/22 and machine-readable work packages. |
| R3-03 | MAJOR | Requirement IDs alone do not produce bounded worker assignments; path ownership, deliverables and prerequisite types remain unclear. | Emit work-package seeds with IDs, requirements, intended scope, outputs, validation plans, risk/closure proposals and dependencies. | Fixed in backlog JSON and sections 18/19. Seeds remain planning-only. |
| R3-04 | MAJOR | Scientific non-promotion could be mistaken for an unsatisfied software dependency, forcing workers to achieve positive findings. | Distinguish completed analysis artifacts from scientifically enabled model capabilities and make downstream fallbacks explicit. | Fixed in sections 16/18/22. |
| R3-05 | MAJOR | A generic AWF contract might leak project-specific fields into a closed revision-3 schema or use fabricated hashes/IDs. | Define an explicit field mapping and a separate project sidecar; validate actual records only after bindings exist. | Fixed in section 19 and planning-file metadata. |
| R3-06 | MAJOR | Substantial scientific methods could be treated as low-risk documentation simply because the edited path is docs/. | Recommend Tier 2 for criterion/threshold/protocol/analysis changes and configure actual specialist coverage. | Fixed in section 19; future role configuration remains visible. |
| R3-07 | MAJOR | Proposed model thresholds could look like established scientific standards; small family counts could be hidden inside pooled sample totals. | Declare project thresholds as preregistered choices, distinguish substance/cluster/family counts and limit each claim to its test design. | Fixed in sections 10/11 and decision register. |
| R3-08 | MAJOR | Final draft could overclaim AWF installation, implementation testing or independent review after merely reading source files. | Add a verified/not-performed evidence statement and retain all review provenance. | Fixed in sections 22/24 and source snapshot record. |
| R3-09 | MINOR | Users need a concrete first implementation sequence and rough work sizing without invented commercial estimates. | Add a first-wave ticket order, size bands and re-estimation conditions. | Fixed in section 18 and backlog metadata. |
| R3-10 | MINOR | Artifact validation checks are not specified for the deliverable itself. | Check requirement/work-package coverage, dependency acyclicity, IDs, links, AWF field mapping, and package hashes. | Resolved by final QA; results shipped as validation evidence. |

Review conclusion: the final document is suitable as a detailed planning baseline for Jira decomposition. Actual project bindings, accepted profiles, budgets, runtime capabilities, independent implementation review and laboratory evidence are explicitly future work. No document review can establish those operational/scientific facts.

