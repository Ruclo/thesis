# V3: Self-Healing Test Generation with GRAVEYARD

## Overview

V3 extends v2.2 with GRAVEYARD verification, runtime self-healing, and a persistent learning loop. Generated code is verified against GRAVEYARD.md before static analysis, then tested against a real cluster with automatic failure recovery.

Key additions over v2.2:
- ✅ Phase 4: GRAVEYARD verification — catch known mistakes before runtime
- ✅ Phase 6: Run tests against live cluster and self-heal failures
- ✅ GRAVEYARD.md: Persistent record of mistakes and lessons learned
- ✅ Exploration phase reads GRAVEYARD.md to avoid repeating past mistakes
- ✅ Code generation phase applies GRAVEYARD lessons proactively

## Architecture

```
v3/
├── skills/
│   ├── v3-generate-std/           # Phase 1: STP → STD transformation
│   ├── v3-explore-test-context/   # Phase 2: Repository exploration + GRAVEYARD review
│   ├── v3-generate-pytest/        # Phase 3: STD → pytest code (GRAVEYARD-aware)
│   ├── v3-graveyard-verify/       # Phase 4: Verify generated code against GRAVEYARD.md
│   ├── v3-pyright-heal/           # Phase 5: Universal Python type fixer
│   └── v3-test-heal/              # Phase 6: Runtime self-healing + GRAVEYARD update
├── orchestrator.md                # 6-phase workflow coordinator
├── run_experiment.sh              # Single experiment runner
└── run_all_experiments.sh         # All experiments runner
```

## Skills

### 1. `/v3-generate-std` - Test Description Generator
**Input**: STP (Software Test Plan) markdown file
**Output**: STD (Software Test Description) markdown file with detailed scenarios
**Reusability**: High

### 2. `/v3-explore-test-context` - Repository Pattern Discovery
**Input**: Repository root (current directory)
**Output**: Verbal summary of utilities, fixtures, conventions + GRAVEYARD lessons
**Process**: Explores docs/, libs/, utilities/, tests/, and **GRAVEYARD.md**
**Reusability**: Medium

### 3. `/v3-generate-pytest` - Test Code Generator
**Input**: STD file
**Output**: Draft pytest `.py` file
**Process**: Uses exploration findings + GRAVEYARD lessons to generate test code
**Reusability**: Medium

### 4. `/v3-graveyard-verify` - GRAVEYARD Verification
**Input**: Generated test file path
**Output**: Verified test file (in-place edits if violations found)
**Process**: Cross-references generated code against every GRAVEYARD.md entry, fixes known mistake patterns
**Reusability**: High

### 5. `/v3-pyright-heal` - Universal Python Validator
**Input**: Any Python file path
**Output**: Type-safe Python file (in-place edits)
**Reusability**: Very High

### 6. `/v3-test-heal` - Runtime Self-Healing
**Input**: Test file path
**Output**: Fixed test file (in-place) + updated GRAVEYARD.md
**Process**: Runs test via `../runtstqe`, analyzes failures, consults docs, fixes code, documents lessons
**Reusability**: High

## Workflow Diagram

```
STP (Software Test Plan)
    ↓
[/v3-generate-std] ──→ STD (Software Test Description)
    ↓
[/v3-explore-test-context] ──→ Repository exploration + GRAVEYARD lessons
    ↓                                    ↑
[/v3-generate-pytest] ──→ Code generation (avoids known mistakes)
    ↓
draft_test.py
    ↓
[/v3-graveyard-verify] ──→ Cross-reference against GRAVEYARD.md, fix violations
    ↓
verified_test.py
    ↓
[/v3-pyright-heal] ──→ Iterate until type-clean
    ↓
type_safe_test.py
    ↓
[/v3-test-heal] ──→ Run on cluster, fix failures, iterate
    ↓                    ↓
passing_test.py ✓    GRAVEYARD.md (lessons learned)
                         ↓
                    [fed back to future /v3-explore-test-context runs]
```

## The GRAVEYARD.md Feedback Loop

GRAVEYARD.md creates a learning loop across experiment runs:

```
Run 1: Generate test → fails → fix → document mistake in GRAVEYARD.md
Run 2: Read GRAVEYARD.md → avoid mistake → generate better test
Run 3: Read GRAVEYARD.md → avoid more mistakes → even better test
...
```

Each run benefits from all previous runs' lessons, creating cumulative improvement.

## Differences from V2.2

| Aspect | V2.2 | V3 |
|--------|------|----|
| **Phases** | 4 phases | 6 phases |
| **Skills** | 4 skills | 6 skills |
| **Runtime testing** | No | Yes - tests run on real cluster |
| **Self-healing** | Pyright only (static) | Pyright + runtime (dynamic) |
| **Learning** | None | GRAVEYARD.md feedback loop |
| **Exploration** | Repo patterns only | Repo patterns + past mistakes |
| **Code generation** | Pattern-aware | Pattern-aware + mistake-aware |
| **Pre-runtime verification** | None | GRAVEYARD.md cross-reference |

## Usage

### Automated Workflow (Orchestrator)
```bash
# Full end-to-end generation with runtime validation
./run_experiment.sh <stp_file> <experiment_name>
```

### Manual Workflow (Granular Control)
```bash
# Step 1: Generate test description
/v3-generate-std stps/3.md

# Step 2: Explore repository context + GRAVEYARD
/v3-explore-test-context

# Step 3: Generate pytest code
/v3-generate-pytest std_output.md

# Step 4: Verify against GRAVEYARD
/v3-graveyard-verify tests/test_new_feature.py

# Step 5: Validate types
/v3-pyright-heal tests/test_new_feature.py

# Step 6: Run test, fix, document
/v3-test-heal tests/test_new_feature.py
```

### Skill Reuse Examples
```bash
# Fix type errors in ANY Python file
/v3-pyright-heal utilities/storage_helper.py

# Generate STD for documentation (no code)
/v3-generate-std stps/5.md

# Run and heal any existing test
/v3-test-heal tests/existing/test_something.py
```

## Experimental Validation

Each experiment will:
1. Run the 6-phase orchestrator workflow
2. Compare success rate vs. v2.2
3. Measure how many GRAVEYARD violations are caught pre-runtime (Phase 4)
4. Measure how many runtime fixes are needed (Phase 6 iterations)
5. Track GRAVEYARD.md growth across experiments
6. Evaluate whether GRAVEYARD lessons reduce errors in later runs
