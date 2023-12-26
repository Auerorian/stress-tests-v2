import subprocess
from 

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
