# Source Map

Flyto2 Flow keeps product source under `src/ui/web`.

## Backend

`src/ui/web/backend` is the local FastAPI application.

| Path | Ownership |
| --- | --- |
| `main_offline.py` | Accountless application assembly and local lifecycle |
| `api/` | HTTP and WebSocket product surfaces |
| `gateway/` | Provider seams, capabilities, and local persistence |
| `services/runtime/` | Workflow validation and execution coordination |
| `services/template/` | Workflow schema, conversion, layout, and validation |
| `mcp_server.py` | Workflow discovery, MCP schemas, stdio bridge, and tool calls |
| `local/` | Offline storage, core loading, static files, and reload lifecycle |

The backend depends on an installed `flyto-core`. Do not duplicate core module
behavior in this repository.

## Frontend

`src/ui/web/frontend` is the Vue 3 and Vite application.

| Path | Ownership |
| --- | --- |
| `src/views/` | Route-level product screens |
| `src/features/mcp/` | MCP Studio view-model and styling |
| `src/components/` | Workflow, execution, evidence, and shared UI components |
| `src/composables/` | Stateful UI behavior and workflow editing operations |
| `src/api/` | Typed-by-convention local API clients and normalization |
| `src/stores/` | Pinia state grouped by product domain |
| `src/i18n/` | Bundled locale catalogs and local overrides |

Frontend code renders backend-computed behavior. Access, validation, execution,
and edition enforcement remain server-side.

## Change Rules

1. Search and assess impact with Flyto2 Indexer before deep changes.
2. Read [`../ARCHITECTURE.md`](../ARCHITECTURE.md) and the edition-boundary
   documents before changing a shared or runtime surface.
3. Keep generic behavior in Flow and hosted behavior downstream.
4. Add focused tests beside the affected layer.
5. Run `make verify` and strict Indexer verification before merge.
