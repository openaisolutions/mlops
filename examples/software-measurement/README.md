# Software Measurement: architecture to working evidence

This is a runnable companion to the supplied Software Measurement DevSecOps Architecture graphic and the existing Software Measurement engineering/publication packages. It is an isolated companion, separate from the AI Math book in the hosting repository.

## Run the teaching example

```sh
cd examples/software-measurement
python -m unittest discover -p 'test_*.py' -v
python measurement.py --input example.json --output out
```

Open `out/dashboard.html`. JSON, CSV and SHA-256 receipts accompany the dashboard. Python's standard library is sufficient. The fixture comes from Software_Measurement_Engineering_Package.zip and remains explicitly synthetic. Its original derived values are preserved as source data; the calculator recomputes facts.

## Run a real pipeline evidence collection

```sh
python collect_github.py --repository openaisolutions/mlops --output out/github-runs.json
```

An optional GITHUB_TOKEN is read from the environment and never included in output. The endpoint is fixed to api.github.com, redirects are rejected, responses are bounded to 4 MiB, and requests time out. Only read-only Actions metadata is collected. The snapshot labels the most recent 100 runs as a sample; it does not silently represent an entire release window.

## Measurement definitions that matter

- Overall defect density divides eligible defects by delivered eSLOC / 1,000. Change defect density uses incremental eSLOC as a distinct denominator.
- Test pass percentage of executed tests differs from passed tests divided by planned tests. Both are reported with named denominators.
- Missing inputs and zero denominators produce null values and quality status, never a fabricated zero.
- The source fixture mentions three fixes in narrative but supplies no structured verified_fixes fact. The rework rate remains unavailable until that fact is supplied.
- Cross-source rates require a CSCI and release scope. Real source exports must establish matching baselines, periods, counting rules, acceptance and labor scope.
- Git changes are not automatically equivalent SLOC. The approved UCC-G and adaptation policy must supply size facts.

## Automation and integration status

The GitHub workflow runs tests and generates teaching artifacts on pull requests, pushes, manual dispatch, and weekly. On trusted main-branch runs it also collects real GitHub Actions evidence with a read-only token. It does not attach repository credentials to pull-request Python execution.

The diagram's DOORS, Jira, UCC-G, SonarQube, JaCoCo, labor, QDB, PostgreSQL, Grafana, SBOM, Kubernetes and release-approval systems are integration contracts, not connected services in this companion. Inputs can be normalized into the fact schema after authorization. Private operational evidence should stay in restricted artifact storage; the example workflow uses short artifact retention.

See `book/automation-companion.md` for the book addendum and acceptance criteria. The supplied diagram is design context, not compliance certification. Existing book files and historical evidence remain source material. Source book version and publication status must be reconciled before replacing a reader or print edition.

