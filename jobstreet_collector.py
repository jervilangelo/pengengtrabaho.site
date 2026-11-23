"""Optional JobStreet Philippines collector via JobSpy's SEEK adapter.

Only run with appropriate authorization and respect the platform's terms.
Returns individual job posting links; no generic search-result URLs.
"""
import os
import re
from urllib.parse import urlparse
import scrape_jobs as scraper


def is_individual_posting(url):
    parsed = urlparse(str(url or ''))
    host = (parsed.hostname or '').lower()
    return (parsed.scheme == 'https' and
            (host == 'jobstreet.com.ph' or host.endswith('.jobstreet.com.ph') or
             host == 'seek.com.au' or host.endswith('.seek.com.au')) and
            bool(re.search(r'/job/[^/]+', parsed.path, re.I)))


def run():
    if os.environ.get("ENABLE_JOBSTREET_SCRAPER", "").lower() != "true":
        print("JobStreet collector disabled. Set ENABLE_JOBSTREET_SCRAPER=true only with authorized access.")
        return
    geos = scraper._cfg("locations.jobstreet", [{"location": "Philippines", "country": "Philippines"}])
    terms = scraper._cfg("search_terms.jobstreet", scraper._cfg("search_terms.seek", []))
    if not terms:
        print("No JobStreet search terms configured.")
        return
    jobs = scraper._scrape_jobspy_board(
        label="JobStreet",
        site_name="seek",
        geos=geos,
        terms=terms,
        hours_old=24,
        prev_basename="jobstreet_jobs",
        results_wanted=30,
    )
    # Only individual listing URLs from the provider are eligible for the dashboard.
    jobs = [j for j in jobs if is_individual_posting(j.get("url", ""))
            and j.get("title") and j.get("company")]
    scraper.save_jobs_output(
        jobs,
        basename="jobstreet_jobs",
        title="JobStreet — Philippines Cloud & IT Jobs",
        subtitle="JobStreet Philippines · recent individual postings",
        accent="#0d3880",
        empty_message="No newly discovered JobStreet listings.",
        window_label="last 24h",
        source="jobstreet",
    )


if __name__ == "__main__":
    run()
