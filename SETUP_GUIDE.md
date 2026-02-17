# Setup Guide for Test Generation Experiments

## Overview

This repository contains multiple versions of test generation approaches, organized as an incremental evolution from v1 (monolithic) to v3 (fully modular with runtime self-healing).

## Running the Setup

```bash
./setup.sh
```

This script will:
1. Clone/update the `openshift-virtualization-tests` repository
2. Set up Python environment with `uv`
3. Install `pyright` for type checking
4. Copy all version commands and skills to `.claude/` directory

## Directory Structure After Setup

```
openshift-virtualization-tests/
├── .claude/
│   ├── commands/
│   │   ├── v0-experiment-*.md          # Individual v0 experiments
│   │   ├── v1-unified-prompt.md        # v1 monolithic prompt
│   │   ├── v2.1-orchestrator.md        # v2.1 orchestrator
│   │   ├── v2.2-orchestrator.md        # v2.2 orchestrator
│   │   ├── v2-orchestrator.md          # v2 full orchestrator
│   │   └── v3-orchestrator.md          # v3 orchestrator (+ runtime self-healing)
│   └── skills/
│       ├── v2.1-explore-test-context/  # v2.1 exploration (no context.json)
│       ├── v2.1-generate-pytest/       # v2.1 pytest generator
│       ├── v2.1-pyright-heal/          # v2.1 type healer
│       ├── v2.2-explore-test-context/  # v2.2 exploration (no context.json)
│       ├── v2.2-generate-std/          # v2.2 STD generator
│       ├── v2.2-generate-pytest/       # v2.2 pytest generator
│       ├── v2.2-pyright-heal/          # v2.2 type healer
│       ├── v2-explore-test-context/    # v2 exploration (context.json)
│       ├── v2-generate-std/            # v2 STD generator
│       ├── v2-generate-pytest/         # v2 pytest generator
│       ├── v2-pyright-heal/            # v2 type healer
│       ├── v3-explore-test-context/    # v3 exploration (+ GRAVEYARD review)
│       ├── v3-generate-std/            # v3 STD generator
│       ├── v3-generate-pytest/         # v3 pytest generator (GRAVEYARD-aware)
│       ├── v3-pyright-heal/            # v3 type healer
│       └── v3-test-heal/              # v3 runtime self-healing (NEW)
├── .venv/                              # Python virtual environment
└── [rest of repository files]
```

## Available Commands

### v0 Experiments
Individual experiment prompts from the initial version:
```
/v0-experiment-1
/v0-experiment-2
...
```

### v1 Unified Prompt
Single monolithic prompt with all phases inline:
```
/v1-unified-prompt
```

### v2.1 Orchestrator
Modular skills with separate exploration (no caching):
```
/v2.1-orchestrator
```

### v2.2 Orchestrator
Adds STD generation to v2.1:
```
/v2.2-orchestrator
```

### v2 Full Orchestrator
Complete modular architecture with context.json caching:
```
/v2-orchestrator
```

### v3 Orchestrator
Adds runtime self-healing and GRAVEYARD.md feedback loop:
```
/v3-orchestrator
```

## Available Skills

Skills are version-prefixed to allow all versions to coexist.

### v2.1 Skills (No context.json)
- `/v2.1-explore-test-context` - Explore repository, report findings verbally
- `/v2.1-generate-pytest` - Generate pytest from STP
- `/v2.1-pyright-heal` - Fix type errors

### v2.2 Skills (+ STD generation, no context.json)
- `/v2.2-explore-test-context` - Explore repository, report findings verbally
- `/v2.2-generate-std` - Generate STD from STP
- `/v2.2-generate-pytest` - Generate pytest from STD
- `/v2.2-pyright-heal` - Fix type errors

### v2 Skills (Full with context.json)
- `/v2-explore-test-context` - Explore repository, output context.json
- `/v2-generate-std` - Generate STD from STP
- `/v2-generate-pytest` - Generate pytest from STD + context.json
- `/v2-pyright-heal` - Fix type errors

### v3 Skills (Runtime self-healing + GRAVEYARD)
- `/v3-explore-test-context` - Explore repository + review GRAVEYARD.md lessons
- `/v3-generate-std` - Generate STD from STP
- `/v3-generate-pytest` - Generate pytest from STD (GRAVEYARD-aware)
- `/v3-pyright-heal` - Fix type errors
- `/v3-test-heal` - Run test on cluster, fix failures, update GRAVEYARD.md

## Usage Examples

### Using v2.1 (Modular, no STD, no caching)

```bash
cd openshift-virtualization-tests

# Option 1: Use orchestrator
/v2.1-orchestrator
# Provide STP file when prompted

# Option 2: Use skills manually
/v2.1-explore-test-context
/v2.1-generate-pytest stps/3.md
/v2.1-pyright-heal tests/virt/lifecycle/test_vm_reset.py
```

### Using v2.2 (+ STD generation, no caching)

```bash
cd openshift-virtualization-tests

# Option 1: Use orchestrator (automated)
/v2.2-orchestrator
# Provide STP file when prompted

# Option 2: Use skills manually
/v2.2-generate-std stps/3.md
/v2.2-explore-test-context
/v2.2-generate-pytest std_vm_reset.md
/v2.2-pyright-heal tests/virt/lifecycle/test_vm_reset.py
```

### Using v2 Full (With context.json caching)

```bash
cd openshift-virtualization-tests

# Option 1: Use orchestrator
/v2-orchestrator
# Provide STP file when prompted

# Option 2: Use skills manually with caching
/v2-generate-std stps/3.md
/v2-explore-test-context  # Creates context.json
/v2-generate-pytest std_vm_reset.md context.json
/v2-pyright-heal tests/virt/lifecycle/test_vm_reset.py

# Generate another test reusing context
/v2-generate-std stps/4.md
/v2-generate-pytest std_vm_restart.md context.json  # Reuses context!
/v2-pyright-heal tests/virt/lifecycle/test_vm_restart.py
```

### Using v3 (Runtime self-healing + GRAVEYARD)

```bash
cd openshift-virtualization-tests

# Option 1: Use orchestrator (all 5 phases automated)
/v3-orchestrator
# Provide STP file when prompted

# Option 2: Use skills manually
/v3-generate-std stps/3.md
/v3-explore-test-context          # Also reads GRAVEYARD.md
/v3-generate-pytest std_vm_reset.md
/v3-pyright-heal tests/virt/lifecycle/test_vm_reset.py
/v3-test-heal tests/virt/lifecycle/test_vm_reset.py  # Runs on cluster, fixes, updates GRAVEYARD
```

## Version Comparison Quick Reference

| Version | Skills | Phases | STD | Context Exploration | Context Caching | Runtime Healing | GRAVEYARD |
|---------|--------|--------|-----|---------------------|-----------------|-----------------|-----------|
| v1 | 0 (monolithic) | 3 | ❌ | Inline | ❌ | ❌ | ❌ |
| v2.1 | 3 | 3 | ❌ | Separate skill (verbal) | ❌ | ❌ | ❌ |
| v2.2 | 4 | 4 | ✅ | Separate skill (verbal) | ❌ | ❌ | ❌ |
| v2 | 4 | 4 | ✅ | Separate skill (context.json) | ✅ | ❌ | ❌ |
| v3 | 5 | 5 | ✅ | Separate skill (verbal + GRAVEYARD) | ❌ | ✅ | ✅ |

## Workflow Diagrams

### v2.1 Workflow
```
STP → /v2.1-explore-test-context → (verbal)
        ↓
    /v2.1-generate-pytest → draft_test.py
        ↓
    /v2.1-pyright-heal → final_test.py ✓
```

### v2.2 Workflow
```
STP → /v2.2-generate-std → STD
        ↓
    /v2.2-explore-test-context → (verbal)
        ↓
    /v2.2-generate-pytest → draft_test.py
        ↓
    /v2.2-pyright-heal → final_test.py ✓
```

### v2 Full Workflow
```
STP → /v2-generate-std → STD
        ↓
    /v2-explore-test-context → context.json (cached!)
        ↓
    /v2-generate-pytest (STD + context.json) → draft_test.py
        ↓
    /v2-pyright-heal → final_test.py ✓
```

### v3 Workflow
```
STP → /v3-generate-std → STD
        ↓
    /v3-explore-test-context → (verbal + GRAVEYARD lessons)
        ↓
    /v3-generate-pytest → draft_test.py (avoids known mistakes)
        ↓
    /v3-pyright-heal → type_safe_test.py
        ↓
    /v3-test-heal → passing_test.py ✓ + GRAVEYARD.md updated
```

## Running Experiments

Each version has experiment scripts:

```bash
# v1 experiments
cd v1
./run_experiment.sh ../stps/3.md experiment_1

# v2.1 experiments
cd v2.1
./run_experiment.sh ../stps/3.md experiment_1

# v2.2 experiments
cd v2.2
./run_experiment.sh ../stps/3.md experiment_1

# v2 experiments
cd v2
./run_experiment.sh ../stps/3.md experiment_1

# v3 experiments
cd v3
./run_experiment.sh ../stps/3.md experiment_1
```

## Key Differences Summary

### v2.1 vs v1
- ✅ Modular skills (can be used independently)
- ✅ Separate exploration skill (clearer workflow)
- ✅ Universal pyright-heal (works on any .py file)
- ❌ No STD generation
- ❌ No context caching

### v2.2 vs v2.1
- ✅ STD generation as intermediate artifact
- ✅ Can review/edit STD before code generation
- ✅ Interactive mode support
- ❌ Still no context caching

### v2 vs v2.2
- ✅ Context caching (context.json artifact)
- ✅ Explore once, generate multiple tests
- ✅ Time/cost savings from reusing context

### v3 vs v2.2
- ✅ Phase 5: Runtime self-healing against live cluster
- ✅ GRAVEYARD.md feedback loop (learn from past mistakes)
- ✅ Exploration reads GRAVEYARD.md to avoid repeating errors
- ✅ Code generation is GRAVEYARD-aware

## Troubleshooting

### Skills not appearing
```bash
# Re-run setup script
./setup.sh

# Verify skills were copied
ls -la openshift-virtualization-tests/.claude/skills/
```

### Pyright not working
```bash
cd openshift-virtualization-tests
uv pip install pyright
uv run pyright --version
```

### Permission denied
```bash
chmod +x setup.sh
./setup.sh
```

## Next Steps

1. Review `VERSION_COMPARISON.md` for detailed evolution explanation
2. Check individual version README files:
   - `v2.1/README.md`
   - `v2.2/README.md`
   - `v2/README.md`
   - `v3/README.md`
3. Start experimenting with different versions
4. Compare results across versions

## Documentation Files

- `VERSION_COMPARISON.md` - Detailed comparison of all versions
- `v2.1/README.md` - v2.1 specific documentation
- `v2.2/README.md` - v2.2 specific documentation
- `v2/README.md` - v2 full version documentation
- `v3/README.md` - v3 specific documentation (runtime self-healing + GRAVEYARD)
