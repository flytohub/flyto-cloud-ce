# Local Workflow Source And Cloud Sync Handoff

Date: 2026-07-23
Status: Active

## Result

Flow commit `79454c0` repaired Docker-local MCP access and persisted execution
storage, moved error-workflow resolution to the saved template store, restored
alert metric collection, corrected scoped dark-mode selectors, removed the
unused workflow CRUD/version frontend and backend surfaces, and added an
idempotent first-run HTTP GET MCP starter workflow.

The follow-up closure removes stale tests for the deleted API and adds CE
regressions for the new runtime contracts. Saved visual workflows, MCP tool
discovery, error-workflow references, and execution loading now share the
template store instead of observing two disconnected providers.

## Cloud Boundary

Only `src/ui/web/frontend/src/features/mcp/studio.css` changed inside
`FLOW_CLOUD_SYNC.json`. The guarded Flow-to-Cloud workflow created Cloud pull
request `#76` containing exactly that file. Backend persistence, local startup,
Docker paths, starter data, and offline routing remain Flow-owned and are not
copied into Cloud.

## Verification

The closure requires:

```bash
make verify
flyto-index verify . --strict
```

Focused regression commands:

```bash
npm --prefix src/ui/web/frontend run test:run -- tests/unit/api/workflows.spec.js
python -m pytest -q tests/ce/test_release.py
```

Remote completion requires a green Flow Verify and CodeQL run, a green and
merged Cloud sync pull request, no open synchronization pull request, and one
remaining `main` branch in each repository.
