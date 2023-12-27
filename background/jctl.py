import os
import subprocess
import re
import signal
import tempfile
import time

SINCE = "today"
SERIAL_NUM = ""
LOCAL_USER = "your_local_user"  # Replace with the actual local user
PATTERNS = r"your_patterns_regex"  # Replace with the actual patterns regex
IGNORE_PATTERNS = r"your_ignore_patterns_regex"  # Replace with the actual ignore patterns regex


def watch_journalctl():
    process = subprocess.Popen(['sudo', 'journalctl', '-f'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        while True:
            line = process.stdout.readline()
            if not line:
                break
            process_log_line(line)
    except KeyboardInterrupt:
        pass
    finally:
        process.terminate()

def process_log_line(line):
    print(line, end='')

if __name__ == "__main__":
    watch_journalctl()