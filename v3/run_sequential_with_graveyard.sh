#!/bin/bash
set -e

# Sequential STP processor with cumulative GRAVEYARD.md
#
# USAGE:
#   cd /home/mvavrine/cnv/thesis/v3
#   ./run_sequential_with_graveyard.sh
#
# This script MUST be run from the v3 directory where it's located.
# Claude will be invoked from within the openshift-virtualization-tests repo.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEST_REPO="$SCRIPT_DIR/../openshift-virtualization-tests"
MODEL_DIR="${MODEL:-opus4.6}"
OUTPUT_BASE="$SCRIPT_DIR/$MODEL_DIR"

# Create base output directory
mkdir -p "$OUTPUT_BASE"

# Temporary GRAVEYARD.md storage (accumulates across runs)
GRAVEYARD_ACCUMULATOR="$OUTPUT_BASE/GRAVEYARD_accumulator.md"

# Progress tracking file
PROGRESS_FILE="$OUTPUT_BASE/PROGRESS.txt"
START_TIME=$(date +%s)

# Start fresh - no GRAVEYARD.md initially
rm -f "$GRAVEYARD_ACCUMULATOR"

# Initialize progress file
cat > "$PROGRESS_FILE" <<EOF
Sequential STP Processing Progress
===================================
Started: $(date)
Model: $MODEL_DIR
Total STPs: 7

Status:
EOF

echo "========================================"
echo "Sequential STP Processing with Cumulative GRAVEYARD.md"
echo "========================================"
echo "Working Directory: $(pwd)"
echo "Script Directory: $SCRIPT_DIR"
echo "Model: $MODEL_DIR"
echo "Test Repository: $TEST_REPO"
echo "Output Base: $OUTPUT_BASE"
echo ""

# Verify we're in the correct directory
if [ "$(pwd)" != "$SCRIPT_DIR" ]; then
    echo "ERROR: Script must be run from $SCRIPT_DIR"
    echo "Current directory: $(pwd)"
    echo ""
    echo "Please run:"
    echo "  cd $SCRIPT_DIR"
    echo "  ./run_sequential_with_graveyard.sh"
    exit 1
fi

# Verify test repository exists
if [ ! -d "$TEST_REPO" ]; then
    echo "ERROR: Test repository not found at $TEST_REPO"
    exit 1
fi

# Process STPs 1-7
for i in {1..7}; do
    STP_FILE="$SCRIPT_DIR/../stps/${i}.md"
    EXPERIMENT_DIR="experiment_${i}"
    OUTPUT_DIR="$OUTPUT_BASE/$EXPERIMENT_DIR"

    echo ""
    echo "========================================"
    echo "EXPERIMENT $i: Processing stps/${i}.md"
    echo "========================================"
    echo "Output: $OUTPUT_DIR"

    # Update progress file
    echo "Experiment $i: IN PROGRESS (started $(date))" >> "$PROGRESS_FILE"

    # Check if STP file exists
    if [ ! -f "$STP_FILE" ]; then
        echo "ERROR: STP file not found: $STP_FILE"
        exit 1
    fi

    # Create experiment output directory
    mkdir -p "$OUTPUT_DIR"

    # Change to test repository
    cd "$TEST_REPO"
    echo "Changed to test repo: $(pwd)"

    # Restore GRAVEYARD.md from previous iteration (if exists)
    if [ -f "$GRAVEYARD_ACCUMULATOR" ]; then
        echo "Restoring GRAVEYARD.md from previous iteration..."
        cp "$GRAVEYARD_ACCUMULATOR" GRAVEYARD.md
        echo "  $(wc -l < "$GRAVEYARD_ACCUMULATOR") lines restored"
    else
        echo "Starting fresh (no GRAVEYARD.md yet)"
        rm -f GRAVEYARD.md
    fi

    # Record initial commit BEFORE running Claude
    INITIAL_COMMIT=$(git rev-parse HEAD)
    echo "Initial commit: $INITIAL_COMMIT"

    # Run claude with /v3-orchestrator command from within the test repo
    echo "Starting Claude session with /v3-orchestrator..."
    echo "/v3-orchestrator $STP_FILE" | claude chat --dangerously-skip-permissions > "$OUTPUT_DIR/claude.log" 2>&1

    CLAUDE_EXIT_CODE=$?
    echo "Claude session completed (exit code: $CLAUDE_EXIT_CODE)"

    # Save artifacts
    echo "Saving artifacts..."

    # Copy test_run.log if generated
    if [ -f "test_run.log" ]; then
        cp test_run.log "$OUTPUT_DIR/test_run.log"
        echo "  ✓ test_run.log saved"
    fi

    # Generate changes.patch from initial commit (captures all changes, committed or not)
    git diff "$INITIAL_COMMIT" > "$OUTPUT_DIR/changes.patch"
    echo "  ✓ changes.patch saved (from commit $INITIAL_COMMIT)"

    # Save GRAVEYARD.md for next iteration (do this BEFORE cleanup)
    if [ -f "GRAVEYARD.md" ]; then
        cp GRAVEYARD.md "$OUTPUT_DIR/GRAVEYARD.md"
        cp GRAVEYARD.md "$GRAVEYARD_ACCUMULATOR"
        echo "  ✓ GRAVEYARD.md saved ($(wc -l < GRAVEYARD.md) lines)"
    else
        echo "  ⚠ No GRAVEYARD.md generated"
    fi

    # Reset to initial commit (removes all changes and commits)
    echo "Resetting to initial state..."
    git reset --hard "$INITIAL_COMMIT"
    git clean -fd

    # Update progress file with completion
    sed -i "s/Experiment $i: IN PROGRESS.*/Experiment $i: COMPLETED (finished $(date))/" "$PROGRESS_FILE"

    echo "Experiment $i complete!"
    echo "  Output: $OUTPUT_DIR/"
    echo "  - claude.log: Conversation transcript"
    echo "  - changes.patch: Generated code changes"
    echo "  - test_run.log: Test execution output (if generated)"
    echo "  - GRAVEYARD.md: Lessons learned (if generated)"

    # Return to script directory for next iteration
    cd "$SCRIPT_DIR"
done

echo ""
echo "========================================"
echo "All Experiments Complete!"
echo "========================================"
echo "Results in: $OUTPUT_BASE/experiment_1 through $OUTPUT_BASE/experiment_7"
echo ""

# Calculate total time
END_TIME=$(date +%s)
TOTAL_SECONDS=$((END_TIME - START_TIME))
HOURS=$((TOTAL_SECONDS / 3600))
MINUTES=$(((TOTAL_SECONDS % 3600) / 60))

# Show final GRAVEYARD.md stats
if [ -f "$GRAVEYARD_ACCUMULATOR" ]; then
    echo "Final GRAVEYARD.md: $(wc -l < "$GRAVEYARD_ACCUMULATOR") lines"
    echo "Location: $GRAVEYARD_ACCUMULATOR"
else
    echo "No GRAVEYARD.md was generated during any experiment"
fi

# Finalize progress file
cat >> "$PROGRESS_FILE" <<EOF

===================================
Completed: $(date)
Total Time: ${HOURS}h ${MINUTES}m
Final GRAVEYARD.md: $(wc -l < "$GRAVEYARD_ACCUMULATOR" 2>/dev/null || echo "0") lines
===================================
EOF

echo ""
echo "Progress tracked in: $PROGRESS_FILE"
