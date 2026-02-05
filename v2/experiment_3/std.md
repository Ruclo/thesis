# Software Test Description (STD)

## Feature: Force/Hard VM Reset

**STP Reference:** [VIRTSTRAT-357: Hard VM Reset](https://issues.redhat.com/browse/VIRTSTRAT-357)
**Jira ID:** VIRTSTRAT-357
**Generated:** 2026-02-03

---

## Summary

This STD covers comprehensive testing for the Force/Hard Reset feature for VirtualMachineInstance objects in OpenShift Virtualization. The tests validate the reset subresource API, virtctl command integration, RBAC enforcement, and proper error handling for edge cases. All tests are designed to verify that VM reset functionality works as expected without requiring pod rescheduling, preserving VMI UID and pod assignment while providing an immediate recovery path for hung guests.

**Coverage:**
- VMI Reset API endpoint functionality
- virtctl reset command integration
- RBAC permission enforcement
- Error handling for non-running VMIs
- VMI UID preservation across resets
- Guest reboot verification via boot time tracking
- Paused VMI reset behavior

---

## Test Files

### File: `tests/virt/lifecycle/test_vm_reset_api.py`

```python
"""
VirtualMachineInstance Reset API Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains tests for the VMI reset subresource API endpoint
(/virtualmachineinstances/{name}/reset) and validates core reset functionality
including guest reboots, UID preservation, and proper integration with
virt-handler and virt-launcher components.
"""

import pytest


class TestVMIResetAPI:
    """
    Tests for VMI reset via subresource API.

    Markers:
        - gating

    Preconditions:
        - CNV deployment with reset subresource support
        - Test cluster meets minimum environment requirements (3-node cluster)
        - Running VirtualMachineInstance with Alpine Linux
        - VMI is SSH accessible
        - Boot time tracking enabled in the guest
    """

    def test_reset_running_vmi_via_api(self):
        """
        Test that a running VMI can be reset via the subresource API and guest reboots.

        Related: TS-01, AC-1, AC-2, AC-3

        Steps:
            1. Record current boot time from the running VMI
            2. Issue PUT request to /virtualmachineinstances/{name}/reset
            3. Wait for VMI to become accessible again
            4. Record new boot time from the VMI

        Expected:
            - Reset API call succeeds with HTTP 200
            - VMI remains in Running state
            - Boot time is different (guest rebooted)
            - VMI is SSH accessible after reset
        """
        pass

    def test_vmi_uid_unchanged_after_reset(self):
        """
        Test that VMI UID remains unchanged after reset operation.

        Related: TS-03, AC-2

        Steps:
            1. Record VMI UID before reset
            2. Issue PUT request to /virtualmachineinstances/{name}/reset
            3. Wait for reset to complete
            4. Retrieve VMI UID after reset

        Expected:
            - VMI UID before reset equals VMI UID after reset
        """
        pass

    def test_pod_not_rescheduled_after_reset(self):
        """
        Test that the virt-launcher pod is not rescheduled during reset.

        Related: AC-2

        Steps:
            1. Record virt-launcher pod name and UID before reset
            2. Issue PUT request to /virtualmachineinstances/{name}/reset
            3. Wait for reset to complete
            4. Retrieve virt-launcher pod name and UID after reset

        Expected:
            - Pod name before reset equals pod name after reset
            - Pod UID before reset equals pod UID after reset
        """
        pass

    def test_boot_time_changes_after_reset(self):
        """
        Test that the guest OS boot time changes after reset, confirming actual reboot.

        Related: TS-11, AC-1

        Steps:
            1. Execute 'uptime -s' command on the VMI to get boot time
            2. Issue PUT request to /virtualmachineinstances/{name}/reset
            3. Wait for VMI to become accessible
            4. Execute 'uptime -s' command again on the VMI

        Expected:
            - Boot time after reset is different from boot time before reset
            - Time difference indicates recent reboot
        """
        pass


class TestVMIResetAPIErrorHandling:
    """
    Tests for VMI reset API error handling.

    Markers:
        - gating

    Preconditions:
        - CNV deployment with reset subresource support
    """

    def test_reset_fails_on_stopped_vmi(self):
        """
        [NEGATIVE] Test that reset fails appropriately on a stopped VMI.

        Related: TS-05, AC-6, KL-01

        Preconditions:
            - VirtualMachineInstance exists in Stopped state

        Steps:
            1. Issue PUT request to /virtualmachineinstances/{name}/reset

        Expected:
            - Reset API call fails with appropriate HTTP error code (4xx)
            - Error message indicates VMI is not running
        """
        pass

    def test_reset_fails_on_nonexistent_vmi(self):
        """
        [NEGATIVE] Test that reset fails gracefully on non-existent VMI.

        Related: TS-06, AC-6

        Steps:
            1. Issue PUT request to /virtualmachineinstances/nonexistent-vmi/reset

        Expected:
            - Reset API call fails with HTTP 404
            - Error message indicates VMI not found
        """
        pass

    def test_reset_on_paused_vmi(self):
        """
        [NEGATIVE] Test reset behavior on a paused VMI.

        Related: TS-12, AC-6, KL-01

        Preconditions:
            - Running VirtualMachineInstance
            - VMI is paused via pause subresource

        Steps:
            1. Issue PUT request to /virtualmachineinstances/{name}/reset

        Expected:
            - Reset API call fails with appropriate HTTP error code
            - Error message indicates VMI is paused
        """
        pass
```

---

### File: `tests/virt/lifecycle/test_vm_reset_virtctl.py`

```python
"""
VirtualMachineInstance Reset via virtctl Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains tests for the 'virtctl reset' command functionality,
validating the CLI user experience and proper integration with the reset
subresource API.
"""

import pytest


class TestVirtctlReset:
    """
    Tests for VMI reset via virtctl command.

    Markers:
        - gating

    Preconditions:
        - virtctl binary includes reset command
        - CNV deployment with reset subresource support
        - Running VirtualMachineInstance with Fedora
        - VMI is SSH accessible
    """

    def test_virtctl_reset_running_vmi(self):
        """
        Test that 'virtctl reset' command successfully resets a running VMI.

        Related: TS-02, AC-1, AC-4

        Steps:
            1. Record current boot time from the running VMI
            2. Execute 'virtctl reset <vmi-name>' command
            3. Wait for command completion
            4. Wait for VMI to become accessible
            5. Record new boot time from the VMI

        Expected:
            - virtctl reset command exits with code 0
            - Command output confirms reset initiated
            - Boot time is different (guest rebooted)
            - VMI is SSH accessible after reset
        """
        pass

    def test_virtctl_reset_with_namespace_flag(self):
        """
        Test that 'virtctl reset' works with --namespace flag.

        Related: AC-4

        Preconditions:
            - VirtualMachineInstance running in custom namespace

        Steps:
            1. Execute 'virtctl reset <vmi-name> --namespace <custom-ns>' command
            2. Wait for command completion

        Expected:
            - virtctl reset command exits with code 0
            - VMI in custom namespace is reset successfully
        """
        pass

    def test_virtctl_reset_nonexistent_vmi(self):
        """
        [NEGATIVE] Test that 'virtctl reset' fails gracefully on non-existent VMI.

        Related: TS-06, AC-6

        Steps:
            1. Execute 'virtctl reset nonexistent-vmi' command

        Expected:
            - virtctl reset command exits with non-zero code
            - Error message indicates VMI not found
        """
        pass

    def test_virtctl_reset_stopped_vmi(self):
        """
        [NEGATIVE] Test that 'virtctl reset' fails appropriately on stopped VMI.

        Related: TS-05, AC-6

        Preconditions:
            - VirtualMachineInstance exists in Stopped state

        Steps:
            1. Execute 'virtctl reset <vmi-name>' command

        Expected:
            - virtctl reset command exits with non-zero code
            - Error message indicates VMI is not running
        """
        pass
```

---

### File: `tests/virt/lifecycle/test_vm_reset_rbac.py`

```python
"""
VirtualMachineInstance Reset RBAC Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains tests for RBAC permission enforcement on the VMI reset
subresource, validating that appropriate permissions are required and enforced
for reset operations.
"""

import pytest


class TestVMIResetRBAC:
    """
    Tests for VMI reset RBAC permissions.

    Markers:
        - gating

    Preconditions:
        - CNV deployment with reset subresource support
        - RBAC manifests include virtualmachineinstances/reset permissions
        - Running VirtualMachineInstance
    """

    def test_user_with_edit_role_can_reset(self):
        """
        Test that a user with 'edit' role can reset a VMI in their namespace.

        Related: TS-04, AC-5

        Preconditions:
            - Test user with 'edit' ClusterRole binding in test namespace
            - User has valid kubeconfig

        Steps:
            1. Switch to test user context
            2. Issue PUT request to /virtualmachineinstances/{name}/reset
            3. Restore admin context

        Expected:
            - Reset API call succeeds with HTTP 200
            - VMI reset operation completes successfully
        """
        pass

    def test_user_with_admin_role_can_reset(self):
        """
        Test that a user with 'admin' role can reset a VMI.

        Related: AC-5

        Preconditions:
            - Test user with 'admin' ClusterRole binding in test namespace
            - User has valid kubeconfig

        Steps:
            1. Switch to test user context
            2. Issue PUT request to /virtualmachineinstances/{name}/reset
            3. Restore admin context

        Expected:
            - Reset API call succeeds with HTTP 200
            - VMI reset operation completes successfully
        """
        pass

    def test_user_with_view_role_cannot_reset(self):
        """
        [NEGATIVE] Test that a user with only 'view' role cannot reset a VMI.

        Related: TS-04, AC-5

        Preconditions:
            - Test user with 'view' ClusterRole binding in test namespace
            - User has valid kubeconfig

        Steps:
            1. Switch to test user context
            2. Attempt to issue PUT request to /virtualmachineinstances/{name}/reset
            3. Restore admin context

        Expected:
            - Reset API call fails with HTTP 403 Forbidden
            - Error message indicates insufficient permissions
        """
        pass

    def test_user_without_reset_permission_cannot_reset(self):
        """
        [NEGATIVE] Test that a user without virtualmachineinstances/reset permission cannot reset.

        Related: AC-5

        Preconditions:
            - Custom role with VMI read/write but NOT reset permission
            - Test user with custom role binding
            - User has valid kubeconfig

        Steps:
            1. Switch to test user context
            2. Attempt to issue PUT request to /virtualmachineinstances/{name}/reset
            3. Restore admin context

        Expected:
            - Reset API call fails with HTTP 403 Forbidden
            - Error message indicates missing virtualmachineinstances/reset permission
        """
        pass

    def test_reset_permission_in_admin_clusterrole(self):
        """
        Test that the 'admin' ClusterRole includes virtualmachineinstances/reset permission.

        Related: AC-5

        Steps:
            1. Retrieve 'admin' ClusterRole definition
            2. Check rules for virtualmachineinstances/reset verb

        Expected:
            - ClusterRole contains rule with resource 'virtualmachineinstances/reset'
            - Verb 'update' or '*' is present for the resource
        """
        pass

    def test_reset_permission_in_edit_clusterrole(self):
        """
        Test that the 'edit' ClusterRole includes virtualmachineinstances/reset permission.

        Related: AC-5

        Steps:
            1. Retrieve 'edit' ClusterRole definition
            2. Check rules for virtualmachineinstances/reset verb

        Expected:
            - ClusterRole contains rule with resource 'virtualmachineinstances/reset'
            - Verb 'update' or '*' is present for the resource
        """
        pass
```

---

### File: `tests/virt/lifecycle/test_vm_reset_integration.py`

```python
"""
VirtualMachineInstance Reset Integration Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains end-to-end integration tests for VMI reset functionality,
validating the complete flow across virt-api, virt-handler, virt-launcher,
and libvirt components.
"""

import pytest


class TestVMIResetIntegration:
    """
    Tests for end-to-end VMI reset integration.

    Markers:
        - gating

    Parametrize:
        - guest_os: [alpine, rhel9]

    Preconditions:
        - CNV deployment with reset subresource support
        - Storage class supporting RWO PVCs available
        - Running VirtualMachineInstance with parametrized guest OS
        - VMI is SSH accessible
        - Guest supports ACPI reset signal
    """

    def test_reset_preserves_disk_data(self):
        """
        Test that VMI reset preserves data on persistent disks.

        Related: G-06

        Preconditions:
            - VMI has persistent data volume mounted
            - Test file written to persistent storage

        Steps:
            1. Write unique content to file on persistent disk
            2. Issue PUT request to /virtualmachineinstances/{name}/reset
            3. Wait for VMI to become accessible
            4. Read file content from persistent disk

        Expected:
            - File content after reset equals content written before reset
        """
        pass

    def test_reset_clears_memory_state(self):
        """
        Test that VMI reset clears in-memory data.

        Related: KL-02

        Preconditions:
            - VMI has tmpfs or ramdisk mounted

        Steps:
            1. Write unique content to tmpfs/ramdisk
            2. Issue PUT request to /virtualmachineinstances/{name}/reset
            3. Wait for VMI to become accessible
            4. Check if tmpfs/ramdisk file exists

        Expected:
            - File in tmpfs/ramdisk does NOT exist after reset
        """
        pass

    def test_reset_updates_vmi_status_phase(self):
        """
        Test that VMI status is updated correctly during reset.

        Steps:
            1. Record initial VMI status phase
            2. Issue PUT request to /virtualmachineinstances/{name}/reset
            3. Monitor VMI status during reset operation
            4. Wait for reset completion

        Expected:
            - VMI status remains Running throughout reset
            - No transition to Stopped or Pending phase
        """
        pass

    def test_reset_triggers_guest_acpi_reset(self):
        """
        Test that reset operation triggers ACPI reset signal to guest.

        Related: KL-03

        Preconditions:
            - Guest OS logs ACPI events
            - Access to guest system logs

        Steps:
            1. Issue PUT request to /virtualmachineinstances/{name}/reset
            2. Wait for VMI to become accessible
            3. Retrieve guest system logs (dmesg or journalctl)

        Expected:
            - Guest system logs contain ACPI reset event
        """
        pass

    def test_multiple_sequential_resets(self):
        """
        Test that multiple sequential reset operations work correctly.

        Steps:
            1. Issue PUT request to /virtualmachineinstances/{name}/reset
            2. Wait for reset completion and VMI accessibility
            3. Repeat steps 1-2 two more times

        Expected:
            - All three reset operations succeed
            - VMI remains running and accessible after each reset
        """
        pass
```

---

### File: `tests/virt/lifecycle/conftest.py`

```python
"""
Shared fixtures for VMI lifecycle tests including reset functionality.

This module provides pytest fixtures for creating test VMs, managing
RBAC test users, and handling boot time tracking utilities.
"""

import pytest


@pytest.fixture
def running_alpine_vmi():
    """
    Fixture providing a running Alpine Linux VMI with SSH access.

    Yields:
        VirtualMachineInstance object with SSH connectivity
    """
    pass


@pytest.fixture
def running_rhel9_vmi():
    """
    Fixture providing a running RHEL 9 VMI with SSH access.

    Yields:
        VirtualMachineInstance object with SSH connectivity
    """
    pass


@pytest.fixture
def stopped_vmi():
    """
    Fixture providing a VMI in Stopped state.

    Yields:
        VirtualMachineInstance object in Stopped phase
    """
    pass


@pytest.fixture
def paused_vmi():
    """
    Fixture providing a VMI in Paused state.

    Yields:
        VirtualMachineInstance object in Paused phase
    """
    pass


@pytest.fixture
def vmi_with_persistent_disk():
    """
    Fixture providing a running VMI with persistent data volume.

    Yields:
        Tuple of (VirtualMachineInstance, PersistentVolumeClaim)
    """
    pass


@pytest.fixture
def test_user_with_edit_role():
    """
    Fixture providing a test user with 'edit' role in test namespace.

    Yields:
        Kubernetes client configured with test user credentials
    """
    pass


@pytest.fixture
def test_user_with_view_role():
    """
    Fixture providing a test user with 'view' role in test namespace.

    Yields:
        Kubernetes client configured with test user credentials
    """
    pass


@pytest.fixture
def test_user_with_custom_role():
    """
    Fixture providing a test user with custom role (VMI read/write, no reset).

    Yields:
        Kubernetes client configured with test user credentials
    """
    pass


@pytest.fixture
def boot_time_tracker():
    """
    Fixture providing utility to track and compare guest boot times.

    Yields:
        BootTimeTracker object with methods to get and compare boot times
    """
    pass
```

---

## Test Coverage Summary

| Test File                        | Test Class                  | Test Count | Priority | Tier               | Related ACs        |
| -------------------------------- | --------------------------- | ---------- | -------- | ------------------ | ------------------ |
| `test_vm_reset_api.py`           | `TestVMIResetAPI`           | 4          | P0       | Tier 2 (E2E)       | AC-1, AC-2, AC-3   |
| `test_vm_reset_api.py`           | `TestVMIResetAPIErrorHandling` | 3       | P0       | Tier 1 (Functional)| AC-6               |
| `test_vm_reset_virtctl.py`       | `TestVirtctlReset`          | 4          | P0       | Tier 1 (Functional)| AC-1, AC-4, AC-6   |
| `test_vm_reset_rbac.py`          | `TestVMIResetRBAC`          | 6          | P0       | Tier 1 (Functional)| AC-5               |
| `test_vm_reset_integration.py`   | `TestVMIResetIntegration`   | 5          | P1       | Tier 2 (E2E)       | G-06, KL-02, KL-03 |
| **Total**                        |                             | **22**     |          |                    |                    |

---

## Acceptance Criteria Coverage

| Criterion ID | Description                                                    | Covered By Tests                                      |
| ------------ | -------------------------------------------------------------- | ----------------------------------------------------- |
| AC-1         | As a VM owner, I can perform a reset of a VMI                  | TS-01, TS-02, TS-11 (all reset success tests)        |
| AC-2         | Reset does not require new pod to be scheduled                 | test_vmi_uid_unchanged_after_reset, test_pod_not_rescheduled_after_reset |
| AC-3         | Reset exposed via subresource API                              | All tests in TestVMIResetAPI class                    |
| AC-4         | Reset accessible via virtctl command                           | All tests in TestVirtctlReset class                   |
| AC-5         | Appropriate RBAC permissions enforced                          | All tests in TestVMIResetRBAC class                   |
| AC-6         | Reset fails gracefully on non-running VMIs                     | All tests in TestVMIResetAPIErrorHandling class       |

---

## Test Execution Strategy

### Tier 1 (Functional) Tests
These tests should run in CI/CD pipelines on every merge request:
- `TestVMIResetAPIErrorHandling.*`
- `TestVirtctlReset.*`
- `TestVMIResetRBAC.*`

### Tier 2 (End-to-End) Tests
These tests validate complete flows and should run in nightly or release builds:
- `TestVMIResetAPI.*`
- `TestVMIResetIntegration.*`

### Parametrization Strategy
- Guest OS parametrization (`alpine`, `rhel9`) ensures compatibility across different VM types
- Tests marked for parametrization will run once per parameter combination

### Gating Tests
All tests are marked as `gating` priority, indicating they are critical for feature validation and must pass before release.

---

## Known Limitations & Test Considerations

1. **KL-01**: Reset only supported for running VMIs
   - Covered by negative tests: `test_reset_fails_on_stopped_vmi`, `test_reset_on_paused_vmi`

2. **KL-02**: Guest data in memory will be lost
   - Validated by: `test_reset_clears_memory_state`

3. **KL-03**: Guest OS must support ACPI reset signal
   - Verified by: `test_reset_triggers_guest_acpi_reset`
   - Test uses guest OSes known to support ACPI (Alpine, RHEL 9)

---

## Checklist

- [x] All STP scenarios covered (TS-01 through TS-12)
- [x] Each test verifies ONE thing
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Markers documented (`gating`)
- [x] Parametrization documented (guest_os)
- [x] STP reference in all module docstrings
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Preconditions (if needed), Steps, Expected
- [x] Test methods contain only `pass`
- [x] Shared fixtures defined in `conftest.py`
- [x] Coverage summary table included
- [x] All acceptance criteria (AC-1 through AC-6) traced to tests
- [x] All goals (G-01 through G-06) addressed
- [x] All known limitations (KL-01 through KL-03) tested
- [x] RBAC permissions validated
- [x] Error handling for edge cases covered
