# Version Progression: v1 → v2.1 → v2.2 → v2

## Overview

This document explains the incremental progression from the monolithic v1 approach to the fully modular v2 architecture.

## Evolution Timeline

```
v1 (Monolithic)
    ↓
v2.1 (Modular Skills, Inline Exploration)
    ↓
v2.2 (+ STD Generation)
    ↓
v2 (+ Context Caching)
```

## Detailed Comparison

| Feature | v1 | v2.1 | v2.2 | v2 |
|---------|-----|------|------|-----|
| **Architecture** | Monolithic | Modular | Modular | Modular |
| **Skills** | - | 3 | 4 | 4 |
| **STD Generation** | ❌ | ❌ | ✅ | ✅ |
| **Context Exploration** | Inline | Separate Skill (verbal) | Separate Skill (verbal) | Separate Skill (context.json) |
| **context.json** | ❌ | ❌ | ❌ | ✅ |
| **Context Caching** | ❌ | ❌ | ❌ | ✅ |
| **Pyright Healing** | Embedded | Skill | Skill | Skill |
| **Workflow Phases** | 3 | 3 | 4 | 4 |
| **Reusability** | Low | Medium | Medium-High | High |
| **Flexibility** | Low | Medium | Medium-High | High |

## Version Details

### V1: Monolithic Prompt

**Structure:**
- Single `prompt.md` file
- All instructions in one place

**Workflow:**
```
STP → [Context Exploration → Code Generation → Pyright Loop] → test.py
```

**Phases:**
1. Context Exploration (inline)
2. Code Generation
3. Validation & Self-Healing

**Limitations:**
- No reusability
- No intermediate artifacts
- Fixed workflow
- Pyright healing embedded

---

### V2.1: Modular Skills with Exploration Skill (No Caching)

**Structure:**
- 3 independent skills
- Orchestrator coordinator

**Skills:**
1. `/explore-test-context` - Repository exploration (verbal summary, no context.json)
2. `/generate-pytest` - STP → pytest
3. `/pyright-heal` - Universal Python fixer

**Workflow:**
```
STP → [/explore-test-context] → (verbal) → [/generate-pytest] → draft_test.py → [/pyright-heal] → final_test.py
```

**Phases:**
1. Repository Exploration (verbal summary)
2. Pytest Code Generation
3. Pyright Validation

**Improvements over v1:**
- ✅ Modular architecture
- ✅ Separate exploration skill (clearer workflow)
- ✅ Universal pyright-heal skill (works on ANY .py file)
- ✅ Skills can be invoked independently
- ✅ Better separation of concerns

**Still lacks:**
- ❌ STD generation
- ❌ Context caching (exploration results not saved)

---

### V2.2: Adding STD Generation

**Structure:**
- 4 independent skills
- Orchestrator coordinator

**Skills:**
1. `/generate-std` - STP → STD
2. `/explore-test-context` - Repository exploration (verbal summary, no context.json)
3. `/generate-pytest` - STD → pytest
4. `/pyright-heal` - Universal Python fixer

**Workflow:**
```
STP → [/generate-std] → STD → [/explore-test-context] → (verbal) → [/generate-pytest] → draft_test.py → [/pyright-heal] → final_test.py
```

**Phases:**
1. STD Generation
2. Repository Exploration (verbal summary)
3. Pytest Code Generation
4. Pyright Validation

**Improvements over v2.1:**
- ✅ STD as intermediate artifact
- ✅ Review test design before coding
- ✅ Interactive mode (review STD)
- ✅ STD useful for documentation/manual testing

**Still lacks:**
- ❌ Context caching (exploration results not saved to context.json)

---

### V2: Full Modular Architecture with Context Caching

**Structure:**
- 4 independent skills
- Orchestrator coordinator

**Skills:**
1. `/generate-std` - STP → STD
2. `/explore-test-context` - Repo exploration → context.json
3. `/generate-pytest` - STD + context.json → pytest
4. `/pyright-heal` - Universal Python fixer

**Workflow:**
```
STP → [/generate-std] → STD
         ↓
    [/explore-test-context] → context.json
         ↓
    [/generate-pytest] ← (STD + context.json) → draft_test.py
         ↓
    [/pyright-heal] → final_test.py
```

**Phases:**
1. STD Generation
2. Context Exploration
3. Pytest Code Generation
4. Pyright Validation

**Improvements over v2.2:**
- ✅ Context caching (exploration results saved to context.json)
- ✅ Context exploration skill outputs reusable artifact
- ✅ Maximum reusability
- ✅ Can explore context once, use many times
- ✅ Can generate multiple tests from same context without re-exploring

**Full benefits:**
- ✅ All skills are independent and reusable
- ✅ Highest flexibility
- ✅ Best for multiple test generation workflows
- ✅ Context can be explored once, used many times

## Incremental Benefits

### Why v2.1 before v2.2?

**v2.1** introduces:
- Modular skills architecture
- Separate exploration skill (clearer workflow phases)
- Universal pyright-heal skill
- Skills that work independently

This is a foundational change that enables all future improvements while keeping the workflow simple.

### Why v2.2 before v2?

**v2.2** adds:
- STD generation as intermediate artifact
- Ability to review test design before coding
- Clearer separation between test description and implementation

This validates that STD generation is valuable before adding the complexity of context caching.

### Why v2 as final step?

**v2** completes the modularity by:
- Enhancing context exploration skill to output context.json
- Enabling context caching for efficiency (explore once, use many times)
- Maximizing reusability across all phases

## Use Case Recommendations

### Use v1 when:
- Simple one-off test generation
- No need for reusability
- Legacy compatibility

### Use v2.1 when:
- Want modular skills with clear phases
- Need universal pyright-heal
- Don't need STD artifact
- Don't need context caching
- Single test generation per run

### Use v2.2 when:
- Want STD for review/documentation
- Need interactive design review
- Want modular workflow with all phases separate
- Don't need context caching (re-exploring is acceptable)
- Single test generation per run

### Use v2 (full) when:
- Generating multiple tests
- Want to cache context for efficiency
- Need maximum flexibility
- Want all skills to be fully independent

## Migration Path

```
Current: v1 monolithic approach
    ↓
Step 1: Migrate to v2.1 (modular, inline exploration)
    - Validate: Skills work independently
    - Validate: Pyright-heal is reusable
    ↓
Step 2: Migrate to v2.2 (add STD generation)
    - Validate: STD is useful for review
    - Validate: Interactive mode works
    ↓
Step 3: Migrate to v2 (add context caching)
    - Validate: Context caching improves efficiency
    - Validate: Context exploration skill is reusable
```

## Experimentation Strategy

### Hypothesis Testing

**v1 → v2.1:**
- Does modular architecture improve maintainability?
- Does separating exploration into its own skill clarify the workflow?
- Is pyright-heal reusable across different files?

**v2.1 → v2.2:**
- Does STD generation improve test quality?
- Is reviewing STD before coding valuable?
- Does STD serve as useful documentation?
- Does the 4-phase workflow provide better control?

**v2.2 → v2:**
- Does context caching (context.json) improve efficiency?
- Is context.json artifact reusable for multiple test generations?
- Can we generate multiple tests from one context without re-exploring?
- What is the time/cost savings from caching?

### Metrics to Track

| Metric | v1 | v2.1 | v2.2 | v2 |
|--------|-----|------|------|-----|
| **Success Rate** | X% | ? | ? | ? |
| **Code Quality** | X | ? | ? | ? |
| **Time to Generate** | Xt | ? | ? | ? |
| **Context Reads** | N | N | N | 1 (cached) |
| **Modularity Score** | Low | Med | Med-High | High |
| **Reusability Score** | 0 | 1 | 2 | 4 |

## Conclusion

The incremental progression v1 → v2.1 → v2.2 → v2 allows for:
1. **Gradual validation** of each new capability
2. **Clear comparison** of benefits at each stage
3. **Risk reduction** by not changing everything at once
4. **Better understanding** of which features provide value

Each version builds on the previous one, adding one or two key features that can be independently validated.
