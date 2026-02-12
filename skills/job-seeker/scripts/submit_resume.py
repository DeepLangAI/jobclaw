#!/usr/bin/env python3
"""
Job seeker CLI: submit, update, delete resume and list matched jobs.
"""
import sys
import json
from base import AuthenticatedClient, DEFAULT_API


def submit_resume(api_url, data):
    """Submit a new resume."""
    client = AuthenticatedClient(api_url, "JOB_SEEKER")

    payload = {
        "resumeText": data["resumeText"],
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "jobIntention": data["jobIntention"]
    }

    result = client.post("/job-seekers/resume", payload)
    result["token"] = client.token_manager.get_token()
    return result


def update_resume(api_url, data):
    """Update an existing resume / profile (partial update supported)."""
    client = AuthenticatedClient(api_url, "JOB_SEEKER")

    # Build payload with only provided fields
    fields = ("resumeText", "name", "email", "phone", "jobIntention")
    payload = {k: data[k] for k in fields if k in data}

    # Map resumeText to resumeRawContent for the update API
    if "resumeText" in payload:
        payload["resumeRawContent"] = payload.pop("resumeText")

    if not payload:
        return {"success": False, "error": "No fields to update"}

    result = client.put("/job-seekers/profile", payload)
    result["token"] = client.token_manager.get_token()
    return result


def delete_resume(api_url, data):
    """Soft-delete resume by setting status to INACTIVE."""
    client = AuthenticatedClient(api_url, "JOB_SEEKER")

    result = client.put("/job-seekers/profile", {"status": "INACTIVE"})
    result["token"] = client.token_manager.get_token()
    return result


def list_matches(api_url, data):
    """List matched job positions for the current job seeker."""
    client = AuthenticatedClient(api_url, "JOB_SEEKER")

    result = client.get("/matches")
    result["token"] = client.token_manager.get_token()
    return result


# Action handlers
ACTIONS = {
    "submit": submit_resume,
    "update": update_resume,
    "delete": delete_resume,
    "matches": list_matches,
}


if __name__ == "__main__":
    try:
        # Parse input
        data = None
        if len(sys.argv) > 1:
            data = json.loads(sys.argv[1])
        elif not sys.stdin.isatty():
            input_data = sys.stdin.read()
            if input_data.strip():
                data = json.loads(input_data)

        if not data:
            print(json.dumps({
                "success": False,
                "error": "Usage: submit_resume.py <json> (or pipe json to stdin)"
            }))
            sys.exit(1)

        # Extract parameters
        api_url = data.pop("apiUrl", DEFAULT_API)
        action = data.pop("action", "submit")

        # Execute action
        fn = ACTIONS.get(action)
        if not fn:
            print(json.dumps({
                "success": False,
                "error": f"Unknown action: {action}. Use: {', '.join(ACTIONS)}"
            }))
            sys.exit(1)

        result = fn(api_url, data)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)
