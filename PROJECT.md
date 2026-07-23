# Project

## Promise

Flyto2 Flow turns an operator-owned visual workflow into a locally executed MCP
tool without requiring a second hand-written server or a vendor account.

## Problem

Workflow builders and agent tools are often separate systems. Teams design an
automation in one place, then repeat its input contract, transport, access
rules, execution code, and observability in an MCP server. The two surfaces
drift, failures become difficult to explain, and a supposedly self-hosted tool
can retain hidden hosted dependencies.

Flyto2 Flow keeps the workflow and tool contract together:

```text
visual workflow + MCP trigger = discoverable local agent tool
```

## Audience

- developers building repeatable tools for MCP-compatible agents;
- operators who need browser and API automation on controlled infrastructure;
- small teams that value inspectable local execution over hosted collaboration;
- security-conscious evaluators who need explicit access and edition borders.

## Core Outcomes

1. A new operator can start the local product with one documented Compose
   command and no account.
2. A workflow author can create, test, expose, call, and audit an MCP tool from
   one product.
3. A reviewer can identify a tool's source workflow, input contract, risk,
   approval policy, and evidence references.
4. A maintainer can prove that hosted identity, billing, telemetry, and managed
   execution did not enter the baseline.

## Scope

The source-available baseline owns:

- the Vue visual workflow and template builder;
- the local FastAPI application and Streamable HTTP MCP endpoint;
- the loopback-only stdio bridge;
- local execution through `flyto-core`;
- SQLite-backed workflows, variables, execution records, evidence, and replay;
- browser runtime packaging and offline core updates;
- boundary, dependency, license, SBOM, test, and build gates.

It does not own hosted identity, organizations, billing, marketplace features,
remote collaboration, telemetry, or a managed runner. See
[`docs/edition-matrix.md`](docs/edition-matrix.md).

## Product Principles

- **Local by default:** no account, implicit outbound request, or public bind.
- **One contract:** workflow inputs generate the MCP tool schema.
- **Evidence over claims:** important behavior must be inspectable in code,
  tests, metadata, or run artifacts.
- **Safe extension:** Cloud consumes the baseline through an explicit allowlist;
  hosted concerns never leak upstream.
- **Honest licensing:** current revisions are source-available, not described as
  OSI-approved open source.

## Success Measures

Repository-level success is measured by reproducible outcomes rather than star
counts alone:

- first local start and first tool call are documented and tested;
- all repository verification gates pass on every main-branch change;
- issues contain enough evidence to reproduce or evaluate the request;
- releases document operator action, compatibility, and rollback;
- public claims remain linked to implemented source or tests.

Community growth is tracked as a downstream result: successful first runs,
useful issues, repeat contributors, published workflows, references from other
projects, and stars earned after users understand the product.
