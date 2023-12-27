
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

def cleanup():
    print("Cleaning up temporary files...")
    os.remove(temp_output.name)
    os.remove(temp_journal.name)
    log_path = f"/home/{LOCAL_USER}/Desktop/journalctl{SERIAL_NUM}.log"
    if os.path.exists(log_path) and os.path.getsize(log_path) == 0:
        os.remove(log_path)
    exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGTERM, cleanup)

if os.path.exists(f"/home/{LOCAL_USER}/Desktop/journalctl{SERIAL_NUM}.log"):
    os.remove(f"/home/{LOCAL_USER}/Desktop/journalctl{SERIAL_NUM}.log")

# Temporary files to store new lines.
temp_output = tempfile.NamedTemporaryFile(delete=False)
temp_journal = tempfile.NamedTemporaryFile(delete=False)

while True:
    # Fetch the entire journal since the given timestamp.
    subprocess.run(["sudo", "journalctl", f"--since={SINCE}"], stdout=temp_journal)

    with open(temp_journal.name, "r") as journal_file:
        journal_content = journal_file.read()

    pattern_matches = re.findall(PATTERNS, journal_content, flags=re.MULTILINE)
    ignore_pattern_matches = re.findall(IGNORE_PATTERNS, journal_content, flags=re.MULTILINE)

    with open(temp_output.name, "w") as output_file:
        output_file.writelines(line for line in pattern_matches if line not in ignore_pattern_matches)

    # Update SINCE to now, so the next iteration will pick up logs from this moment onward.
    SINCE = time.strftime('%Y-%m-%d %H:%M:%S')

    # Process the new lines.
    with open(temp_output.name, "r") as output_file:
        for line in output_file:
            timestamp = line.split()[0] + " " + line.split()[1] + " " + line.split()[2]

            if "[ cut here ]" in line:
                block_start = f"{timestamp}.*[ cut here ]"
                block_end = f"{timestamp}.*[ end trace ]"
                block_match = re.search(f"{block_start}.*{block_end}", journal_content, flags=re.DOTALL)
                block = block_match.group() if block_match else line
            elif "invoked oom-killer" in line:
                if any("memtester" in process for process in subprocess.run(["pgrep", "-x", "memtester"], capture_output=True, text=True).stdout.splitlines()):
                    continue
                block_start = f"{timestamp}.*invoked oom-killer"
                block_end = f"{timestamp}.*Out of memory"
                block_match = re.search(f"{block_start}.*{block_end}", journal_content, flags=re.DOTALL)
                block = block_match.group() if block_match else line
            else:
                block = line

            with open(f"/home/{LOCAL_USER}/Desktop/journalctl{SERIAL_NUM}.log", "a") as log_file:
                log_file.write(block)

    time.sleep(5)
