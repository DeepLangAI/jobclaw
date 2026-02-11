#!/usr/bin/env python3
"""
Job seeker CLI: submit, update, delete resume and list matched jobs.
"""
import sys
import json
import urllib.request
import urllib.error

DEFAULT_API = "http://localhost:8989"


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
    """Return existing token or create a new JOB_SEEKER account and return its token."""
    if token:
        return token, None
    res = _request(f"{api_url}/auth/token", method="POST", data={"userType": "JOB_SEEKER"})
    if "result" in res:
        return res["result"]["token"], None
    return None, res


# ── Actions ───────────────────────────────────────────────────────────────────

def submit_resume(api_url, data):
    """Submit a new resume."""
    token, err = _ensure_token(api_url, data.get("token"))
    if err:
        return err
    payload = {k: data[k] for k in ("resumeText", "name", "email", "phone", "jobIntention")}
    res = _request(f"{api_url}/job-seekers/resume", method="POST", data=payload, token=token)
    res["token"] = token
    return res


def update_resume(api_url, data):
    """Update an existing resume / profile (partial update supported)."""
    token = data.get("token")
    if not token:
        return {"success": False, "error": "token is required for update"}
    fields = ("resumeText", "name", "email", "phone", "jobIntention")
    payload = {k: data[k] for k in fields if k in data}
    # Map resumeText to resumeRawContent for the update API
    if "resumeText" in payload:
        payload["resumeRawContent"] = payload.pop("resumeText")
    if not payload:
        return {"success": False, "error": "No fields to update"}
    res = _request(f"{api_url}/job-seekers/profile", method="PUT", data=payload, token=token)
    res["token"] = token
    return res


def delete_resume(api_url, data):
    """Soft-delete resume by setting status to INACTIVE."""
    token = data.get("token")
    if not token:
        return {"success": False, "error": "token is required for delete"}
    res = _request(f"{api_url}/job-seekers/profile", method="PUT", data={"status": "INACTIVE"}, token=token)
    res["token"] = token
    return res


def list_matches(api_url, data):
    """List matched job positions for the current job seeker."""
    token = data.get("token")
    if not token:
        return {"success": False, "error": "token is required for listing matches"}
    res = _request(f"{api_url}/matches", token=token)
    res["token"] = token
    return res


# ── CLI entry ─────────────────────────────────────────────────────────────────

ACTIONS = {
    "submit": submit_resume,
    "update": update_resume,
    "delete": delete_resume,
    "matches": list_matches,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": f"Usage: submit_resume.py <json>  (action: {', '.join(ACTIONS)})"}))
        sys.exit(1)
    try:
        data = json.loads(sys.argv[1])
        api_url = data.pop("apiUrl", DEFAULT_API)
        action = data.pop("action", "submit")
        fn = ACTIONS.get(action)
        if not fn:
            print(json.dumps({"success": False, "error": f"Unknown action: {action}. Use: {', '.join(ACTIONS)}"}))
            sys.exit(1)
        print(json.dumps(fn(api_url, data), ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)
