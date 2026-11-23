# PengengTrabaho — Philippine job sources

This fork is configured for Philippine Cloud, AWS, DevOps, Infrastructure, Networking and IT Support roles. It retains ScottCoffin/Job_Scraper's original collectors and dashboard.

## Live collector integrations (subject to source availability)
- **LinkedIn**: Existing LinkedIn workflow; searches Philippines and Metro Manila. Source is an unofficial public guest endpoint, so availability and access restrictions can change.
- **Indeed**: Existing JobSpy/Indeed workflow, configured for the Philippines.
- **Google Jobs**: Existing JobSpy workflow, configured for Philippine searches. Some listings link to other job boards. An individual posting URL is required.
- **Glassdoor**: Existing collector, configured for the Philippines, but provider support and search results may vary.
- **JobStreet**: Added the JobSpy `seek` integration and its own workflow. **Disabled by default** because the source's access terms and permitted automated use must be assessed before enabling. To enable *only if you have authorization*, set repository Actions variable `ENABLE_JOBSTREET_SCRAPER=true`. Then manually trigger **JobStreet PH (opt-in)**. This uses the individual job URL returned by JobSpy; no generic search-link results are inserted into the job database.

## Other useful Philippine job sites

The dashboard includes clickable **search shortcuts**, **not automated job feed integrations**, for:
- [Kalibrr](https://www.kalibrr.com/)
- [Bossjob](https://bossjob.ph/)
- [Mynimo](https://www.mynimo.com/)
- [PhilJobNet](https://philjobnet.gov.ph/)
- [OnlineJobs.ph](https://www.onlinejobs.ph/)

Direct-feed integrations for these providers require permitted APIs/feeds or verified employer-specific job endpoints. Do not present their general search pages as individual jobs.

## Initial setup

1. Review `config.json`, especially `keywords.include`, `keywords.exclude`, `search_terms` and `locations`.
2. Set GitHub Actions variable `ENABLE_DATA_COMMITS=true` and enable **Read and write** workflow permissions.
3. In GitHub Actions run **Validate Setup**, then run **LinkedIn Watcher**, **Indeed Watcher**, and **Google Jobs Watcher** one at a time.
4. For a Philippine LinkedIn historical backfill, use the ordinary LinkedIn Watcher's one-time backfill toggle; the **LinkedIn Backfill (Parallel)** workflow is designed for US partitions.
5. Enable GitHub Pages on `main` / root to publish `triage.html`.
6. After the workflows commit results, reload the dashboard. Browser reload **does not initiate a new scrape**.

## Direct links, reliability and freshness

- Results use an individual listing URL from the data source. The job description may be missing or truncated if the board does not expose it.
- Collection success does not guarantee that a job is still open: verify the listing before applying.
- `date_posted` is provider-reported and may not be available or accurate. Do not confuse the source posting date with `scraped_at`/first discovery.
- Scraping may be blocked, throttled or disallowed by source terms. Respect robots, terms, rate limits, and access controls. Do not bypass CAPTCHAs, login protections, or anti-bot controls.
- The fork is public; repository job-tracker data is visible publicly and local dashboard application statuses are browser-local. Do not commit personal résumé data or API tokens.

## Test locally

```powershell
python -m pip install -r requirements.txt
python scrape_jobs.py --linkedin-only
python scrape_jobs.py --indeed-only
python scrape_jobs.py --google-jobs-only
python -m http.server 8000
```

Then visit http://localhost:8000/triage.html.

JobStreet is **not enabled** without `ENABLE_JOBSTREET_SCRAPER=true`. When authorized, run `python jobstreet_collector.py` after setting the environment variable, or use the opt-in GitHub Action.
