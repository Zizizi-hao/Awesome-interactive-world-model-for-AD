"""Offline regression tests: python -m unittest discover -s tests."""

import contextlib
import datetime
import email.utils
import http.client
import importlib.util
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import urllib.error


SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("fetch_arxiv", SCRIPTS / "fetch_arxiv.py")
fetch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fetch)


def http_error(code, retry_after=None):
    headers = {} if retry_after is None else {"Retry-After": retry_after}
    return urllib.error.HTTPError("https://example.invalid", code, "test", headers, None)


def paper(arxiv_id="2609.00001", **changes):
    result = {
        "id": arxiv_id,
        "title": "World model for driving robots and interactive video",
        "abstract": "A research paper.",
        "published": datetime.date.today().isoformat(),
        "authors": ["Test Author"],
        "primary_category": "cs.CV",
        "categories": ["cs.CV"],
    }
    result.update(changes)
    return result


class MainTests(unittest.TestCase):
    def setUp(self):
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.temp = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.config_path = self.temp / "config.yaml"
        self.output_path = self.temp / "output.txt"
        self.summary_path = self.temp / "summary.md"
        self.cfg = {
            "lookback_days": 7,
            "retry_attempts": 3,
            "timeout_seconds": 60,
            "delay_seconds": 5,
            "rss_fallback": True,
            "category_filter": ["cs.CV", "cs.RO"],
            "queries": [
                {
                    "name": name,
                    "search": "all:" + keyword,
                    "feed_keywords": [["world model"], [keyword]],
                }
                for name, keyword in [
                    ("Driving", "driving"),
                    ("Robotics", "robot"),
                    ("Interactive", "interactive"),
                ]
            ],
        }
        self.stack.enter_context(patch.object(fetch, "CONFIG_FILE", self.config_path))
        self.stack.enter_context(patch.dict(os.environ, {
            "GITHUB_OUTPUT": str(self.output_path),
            "GITHUB_STEP_SUMMARY": str(self.summary_path),
        }))
        self.stack.enter_context(patch.object(fetch.tempfile, "gettempdir", return_value=str(self.temp)))
        self.stack.enter_context(patch.object(fetch.time, "sleep"))
        self.stack.enter_context(patch.object(fetch.urllib.request, "urlopen", side_effect=AssertionError("Offline test attempted an HTTP request")))
        self.existing = self.stack.enter_context(patch.object(fetch, "existing_arxiv_ids", return_value=set()))
        self.seen = self.stack.enter_context(patch.object(fetch, "load_seen", return_value=set()))
        self.append_seen = self.stack.enter_context(patch.object(fetch, "append_seen"))
        self.api = self.stack.enter_context(patch.object(fetch, "fetch_query", return_value=b"api"))
        self.feed = self.stack.enter_context(patch.object(fetch, "fetch_url", return_value=b"feed"))
        self.parse_api = self.stack.enter_context(patch.object(fetch, "parse_entries", return_value=[]))
        self.parse_feed = self.stack.enter_context(patch.object(fetch, "parse_feed", return_value=[]))

    def run_main(self, dry_run=False):
        self.config_path.write_text(fetch.yaml.safe_dump(self.cfg), encoding="utf-8")
        stdout = io.StringIO()
        with patch.object(sys, "argv", ["fetch_arxiv.py"] + (["--dry-run"] if dry_run else [])), contextlib.redirect_stdout(stdout):
            try:
                fetch.main()
            except SystemExit as exc:
                code = exc.code or 0
            else:
                code = 0
        return code, stdout.getvalue()

    def output(self):
        return dict(line.split("=", 1) for line in self.output_path.read_text(encoding="utf-8").splitlines())

    def test_successful_empty_scan_is_success(self):
        code, _ = self.run_main()
        self.assertEqual(code, 0)
        self.assertEqual(self.api.call_count, 3)
        self.assertEqual(self.output()["scan_status"], "success")
        self.assertEqual(self.output()["has_new"], "false")
        self.assertTrue(self.summary_path.is_file())
        self.feed.assert_not_called()
        self.append_seen.assert_not_called()

    def test_total_failure_is_not_reported_as_no_new_papers(self):
        self.api.side_effect = TimeoutError("API timed out")
        self.feed.side_effect = http_error(429)
        code, stdout = self.run_main()
        self.assertEqual(code, 1)
        self.assertEqual(self.output()["scan_status"], "failed")
        self.assertEqual(self.output()["has_new"], "false")
        self.assertNotIn("没有新候选论文", stdout)
        self.assertTrue(self.summary_path.is_file())
        self.append_seen.assert_not_called()

    def test_partial_api_success_keeps_candidates(self):
        self.cfg["rss_fallback"] = False
        self.api.side_effect = [b"api", http_error(400), b"api"]
        self.parse_api.side_effect = [[paper()], []]
        code, _ = self.run_main()
        self.assertEqual(code, 0)
        self.assertEqual(self.output()["scan_status"], "partial")
        self.assertEqual(self.output()["has_new"], "true")
        self.append_seen.assert_called_once()
        self.assertEqual(set(self.append_seen.call_args.args[0]), {"2609.00001"})
        self.feed.assert_not_called()

    def test_deferred_request_also_stops_fallback(self):
        self.api.side_effect = fetch.RequestDeferred("Long server cooldown")
        code, _ = self.run_main()
        self.assertEqual(code, 1)
        self.assertEqual(self.output()["scan_status"], "failed")
        self.api.assert_called_once()
        self.feed.assert_not_called()
        self.append_seen.assert_not_called()

    def test_rate_limit_stops_api_queries_and_fetches_feed_once(self):
        self.api.side_effect = http_error(429)
        self.existing.return_value = {"2609.00002"}
        self.seen.return_value = {"2609.00003"}
        candidate = paper(published="", announced=datetime.date.today().isoformat(),
                          primary_category="", categories=["cs.LG", "cs.CV"], date_label="公告日期")
        self.parse_feed.return_value = [
            candidate, candidate,
            dict(candidate, id="2609.00002"), dict(candidate, id="2609.00003"),
        ]
        code, _ = self.run_main()
        self.assertEqual(code, 0)
        self.api.assert_called_once()
        self.feed.assert_called_once()
        self.assertTrue(self.feed.call_args.args[0].startswith("https://rss.arxiv.org/atom/"))
        self.assertEqual(self.feed.call_args.kwargs["retries"], 1)
        self.assertEqual(self.output()["scan_status"], "partial")
        self.assertEqual(self.output()["has_new"], "true")
        self.append_seen.assert_called_once()
        self.assertEqual(set(self.append_seen.call_args.args[0]), {"2609.00001"})
        report = Path(self.output()["report"]).read_text(encoding="utf-8")
        self.assertEqual(report.count("https://arxiv.org/abs/2609.00001"), 1)
        self.assertIn("公告日期", report)

    def test_empty_feed_still_reports_incomplete_scan(self):
        self.api.side_effect = http_error(429)
        code, _ = self.run_main()
        self.assertEqual(code, 0)
        self.assertEqual(self.output()["scan_status"], "partial")
        self.assertEqual(self.output()["has_new"], "false")
        summary = self.summary_path.read_text(encoding="utf-8")
        self.assertTrue(any(label in summary for label in ("RSS", "Atom", "备用")))
        self.assertIn("7", summary)
        self.append_seen.assert_not_called()

    def test_dry_run_does_not_write_state_or_github_files(self):
        for outcome in ("success", "empty", "failed"):
            with self.subTest(outcome=outcome):
                self.api.side_effect = TimeoutError("offline") if outcome == "failed" else None
                self.feed.side_effect = TimeoutError("offline") if outcome == "failed" else None
                self.parse_api.return_value = [paper()] if outcome == "success" else []
                code, _ = self.run_main(dry_run=True)
                self.assertEqual(code, 1 if outcome == "failed" else 0)
                self.append_seen.assert_not_called()
                self.assertFalse(self.output_path.exists())
                self.assertFalse(self.summary_path.exists())
                self.assertFalse((self.temp / "arxiv_report.md").exists())


class FetchUrlTests(unittest.TestCase):
    def setUp(self):
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
        self.now = 1000.0
        self.stack.enter_context(patch.object(fetch, "_next_request_at", 0.0))
        self.stack.enter_context(patch.object(fetch.time, "monotonic", side_effect=lambda: self.now))
        self.stack.enter_context(patch.object(fetch.time, "time", side_effect=lambda: 1_800_000_000 + self.now))
        real_datetime = datetime.datetime
        fake_datetime = self.stack.enter_context(patch.object(fetch.datetime, "datetime", wraps=real_datetime))
        fake_datetime.now.side_effect = lambda tz=None: real_datetime.fromtimestamp(1_800_000_000 + self.now, tz)
        self.sleep = self.stack.enter_context(patch.object(fetch.time, "sleep", side_effect=self.advance))
        self.stack.enter_context(patch.object(fetch.random, "uniform", return_value=0))
        self.urlopen = self.stack.enter_context(patch.object(fetch.urllib.request, "urlopen"))
        self.response = MagicMock()
        self.response.__enter__.return_value.read.return_value = b"<feed />"

    def advance(self, seconds):
        self.now += seconds

    def test_transient_errors_retry_and_recover(self):
        errors = [http_error(code) for code in (408, 429, 500, 502, 503, 504)] + [
            urllib.error.URLError("offline"), TimeoutError("timed out"),
            ConnectionError("disconnected"), http.client.RemoteDisconnected("closed"),
        ]
        for error in errors:
            with self.subTest(error=repr(error)):
                fetch._next_request_at = 0
                self.urlopen.reset_mock()
                self.urlopen.side_effect = [error, self.response]
                result = fetch.fetch_url("https://example.invalid", retries=2, timeout=12, delay=5)
                self.assertEqual(result, b"<feed />")
                self.assertEqual(self.urlopen.call_count, 2)
                self.assertEqual(self.urlopen.call_args.kwargs["timeout"], 12)

    def test_http_400_is_not_retried(self):
        self.urlopen.side_effect = http_error(400)
        with self.assertRaises(urllib.error.HTTPError):
            fetch.fetch_url("https://example.invalid", retries=3)
        self.urlopen.assert_called_once()

    def test_retry_after_cooldown_is_shared_between_api_and_feed(self):
        for header in ("40", email.utils.formatdate(1_800_001_060, usegmt=True)):
            with self.subTest(retry_after=header):
                self.now = 1000.0
                fetch._next_request_at = 0
                self.urlopen.side_effect = [http_error(429, header), self.response]
                with self.assertRaises(urllib.error.HTTPError):
                    fetch.fetch_query("all:test", 10, retries=1)
                result = fetch.fetch_url("https://rss.arxiv.org/atom/cs.CV", retries=1)
                self.assertEqual(result, b"<feed />")
                self.assertGreaterEqual(self.now, 1040.0 if header == "40" else 1060.0)

    def test_long_retry_after_defers_without_another_request(self):
        self.urlopen.side_effect = http_error(429, "600")
        with self.assertRaises(fetch.RequestDeferred):
            fetch.fetch_url("https://example.invalid", retries=3)
        self.urlopen.assert_called_once()
        self.assertLessEqual(self.now - 1000.0, fetch.REQUEST_WAIT_BUDGET)
        with self.assertRaises(fetch.RequestDeferred):
            fetch.fetch_url("https://rss.arxiv.org/atom/cs.CV", retries=1)
        self.urlopen.assert_called_once()


if __name__ == "__main__":
    unittest.main()
