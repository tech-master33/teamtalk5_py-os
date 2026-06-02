# Security Policy

## Why security matters in this project

The andrdscren screen reader runs as a privileged AccessibilityService.
That means it can read the content of every app on the device — including banking apps,
password managers, and messaging apps.

The aotts TTS engine runs as a system-level service that processes all text
sent to it before speaking it aloud.

A security flaw in either of these components could expose private information
to anyone with access to the device or its network.
Because the primary users of this project are blind people who depend on these services
to use their phones at all, a broken or compromised accessibility service is not just
a privacy problem — it can make the entire device unusable.

Please report security vulnerabilities. Every report is taken seriously.

---

## How to report a vulnerability

**Do not open a public GitHub issue for a security vulnerability.**
Public issues are readable by everyone, including people who might exploit the problem
before it is fixed.

Use one of these private channels instead:

### Option 1 — GitHub private security advisory (preferred)

1. Open the Security tab on the relevant repository:
   - Screen reader: github.com/tech-master33/andrdscren/security/advisories/new
   - TTS engine: github.com/tech-master33/aotts/security/advisories/new
   - AOSP build: github.com/tech-master33/baosp/security/advisories/new
2. Activate New draft security advisory
3. Fill in the form — described in detail below
4. Submit — only you and the maintainers can see it

### Option 2 — Direct message on GitHub

Send a direct message to github.com/tech-master33 with:
- A short subject line describing the type of vulnerability
- The full details in the message body

---

## What to include in your report

Include as much of the following as you can.
You do not need to have a complete analysis — a partial report is better than no report.

1. Which component is affected — andrdscren, aotts, or the AOSP build
2. A description of the vulnerability in plain language
3. What an attacker could do if they exploited it
4. Steps to reproduce or a proof of concept — a description of the steps is enough,
   you do not need to write exploit code
5. The Android version and device model where you confirmed the problem
6. The APK version (the short commit SHA from the nightly release filename)
7. Whether you think this is already being exploited or is just a potential risk

---

## What happens after you report

1. You will receive an acknowledgment within 72 hours
2. The maintainer will assess the severity and ask any follow-up questions
3. A fix will be developed privately
4. The fix will be released and a public security advisory will be published
5. You will be credited in the advisory if you want to be

The time from report to fix depends on the severity and complexity.
A critical vulnerability that makes the device unusable or exposes passwords
will be treated as the highest priority.

---

## Supported versions

Security fixes are applied to the latest version only.
If you are running an old nightly build, update to the latest before reporting —
the problem may already be fixed.

| Component | Supported |
|-----------|-----------|
| Latest nightly build | Yes — fixes applied here |
| Older nightly builds | No — update to the latest |
| Locally built from source (latest main) | Yes |
| Locally built from older commits | No |

---

## Scope — what counts as a security vulnerability

These are in scope:

- Any way for a third-party app to read data that andrdscren or aotts processes
- Any way for an attacker to use the screen reader's AccessibilityService permissions
  to access apps or data without the user's knowledge
- Any way for malicious text input to crash or compromise the TTS engine
- Any unintended network communication by either app
- Any vulnerability in the AOSP platform patches included in the BAOSP build
- Any way for a locally installed app to gain the system privileges that BAOSP grants
  to andrdscren or aotts

These are out of scope:

- Vulnerabilities in the Android OS that BAOSP does not modify
- Vulnerabilities in SVOX Pico that would also affect the upstream AOSP version
- Theoretical attacks with no realistic exploitation path
- Issues that require physical access to an already unlocked device

If you are not sure whether something is in scope, report it anyway.
It is better to get a "this is out of scope" response than to not report a real problem.

---

## Responsible disclosure

Please give the maintainers a reasonable amount of time to fix the problem before
publishing details publicly. For most vulnerabilities, 90 days is standard.
For a critical vulnerability that is actively being exploited, contact the maintainer
immediately and we will work as fast as possible.

The maintainer will not take legal action against good-faith security researchers.
