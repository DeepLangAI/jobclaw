#!/usr/bin/env python3
"""
Job seeker profile and matches viewer.
View your profile information and matched job positions.
"""
import sys
import json
from base import AuthenticatedClient, DEFAULT_API


def get_profile(api_url):
    """Get job seeker profile information."""
    client = AuthenticatedClient(api_url, "JOB_SEEKER")
    result = client.get("/job-seekers/profile")
    return result


def get_matches(api_url):
    """Get matched job positions."""
    client = AuthenticatedClient(api_url, "JOB_SEEKER")
    result = client.get("/matches")
    return result


def get_full_info(api_url):
    """Get complete information: profile + matches."""
    client = AuthenticatedClient(api_url, "JOB_SEEKER")

    # Get profile
    profile_result = client.get("/job-seekers/profile")

    # Get matches
    matches_result = client.get("/matches")

    return {
        "success": True,
        "result": {
            "profile": profile_result.get("result"),
            "matches": matches_result.get("result")
        }
    }


# Action handlers
ACTIONS = {
    "profile": get_profile,
    "matches": get_matches,
    "full": get_full_info,
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
                "error": "Usage: get_profile.py <json> (or pipe json to stdin)\n"
                         "Actions: profile, matches, full"
            }))
            sys.exit(1)

        # Extract parameters
        api_url = data.pop("apiUrl", DEFAULT_API)
        action = data.pop("action", "full")

        # Execute action
        fn = ACTIONS.get(action)
        if not fn:
            print(json.dumps({
                "success": False,
                "error": f"Unknown action: {action}. Use: {', '.join(ACTIONS)}"
            }))
            sys.exit(1)

        result = fn(api_url)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)
