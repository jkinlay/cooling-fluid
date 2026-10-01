# Jira status reconciliation — CFD-1

The owner directly instructed the controller on 1 October 2026 to update each Jira ticket as work progresses. This log records manual connector actions while AWF's configured Epic selector is empty. It is not an AWF lifecycle record or evidence that automatic Jira mirroring is enabled. Read Jira again before each subsequent transition; do not transition the Epic.

| Ticket | Pre-write observation | Action | Post-write observation | Reason |
| --- | --- | --- | --- | --- |
| [CFD-2](https://jkinlay.atlassian.net/browse/CFD-2) | Backlog, read via Atlassian connector on 2026-10-01 | Transition ID 31, `In Progress`, one attempt | `In Progress`, Jira `updated` 2026-10-01T13:18:59.189+0100, read back via connector | W01 owner control accepted and independently reviewed; W02 three-profile research draft underway. |
| [CFD-3](https://jkinlay.atlassian.net/browse/CFD-3) | Backlog, read via Atlassian connector on 2026-10-01 | Transition ID 31, `In Progress`, one attempt | `In Progress`, Jira `updated` 2026-10-01T13:29:06.708+0100, read back via connector | CFD-2 register v0.2 froze the three-profile baseline for bounded offline inventory; workbook/JSON reconciliation has started. |

CFD-4 through CFD-10 have no controller status transitions yet; their dependency gates and actual Jira states must be read when work starts. Jira's observed CFD-2 workflow offered Backlog, Selected for development, In Progress and Done; no In Review transition was observed. Keep the ticket In Progress during review unless the project workflow changes. Done requires actual task completion and owner-required closure, not merely a draft artifact.
