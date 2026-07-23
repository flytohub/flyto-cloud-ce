# Contributing to Flyto2 Flow

## Find The Smallest Useful Change

- For a bug, start with the structured bug report and a minimal reproduction.
- For a feature, describe the user problem, smallest useful outcome, and why it
  belongs in the accountless self-hosted baseline.
- Keep one pull request focused on one behavior. Separate cleanup that is not
  required for the outcome.
- Ask in the issue before investing in a new subsystem, stored-data change,
  public API, or edition-boundary change.

## Before Opening A Change

- Use an issue for behavior changes that alter APIs, stored data, or edition
  contracts.
- Read `docs/ce-cloud-boundary.md`. Hosted product source belongs only in the
  downstream `flyto-cloud` repository.
- Shared fixes normally land in Flyto2 Flow first and flow downstream. A
  generic fix discovered in Cloud may return only through the allowlisted
  backport workflow and must pass every Flow purity and security gate. Do not
  add hosted compatibility shims to make synchronization easier.
- Never include credentials, customer data, production URLs, or generated
  runtime state.
- Read `PROJECT.md`, `ARCHITECTURE.md`, and `DECISIONS.md` when changing product
  behavior or ownership boundaries.

## Development Checks

Run the checks relevant to your change. Before submitting a release-sensitive
change, run the complete CE gate:

```bash
make verify
flyto-index scan .
flyto-index verify . --strict
```

`make verify` checks the public documentation contract, edition purity, backend
smoke tests, frontend tests and build, dependency licenses, and SBOM output.
Add the narrowest test that proves the changed behavior; do not rely on the
full gate as a substitute for focused coverage.

## License And Contributor Agreement

Current contributions are accepted under the root PolyForm Shield license and
the [Flyto2 Contributor License Agreement](CONTRIBUTOR_LICENSE_AGREEMENT.md).
The CLA gives Flyto2 the rights needed to publish the same generic work in
Flyto2 Flow and Flyto2 Cloud and to offer separate commercial licenses.

Every commit must contain both trailers:

```text
Signed-off-by: Your Name <your-email>
Flyto2-CLA: accepted
```

`git commit --signoff` adds the first trailer. Add the exact CLA trailer to the
commit message. Do not submit code if you cannot make the grants and
representations in the CLA.

## Pull Requests

- Explain the user-visible behavior and security impact.
- Add or update tests for changed behavior.
- Document migrations and compatibility changes.
- Run `python scripts/check-ce-purity.py` and add boundary regression tests when
  a change touches routes, navigation, dependencies, networking, or packaging.
- Run `python scripts/check_license_policy.py` when a change touches licensing,
  contribution terms, branding, release metadata, or the sync contract.
- Update public documentation in the same pull request when behavior, commands,
  defaults, limits, or client contracts change.
- Include before/after screenshots at desktop and mobile widths for visible UI
  changes.
- State what was not tested and why. A passing unrelated test is not evidence
  for the changed behavior.

## Review Standard

A review checks behavior, security, compatibility, edition ownership, tests,
documentation, and rollback. Maintainers may ask for a smaller change when a
proposal mixes these concerns or cannot be verified independently.

Security vulnerabilities must follow `SECURITY.md` and must never be disclosed
through a public issue or pull request.
