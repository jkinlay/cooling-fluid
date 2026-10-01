# Proposed M0 stream work packets for CFD-1

These packets are planning records. They are not AWF execution contracts, Jira transitions, or chemistry findings. The M0 control was accepted on 1 October 2026. All three streams share the limits in `docs/feasibility/study_control.json`. A packet becomes eligible only after its listed dependencies are accepted, a bounded ticket contract and independent reviewer are assigned, and the AWF controller confirms capacity and reservations. The dependency graph may leave fewer than three streams active at a time.

## Stream A — CFD-2 (FDE-FEAS-001 and FDE-FEAS-002)

**Prerequisite:** The owner accepted W01 control limits on 1 October 2026. W01 control cases and the stop-rule register passed independent review on 1 October 2026. W02 profile comparison used that accepted prerequisite; AWF dispatch remains separately gated.

**Scope:** Compare the three application profiles named in the M0 plan: two-phase immersion, single-phase immersion, and two-phase direct-to-chip. For each, record operating temperature and pressure ranges, wetted/contact boundaries, electrical constraints, fire and environmental constraints, material compatibility, and jurisdiction/OEM/insurer requirements. Mark each constraint `ADOPTED`, `PROPOSED`, or `UNKNOWN`; capture units, conditions, source or decision owner, and rationale. Do not treat a guessed limit as a hard gate.

**Proposed deliverables:** A versioned application-profile and constraint register, an evidence/source register, and a bounded list of unresolved owner decisions. CFD-3 and CFD-4 consume only accepted profile and identity scope.

**Acceptance evidence:** Every proposed hard constraint has an identified source or named decision owner; the three profiles remain distinct; the M0 control has an acceptance record and actual dates/caps.

## Stream B — CFD-3 / FDE-FEAS-003

**Prerequisites:** Accepted M0 control and CFD-2 register v0.2, SHA-256 `019CA9DE23AAC6766643BC7F289B7E8D3282B3E17CD7E7367FA838EC7EA38E44`, frozen for offline identity/source inventory only. The three profile states remain RESEARCH_DRAFT; no candidate judgement is enabled.

**Immutable inputs:** `docs/feasibility/Cooling_Fluid_Candidate_Table.xlsx` SHA-256 `888fa3d843d8b05c34f031dd0843b81dbee2f74a9fe991a7c5df828ab9d56fb2`; `docs/feasibility/feasibility_table.json` SHA-256 `517bcee853ab0e0c2eb1018068f816409899ce12e52c1b0600013fae4d1f3ea1`. The existing screen has 32 candidates, 164 observations, and 66 source records. It is exploratory public-source evidence, not M0 qualification.

**Scope:** Reconcile candidate ID, exact name, CAS, isomer/mixture specification, and any aliases across workbook, JSON and original references. Track each source's record, retrieval date and limitations. Preserve conflicts and absent identities as `UNKNOWN`; do not silently resolve an ambiguous identity or treat one boiling observation as proof of safety.

**Proposed deliverables:** New candidate inventory, source register, search/coverage log, and reconciliation report under `docs/feasibility/`, leaving the historical baseline unchanged.

**Acceptance evidence:** One auditable identity row per in-scope candidate; original source links and observed values remain traceable; disagreements and missing records are explicit; independent reviewer verifies the reconciliation.

## Stream C — CFD-4 (Wolfram coverage supporting FDE-FEAS-004)

**Prerequisites:** Accepted M0 control, CFD-2 property requirements, and CFD-3 resolved candidate identities.

**Read-only capability observation:** `wolframscript` resolves to WolframScript 1.4.0; installed Mathematica 13.3/14.0 and Wolfram 14.3/15.0 executable trees and base Chemistry components were observed. Kernel launch, licence, online connectivity, ChemicalData availability, and third-party chemistry paclets remain `UNOBSERVED`.

**Scope:** First validate the runtime without paid computation. For each exact candidate identity, record ChemicalData identity resolution as `EXACT`, `AMBIGUOUS`, `MISSING`, or `ERROR`. For exactly resolved identities, audit `BoilingPoint`, `VaporPressure`, `VaporizationHeat`, `Density`, heat capacity, `Viscosity`, `ThermalConductivity`, `DielectricConstant`, and `Resistivity` through ChemicalData and, where supported, ThermodynamicData. Unsupported property names and meanings are recorded explicitly. Preserve raw Wolfram expressions including `Quantity`, `Missing`, failures, and messages before normalization. Capture input/script hashes, executable and kernel version, query order, retrieval time, conditions, source attribution when actually provided, and output hashes. No silent synonym substitution or missing-value estimate.

**Proposed deliverables:** `docs/feasibility/wolfram_coverage/` containing input snapshot, identity-resolution records, raw responses, normalized coverage matrix, provenance register, run manifest and coverage audit.

**Acceptance evidence:** A complete response-status matrix for all CF001–CF032 rows in the hash-bound, accepted CFD-3 inventory × the nine Jira-required property concepts (including explicit missing/error responses for unresolved identities), raw-to-normalized traceability, reproducible hashes, and independent review. Coverage is a subordinate input to W04; W04 separately requires candidate-profile feasibility and hazard dispositions, its prescribed outputs, and chemistry/thermal review. Coverage alone does not revise the screening verdict or establish chemical safety.

## Later Jira sequence

CFD-5 (boiling/vapour/enthalpy), CFD-6 (fire/hazard), and CFD-7 (transport/electrical/compatibility) draw on the accepted identity, profile and coverage evidence and may use separate streams when the DAG allows. CFD-8 integrates the attributed dataset and CFD-9 screens each application profile. CFD-10 records specialist-review status and the bounded G0 decision only after W05 value/publication work, W06 cost/laboratory status, W07 independent professional review, and W08 dossier audit; unavailable inputs remain explicit. No ticket implies procurement, outreach, experiments, paid activity, or candidate-level public release.
