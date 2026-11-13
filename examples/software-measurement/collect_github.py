"""Read-only, bounded GitHub Actions evidence collector. Never emits tokens."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.request

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def collect(repository, token=None, opener=None):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) or any(s in {".", ".."} for s in repository.split("/")):
        raise ValueError("Expected owner/repository")
    opener = opener or urllib.request.build_opener(NoRedirect())
    headers = {"Accept":"application/vnd.github+json", "X-GitHub-Api-Version":"2022-11-28"}
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request("https://api.github.com/repos/" + repository + "/actions/runs?per_page=100", headers=headers)
    with opener.open(request, timeout=20) as response:
        body = response.read(4*1024*1024 + 1)
    if len(body) > 4*1024*1024:
        raise ValueError("GitHub response exceeds 4 MiB")
    payload = json.loads(body)
    runs = payload.get("workflow_runs", [])
    records = [{k:r.get(k) for k in ("id","name","head_sha","event","status","conclusion","created_at","updated_at","html_url")} for r in runs]
    return {"repository":repository,"collected_at":dt.datetime.now(dt.timezone.utc).isoformat(),
            "source":"GitHub Actions API","sample_kind":"most_recent_100_runs",
            "total_available":payload.get("total_count"),"complete_inventory":payload.get("total_count", 101) <= len(records),
            "source_payload_sha256":hashlib.sha256(body).hexdigest(),"runs":records,
            "limitations":["This is a recent-run sample, not release acceptance or a complete reporting-period inventory.",
                           "A successful job does not establish absence of source vulnerabilities."]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repository", required=True)
    p.add_argument("--output", type=Path, required=True)
    a=p.parse_args()
    try:
        result=collect(a.repository, os.environ.get("GITHUB_TOKEN"))
    except urllib.error.HTTPError as exc:
        raise SystemExit("GitHub evidence unavailable: HTTP " + str(exc.code)) from None
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":
    main()

