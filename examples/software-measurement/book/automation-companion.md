# Architecture to evidence: a runnable DevSecOps field lab

The architecture graphic traces requirements and work through development, assurance, measurement and reporting. This companion turns a bounded portion of that architecture into executable examples. The existing Software Measurement publication proof v0.5 supplies data models, dashboards, release receipts and field labs. The engineering package supplies a synthetic normalized source contract. These are existing foundations; this lab adds automated checks, a repeatable measurement calculation, evidence hashes and pipeline execution.

## The exercise

Run the tests, calculate the engineering fixture and open the resulting dashboard. Inspect each numerator, denominator, quality status and input digest. Change planned tests to zero: the output becomes unavailable, rather than a misleading zero percent. Remove the release identifier: cross-source productivity is suppressed. These are reporting controls that students can execute.

The fixture contains 8 eligible defects, 10,000 delivered equivalent lines, 410 incremental equivalent lines and 100 actual engineering hours. Overall density is 0.8 defects per thousand delivered equivalent lines. Productivity is 4.1 incremental equivalent lines per hour, conditional on matching scope. The source has 68 passed tests out of 75 executed and 100 planned: pass of executed is approximately 90.67%, while pass of planned is 68%. Reporting either as an unnamed pass rate hides a consequential definition.

The graphic's separate example uses an increment of 4,710 equivalent lines and four defects to obtain approximately 0.85 defects per thousand changed equivalent lines. That denominator is a change measure. It must not be silently substituted for delivered stock.

## What runs

1. Validate normalized facts and reconcile test counts.
2. Compute the named measures and retain missing-data statuses.
3. Produce JSON, CSV and a local HTML dashboard from the same result.
4. Hash the exact source input and output files.
5. In GitHub Actions, run the tests before generating the teaching artifacts.
6. On trusted main-branch runs, collect recent real pipeline metadata separately from the synthetic measurement example.
7. Publish short-lived workflow artifacts for inspection. A job success is execution evidence, not a release acceptance signature.

## What remains a governed integration

DOORS owns approved requirement baselines; Jira owns work and test records; an approved UCC-G process owns size observations; coverage tools own test coverage; approved labor exports own hours. A future collector must preserve account, project, baseline, release, period, counting method, source record, cutoff and digest. Names matching across systems are insufficient evidence of the same scope.

No credential should be pasted into a notebook, graphic, CSV, source file or report. A deployment must use its secret store and a read-only identity for collection. The release gate needs an independent authorized reviewer and accepted evidence; the reporting pipeline does not grant deployment authority.

## Mapping to the complete architecture

Plan/design/branch/merge/build/test/security/package/SBOM/integration/release/deploy stages retain their own evidence owners. This lab implements calculation and evidence packaging plus a read-only GitHub collector. Existing security workflows supply CodeQL and dependency-update checks. It does not impersonate unavailable DOORS, Jira, Grafana or Kubernetes services, and it does not certify a DID or CDRL delivery.

## Acceptance record

Record the repository commit, workflow run, source digest, method version, test result, unavailable inputs, reviewer and decision. Distinguish a generated report, an accepted measurement baseline, a passed security check, and an authorized release.

This addendum is source for the Software Measurement book. The generated supplemental reader preserves all 794 pages of Software Measurement and Reporting With Design Appendix (2026-11-09) and appends this lab; it is a review copy. The separate 188-page v0.5 Satellite Software Measurement package is supporting historical material, not a replacement for that reader. Print pagination, covers, contents, contributor metadata and publication approval must be reconciled for a new production edition.

