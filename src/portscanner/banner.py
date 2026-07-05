# src/portscanner/banner.py - Made by Alex M.

import sys
import time

LOGO = r"""
             _         ____
           /' \       /\  _`\
  ___ ___ /\_, \  _ __\ \ \L\ \
/' __` __`\/_/\ \/\`'__\ \ ,  /
/\ \/\ \/\ \ \ \ \ \ \/ \ \ \\ \   __
\ \_\ \_\ \_\ \ \_\ \_\  \ \_\ \_\/\_\
 \/_/\/_/\/_/  \/_/\/_/   \/_/\/ /\/_/
"""


def print_logo(delay: float = 0.01) -> None:
    """Print the logo character-by-character for a typewriter effect."""
    for char in LOGO:
        sys.stdout.write(char)
        sys.stdout.flush()
        if delay:
            time.sleep(delay)