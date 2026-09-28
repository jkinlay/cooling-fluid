# M0 — Feasibility and value study

Version 1.1 · Proposed procedures; study not performed.

M0 contains nine small desk tasks and no software prerequisite. Accept [the control record](M0_Study_Control_Template.json) before kickoff. The proposed timebox is ten working days, 40 research hours, eight owner-review hours, and zero external spend. Actual dates/capacity remain unaccepted. Use [the decision template](Feasibility_Decision_Template.json) at the deadline or cap.

A spreadsheet or small reproducible script is permissible. Do not build a platform to execute this phase. Quotes/reviewer contact require separate outreach authorization; their absence must remain explicit. No fluid-handling or experimental procedure is authorized.

For each acceptance case, retain its input scenario, procedure, expected and observed outcome, PASS/FAIL/UNKNOWN, reviewer, date and evidence reference. The cases below define future acceptance; none has been run as a scientific study by this amendment.

Candidate/hazard table fields: profile/version; identity/CAS/structure policy; sample/purity where known; supplier and dated availability; original and normalized units; boiling/vapour-pressure conditions; flash point and method; LEL/UEL and autoignition where available; resistivity/breakdown method and conditions; SDS/GHS status; applicable chemical registration/restriction references; VOC, GWP/ODP and aquatic/environmental evidence; provenance; hard PASS/FAIL/UNKNOWN reasons; next evidence need. Missing fields remain unknown.

The value thesis is one page: buyer/use case; artifact to deliver; why existing solutions do not resolve it; evidence of the problem versus assumptions; smallest saleable/useful milestone; competing approaches; estimated cost scenarios with provenance; route (commercial or consciously chosen research/public-good); IP/publication decision. It is not a full business plan.

## FDE-E15-W01 / FDE-FEAS-001 — Bind the study mandate, capacity and stop rules

Agree the question, named decision owner, elapsed-time limit, research hours, owner review capacity, spend limit and outcome rules before starting the study.

Dependencies: None. Proposed risk tier: 2.

Outputs: `study_control.json`, `stop_rule_register.md`.

Read each control field against the owner acceptance record; calculate consumed/remaining hours and the deadline; apply the rules to the three supplied scenarios.

| Case | Procedure and expected result |
|---|---|
| Positive | Inspect a control record with a named accountable owner, accepted start/deadline, hours and spend caps, review capacity and rules for STOP_DOMAIN, INCONCLUSIVE and CONTINUE. Confirm every field has explicit owner acceptance and a dated evidence reference. |
| Negative | Present a record with an absent owner, null deadline or missing spend cap. It must remain PROPOSED_NOT_STARTED and cannot authorize research dispatch or spending. |
| Boundary | Present a record exactly at its hours or calendar cap with unresolved evidence. Further work is blocked pending a dated decision; zero authorized spend permits public desk research only. |

## FDE-E15-W02 / FDE-FEAS-002 — Compare application profiles and acceptance constraints

Compare two-phase immersion, single-phase immersion and two-phase direct-to-chip before choosing the initial application.

Dependencies: FDE-E15-W01. Proposed risk tier: 2.

Outputs: `application_comparison.md`, `acceptability_register.json`.

Use one comparison row per application; open every cited requirement source; distinguish adopted requirements, proposals, vendor claims and unanswered questions; apply the three-state decisions.

| Case | Procedure and expected result |
|---|---|
| Positive | For each of the three applications, trace temperature/pressure, fluid-contact boundary, electrical and fire requirements to a named source or responsible decision-maker. Record jurisdiction, standard edition/clause where obtained, equipment arrangement, buyer/OEM requirements and insurer status separately. |
| Negative | Present a generic assertion that NFPA bans all flammable cooling fluids, a manufacturer aspiration treated as deployment evidence, or a PFAS-free label treated as fluorine-free. Reject the unsupported inference and record UNKNOWN. |
| Boundary | For a profile with physical limits documented but insurance acceptance unresolved, retain RESEARCH_DRAFT; it cannot be marked commercially deployable. An explicitly scoped offline study may investigate the uncertainty. |

## FDE-E15-W03 / FDE-FEAS-003 — Assemble a bounded candidate and source inventory

Produce an auditable inventory of the searched catalogues, chemical families, identities and measurements without claiming an exhaustive universe.

Dependencies: FDE-E15-W02. Proposed risk tier: 1.

Outputs: `candidate_inventory.json`, `search_coverage.md`, `source_register.json`.

Audit the search log and selected rows against their sources; recompute only documented unit conversions; report numbers searched, deduplicated, excluded and unresolved. Do not set scientific acceptance limits in this task.

| Case | Procedure and expected result |
|---|---|
| Positive | Select one included record, one excluded record and one missing-property record; reproduce each from its source locator and retrieval date. Verify identities, original units, measurement conditions and searched scope are retained. |
| Negative | Seed duplicate synonyms, an unsupported supplier-availability claim and an unsourced property. Mark the duplicate linkage, quarantine the unsupported value and retain the availability uncertainty. |
| Boundary | A catalogue search returns zero matches, or a measurement lies exactly on a proposed boiling limit. Record the search boundary, uncertainty and explicit inclusive/exclusive rule; do not claim no such chemical exists globally. |

## FDE-E15-W04 / FDE-FEAS-004 — Evaluate chemical feasibility and hazards before software

Use existing evidence to identify hard failures, plausible investigation candidates and missing evidence for each application profile.

Dependencies: FDE-E15-W02, FDE-E15-W03. Proposed risk tier: 2.

Outputs: `feasibility_table.json`, `hazard_regulatory_register.json`, `feasibility_memo.md`.

Review every decisive exclusion and at least one unresolved case against primary evidence; distinguish measured values, correlations and predictions; have the chemistry/thermal reviewers challenge the inference. No chemical handling is part of this desk task.

| Case | Procedure and expected result |
|---|---|
| Positive | For each candidate-profile pair, record each hard constraint as PASS, FAIL or UNKNOWN with evidence. Include flash-point method, LEL/UEL and autoignition where available, electrical-property conditions, GHS/SDS information, jurisdiction-specific chemical status, VOC/environmental evidence and procurement status. |
| Negative | Seed a measured fire-limit failure plus excellent heat-transfer data. The hard failure must persist. Seed a missing resistivity or toxicity value; it must remain UNKNOWN rather than passing or being imputed from molecular identity. |
| Boundary | If every candidate in the declared universe has a documented hard failure, recommend STOP_DOMAIN for that universe/profile. If plausible candidates remain but decisive measurements are missing, report INCONCLUSIVE with a bounded evidence request, not proof of infeasibility. |

## FDE-E15-W05 / FDE-FEAS-005 — Define buyer value, competition and publication policy

Write a one-page value thesis specifying buyer/use case, deliverable, differentiation, evidence needed to be useful, alternative solutions and an IP/publication route.

Dependencies: FDE-E15-W02. Proposed risk tier: 2.

Outputs: `value_thesis.md`, `competition_evidence.md`, `publication_policy.json`.

Complete the one-page thesis and evidence table; record remaining buyer assumptions, information sensitivity, publication authority and alternatives. Obtain legal input for specific patent decisions rather than infer patentability from this document.

| Case | Procedure and expected result |
|---|---|
| Positive | Trace each proposed buyer problem and competitor claim to a dated source, and distinguish a buyer hypothesis from buyer validation. Identify a specific first useful artifact and why it could matter beyond a generic screening platform. |
| Negative | Present an unsupported market-share figure, assume a two-phase direct-to-chip vendor is an immersion buyer, or label a public methodology automatically unpatentable. Mark the claim unsupported and prevent it from deciding the thesis. |
| Boundary | If no commercial route is supported, permit an explicitly owner-chosen, capped research/public-good objective or STOP/INCONCLUSIVE; do not label it a validated commercial opportunity. Undecided IP strategy blocks new candidate-level publication. |

## FDE-E15-W06 / FDE-FEAS-006 — Establish laboratory access and indicative cost bounds

Collect two independent indicative laboratory capability/cost responses where obtainable and record an affordable validation path or a clearly blocked physical route.

Dependencies: FDE-E15-W02, FDE-E15-W05. Proposed risk tier: 1.

Outputs: `laboratory_feasibility.md`, `cost_envelope.json`, `quote_register.json`.

Check documentary evidence and sum itemized scenario costs with assumptions. Obtaining new responses requires separately authorized outreach; no email, booking or purchase is authorized by this planning record. Record unavailable quotations honestly.

| Case | Procedure and expected result |
|---|---|
| Positive | For each response retain provider/date, relevant methods, sample amounts, controls, inclusions/exclusions, currency, taxes/shipping/disposal assumptions, rig scope, lead time and validity. Compare both with the proposed first useful artifact. |
| Negative | Seed an invented quotation, an unpriced custom rig or an assay listed as available without provider evidence. The physical route remains uncosted/blocked; do not replace missing data with a claimed minimum price. |
| Boundary | With one or zero responses by the deadline, report missing evidence and use a bounded offline-only decision or INCONCLUSIVE. A quote is not an order or spend authorization; no laboratory work starts from this record. |

## FDE-E15-W07 / FDE-FEAS-007 — Obtain independent chemistry and thermal assessments

Obtain separate physical-chemistry and data-centre thermal/fire assessments with explicit permission to reject the premise.

Dependencies: FDE-E15-W04, FDE-E15-W05, FDE-E15-W06. Proposed risk tier: 2.

Outputs: `specialist_review_register.json`, `chemistry_assessment.md`, `thermal_assessment.md`.

Match review conclusions to the exact dossier hash and qualifications. Record who reviewed what, open objections and limitations; do not contact or engage a reviewer without separate authorization.

| Case | Procedure and expected result |
|---|---|
| Positive | Verify named reviewers, relevant expertise, scope, conflicts/independence, source dossier version and signed/attributed conclusions. Record objections and unresolved evidence separately from document edits. |
| Negative | Present an LLM self-review or an unassigned role placeholder as independent professional approval. Reject the attribution and retain the absent review as a gate limitation. |
| Boundary | One reviewer unavailable: an owner-attested limited offline investigation may be proposed, but independent scientific endorsement and authorization for physical work cannot be claimed. |

## FDE-E15-W08 / FDE-FEAS-008 — Audit the desk dossier and record dissent

Check source traceability, consistent profile IDs, financial assumptions and the disposition register without changing scientific thresholds.

Dependencies: FDE-E15-W03, FDE-E15-W04, FDE-E15-W05, FDE-E15-W06, FDE-E15-W07. Proposed risk tier: 1.

Outputs: `desk_audit.md`, `finding_dispositions.json`.

Follow the source and artifact references; reconcile issue dispositions to affected decision fields; preserve dissent and report all unavailable evidence. Tier 1 applies only to this clerical audit, not scientific adjudication.

| Case | Procedure and expected result |
|---|---|
| Positive | Reproduce an inclusion, exclusion and cost scenario; verify every external finding has an accepted, qualified, rejected or unresolved disposition with reasons and links. Confirm design amendments are not presented as completed experiments. |
| Negative | Seed a broken source reference, changed threshold without version increment and a missing quotation labelled received. Fail dossier completeness and return the affected item to its owner. |
| Boundary | A disputed finding remains open with named decision owner and impact. Do not fabricate a rejected finding to meet a quota; an unresolved decision-critical finding blocks full CONTINUE. |

## FDE-E15-W09 / FDE-FEAS-009 — Issue the dated feasibility and investment decision

Choose STOP_DOMAIN, INCONCLUSIVE or a precisely scoped CONTINUE from the dossier before authorizing platform implementation.

Dependencies: FDE-E15-W01, FDE-E15-W02, FDE-E15-W04, FDE-E15-W05, FDE-E15-W06, FDE-E15-W07, FDE-E15-W08. Proposed risk tier: 2.

Outputs: `feasibility_decision.json`, `feasibility_decision.md`.

Apply the predeclared rules in order to the actual dossier and the positive/negative/boundary scenarios; reconcile authorized package IDs and capability claims; write a dated decision and next review deadline. Preserve reasons for stop or scope change.

| Case | Procedure and expected result |
|---|---|
| Positive | A CONTINUE identifies the application/profile version, bounded candidate domain, credible evidence path, buyer/research purpose, funded or capped next scope, owner capacity, review status and specific work packages released. The owner signs the exact dossier revision. |
| Negative | Attempt CONTINUE using an empty eligible universe where all candidates have measured hard failures, an exhausted cap, missing decision owner, or undefined next work. It must be rejected; already-written software cannot override the gate. |
| Boundary | For plausible but unmeasured candidates, issue INCONCLUSIVE plus a separately bounded follow-up or CONTINUE_LIMITED_OFFLINE only when a specific useful offline artifact is justified. This does not release the full M1 backlog or authorize lab work. |
