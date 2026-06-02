# Agent Working

A minimal, dark-mode terminal screensaver for macOS and Linux. Perfect for when AI agents are working on your laptop and you don't want anyone to touch it.

![demo](demo.gif)

## Installation

**pip:**
```bash
pip install agent-working
```

**uv:**
```bash
uv tool install agent-working
```

**Homebrew:**
```bash
brew install infinity811/tap/agent-working
```

**pipx (Linux):**
```bash
pipx install agent-working
```

## Usage

```bash
agent-working
```

Press `Ctrl+C` to exit.

## Features

- Dark red, sleep-friendly display
- "DO NOT TOUCH" ASCII banner
- Live AI news from TechCrunch/The Verge (refreshes every 30 min)
- Timer showing how long agents have been working
- Auto-prevents sleep (caffeinate on macOS, systemd-inhibit on Linux)

## Requirements

- macOS or Linux
- Python 3.8+

## License

MIT
