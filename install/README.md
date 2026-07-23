# Flyto2 Flow Deployment Files

This directory contains the reviewed inputs for the source-available,
self-hosted Flyto2 Flow image and Docker Compose deployment.

## Supported Path

Run Compose from the repository root so build context, environment files, and
relative paths resolve consistently:

```bash
cp install/.env.ce.example install/.env.ce
docker compose --env-file install/.env.ce -f install/docker-compose.ce.yml up --build
```

The default port binding is `127.0.0.1:9000:9000`. The named
`flyto-flow-data` volume stores the local database and execution artifacts.
Do not add `--volumes` to `docker compose down` unless that workspace is meant
to be deleted.

## File Ownership

| Path | Purpose |
| --- | --- |
| `.env.ce.example` | Reviewed local configuration template without secrets |
| `docker-compose.ce.yml` | Loopback-first service, volume, and health-check contract |
| `Dockerfile.ce` | Reproducible application, Flyto2 Core, Playwright, and Chromium image |
| `check-bundled-browser.py` | Release check for the packaged browser runtime |

Only `.env.ce.example` belongs in version control. Keep `install/.env.ce`
local, use strong values for access guards, and never put credentials in the
Compose file or workflow definitions.

## Verify A Build

The complete repository gate builds the frontend, runs backend and frontend
tests, audits dependency licenses, and regenerates the CycloneDX SBOM:

```bash
make verify
```

For an image-level release check, build the CE image through the repository's
release workflow and confirm `/api/health`, the bundled browser, persistent
storage, and loopback access before publishing an image digest.

See [Getting Started](../docs/getting-started.md) for operator steps,
[Architecture](../ARCHITECTURE.md) for runtime boundaries, and
[Security Policy](../SECURITY.md) before changing network exposure.
