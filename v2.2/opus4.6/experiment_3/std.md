# Software Test Description (STD)

## Feature: VMI Force/Hard Reset

**STP Reference:** [VIRTSTRAT-357: Hard VM Reset](https://issues.redhat.com/browse/VIRTSTRAT-357)
**Jira ID:** VIRTSTRAT-357
**Generated:** 2026-02-11

---

## Summary

This STD covers the Force/Hard Reset feature for VirtualMachineInstance objects in OpenShift Virtualization. The tests verify that a running VMI can be reset via the subresource API and the `virtctl reset` command, that the reset preserves the VMI UID and pod assignment, that RBAC permissions are enforced, and that appropriate errors are returned for non-running or non-existent VMIs.

---

## Test Files

### File: `tests/virt/node/general/test_vmi_hard_reset.py`

```python
"""
VMI Force/Hard Reset Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains tests for the VMI hard reset feature, which allows
resetting a hung or unresponsive VirtualMachineInstance without pod
rescheduling. The reset simulates pressing the hardware reset button
on a physical machine.
"""

import pytest


class TestVMIHardResetAPI:
    """
    Tests for VMI hard reset via the subresource API.

    Preconditions:
        - Running VM with SSH accessible guest
        - Boot time recorded before reset
        - VMI UID recorded before reset
        - Pod name recorded before reset
    """

    def test_vmi_reset_triggers_guest_reboot(self):
        """
        Test that resetting a running VMI via the API triggers a guest reboot.

        Steps:
            1. Reset the VMI via the subresource API
            2. Wait for the VM to become running and SSH accessible
            3. Read the guest boot time

        Expected:
            - Guest boot time after reset is more recent than boot time before reset
        """
        pass

    def test_vmi_reset_preserves_pod(self):
        """
        Test that resetting a VMI does not cause pod rescheduling.

        Preconditions:
            - VMI has been reset via the API and is running

        Steps:
            1. Read the pod name hosting the VMI after reset

        Expected:
            - Pod name after reset equals pod name before reset
        """
        pass

    def test_vmi_reset_preserves_uid(self):
        """
        Test that the VMI UID remains unchanged after a reset.

        Preconditions:
            - VMI has been reset via the API and is running

        Steps:
            1. Read the VMI UID after reset

        Expected:
            - VMI UID after reset equals VMI UID before reset
        """
        pass


class TestVMIHardResetVirtctl:
    """
    Tests for VMI hard reset via the virtctl CLI.

    Preconditions:
        - Running VM with SSH accessible guest
        - Boot time recorded before reset
    """

    def test_virtctl_reset_triggers_guest_reboot(self):
        """
        Test that resetting a running VMI via virtctl triggers a guest reboot.

        Steps:
            1. Execute `virtctl reset <vm-name>` command
            2. Wait for the VM to become running and SSH accessible
            3. Read the guest boot time

        Expected:
            - Guest boot time after reset is more recent than boot time before reset
        """
        pass


class TestVMIHardResetRBAC:
    """
    Tests for RBAC enforcement on the VMI reset operation.

    Preconditions:
        - Running VM
        - Unprivileged service account created in the VM namespace
    """

    def test_unprivileged_user_cannot_reset_vmi(self):
        """
        [NEGATIVE] Test that an unprivileged user cannot reset a VMI.

        Steps:
            1. Attempt to reset the VMI using the unprivileged service account

        Expected:
            - Reset operation fails with a 403 Forbidden error
        """
        pass

    def test_user_with_edit_role_can_reset_vmi(self):
        """
        Test that a user with the edit ClusterRole can reset a VMI.

        Preconditions:
            - Service account bound to the edit ClusterRole in the VM namespace

        Steps:
            1. Reset the VMI using the service account with edit role
            2. Wait for the VM to become running

        Expected:
            - Reset operation succeeds without error
        """
        pass


class TestVMIHardResetNegative:
    """
    Tests for VMI reset error handling on non-running VMIs.

    Preconditions:
        - VM exists in the namespace
    """

    def test_reset_stopped_vmi_fails(self):
        """
        [NEGATIVE] Test that resetting a stopped VMI returns an appropriate error.

        Preconditions:
            - VM is in stopped state (not running)

        Steps:
            1. Attempt to reset the stopped VMI via the API

        Expected:
            - Reset operation fails with an error indicating the VMI is not running
        """
        pass

    def test_reset_paused_vmi_fails(self):
        """
        [NEGATIVE] Test that resetting a paused VMI returns an appropriate error.

        Preconditions:
            - VM is running and has been paused

        Steps:
            1. Attempt to reset the paused VMI via the API

        Expected:
            - Reset operation fails with an error indicating the VMI is paused
        """
        pass

    def test_reset_nonexistent_vmi_fails(self):
        """
        [NEGATIVE] Test that resetting a non-existent VMI returns a 404 error.

        Steps:
            1. Attempt to reset a VMI with a name that does not exist in the namespace

        Expected:
            - Reset operation fails with a 404 Not Found error
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Tier | Related ACs |
| --- | --- | --- | --- | --- |
| `test_vmi_hard_reset.py` | `TestVMIHardResetAPI` | 3 | Tier 2 (End-to-End) | AC-1, AC-2, AC-3 |
| `test_vmi_hard_reset.py` | `TestVMIHardResetVirtctl` | 1 | Tier 1 (Functional) | AC-1, AC-4 |
| `test_vmi_hard_reset.py` | `TestVMIHardResetRBAC` | 2 | Tier 1 (Functional) | AC-5 |
| `test_vmi_hard_reset.py` | `TestVMIHardResetNegative` | 3 | Tier 1 (Functional) | AC-6 |

---

## Traceability Matrix

| Test ID (STP) | Test Method | AC Coverage |
| --- | --- | --- |
| TS-01 | `test_vmi_reset_triggers_guest_reboot` | AC-1, AC-3 |
| TS-01 | `test_vmi_reset_preserves_pod` | AC-2 |
| TS-02 | `test_virtctl_reset_triggers_guest_reboot` | AC-1, AC-4 |
| TS-03 | `test_vmi_reset_preserves_uid` | AC-2, AC-3 |
| TS-04 | `test_unprivileged_user_cannot_reset_vmi` | AC-5 |
| TS-04 | `test_user_with_edit_role_can_reset_vmi` | AC-5 |
| TS-05 | `test_reset_stopped_vmi_fails` | AC-6 |
| TS-06 | `test_reset_nonexistent_vmi_fails` | AC-6 |
| TS-11 | `test_vmi_reset_triggers_guest_reboot` | AC-1 |
| TS-12 | `test_reset_paused_vmi_fails` | AC-6 |

---

## Checklist

- [x] STP link in module docstring
- [x] All STP scenarios covered (TS-01 through TS-06, TS-11, TS-12)
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Preconditions (if needed), Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/vmi_hard_reset/std_virtstrat_357.md`
