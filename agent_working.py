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

def main():
    hide_cursor()
    frame_idx = 0
    dots_frames = ["·  ", "·· ", "···", " ··", "  ·", "   "]

    # Fetch news on startup
    headlines = fetch_news()
    news_idx = 0
    start_time = time.time()

    # Start caffeinate to prevent sleep
    caffeinate_proc = subprocess.Popen(
        ["caffeinate", "-d"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

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
            status_line = f"{COLOR}{DIM}please do not touch {dots}{RESET}"
            padding = (cols - 23) // 2
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

            time.sleep(0.8)

    except KeyboardInterrupt:
        pass
    finally:
        caffeinate_proc.terminate()
        show_cursor()
        clear_screen()

if __name__ == "__main__":
    main()
