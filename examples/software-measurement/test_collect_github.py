import io
import json
import unittest

from collect_github import NoRedirect, collect


class Response(io.BytesIO):
    pass


class Opener:
    def __init__(self, payload):
        self.payload = payload
        self.request = None

    def open(self, request, timeout):
        self.request = request
        assert timeout == 20
        return Response(json.dumps(self.payload).encode())


class CollectorTests(unittest.TestCase):
    def test_rejects_host_and_path_injection(self):
        for repo in ["https://evil.test/x", "a/b/c", "../x", "a/b?token=x"]:
            with self.subTest(repo=repo), self.assertRaises(ValueError):
                collect(repo)

    def test_bounded_sample_and_safe_output(self):
        op = Opener(
            {
                "total_count": 101,
                "workflow_runs": [
                    {
                        "id": 1,
                        "head_sha": "abc",
                        "status": "completed",
                        "conclusion": "success",
                    }
                ],
            }
        )
        result = collect("owner/repo", "test-token-value", op)
        self.assertFalse(result["complete_inventory"])
        self.assertNotIn("test-token-value", json.dumps(result))
        self.assertTrue(
            op.request.full_url.startswith("https://api.github.com/repos/owner/repo/")
        )
        self.assertEqual(len(result["source_payload_sha256"]), 64)

    def test_redirect_is_not_followed(self):
        self.assertIsNone(
            NoRedirect().redirect_request(None, None, 302, "", {}, "https://evil.test")
        )


if __name__ == "__main__":
    unittest.main()
