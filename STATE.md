# Current State

Last reviewed: 2026-07-23

This file records verified repository state, not a release promise. Use the
issue tracker and commit history for work completed after this date.

## Shipped

- Accountless local application with a Vue visual builder and FastAPI backend.
- Local workflow execution through installed `flyto-core`.
- MCP Studio with workflow-tool discovery, generated input forms, live calls,
  client configuration, and audit views.
- MCP stdio and Streamable HTTP surfaces with loopback-first access controls.
- Local workflows, templates, variables, execution records, evidence, replay,
  lineage, metrics, traces, and alerts.
- Saved workflow definitions now use the local template store as the single
  persistence surface. The disconnected workflow CRUD provider and frontend
  wrappers are no longer exposed.
- Empty first-run workspaces receive three idempotent MCP starter workflows:
  HTTP GET, browser screenshot, and JSON-to-CSV. Existing template libraries
  are not modified. Docker keeps workflow data and execution records on
  explicit persisted-volume database paths.
- Playwright and Chromium in the CE container image.
- SHA-256-verified offline `flyto-core` wheel import.
- Explicit Flow/Cloud ownership and synchronization contracts.
- Byte-identical Header interaction styles shared with Cloud while each edition
  retains its own routes and product actions.
- PolyForm Shield current license with preserved Apache-2.0 history.

## Verified

- Flyto2 Indexer full-project verification: 17 of 17 checks passed on
  2026-07-23.
- Flyto2 Indexer code-health audit: grade A, 91/100 on 2026-07-23.
- Secret scan: no findings during the same audit.
- CI covers boundary inventory, backend smoke, frontend tests and build,
  dependency licenses, SBOM generation, contribution terms, and container
  construction.
- CE regression coverage now locks all three starter contracts and idempotent
  seeding, template-backed error workflow resolution, current metrics
  collector, removed workflow CRUD routes, persisted execution database path,
  and scoped dark-mode selectors.
- The shared Flyto2 documentation contract now passes with a documentation
  index, feature/source manifest, workflow guides, and handoff registry.

These results describe one revision and must be regenerated after changes.
They are not a warranty that every workflow or external service will succeed.

## Deliberate Limits

- No hosted accounts, organizations, billing, marketplace, chat, analytics,
  telemetry, remote collaboration, or managed runner.
- No automatic runtime download when an appliance starts.
- No claim that current revisions are OSI-approved open source.
- No public-network exposure by default.

## Known Work

- Add tested importable workflow recipes for common browser and API jobs.
- Improve contributor-facing architecture references at complex runtime
  boundaries.
- Continue reducing high-complexity functions identified by the Indexer without
  changing public behavior.
- Establish a repeatable release artifact and compatibility verification path.

See [`ROADMAP.md`](ROADMAP.md) for priorities and [`tasks.md`](tasks.md) for the
maintainer queue.
