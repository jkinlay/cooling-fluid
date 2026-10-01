# M0 usage ledger — CFD-1

The owner initially accepted a shared ceiling of 40 research hours, eight owner-review hours (at most four per week), and £0 external spend on 1 October 2026. Later that day the owner raised **only the shared research-hour ceiling to 120**; the dated amendment is in [the study control](../feasibility/study_control.json). This ledger charges bounded work after acceptance across streams A, B, and C. Because minute-by-minute timers were not retained for the initial sessions, the entries below are **conservative rounded charges**, not measured durations. All subsequent work should log actual start/end times. If actual effort is later found higher, increase the charge; never use an estimate to extend the cap.

| Date | Work | Charged research hours | Owner-review hours | External spend | Evidence |
| --- | --- | ---: | ---: | ---: | --- |
| 2026-10-01 | W01 acceptance record, stop-rule checker and independent case review | 1.0 | 0 | £0 | `docs/feasibility/study_control.json`, `study_control_case_results.json` |
| 2026-10-01 | W02 three-profile source review, register, cases and independent review | 2.0 | 0 | £0 | `docs/feasibility/application_comparison.md`, `acceptability_register.json` |
| 2026-10-01 | W03 initial read-only workbook/JSON reconciliation and limited independent review | 1.0 | 0 | £0 | Local controlled `docs/feasibility/m0_working/` evidence; CFD-3 remains In Progress |

**Balance at 2026-10-01 13:35 BST:** 4.0 of 40 research hours charged; 36.0 remain. Owner-review: 0 of eight hours charged, with 0 of four charged this week. External spend: £0 of £0. The five-working-day/20-hour checkpoint has not been reached. This balance is provisional pending more precise time capture and should be reviewed before further dispatch. The control record's `actual_research_hours: 0` is its acceptance-time snapshot, not this live ledger.

The balance above is the historical snapshot under the initial 40-hour cap. The owner subsequently authorized 120 shared research hours. Later charged work and the effective remaining balance are reconciled in the controller's local working addendum pending review; the original 13:35 snapshot is retained rather than restated as a current balance.
