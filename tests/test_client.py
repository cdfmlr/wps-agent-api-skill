import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from wps_api import WPSAPIError, WPSClient, _is_api_error


class FakeClient(WPSClient):
    def __init__(self, pages):
        self.pages = pages
        self.calls = []

    def get(self, path, **kwargs):
        params = kwargs.get("params") or {}
        self.calls.append((path, params))
        return self.pages[params.get("page_token", "")]


class ListFilesTest(unittest.TestCase):
    def test_follows_next_page_token(self):
        pages = {
            "": {"code": 0, "data": {"items": [{"id": "1"}, {"id": "2"}],
                                     "next_page_token": "t1"}},
            "t1": {"code": 0, "data": {"items": [{"id": "3"}],
                                       "next_page_token": "t2"}},
            "t2": {"code": 0, "data": {"items": [{"id": "4"}],
                                       "next_page_token": ""}},
        }
        client = FakeClient(pages)
        result = client.list_files("drive", "0", page_size=2)

        self.assertEqual([item["id"] for item in result["data"]["items"]],
                         ["1", "2", "3", "4"])
        self.assertNotIn("next_page_token", result["data"])
        self.assertEqual([call[1].get("page_token") for call in client.calls],
                         [None, "t1", "t2"])

    def test_clamps_page_size(self):
        client = FakeClient({"": {"code": 0, "data": {"items": [],
                                                      "next_page_token": ""}}})
        client.list_files("drive", page_size=9999)
        self.assertEqual(client.calls[0][1]["page_size"], 500)

    def test_repeated_token_raises(self):
        pages = {
            "": {"code": 0, "data": {"items": [], "next_page_token": "t1"}},
            "t1": {"code": 0, "data": {"items": [], "next_page_token": "t1"}},
        }
        with self.assertRaises(WPSAPIError):
            FakeClient(pages).list_files("drive")


class ErrorTest(unittest.TestCase):
    def test_error_detection(self):
        self.assertFalse(_is_api_error({"code": 0, "msg": "ok"}))
        self.assertFalse(_is_api_error({"code": "0", "errno": 0}))
        self.assertTrue(_is_api_error({"code": 401000001, "msg": "bad"}))
        self.assertTrue(_is_api_error({"errno": 10000, "msg": "unable to parse claims"}))
        self.assertTrue(_is_api_error({"result": "permissionDenied"}))

    def test_error_message_is_readable(self):
        err = WPSAPIError({"errno": 10000, "msg": "unable to parse claims",
                           "reason": "permissionDenied"}, http_status=401)
        text = str(err)
        self.assertIn("HTTP 401", text)
        self.assertIn("errno=10000", text)
        self.assertIn("unable to parse claims", text)
        self.assertIn("reason=permissionDenied", text)
        self.assertFalse(err.retryable)

    def test_retryable_status(self):
        self.assertTrue(WPSAPIError({"msg": "busy"}, http_status=429).retryable)
        self.assertTrue(WPSAPIError({"msg": "boom"}, http_status=503).retryable)
        self.assertFalse(WPSAPIError({"msg": "bad"}, http_status=400).retryable)


if __name__ == "__main__":
    unittest.main()
