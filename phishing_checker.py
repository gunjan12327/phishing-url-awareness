"""
EWB Phishing URL Awareness Checker
Educational Mini Project - Defensive Learning Only

This program inspects visible URL text for selected heuristic warning signs.
It operates purely on text analysis and never visits, connects to,
or sends requests to any URL.
"""

import re
from urllib.parse import urlparse

# Messages indicating informational status rather than active phishing heuristics
INFO_MESSAGES = (
    "No URL entered.",
    "Could not identify a hostname.",
    "This text is not a valid URL format.",
    "No listed warning signs found. This does NOT prove safety.",
)


def inspect_url(raw_url):
    """Check visible URL text for selected warning signs."""
    url = raw_url.strip()
    findings = []

    if not url:
        return ["No URL entered."]

    try:
        candidate = url if "://" in url else "http://" + url
        parsed = urlparse(candidate)
        host = (parsed.hostname or "").lower()
    except ValueError:
        return ["This text is not a valid URL format."]

    if not host:
        return ["Could not identify a hostname."]

    # 1. Check for @ symbol
    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")

    # 2. Check URL length
    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")

    # 3. Check for IP address
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append("Uses an IP address instead of a familiar domain.")

    # 4. Check for many hostname segments
    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")

    # 5. Check for punycode
    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")

    # 6. Check for HTTP
    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")

    if not findings:
        findings.append(
            "No listed warning signs found. This does NOT prove safety."
        )

    return findings


def has_warnings(findings):
    """Check if the findings contain actual security warning signs."""
    return any(item not in INFO_MESSAGES for item in findings)


def main():
    print("=" * 50)
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")
    print("=" * 50)

    # Improvement 1: Loop allowing multiple URL checks without restarting
    while True:
        print()
        raw_url = input("Enter a sample URL to inspect (or 'q' to quit): ").strip()

        if raw_url.lower() in ("q", "quit", "exit"):
            print("\nGoodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)

        print("\nResult:")
        for item in findings:
            print("- " + item)

        # Improvement 2: Clear summary alert when warnings are detected
        if has_warnings(findings):
            print(f"\nREVIEW CAREFULLY: {len(findings)} warning sign(s) found.")

        print("\nNever enter passwords from unexpected links.")


if __name__ == "__main__":
    main()