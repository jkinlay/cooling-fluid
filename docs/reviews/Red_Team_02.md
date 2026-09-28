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
