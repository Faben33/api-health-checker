# API Health Checker

*A small Python tool that checks API endpoints, flags failures and slow responses, and generates a ready-to-use escalation report*.

I built it to practice the same workflow I follow in technical support and incident management: **detect, investigate, document, escalate.**

## What it does

- Calls a list of public API endpoints
- Records the status code and response time for each
- Labels each result as **OK**, **SLOW**, or **FAIL**
- Writes an escalation report in Markdown for every problem found, with summary, severity, expected vs. actual behavior, and steps to reproduce

## Example output

    [OK] https://api.github.com -> status 200 in 0.24s
    [SLOW] https://httpbin.org/delay/2 -> status 200 in 2.53s
    [FAIL] https://httpbin.org/status/500 -> status 500 in 0.53s

    Summary: 1 OK, 1 slow, 1 failing

See [sample_escalation_report.md](sample_escalation_report.md) for a generated report.

## How to run

1. Install Python 3
2. Install the dependency: `pip install -r requirements.txt`
3. Run: `python3 health_check.py`

To test your own endpoints, edit the `ENDPOINTS` list at the top of `health_check.py`. The slowness limit is set by `SLOW_THRESHOLD_SECONDS`.

## Limitations

- A 200 status only means an endpoint answered. Status pages can return 200 while reporting an incident inside the response.
- It uses public endpoints only. No real customer or company data is used.

## What I'm learning

Building my Python and API skills alongside a Project Management course.

## Author

Fabiola González · [LinkedIn](https://www.linkedin.com/in/fabiola-gonzalez-socorro-8ba728116/)
