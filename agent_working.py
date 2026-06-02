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
import subprocess
import signal

# Single dim color - soft blue/gray
RESET = "\033[0m"
DIM = "\033[2m"
COLOR = "\033[38;5;88m"  # Dark red

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

def main():
    hide_cursor()
    frame_idx = 0
    dots_frames = ["·  ", "·· ", "···", " ··", "  ·", "   "]

    # Start caffeinate to prevent sleep
    caffeinate_proc = subprocess.Popen(
        ["caffeinate", "-d"],  # -d prevents display sleep
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        while True:
            clear_screen()
            cols, rows = get_terminal_size()

            # Calculate vertical centering
            banner_lines = BANNER.count('\n') + 1
            total_content_lines = banner_lines + 8
            top_padding = max(0, (rows - total_content_lines) // 2)

            # Print top padding
            print('\n' * top_padding, end='')

            # Print banner
            for line in BANNER.split('\n'):
                padding = (cols - 70) // 2
                print(' ' * max(0, padding) + f"{COLOR}{DIM}{line}{RESET}")

            print()
            print()

            # Simple status
            dots = dots_frames[frame_idx % len(dots_frames)]
            status_line = f"{COLOR}{DIM}agents working {dots}{RESET}"
            padding = (cols - 18) // 2
            print(' ' * max(0, padding) + status_line)

            print()

            # Warning
            warning = f"{COLOR}{DIM}please do not touch{RESET}"
            padding = (cols - 19) // 2
            print(' ' * max(0, padding) + warning)

            sys.stdout.flush()

            frame_idx += 1
            time.sleep(0.8)  # Slow, calm animation

    except KeyboardInterrupt:
        pass
    finally:
        caffeinate_proc.terminate()
        show_cursor()
        clear_screen()

if __name__ == "__main__":
    main()
