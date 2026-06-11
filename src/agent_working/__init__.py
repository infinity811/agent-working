#!/usr/bin/env python3
"""
Agent Working Screensaver (Dark Mode - Sleep Friendly)
A calm terminal screensaver for bedroom use.
Press Ctrl+C to exit.
"""

import os
import sys
import time
import shutil
import argparse
import subprocess
import platform
import urllib.request
import xml.etree.ElementTree as ET

# Single dim color - dark red
RESET = "\033[0m"
DIM = "\033[2m"
COLOR = "\033[38;5;88m"  # Dark red
NEWS_COLOR = "\033[38;5;240m"  # Dim gray for news

BANNER = r"""
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
"""

def fetch_news():
    """Fetch latest AI news from TechCrunch"""
    headlines = []
    feeds = [
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    ]

    for url in feeds:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'agent-working/1.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()

            root = ET.fromstring(xml_data)
            for item in root.findall('.//item')[:8]:
                title = item.find('title')
                if title is not None and title.text:
                    headlines.append(title.text.strip())
            if headlines:
                break
        except:
            continue

    return headlines if headlines else ["ai news unavailable"]

def truncate_headline(headline, max_width):
    if len(headline) <= max_width:
        return headline
    return headline[:max_width - 3] + "..."

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def get_terminal_size():
    return shutil.get_terminal_size()

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

def start_caffeine(lock_mode=False):
    """Prevent sleep - works on macOS and Linux.

    In normal mode we keep the display awake so the screensaver stays visible.
    In lock mode we keep the *system* awake (so agents keep running) but let
    the *display* sleep/lock - otherwise the screen could never lock.
    """
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            # -d keeps display awake (normal). -i prevents idle system sleep
            # while allowing the display to lock - and works on battery too
            # (unlike -s, which only applies on AC power).
            flags = "-i" if lock_mode else "-d"
            return subprocess.Popen(
                ["caffeinate", flags],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        elif system == "Linux":
            # Inhibit idle/sleep but never the screen lock itself.
            return subprocess.Popen(
                ["systemd-inhibit", "--what=idle:sleep", "--why=agents working", "sleep", "infinity"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    except:
        pass
    return None

LOGINWINDOW_PLIST = "/Library/Preferences/com.apple.loginwindow"
LOCK_MESSAGE = "agents working - please do not touch"

def _get_lock_message():
    """Return the current macOS lock-screen message, or None if unset."""
    try:
        out = subprocess.run(
            ["defaults", "read", LOGINWINDOW_PLIST, "LoginwindowText"],
            capture_output=True, text=True,
        )
        if out.returncode == 0:
            return out.stdout.rstrip("\n")
    except OSError:
        pass
    return None

def set_lock_message(text):
    """Set the native macOS lock-screen message. Needs sudo. True on success."""
    try:
        r = subprocess.run(
            ["sudo", "defaults", "write", LOGINWINDOW_PLIST, "LoginwindowText", text]
        )
        return r.returncode == 0
    except OSError:
        return False

def restore_lock_message(previous):
    """Restore the lock-screen message to its prior value (or remove it)."""
    try:
        if previous is None:
            subprocess.run(
                ["sudo", "defaults", "delete", LOGINWINDOW_PLIST, "LoginwindowText"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        else:
            subprocess.run(
                ["sudo", "defaults", "write", LOGINWINDOW_PLIST,
                 "LoginwindowText", previous],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
    except OSError:
        pass

def get_lid_sleep_disabled():
    """Return current macOS 'SleepDisabled' value ('0'/'1'), or None if unknown."""
    try:
        out = subprocess.run(["pmset", "-g"], capture_output=True, text=True)
        if out.returncode == 0:
            for line in out.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 2 and parts[0] == "SleepDisabled":
                    return parts[1]
            return "0"  # not listed = default (lid sleep enabled)
    except OSError:
        pass
    return None

def set_lid_sleep_disabled(value):
    """Disable/enable lid-close sleep on macOS. Needs sudo. True on success.

    `value` is "1" (lid close won't sleep) or "0" (normal). Lets agents keep
    running with the lid shut - use only on power and a hard surface.
    """
    try:
        r = subprocess.run(["sudo", "pmset", "-a", "disablesleep", value])
        return r.returncode == 0
    except OSError:
        return False

def _macos_lock_via_framework():
    """Lock instantly via login.framework's SACLockScreenImmediate.

    Works on modern macOS with no Accessibility permission and regardless of
    energy-saver settings. Returns True on success.
    """
    import ctypes
    try:
        lib = ctypes.CDLL(
            "/System/Library/PrivateFrameworks/login.framework"
            "/Versions/Current/login"
        )
        lib.SACLockScreenImmediate()
        return True
    except (OSError, AttributeError):
        return False

def lock_screen():
    """Lock the OS screen immediately. Returns True on success."""
    system = platform.system()
    if system == "Darwin":  # macOS
        # Preferred: private framework call - real lock, no permissions needed.
        if _macos_lock_via_framework():
            return True
        # Legacy CGSession path (pre-Tahoe) - harmless if absent.
        cgsession = ("/System/Library/CoreServices/Menu Extras/User.menu"
                     "/Contents/Resources/CGSession")
        candidates = [
            [cgsession, "-suspend"],
            # Standard "Lock Screen" shortcut (Cmd+Ctrl+Q). Needs the terminal
            # to have Accessibility permission (System Settings > Privacy).
            ["osascript", "-e",
             'tell application "System Events" to keystroke "q" '
             'using {control down, command down}'],
        ]
        # NOTE: deliberately no `pmset displaysleepnow` fallback - it blanks the
        # display without locking, which looks like a lock but isn't.
    elif system == "Linux":
        candidates = [
            ["loginctl", "lock-session"],
            ["xdg-screensaver", "lock"],
            ["gnome-screensaver-command", "-l"],
            ["dm-tool", "lock"],
        ]
    else:
        return False

    for cmd in candidates:
        try:
            subprocess.run(cmd, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (OSError, subprocess.CalledProcessError):
            continue
    return False

LID_WARNING = """
\033[1;33m┌──────────────────────────────────────────────────────────────┐
│  ⚠  WARNING: --lid disables lid-close sleep                   │
│                                                              │
│  Your Mac will KEEP RUNNING AT FULL POWER with the lid shut. │
│                                                              │
│    • Keep it plugged into power.                             │
│    • Keep it on a hard, open surface for airflow.            │
│    • NEVER put it in a bag or under cover while running.     │
│                                                              │
│  A closed lid with no airflow can OVERHEAT the machine.      │
│  Normal sleep is restored automatically when you exit.       │
└──────────────────────────────────────────────────────────────┘\033[0m
"""

def _confirm_lid(assume_yes):
    """Show the lid warning and require explicit confirmation. True to proceed."""
    sys.stderr.write(LID_WARNING + "\n")
    sys.stderr.flush()
    if assume_yes:
        sys.stderr.write("Proceeding (--yes given).\n")
        return True
    if not sys.stdin.isatty():
        # No way to ask - fail safe rather than silently keeping the lid awake.
        sys.stderr.write("Refusing --lid without a terminal to confirm; "
                         "re-run with --yes to accept the risk.\n")
        return False
    try:
        answer = input("Continue with the lid feature? [y/N] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False
    return answer in ("y", "yes")

def main():
    parser = argparse.ArgumentParser(
        prog="agent-working",
        description="A minimal terminal screensaver for when AI agents are working.",
    )
    parser.add_argument(
        "--lock", action="store_true",
        help="Lock the OS screen while keeping the machine awake so agents keep "
             "running. Nobody can touch the laptop; the agent keeps working.",
    )
    parser.add_argument(
        "--lid", action="store_true",
        help="Keep working even with the lid closed (macOS: disables lid-close "
             "sleep via pmset; needs sudo, restored on exit). Use only on power "
             "and a hard surface - a closed lid with no airflow can overheat.",
    )
    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="Skip the --lid safety confirmation prompt (for non-interactive use).",
    )
    args = parser.parse_args()

    is_macos = platform.system() == "Darwin"

    # macOS: put a message on the native lock screen *before* hiding the cursor,
    # so the one-time sudo prompt appears on a clean terminal.
    prev_lock_message = None
    lock_message_set = False
    if args.lock and is_macos:
        prev_lock_message = _get_lock_message()
        lock_message_set = set_lock_message(LOCK_MESSAGE)
        if not lock_message_set:
            sys.stderr.write("agent-working: couldn't set the lock-screen "
                             "message (needs admin); locking without it.\n")

    # macOS: optionally disable lid-close sleep so agents keep running with the
    # lid shut. Captured here so the sudo prompt shares the clean terminal.
    prev_lid_disabled = None
    lid_sleep_disabled = False
    if args.lid:
        if is_macos:
            if _confirm_lid(args.yes):
                prev_lid_disabled = get_lid_sleep_disabled()
                lid_sleep_disabled = set_lid_sleep_disabled("1")
                if not lid_sleep_disabled:
                    sys.stderr.write("agent-working: couldn't disable lid sleep "
                                     "(needs admin); the Mac will sleep on lid "
                                     "close.\n")
            else:
                sys.stderr.write("agent-working: --lid cancelled; the Mac will "
                                 "sleep on lid close.\n")
        else:
            sys.stderr.write("agent-working: --lid is only supported on macOS; "
                             "ignoring.\n")

    hide_cursor()
    frame_idx = 0
    dots_frames = ["·  ", "·· ", "···", " ··", "  ·", "   "]

    # Fetch news on startup
    headlines = fetch_news()
    news_idx = 0
    start_time = time.time()
    last_news_fetch = time.time()

    # Prevent sleep (macOS + Linux). In lock mode, keep the system awake but
    # allow the display to lock.
    caffeine_proc = start_caffeine(lock_mode=args.lock)

    # Lock the screen *after* caffeinate is holding the system awake, so the
    # machine stays running behind the lock screen.
    if args.lock:
        if not lock_screen():
            sys.stderr.write("agent-working: could not lock the screen on this "
                             "platform; running unlocked.\n")

    try:
        while True:
            clear_screen()
            cols, rows = get_terminal_size()

            banner_lines = BANNER.count('\n') + 1
            total_content_lines = banner_lines + 12
            top_padding = max(0, (rows - total_content_lines) // 2)

            print('\n' * top_padding, end='')

            for line in BANNER.split('\n'):
                padding = (cols - 70) // 2
                print(' ' * max(0, padding) + f"{COLOR}{DIM}{line}{RESET}")

            print()
            print()

            # Timer
            elapsed = time.time() - start_time
            duration = format_duration(elapsed)
            timer_line = f"{COLOR}{DIM}agents working for {duration}{RESET}"
            padding = (cols - len(f"agents working for {duration}")) // 2
            print(' ' * max(0, padding) + timer_line)

            print()

            # Status
            dots = dots_frames[frame_idx % len(dots_frames)]
            status_text = "screen locked · agents working" if args.lock else "please do not touch"
            status_line = f"{COLOR}{DIM}{status_text} {dots}{RESET}"
            padding = (cols - (len(status_text) + 4)) // 2
            print(' ' * max(0, padding) + status_line)

            print()
            print()

            # News headline
            current_headline = headlines[news_idx % len(headlines)]
            max_news_width = min(cols - 10, 70)
            truncated = truncate_headline(current_headline, max_news_width)
            news_line = f"{NEWS_COLOR}{DIM}› {truncated}{RESET}"
            padding = (cols - len(truncated) - 2) // 2
            print(' ' * max(0, padding) + news_line)

            sys.stdout.flush()

            frame_idx += 1
            if frame_idx % 10 == 0:
                news_idx += 1

            # Refresh news every 30 minutes
            if time.time() - last_news_fetch > 1800:
                new_headlines = fetch_news()
                if new_headlines and new_headlines[0] != "ai news unavailable":
                    headlines = new_headlines
                    news_idx = 0
                last_news_fetch = time.time()

            time.sleep(0.8)

    except KeyboardInterrupt:
        pass
    finally:
        if caffeine_proc:
            caffeine_proc.terminate()
        if lock_message_set:
            restore_lock_message(prev_lock_message)
        if lid_sleep_disabled:
            set_lid_sleep_disabled(prev_lid_disabled or "0")
        show_cursor()
        clear_screen()

if __name__ == "__main__":
    main()
