# Skill: /v2-generate-pytest

**Purpose**: Generate executable pytest code from Software Test Description (STD) and repository context

## Input
- **Required**: Path to STD markdown file
- **Required**: Path to context.json (from `/v2-explore-test-context`)
- **Optional**: `--output-dir` - target directory (default: infer from context)

## Output
- **File**: `test_<feature_name>.py`
- **Location**: Determined by context conventions (e.g., `tests/<domain>/<feature>/`)
- **Format**: Executable pytest file with proper structure

## Implementation

### Phase 1: Parse Inputs
```
1. READ std_file
   - Extract test scenarios
   - Parse preconditions
   - Identify test data requirements
   - Extract acceptance criteria

2. READ context.json
   - Load available utilities
   - Load fixture patterns
   - Load import conventions
   - Load naming conventions
```

### Phase 2: Design Test Structure
```
1. MAP scenarios to test functions
   - test_scenario_1()
   - test_scenario_2()
   ...

2. IDENTIFY required fixtures
   - Based on scenario requirements
   - Match from context.fixtures

3. PLAN imports
   - Use context.imports.common_patterns
   - Add scenario-specific imports
   - Include utilities from context.utilities

4. DESIGN test data
   - Extract from STD requirements
   - Use context.constants where applicable
```

### Phase 3: Generate Code
```
1. WRITE file header
   - Module docstring
   - Imports (from context)

2. WRITE test functions
   FOR each scenario in STD:
     - Function signature with fixtures
     - Docstring with scenario description
     - Precondition setup
     - Test execution
     - Assertion/validation
     - Cleanup (if needed)
     - Add pytest markers from context.conventions

3. WRITE helper functions (if needed)
   - Only if utility missing in context
   - Mark as local helper
   - Use base Kubernetes client

4. APPLY conventions
   - Follow context.conventions.naming
   - Use context.conventions.markers
   - Match context.conventions.file_structure
```

### Phase 4: Validation
```
1. VERIFY all imports exist in context
2. VERIFY all fixtures exist in context
3. VERIFY no hallucinated utilities
4. VERIFY proper pytest structure
```

## Code Generation Template

```python
# -*- coding: utf-8 -*-

"""
{feature_name} Tests

{brief_description}

Based on: {std_file}
"""

import logging

import pytest

# Imports from context.json
{context_imports}

LOGGER = logging.getLogger(__name__)


{fixture_definitions_if_needed}


@pytest.mark.polarion("{polarion_id}")
@pytest.mark.{tier}
def test_{scenario_name}({fixtures}):
    """
    {scenario_description}

    Steps:
    {test_steps}

    Expected:
    {expected_outcome}
    """
    LOGGER.info(f"Starting test: {scenario_name}")

    # Preconditions
    {precondition_code}

    # Test execution
    {test_code}

    # Validation
    {assertion_code}

    # Cleanup (if needed)
    {cleanup_code}
```

## Strict Constraints

### 1. No Hallucination
- **MUST** only use utilities/classes/methods from `context.json`
- If a helper is missing → implement locally using base Kubernetes client
- Never assume a method exists without verification

### 2. Context Fidelity
- **MUST** follow `context.conventions.naming`
- **MUST** use `context.fixtures` as discovered
- **MUST** match `context.imports` patterns
- **MUST** place file in `context.conventions.file_structure`

### 3. STD Completeness
- **MUST** implement ALL scenarios from STD
- **MUST** cover ALL acceptance criteria
- **MUST** include ALL preconditions from STD
- **MUST** add test data from STD requirements

## Algorithm

```
1. PARSE std_file → scenarios[]
2. PARSE context.json → {utilities, fixtures, imports, conventions}

3. FOR each scenario in scenarios:
     a. EXTRACT requirements
     b. MAP to fixtures from context
     c. SELECT utilities from context
     d. DESIGN test function

4. GENERATE imports (from context.imports)
5. GENERATE test functions
6. VERIFY no hallucinated code
7. WRITE to output file
8. RETURN file path
```

## Output Example

Given STD with 2 scenarios:
```python
# -*- coding: utf-8 -*-

"""
VM Reset Tests

Tests for Force/Hard Reset functionality

Based on: std_vm_reset.md
"""

import logging

import pytest
from ocp_resources.virtual_machine import VirtualMachine
from utilities.virt import VirtualMachineForTests, wait_for_vm_running

LOGGER = logging.getLogger(__name__)


@pytest.mark.polarion("CNV-12345-01")
@pytest.mark.tier1
def test_reset_running_vmi_via_api(namespace, admin_client):
    """
    Reset running VMI via API and verify guest reboots

    Steps:
    1. Create and start VM
    2. Record boot time
    3. Call reset API
    4. Verify boot time changed

    Expected:
    - VM reboots without pod rescheduling
    - Boot time is updated
    """
    LOGGER.info("Creating VM for reset test")

    vm = VirtualMachineForTests(
        name="test-reset-vm",
        namespace=namespace.name,
        client=admin_client
    )
    vm.deploy(wait=True)
    wait_for_vm_running(vm)

    initial_boot_time = vm.instance.status.boot_time
    LOGGER.info(f"Initial boot time: {initial_boot_time}")

    LOGGER.info("Calling reset API")
    vm.instance.reset()

    wait_for_vm_running(vm)
    new_boot_time = vm.instance.status.boot_time

    assert new_boot_time != initial_boot_time, "Boot time should change after reset"
    LOGGER.info("Reset successful - boot time updated")


@pytest.mark.polarion("CNV-12345-02")
@pytest.mark.tier1
def test_reset_via_virtctl(namespace, admin_client):
    """
    Reset running VMI via virtctl command

    Steps:
    1. Create and start VM
    2. Execute virtctl reset command
    3. Verify VM reboots

    Expected:
    - virtctl reset succeeds
    - VM reboots successfully
    """
    # Implementation here...
```

## Usage

```bash
# Standard usage
/v2-generate-pytest std_vm_reset.md context.json

# Custom output directory
/v2-generate-pytest std_feature.md context.json --output-dir tests/custom/

# Output: tests/virt/lifecycle/test_vm_reset.py
```

## Error Handling

If context.json is missing/invalid:
```
ERROR: context.json not found or invalid
HINT: Run `/v2-explore-test-context` first to generate context
```

If STD is malformed:
```
ERROR: Could not parse STD file
HINT: Ensure STD follows expected structure
```

If utility is missing from context:
```
WARNING: Utility 'FooHelper' not found in context
ACTION: Implementing locally using base Kubernetes client
```

## Reusability
**Medium-High** - Can be used for:
- Generating pytest tests from any STD
- Framework could be adapted for other test frameworks
- Pattern is reusable across different repos with similar structure

## Dependencies
- STD file (from `/v2-generate-std` or manual)
- context.json (from `/v2-explore-test-context`)
- Read tool
- Write tool
