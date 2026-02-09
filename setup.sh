#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

REPO_URL="https://github.com/Ruclo/openshift-virtualization-tests.git"
TARGET_DIR="openshift-virtualization-tests"
THESIS_DIR="$(cd "$(dirname "$0")" && pwd)"

print_info "Setting up OpenShift Virtualization Tests repository..."

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

# Copy v2.1 skills
if [ -d "$THESIS_DIR/v2.1/skills" ]; then
    print_info "Copying v2.1 skills to .claude/skills/"
    for skill_dir in "$THESIS_DIR"/v2.1/skills/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            skill_name_v21="v2.1-$skill_name"
            mkdir -p ".claude/skills/$skill_name_v21"
            if [ -f "$skill_dir/SKILL.md" ]; then
                cp "$skill_dir/SKILL.md" ".claude/skills/$skill_name_v21/"
                print_info "  Copied skill: $skill_name_v21"
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

# Copy v2.2 skills
if [ -d "$THESIS_DIR/v2.2/skills" ]; then
    print_info "Copying v2.2 skills to .claude/skills/"
    for skill_dir in "$THESIS_DIR"/v2.2/skills/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            skill_name_v22="v2.2-$skill_name"
            mkdir -p ".claude/skills/$skill_name_v22"
            if [ -f "$skill_dir/SKILL.md" ]; then
                cp "$skill_dir/SKILL.md" ".claude/skills/$skill_name_v22/"
                print_info "  Copied skill: $skill_name_v22"
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

# Copy v2 skills
if [ -d "$THESIS_DIR/v2/skills" ]; then
    print_info "Copying v2 skills to .claude/skills/"
    for skill_dir in "$THESIS_DIR"/v2/skills/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            skill_name_v2="v2-$skill_name"
            mkdir -p ".claude/skills/$skill_name_v2"
            if [ -f "$skill_dir/SKILL.md" ]; then
                cp "$skill_dir/SKILL.md" ".claude/skills/$skill_name_v2/"
                print_info "  Copied skill: $skill_name_v2"
            fi
        fi
    done
    print_success "v2 skills set up"
else
    print_error "v2/skills directory not found"
fi

cd "$THESIS_DIR"

print_success "Setup complete!"
echo ""
echo "Repository location: $TARGET_DIR"
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
echo "Next steps:"
echo "  cd $TARGET_DIR"
echo "  # Use Claude Code with the configured commands and skills"
