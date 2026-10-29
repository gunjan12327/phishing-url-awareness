
# Phishing URL Awareness Checker - Test Results

**Python version used:** Python 3.13.12  
**Operating system:** Windows (PowerShell)  
**Execution Date:** 2026-10-29  
**Execution Status:** All tests verified against active `phishing_checker.py` execution.

---

## Workbook Test Summary Table

| # | Input | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|
| 1 | `https://www.example.com/login` | No listed warning signs | `- No listed warning signs found. This does NOT prove safety.` | **PASS** |
| 2 | `http://192.0.2.10/account` | IP address + HTTP | `- Uses an IP address instead of a familiar domain.`<br>`- Uses HTTP. HTTPS alone does not prove trust.`<br>`REVIEW CAREFULLY: 2 warning sign(s) found.` | **PASS** |
| 3 | `http://example.com@sample.invalid/login` | @ symbol + HTTP | `- Contains an @ symbol; inspect carefully.`<br>`- Uses HTTP. HTTPS alone does not prove trust.`<br>`REVIEW CAREFULLY: 2 warning sign(s) found.` | **PASS** |
| 4 | `https://a.b.c.d.e.example.invalid/path` | Many hostname segments | `- Contains many hostname segments/subdomains.`<br>`REVIEW CAREFULLY: 1 warning sign(s) found.` | **PASS** |
| 5 | `https://xn--example.invalid/` | Punycode-style hostname | `- Contains a punycode-style hostname.`<br>`REVIEW CAREFULLY: 1 warning sign(s) found.` | **PASS** |

---

## Detailed Test Cases

### Test 1: Legitimate Sample HTTPS URL
- **Input URL:** `https://www.example.com/login`
- **Expected Result:** No listed warning signs found.
- **Actual Output:**
  ```text
  Result:
  - No listed warning signs found. This does NOT prove safety.

  Never enter passwords from unexpected links.
  ```
- **Status:** **PASS**
- **Observation:** Legitimate standard domain using HTTPS triggers no heuristics. The safety reminder ensures users do not assume unflagged links are safe.

---

### Test 2: IP Address Hostname with Insecure HTTP
- **Input URL:** `http://192.0.2.10/account`
- **Expected Result:**
  - Uses an IP address instead of a familiar domain.
  - Uses HTTP.
  - Summary alert indicating warning signs.
- **Actual Output:**
  ```text
  Result:
  - Uses an IP address instead of a familiar domain.
  - Uses HTTP. HTTPS alone does not prove trust.

  REVIEW CAREFULLY: 2 warning sign(s) found.

  Never enter passwords from unexpected links.
  ```
- **Status:** **PASS**
- **Observation:** Direct IP address usage bypasses normal domain registration and obscures destination identity; combined with unencrypted HTTP, this is a major warning.

---

### Test 3: Embedded Userinfo `@` Symbol with HTTP
- **Input URL:** `http://example.com@sample.invalid/login`
- **Expected Result:**
  - Contains an @ symbol.
  - Uses HTTP.
  - Summary alert indicating warning signs.
- **Actual Output:**
  ```text
  Result:
  - Contains an @ symbol; inspect carefully.
  - Uses HTTP. HTTPS alone does not prove trust.

  REVIEW CAREFULLY: 2 warning sign(s) found.

  Never enter passwords from unexpected links.
  ```
- **Status:** **PASS**
- **Observation:** Browsers interpret text prior to `@` as user credentials and actually navigate to `sample.invalid`. Phishers use this trick to spoof well-known brand names.

---

### Test 4: Excessive Hostname Segments (Subdomain Flooding)
- **Input URL:** `https://a.b.c.d.e.example.invalid/path`
- **Expected Result:**
  - Contains many hostname segments/subdomains.
  - Summary alert indicating warning signs.
- **Actual Output:**
  ```text
  Result:
  - Contains many hostname segments/subdomains.

  REVIEW CAREFULLY: 1 warning sign(s) found.

  Never enter passwords from unexpected links.
  ```
- **Status:** **PASS**
- **Observation:** Having 5 or more dots/segments in the hostname often masks the true apex domain or simulates trusted domains in sub-labels.

---

### Test 5: Internationalized Domain Name (Punycode Prefix)
- **Input URL:** `https://xn--example.invalid/`
- **Expected Result:**
  - Contains a punycode-style hostname.
  - Summary alert indicating warning signs.
- **Actual Output:**
  ```text
  Result:
  - Contains a punycode-style hostname.

  REVIEW CAREFULLY: 1 warning sign(s) found.

  Never enter passwords from unexpected links.
  ```
- **Status:** **PASS**
- **Observation:** The `xn--` prefix indicates punycode representation for non-ASCII characters, which is frequently used in IDN homograph spoofing attacks (e.g. Cyrillic letters that look identical to Latin letters).

---

## Bonus Edge Case Verifications

### Edge Case A: Empty Input
- **Input:** `""` (User presses Enter without typing a URL)
- **Actual Output:**
  ```text
  Result:
  - No URL entered.

  Never enter passwords from unexpected links.
  ```
- **Status:** **PASS** (Handled cleanly without raising exceptions)

### Edge Case B: Malformed URL Syntax
- **Input:** `http://[bad`
- **Actual Output:**
  ```text
  Result:
  - This text is not a valid URL format.

  Never enter passwords from unexpected links.
  ```
- **Status:** **PASS** (Protected by `try...except ValueError` block; avoids crashes)

### Edge Case C: Interactive Session Exit
- **Input:** `q` (or `quit` / `exit`)
- **Actual Output:**
  ```text
  Goodbye! Stay alert online.
  ```
- **Status:** **PASS** (Interactive loop terminates cleanly)

---

## Notes & What We Learned
1. **Defensive Heuristics vs. Proof of Safety:** A URL having no warnings is **not** proof of legitimacy. Many real phishing sites now operate on standard HTTPS domains with clean subdomains.
2. **Deceptive Anatomy:** Attackers exploit browser parsing rules (such as user credentials before `@` or punycode rendering) to make links appear authentic at a glance.
3. **Safe Local Analysis:** Pure string inspection allows users to evaluate link structure without risking network traffic, DNS leaks, or drive-by payload downloads.


