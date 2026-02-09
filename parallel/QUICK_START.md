# Quick Start Guide - Parallel Execution

## TL;DR

```bash
# 1. Setup (first time only - takes 5-10 minutes)
cd parallel
./setup_parallel.sh

# 2. Run experiments on all STPs in parallel
./run_parallel.sh v2.1

# 3. Collect results (replace timestamp with actual value from step 2)
./collect_results.sh v2.1 20260209_143022

# 4. View summary
cat results_v2.1_20260209_143022/summary.md
```

## What Gets Created

### After Setup
```
parallel/
├── 1-openshift-virtualization-tests/  # STP 1
├── 2-openshift-virtualization-tests/  # STP 2
├── 3-openshift-virtualization-tests/  # STP 3
├── 4-openshift-virtualization-tests/  # STP 4
├── 5-openshift-virtualization-tests/  # STP 5
├── 6-openshift-virtualization-tests/  # STP 6
└── 7-openshift-virtualization-tests/  # STP 7
```

Each clone has all versions (v1, v2.1, v2.2, v2) configured.

### After Running Experiments
```
parallel/
├── 1-openshift-virtualization-tests/
│   └── v2.1_experiment_20260209_143022/
│       ├── claude.log
│       ├── status.txt
│       └── [generated test files]
├── 2-openshift-virtualization-tests/
│   └── v2.1_experiment_20260209_143022/
│       └── ...
└── ...
```

### After Collecting Results
```
parallel/
└── results_v2.1_20260209_143022/
    ├── summary.md          # Overview of all results
    ├── stp_1/              # Copy of STP 1 results
    ├── stp_2/              # Copy of STP 2 results
    └── ...
```

## Available Commands

### Setup
```bash
./setup_parallel.sh
```
- Clones repo 7 times (one per STP)
- Sets up Python environment
- Installs pyright
- Copies all version skills/commands

**Run once.** Re-running will update repos.

### Run Experiments
```bash
./run_parallel.sh <version>
```

Where `<version>` is:
- `v1` - Monolithic prompt
- `v2.1` - Modular, no STD, no caching
- `v2.2` - Modular, + STD, no caching
- `v2` - Full modular with caching

**Example:**
```bash
./run_parallel.sh v2.2
```

**Output:**
```
Running v2.2 Experiments in Parallel
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Version: v2.2
Number of STPs: 7
Parallel execution with --dangerously-skip-permissions

Launching 7 parallel experiments...

→ [STP 1] Started (PID: 12345) → 1-openshift-virtualization-tests/v2.2_experiment_20260209_143022/
→ [STP 2] Started (PID: 12346) → 2-openshift-virtualization-tests/v2.2_experiment_20260209_143022/
...

All experiments launched. Waiting for completion...

✓ [STP 1] Experiment completed (PID: 12345)
✓ [STP 2] Experiment completed (PID: 12346)
...
```

**Note the timestamp!** You'll need it for collecting results.

### Collect Results
```bash
./collect_results.sh <version> <timestamp>
```

**Example:**
```bash
./collect_results.sh v2.2 20260209_143022
```

**Creates:**
- `results_v2.2_20260209_143022/summary.md`
- Copies of all experiment outputs

## Monitoring Progress

### Watch All Logs
```bash
# In separate terminals, one per STP
tail -f 1-openshift-virtualization-tests/v2.1_experiment_*/claude.log
tail -f 2-openshift-virtualization-tests/v2.1_experiment_*/claude.log
# ... etc
```

### Check Running Processes
```bash
ps aux | grep claude
```

### Monitor System Resources
```bash
htop  # or top
```

## Typical Workflow

### Single Version Test
```bash
# 1. Setup
./setup_parallel.sh

# 2. Run one version
./run_parallel.sh v2.1
# Note timestamp: 20260209_143022

# 3. Monitor (optional)
tail -f *-openshift-virtualization-tests/v2.1_experiment_20260209_143022/claude.log

# 4. Collect results
./collect_results.sh v2.1 20260209_143022

# 5. Review
cat results_v2.1_20260209_143022/summary.md
```

### Compare All Versions
```bash
# 1. Setup
./setup_parallel.sh

# 2. Run all versions (note each timestamp)
./run_parallel.sh v1      # Timestamp: T1
./run_parallel.sh v2.1    # Timestamp: T2
./run_parallel.sh v2.2    # Timestamp: T3
./run_parallel.sh v2      # Timestamp: T4

# 3. Collect all results
./collect_results.sh v1 T1
./collect_results.sh v2.1 T2
./collect_results.sh v2.2 T3
./collect_results.sh v2 T4

# 4. Compare
diff results_v1_T1/summary.md results_v2.1_T2/summary.md
diff results_v2.1_T2/summary.md results_v2.2_T3/summary.md
diff results_v2.2_T3/summary.md results_v2_T4/summary.md
```

## Expected Timing

| Phase | Time |
|-------|------|
| Setup (first run) | 5-10 minutes |
| Setup (updates) | 1-2 minutes |
| v1 experiment | 5-10 min per STP |
| v2.1 experiment | 8-12 min per STP |
| v2.2 experiment | 10-15 min per STP |
| v2 experiment | 10-15 min per STP |
| Collect results | 30 seconds |

**Parallel speedup:** ~7x faster than sequential!

## Disk Space Requirements

- Each clone: ~500 MB
- 7 clones: ~3.5 GB
- Experiments: ~100 MB per run
- **Total recommended:** 5 GB free space

## Troubleshooting

### "claude command not found"
Install Claude Code CLI first.

### "No experiment directories found"
Check the timestamp matches the run output.

### Out of memory
Run fewer experiments in parallel by modifying `run_parallel.sh`.

### Stale experiments
Clean up old runs:
```bash
rm -rf *-openshift-virtualization-tests/v*_experiment_*/
```

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│ PARALLEL TEST GENERATION - QUICK REFERENCE              │
├─────────────────────────────────────────────────────────┤
│ Setup (once):                                           │
│   ./setup_parallel.sh                                   │
│                                                          │
│ Run experiments:                                        │
│   ./run_parallel.sh v1      # Monolithic               │
│   ./run_parallel.sh v2.1    # Modular, no STD/caching  │
│   ./run_parallel.sh v2.2    # + STD, no caching        │
│   ./run_parallel.sh v2      # Full with caching        │
│                                                          │
│ Collect results:                                        │
│   ./collect_results.sh <version> <timestamp>           │
│                                                          │
│ Monitor:                                                │
│   tail -f <N>-*/v*_experiment_*/claude.log             │
│   ps aux | grep claude                                  │
│                                                          │
│ Clean up:                                               │
│   rm -rf *-openshift-virtualization-tests/             │
└─────────────────────────────────────────────────────────┘
```

## Next Steps

- Read full documentation: `README.md`
- Review version comparison: `../VERSION_COMPARISON.md`
- Check setup guide: `../SETUP_GUIDE.md`
