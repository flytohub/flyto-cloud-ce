# First-Run Starter Templates

Flyto2 Flow seeds three working examples when a local workspace starts with an
empty template library. Each example is a saved workflow template with an MCP
trigger, a typed input, and the minimum steps needed to produce a useful
result.

The seed is intentionally conservative:

- it runs only when the template library is empty;
- it does not replace, rename, or duplicate existing templates;
- running startup again leaves the library unchanged;
- external network access occurs only when an operator runs a network-capable
  starter.

## HTTP GET Request Tool

Use this starter to turn a URL fetch into a typed MCP tool.

| Contract | Value |
| --- | --- |
| MCP tool | `http_get_tool` |
| Required input | `url` (`string`) |
| Steps | `flow.trigger` -> `core.api.http_get` |
| Default timeout | 30 seconds |
| TLS verification | Enabled |

Before using it with an agent, restrict the accepted destination or add an
approval step when the URL may come from untrusted input. Do not put
credentials directly in the URL or workflow definition.

## Browser Screenshot Tool

Use this starter to open a page in headless Chromium and save a PNG screenshot.

| Contract | Value |
| --- | --- |
| MCP tool | `screenshot_tool` |
| Required input | `url` (`string`) |
| Steps | `flow.trigger` -> `browser.ensure` -> `browser.goto` -> `browser.screenshot` -> `browser.close` |
| Viewport | 1280 x 720 |
| Output path | `screenshot.png` |

The navigation step enables SSRF protection and waits for
`domcontentloaded`. Review destination policy before exposing the tool beyond a
trusted local client. Keep `browser.close` in the workflow so completed and
failed test runs do not leave browser resources open.

## JSON to CSV Tool

Use this starter to convert an array of JSON records into a CSV artifact.

| Contract | Value |
| --- | --- |
| MCP tool | `json_to_csv_tool` |
| Required input | `records` (`array`) |
| Steps | `flow.trigger` -> `data.json_to_csv` |
| Output path | `csv_output.csv` |
| Defaults | Header included; nested values flattened |

Test mixed, missing, and nested fields before relying on the generated file as
an import contract for another system. Treat spreadsheet-bound text as
untrusted when a downstream application may interpret formulas.

## Use A Starter

1. Open **Templates** and select a starter.
2. Review the MCP trigger name, description, and typed input.
3. Replace example settings with the destination and policy required for one
   focused task.
4. Save the workflow and run it with non-sensitive test data.
5. Open **MCP Studio**, refresh discovery, and make a local test call.
6. Inspect the response, run history, and evidence before connecting an agent.

Starter templates are examples, not production policy. Add credentials through
the credential surface, place approval checkpoints before sensitive side
effects, and keep the default loopback-only network boundary unless remote
access is deliberately secured.

## Restore Missing Starters

Startup does not add starters to a non-empty library. This prevents upgrades
from modifying an operator's workspace. To recover an example, create a new
template with the contract above or test in a separate empty workspace. Do not
delete a production library merely to trigger the seed.

Implementation and regression coverage:

- `src/ui/web/backend/local/lifespan_local.py`
- `tests/ce/test_release.py::test_first_run_starter_template_seed_is_idempotent`
