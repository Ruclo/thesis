# V2.1: Modular Skills with Inline Context Exploration

## Overview

V2.1 is an intermediate step between v1 and v2, introducing modular skills while keeping the context exploration inline (like v1). This version does NOT generate:
- STD (Software Test Description) as a separate artifact
- context.json file

## Architecture

```
v2.1/
├── skills/
│   ├── explore-test-context/  # Repository exploration (no context.json output)
│   ├── generate-pytest/       # STP → pytest code
│   └── pyright-heal/          # Universal Python type fixer
├── orchestrator.md            # 3-phase workflow coordinator
└── run_experiment.sh          # Experiment runner
```

## Skills

### 1. `/explore-test-context` - Repository Pattern Discovery
**Input**: Repository root (current directory)
**Output**: Verbal summary of utilities, fixtures, conventions (NO context.json file)
**Process**: Explores docs/, libs/, utilities/, tests/ and reports findings
**Reusability**: Medium - useful before generating any test

### 2. `/generate-pytest` - Test Code Generator
**Input**: STP (Software Test Plan) markdown file
**Output**: Draft pytest `.py` file
**Process**: Uses findings from exploration to generate test code
**Reusability**: Medium - specific to pytest generation

### 3. `/pyright-heal` - Universal Python Validator
**Input**: Any Python file path
**Output**: Type-safe Python file (in-place edits)
**Reusability**: **Very High** - works on tests, utilities, scripts, fixtures, etc.

## Workflow

### Automated Workflow
```bash
# Full end-to-end generation
./run_experiment.sh <stp_file> <experiment_name>
```

```
STP (Software Test Plan)
    ↓
[/explore-test-context] ──→ Repository exploration (verbal summary)
    ↓
[/generate-pytest] ──→ Code generation using exploration findings
    ↓
draft_test.py
    ↓
[/pyright-heal] ──→ Iterate until clean
    ↓
final_test.py ✓
```

## Differences from V1

| Aspect | V1 (Monolithic) | V2.1 (Modular) |
|--------|-----------------|----------------|
| **Structure** | Single prompt file | 3 independent skills + orchestrator |
| **Reusability** | None - one-shot workflow | Skills work independently |
| **Pyright Heal** | Embedded in prompt | Universal skill for ANY .py file |
| **Context Exploration** | Inline in main prompt | Separate skill (verbal output only) |
| **STD Support** | No | No |
| **context.json** | No | No |

## Differences from V2

| Aspect | V2.1 | V2 (Full) |
|--------|------|-----------|
| **STD Generation** | No - direct STP → code | Yes - STP → STD → code |
| **Context Caching** | No context.json | Yes - context.json artifact |
| **Context Exploration** | Verbal summary only | context.json artifact |
| **Skills** | 3 skills | 4 skills |
| **Workflow Phases** | 3 phases | 4 phases |
| **Flexibility** | Medium | High |

## Key Innovations over V1

### 1. Universal Pyright Healer
```bash
# Works on ANY Python code in the project
/pyright-heal utilities/new_helper.py
/pyright-heal conftest.py
/pyright-heal tests/fixtures/base.py
```

### 2. Modular Architecture
- Skills can be invoked independently
- Easier to maintain and improve
- Better separation of concerns

## Usage

### Automated Workflow (Orchestrator)
```bash
# Full end-to-end generation
./run_experiment.sh <stp_file> <experiment_name>
```

### Manual Workflow (Granular Control)
```bash
# Step 1: Explore repository context
/explore-test-context

# Step 2: Generate pytest code
/generate-pytest stps/3.md

# Step 3: Validate and heal
/pyright-heal tests/test_new_feature.py
```

### Skill Reuse Examples
```bash
# Fix type errors in ANY Python file
/pyright-heal utilities/storage_helper.py

# Generate test from STP
/generate-pytest stps/5.md
```

## Experimental Validation

Each experiment will:
1. Run the orchestrator workflow
2. Compare success rate vs. v1
3. Measure skill reusability
4. Track time/cost per phase
5. Validate pyright-heal effectiveness

## Next Steps (v2.2)

V2.2 will add:
- `/generate-std` skill for STP → STD transformation
- STD as intermediate artifact for review
- Still no context.json (exploration remains inline)
