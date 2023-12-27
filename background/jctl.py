import os
import subprocess
import re
import signal
import tempfile
import time


SINCE = "today"
SERIAL_NUM = ""
LOCAL_USER = os.getenv('SUDO_USER') or os.getenv('USER')
PATTERNS = r"bin/PATTERNS"
IGNORE_PATTERNS = r"bin/IGNORE_PATTERNS"


# Function to handle cleanup
def cleanup(signum, frame):
    print("Cleaning up temporary files...")
    os.remove(temp_output.name)
    os.remove(temp_journal.name)
    log_path = f"/home/{LOCAL_USER}/Desktop/journalctl{SERIAL_NUM}.log"
    if os.path.exists(log_path) and os.path.getsize(log_path) == 0:
        os.remove(log_path)
    exit(0)


# Set signal handlers
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)


# Check if the log file exists and remove it
log_file_path = f"/home/{LOCAL_USER}/Desktop/journalctl{SERIAL_NUM}.log"
if os.path.exists(log_file_path):
    os.remove(log_file_path)


# Temporary files to store new lines.
temp_output = tempfile.NamedTemporaryFile(delete=False)
temp_journal = tempfile.NamedTemporaryFile(delete=False)


# Function to handle file writing
def write_to_log_file(data):
    with open(log_file_path, "a") as log_file:
        log_file.write(data)


# Main loop
while True:
    # Run journalctl command and capture stdout
    journal_process = subprocess.Popen(["sudo", "journalctl", f"--since={SINCE}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    # Get stdout and stderr
    journal_stdout, journal_stderr = journal_process.communicate()


    # Check for errors in stderr
    if journal_stderr:
        print(f"Error running journalctl: {journal_stderr.decode()}")


    # Process stdout
    journal_content = journal_stdout.decode()


    # Find and write matching lines to temp_output
    pattern_matches = re.findall(PATTERNS, journal_content, flags=re.MULTILINE)
    ignore_pattern_matches = re.findall(IGNORE_PATTERNS, journal_content, flags=re.MULTILINE)


    with open(temp_output.name, "w") as output_file:
        output_file.writelines(line for line in pattern_matches if line not in ignore_pattern_matches)


    SINCE = time.strftime('%Y-%m-%d %H:%M:%S')


    # Process new lines
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


            # Write the block to the log file
            write_to_log_file(block)


    time.sleep(5)