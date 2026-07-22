# Contributing to Flyto2 Flow

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

## Development Checks

Run the checks relevant to your change. Before submitting a release-sensitive
change, run the complete CE gate:

```bash
make verify
```

## License And Contributor Agreement

Current contributions are accepted under the root PolyForm Shield license and
the [Flyto2 Contributor License Agreement](CONTRIBUTOR_LICENSE_AGREEMENT.md).
The CLA gives Flyto2 the rights needed to publish the same generic work in
Flyto2 Flow and Flyto2 Cloud and to offer separate commercial licenses.

Every commit must contain both trailers:

```text
Signed-off-by: Your Name <you@example.com>
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
