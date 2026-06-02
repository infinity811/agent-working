# Agent Working Screensaver

A minimal, dark-mode terminal screensaver for macOS and Linux. Perfect for when AI agents are working on your laptop and you don't want anyone to touch it.

## Features

- Dark red, sleep-friendly display
- "DO NOT TOUCH" ASCII banner
- Live AI news from TechCrunch/The Verge (refreshes every 30 min)
- Timer showing how long agents have been working
- Auto-prevents sleep (caffeinate on macOS, systemd-inhibit on Linux)
- Single command to start

## Installation

```bash
git clone https://github.com/infinity811/agent-working.git
cd agent-working
./install.sh
```

Then open a new terminal or run `source ~/.zshrc` (or `~/.bashrc`).

## Usage

```bash
agent-working
```

Press `Ctrl+C` to exit.

## Screenshot

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║      ██████╗  ██████╗     ███╗   ██╗ ██████╗ ████████╗           ║
║      ██╔══██╗██╔═══██╗    ████╗  ██║██╔═══██╗╚══██╔══╝           ║
║      ██║  ██║██║   ██║    ██╔██╗ ██║██║   ██║   ██║              ║
║      ██║  ██║██║   ██║    ██║╚██╗██║██║   ██║   ██║              ║
║      ██████╔╝╚██████╔╝    ██║ ╚████║╚██████╔╝   ██║              ║
║      ╚═════╝  ╚═════╝     ╚═╝  ╚═══╝ ╚═════╝    ╚═╝              ║
║                                                                  ║
║      ████████╗ ██████╗ ██╗   ██╗ ██████╗██╗  ██╗                 ║
║      ╚══██╔══╝██╔═══██╗██║   ██║██╔════╝██║  ██║                 ║
║         ██║   ██║   ██║██║   ██║██║     ███████║                 ║
║         ██║   ██║   ██║██║   ██║██║     ██╔══██║                 ║
║         ██║   ╚██████╔╝╚██████╔╝╚██████╗██║  ██║                 ║
║         ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝                 ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

                    agents working for 2h 34m

                    please do not touch ···

              › OpenAI announces new reasoning model
```

## Requirements

- macOS or Linux
- Python 3
- Terminal with dark background

## License

MIT
