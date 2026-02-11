#!/usr/bin/env python3
"""
Submit a chat profile (career portrait from conversation) to the job matching system.
"""
import sys
import json
import os
import urllib.request
import urllib.error

TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".token")

DEFAULT_API = "https://api.jobclaw.ai"


def _request(url, method="POST", data=None, token=None):
    """Send an HTTP request and return parsed JSON or an error dict."""
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "JobClaw-Skill-Script/1.0"
    }
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
    data = None
    try:
        if len(sys.argv) > 1:
            data = json.loads(sys.argv[1])
        elif not sys.stdin.isatty():
            input_data = sys.stdin.read()
            if input_data.strip():
                data = json.loads(input_data)
        
        if not data:
            print(json.dumps({"success": False, "error": "Usage: submit_chat_profile.py <json> (or pipe json to stdin)"}))
            sys.exit(1)
        api_url = data.pop("apiUrl", DEFAULT_API)
        token = data.pop("token", None)
        
        # Fallback to local token file if token not provided
        if not token and os.path.exists(TOKEN_FILE):
            try:
                with open(TOKEN_FILE, 'r') as f:
                    token = f.read().strip()
            except:
                pass
        payload = {
            "profileText": data["profileText"],
            "rawConversation": data["rawConversation"],
        }
        res = _request(f"{api_url}/job-seekers/chat-profile", data=payload, token=token)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)
