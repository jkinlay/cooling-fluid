# M0 desk-study control and stream plan for CFD-1

The owner accepted the control in `docs/feasibility/study_control.json` on 1 October 2026 for public desk research through 14 October 2026. Its ten working days, 40 research hours, eight owner-review hours and £0 external spend are shared across all streams. This is the M0 mandate; it does not complete the analysis or activate AWF dispatch/Jira lifecycle writes.

The frozen existing baseline is `docs/feasibility/Cooling_Fluid_Candidate_Table.xlsx` (SHA-256 `888fa3d843d8b05c34f031dd0843b81dbee2f74a9fe991a7c5df828ab9d56fb2`) and `docs/feasibility/feasibility_table.json` (SHA-256 `517bcee853ab0e0c2eb1018068f816409899ce12e52c1b0600013fae4d1f3ea1`). These are prior public-source evidence, not M0 acceptance or fluid qualification.

See `stream_work_packets.md` for bounded planning scope and `docs/feasibility/stop_rule_register.md` for the accepted decision boundaries.

## Stream order

| Stream | Initial preparation | First eligible M0 work after control acceptance | Gate before later work |
| --- | --- | --- | --- |
| A | Review CFD-2 and bind the study control/profile questions | CFD-2: compare the three application profiles and identify adopted versus proposed constraints | W01 independent control-case review completed; profile decisions have source or named owner |
| B | Plan a read-only reconciliation of the existing 32-compound baseline | CFD-3: reconcile identities, observations and source records | CFD-2 register v0.2 frozen for offline inventory only (SHA-256 019CA9DE23AAC6766643BC7F289B7E8D3282B3E17CD7E7367FA838EC7EA38E44) |
| C | Check Wolfram runtime availability and design a raw Quantity/Missing export | CFD-4: run the exact-identity property-coverage audit | CFD-3 identities reconciled and CFD-2 requirements bound |

Later CFD-5/6/7 property, hazard and transport work can occupy separate streams only after their prerequisites and the shared study cap permit it. CFD-8/9/10 integrate, screen and decide after the evidence tasks. A configured stream is not a running agent or a permission to skip these dependencies.

AWF's Jira scope remains empty, so automatic lifecycle mirroring is inactive. Under the owner's explicit status-update instruction, the controller manually transitioned CFD-2 and CFD-3 from Backlog to In Progress on 1 October 2026 and verified both readbacks; see jira_status_log.md. The Epic and other tasks were observed in Backlog earlier that day. Read Jira before each later transition. No outreach, spending, laboratory action, or candidate-level publication is authorized by the accepted desk-study control.
