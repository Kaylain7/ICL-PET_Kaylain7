#!/usr/bin/env bash

# archive_expenses.sh
# Usage:
#   ./archive_expenses.sh archive expenses_YYYY-MM-DD.txt
#   ./archive_expenses.sh search YYYY-MM-DD

ARCHIVE_DIR="archives"
LOG_FILE="archive_log.txt"

# Ensure archive directory exists
mkdir -p "$ARCHIVE_DIR"

cmd="$1"
arg="$2"

timestamp() {
    date +"%Y-%m-%d %H:%M:%S"
}

if [[ "$cmd" == "archive" && -n "$arg" ]]; then
    if [[ ! -f "$arg" ]]; then
        echo "File '$arg' not found."
        exit 1
    fi
    mv "$arg" "$ARCHIVE_DIR/"
    echo "$(timestamp) ARCHIVED $arg -> $ARCHIVE_DIR/" >> "$LOG_FILE"
    echo "Archived $arg to $ARCHIVE_DIR/ and logged to $LOG_FILE"
    exit 0

elif [[ "$cmd" == "search" && -n "$arg" ]]; then
    pattern="expenses_${arg}.txt"
    if [[ -f "$ARCHIVE_DIR/$pattern" ]]; then
        echo "--- Contents of $ARCHIVE_DIR/$pattern ---"
        cat "$ARCHIVE_DIR/$pattern"
        exit 0
    else
        echo "No archived file found for date $arg"
        exit 1
    fi

else
    echo "Usage: $0 archive <expense_file> | search <YYYY-MM-DD>"
    exit 1
fi

