# Test Guide

Flyto2 Flow uses focused backend boundary tests, frontend unit and integration
tests, release smoke scripts, and a container build.

## Baseline Tests

`tests/ce` verifies the source-available product boundary and repository-level
contracts.

```bash
DEPLOYMENT_MODE=offline python -m pytest -q tests/ce
```

## Frontend Tests

Vue behavior, API clients, stores, composables, and workflow integration live
under `src/ui/web/frontend/tests`.

```bash
npm --prefix src/ui/web/frontend ci
npm --prefix src/ui/web/frontend run test:run
npm --prefix src/ui/web/frontend run build
```

Run Playwright tests for changed end-to-end behavior and inspect desktop and
mobile screenshots for visible UI changes.

## Complete Gate

```bash
make verify
flyto-index scan .
flyto-index verify . --strict
```

A passing full suite does not replace a focused regression test. New behavior
should be proved at the smallest stable boundary, then covered by the complete
gate for integration confidence.
