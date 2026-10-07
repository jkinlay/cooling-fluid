# AWF 1.9.1 GitHub acceptance adapter

Cooling Fluid Discovery uses the pinned AWF 1.9.1 release. Its read-only `status` command needs a host GitHub executable. GitHub's `2026-03-10` pull-request response omits `merge_commit_sha`, and PR #1's file response exceeds AWF's 1 MiB per-response limit because it includes patch bodies.

This project-owned host adapter lets the **unchanged** 1.9.1 verifier observe the same GitHub facts without relaxing its acceptance checks. It accepts only AWF's exact `gh api` GET invocation for this repository, verifies the SHA-256 of the official GitHub CLI executable, changes only pull-request detail requests to API version `2022-11-28`, and projects each PR-files page to every entry's `filename`, `status`, and `sha`. AWF still checks the receipt's exact blob SHA, merge ancestry, release pin, managed bytes, default-branch blobs, and final repository tip. The adapter has no write path.

AWF 1.9.2 `status` also reads repository rules. The allow-list therefore admits exactly two further GETs, both on this repository: `rules/branches/main?per_page=100&page=1..5` (effective branch rules) and `rulesets/{id}?includes_parents=true` (ruleset detail). Neither request is rewritten or projected; responses keep the 1 MiB bound.

## Build and run

Build with .NET 7, then copy the four `Awf191GhCompat` runtime files (`.exe`, `.dll`, `.deps.json`, `.runtimeconfig.json`) to a directory **outside** the cooling-fluid checkout. AWF refuses a `--gh` executable inside the checkout.

```powershell
$source = 'tools/awf191-gh-compat'
dotnet build "$source/Awf191GhCompat.csproj" -c Release
$external = Join-Path $env:TEMP 'awf191-gh-compat'
New-Item -ItemType Directory -Path $external -Force | Out-Null
Copy-Item "$source/bin/Release/net7.0/Awf191GhCompat.*" $external -Force
```

Set `AWF191_GH_EXE` to the absolute path of the verified GitHub CLI 2.102.0 `gh.exe` (SHA-256 `756724853cc579510b58e65e7a7429ad6b1af29cf99ef19b3a95f3b701c5c580`). Supply authentication to the official CLI through the host's existing credential mechanism or a process-only `GH_TOKEN`. From an up-to-date `main` checkout, run:

```powershell
$env:AWF191_GH_EXE = 'ABSOLUTE_PATH_TO_PINNED_GH_EXE'
python -B -I .agentic/scripts/workflow.py status --json --adoption-pr 1 --gh "$external/Awf191GhCompat.exe" --release-source ABSOLUTE_EXTERNAL_AWF_1_9_1_SOURCE --expected-manifest-sha256 d10a180af0109ffda59f70d925dd934c8fb78d9a8016d7ca39086d715f1194bd
Remove-Item Env:AWF191_GH_EXE
```

The release source must be the independently approved 1.9.1 source outside this checkout. The `status` command recomputes acceptance on each run. The adapter does not enable Jira writes, live review, scheduling, or merge authority. Replace this adapter only through a reviewed change when a published AWF release can observe these responses directly.