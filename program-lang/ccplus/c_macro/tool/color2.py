#!/usr/bin/env python3
import sys
from collections import defaultdict

# High-contrast colors for dark backgrounds (ANSI codes)
#  COLORS = [
#      '\033[38;5;213m',  # Bright pink
#      '\033[38;5;159m',  # Light cyan
#      '\033[38;5;229m',  # Pale yellow
#      '\033[38;5;123m',  # Electric blue
#      '\033[38;5;219m',  # Lavender
#      '\033[38;5;158m'   # Mint green
#  ]

COLORS = [
    '\033[38;5;196m',  # Red
    '\033[38;5;226m',  # Yellow
    '\033[38;5;46m',   # Green
    '\033[38;5;51m',   # Cyan
    '\033[38;5;21m',   # Blue
    '\033[38;5;201m'   # Magenta
]

RESET = '\033[0m'
BRACKETS = {'{': '}', '[': ']', '(': ')'}
RESET_TRIGGER = "---NEW ENTRY---"  # Customize this

def rainbow_brackets():
    stack = []
    for line in sys.stdin:
        # Reset on trigger string
        if RESET_TRIGGER in line:
            stack.clear()
            sys.stdout.write("\n" + line)  # Print trigger without coloring
            continue

        for char in line:
            if char in BRACKETS:
                color = COLORS[len(stack) % len(COLORS)]
                sys.stdout.write(color + char + RESET)
                stack.append(BRACKETS[char])
            elif stack and char == stack[-1]:
                color = COLORS[(len(stack)-1) % len(COLORS)]
                sys.stdout.write(color + char + RESET)
                stack.pop()
            else:
                sys.stdout.write(char)
        sys.stdout.flush()

if __name__ == "__main__":
    rainbow_brackets()
