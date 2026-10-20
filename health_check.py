import time
from datetime import datetime, timezone
import requests

# Anything slower than this many seconds gets flagged as SLOW
SLOW_THRESHOLD_SECONDS = 1.0

# The report file the script will create
REPORT_FILE = "escalation_report.md"

# Public endpoints to check (no login needed)
ENDPOINTS = [
    "https://api.github.com",
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://httpbin.org/status/200",
    "https://httpbin.org/delay/2",     # slow on purpose
    "https://httpbin.org/status/500",  # fails on purpose
]


def check_endpoint(url):
    """Call one URL and return its status code and response time."""
    start = time.time()
    try:
        response = requests.get(url, timeout=10)
        elapsed = round(time.time() - start, 2)
        return {"url": url, "status": response.status_code, "seconds": elapsed, "error": None}
    except requests.exceptions.RequestException as error:
        elapsed = round(time.time() - start, 2)
        return {"url": url, "status": None, "seconds": elapsed, "error": str(error)}


def evaluate(result):
    """Label a result as OK, SLOW, or FAIL."""
    if result["error"] or result["status"] >= 400:
        return "FAIL"
    if result["seconds"] > SLOW_THRESHOLD_SECONDS:
        return "SLOW"
    return "OK"


def severity_for(label):
    """A failing endpoint is more urgent than a slow one."""
    return "High" if label == "FAIL" else "Medium"


def build_report(problems, total_checked, detected_at):
    """Turn the list of problems into a Markdown escalation report."""
    healthy = total_checked - len(problems)
    lines = [
        "# Escalation Report",
        "",
        f"Generated: {detected_at}",
        f"Endpoints checked: {total_checked}",
        f"Endpoints with issues: {len(problems)}",
        "",
    ]

    for result, label in problems:
        if result["error"]:
            actual = f"Request failed after {result['seconds']}s: {result['error']}"
        else:
            actual = f"Status {result['status']} in {result['seconds']}s"

        if label == "FAIL":
            summary = "Endpoint is failing"
        else:
            summary = "Endpoint is responding slowly"

        lines += [
            f"## {label}: {result['url']}",
            "",
            f"- **Summary:** {summary}",
            f"- **Detected at:** {detected_at}",
            f"- **Severity:** {severity_for(label)}",
            f"- **Expected:** Status 200-399 in under {SLOW_THRESHOLD_SECONDS}s",
            f"- **Actual:** {actual}",
            f"- **Steps to reproduce:** run `curl -i {result['url']}` in Terminal",
            f"- **Already checked:** {healthy} of {total_checked} endpoints responded normally",
            "- **Customer impact:** [fill in: who is affected and how]",
            "- **Escalate to:** [fill in: team or owner]",
            "",
        ]

    return "\n".join(lines)


def main():
    print("API Health Check\n")
    detected_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    counts = {"OK": 0, "SLOW": 0, "FAIL": 0}
    problems = []

    for url in ENDPOINTS:
        result = check_endpoint(url)
        label = evaluate(result)
        counts[label] += 1

        if label != "OK":
            problems.append((result, label))

        if result["error"]:
            detail = f"ERROR after {result['seconds']}s"
        else:
            detail = f"status {result['status']} in {result['seconds']}s"
        print(f"[{label}] {url} -> {detail}")

    print(f"\nSummary: {counts['OK']} OK, {counts['SLOW']} slow, {counts['FAIL']} failing")

    if problems:
        report = build_report(problems, len(ENDPOINTS), detected_at)
        with open(REPORT_FILE, "w", encoding="utf-8") as file:
            file.write(report)
        print(f"Escalation report written to {REPORT_FILE}")
    else:
        print("All endpoints healthy. No escalation needed.")


if __name__ == "__main__":
    main()