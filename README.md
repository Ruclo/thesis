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

## 4. Repository Structure

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
