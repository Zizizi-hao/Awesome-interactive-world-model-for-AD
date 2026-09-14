import unittest

from scripts.arxiv_feed import matches_query, parse_feed


def feed(entries="", updated="2026-09-14T04:00:17+00:00"):
    return f'''<feed xmlns="http://www.w3.org/2005/Atom"
        xmlns:arxiv="http://arxiv.org/schemas/atom"
        xmlns:dc="http://purl.org/dc/elements/1.1/">
        <id>http://rss.arxiv.org/atom/cs.CV</id><title>cs.CV updates on arXiv.org</title>
        <updated>{updated}</updated>{entries}</feed>'''.encode()


ENTRY = '''<entry>
    <id>oai:arXiv.org:2609.12345v2</id>
    <title>World models for self-driving cars</title>
    <updated>2026-09-14T04:00:17+00:00</updated>
    <published>2026-09-14T00:00:00-04:00</published>
    <summary>arXiv:2609.12345v2 Announce Type: replace
        Abstract: An action-conditioned world model for robotics.</summary>
    <category term="cs.RO"/><category term="cs.CV"/>
    <arxiv:announce_type>replace</arxiv:announce_type>
    <dc:creator>Alice Example, Bob Example</dc:creator>
</entry>'''


class FeedTests(unittest.TestCase):
    def test_daily_metadata_keeps_announcement_separate_from_submission(self):
        entry = parse_feed(feed(ENTRY))[0]
        self.assertEqual(entry["id"], "2609.12345")
        self.assertEqual(entry["published"], "")
        self.assertEqual(entry["announced"], "2026-09-14")
        self.assertEqual(entry["abstract"], "An action-conditioned world model for robotics.")
        self.assertEqual(entry["authors"], ["Alice Example", "Bob Example"])
        self.assertEqual(entry["primary_category"], "")
        self.assertEqual(entry["categories"], ["cs.RO", "cs.CV"])
        self.assertEqual(entry["announce_type"], "replace")

    def test_valid_empty_feed(self):
        self.assertEqual(parse_feed(feed()), [])

    def test_invalid_responses_do_not_become_empty_success(self):
        error_entry = "<entry><id>http://arxiv.org/api/errors#failed</id><title>Error</title></entry>"
        for payload in (b"<html><body>Service unavailable</body></html>", feed(error_entry),
                        feed(updated="1970-01-01T00:00:00+00:00"), feed(updated="")):
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    parse_feed(payload)

    def test_missing_announced_date_does_not_use_generation_time(self):
        with self.assertRaises(ValueError):
            parse_feed(feed(ENTRY.replace("<published>2026-09-14T00:00:00-04:00</published>", "")))

    def test_legacy_id_retains_archive_prefix(self):
        entry = parse_feed(feed(ENTRY.replace("oai:arXiv.org:2609.12345v2", "oai:arXiv.org:hep-ex/0307015v2")))[0]
        self.assertEqual(entry["id"], "hep-ex/0307015")

    def test_cap_is_reported_as_possible_truncation(self):
        with self.assertRaisesRegex(ValueError, "truncated"):
            parse_feed(feed(ENTRY * 2000))

    def test_case_hyphens_and_and_of_or_groups(self):
        query = {"feed_keywords": [["world model", "world models"], ["self driving", "manipulation"]]}
        self.assertTrue(matches_query({"title": "WORLD–MODELS for self-driving cars"}, query))
        self.assertFalse(matches_query({"title": "World models for weather"}, query))

    def test_matches_only_title_and_abstract_and_whole_words(self):
        query = {"feed_keywords": [["world model"], ["robotic"]]}
        self.assertFalse(matches_query({"title": "world model", "authors": ["robotic"]}, query))
        self.assertFalse(matches_query({"title": "world model for robotics"}, query))
        self.assertFalse(matches_query({"title": "world", "abstract": "model for robotic tasks"}, query))
        self.assertTrue(matches_query({"title": "world model", "abstract": "for robotic tasks"}, query))

    def test_missing_or_invalid_keyword_groups_fail_explicitly(self):
        for value in (None, [], ["world model"], [[]], [[""]], [[None]]):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    matches_query({}, {"feed_keywords": value})


if __name__ == "__main__":
    unittest.main()
