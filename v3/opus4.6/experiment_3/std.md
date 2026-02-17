# Software Test Description (STD)

## Feature: Force/Hard VM Reset

**STP Reference:** [../stps/3.md](../../../stps/3.md)
**Jira ID:** [VIRTSTRAT-357](https://issues.redhat.com/browse/VIRTSTRAT-357)
**Generated:** 2026-02-16

---

## Summary

This STD covers the Force/Hard Reset feature for VirtualMachineInstance (VMI) objects in OpenShift Virtualization. The reset simulates pressing the hardware reset button, rebooting the guest without pod rescheduling. Tests verify:

- Reset via subresource API and virtctl command (TS-01, TS-02)
- VMI UID preservation and boot time changes after reset (TS-03, TS-11)
- RBAC enforcement for reset operations (TS-04)
- Error handling for non-running, non-existent, and paused VMIs (TS-05, TS-06, TS-12)

---

## Test Files

### File: `tests/virt/node/general/test_vmi_reset.py`

```python
"""
Force/Hard VM Reset Tests

STP Reference: ../stps/3.md
Jira: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains tests for the VMI reset subresource API,
virtctl reset command, and associated error handling. The reset
operation simulates a hardware reset button press, rebooting the
guest OS without requiring pod rescheduling.
"""

import pytest


class TestVMIReset:
    """
    Tests for core VMI reset functionality.

    Preconditions:
        - Running Fedora virtual machine with SSH access
        - Boot count recorded before reset
    """

    def test_reset_running_vmi_via_api(self):
        """
        Test that a running VMI can be reset via the subresource API
        and the guest reboots successfully.

        Steps:
            1. Call the VMI reset subresource API endpoint
            2. Wait for the VM to return to Running state
            3. Read the boot count from the guest via journalctl

        Expected:
            - Boot count increased by 1 compared to pre-reset value
        """
        pass

    def test_reset_running_vmi_via_virtctl(self):
        """
        Test that a running VMI can be reset using the virtctl reset command.

        Steps:
            1. Execute `virtctl reset <vmi-name>` command
            2. Wait for the VM to return to Running state

        Expected:
            - virtctl command exits with return code 0
        """
        pass

    def test_vmi_uid_unchanged_after_reset(self):
        """
        Test that the VMI UID remains the same after a reset,
        confirming no pod rescheduling occurred.

        Steps:
            1. Record VMI UID before reset
            2. Perform VMI reset via API
            3. Wait for VM to return to Running state
            4. Read VMI UID after reset

        Expected:
            - VMI UID after reset equals VMI UID before reset
        """
        pass

    def test_boot_time_changes_after_reset(self):
        """
        Test that the guest system boot time changes after a reset,
        confirming the guest OS actually rebooted.

        Steps:
            1. Read system boot time from the guest via uptime
            2. Perform VMI reset via API
            3. Wait for VM to return to Running state
            4. Read system boot time from the guest after reset

        Expected:
            - Boot time after reset is more recent than boot time before reset
        """
        pass


class TestVMIResetNegative:
    """
    Tests for VMI reset error handling and edge cases.

    Preconditions:
        - Namespace available for VM operations
    """

    def test_reset_fails_on_stopped_vmi(self):
        """
        [NEGATIVE] Test that resetting a stopped VMI returns an appropriate error.

        Preconditions:
            - VM created and in Stopped state (not started)

        Steps:
            1. Attempt to call the VMI reset subresource API on the stopped VM

        Expected:
            - API returns an error indicating reset is not allowed on non-running VMI
        """
        pass

    def test_reset_fails_on_nonexistent_vmi(self):
        """
        [NEGATIVE] Test that resetting a non-existent VMI returns a Not Found error.

        Steps:
            1. Attempt to call the VMI reset subresource API with a non-existent VMI name

        Expected:
            - API returns a 404 Not Found error
        """
        pass

    def test_reset_fails_on_paused_vmi(self):
        """
        [NEGATIVE] Test that resetting a paused VMI returns an appropriate error.

        Preconditions:
            - Running Fedora virtual machine
            - VM is paused via the pause subresource API

        Steps:
            1. Attempt to call the VMI reset subresource API on the paused VMI

        Expected:
            - API returns an error indicating reset is not allowed on paused VMI
        """
        pass


class TestVMIResetRBAC:
    """
    Tests for RBAC enforcement on VMI reset operations.

    Preconditions:
        - Running Fedora virtual machine
        - Unprivileged user with edit ClusterRole bound to the test namespace
    """

    def test_user_with_edit_role_can_reset_vmi(self):
        """
        Test that a user with the edit ClusterRole can perform a VMI reset.

        Steps:
            1. As the unprivileged user with edit role, call the VMI reset subresource API

        Expected:
            - Reset operation succeeds without authorization error
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Tier | Related ACs |
|---|---|---|---|---|
| `test_vmi_reset.py` | `TestVMIReset` | 4 | Tier 2 (End-to-End) | AC-1, AC-2, AC-3, AC-4 |
| `test_vmi_reset.py` | `TestVMIResetNegative` | 3 | Tier 1 (Functional) | AC-6 |
| `test_vmi_reset.py` | `TestVMIResetRBAC` | 1 | Tier 1 (Functional) | AC-5 |

## Traceability Matrix

| Test ID | Test Method | Acceptance Criteria |
|---|---|---|
| TS-01 | `test_reset_running_vmi_via_api` | AC-1, AC-2, AC-3 |
| TS-02 | `test_reset_running_vmi_via_virtctl` | AC-1, AC-4 |
| TS-03 | `test_vmi_uid_unchanged_after_reset` | AC-2 |
| TS-04 | `test_user_with_edit_role_can_reset_vmi` | AC-5 |
| TS-05 | `test_reset_fails_on_stopped_vmi` | AC-6 |
| TS-06 | `test_reset_fails_on_nonexistent_vmi` | AC-6 |
| TS-11 | `test_boot_time_changes_after_reset` | AC-1 |
| TS-12 | `test_reset_fails_on_paused_vmi` | AC-6 |

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Preconditions (if needed), Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] All STP scenarios covered (TS-01 through TS-12)
- [x] All files in single markdown output
- [x] Coverage summary table included
