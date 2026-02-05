# Skill: /explore-test-context

**Purpose**: Discover repository-specific testing patterns, utilities, fixtures, and conventions

## Input
- **Required**: Repository root (implicit - current working directory)

## Output
- **File**: `context.json`
- **Format**: Structured JSON containing:
```json
{
  "utilities": {
    "classes": ["ClassName", ...],
    "methods": ["method_name", ...],
    "constants": ["CONSTANT_NAME", ...]
  },
  "fixtures": {
    "common": ["fixture_name", ...],
    "scopes": {"fixture_name": "scope"}
  },
  "imports": {
    "common_patterns": ["from ocp_resources import ...", ...]
  },
  "conventions": {
    "markers": ["@pytest.mark.polarion(...)", ...],
    "naming": "test_<feature>_<scenario>",
    "file_structure": "tests/<domain>/<feature>/test_*.py"
  },
  "precedents": {
    "similar_tests": ["path/to/test.py:line", ...]
  }
}
```

## Implementation

### Phase 1: Scan Documentation
```python
# Read docs/ for testing conventions
- docs/testing_guidelines.md
- docs/pytest_markers.md
- docs/fixture_usage.md
```

### Phase 2: Map Utilities
```python
# Analyze libs/ and utilities/
- Scan utilities/*.py for helper classes
- Extract method signatures
- Identify constants (TIMEOUT_*, DEFAULT_*, etc.)
- Map commonly used patterns
```

### Phase 3: Analyze Precedents
```python
# Look at existing tests in tests/
- Find similar test files (by domain)
- Extract import patterns
- Identify fixture usage patterns
- Note pytest markers and decorators
```

### Thoroughness
- Deep scan all docs
- Analyze all utilities
- Review 10+ existing tests
- Extract detailed signatures
- Map all fixtures

## Algorithm

```
1. READ docs/testing_guidelines.md
2. GLOB utilities/*.py
   FOR each utility_file:
     EXTRACT classes, methods, constants
3. GLOB tests/**/*.py
   FILTER by domain similarity
   FOR each test_file:
     EXTRACT imports, fixtures, markers
4. GENERATE context.json
5. WRITE context.json to disk
6. RETURN success
```

## Output Example

```json
{
  "utilities": {
    "classes": ["VirtualMachineForTests", "DataVolumeForTests"],
    "methods": ["wait_for_vm_running", "create_snapshot"],
    "constants": ["TIMEOUT_5MIN", "DEFAULT_STORAGE_CLASS"]
  },
  "fixtures": {
    "common": ["namespace", "admin_client", "storage_class_matrix"],
    "scopes": {
      "namespace": "function",
      "admin_client": "session"
    }
  },
  "imports": {
    "common_patterns": [
      "from ocp_resources.virtual_machine import VirtualMachine",
      "from utilities.virt import VirtualMachineForTests"
    ]
  },
  "conventions": {
    "markers": [
      "@pytest.mark.polarion('CNV-XXXXX')",
      "@pytest.mark.tier1"
    ],
    "naming": "test_<feature>_<scenario>",
    "file_structure": "tests/<domain>/<feature>/test_*.py"
  },
  "precedents": {
    "similar_tests": [
      "tests/storage/snapshots/test_snapshots.py:145",
      "tests/virt/lifecycle/test_reset.py:89"
    ]
  }
}
```

## Usage

```bash
# Explore repository context
/explore-test-context
```

## Constraints
- **Must not hallucinate**: Only report actual findings
- **Must verify**: Check that classes/methods actually exist
- **Cache-friendly**: Output must be JSON for easy reuse
- **Deterministic**: Same repo state = same output

## Reusability
**Very High** - Can be used for:
- Any test generation in this repository
- Manual test development (developers read context.json)
- CI/CD validation (ensure conventions are followed)
- Onboarding new developers (show patterns)

## Dependencies
- Glob tool (file discovery)
- Grep tool (pattern searching)
- Read tool (file content)
