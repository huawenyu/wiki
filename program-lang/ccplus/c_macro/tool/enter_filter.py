#!/usr/bin/env python3
import sys
import select

def filter_input():
    while True:
        # Wait until stdin has data
        r, _, _ = select.select([sys.stdin], [], [])
        if sys.stdin in r:
            line = sys.stdin.readline()
            if not line:
                break

            if line == '\n':
                sys.stdout.write("SPECIAL_HANDLING_FOR_ENTER\n")
            else:
                sys.stdout.write(line)
            sys.stdout.flush()

if __name__ == "__main__":
    filter_input()
