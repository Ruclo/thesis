# Skill: /generate-pytest

**Purpose**: Generate executable pytest code from Software Test Description (STD) and repository context

## Input
- **Required**: Path to STD markdown file
- **Optional**: `--output-dir` - target directory (default: infer from repository patterns)
- **Prerequisite**: Repository context should be examined via `/explore-test-context` first

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

2. USE repository context from memory
   - Recall available utilities from docs/ examination
   - Recall fixture patterns from test analysis
   - Recall import conventions observed
   - Recall naming conventions discovered
```

### Phase 2: Design Test Structure
```
1. MAP scenarios to test functions
   - test_scenario_1()
   - test_scenario_2()
   ...

2. IDENTIFY required fixtures
   - Based on scenario requirements
   - Match from observed fixture patterns

3. PLAN imports
   - Use observed common import patterns
   - Add scenario-specific imports
   - Include utilities discovered in repository

4. DESIGN test data
   - Extract from STD requirements
   - Use constants observed in codebase
```

### Phase 3: Generate Code
```
1. WRITE file header
   - Module docstring
   - Imports (from observed patterns)

2. WRITE test functions
   FOR each scenario in STD:
     - Function signature with fixtures
     - Docstring with scenario description
     - Precondition setup
     - Test execution
     - Assertion/validation
     - Cleanup (if needed)
     - Add pytest markers from observed conventions

3. WRITE helper functions (if needed)
   - Only if utility not found in repository
   - Mark as local helper
   - Use base Kubernetes client

4. APPLY conventions
   - Follow observed naming patterns
   - Use discovered marker conventions
   - Match observed file structure
```

### Phase 4: Validation
```
1. VERIFY all imports match observed patterns
2. VERIFY all fixtures are known from repository examination
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

# Imports based on observed patterns
{repository_imports}

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
- **MUST** only use utilities/classes/methods observed in repository
- If a helper is missing → implement locally using base Kubernetes client
- Never assume a method exists without verification

### 2. Pattern Fidelity
- **MUST** follow observed naming conventions
- **MUST** use fixtures as discovered in repository
- **MUST** match observed import patterns
- **MUST** place file according to observed file structure

### 3. STD Completeness
- **MUST** implement ALL scenarios from STD
- **MUST** cover ALL acceptance criteria
- **MUST** include ALL preconditions from STD
- **MUST** add test data from STD requirements

## Algorithm

```
1. PARSE std_file → scenarios[]
2. RECALL repository patterns → {utilities, fixtures, imports, conventions}

3. FOR each scenario in scenarios:
     a. EXTRACT requirements
     b. MAP to fixtures from observed patterns
     c. SELECT utilities from repository knowledge
     d. DESIGN test function

4. GENERATE imports (from observed patterns)
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
# First, examine repository context
/explore-test-context

# Then generate pytest from STD
/generate-pytest std_vm_reset.md

# Custom output directory
/generate-pytest std_feature.md --output-dir tests/custom/

# Output: tests/virt/lifecycle/test_vm_reset.py
```

## Error Handling

If repository context is not available:
```
ERROR: Repository patterns not examined
HINT: Run `/explore-test-context` first to understand repository conventions
```

If STD is malformed:
```
ERROR: Could not parse STD file
HINT: Ensure STD follows expected structure
```

If utility is not found in repository:
```
WARNING: Utility 'FooHelper' not found in repository
ACTION: Implementing locally using base Kubernetes client
```

## Reusability
**Medium-High** - Can be used for:
- Generating pytest tests from any STD
- Framework could be adapted for other test frameworks
- Pattern is reusable across different repos with similar structure

## Dependencies
- STD file (from `/generate-std` or manual)
- Repository context (from `/explore-test-context`)
- Read tool
- Write tool
