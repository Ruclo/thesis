# Software Test Description (STD)

## Feature: CPU Hotplug Logic - Maximum Limits Enforcement

**STP Reference:** `/thesis/stps/6.md`
**Jira ID:** CNV-57352 (Bug Fix), CNV-61263 (Feature)
**Generated:** 2026-02-10

---

## Summary

This STD covers tests for the CPU hotplug bug fix that ensures MaxSockets is properly limited based on maximum vCPUs. The bug (CNV-57352) allowed CPU hotplug to exceed maximum vCPU limits, causing unpredictable behavior. The fix limits MaxSockets calculation to prevent resource overcommit.

**Test Coverage:**
- MaxSockets calculation based on maximum vCPUs
- CPU hotplug cannot exceed limits
- VM behavior at maximum CPU
- Error handling when attempting to exceed limits

---

## Test Files

### File: `tests/virt/compute/test_cpu_hotplug_max_limits.py`

```python
"""
CPU Hotplug Maximum Limits Tests

STP Reference: /thesis/stps/6.md
Jira: CNV-57352, CNV-61263

This module contains tests for the CPU hotplug bug fix that ensures MaxSockets
is properly limited based on maximum vCPUs allowed, preventing resource overcommit
and unpredictable guest behavior.

PR Reference: https://github.com/kubevirt/kubevirt/pull/14511
"""

import pytest


class TestCPUHotplugMaxSockets:
    """
    Tests for MaxSockets calculation and CPU hotplug limits.

    Markers:
        - gating
        - tier1

    Preconditions:
        - OpenShift cluster with OpenShift Virtualization operator installed
        - CPU hotplug feature available
        - Cluster nodes with multiple CPUs available
    """

    def test_max_sockets_limited_by_max_vcpus(self):
        """
        Test that MaxSockets is calculated based on maximum vCPUs allowed.

        Steps:
            1. Create VirtualMachine with CPU hotplug enabled and specific max vCPUs (e.g., 8)
            2. Get the calculated MaxSockets from VM spec
            3. Verify MaxSockets value

        Expected:
            - MaxSockets is less than or equal to max vCPUs (8)
        """
        pass

    def test_max_sockets_with_different_max_vcpus(self):
        """
        Test MaxSockets calculation with various max vCPU configurations.

        Parametrize:
            - max_vcpus: [4, 8, 16, 32]

        Steps:
            1. Create VirtualMachine with CPU hotplug enabled and max_vcpus from parameter
            2. Get the calculated MaxSockets from VM spec
            3. Verify MaxSockets does not exceed max_vcpus

        Expected:
            - MaxSockets equals max_vcpus divided by cores and threads configuration
        """
        pass

    def test_cpu_hotplug_blocked_at_max_vcpus(self):
        """
        Test that CPU hotplug cannot exceed maximum vCPUs.

        Steps:
            1. Create VirtualMachine with CPU hotplug enabled, max vCPUs set to 8
            2. Start VM with 6 vCPUs
            3. Hotplug 2 additional CPUs (reaching max of 8)
            4. Attempt to hotplug 1 more CPU (would exceed max)
            5. Verify hotplug operation result

        Expected:
            - VM has 8 vCPUs after successful hotplug
            - Further hotplug attempt is blocked or fails gracefully
        """
        pass

    def test_error_message_when_exceeding_max_vcpus(self):
        """
        Test that attempting to exceed max vCPUs provides clear error message.

        Steps:
            1. Create VirtualMachine with CPU hotplug enabled, max vCPUs set to 4
            2. Start VM at max vCPUs (4)
            3. Attempt to hotplug additional CPU
            4. Capture error message or validation failure

        Expected:
            - Error message indicates max vCPU limit reached
        """
        pass


class TestCPUHotplugFullCycle:
    """
    End-to-end tests for CPU hotplug within limits.

    Markers:
        - tier2

    Preconditions:
        - OpenShift cluster with OpenShift Virtualization operator installed
        - CPU hotplug feature available
        - Guest OS supporting CPU hotplug (RHEL or Fedora)
    """

    def test_hotplug_from_min_to_max_vcpus(self):
        """
        Test full CPU hotplug cycle from minimum to maximum vCPUs.

        Steps:
            1. Create VirtualMachine with CPU hotplug enabled, initial vCPUs=2, max vCPUs=8
            2. Start VM and wait for running state
            3. Verify guest OS sees 2 CPUs
            4. Hotplug CPUs incrementally to reach max (8 total)
            5. Verify guest OS sees all 8 CPUs
            6. Attempt to hotplug beyond max
            7. Verify hotplug is blocked

        Expected:
            - Guest OS correctly sees all hotplugged CPUs up to max
            - No further hotplug allowed after reaching max vCPUs
        """
        pass

    def test_hotplug_respects_max_sockets_limit(self):
        """
        Test that CPU hotplug operations respect MaxSockets calculated limit.

        Steps:
            1. Create VirtualMachine with CPU hotplug enabled, specific CPU topology (sockets=2, cores=2, threads=1)
            2. Set max vCPUs to 8 (MaxSockets should be 2 based on topology)
            3. Start VM with initial 4 vCPUs (1 socket fully populated)
            4. Hotplug to add second socket (reaching 8 vCPUs)
            5. Verify VM has 8 vCPUs
            6. Attempt to add third socket
            7. Verify operation blocked

        Expected:
            - VM successfully hotplugs up to MaxSockets limit
            - Further socket addition is blocked
        """
        pass


class TestCPUHotplugGuestOSCompatibility:
    """
    Tests for CPU hotplug with different guest operating systems.

    Markers:
        - tier2

    Parametrize:
        - os_image: [rhel9, fedora]

    Preconditions:
        - OpenShift cluster with OpenShift Virtualization operator installed
        - CPU hotplug feature available
        - Guest OS images with CPU hotplug support
    """

    def test_cpu_hotplug_guest_os_detection(self):
        """
        Test that guest OS correctly detects hotplugged CPUs within limits.

        Parametrize:
            - os_image: [rhel9, fedora]

        Steps:
            1. Create VirtualMachine with CPU hotplug enabled using os_image from parameter
            2. Start VM with 2 vCPUs, max vCPUs=6
            3. Wait for VM to boot and SSH to be accessible
            4. Check CPU count from guest (should be 2)
            5. Hotplug 2 additional CPUs (total 4)
            6. Verify guest OS detects 4 CPUs
            7. Hotplug 2 more CPUs (reaching max of 6)
            8. Verify guest OS detects 6 CPUs

        Expected:
            - Guest OS correctly detects all hotplugged CPUs up to max limit
        """
        pass


class TestCPUHotplugNegative:
    """
    Negative tests for CPU hotplug maximum limits enforcement.

    Markers:
        - tier1

    Preconditions:
        - OpenShift cluster with OpenShift Virtualization operator installed
        - CPU hotplug feature available
    """

    def test_cannot_hotplug_beyond_max_vcpus_single_operation(self):
        """
        [NEGATIVE] Test that a single hotplug operation cannot exceed max vCPUs.

        Steps:
            1. Create VirtualMachine with CPU hotplug enabled, initial vCPUs=2, max vCPUs=4
            2. Start VM and wait for running state
            3. Attempt to hotplug 4 CPUs in one operation (would result in 6 total, exceeding max)
            4. Verify operation result

        Expected:
            - Hotplug operation fails or is rejected with validation error
        """
        pass

    def test_cannot_set_max_sockets_exceeding_max_vcpus(self):
        """
        [NEGATIVE] Test that MaxSockets cannot be manually set to exceed max vCPUs.

        Steps:
            1. Attempt to create VirtualMachine with max vCPUs=4 and manually specified MaxSockets=8
            2. Verify VM creation result

        Expected:
            - VM creation fails with validation error indicating MaxSockets exceeds max vCPUs
        """
        pass

    def test_hotplug_incrementally_blocked_at_max_vcpus(self):
        """
        [NEGATIVE] Test that incremental hotplug operations are blocked when reaching max vCPUs.

        Steps:
            1. Create VirtualMachine with CPU hotplug enabled, initial vCPUs=1, max vCPUs=4
            2. Start VM
            3. Hotplug 1 CPU (total 2)
            4. Hotplug 1 CPU (total 3)
            5. Hotplug 1 CPU (total 4, at max)
            6. Attempt to hotplug 1 more CPU (would exceed max)
            7. Verify last operation result

        Expected:
            - Final hotplug attempt fails with error indicating max vCPU limit reached
        """
        pass


class TestCPUHotplugExistingVMs:
    """
    Tests for CPU hotplug limits on existing VMs (backward compatibility).

    Markers:
        - tier2

    Preconditions:
        - OpenShift cluster with OpenShift Virtualization operator installed
        - Existing VMs created before MaxSockets fix
    """

    def test_existing_vm_keeps_original_max_sockets(self):
        """
        Test that existing VMs retain their original MaxSockets configuration.

        Steps:
            1. Verify existing VM spec contains MaxSockets value
            2. Check that MaxSockets has not been recalculated
            3. Verify VM can still use CPU hotplug with original limits

        Expected:
            - Existing VM MaxSockets value is unchanged
            - CPU hotplug respects original MaxSockets limit
        """
        pass

    def test_new_vm_uses_updated_max_sockets_calculation(self):
        """
        Test that newly created VMs use the updated MaxSockets calculation.

        Steps:
            1. Create new VirtualMachine with CPU hotplug enabled, max vCPUs=8
            2. Get calculated MaxSockets from VM spec
            3. Compare with expected value based on new calculation logic
            4. Verify MaxSockets is properly limited

        Expected:
            - MaxSockets is calculated using new logic (limited by max vCPUs)
            - MaxSockets does not exceed max vCPUs
        """
        pass
```

---

### File: `tests/virt/compute/conftest.py` (shared fixtures)

```python
"""
Shared fixtures for compute tests.

This conftest provides fixtures for CPU hotplug testing including
VMs with CPU hotplug enabled and various configurations.
"""

import pytest


@pytest.fixture(scope="function")
def vm_with_cpu_hotplug(namespace, unprivileged_client):
    """
    Running VM with CPU hotplug enabled.

    Yields:
        VirtualMachine: VM with CPU hotplug enabled, initial 2 vCPUs, max 8 vCPUs
    """
    pass


@pytest.fixture(scope="function")
def vm_at_max_vcpus(namespace, unprivileged_client):
    """
    Running VM already at maximum vCPU limit.

    Yields:
        VirtualMachine: VM with CPU hotplug enabled, at max vCPUs (4)
    """
    pass


@pytest.fixture(scope="function")
def vm_with_custom_cpu_topology(namespace, unprivileged_client, request):
    """
    Running VM with custom CPU topology for hotplug testing.

    Parametrize via request.param:
        {
            "sockets": int,
            "cores": int,
            "threads": int,
            "initial_vcpus": int,
            "max_vcpus": int
        }

    Yields:
        VirtualMachine: VM with specified CPU topology and hotplug enabled
    """
    pass
```

---

## Test Coverage Summary

| Test File                           | Test Class                          | Test Count | Priority | Tier  |
| ----------------------------------- | ----------------------------------- | ---------- | -------- | ----- |
| `test_cpu_hotplug_max_limits.py`    | `TestCPUHotplugMaxSockets`          | 4          | P0       | T1    |
| `test_cpu_hotplug_max_limits.py`    | `TestCPUHotplugFullCycle`           | 2          | P1       | T2    |
| `test_cpu_hotplug_max_limits.py`    | `TestCPUHotplugGuestOSCompatibility`| 1          | P1       | T2    |
| `test_cpu_hotplug_max_limits.py`    | `TestCPUHotplugNegative`            | 3          | P0       | T1    |
| `test_cpu_hotplug_max_limits.py`    | `TestCPUHotplugExistingVMs`         | 2          | P1       | T2    |
| **Total**                           |                                     | **12**     |          |       |

---

## Requirements Traceability

| Requirement ID | Test Method(s)                                    | Coverage |
| -------------- | ------------------------------------------------- | -------- |
| CNV-61263      | `test_max_sockets_limited_by_max_vcpus`           | ✓        |
| CNV-61263      | `test_max_sockets_with_different_max_vcpus`       | ✓        |
| CNV-61263      | `test_cpu_hotplug_blocked_at_max_vcpus`           | ✓        |
| CNV-61263      | `test_error_message_when_exceeding_max_vcpus`     | ✓        |
| CNV-61263      | `test_hotplug_from_min_to_max_vcpus`              | ✓        |
| CNV-61263      | `test_hotplug_respects_max_sockets_limit`         | ✓        |
| CNV-61263      | `test_cannot_hotplug_beyond_max_vcpus_single_operation` | ✓  |
| CNV-61263      | `test_cannot_set_max_sockets_exceeding_max_vcpus` | ✓        |

---

## Test Strategy Notes

### Functional Testing (Tier 1)
- **MaxSockets Calculation**: Verify MaxSockets is properly limited based on max vCPUs
- **Hotplug Blocking**: Ensure CPU hotplug operations cannot exceed max vCPUs
- **Error Handling**: Validate appropriate error messages when limits are violated
- **Negative Tests**: Verify various scenarios where hotplug should be blocked

### End-to-End Testing (Tier 2)
- **Full Hotplug Cycle**: Test complete workflow from minimum to maximum vCPUs
- **Guest OS Compatibility**: Verify CPU hotplug works correctly with RHEL and Fedora guests
- **Topology Constraints**: Test hotplug with various CPU topologies (sockets, cores, threads)
- **Backward Compatibility**: Ensure existing VMs retain their configuration

### Test Markers
- `gating`: Critical tests for CI/CD pipeline (P0 tests)
- `tier1`: Functional tests (fast, core functionality)
- `tier2`: E2E tests (more complex, time-consuming)

### Parametrization Strategy
- **max_vcpus**: Test with various maximum vCPU limits (4, 8, 16, 32)
- **os_image**: Test with different guest OS (rhel9, fedora)
- **CPU topology**: Test with different sockets/cores/threads configurations

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Preconditions, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented (gating, tier1, tier2)
- [x] Parametrization documented where needed
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/cpu_hotplug_max_limits/std_cnv_57352.md`
- [x] Shared fixtures included in conftest.py
- [x] Requirements traceability matrix included

---

## Implementation Notes

### Key Testing Patterns
1. **MaxSockets Verification**: Check VM spec for calculated MaxSockets value
2. **Hotplug Operations**: Use virtctl or API to hotplug CPUs
3. **Guest Verification**: SSH to guest and check `/proc/cpuinfo` or `lscpu`
4. **Error Validation**: Capture and verify error messages from failed operations

### Dependencies
- **libvirt**: Backend CPU hotplug support
- **QEMU**: Virtual CPU management
- **Guest OS**: Must support CPU hotplug (RHEL 9, Fedora)
- **virtctl**: CLI tool for VM operations

### Known Limitations
- CPU hotplug requires guest OS support (not all OS support it)
- Some guest OS may require specific kernel versions or modules
- MaxSockets limit applies only to new VMs created after fix
- Existing VMs retain their original MaxSockets configuration
