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

### Lock mode

```bash
agent-working --lock
```

Locks the OS screen so nobody can touch the laptop, while keeping the machine
awake so your agents keep running behind the lock screen. On macOS this keeps
the *system* awake (`caffeinate -i`, which also works on battery) while letting
the *display* lock; on Linux
it inhibits idle/sleep and locks the session. Unlock normally; the timer and
caffeinate keep running until you press `Ctrl+C`.

> **Note:** the lock is the real, OS-owned secure lock screen, so the animated
> terminal display can't be drawn on top of it. On macOS, `--lock` instead sets
> a *"agents working - please do not touch"* message on the native lock screen
> (via `LoginwindowText`). Setting that message needs admin, so `--lock` prompts
> for `sudo` once; your previous message is restored on exit. If you decline
> sudo, it still locks, just without the custom message.

## Features

- Dark red, sleep-friendly display
- "DO NOT TOUCH" ASCII banner
- `--lock` mode: lock the screen but stay awake so agents keep working
- Live AI news from TechCrunch/The Verge (refreshes every 30 min)
- Timer showing how long agents have been working
- Auto-prevents sleep (caffeinate on macOS, systemd-inhibit on Linux)

## Requirements

- macOS or Linux
- Python 3.8+

## License

MIT
