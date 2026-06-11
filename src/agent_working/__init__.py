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
    args = parser.parse_args()

    # macOS: put a message on the native lock screen *before* hiding the cursor,
    # so the one-time sudo prompt appears on a clean terminal.
    prev_lock_message = None
    lock_message_set = False
    if args.lock and platform.system() == "Darwin":
        prev_lock_message = _get_lock_message()
        lock_message_set = set_lock_message(LOCK_MESSAGE)
        if not lock_message_set:
            sys.stderr.write("agent-working: couldn't set the lock-screen "
                             "message (needs admin); locking without it.\n")

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
        show_cursor()
        clear_screen()

if __name__ == "__main__":
    main()
