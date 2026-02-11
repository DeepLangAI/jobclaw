#!/usr/bin/env python3
"""
Submit a chat profile (career portrait from conversation) to the job matching system.
"""
import sys
import json
import urllib.request
import urllib.error

DEFAULT_API = "http://localhost:8989"


def _request(url, method="POST", data=None, token=None):
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "Usage: submit_chat_profile.py '<json>'"}))
        sys.exit(1)
    try:
        data = json.loads(sys.argv[1])
        api_url = data.pop("apiUrl", DEFAULT_API)
        token = data.pop("token", None)
        payload = {
            "profileText": data["profileText"],
            "rawConversation": data["rawConversation"],
        }
        res = _request(f"{api_url}/job-seekers/chat-profile", data=payload, token=token)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)
