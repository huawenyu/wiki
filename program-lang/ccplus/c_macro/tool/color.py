#!/usr/bin/env python3
import sys
from collections import defaultdict

COLORS = ['\033[31m', '\033[33m', '\033[32m', '\033[36m', '\033[34m']
RESET = '\033[0m'
BRACKETS = {'{': '}', '[': ']', '(': ')'}

def rainbow_brackets():
    stack = []
    for line in sys.stdin:
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

if __name__ == "__main__":
    rainbow_brackets()
