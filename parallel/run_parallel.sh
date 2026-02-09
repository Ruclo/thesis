#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

usage() {
    cat <<EOF
Usage: $0 <version>

Run test generation experiments in parallel across all STPs.

Versions:
  v1      - Monolithic prompt (3 phases inline)
  v2.1    - Modular skills (exploration verbal, no STD, no caching)
  v2.2    - Modular skills (+ STD generation, exploration verbal, no caching)
  v2      - Full modular (+ STD generation, context.json caching)

Example:
  $0 v1       # Run v1 on all 7 STPs in parallel
  $0 v2.1     # Run v2.1 on all 7 STPs in parallel
  $0 v2.2     # Run v2.2 on all 7 STPs in parallel
  $0 v2       # Run v2 on all 7 STPs in parallel

Output:
  Each run creates a directory: <clone>/<version>_experiment_<timestamp>/
  Logs are written to: <clone>/<version>_experiment_<timestamp>/claude.log
EOF
    exit 1
}

if [ $# -ne 1 ]; then
    usage
fi

VERSION=$1
THESIS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PARALLEL_DIR="$THESIS_DIR/parallel"
STPS_DIR="$THESIS_DIR/stps"

# Validate version
case $VERSION in
    v1|v2.1|v2.2|v2)
        ;;
    *)
        print_error "Invalid version: $VERSION"
        usage
        ;;
esac

# Check if claude is available
if ! command -v claude &> /dev/null; then
    print_error "claude command not found. Please install Claude Code CLI."
    exit 1
fi

# Count STPs
STP_COUNT=$(find "$STPS_DIR" -name "*.md" -type f | wc -l)

print_header "Running $VERSION Experiments in Parallel"
echo ""
print_info "Version: $VERSION"
print_info "Number of STPs: $STP_COUNT"
print_info "Parallel execution with --dangerously-skip-permissions"
echo ""

# Create timestamp for this run
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Array to hold background job PIDs
declare -a PIDS

# Function to run experiment in a clone
run_experiment() {
    local stp_num=$1
    local clone_dir="$PARALLEL_DIR/${stp_num}-openshift-virtualization-tests"
    local stp_file="$STPS_DIR/${stp_num}.md"
    local experiment_dir="${VERSION}_experiment_${TIMESTAMP}"
    local output_dir="$clone_dir/$experiment_dir"

    mkdir -p "$output_dir"

    # Determine the prompt based on version
    local prompt=""
    case $VERSION in
        v1)
            # For v1, use the unified prompt with STP content
            prompt="$(cat "$THESIS_DIR/v1/prompt.md") STP File: $stp_file"
            ;;
        v2.1)
            # For v2.1, invoke the orchestrator
            prompt="/v2.1-orchestrator STP file path: $stp_file"
            ;;
        v2.2)
            # For v2.2, invoke the orchestrator
            prompt="/v2.2-orchestrator STP file path: $stp_file"
            ;;
        v2)
            # For v2, invoke the orchestrator
            prompt="/v2-orchestrator STP file path: $stp_file"
            ;;
    esac

    # Run claude in the background
    (
        cd "$clone_dir"
        echo -e "$prompt" | claude --dangerously-skip-permissions > "$output_dir/claude.log" 2>&1
        exit_code=$?

        if [ $exit_code -eq 0 ]; then
            echo "[STP $stp_num] ✓ Completed successfully" >> "$output_dir/status.txt"
        else
            echo "[STP $stp_num] ✗ Failed with exit code $exit_code" >> "$output_dir/status.txt"
        fi
    ) &

    PIDS+=($!)
    print_info "[STP $stp_num] Started (PID: ${PIDS[-1]}) → $output_dir"
}

# Launch all experiments in parallel
print_info "Launching $STP_COUNT parallel experiments..."
echo ""

for i in $(seq 1 $STP_COUNT); do
    run_experiment $i
    sleep 0.5  # Small delay to avoid overwhelming the system
done

echo ""
print_info "All experiments launched. Waiting for completion..."
echo ""

# Wait for all background jobs to complete
for i in "${!PIDS[@]}"; do
    pid=${PIDS[$i]}
    stp_num=$((i + 1))

    wait $pid
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        print_success "[STP $stp_num] Experiment completed (PID: $pid)"
    else
        print_error "[STP $stp_num] Experiment failed (PID: $pid, exit code: $exit_code)"
    fi
done

echo ""
print_header "All Experiments Completed"
echo ""
print_info "Results location: $PARALLEL_DIR/*-openshift-virtualization-tests/${VERSION}_experiment_${TIMESTAMP}/"
echo ""
print_info "To view logs:"
for i in $(seq 1 $STP_COUNT); do
    echo "  cat $PARALLEL_DIR/${i}-openshift-virtualization-tests/${VERSION}_experiment_${TIMESTAMP}/claude.log"
done
echo ""
print_info "To check status:"
for i in $(seq 1 $STP_COUNT); do
    status_file="$PARALLEL_DIR/${i}-openshift-virtualization-tests/${VERSION}_experiment_${TIMESTAMP}/status.txt"
    if [ -f "$status_file" ]; then
        cat "$status_file"
    fi
done
echo ""
