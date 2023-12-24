#!/bin/bash


##todo:
#make sure paths are either absolute or fluid.
#this can probably be absolute.


SINCE="today"
SERIAL_NUM=""

cleanup() {
    echo "Cleaning up temporary files..."
    rm -f "$temp_output"
    rm -f "$temp_journal"
    if [ ! -s "/home/${LOCAL_USER}/Desktop/journalctl${SERIAL_NUM}.log" ]; then
        rm -f "/home/${LOCAL_USER}/Desktop/journalctl${SERIAL_NUM}.log"
    fi
    exit 0
}

trap cleanup INT TERM EXIT

if [ -f "/home/${LOCAL_USER}/Desktop/journalctl${SERIAL_NUM}.log" ]; then
    rm -f "/home/${LOCAL_USER}/Desktop/journalctl${SERIAL_NUM}.log"
fi

# Temporary file to store new lines.
temp_output=$(mktemp)
temp_journal=$(mktemp)

while true; do
    # Fetch the entire journal since the given timestamp.
    sudo journalctl --since="$SINCE" > "$temp_journal"

    grep -Ef PATTERNS "$temp_journal" | grep -vEf IGNORE_PATTERNS > "$temp_output"

    # Update SINCE to now, so the next iteration will pick up logs from this moment onward.
    SINCE=$(date +'%Y-%m-%d %H:%M:%S')

    # Process the new lines.
    while IFS= read -r line; do
        timestamp=$(echo "$line" | awk '{print $1, $2, $3}')

        if [[ $line == *"[ cut here ]"* ]]; then
            block=$(awk "/${timestamp}.*\[ cut here \]/,/${timestamp}.*\[ end trace/" "$temp_journal")
            if [[ -n $block ]]; then
                echo "$block" >> "/home/${LOCAL_USER}/Desktop/journalctl${SERIAL_NUM}.log"
            else
                echo "$line" >> "/home/${LOCAL_USER}/Desktop/journalctl${SERIAL_NUM}.log"
            fi
        elif [[ $line == *"invoked oom-killer"* ]]; then
            if pgrep -x "memtester" &>/dev/null
            then
                continue
            fi
            block=$(awk "/${timestamp}.*invoked oom-killer/,/${timestamp}.*Out of memory/" "$temp_journal")
            if [[ -n $block ]]; then
                echo "$block" >> "/home/${LOCAL_USER}/Desktop/journalctl${SERIAL_NUM}.log"
            else
                echo "$line" >> "/home/${LOCAL_USER}/Desktop/journalctl${SERIAL_NUM}.log"
            fi
        else
            echo "$line" >> "/home/${LOCAL_USER}/Desktop/journalctl${SERIAL_NUM}.log"
        fi
    done < "$temp_output"
    sleep 5
done