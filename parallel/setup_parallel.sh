#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

REPO_URL="https://github.com/Ruclo/openshift-virtualization-tests.git"
THESIS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PARALLEL_DIR="$THESIS_DIR/parallel"
STPS_DIR="$THESIS_DIR/stps"

print_header "Setting up Parallel Test Generation Environment"

# Count STPs
STP_COUNT=$(find "$STPS_DIR" -name "*.md" -type f | wc -l)
print_info "Found $STP_COUNT STP files"

cd "$PARALLEL_DIR"

# Clone repository for each STP
for i in $(seq 1 $STP_COUNT); do
    TARGET_DIR="${i}-openshift-virtualization-tests"

    if [ -d "$TARGET_DIR" ]; then
        print_info "[$i/$STP_COUNT] Repository $TARGET_DIR already exists, pulling latest changes..."
        cd "$TARGET_DIR"
        git pull --quiet
        cd "$PARALLEL_DIR"
    else
        print_info "[$i/$STP_COUNT] Cloning repository into $TARGET_DIR..."
        git clone --quiet "$REPO_URL" "$TARGET_DIR"
    fi

    print_success "[$i/$STP_COUNT] Repository ready: $TARGET_DIR"
done

print_header "Setting up Python Environment and Dependencies"

# Set up Python environment in each clone
for i in $(seq 1 $STP_COUNT); do
    TARGET_DIR="${i}-openshift-virtualization-tests"
    cd "$PARALLEL_DIR/$TARGET_DIR"

    print_info "[$i/$STP_COUNT] Setting up Python environment in $TARGET_DIR..."

    # Create venv if it doesn't exist
    if [ ! -d ".venv" ]; then
        uv venv --quiet
    fi

    # Install pyright if not installed
    if ! uv run pyright --version &> /dev/null; then
        print_info "[$i/$STP_COUNT] Installing pyright..."
        uv pip install --quiet pyright
    fi

    print_success "[$i/$STP_COUNT] Python environment ready"
done

print_header "Copying Skills and Commands to Each Clone"

# Set up all versions in each clone
for i in $(seq 1 $STP_COUNT); do
    TARGET_DIR="$PARALLEL_DIR/${i}-openshift-virtualization-tests"

    print_info "[$i/$STP_COUNT] Setting up versions in $TARGET_DIR..."

    mkdir -p "$TARGET_DIR/.claude/commands"
    mkdir -p "$TARGET_DIR/.claude/skills"

    # Set up v1
    if [ -f "$THESIS_DIR/v1/prompt.md" ]; then
        cp "$THESIS_DIR/v1/prompt.md" "$TARGET_DIR/.claude/commands/v1-unified-prompt.md"
    fi

    # Set up v2.1
    if [ -f "$THESIS_DIR/v2.1/orchestrator.md" ]; then
        cp "$THESIS_DIR/v2.1/orchestrator.md" "$TARGET_DIR/.claude/commands/v2.1-orchestrator.md"
    fi
    if [ -d "$THESIS_DIR/v2.1/skills" ]; then
        cp -r "$THESIS_DIR/v2.1/skills/"* "$TARGET_DIR/.claude/skills/"
    fi

    # Set up v2.2
    if [ -f "$THESIS_DIR/v2.2/orchestrator.md" ]; then
        cp "$THESIS_DIR/v2.2/orchestrator.md" "$TARGET_DIR/.claude/commands/v2.2-orchestrator.md"
    fi
    if [ -d "$THESIS_DIR/v2.2/skills" ]; then
        cp -r "$THESIS_DIR/v2.2/skills/"* "$TARGET_DIR/.claude/skills/"
    fi

    # Set up v2
    if [ -f "$THESIS_DIR/v2/orchestrator.md" ]; then
        cp "$THESIS_DIR/v2/orchestrator.md" "$TARGET_DIR/.claude/commands/v2-orchestrator.md"
    fi
    if [ -d "$THESIS_DIR/v2/skills" ]; then
        cp -r "$THESIS_DIR/v2/skills/"* "$TARGET_DIR/.claude/skills/"
    fi

    print_success "[$i/$STP_COUNT] All versions configured"
done

cd "$PARALLEL_DIR"

print_header "Setup Complete!"
echo ""
echo "Created $STP_COUNT parallel repositories:"
for i in $(seq 1 $STP_COUNT); do
    echo "  ${i}-openshift-virtualization-tests → stps/${i}.md"
done
echo ""
echo "Each repository has the following versions configured:"
echo "  - v1 (command: /v1-unified-prompt)"
echo "  - v2.1 (command: /v2.1-orchestrator, skills: /v2.1-*)"
echo "  - v2.2 (command: /v2.2-orchestrator, skills: /v2.2-*)"
echo "  - v2 (command: /v2-orchestrator, skills: /v2-*)"
echo ""
echo "Next steps:"
echo "  ./run_parallel.sh <version>   # Run all experiments in parallel"
echo "  ./run_parallel.sh v1          # Example: run v1 on all STPs"
echo "  ./run_parallel.sh v2.1        # Example: run v2.1 on all STPs"
echo ""
