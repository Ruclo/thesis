#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
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
TARGET_DIR="openshift-virtualization-tests"
THESIS_DIR="$(cd "$(dirname "$0")" && pwd)"
STPS_DIR="$THESIS_DIR/stps"

print_header "Setting up OpenShift Virtualization Tests repository"

# Navigate to thesis directory
cd "$THESIS_DIR"

# Handle existing directory
if [ -d "$TARGET_DIR" ]; then
    if [ -d "$TARGET_DIR/.git" ]; then
        print_info "Git repository already exists in $TARGET_DIR, pulling latest changes..."
        cd "$TARGET_DIR"
        git pull
        cd "$THESIS_DIR"
    else
        print_error "Directory $TARGET_DIR exists but is not a git repository. Please remove it first."
        exit 1
    fi
else
    # Clone repository
    print_info "Cloning repository into $TARGET_DIR..."
    git clone "$REPO_URL" "$TARGET_DIR"
fi

print_success "Repository ready in $TARGET_DIR"

# Navigate to target directory
cd "$TARGET_DIR"

# Check if uv is installed
print_info "Checking for uv installation..."
if ! command -v uv &> /dev/null; then
    print_error "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi
print_success "uv is installed"

# Set up Python environment and check pyright
print_info "Setting up Python environment..."
if [ ! -d ".venv" ]; then
    uv venv
fi
print_success "Python environment ready"

print_info "Checking pyright installation..."
if ! uv run pyright --version &> /dev/null; then
    print_info "Installing pyright..."
    uv pip install pyright
fi
print_success "pyright is working"

# Set up parallel worktrees if STPs exist
if [ -d "$STPS_DIR" ]; then
    STP_COUNT=$(find "$STPS_DIR" -name "*.md" -type f | wc -l)

    if [ $STP_COUNT -gt 0 ]; then
        print_header "Setting up parallel test generation worktrees"
        print_info "Found $STP_COUNT STP files"

        PARALLEL_DIR="$THESIS_DIR/parallel"
        mkdir -p "$PARALLEL_DIR"

        # Set up worktree for each STP
        for i in $(seq 1 $STP_COUNT); do
            WORKTREE_DIR="$PARALLEL_DIR/${i}-openshift-virtualization-tests"

            if [ -d "$WORKTREE_DIR" ]; then
                print_info "[$i/$STP_COUNT] Worktree already exists: ${i}-openshift-virtualization-tests"
            else
                print_info "[$i/$STP_COUNT] Creating worktree: ${i}-openshift-virtualization-tests"
                git worktree add "$WORKTREE_DIR" HEAD
            fi

            print_success "[$i/$STP_COUNT] Worktree ready: ${i}-openshift-virtualization-tests"
        done

        print_header "Setting up Python environment in worktrees"

        # Set up Python environment in each worktree
        for i in $(seq 1 $STP_COUNT); do
            WORKTREE_DIR="$PARALLEL_DIR/${i}-openshift-virtualization-tests"
            cd "$WORKTREE_DIR"

            print_info "[$i/$STP_COUNT] Setting up Python environment..."

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

        cd "$THESIS_DIR/$TARGET_DIR"
    fi
fi

# Create Claude directories
print_info "Setting up Claude configuration..."
mkdir -p .claude/commands
mkdir -p .claude/skills

# v0: Copy all experiment prompts as commands with v0- prefix
print_info "Setting up v0 commands..."
for exp_dir in "$THESIS_DIR"/v0/experiment_*/; do
    if [ -d "$exp_dir" ]; then
        exp_name=$(basename "$exp_dir")
        prompt_file="$exp_dir/prompt.md"
        if [ -f "$prompt_file" ]; then
            # Extract experiment number and name
            exp_id=$(echo "$exp_name" | grep -oP 'experiment_\K\d+')
            exp_topic=$(echo "$exp_name" | sed 's/experiment_[0-9]*_*//')

            if [ -z "$exp_topic" ]; then
                command_name="v0-experiment-${exp_id}.md"
            else
                command_name="v0-experiment-${exp_id}-${exp_topic}.md"
            fi

            cp "$prompt_file" ".claude/commands/$command_name"
            print_info "  Copied: $command_name"
        fi
    fi
done
print_success "v0 commands set up"

# v1: Copy single prompt as command with v1- prefix
print_info "Setting up v1 command..."
if [ -f "$THESIS_DIR/v1/prompt.md" ]; then
    cp "$THESIS_DIR/v1/prompt.md" ".claude/commands/v1-unified-prompt.md"
    print_success "v1 command set up"
else
    print_error "v1/prompt.md not found"
fi

# v2.1: Copy orchestrator as command with v2.1- prefix and skills
print_info "Setting up v2.1 command and skills..."
if [ -f "$THESIS_DIR/v2.1/orchestrator.md" ]; then
    cp "$THESIS_DIR/v2.1/orchestrator.md" ".claude/commands/v2.1-orchestrator.md"
    print_success "v2.1 orchestrator command set up"
else
    print_error "v2.1/orchestrator.md not found"
fi

# Copy v2.1 skills (directories already have v2.1- prefix)
if [ -d "$THESIS_DIR/v2.1/skills" ]; then
    print_info "Copying v2.1 skills to .claude/skills/"
    for skill_dir in "$THESIS_DIR"/v2.1/skills/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            mkdir -p ".claude/skills/$skill_name"
            if [ -f "$skill_dir/SKILL.md" ]; then
                cp "$skill_dir/SKILL.md" ".claude/skills/$skill_name/"
                print_info "  Copied skill: $skill_name"
            fi
        fi
    done
    print_success "v2.1 skills set up"
else
    print_error "v2.1/skills directory not found"
fi

# v2.2: Copy orchestrator as command with v2.2- prefix and skills
print_info "Setting up v2.2 command and skills..."
if [ -f "$THESIS_DIR/v2.2/orchestrator.md" ]; then
    cp "$THESIS_DIR/v2.2/orchestrator.md" ".claude/commands/v2.2-orchestrator.md"
    print_success "v2.2 orchestrator command set up"
else
    print_error "v2.2/orchestrator.md not found"
fi

# Copy v2.2 skills (directories already have v2.2- prefix)
if [ -d "$THESIS_DIR/v2.2/skills" ]; then
    print_info "Copying v2.2 skills to .claude/skills/"
    for skill_dir in "$THESIS_DIR"/v2.2/skills/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            mkdir -p ".claude/skills/$skill_name"
            if [ -f "$skill_dir/SKILL.md" ]; then
                cp "$skill_dir/SKILL.md" ".claude/skills/$skill_name/"
                print_info "  Copied skill: $skill_name"
            fi
        fi
    done
    print_success "v2.2 skills set up"
else
    print_error "v2.2/skills directory not found"
fi

# v2: Copy orchestrator as command with v2- prefix and skills
print_info "Setting up v2 (full) command and skills..."
if [ -f "$THESIS_DIR/v2/orchestrator.md" ]; then
    cp "$THESIS_DIR/v2/orchestrator.md" ".claude/commands/v2-orchestrator.md"
    print_success "v2 orchestrator command set up"
else
    print_error "v2/orchestrator.md not found"
fi

# Copy v2 skills (directories already have v2- prefix)
if [ -d "$THESIS_DIR/v2/skills" ]; then
    print_info "Copying v2 skills to .claude/skills/"
    for skill_dir in "$THESIS_DIR"/v2/skills/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            mkdir -p ".claude/skills/$skill_name"
            if [ -f "$skill_dir/SKILL.md" ]; then
                cp "$skill_dir/SKILL.md" ".claude/skills/$skill_name/"
                print_info "  Copied skill: $skill_name"
            fi
        fi
    done
    print_success "v2 skills set up"
else
    print_error "v2/skills directory not found"
fi

cd "$THESIS_DIR"

# Copy Claude configurations to worktrees
if [ -d "$STPS_DIR" ]; then
    STP_COUNT=$(find "$STPS_DIR" -name "*.md" -type f | wc -l)

    if [ $STP_COUNT -gt 0 ]; then
        print_header "Copying configurations to worktrees"

        PARALLEL_DIR="$THESIS_DIR/parallel"

        for i in $(seq 1 $STP_COUNT); do
            WORKTREE_DIR="$PARALLEL_DIR/${i}-openshift-virtualization-tests"

            print_info "[$i/$STP_COUNT] Copying Claude configuration to worktree ${i}..."

            # Create Claude directories
            mkdir -p "$WORKTREE_DIR/.claude/commands"
            mkdir -p "$WORKTREE_DIR/.claude/skills"

            # Copy v1
            if [ -f "$THESIS_DIR/v1/prompt.md" ]; then
                cp "$THESIS_DIR/v1/prompt.md" "$WORKTREE_DIR/.claude/commands/v1-unified-prompt.md"
            fi

            # Copy v2.1
            if [ -f "$THESIS_DIR/v2.1/orchestrator.md" ]; then
                cp "$THESIS_DIR/v2.1/orchestrator.md" "$WORKTREE_DIR/.claude/commands/v2.1-orchestrator.md"
            fi
            if [ -d "$THESIS_DIR/v2.1/skills" ]; then
                cp -r "$THESIS_DIR/v2.1/skills/"* "$WORKTREE_DIR/.claude/skills/" 2>/dev/null || true
            fi

            # Copy v2.2
            if [ -f "$THESIS_DIR/v2.2/orchestrator.md" ]; then
                cp "$THESIS_DIR/v2.2/orchestrator.md" "$WORKTREE_DIR/.claude/commands/v2.2-orchestrator.md"
            fi
            if [ -d "$THESIS_DIR/v2.2/skills" ]; then
                cp -r "$THESIS_DIR/v2.2/skills/"* "$WORKTREE_DIR/.claude/skills/" 2>/dev/null || true
            fi

            # Copy v2
            if [ -f "$THESIS_DIR/v2/orchestrator.md" ]; then
                cp "$THESIS_DIR/v2/orchestrator.md" "$WORKTREE_DIR/.claude/commands/v2-orchestrator.md"
            fi
            if [ -d "$THESIS_DIR/v2/skills" ]; then
                cp -r "$THESIS_DIR/v2/skills/"* "$WORKTREE_DIR/.claude/skills/" 2>/dev/null || true
            fi

            print_success "[$i/$STP_COUNT] Configuration copied"
        done
    fi
fi

print_header "Setup Complete!"
echo ""
echo "Main repository location: $TARGET_DIR"
echo ""
echo "Available commands:"
echo "  v0-experiment-* : Individual experiment prompts from v0"
echo "  v1-unified-prompt : Single unified prompt from v1"
echo "  v2.1-orchestrator : Orchestrator command from v2.1 (modular, no context.json)"
echo "  v2.2-orchestrator : Orchestrator command from v2.2 (+ STD generation)"
echo "  v2-orchestrator : Orchestrator command from v2 (full, with context.json)"
echo ""
echo "Available skills:"
ls -1 "$TARGET_DIR/.claude/skills/" 2>/dev/null | sed 's/^/  /'
echo ""
echo "Skill versions:"
echo "  v2.1-* : Skills from v2.1 (exploration outputs verbal summary, no context.json)"
echo "  v2.2-* : Skills from v2.2 (adds STD generation)"
echo "  v2-* : Skills from v2 (full version with context.json caching)"
echo ""

# Print parallel setup info if STPs exist
if [ -d "$STPS_DIR" ]; then
    STP_COUNT=$(find "$STPS_DIR" -name "*.md" -type f | wc -l)
    if [ $STP_COUNT -gt 0 ]; then
        echo "Parallel worktrees created: $STP_COUNT"
        echo "Worktree locations:"
        for i in $(seq 1 $STP_COUNT); do
            echo "  parallel/${i}-openshift-virtualization-tests → stps/${i}.md"
        done
        echo ""
        echo "Each worktree shares the same git repository and has:"
        echo "  - v1 (command: /v1-unified-prompt)"
        echo "  - v2.1 (command: /v2.1-orchestrator, skills: /v2.1-*)"
        echo "  - v2.2 (command: /v2.2-orchestrator, skills: /v2.2-*)"
        echo "  - v2 (command: /v2-orchestrator, skills: /v2-*)"
        echo ""
    fi
fi

echo "Next steps:"
echo "  cd $TARGET_DIR"
echo "  # Use Claude Code with the configured commands and skills"
if [ -d "$STPS_DIR" ]; then
    STP_COUNT=$(find "$STPS_DIR" -name "*.md" -type f | wc -l)
    if [ $STP_COUNT -gt 0 ]; then
        echo ""
        echo "For parallel execution:"
        echo "  cd parallel/<N>-openshift-virtualization-tests"
        echo "  # Run your preferred version on that STP"
    fi
fi
echo ""
