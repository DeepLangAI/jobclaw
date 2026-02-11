#!/usr/bin/env python3
"""
Recruiter CLI: publish, update, delete job postings and list matched candidates.
"""
import sys
import json
import urllib.request
import urllib.error

DEFAULT_API = "https://api.jobclaw.ai"


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _request(url, method="GET", data=None, token=None):
    """Send an HTTP request and return parsed JSON or an error dict."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"success": False, "error": e.read().decode("utf-8")}


def _ensure_token(api_url, token):
    """Return existing token or create a new RECRUITER account and return its token."""
    if token:
        return token, None
    res = _request(f"{api_url}/auth/token", method="POST", data={"userType": "RECRUITER"})
    if "result" in res:
        return res["result"]["token"], None
    return None, res


# ── Actions ───────────────────────────────────────────────────────────────────

JOB_FIELDS = ("title", "companyName", "requirement", "salary", "location", "jobType", "education", "experience")


def publish_job(api_url, data):
    """Publish a new job posting."""
    token, err = _ensure_token(api_url, data.get("token"))
    if err:
        return err
    payload = {k: data[k] for k in JOB_FIELDS}
    payload["status"] = data.get("status", "ACTIVE")
    res = _request(f"{api_url}/jobs", method="POST", data=payload, token=token)
    res["token"] = token
    return res


def update_job(api_url, data):
    """Update an existing job posting (partial update supported)."""
    token = data.get("token")
    job_id = data.get("jobId")
    if not token:
        return {"success": False, "error": "token is required for update"}
    if not job_id:
        return {"success": False, "error": "jobId is required for update"}
    payload = {k: data[k] for k in (*JOB_FIELDS, "status") if k in data}
    if not payload:
        return {"success": False, "error": "No fields to update"}
    res = _request(f"{api_url}/jobs/{job_id}", method="PUT", data=payload, token=token)
    res["token"] = token
    return res


def delete_job(api_url, data):
    """Soft-delete a job posting by setting status to INACTIVE."""
    token = data.get("token")
    job_id = data.get("jobId")
    if not token:
        return {"success": False, "error": "token is required for delete"}
    if not job_id:
        return {"success": False, "error": "jobId is required for delete"}
    res = _request(f"{api_url}/jobs/{job_id}", method="PUT", data={"status": "INACTIVE"}, token=token)
    res["token"] = token
    return res


def list_matches(api_url, data):
    """List matched candidates for a specific job posting."""
    token = data.get("token")
    job_id = data.get("jobId")
    if not token:
        return {"success": False, "error": "token is required for listing matches"}
    if not job_id:
        return {"success": False, "error": "jobId is required for listing matches"}
    res = _request(f"{api_url}/matches/job/{job_id}", token=token)
    res["token"] = token
    return res


# ── CLI entry ─────────────────────────────────────────────────────────────────

ACTIONS = {
    "publish": publish_job,
    "update": update_job,
    "delete": delete_job,
    "matches": list_matches,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": f"Usage: publish_job.py <json>  (action: {', '.join(ACTIONS)})"}))
        sys.exit(1)
    try:
        data = json.loads(sys.argv[1])
        api_url = data.pop("apiUrl", DEFAULT_API)
        action = data.pop("action", "publish")
        fn = ACTIONS.get(action)
        if not fn:
            print(json.dumps({"success": False, "error": f"Unknown action: {action}. Use: {', '.join(ACTIONS)}"}))
            sys.exit(1)
        print(json.dumps(fn(api_url, data), ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)
