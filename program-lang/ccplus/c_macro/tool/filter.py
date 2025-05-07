#!/usr/bin/env python3

"""A demo filter dat does the same as rlwrap's --remember option
   with a few extra bells and whistles

   Save this script as 'remember.py' sowewhere in RLWRAP_FILTERDIR and invoke as follows:
   rlwrap -z remember.py sml
   N.B. Don't use the --remember option in this case!
"""

import os
import re
import sys
import atexit
import tempfile
import subprocess

# Initialize at module level
my_index = 0
log_file = open('out.log', 'a+')
log_file.write(f"\n\n# {my_index} ---NEW ENTRY---\n\n")
log_file.flush()
# Register cleanup
atexit.register(lambda: log_file.close())

if 'RLWRAP_FILTERDIR' in os.environ:
    sys.path.append(os.environ['RLWRAP_FILTERDIR'])
else:
    sys.path.append('.')

import rlwrapfilter

# List of command
Commands = ["quit", "step", "continue", "run", "backtrace", "bt", "forwardtrace", "ft", "break", "delete"]

filter = rlwrapfilter.RlwrapFilter()
filter.help_text = """\
Usage: rlwrap [-options] -z ./filter.py <command>

Source:
    https://github.com/notfoundry/ppstep
    /nix/store/238vrcj4b0fcp0yivxcp7mzl1m9jrmkk-rlwrap-0.46.1/share/rlwrap/filters/rlwrapfilter.py
Pre-requirement:
---
    clang-format: nix-env -iA nixpkgs.clang-tools

pp-shell:
---
prompt: pp>
commands:
    q-quit
    s-step
    c-continue, r-run

    bt-backtrace
    ft-forwardtrace
    b-break, For example:
        break call <macro>
        break expand <macro>
    d-delete: delete call <macro>

process-status:
    called   -  Scanned a expandable macro-call
    expanded -  Start macro expand
    rescanned-  Back to the current frame's cursor, and start scan again
    lexed    -  Token

color explained:
    white   -   Found expandable token macro-call, but still require check it's argument firstly,
    yellow  -   expaned result, but still keep cursor unmoved for rescan:
                  1. expanded done, result as!
                  2. then back to the cursor at beginning of the white region
                  3. and rescan again
    blue    -   move cursor: totally done this token, and put cursor to next token, please note it's not 'blue-paint'
"""


def format_with_ignore_errors(code):
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.c', delete=False) as f:
        f.write(code)
        f.flush()
        temp_name = f.name

    try:
        result = subprocess.run(
            ['clang-format', '-i', temp_name],
            stderr=subprocess.PIPE,
            check=False
        )

        with open(temp_name, 'r') as f:
            formatted = f.read()

        return formatted
    finally:
        os.unlink(temp_name)


def format_with_clang(text, config_file):
    """Format text using clang-format and ignore all errors"""
    try:
        result = subprocess.run(
            ['clang-format', f'-style=file:{config_file}'],
            input=text.encode(),
            text=True,
            capture_output=True,
            check=False  #  Don't raise exception on error
        )

        #  return result.stdout if result.returncode == 0 else text
        log_file.write(f"format succ\n")
        log_file.write(f"{result.stdout}\n")
        return result.stdout.decode()
    except Exception:
        log_file.write(f"format fail\n")
        return text


def remove_color_codes(text):
    # Remove all ANSI color codes (including 8-bit and 24-bit colors)
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def feed_into_completion_list(message):
    for word in message.split():
        filter.add_to_completion_list(word)

# Input handler: use everything
def handle_input(message):
    global Commands

    #feed_into_completion_list(message)
    #  msg = repr(message)
    #  print(f"Input:{msg}")
    matches = [cmd for cmd in Commands if cmd.startswith(message.lower())]

    if message == '':
        return "step"
    elif message.strip() in ('?', 'help'):
        log_file.write(f"\n# {my_index} ---NEW ENTRY---\n")
        log_file.write(filter.help_text)
        return ""   # Return empty line to skip processing
    elif matches == 'run':
        return "continue"
    elif len(matches) > 0:
        return matches[0]
    return message

filter.input_handler = handle_input


# Output handler: use every output line not containing "Standard ML ..."
def handle_output(message):
    global my_index

    #  if "Standard ML of New Jersey" not in message:
    #      feed_into_completion_list(message)

    pattern = r'\[([^:]+):(\d+):(\d+)]: (.*)'
    plain_text = remove_color_codes(message)
    match = re.match(pattern, plain_text, re.DOTALL)

    if match:
        filename, line, column, macro = match.groups()
        #  print(f"File: {filename}")
        #  print(f"Line: {line}")
        #  print(f"Column: {column}")
        #  print(f"Message: {message}")
        #  formatted = format_with_clang(macro, './clangformat.conf')
        formatted = format_with_ignore_errors(macro)
        #  log_file.write("[{f}:{l}:{c}  {n}]  {m}".format(f=filename, l=line, c=column, n=name, m=formatted))
        log_file.write(f"\n# {my_index} ---NEW ENTRY---\n")
        my_index += 1
        log_file.write(f"{formatted}\n\n")
        log_file.flush()

    return message

filter.output_handler = handle_output

for cmd in Commands:
    filter.add_to_completion_list(cmd)

# Start filter event loop:
filter.run()

