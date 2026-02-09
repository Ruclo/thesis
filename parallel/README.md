# Parallel Test Generation Experiments

This directory contains infrastructure for running test generation experiments in parallel across all Software Test Plans (STPs).

## Overview

The parallel setup allows you to:
- Clone the openshift-virtualization-tests repository multiple times (one per STP)
- Run experiments on all STPs simultaneously
- Compare results across different versions (v1, v2.1, v2.2, v2)
- Efficiently test the entire test suite in parallel

## Directory Structure After Setup

```
parallel/
├── setup_parallel.sh           # Setup script (run first)
├── run_parallel.sh             # Execute experiments in parallel
├── collect_results.sh          # Collect and analyze results
├── README.md                   # This file
├── 1-openshift-virtualization-tests/   # Clone for STP 1
│   ├── .claude/
│   │   ├── commands/
│   │   │   ├── v1-unified-prompt.md
│   │   │   ├── v2.1-orchestrator.md
│   │   │   ├── v2.2-orchestrator.md
│   │   │   └── v2-orchestrator.md
│   │   └── skills/
│   │       ├── v2.1-*/
│   │       ├── v2.2-*/
│   │       └── v2-*/
│   └── [repository files]
├── 2-openshift-virtualization-tests/   # Clone for STP 2
├── 3-openshift-virtualization-tests/   # Clone for STP 3
├── 4-openshift-virtualization-tests/   # Clone for STP 4
├── 5-openshift-virtualization-tests/   # Clone for STP 5
├── 6-openshift-virtualization-tests/   # Clone for STP 6
└── 7-openshift-virtualization-tests/   # Clone for STP 7
```

## Setup

### 1. Initial Setup

Run the setup script to clone repositories and configure all versions:

```bash
cd parallel
./setup_parallel.sh
```

This will:
- Clone openshift-virtualization-tests 7 times (one per STP)
- Set up Python environment in each clone
- Install pyright in each clone
- Copy all version commands and skills to each clone's `.claude/` directory

The setup takes a few minutes on first run. Subsequent runs will pull latest changes.

## Running Experiments

### Run All STPs in Parallel

Execute a specific version across all STPs:

```bash
# Run v1 on all 7 STPs in parallel
./run_parallel.sh v1

# Run v2.1 on all 7 STPs in parallel
./run_parallel.sh v2.1

# Run v2.2 on all 7 STPs in parallel
./run_parallel.sh v2.2

# Run v2 (full) on all 7 STPs in parallel
./run_parallel.sh v2
```

### What Happens

For each STP:
1. The script launches `claude` in the corresponding clone directory
2. The STP file path is automatically determined by the clone prefix (1-7)
3. Claude runs with `--dangerously-skip-permissions` flag
4. Output is logged to `<version>_experiment_<timestamp>/claude.log`
5. All experiments run simultaneously in the background

### Experiment Output

Each run creates a directory structure:
```
<N>-openshift-virtualization-tests/
└── <version>_experiment_<timestamp>/
    ├── claude.log          # Full Claude output
    ├── status.txt          # Success/failure status
    └── [generated files]   # Test files, STDs, context.json, etc.
```

Example:
```
1-openshift-virtualization-tests/
└── v2.1_experiment_20260209_143022/
    ├── claude.log
    ├── status.txt
    └── tests/virt/lifecycle/test_vm_reset.py
```

## Collecting Results

After experiments complete, collect and analyze results:

```bash
./collect_results.sh <version> <timestamp>
```

Example:
```bash
./collect_results.sh v2.1 20260209_143022
```

This creates a `results_<version>_<timestamp>/` directory with:
- Summary report (summary.md)
- Copies of all experiment outputs
- Status of each STP experiment
- Error counts and analysis

## Monitoring Progress

### Check Running Experiments

```bash
# View all Claude processes
ps aux | grep claude

# Monitor a specific experiment log (follow mode)
tail -f 1-openshift-virtualization-tests/v2.1_experiment_*/claude.log
```

### Check Status Files

```bash
# Check status of all experiments
cat *-openshift-virtualization-tests/v2.1_experiment_*/status.txt
```

## Version Workflows

### v1 Workflow (Monolithic)
```
STP → [3 inline phases] → test.py
```
- Single prompt with all phases inline
- No separate skills
- Context exploration, code generation, pyright healing all in one

### v2.1 Workflow (Modular, No Caching)
```
STP → /v2.1-explore-test-context (verbal)
    → /v2.1-generate-pytest
    → /v2.1-pyright-heal
    → test.py
```
- 3 separate skills
- Context exploration outputs verbal summary
- No STD generation
- No context.json caching

### v2.2 Workflow (+ STD Generation)
```
STP → /v2.2-generate-std → STD
    → /v2.2-explore-test-context (verbal)
    → /v2.2-generate-pytest
    → /v2.2-pyright-heal
    → test.py
```
- 4 separate skills
- STD as intermediate artifact
- Context exploration outputs verbal summary
- No context.json caching

### v2 Workflow (Full, With Caching)
```
STP → /v2-generate-std → STD
    → /v2-explore-test-context → context.json
    → /v2-generate-pytest
    → /v2-pyright-heal
    → test.py
```
- 4 separate skills
- STD as intermediate artifact
- Context exploration outputs context.json
- Context caching enabled

## Example: Complete Run

```bash
# 1. Setup (first time only)
cd parallel
./setup_parallel.sh

# 2. Run v2.1 experiments in parallel
./run_parallel.sh v2.1

# 3. Wait for completion (monitor in another terminal)
tail -f *-openshift-virtualization-tests/v2.1_experiment_*/claude.log

# 4. Collect results (use the timestamp from the run)
./collect_results.sh v2.1 20260209_143022

# 5. View summary
cat results_v2.1_20260209_143022/summary.md
```

## Comparing Versions

To compare different versions:

```bash
# Run all versions in sequence
./run_parallel.sh v1      # Note the timestamp
./run_parallel.sh v2.1    # Note the timestamp
./run_parallel.sh v2.2    # Note the timestamp
./run_parallel.sh v2      # Note the timestamp

# Collect results for each
./collect_results.sh v1 <timestamp1>
./collect_results.sh v2.1 <timestamp2>
./collect_results.sh v2.2 <timestamp3>
./collect_results.sh v2 <timestamp4>

# Compare summary reports
diff results_v1_*/summary.md results_v2.1_*/summary.md
```

## Troubleshooting

### Claude Command Not Found

```bash
# Install Claude Code CLI
# Follow installation instructions from Anthropic
```

### Permission Issues

The scripts use `--dangerously-skip-permissions` flag to avoid interactive prompts. Ensure you understand the implications.

### Disk Space

Each clone is ~500MB. With 7 clones, you need ~3.5GB free space.

### Memory Usage

Running 7 Claude instances in parallel can be memory-intensive. Monitor system resources:

```bash
htop  # or top
```

Consider running in smaller batches if memory is limited:

```bash
# Modify run_parallel.sh to run only a subset
# e.g., run 1-3, wait, then run 4-7
```

### Cleaning Up

Remove all clones and start fresh:

```bash
cd parallel
rm -rf *-openshift-virtualization-tests/
./setup_parallel.sh
```

## Performance Notes

- **Setup time:** ~5-10 minutes for initial clone and setup
- **Experiment runtime:** Varies by version (v1: 5-10min, v2: 10-15min per STP)
- **Parallel speedup:** 7x faster than running sequentially
- **Resource usage:** High CPU and memory during parallel execution

## Best Practices

1. **Run setup first:** Always run `./setup_parallel.sh` before experiments
2. **Note timestamps:** Write down timestamps from each run for result collection
3. **Monitor resources:** Keep an eye on system resources during parallel runs
4. **Sequential comparison:** Consider running versions sequentially for fair comparison
5. **Clean logs:** Review logs regularly and clean up old experiment directories

## Output Files Reference

| File | Description |
|------|-------------|
| `claude.log` | Full Claude conversation log |
| `status.txt` | Success/failure status |
| `test_*.py` | Generated test file |
| `std_*.md` | Generated STD (v2.2, v2 only) |
| `context.json` | Repository context (v2 only) |
| `changes.patch` | Git diff of changes |

## Advanced Usage

### Custom STP Selection

Modify `run_parallel.sh` to run on specific STPs only:

```bash
# In run_parallel.sh, change the loop:
for i in 1 3 5; do  # Only run STPs 1, 3, 5
    run_experiment $i
done
```

### Different Versions Per STP

Create custom scripts to run different versions on different STPs based on STP characteristics.

### Automated Analysis

Extend `collect_results.sh` to perform automated analysis:
- Code quality metrics
- Test coverage analysis
- Success rate calculations
- Performance comparisons
