# teamtalk5_py-os

[![Python CI](https://github.com/tech-master33/teamtalk5_py-os/actions/workflows/python.yml/badge.svg)](https://github.com/tech-master33/teamtalk5_py-os/actions/workflows/python.yml)

An accessible TeamTalk 5 voice communication client for PyOS — the accessible desktop environment for blind users. Built with Python and wxPython so every control is reachable by keyboard and screen reader.

## What is this?

TeamTalk 5 is a voice conferencing system widely used in the blind community for real-time voice chat, text messaging, and group channels. This client provides a fully accessible wxPython interface that integrates with the TeamTalk 5 SDK and runs inside PyOS.

## Features

- **Real TeamTalk 5 connection** — connects to any TeamTalk 5 server
- **Channel browser** — list and join channels by keyboard or swipe
- **Text chat** — send and receive messages in channels
- **User presence** — see who is in each channel
- **Simulation mode** — runs without the TeamTalk SDK installed, for testing
- **Screen reader integration** — all controls labelled, status changes spoken aloud
- **Keyboard shortcuts** — every action reachable without a mouse

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| `Tab` | Move between controls |
| `Enter` | Connect or join selected channel |
| `Up / Down` | Navigate channel or user list |
| `Ctrl+L` | Focus server address field |
| `Ctrl+U` | Focus username field |
| `Ctrl+P` | Focus password field |
| `Ctrl+M` | Focus chat input |
| `F1` | Show help text |

## Requirements

- Python 3.9 or later
- wxPython 4.x
- TeamTalk 5 SDK (optional — runs in simulation mode without it)

## Installing

```bash
git clone https://github.com/tech-master33/teamtalk5_py-os.git
cd teamtalk5_py-os
pip install wxPython
```

If you have the TeamTalk SDK, place `TeamTalk5.dll` (Windows) or `libteamtalk.so` (Linux) in the project root or install it system-wide. See `teamtalk_config.ini` for the full search path list.

## Running

```bash
python teamtalk5_app.py
```

On first launch without the SDK, the app starts in simulation mode and announces:
> "Warning: TeamTalk SDK not found. Client will run in simulation mode."

## Configuration — teamtalk_config.ini

| Setting | Default | Description |
|---------|---------|-------------|
| `[SDK] lib_path` | `./lib` | Folder containing the TeamTalk SDK library |
| `[Connection] default_host` | `localhost` | Pre-filled server address |
| `[Connection] default_port` | `10333` | Pre-filled port |
| `[Audio] codec` | `opus` | Audio codec (opus or speex) |

## Project structure

```
teamtalk5_py-os/
├── teamtalk5_app.py      ← Main wxPython client (TeamTalk5App class)
├── teamtalk_sdk.py       ← SDK wrapper (ctypes bindings)
├── teamtalk_sdk_test.py  ← Unit tests for SDK wrapper
├── teamtalk_config.ini   ← Default configuration
└── apps/                 ← Additional PyOS app modules
```

## Running the tests

```bash
python -m pytest teamtalk_sdk_test.py -v
```

Or without pytest:

```bash
python teamtalk_sdk_test.py
```

## Related projects

| Repo | What it does |
|------|-------------|
| [baosp](https://github.com/tech-master33/baosp) | BAOSP main project — accessible Android OS |
| [tt-classic-revived](https://github.com/tech-master33/tt-classic-revived) | TeamTalk classic web companion |

## License

Apache License 2.0
