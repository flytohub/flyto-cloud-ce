# Licensing Strategy

## Current model

Flyto2 Flow is source-available/fair-code under PolyForm Shield License 1.0.0.
The source can be inspected, self-hosted, modified, and redistributed for
permitted purposes, but it cannot be used to provide a product or service that
competes with Flyto2 or its affiliates. A separate signed commercial license
can grant rights outside that boundary.

This is intentionally similar in business objective to fair-code projects such
as n8n: users can understand and self-host the product, while the copyright
license prevents a third party from repackaging the work as a competing
offering. The exact Flyto2 terms are PolyForm Shield, not n8n's custom license.

## Terminology

A license that restricts commercial or competitive use is not OSI-approved open
source because the Open Source Definition requires permission to use software
in every field of endeavor. Public materials therefore use **source-available**
or **fair-code**, never an unqualified claim that current revisions are open
source.

## Historical Apache boundary

Revisions through commit `9398a622a2b53bde6df5e661d71735d1cefdbabc`
were released under Apache License 2.0. Those grants are not revoked. Anyone who
received one of those revisions may continue using that revision under Apache
2.0, including to fork, resell, or compete. The practical protection is that
new fixes, releases, assets, and improvements after that boundary use PolyForm
Shield. See `LICENSE_HISTORY.md`.

## Contribution and dual licensing

Every new contribution requires explicit acceptance of
`CONTRIBUTOR_LICENSE_AGREEMENT.md`. The CLA preserves contributor ownership but
grants Flyto2 broad sublicensing and relicensing rights, allowing generic work
to appear in both Flow and Cloud and allowing Flyto2 to offer a commercial
license without seeking consent again for every accepted contribution.

## Protection layers

1. PolyForm Shield prohibits competitive products and services for current
   revisions.
2. `COMMERCIAL_LICENSE.md` identifies uses that require a written grant.
3. `TRADEMARKS.md` prevents forks from presenting themselves as official
   Flyto2 products.
4. The CLA protects future relicensing and commercial distribution rights.
5. `FLOW_CLOUD_SYNC.json` and Flow purity gates prevent private Cloud code from
   being accidentally published while allowing safe generic backports.
6. CodeQL, dependency auditing, SBOM generation, CODEOWNERS, and protected
   branches make the legal boundary operational rather than purely textual.

The licensor name and any corporate CLA form should be reviewed by qualified
counsel before accepting outside corporate contributions or signing commercial
licenses. This document records the engineering and release policy; it is not
jurisdiction-specific legal advice.
