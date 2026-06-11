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

#### Lid closed

By default, closing the lid sleeps the Mac (caffeinate can't override that), so
the agent pauses. Add `--lid` to keep working with the lid shut:

```bash
agent-working --lock --lid
```

This disables lid-close sleep (`pmset disablesleep 1`, needs `sudo` once) and
restores it on exit. macOS only.

`--lid` shows a prominent warning and asks for confirmation before doing
anything. Pass `-y`/`--yes` to skip the prompt for non-interactive use; without
a terminal to confirm, it refuses (fails safe) unless `--yes` is given.

> ⚠️ A closed lid with no airflow can overheat. Use `--lid` only while on power
> and on a hard surface - never in a bag.

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
