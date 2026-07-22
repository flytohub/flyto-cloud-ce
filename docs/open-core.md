# Flyto2 Flow Source-Available Upstream Model

Flyto2 Flow is the canonical source-available baseline. It contains the visual
workflow editor, local execution, local storage, evidence and replay, and MCP
delivery. It is a complete single-workspace product and does not depend on a
hosted Flyto2 service.

`flyto-cloud` is a downstream product. It may consume Flow releases and add
hosted product features in its own repository. Those additions are not edition
flags hidden inside Flow; their source stays downstream.

## Direction of change

```text
generic editor/runtime fix     Flyto2 Flow <-> guarded Cloud backport
hosted product capability      flyto-cloud only
```

Changes that apply to both products normally land in Flow first and then move
downstream. When a generic defect is discovered and fixed in Cloud, automation
may copy only the paths declared in `FLOW_CLOUD_SYNC.json` into a Flow pull
request. That pull request must remove every hosted dependency and identity
assumption and pass Flow purity, frontend, backend, container, contribution,
and CodeQL gates before merge. Automation never writes Flow `main` directly.

## Stable seams

- Frontend: `@edition` resolves to `src/edition/ce.js` by default. A downstream
  build may set `FLYTO_UI_EDITION_ENTRY` to its own adapter for additive routes,
  navigation, actions, page slots, banners, installation, and route guards.
  Shared pages and layout shells remain upstream files; an edition must not
  replace `AppNavbar`, `AppFooter`, or `MyTemplates` with a parallel UI.
- Backend: Flow owns `main_offline.py` and `create_offline_router()`. A
  downstream product composes a separate entry point and router; it must not
  add hosted routers to the Flow entry point.
- Data: Flow records are scoped to the fixed `local-workspace`. Downstream
  identity and organization schemas are separate migrations maintained
  downstream.

See [CE/Cloud Boundary](ce-cloud-boundary.md) for the enforceable rules.
