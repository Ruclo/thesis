#!/bin/bash

# Quick progress checker for sequential STP processing
# Usage: ./check_progress.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODEL_DIR="${MODEL:-opus4.6}"
OUTPUT_BASE="$SCRIPT_DIR/$MODEL_DIR"
PROGRESS_FILE="$OUTPUT_BASE/PROGRESS.txt"

echo "========================================"
echo "V3 Sequential Experiments - Progress"
echo "========================================"
echo ""

# Check if progress file exists
if [ ! -f "$PROGRESS_FILE" ]; then
    echo "No progress file found. Has the script started yet?"
    echo "Expected: $PROGRESS_FILE"
    exit 1
fi

# Display progress file
cat "$PROGRESS_FILE"
echo ""

# Find most recent experiment
LATEST_EXP=""
for i in {7..1}; do
    if [ -d "$OUTPUT_BASE/experiment_$i" ]; then
        LATEST_EXP="$i"
        break
    fi
done

if [ -n "$LATEST_EXP" ]; then
    echo "========================================"
    echo "Latest Experiment: $LATEST_EXP"
    echo "========================================"

    EXP_DIR="$OUTPUT_BASE/experiment_$LATEST_EXP"

    # Show experiment details
    if [ -f "$EXP_DIR/claude.log" ]; then
        LOG_SIZE=$(wc -l < "$EXP_DIR/claude.log")
        echo "Claude log: $LOG_SIZE lines"
        echo ""
        echo "Last 15 lines of claude.log:"
        echo "---"
        tail -n 15 "$EXP_DIR/claude.log"
    fi

    echo ""

    # Show GRAVEYARD stats if exists
    if [ -f "$EXP_DIR/GRAVEYARD.md" ]; then
        GRAVEYARD_LINES=$(wc -l < "$EXP_DIR/GRAVEYARD.md")
        echo "GRAVEYARD.md: $GRAVEYARD_LINES lines"
    fi

    # Show changes.patch stats if exists
    if [ -f "$EXP_DIR/changes.patch" ]; then
        PATCH_LINES=$(wc -l < "$EXP_DIR/changes.patch")
        echo "changes.patch: $PATCH_LINES lines"
    fi
fi

echo ""
echo "========================================"
echo "To monitor live Claude output:"
echo "  tail -f $OUTPUT_BASE/experiment_*/claude.log"
echo "========================================"
