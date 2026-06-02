# Contributing to teamtalk5_py-os

Thank you for contributing to the accessible TeamTalk 5 client for PyOS.
This guide is written to work well with screen readers and keyboard-only navigation.
Every step is numbered and linear — no visual layout is assumed.

---

## Ways to contribute

1. Report a bug — something does not work as expected
2. Report an accessibility issue — a control is not announced correctly or is unreachable by keyboard
3. Request a feature — something that would help blind TeamTalk users
4. Fix a bug or add a feature
5. Improve documentation

---

## Before you start

1. A GitHub account — github.com/join
2. Git — git-scm.com
3. Python 3.9 or later — python.org
4. wxPython — `pip install wxPython`
5. TeamTalk 5 SDK (optional, simulation mode works without it)

---

## Step 1 — Fork

1. Open github.com/tech-master33/teamtalk5_py-os
2. Activate Fork → Create fork
3. Your copy is at github.com/YOUR-USERNAME/teamtalk5_py-os

---

## Step 2 — Clone

```bash
git clone https://github.com/YOUR-USERNAME/teamtalk5_py-os.git
cd teamtalk5_py-os
git remote add upstream https://github.com/tech-master33/teamtalk5_py-os.git
pip install wxPython flake8
```

---

## Step 3 — Branch

```bash
git checkout -b your-branch-name
```

Examples: `fix/chat-not-announced`, `feature/server-bookmarks`, `a11y/status-bar-label`

---

## Step 4 — Make changes

Key files:

- `teamtalk5_app.py` — main GUI client, `TeamTalk5App` class
- `teamtalk_sdk.py` — SDK wrapper, ctypes bindings
- `teamtalk_sdk_test.py` — unit tests
- `teamtalk_config.ini` — default configuration

### Accessibility rules

1. Every `wx.Button`, `wx.TextCtrl`, and `wx.ListBox` must have a meaningful label
2. Status changes (connected, disconnected, joined channel) must call `self.api.speak()`
3. Errors must be announced and not silently ignored
4. Every action must be reachable by keyboard without a mouse
5. Test navigation with the Tab key before submitting

---

## Step 5 — Lint and test

```bash
flake8 . --select=E9,F63,F7,F82   # Must pass
python -m py_compile teamtalk5_app.py
python teamtalk_sdk_test.py
```

---

## Step 6 — Commit

```bash
git add .
git commit -m "fix: chat messages not announced when received

The on_message_received handler updated the display but did not
call self.api.speak(). Added a speak call for new messages."
```

Types: `fix`, `feature`, `docs`, `refactor`, `a11y`, `test`

---

## Step 7 — Push and pull request

```bash
git push origin your-branch-name
```

1. Open github.com/YOUR-USERNAME/teamtalk5_py-os
2. Activate Compare and pull request
3. Title: one sentence — what changed
4. Description: what problem does this solve, how did you test it
5. Activate Create pull request

---

## Reporting a bug

1. Open github.com/tech-master33/teamtalk5_py-os/issues
2. Activate New issue → Bug report
3. Include: what you did, what happened, Python version, OS, and whether the SDK is installed

---

## Community

- Issues: github.com/tech-master33/teamtalk5_py-os/issues
- BAOSP main: github.com/tech-master33/baosp
