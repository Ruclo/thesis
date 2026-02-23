# Software Test Description (STD)

## Feature: VMI Force/Hard Reset

**STP Reference:** [VIRTSTRAT-357: Hard VM Reset](https://issues.redhat.com/browse/VIRTSTRAT-357)
**Jira ID:** VIRTSTRAT-357
**Generated:** 2026-02-10

---

## Summary

This STD covers the Force/Hard Reset feature for VirtualMachineInstance objects in OpenShift Virtualization. The feature provides the ability to reset a running VMI without requiring pod rescheduling, analogous to the `virsh reset` command in libvirt.

The tests verify:
- VMI reset API endpoint functionality (`/virtualmachineinstances/{name}/reset`)
- `virtctl reset` command integration
- RBAC permission enforcement for reset operations
- Error handling for non-running VMIs
- Pod and UID preservation during reset
- Actual guest reboot verification via boot time changes

---

## Test Files

### File: `tests/virt/lifecycle/test_vmi_reset.py`

```python
"""
VMI Force/Hard Reset Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains tests for the VMI Force/Hard Reset feature, which allows
resetting a running VMI without requiring pod rescheduling.
"""

import pytest


class TestVMIReset:
    """
    Tests for VMI Force/Hard Reset functionality.

    Markers:
        - gating

    Preconditions:
        - Running VirtualMachineInstance with Alpine Linux or RHEL 9
        - VMI is in Running state with guest agent installed
        - VMI has SSH access enabled
    """

    def test_reset_running_vmi_via_api(self):
        """
        Test that a running VMI can be reset via the API and the guest reboots.

        Steps:
            1. Get initial boot time from the running VMI via SSH
            2. Execute reset operation via the VMI reset subresource API
            3. Wait for VMI to become accessible after reset
            4. Get new boot time from the VMI via SSH

        Expected:
            - Reset operation succeeds without error
            - VMI remains in Running state
            - Boot time has changed (indicating guest rebooted)
        """
        pass

    def test_reset_running_vmi_via_virtctl(self):
        """
        Test that a running VMI can be reset via virtctl command.

        Steps:
            1. Get initial boot time from the running VMI via SSH
            2. Execute 'virtctl reset <vmi-name>' command
            3. Wait for VMI to become accessible after reset
            4. Get new boot time from the VMI via SSH

        Expected:
            - virtctl command succeeds with appropriate output message
            - VMI remains in Running state
            - Boot time has changed (indicating guest rebooted)
        """
        pass

    def test_vmi_uid_unchanged_after_reset(self):
        """
        Test that the VMI UID remains unchanged after reset operation.

        Steps:
            1. Record VMI UID before reset
            2. Execute reset operation via API
            3. Wait for VMI to become accessible after reset
            4. Get VMI UID after reset

        Expected:
            - VMI UID before reset equals VMI UID after reset
        """
        pass

    def test_vmi_pod_unchanged_after_reset(self):
        """
        Test that the VMI pod is not rescheduled after reset operation.

        Steps:
            1. Record VMI pod name and UID before reset
            2. Execute reset operation via API
            3. Wait for VMI to become accessible after reset
            4. Get VMI pod name and UID after reset

        Expected:
            - Pod name remains unchanged
            - Pod UID remains unchanged
        """
        pass

    def test_boot_time_changes_after_reset(self):
        """
        Test that the guest boot time changes after reset, confirming actual reboot.

        Steps:
            1. Get boot time from running VMI via 'uptime -s' or equivalent
            2. Execute reset operation via API
            3. Wait for VMI to become accessible after reset
            4. Get boot time from VMI again

        Expected:
            - Boot time after reset is greater than boot time before reset
        """
        pass


class TestVMIResetRBAC:
    """
    Tests for RBAC permission enforcement for VMI reset operations.

    Preconditions:
        - Running VirtualMachineInstance
        - Test service account with 'edit' role in the VMI namespace
        - Test service account without reset permissions
    """

    def test_user_with_edit_role_can_reset_vmi(self):
        """
        Test that a user with 'edit' role can successfully reset a VMI.

        Steps:
            1. Impersonate service account with 'edit' role
            2. Execute reset operation on VMI via API

        Expected:
            - Reset operation succeeds without authorization error
        """
        pass

    def test_user_without_reset_permission_cannot_reset_vmi(self):
        """
        [NEGATIVE] Test that a user without reset permission cannot reset a VMI.

        Steps:
            1. Impersonate service account without 'virtualmachineinstances/reset' permission
            2. Attempt to execute reset operation on VMI via API

        Expected:
            - Reset operation fails with HTTP 403 Forbidden error
        """
        pass


class TestVMIResetErrorHandling:
    """
    Tests for error handling in VMI reset operations.

    Preconditions:
        - VirtualMachineInstance in various states (Stopped, Paused, non-existent)
    """

    def test_reset_stopped_vmi_fails(self):
        """
        [NEGATIVE] Test that reset operation fails on a stopped VMI.

        Preconditions:
            - VirtualMachineInstance in Stopped state

        Steps:
            1. Execute reset operation on stopped VMI via API

        Expected:
            - Reset operation fails with appropriate error message
            - Error message indicates VMI must be running to perform reset
        """
        pass

    def test_reset_paused_vmi_behavior(self):
        """
        [NEGATIVE] Test that reset operation on paused VMI returns appropriate error.

        Preconditions:
            - VirtualMachineInstance in Paused state

        Steps:
            1. Execute reset operation on paused VMI via API

        Expected:
            - Reset operation fails with appropriate error message
            - Error message indicates VMI must be running (not paused) to perform reset
        """
        pass

    def test_reset_nonexistent_vmi_fails(self):
        """
        [NEGATIVE] Test that reset operation fails on a non-existent VMI.

        Steps:
            1. Attempt to execute reset operation on a non-existent VMI name via API

        Expected:
            - Reset operation fails with HTTP 404 Not Found error
        """
        pass


class TestVMIResetClientGo:
    """
    Tests for client-go integration with VMI reset functionality.

    Preconditions:
        - Running VirtualMachineInstance
        - client-go library with Reset() method support
    """

    def test_clientgo_reset_method_succeeds(self):
        """
        Test that the client-go Reset() method successfully resets a running VMI.

        Steps:
            1. Get initial boot time from running VMI
            2. Call Reset() method on VirtualMachineInstance client-go interface
            3. Wait for VMI to become accessible after reset
            4. Get new boot time from VMI

        Expected:
            - Reset() method returns without error
            - Boot time has changed (indicating guest rebooted)
        """
        pass
```

---

### File: `tests/virt/lifecycle/conftest.py`

```python
"""
Shared fixtures for VMI lifecycle tests.
"""

import pytest


@pytest.fixture(scope="function")
def running_alpine_vmi(namespace, unprivileged_client):
    """
    Running Alpine Linux VirtualMachineInstance with SSH access.

    Yields:
        VirtualMachineInstance: Running VMI with Alpine Linux
    """
    pass


@pytest.fixture(scope="function")
def running_rhel9_vmi(namespace, unprivileged_client):
    """
    Running RHEL 9 VirtualMachineInstance with SSH access.

    Yields:
        VirtualMachineInstance: Running VMI with RHEL 9
    """
    pass


@pytest.fixture(scope="function")
def stopped_vmi(namespace, unprivileged_client):
    """
    Stopped VirtualMachineInstance.

    Yields:
        VirtualMachineInstance: VMI in Stopped state
    """
    pass


@pytest.fixture(scope="function")
def paused_vmi(namespace, unprivileged_client):
    """
    Paused VirtualMachineInstance.

    Yields:
        VirtualMachineInstance: VMI in Paused state
    """
    pass


@pytest.fixture(scope="function")
def service_account_with_edit_role(namespace, admin_client):
    """
    Service account with 'edit' role in the VMI namespace.

    Yields:
        ServiceAccount: Service account with edit permissions
    """
    pass


@pytest.fixture(scope="function")
def service_account_without_reset_permission(namespace, admin_client):
    """
    Service account without 'virtualmachineinstances/reset' permission.

    Yields:
        ServiceAccount: Service account without reset permission
    """
    pass
```

---

## Test Coverage Summary

| Test File                     | Test Class                    | Test Count | Priority | Tier               |
| ----------------------------- | ----------------------------- | ---------- | -------- | ------------------ |
| `test_vmi_reset.py`           | `TestVMIReset`                | 5          | P0       | Tier 2 (End-to-End)|
| `test_vmi_reset.py`           | `TestVMIResetRBAC`            | 2          | P0       | Tier 1 (Functional)|
| `test_vmi_reset.py`           | `TestVMIResetErrorHandling`   | 3          | P1       | Tier 1 (Functional)|
| `test_vmi_reset.py`           | `TestVMIResetClientGo`        | 1          | P1       | Tier 1 (Functional)|

**Total Test Count:** 11

---

## Test Scenario Traceability

| Test ID | Test Function                                      | Acceptance Criteria |
| ------- | -------------------------------------------------- | ------------------- |
| TS-01   | `test_reset_running_vmi_via_api`                   | AC-1, AC-2, AC-3    |
| TS-02   | `test_reset_running_vmi_via_virtctl`               | AC-1, AC-4          |
| TS-03   | `test_vmi_uid_unchanged_after_reset`               | AC-2                |
| TS-03   | `test_vmi_pod_unchanged_after_reset`               | AC-2                |
| TS-04   | `test_user_with_edit_role_can_reset_vmi`           | AC-5                |
| TS-04   | `test_user_without_reset_permission_cannot_reset_vmi` | AC-5             |
| TS-05   | `test_reset_stopped_vmi_fails`                     | AC-6                |
| TS-06   | `test_reset_nonexistent_vmi_fails`                 | AC-6                |
| TS-11   | `test_boot_time_changes_after_reset`               | AC-1                |
| TS-12   | `test_reset_paused_vmi_behavior`                   | AC-6                |
| N/A     | `test_clientgo_reset_method_succeeds`              | AC-1, AC-3          |

---

## Checklist

- [x] All STP scenarios covered
- [x] Each test verifies ONE thing
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Markers documented (`gating`)
- [x] Parametrization documented (not applicable for this feature)
- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Preconditions, Steps, Expected
- [x] Test methods contain only `pass`
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/vmi_reset/std_virtstrat_357.md`

---

## Notes

1. **Fixtures Required**: The conftest.py file includes fixture stubs for:
   - Running VMIs with different OS types (Alpine, RHEL 9)
   - VMIs in different states (Stopped, Paused)
   - Service accounts with different RBAC permissions

2. **Boot Time Verification**: Multiple tests verify boot time changes to confirm actual guest reboot occurred, not just API success.

3. **RBAC Testing**: Separate test class for RBAC validation ensures proper permission enforcement.

4. **Error Handling**: Comprehensive negative tests cover all documented known limitations (KL-01).

5. **Client Integration**: client-go library integration is tested separately to ensure programmatic access works correctly.
