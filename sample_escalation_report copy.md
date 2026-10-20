# Escalation Report

Generated: 2026-10-20 17:36 UTC
Endpoints checked: 5
Endpoints with issues: 2

## SLOW: https://httpbin.org/delay/2

- **Summary:** Endpoint is responding slowly
- **Detected at:** 2026-10-20 17:36 UTC
- **Severity:** Medium
- **Expected:** Status 200-399 in under 1.0s
- **Actual:** Status 200 in 2.53s
- **Steps to reproduce:** run `curl -i https://httpbin.org/delay/2` in Terminal
- **Already checked:** 3 of 5 endpoints responded normally
- **Customer impact:** [fill in: who is affected and how]
- **Escalate to:** [fill in: team or owner]

## FAIL: https://httpbin.org/status/500

- **Summary:** Endpoint is failing
- **Detected at:** 2026-10-20 17:36 UTC
- **Severity:** High
- **Expected:** Status 200-399 in under 1.0s
- **Actual:** Status 500 in 0.58s
- **Steps to reproduce:** run `curl -i https://httpbin.org/status/500` in Terminal
- **Already checked:** 3 of 5 endpoints responded normally
- **Customer impact:** [fill in: who is affected and how]
- **Escalate to:** [fill in: team or owner]
