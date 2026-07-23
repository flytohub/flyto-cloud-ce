# Use Cases

These patterns show where a visual, locally executed, MCP-callable workflow is
useful. They are workflow shapes, not claims that every external service is
available without configuration.

## Browser Research With Evidence

**Pain:** an agent can summarize a page, but the operator cannot tell which
page state, interaction, or extracted value produced the answer.

**Workflow shape:**

```text
MCP input -> validate URL -> open browser -> interact -> extract -> normalize -> return
                                      |
                                      +-> screenshots / DOM evidence
```

**Good fit:** release-note collection, public catalog checks, support research,
and repeatable web QA.

**Guardrails:** constrain allowed destinations, respect site terms and robots
policies, avoid personal data, use conservative rates, and require approval
before any state-changing browser action.

## API Triage Tool

**Pain:** an operator repeats several API calls and manual transforms whenever
an incident or customer question arrives.

**Workflow shape:**

```text
typed identifier -> authenticated HTTP calls -> branch on status -> normalize -> summary
```

**Good fit:** read-only service health, issue enrichment, deployment lookup, and
cross-system status summaries.

**Guardrails:** store credentials through the credential service, redact
response secrets, set timeouts, and distinguish a partial result from success.

## Human-Approved Side Effect

**Pain:** an agent can prepare an action, but the final write should not occur
without an operator reviewing the exact target and payload.

**Workflow shape:**

```text
collect -> validate -> prepare preview -> approval breakpoint -> execute -> evidence
```

**Good fit:** publishing, ticket updates, notification sends, or controlled
configuration changes.

**Guardrails:** show the complete side effect before approval, bind approval to
the prepared payload, fail closed on expiry, and retain the decision with run
evidence.

## Local File Pipeline

**Pain:** documents or exports must be processed on operator-controlled storage
rather than uploaded to a workflow vendor.

**Workflow shape:**

```text
local path -> validate scope -> read -> transform -> write new artifact -> report
```

**Good fit:** structured export cleanup, local report generation, metadata
normalization, and repeatable development tasks.

**Guardrails:** restrict roots, reject traversal, write to a new path before
replacement, avoid logging file contents, and back up irreplaceable input.

## Agent Tool From an Existing Workflow

**Pain:** a tested workflow already exists, but making it available to an agent
would normally require another service and duplicated schema.

**Workflow shape:**

```text
existing workflow -> add MCP trigger -> define typed inputs -> test -> connect client
```

**Good fit:** any stable local workflow with one clear outcome and a bounded
input contract.

**Guardrails:** treat names and required fields as API contracts, keep responses
small, version breaking changes, and use risk and approval metadata honestly.

## When Not to Use Flow

Choose another design when:

- the requirement is a hosted multi-tenant collaboration product;
- an unauthenticated public webhook must be operated directly on the internet;
- a hard real-time or safety-critical controller is required;
- the task is simpler and safer as a short reviewed script;
- the operator cannot comply with the target system's terms, privacy rules, or
  applicable law.

Flyto2 Flow reduces integration glue; it does not remove the need to design
permissions, failure behavior, data handling, and human control.
