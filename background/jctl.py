import os
import subprocess
import re
import signal
import tempfile
import time
import sys

#make a way to input the s/n in the app.py and import or something into the "SERIAL_NUM" here and in other python scripts
SINCE = "today"
SERIAL_NUM = ""
LOCAL_USER = os.getenv('SUDO_USER') or os.getenv('USER')
PATTERNS = r"../bin/PATTERNS"
IGNORE_PATTERNS = r"../bin/IGNORE_PATTERNS"

def cleanup(signum, frame):
    print(" Cleaning up temporary files...")
    temp_output.close()
    temp_journal.close()
    os.remove(temp_output.name)
    os.remove(temp_journal.name)
    log_path = f"/home/{LOCAL_USER}/Desktop/journalctl{SERIAL_NUM}.log"
    if os.path.exists(log_path) and os.path.getsize(log_path) == 0:
        os.remove(log_path)
    exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

log_file_path = f"/home/{LOCAL_USER}/Desktop/journalctl{SERIAL_NUM}.log"
if os.path.exists(log_file_path):
    os.remove(log_file_path)

temp_output = tempfile.NamedTemporaryFile(delete=False)
temp_journal = tempfile.NamedTemporaryFile(delete=False)

def write_to_log_file(data):
    with open(log_file_path, "a") as log_file:
        log_file.write(data)


while True:
    journal_process = subprocess.Popen(["sudo", "journalctl", f"--since={SINCE}"], stdout=open(temp_journal), stderr=subprocess.PIPE)
    
    if journal_stderr:
        print(f"Error running journalctl: {journal_stderr.decode()}")

    journal_content = journal_stdout.decode()

    pattern_matches = re.findall(PATTERNS, journal_content, flags=re.MULTILINE)
    ignore_pattern_matches = re.findall(IGNORE_PATTERNS, journal_content, flags=re.MULTILINE)


    with open(temp_output.name, "w") as output_file:
        output_file.writelines(line for line in pattern_matches if line not in ignore_pattern_matches)


    SINCE = time.strftime('%Y-%m-%d %H:%M:%S')

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

            write_to_log_file(block)


    time.sleep(5)