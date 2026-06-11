# Agent Working

A minimal, dark-mode terminal screensaver for macOS and Linux. Perfect for when AI agents are working on your laptop and you don't want anyone to touch it — with an optional **real OS lock** that keeps the machine awake (and even keeps running with the lid closed) so the agent never stops.

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

Press `Ctrl+C` to exit. The plain command shows the animated "DO NOT TOUCH"
display and prevents the machine from sleeping while it runs.

### Options

| Flag         | What it does                                                                 |
| ------------ | ---------------------------------------------------------------------------- |
| `--lock`     | Lock the real OS screen (password required) while keeping the system awake.  |
| `--lid`      | Keep working even with the lid closed (macOS). Asks for confirmation first.   |
| `-y`, `--yes`| Skip the `--lid` safety confirmation prompt (for non-interactive use).        |
| `-h`, `--help`| Show help and exit.                                                          |

These compose — the typical "leave it locked and working" invocation is:

```bash
agent-working --lock --lid
```

### Lock mode (`--lock`)

```bash
agent-working --lock
```

Locks the OS screen so nobody can touch the laptop, while keeping the machine
awake so your agents keep running behind the lock screen.

- **macOS** — keeps the *system* awake with `caffeinate -i` (works on **AC and
  battery**) while letting the *display* lock. The lock itself uses
  `login.framework`'s `SACLockScreenImmediate` — a real, immediate, secure lock
  with no Accessibility permission required.
- **Linux** — inhibits idle/sleep via `systemd-inhibit` and locks the session
  (`loginctl lock-session`, with `xdg-screensaver` / `gnome-screensaver` /
  `dm-tool` fallbacks).

Unlock normally; the timer and caffeinate keep running until you press `Ctrl+C`.

> **Why you don't see the animation while locked:** the lock is the real,
> OS-owned secure lock screen, and no terminal app can draw on top of it.
> Instead, on macOS `--lock` sets a *"agents working - please do not touch"*
> message on the native lock screen (via `LoginwindowText`). That needs admin,
> so `--lock` prompts for `sudo` **once**; your previous message is restored on
> exit. Decline sudo and it still locks, just without the custom message. The
> animation reappears the moment you unlock.

### Keep working with the lid closed (`--lid`)

By default, closing the lid triggers clamshell sleep that `caffeinate` **cannot**
override, so the agent pauses. Add `--lid` to keep working with the lid shut:

```bash
agent-working --lock --lid
```

This disables lid-close sleep via `pmset disablesleep 1` (needs `sudo` once) and
**restores your previous setting automatically on exit**. macOS only — on other
platforms the flag is ignored with a notice.

`--lid` shows a prominent warning and **requires explicit confirmation** before
changing anything:

- Type anything other than `y` → the lid feature is cancelled (the lock still
  works; the Mac just sleeps on lid close).
- No terminal to ask (piped/automated) → it **refuses** rather than silently
  keeping the lid awake. Pass `-y`/`--yes` to accept the risk non-interactively.

> ⚠️ **Heat & battery warning.** With the lid shut and no airflow, a Mac running
> at full power can **overheat**. Use `--lid` only while **plugged into power**
> and on a **hard, open surface** — never in a bag or under cover.

## Features

- Dark red, sleep-friendly display
- "DO NOT TOUCH" ASCII banner with a live timer of how long agents have worked
- Live AI news from TechCrunch / The Verge (refreshes every 30 min)
- Prevents sleep automatically (caffeinate on macOS, `systemd-inhibit` on Linux)
- `--lock` — real secure OS lock + custom lock-screen message, while staying
  awake on AC **and** battery
- `--lid` — keep agents running with the lid closed (macOS), with a mandatory
  safety confirmation and automatic restore on exit

## Requirements

- macOS or Linux
- Python 3.8+
- `--lock` message and `--lid` use `sudo` on macOS (you'll be prompted once)

## License

MIT
