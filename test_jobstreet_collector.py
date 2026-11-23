"""Offline contract tests for the opt-in Philippine JobStreet collector."""
import os
import unittest
from unittest.mock import patch
import jobstreet_collector


class JobStreetCollectorTests(unittest.TestCase):
    def test_disabled_by_default(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(jobstreet_collector.scraper, "_scrape_jobspy_board") as collect:
                jobstreet_collector.run()
                collect.assert_not_called()

    def test_enabled_uses_seek_and_individual_links(self):
        rows = [
            {"title": "Junior Cloud Engineer", "company": "Example PH", "location": "Manila",
             "url": "https://www.jobstreet.com.ph/job/12345678", "date_posted": "2026-11-23"},
            {"title": "Cloud Engineer", "company": "Example PH",
             "url": "https://www.jobstreet.com.ph/cloud-engineer-jobs"},
            {"title": "Broken", "company": "Example PH", "url": ""},
        ]
        with patch.dict(os.environ, {"ENABLE_JOBSTREET_SCRAPER": "true"}):
            with patch.object(jobstreet_collector.scraper, "_scrape_jobspy_board", return_value=rows) as collect:
                with patch.object(jobstreet_collector.scraper, "save_jobs_output") as save:
                    jobstreet_collector.run()
        self.assertEqual(collect.call_args.kwargs["site_name"], "seek")
        self.assertEqual(collect.call_args.kwargs["geos"][0]["country"], "Philippines")
        saved = save.call_args.args[0]
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["url"], "https://www.jobstreet.com.ph/job/12345678")


if __name__ == "__main__":
    unittest.main()
