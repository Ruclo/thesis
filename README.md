# Agentic Architecture for E2E Test Generation
**Bachelor's Thesis Project** | *OpenShift Virtualization*

## 1. Project Overview
This repository contains the implementation, experimental data, and results for the thesis: **"Bridging the Gap: An Agentic Architecture for Translating Natural Language Test Plans into Executable E2E Code."**

The goal is to develop an AI agent capable of reading a "Written Test Plan" (STP) and deterministically generating compilable, compliant End-to-End tests for the OpenShift Virtualization repository.

## 2. Research Methodology
The research is divided into phases to measure the impact of Context Engineering.

* **Phase 0 (Baseline):** Naive LLM generation using state-of-the-art models (Claude 3.7 Sonnet / Claude Code) with zero repository context.
* **Phase 1 (Context Retrieval):** Augmented generation using a custom MCP (Model Context Protocol) server to fetch repo-specific utilities and constants.
* **Phase 2 (Agentic Loop):** Closed-loop generation where the agent iteratively fixes compilation/linting errors.

## 3. Setup

Run the setup script from the thesis directory:

```bash
./setup.sh
```

The setup script will:
1. Clone the openshift-virtualization-tests repository once
2. Set up Python environment with `uv`
3. Install and verify `pyright` works
4. Configure Claude Code commands and skills:
   - **v0**: Each experiment prompt → `.claude/commands/v0-experiment-*.md`
   - **v1**: Unified prompt → `.claude/commands/v1-unified-prompt.md`
   - **v2**: Orchestrator → `.claude/commands/v2-orchestrator.md` + skills → `.claude/skills/`

After setup, navigate to the repository:
```bash
cd openshift-virtualization-tests
```

All version-specific commands and skills will be available through Claude Code.

## 4. Parallel Execution

The `parallel/` directory contains scripts to run experiments across all 7 STPs simultaneously using git worktrees.

### Setup

The main `./setup.sh` script automatically creates git worktrees in `parallel/` (one per STP) and configures all versions for each worktree.

**Git worktrees** share the same `.git` directory, saving significant disk space (~100MB per worktree vs ~500MB per clone).

After setup, you'll have:
```
parallel/
├── run_parallel.sh              # Execute experiments in parallel
├── collect_results.sh           # Collect and analyze results
├── 1-openshift-virtualization-tests/   # Worktree for STP 1
├── 2-openshift-virtualization-tests/   # Worktree for STP 2
├── ...
└── 7-openshift-virtualization-tests/   # Worktree for STP 7
```

### Running Parallel Experiments

Execute a version across all 7 STPs:

```bash
cd parallel

# Run v1 on all STPs in parallel
./run_parallel.sh v1

# Run v2.1 on all STPs in parallel
./run_parallel.sh v2.1

# Run v2.2 on all STPs in parallel
./run_parallel.sh v2.2

# Run v2 (full) on all STPs in parallel
./run_parallel.sh v2
```

**Note the timestamp** from the output - you'll need it for collecting results.

### Collecting Results

After experiments complete:

```bash
./collect_results.sh <version> <timestamp>

# Example:
./collect_results.sh v2.1 20260209_143022
```

This creates `results_<version>_<timestamp>/` with:
- `summary.md` - Overview of all results
- Copies of all experiment outputs per STP
- Status and error analysis

### Monitoring Progress

```bash
# Watch experiment logs
tail -f 1-openshift-virtualization-tests/v2.1_experiment_*/claude.log

# Check running processes
ps aux | grep claude

# Monitor system resources
htop
```

### Performance

- **Parallel speedup:** ~7x faster than sequential execution
- **Disk space:** ~1.2GB total (main repo + 7 worktrees) vs ~3.5GB for full clones
- **Runtime:** Varies by version (v1: 5-10min, v2: 10-15min per STP)

## 5. Repository Structure

### `/v0` - Baseline Experiments (Control Group)
This folder contains the "Naive" generation attempts. In these experiments, the LLM was given the Test Plan and basic instructions but **no access** to the repository's helper functions, constants, or fixture definitions.

**Naming Convention:** `experiment_{id}_{topic}`

#### Example Structure:
```text
v0/
├── experiment_01_common_instancetypes/
│   ├── prompt.md           # The exact input prompt (STP + Instructions)
│   ├── claude.log         # Full conversation log with Claude Code
│   ├── changes.patch       # Git diff showing file placement in the repo
│   └── test_run.log     # Pytest traceback/error log (The "Result")
├── experiment_02_windows_vnc/
│   └── ...
└── experiment_03_rhel_vnc/
    └── ...
