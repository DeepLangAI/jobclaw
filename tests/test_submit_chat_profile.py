"""Offline subprocess tests for the chat-profile CLI exit status."""
import json
from pathlib import Path
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/job-seeker/scripts/submit_chat_profile.py"

# Run the real CLI entry point, replacing only the HTTP transport. An explicit
# synthetic token prevents reading a user's token file.
RUNNER = """
import io
import json
import runpy
import sys
import urllib.error
from unittest.mock import patch

script, scenario, input_mode = sys.argv[1:]
payload = json.dumps({
    "apiUrl": "https://example.invalid",
    "token": "synthetic-test-token",
    "profileText": "Synthetic test profile",
    "rawConversation": "Synthetic test conversation",
})
sys.argv = [script] + ([payload] if input_mode == "argv" else [])
sys.stdin = io.StringIO(payload)

def respond(request):
    if scenario == "http-json":
        raise urllib.error.HTTPError(
            request.full_url, 400, "Bad Request", {},
            io.BytesIO(b'{"message": "Invalid profile"}'),
        )
    if scenario == "http-text":
        raise urllib.error.HTTPError(
            request.full_url, 503, "Service Unavailable", {},
            io.BytesIO(b"Service unavailable"),
        )
    if scenario == "connection":
        raise urllib.error.URLError("Offline test failure")
    responses = {
        "success": {"success": True, "result": {"id": "synthetic-profile"}},
        "implicit-success": {"result": {"id": "synthetic-profile"}},
        "api-failure": {"success": False, "error": "Invalid profile"},
    }
    return io.BytesIO(json.dumps(responses[scenario]).encode("utf-8"))

with patch("urllib.request.urlopen", side_effect=respond):
    runpy.run_path(script, run_name="__main__")
"""


class ChatProfileExitStatusTests(unittest.TestCase):
    def run_cli(self, scenario, expected_code):
        for input_mode in ("argv", "stdin"):
            with self.subTest(input_mode=input_mode):
                result = subprocess.run(
                    [sys.executable, "-c", RUNNER, str(SCRIPT), scenario, input_mode],
                    capture_output=True, text=True, timeout=10,
                )
                self.assertEqual(result.stderr, "")
                response = json.loads(result.stdout)
                self.assertEqual(result.returncode, expected_code, result.stdout)
                if expected_code:
                    self.assertIs(response["success"], False)
                    self.assertTrue(response["error"])
                else:
                    self.assertEqual(response["result"], {"id": "synthetic-profile"})

    def test_success(self):
        self.run_cli("success", 0)

    def test_response_without_success_flag(self):
        self.run_cli("implicit-success", 0)

    def test_http_error_with_json_body(self):
        self.run_cli("http-json", 1)

    def test_http_error_with_plain_text_body(self):
        self.run_cli("http-text", 1)

    def test_api_failure_in_successful_http_response(self):
        self.run_cli("api-failure", 1)

    def test_connection_error(self):
        self.run_cli("connection", 1)


if __name__ == "__main__":
    unittest.main()
