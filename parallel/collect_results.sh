#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

usage() {
    cat <<EOF
Usage: $0 <version> <timestamp>

Collect and analyze results from parallel experiment runs.

Arguments:
  version    - Version that was run (v1, v2.1, v2.2, v2)
  timestamp  - Timestamp of the run (format: YYYYMMDD_HHMMSS)

Example:
  $0 v2.1 20260209_143022

This will create a summary report of all experiments from that run.
EOF
    exit 1
}

if [ $# -ne 2 ]; then
    usage
fi

VERSION=$1
TIMESTAMP=$2
PARALLEL_DIR="$(cd "$(dirname "$0")" && pwd)"
RESULTS_DIR="$PARALLEL_DIR/results_${VERSION}_${TIMESTAMP}"

mkdir -p "$RESULTS_DIR"

print_header "Collecting Results: $VERSION @ $TIMESTAMP"

# Find all experiment directories for this run
experiment_dirs=()
for i in {1..7}; do
    exp_dir="$PARALLEL_DIR/${i}-openshift-virtualization-tests/${VERSION}_experiment_${TIMESTAMP}"
    if [ -d "$exp_dir" ]; then
        experiment_dirs+=("$exp_dir")
    fi
done

if [ ${#experiment_dirs[@]} -eq 0 ]; then
    echo -e "${RED}No experiment directories found for $VERSION @ $TIMESTAMP${NC}"
    exit 1
fi

echo "Found ${#experiment_dirs[@]} experiment directories"
echo ""

# Create summary report
SUMMARY_FILE="$RESULTS_DIR/summary.md"

cat > "$SUMMARY_FILE" <<EOF
# Experiment Results Summary

**Version:** $VERSION
**Timestamp:** $TIMESTAMP
**Date:** $(date)

## Overview

| STP | Status | Test File | Errors |
|-----|--------|-----------|--------|
EOF

# Collect results from each experiment
for i in "${!experiment_dirs[@]}"; do
    stp_num=$((i + 1))
    exp_dir="${experiment_dirs[$i]}"

    echo "Processing STP $stp_num: $exp_dir"

    # Copy entire experiment directory to results
    cp -r "$exp_dir" "$RESULTS_DIR/stp_${stp_num}/"

    # Extract status
    status="❌ Unknown"
    if [ -f "$exp_dir/status.txt" ]; then
        if grep -q "Completed successfully" "$exp_dir/status.txt"; then
            status="✅ Success"
        else
            status="❌ Failed"
        fi
    fi

    # Find generated test file
    test_file="N/A"
    if [ -d "$exp_dir" ]; then
        found_test=$(find "$exp_dir" -name "test_*.py" -type f 2>/dev/null | head -1)
        if [ -n "$found_test" ]; then
            test_file=$(basename "$found_test")
        fi
    fi

    # Check for pyright errors in log
    errors="0"
    if [ -f "$exp_dir/claude.log" ]; then
        error_count=$(grep -c "error:" "$exp_dir/claude.log" 2>/dev/null || echo "0")
        errors="$error_count"
    fi

    # Add to summary table
    echo "| $stp_num | $status | \`$test_file\` | $errors |" >> "$SUMMARY_FILE"
done

# Add experiment details section
cat >> "$SUMMARY_FILE" <<EOF

## Experiment Details

EOF

for i in "${!experiment_dirs[@]}"; do
    stp_num=$((i + 1))
    exp_dir="${experiment_dirs[$i]}"

    cat >> "$SUMMARY_FILE" <<EOF
### STP $stp_num

**Experiment Directory:** \`$exp_dir\`

**Files Generated:**
\`\`\`
$(ls -lh "$exp_dir" 2>/dev/null | tail -n +2 || echo "No files found")
\`\`\`

**Status:**
\`\`\`
$(cat "$exp_dir/status.txt" 2>/dev/null || echo "No status file")
\`\`\`

**Log Summary (last 50 lines):**
\`\`\`
$(tail -50 "$exp_dir/claude.log" 2>/dev/null || echo "No log file")
\`\`\`

---

EOF
done

echo ""
print_header "Results Collection Complete"
echo ""
echo "Summary report: $SUMMARY_FILE"
echo "All results copied to: $RESULTS_DIR/"
echo ""
echo "View summary:"
echo "  cat $SUMMARY_FILE"
echo ""
