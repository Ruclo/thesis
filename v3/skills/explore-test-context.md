# Skill: /explore-test-context

**Purpose**: Discover repository-specific testing patterns, utilities, fixtures, and conventions

## Input
- **Required**: Repository root (implicit - current working directory)

## Output
- **Direct Report**: Findings reported directly to the user
- **No file output**: Analysis is presented in the conversation, not written to disk

## Implementation

### Phase 1: Examine Documentation
```python
# Read all files in docs/ folder
- Look for testing guidelines
- Look for pytest configuration docs
- Look for fixture documentation
- Extract conventions and standards
```

### Phase 2: Analyze Test Patterns
```python
# Look at existing tests in tests/
- Find common import patterns
- Identify fixture usage patterns
- Note pytest markers and decorators
- Observe naming conventions
- Understand file organization
```

### Thoroughness
- Scan all documentation in docs/
- Review representative sample of test files
- Focus on patterns, not exhaustive enumeration
- Report findings conversationally

## Algorithm

```
1. READ all files in docs/ folder
   EXTRACT testing conventions, patterns, guidelines
2. GLOB tests/**/*.py
   ANALYZE patterns:
     - Common imports
     - Fixture usage
     - Test markers and decorators
     - Naming conventions
     - File structure patterns
3. REPORT findings directly to user
   SUMMARIZE observed patterns and conventions
```

## Output Example

```
Repository Testing Patterns Analysis:

Documentation Found:
- docs/testing_guidelines.md
- docs/pytest_markers.md

Common Import Patterns:
- from ocp_resources.virtual_machine import VirtualMachine
- from utilities.virt import VirtualMachineForTests
- pytest fixtures from conftest.py

Common Fixtures:
- namespace (function scope)
- admin_client (session scope)
- storage_class_matrix

Test Markers:
- @pytest.mark.polarion('CNV-XXXXX')
- @pytest.mark.tier1

Naming Convention:
- test_<feature>_<scenario>

File Structure:
- tests/<domain>/<feature>/test_*.py

Similar Test References:
- tests/storage/snapshots/test_snapshots.py:145
- tests/virt/lifecycle/test_reset.py:89
```

## Usage

```bash
# Explore repository context
/explore-test-context
```

## Constraints
- **Must not hallucinate**: Only report actual findings from files
- **Must verify**: Check that patterns actually exist in the repository
- **Focus on docs**: Prioritize examining documentation folder for conventions
- **Pattern-based**: Look for recurring patterns across test files

## Reusability
**High** - Can be used for:
- Understanding repository testing patterns before generating tests
- Quick analysis of testing conventions
- Discovering existing patterns without creating artifacts

## Dependencies
- Glob tool (file discovery)
- Grep tool (pattern searching)
- Read tool (file content)
