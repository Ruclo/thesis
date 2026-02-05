# V2: Modular Skills-Based Test Generation Architecture

## Overview

V2 refactors the monolithic v1 prompt into composable, reusable skills with a general orchestrator. This enables:

- **Reusability**: Skills like `/pyright-heal` work on ANY Python file
- **Flexibility**: Compose workflows manually or use orchestrator
- **Maintainability**: Improve skills independently
- **Testability**: Test individual components

## Architecture

```
v2/
├── skills/                    # Individual atomic skills
│   ├── generate-std.md       # STP → STD transformation
│   ├── explore-test-context.md   # Discover repo patterns
│   ├── generate-pytest.md    # STD + context → pytest code
│   └── pyright-heal.md       # Universal Python type fixer
├── orchestrator.md           # Workflow coordinator
└── run_experiment.sh         # Experiment runner
```

## Skills

### 1. `/generate-std` - Test Description Generator
**Input**: STP (Software Test Plan) markdown file
**Output**: STD (Software Test Description) markdown file with detailed scenarios
**Reusability**: High - useful for any test planning phase

### 2. `/explore-test-context` - Context Discovery
**Input**: Repository root (implicit), optional mode flag
**Output**: JSON context file with utilities, fixtures, patterns
**Reusability**: High - useful before writing ANY test

### 3. `/generate-pytest` - Test Code Generator
**Input**: STD file + context JSON
**Output**: Draft pytest `.py` file
**Reusability**: Medium - specific to pytest but framework-agnostic

### 4. `/pyright-heal` - Universal Python Validator
**Input**: Any Python file path
**Output**: Type-safe Python file (in-place edits)
**Reusability**: **Very High** - works on tests, utilities, scripts, fixtures, etc.

## Usage

### Automated Workflow (Orchestrator)
```bash
# Full end-to-end generation
./run_experiment.sh <stp_file> <experiment_name>
```

### Manual Workflow (Granular Control)
```bash
# Step 1: Generate test description
/generate-std stps/3.md

# Step 2: Review STD, edit if needed
vim std_output.md

# Step 3: Explore context
/explore-test-context --mode thorough

# Step 4: Generate pytest code
/generate-pytest std_output.md context.json

# Step 5: Validate and heal
/pyright-heal tests/test_new_feature.py
```

### Skill Reuse Examples
```bash
# Fix type errors in ANY Python file
/pyright-heal utilities/storage_helper.py

# Explore context without generating code
/explore-test-context --mode quick

# Generate STD for manual testing (no code)
/generate-std stps/5.md
```

## Workflow Diagram

```
STP (Software Test Plan)
    ↓
[/generate-std] ──→ STD (Software Test Description)
                     ↓
              ┌──────┴──────┐
              ↓             ↓
    [/explore-test-context] STD
              ↓             ↓
          context.json ─────┘
              ↓
    [/generate-pytest]
              ↓
    draft_test.py
              ↓
    [/pyright-heal] ──→ Iterate until clean
              ↓
    final_test.py ✓
```

## Differences from V1

| Aspect | V1 (Monolithic) | V2 (Modular) |
|--------|-----------------|--------------|
| **Structure** | Single 24-line prompt | 4 independent skills + orchestrator |
| **Reusability** | None - one-shot workflow | High - skills work independently |
| **Flexibility** | Fixed 3-phase sequence | Composable workflows |
| **STD Support** | No | Yes - `/generate-std` skill |
| **Pyright Heal** | Embedded in prompt | Universal skill for ANY .py file |
| **Context Caching** | No | Yes - `context.json` can be reused |
| **Manual Control** | Limited | Full - run any skill independently |

## Key Innovations

### 1. Context Caching
```bash
# Explore once, generate many tests
/explore-test-context --mode thorough > context.json
/generate-pytest std_test1.md context.json
/generate-pytest std_test2.md context.json  # Reuses context!
```

### 2. Universal Pyright Healer
```bash
# Works on ANY Python code in the project
/pyright-heal utilities/new_helper.py
/pyright-heal conftest.py
/pyright-heal tests/fixtures/base.py
```

### 3. STD as Intermediate Artifact
- Review test design before implementation
- Version control test descriptions
- Share STDs with manual testers
- Generate STDs for documentation purposes

## Experimental Validation

Each experiment will:
1. Run the orchestrator workflow
2. Compare success rate vs. v1
3. Measure skill reusability
4. Track time/cost per phase
5. Validate pyright-heal effectiveness

## Future Extensions

- `/validate-test` - Run pytest --collect-only
- `/generate-test-data` - Create mocks/fixtures
- `/explore-fixtures` - Specialized fixture discovery
- `/refactor-test` - Improve existing tests
