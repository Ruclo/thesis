# V2.2: Modular Skills with STD Generation

## Overview

V2.2 adds STD (Software Test Description) generation as an intermediate step between v2.1 and v2. This version:
- ✅ Generates STD as a separate artifact from STP
- ✅ Uses modular skills architecture
- ❌ Does NOT generate context.json (exploration remains inline)

## Architecture

```
v2.2/
├── skills/
│   ├── generate-std/          # STP → STD transformation
│   ├── explore-test-context/  # Repository exploration (no context.json output)
│   ├── generate-pytest/       # STD → pytest code
│   └── pyright-heal/          # Universal Python type fixer
├── orchestrator.md            # 4-phase workflow coordinator
└── run_experiment.sh          # Experiment runner
```

## Skills

### 1. `/generate-std` - Test Description Generator
**Input**: STP (Software Test Plan) markdown file
**Output**: STD (Software Test Description) markdown file with detailed scenarios
**Reusability**: High - useful for any test planning phase

### 2. `/explore-test-context` - Repository Pattern Discovery
**Input**: Repository root (current directory)
**Output**: Verbal summary of utilities, fixtures, conventions (NO context.json file)
**Process**: Explores docs/, libs/, utilities/, tests/ and reports findings
**Reusability**: Medium - useful before generating any test

### 3. `/generate-pytest` - Test Code Generator
**Input**: STD file
**Output**: Draft pytest `.py` file
**Process**: Uses findings from exploration to generate test code
**Reusability**: Medium - specific to pytest generation

### 4. `/pyright-heal` - Universal Python Validator
**Input**: Any Python file path
**Output**: Type-safe Python file (in-place edits)
**Reusability**: **Very High** - works on tests, utilities, scripts, fixtures, etc.

## Workflow Modes

### Mode 1: Full Automated (Default)
Execute complete STP → pytest pipeline without user intervention.

### Mode 2: Interactive Review
Pause for user review at STD generation phase.

## Workflow Diagram

```
STP (Software Test Plan)
    ↓
[/generate-std] ──→ STD (Software Test Description)
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

## Differences from V2.1

| Aspect | V2.1 | V2.2 |
|--------|------|------|
| **STD Generation** | No - direct STP → code | Yes - STP → STD → code |
| **Skills** | 3 skills | 4 skills |
| **Workflow Phases** | 3 phases | 4 phases |
| **STD Review** | Not possible | Can review/edit STD before code gen |
| **Flexibility** | Medium | Higher |

## Differences from V2 (Full)

| Aspect | V2.2 | V2 (Full) |
|--------|------|-----------|
| **STD Generation** | Yes | Yes |
| **Context Caching** | No context.json | Yes - context.json artifact |
| **Context Exploration** | Separate skill (verbal output) | Separate skill (context.json output) |
| **Skills** | 4 skills | 4 skills |
| **Workflow Phases** | 4 phases | 4 phases |
| **Context Reuse** | No - explores each time | Yes - cache context.json |

## Key Innovations

### 1. STD as Intermediate Artifact
- Review test design before implementation
- Version control test descriptions
- Share STDs with manual testers
- Generate STDs for documentation purposes

### 2. Universal Pyright Healer
```bash
# Works on ANY Python code in the project
/pyright-heal utilities/new_helper.py
/pyright-heal conftest.py
/pyright-heal tests/fixtures/base.py
```

### 3. Interactive Review Mode
- Pause for STD review
- Edit STD before code generation
- Ensures test design alignment

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

# Step 3: Explore repository context
/explore-test-context

# Step 4: Generate pytest code
/generate-pytest std_output.md

# Step 5: Validate and heal
/pyright-heal tests/test_new_feature.py
```

### Skill Reuse Examples
```bash
# Fix type errors in ANY Python file
/pyright-heal utilities/storage_helper.py

# Generate STD for documentation (no code)
/generate-std stps/5.md

# Generate test from existing STD
/generate-pytest existing_std.md
```

## Experimental Validation

Each experiment will:
1. Run the orchestrator workflow
2. Compare success rate vs. v2.1
3. Measure STD quality and usefulness
4. Track time/cost per phase
5. Validate pyright-heal effectiveness

## Benefits of STD Generation

1. **Early Design Review**: Catch design issues before coding
2. **Clear Contracts**: STD serves as clear specification
3. **Reduced Rework**: Design validation happens early
4. **Better Documentation**: Always have test descriptions
5. **Planning Aid**: Create STDs during sprint planning

## Next Steps (v2 Full)

V2 (full) will add:
- `/explore-test-context` skill for context discovery
- context.json as reusable artifact
- Context caching for efficiency
- 4-phase workflow
