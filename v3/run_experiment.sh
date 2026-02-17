#!/bin/bash
set -e

# Usage: ./run_experiment.sh <stp_file> <experiment_dir>
# Example: ./run_experiment.sh ../stps/1.md experiment_1

STP_FILE="$1"
EXPERIMENT_DIR="$2"
TEST_REPO="/home/mvavrine/cnv/openshift-virtualization-tests"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$STP_FILE" ] || [ -z "$EXPERIMENT_DIR" ]; then
    echo "Usage: $0 <stp_file> <experiment_dir>"
    exit 1
fi

# Resolve model directory from environment or default
MODEL_DIR="${MODEL:-opus4.6}"
OUTPUT_DIR="$SCRIPT_DIR/$MODEL_DIR/$EXPERIMENT_DIR"
mkdir -p "$OUTPUT_DIR"

# Create temporary prompt file by combining orchestrator with STP
TEMP_PROMPT=$(mktemp)

# Write orchestrator content
cat "$SCRIPT_DIR/orchestrator.md" > "$TEMP_PROMPT"

# Append STP content
echo "" >> "$TEMP_PROMPT"
echo "---" >> "$TEMP_PROMPT"
echo "" >> "$TEMP_PROMPT"
echo "## STP Input" >> "$TEMP_PROMPT"
echo "" >> "$TEMP_PROMPT"
cat "$STP_FILE" >> "$TEMP_PROMPT"

echo "Running experiment in $OUTPUT_DIR with STP from $STP_FILE"
echo "Temp prompt: $TEMP_PROMPT"

# Change to test repository
cd "$TEST_REPO"

# Get initial git state
git diff > /dev/null 2>&1 || true
INITIAL_COMMIT=$(git rev-parse HEAD)

# Run claude with the prompt via stdin
echo "Starting Claude session..."
cat "$TEMP_PROMPT" | claude chat > "$OUTPUT_DIR/claude.log" 2>&1

# Copy test_run.log if it was generated
if [ -f "test_run.log" ]; then
    cp test_run.log "$OUTPUT_DIR/test_run.log"
fi

# Generate changes.patch
echo "Generating changes.patch..."
git diff > "$OUTPUT_DIR/changes.patch"

# Copy GRAVEYARD.md if it was created/updated
if [ -f "GRAVEYARD.md" ]; then
    cp GRAVEYARD.md "$OUTPUT_DIR/GRAVEYARD.md"
fi

# Reset git state for next experiment
echo "Resetting git state..."
git restore .
git clean -fd

# Cleanup
rm -f "$TEMP_PROMPT"

echo "Experiment complete! Output in $OUTPUT_DIR/"
echo "  - claude.log: Conversation transcript"
echo "  - changes.patch: Generated code changes"
echo "  - test_run.log: Test execution output (if generated)"
echo "  - GRAVEYARD.md: Lessons learned (if generated)"
