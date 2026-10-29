# Phishing URL Awareness Checker

An educational, beginner-friendly cybersecurity mini project built in Python. This tool inspects the visible text structure of suspicious URLs for common heuristic warning signs without ever visiting or connecting to the web pages.

Developed as part of the **EWB Cybersecurity Mini Project** curriculum.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Project Folder Structure](#project-folder-structure)
- [Installation and Execution (Windows & macOS/Linux)](#installation-and-execution)
- [Example Input and Output](#example-input-and-output)
- [Testing and Results](#testing-and-results)
- [Implemented Improvements](#implemented-improvements)
- [Screenshots](#screenshots)
- [Limitations](#limitations)
- [Ethical Use and Safety Disclaimer](#ethical-use-and-safety-disclaimer)

---

## Project Overview

**Phishing** is a social engineering attack where malicious actors craft deceptive messages, emails, or links to trick victims into revealing sensitive information—such as login credentials, credit card details, or one-time passwords (OTPs). Deceptive links often look legitimate at a casual glance but use structural tricks to divert traffic to fraudulent servers.

The **Phishing URL Awareness Checker** is a local, lightweight Python command-line utility designed for defensive security awareness. It performs heuristic textual analysis on candidate URLs, looking for six structural red flags commonly seen in deceptive links.

---

## Objectives

1. **Understand Deceptive URL Anatomy:** Learn how attackers manipulate URL schemes, credentials, hostnames, and domain labels.
2. **Safe Defensive Analysis:** Analyze potentially untrusted URLs locally using pure string parsing, preventing credential harvesting, DNS leakage, or malware downloads.
3. **Robust Scripting Skills:** Practice structured Python development with `urllib.parse`, regular expressions (`re`), input validation, and user feedback loops.

---

## Key Features

The tool evaluates URL text against **six security warning checks**:

1. **`@` Symbol in URL:** Browsers treat characters before `@` as user authentication credentials and route the request to the host specified *after* the `@`. Attackers exploit this to display a familiar brand name before the `@` while steering visitors to an attacker-controlled server.
2. **Unusually Long URL (> 100 characters):** Attackers often pad URLs with excessive subdomains, random hash parameters, or obfuscated tokens to conceal destination details or bypass simple visual scans.
3. **IPv4 Address as Hostname:** Legitimate consumer services almost always use registered domain names. Using raw IPv4 addresses (e.g., `http://192.0.2.10/account`) avoids domain registration history and obfuscates ownership.
4. **Excessive Hostname Segments (≥ 5 labels):** Hostnames split into five or more dot-separated segments (e.g., `a.b.c.d.e.example.invalid`) frequently attempt to mimic multi-tiered institutional domains or hide the real top-level domain.
5. **Punycode Hostname (`xn--`):** The `xn--` prefix indicates Internationalized Domain Name (IDN) punycode encoding. Attackers use lookalike Cyrillic or Greek glyphs (homograph attacks) that mimic standard Latin letters in browsers.
6. **Insecure HTTP Scheme:** Flags plain `http://` connections. While HTTPS encrypts in transit, it does not prove safety; unencrypted HTTP is an immediate security risk for sensitive operations.

---

## Technologies Used

- **Language:** Python 3.10+ (Tested on Python 3.13)
- **Standard Library Modules:**
  - `urllib.parse` (`urlparse`): For standard-compliant URL parsing.
  - `re`: For regular expression matching on IP patterns.
- **External Dependencies:** **None** (zero third-party dependencies required).

---

## Requirements

- Python 3.10 or higher.
- A standard command terminal (PowerShell, Command Prompt, or Bash).
- No external packages required (standard Python installation is sufficient).

---

## Project Folder Structure

```text
phishing-url-awareness/
├── phishing_checker.py        # Core Python inspection program
├── README.md                  # Comprehensive project documentation
├── requirements.txt           # Dependency documentation (Python built-ins only)
├── screenshots/               # Terminal execution screenshots
│   ├── sample_run.png         # Screenshot of a sample interactive run
│   └── test_results.png       # Screenshot verifying test executions
└── tests/
    └── test_samples.md        # Documented test plan and verified results
```

---

## Installation and Execution

### Windows (PowerShell or Command Prompt)
1. Verify Python is installed:
   ```powershell
   python --version
   ```
2. Navigate to the project directory:
   ```powershell
   cd "C:\Users\<YourUsername>\OneDrive\Desktop\phishing-url-awareness"
   ```
3. Run the program:
   ```powershell
   python phishing_checker.py
   ```
   *(Alternatively, use `py phishing_checker.py`)*

### macOS / Linux
1. Verify Python is installed:
   ```bash
   python3 --version
   ```
2. Run the program:
   ```bash
   python3 phishing_checker.py
   ```

---

## Example Input and Output

### Sample 1: Suspicious IP Address over HTTP
```text
==================================================
EWB Phishing URL Awareness Checker
Text checks only - this program does not open URLs.
==================================================

Enter a sample URL to inspect (or 'q' to quit): http://192.0.2.10/account

Result:
- Uses an IP address instead of a familiar domain.
- Uses HTTP. HTTPS alone does not prove trust.

REVIEW CAREFULLY: 2 warning sign(s) found.

Never enter passwords from unexpected links.
```

### Sample 2: Legitimate Domain over HTTPS
```text
Enter a sample URL to inspect (or 'q' to quit): https://www.example.com/login

Result:
- No listed warning signs found. This does NOT prove safety.

Never enter passwords from unexpected links.
```

### Sample 3: Quitting the Session
```text
Enter a sample URL to inspect (or 'q' to quit): q

Goodbye! Stay alert online.
```

---

## Testing and Results

All five workbook test URLs have been verified against active execution in `phishing_checker.py`:

| # | Test Input URL | Key Expected Warning | Actual Verified Status | Pass/Fail |
|---|---|---|---|---|
| 1 | `https://www.example.com/login` | No listed warning signs | `- No listed warning signs found. This does NOT prove safety.` | **PASS** |
| 2 | `http://192.0.2.10/account` | IP Address + Insecure HTTP | Flags IP hostname & HTTP; reports 2 warnings | **PASS** |
| 3 | `http://example.com@sample.invalid/login` | `@` symbol + HTTP | Flags `@` symbol & HTTP; reports 2 warnings | **PASS** |
| 4 | `https://a.b.c.d.e.example.invalid/path` | Many hostname segments | Flags ≥ 5 segments; reports 1 warning | **PASS** |
| 5 | `https://xn--example.invalid/` | Punycode hostname | Flags punycode (`xn--`); reports 1 warning | **PASS** |

Complete test logs, actual command outputs, and edge case evaluations (empty input, malformed URL syntax) are documented in [`tests/test_samples.md`](tests/test_samples.md).

---

## Implemented Improvements

### Improvement 1: Multi-URL Interactive Loop with Graceful Exit (Option A)
- **What Changed:** Instead of inspecting a single URL and immediately terminating, `main()` wraps input handling in a `while True:` loop. Users can evaluate multiple URLs in a single session without restarting the script.
- **Exit Mechanism:** Typing `q`, `quit`, or `exit` displays a friendly exit message (`"Goodbye! Stay alert online."`) and terminates cleanly.
- **Why It Was Added:** Real-world triage requires checking multiple links received in emails or text messages consecutively.
- **Testing:** Verified by running multiple URLs in one command session and terminating via `q`.

### Improvement 2: Actionable "Review Carefully" Summary Alert (Option B)
- **What Changed:** Introduced a helper function `has_warnings(findings)` that distinguishes informational notices (e.g. empty input or no warnings) from active heuristics. When warnings exist, a prominent summary alert is printed:
  ```text
  REVIEW CAREFULLY: <N> warning sign(s) found.
  ```
- **Why It Was Added:** Provides an unambiguous visual verdict so non-technical users immediately recognize that caution is warranted.
- **Testing:** Verified across all five test cases: suspicious URLs trigger the alert with the exact count of flags, while clean links and info prompts do not.

### Additional Stability Enhancement: Malformed URL Protection (Option C)
- **What Changed:** Wrapped URL candidate parsing in a `try...except ValueError` block. Inputs with invalid bracket formatting (such as malformed IPv6 literals `http://[bad`) return `"This text is not a valid URL format."` rather than crashing Python.

---

## Screenshots

The project requires two genuine terminal screenshots saved in the `screenshots/` directory:

1. **`screenshots/sample_run.png`**  
   *Shows the terminal running `python phishing_checker.py`, checking a sample suspicious URL (e.g., `http://192.0.2.10/account`), and printing the detected warnings and summary.*  
   ![Sample run](screenshots/sample_run.png)

2. **`screenshots/test_results.png`**  
   *Shows evidence of the five workbook test URLs being evaluated in the terminal or the completed test report.*  
   ![Test results](screenshots/test_results.png)

> **Note on Screenshot Capture:** Please follow the instructions in the project guide to capture genuine terminal screenshots from your machine using `Win + Shift + S`.

---

## Limitations

- **Text-Only Heuristics:** This program inspects the visible characters of a URL string. It cannot evaluate web page content, backend scripts, or redirects.
- **No Internet Connectivity:** The tool intentionally does **not** visit websites, resolve DNS, check SSL/TLS certificate validity, or query real-time threat intelligence blacklists (e.g., Google Safe Browsing, VirusTotal).
- **Not Proof of Safety:** An absence of heuristic warning signs does **NOT** prove a URL is safe. Sophisticated phishing campaigns routinely register standard domain names with valid HTTPS certificates.

---

## Ethical Use and Safety Disclaimer

- **Defensive & Educational Learning Only:** This software is intended solely for student education, cybersecurity training, and personal awareness.
- **No Malicious Use:** Do not use this tool to harvest credentials, craft deceptive URLs, or assist in unauthorized testing.
- **Do Not Test Live Threat Links:** When practicing, use the five provided safe test strings or documentation samples. Never paste unknown, active malicious payloads into an untrusted environment.
- **Always Practice Safe Browsing:** Never enter passwords or personal data into unfamiliar links received via unsolicited emails, SMS messages, or social media.

---

## Author & Course Details

- **Project:** Phishing URL Awareness Checker
- **Course:** EWB Cybersecurity Mini Project
- **Language:** Python 3.10+
- **License:** Educational Open Source
