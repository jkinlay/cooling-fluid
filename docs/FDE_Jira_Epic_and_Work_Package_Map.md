# Jira Epic and Work-Package Map

Planning-only companion to the final specification. All items are DRAFT_NOT_DISPATCHABLE until actual project bindings, scope, evidence, commands and AWF validation exist. Work-package IDs are logical IDs, not Jira keys.

| Work package | Requirement | Increment | Predecessors | Deliverable |
|---|---|---|---|---|
| FDE-E00-W01 | FDE-GOV-001 | M0 | None | Freeze an explicit application profile |
| FDE-E01-W01 | FDE-GOV-002 | M0 | FDE-E01-W02, FDE-E00-W02 | Verify the controlling AWF |
| FDE-E00-W02 | FDE-GOV-003 | M0 | None | Separate engineering and scientific outcomes |
| FDE-E00-W03 | FDE-GOV-004 | M0 | None | Record responsibilities and resource limits |
| FDE-E01-W02 | FDE-RUN-001 | M0 | FDE-E00-W01, FDE-E00-W03 | Run core workflows without notebook state |
| FDE-E01-W03 | FDE-RUN-002 | M0 | FDE-E01-W02 | Validate all inter-component contracts |
| FDE-E01-W04 | FDE-RUN-003 | M0 | FDE-E01-W03 | Capture execution provenance |
| FDE-E01-W05 | FDE-RUN-004 | M0 | FDE-E01-W02 | Separate optional capability availability |
| FDE-E02-W01 | FDE-DATA-001 | M1 | FDE-E01-W03 | Preserve source provenance |
| FDE-E02-W02 | FDE-DATA-002 | M1 | FDE-E02-W01 | Preserve measurement semantics |
| FDE-E02-W03 | FDE-DATA-003 | M1 | FDE-E02-W02 | Deduplicate without destroying conflicting evidence |
| FDE-E02-W04 | FDE-DATA-004 | M1 | FDE-E02-W02 | Keep evidence classes separate |
| FDE-E02-W05 | FDE-DATA-005 | M1 | FDE-E02-W01, FDE-E02-W04 | Review machine-extracted evidence |
| FDE-E02-W06 | FDE-DATA-006 | M1 | FDE-E02-W03, FDE-E02-W04 | Audit data coverage and exclusions |
| FDE-E03-W01 | FDE-CHEM-001 | M1 | FDE-E01-W03 | Version chemical normalization |
| FDE-E03-W02 | FDE-CHEM-002 | M1 | FDE-E03-W01, FDE-E02-W02 | Represent samples and formulations |
| FDE-E03-W03 | FDE-CHEM-003 | M1 | FDE-E03-W01, FDE-E01-W06 | Version descriptors and capabilities |
| FDE-E03-W04 | FDE-CHEM-004 | M1 | FDE-E03-W01, FDE-E00-W01 | Freeze eligible candidate universes |
| FDE-E04-W01 | FDE-PHYS-001 | M1 | FDE-E02-W06, FDE-E03-W03 | Implement a physical reference baseline |
| FDE-E04-W02 | FDE-PHYS-002 | M1 | FDE-E04-W01, FDE-E00-W01 | Evaluate the feasible region |
| FDE-E04-W03 | FDE-PHYS-003 | EXT | FDE-E03-W02, FDE-E04-W01 | Model mixture phase behavior explicitly |
| FDE-E04-W04 | FDE-PHYS-004 | M1 | FDE-E02-W02, FDE-E00-W01 | Preserve system-dependent endpoints |
| FDE-E05-W01 | FDE-VAL-001 | M1 | FDE-E02-W07, FDE-E03-W04 | Prevent correlated-label leakage |
| FDE-E05-W02 | FDE-VAL-002 | M1 | FDE-E05-W01, FDE-E01-W04 | Freeze information available to evaluation |
| FDE-E05-W03 | FDE-VAL-003 | M1 | FDE-E05-W02, FDE-E04-W01 | Compare valid baselines |
| FDE-E05-W04 | FDE-VAL-004 | M2 | FDE-E05-W02, FDE-E03-W04 | Replay sequential policies honestly |
| FDE-E05-W05 | FDE-VAL-005 | M1 | FDE-E05-W03 | Report inconclusive evaluations |
| FDE-E06-W01 | FDE-ML-001 | M1 | FDE-E05-W03, FDE-E03-W03 | Train reproducible baseline property models |
| FDE-E06-W02 | FDE-ML-002 | M1 | FDE-E06-W01 | Condition predictions on physical context |
| FDE-E06-W03 | FDE-ML-003 | M1 | FDE-E06-W01, FDE-E05-W05 | Calibrate uncertainty and abstention |
| FDE-E06-W04 | FDE-ML-004 | M1 | FDE-E06-W03 | Handle joint constraints and missing properties |
| FDE-E06-W05 | FDE-ML-005 | M2 | FDE-E06-W01, FDE-E04-W01 | Compare physics-assisted learning fairly |
| FDE-E07-W01 | FDE-SIM-001 | M2 | FDE-E01-W05, FDE-E03-W03 | Declare engine capabilities and requirements |
| FDE-E07-W02 | FDE-SIM-002 | M2 | FDE-E07-W01, FDE-E04-W01 | Validate calculations against references |
| FDE-E07-W03 | FDE-SIM-003 | M2 | FDE-E07-W01, FDE-E01-W04 | Bound computation and handle failures |
| FDE-E07-W04 | FDE-SIM-004 | M2 | FDE-E07-W02, FDE-E07-W03 | Avoid invalid cross-engine reuse |
| FDE-E08-W01 | FDE-SCR-001 | M1 | FDE-E00-W01, FDE-E04-W04, FDE-E01-W03 | Evaluate hard constraints without compensation |
| FDE-E08-W02 | FDE-SCR-002 | M1 | FDE-E08-W01, FDE-E03-W04 | Maintain traceable screening decisions |
| FDE-E08-W03 | FDE-SCR-003 | M1 | FDE-E08-W02, FDE-E06-W04 | Generate interpretable trade-off sets |
| FDE-E08-W04 | FDE-SCR-004 | M1 | FDE-E08-W02 | Separate exploration from qualification |
| FDE-E09-W01 | FDE-AL-001 | M1 | FDE-E08-W04 | Select measurement actions under cost |
| FDE-E09-W02 | FDE-AL-002 | M2 | FDE-E09-W01, FDE-E05-W04, FDE-E09-W04, FDE-E09-W05 | Compare sequential selection policies |
| FDE-E09-W03 | FDE-AL-003 | M1 | FDE-E09-W01 | Respect batching and pending work |
| FDE-E09-W04 | FDE-AL-004 | M1 | FDE-E09-W03, FDE-E01-W04 | Reproduce the selection history |
| FDE-E10-W01 | FDE-LAB-001 | M3 | FDE-E00-W01, FDE-E01-W03 | Specify executable measurement requests |
| FDE-E10-W02 | FDE-LAB-002 | M3 | FDE-E10-W01, FDE-E02-W04, FDE-E03-W02 | Validate experimental intake |
| FDE-E10-W03 | FDE-LAB-003 | M3 | FDE-E10-W01, FDE-E04-W04 | Characterize relevant failure mechanisms |
| FDE-E10-W04 | FDE-LAB-004 | M3 | FDE-E10-W02 | Preserve protocol deviations and outcomes |
| FDE-E11-W01 | FDE-EXP-001 | M3 | FDE-E10-W03, FDE-E09-W02 | Freeze prospective comparison design |
| FDE-E11-W02 | FDE-EXP-002 | M3 | FDE-E11-W01, FDE-E09-W05 | Track actual experiment resources |
| FDE-E11-W03 | FDE-EXP-003 | M3 | FDE-E11-W02, FDE-E10-W04 | Evaluate prospective scientific outcomes |
| FDE-E12-W01 | FDE-REP-001 | M1 | FDE-E08-W03 | Produce candidate evidence dossiers |
| FDE-E12-W02 | FDE-REP-002 | M1 | FDE-E12-W01, FDE-E05-W05 | Produce gate decisions with rationale |
| FDE-E12-W03 | FDE-REP-003 | M1 | FDE-E12-W02 | Create reproducible research exports |
| FDE-E13-W01 | FDE-EXT-001 | EXT | FDE-E06-W03, FDE-E09-W02 | Gate generative and RL extensions |
| FDE-E13-W02 | FDE-EXT-002 | EXT | FDE-E07-W02, FDE-E06-W03 | Gate learned simulation extensions |
| FDE-E14-W01 | FDE-REL-001 | M1 | FDE-E12-W03, FDE-E01-W06, FDE-E09-W04, FDE-E09-W05 | Package independent rerun evidence |
| FDE-E14-W02 | FDE-REL-002 | M1 | FDE-E14-W01 | Complete requirements-to-evidence traceability |
| FDE-E14-W03 | FDE-REL-003 | M1 | FDE-E01-W01, FDE-E14-W02 | Prepare AWF handoff without bypassing approval |
| FDE-E01-W06 | FDE-RUN-005 | M0 | FDE-E01-W03 | Implement cross-runtime operation envelopes |
| FDE-E02-W07 | FDE-DATA-007 | M1 | FDE-E02-W03, FDE-E02-W04 | Preserve transitive lineage and corrections |
| FDE-E09-W05 | FDE-AL-005 | M1 | FDE-E09-W03 | Account for actions and unknown outcomes |
| FDE-E14-W04 | FDE-REL-004 | M1 | FDE-E14-W01 | Verify artifact recovery and scientific claims |

Each package has full scope, evidence, review and conversion metadata in `FDE_Requirements_and_Backlog.json`. Later increments and optional methods are not prerequisites for an honest offline release.
