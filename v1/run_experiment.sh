#!/bin/bash
set -e

# Usage: ./run_experiment.sh <stp_file> <experiment_dir>
# Example: ./run_experiment.sh ../stps/1.md experiment_1

STP_FILE="$1"
EXPERIMENT_DIR="$2"
TEST_REPO="/home/mvavrine/cnv/openshift-virtualization-tests"

if [ -z "$STP_FILE" ] || [ -z "$EXPERIMENT_DIR" ]; then
    echo "Usage: $0 <stp_file> <experiment_dir>"
    exit 1
fi

# Create temporary prompt file by combining template with STP
TEMP_PROMPT=$(mktemp)

# Read prompt template up to the placeholder and write to temp file
sed '/\${STP_CONTENT}/q' prompt.md | sed '/\${STP_CONTENT}/d' > "$TEMP_PROMPT"

# Append STP content
cat "$STP_FILE" >> "$TEMP_PROMPT"

echo "Running experiment in $EXPERIMENT_DIR with STP from $STP_FILE"
echo "Temp prompt: $TEMP_PROMPT"

# Change to test repository
cd "$TEST_REPO"

# Get initial git state
git diff > /dev/null 2>&1 || true
INITIAL_COMMIT=$(git rev-parse HEAD)

# Run claude with the prompt via stdin
echo "Starting Claude session..."
cat "$TEMP_PROMPT" | claude chat > "../thesis/v1/$EXPERIMENT_DIR/claude.log" 2>&1

# Generate changes.patch
echo "Generating changes.patch..."
git diff > "../thesis/v1/$EXPERIMENT_DIR/changes.patch"

# Reset git state for next experiment
echo "Resetting git state..."
git restore .
git clean -fd

# Cleanup
rm -f "$TEMP_PROMPT"

echo "Experiment complete! Output in v1/$EXPERIMENT_DIR/"
echo "  - claude.log: Conversation transcript"
echo "  - changes.patch: Generated code changes"
