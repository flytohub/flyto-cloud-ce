# Roadmap

The roadmap is ordered by user outcome, not a promised date. A roadmap item is
complete only when behavior, documentation, tests, and edition-boundary checks
land together.

## Now: Make the First Useful Tool Obvious

- Ship small, importable browser and HTTP workflow examples with sanitized test
  fixtures.
- Validate the documented install-to-first-call path in CI.
- Improve errors for missing core runtime, invalid MCP triggers, and failed
  workflow calls.
- Keep every public capability claim tied to source, tests, or a reproducible
  command.

## Next: Make Tools Safer to Operate

- Make approval and evidence expectations easier to configure from the MCP
  trigger.
- Add focused export and retention controls for local run artifacts.
- Expand compatibility tests across supported MCP protocol versions and common
  clients.
- Document authenticated reverse-proxy patterns without weakening the
  loopback-only default.

## Later: Grow a Reusable Workflow Commons

- Define a versioned, reviewable workflow-package format.
- Add a community contribution path for recipes that includes provenance,
  permissions, expected output, and deterministic tests.
- Publish domain-focused examples for research, operations, data preparation,
  and human-approved actions.
- Improve discoverability by use case, required permission, and runtime cost.

This is a local recipe commons, not a hosted marketplace. Hosted discovery,
billing, organizations, and managed execution remain outside this repository.

## Ongoing Engineering

- Reduce complexity hotspots in small behavior-preserving changes.
- Keep dependencies pinned, licensed, audited, and represented in the SBOM.
- Preserve stored-data and API compatibility or document migration and rollback.
- Keep Flow canonical for every shared path in `FLOW_CLOUD_SYNC.json`.
- Review accessibility, responsive behavior, and localization with every
  frontend change.

## Not Planned for the Baseline

- hosted identity or organization membership;
- subscription billing or usage metering;
- remote team collaboration and chat;
- application telemetry or analytics phone-home;
- a Flyto2-managed workflow runner.

Proposals should start from a user problem, explain why it belongs in the local
baseline, and identify the smallest testable outcome. See
[`CONTRIBUTING.md`](CONTRIBUTING.md).
