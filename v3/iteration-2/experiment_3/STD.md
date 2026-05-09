# Software Test Description (STD)

## Feature: VMI Hard Reset (Force Reset)

**STP Reference:** [stps/3.md](/home/fedora/thesis/stps/3.md)
**Jira ID:** [VIRTSTRAT-357](https://issues.redhat.com/browse/VIRTSTRAT-357)
**Generated:** 2026-02-23

---

## Summary

This STD covers the VMI hard reset feature for OpenShift Virtualization. The hard reset simulates pressing the hardware reset button on a physical machine, resetting a hung or unresponsive VirtualMachineInstance without pod rescheduling.

The test suite verifies:

- Reset via the subresource API endpoint (`/virtualmachineinstances/{name}/reset`)
- Reset via the `virtctl reset` command
- VMI state preservation (UID, pod) across resets
- Guest reboot confirmation via boot time changes
- RBAC enforcement for the reset operation
- Error handling for non-running and non-existent VMIs

---

## Test Files

### File: `tests/virt/reset/test_vmi_reset.py`

```python
"""
VMI Hard Reset Tests

STP Reference: /home/fedora/thesis/stps/3.md
Jira: VIRTSTRAT-357

This module contains tests for the VMI hard reset (force reset) functionality,
which allows resetting a hung or unresponsive VirtualMachineInstance without
pod rescheduling. The reset is analogous to the `virsh reset` command in libvirt.
"""

import pytest


class TestVMIResetViaAPI:
    """
    Tests for VMI reset via the subresource API.

    Preconditions:
        - Running VMI with SSH access
        - VMI UID recorded before reset
        - Virt-launcher pod name recorded before reset
        - Guest boot time recorded before reset
        - VMI reset performed via subresource API (/virtualmachineinstances/{name}/reset)
        - VMI is Running and SSH accessible after reset
    """

    def test_guest_accessible_after_api_reset(self):
        """
        Test that the VMI is Running and the guest is accessible after a hard reset via the API.

        Steps:
            1. Verify VMI status is Running and SSH connection succeeds after reset

        Expected:
            - VMI is "Running"
        """
        pass

    def test_vmi_uid_unchanged_after_reset(self):
        """
        Test that VMI UID remains unchanged after a hard reset.

        Steps:
            1. Compare VMI UID before and after reset

        Expected:
            - VMI UID after reset equals VMI UID before reset
        """
        pass

    def test_pod_not_rescheduled_after_reset(self):
        """
        Test that the virt-launcher pod is not rescheduled after a hard reset.

        Steps:
            1. Compare virt-launcher pod name before and after reset

        Expected:
            - Virt-launcher pod name after reset equals pod name before reset
        """
        pass

    def test_boot_time_changes_after_reset(self):
        """
        Test that the guest boot time changes after a hard reset, confirming guest reboot.

        Steps:
            1. Compare guest boot time before and after reset

        Expected:
            - Guest boot time after reset does not equal boot time before reset
        """
        pass


class TestVMIResetViaVirtctl:
    """
    Tests for VMI reset via the virtctl CLI command.

    Preconditions:
        - Running VMI with SSH access
        - Guest boot time recorded before reset
    """

    def test_virtctl_reset_reboots_guest(self):
        """
        Test that the virtctl reset command successfully resets the guest.

        Steps:
            1. Execute `virtctl reset <vmi-name>` command
            2. Wait for VMI to be Running and SSH accessible
            3. Compare guest boot time before and after reset

        Expected:
            - Guest boot time after reset does not equal boot time before reset
        """
        pass


class TestVMIResetRBAC:
    """
    Tests for RBAC enforcement on the VMI reset operation.

    Preconditions:
        - Running VMI with SSH access
        - ServiceAccount with edit ClusterRole binding in the test namespace
    """

    def test_edit_role_user_can_reset_vmi(self):
        """
        Test that a user with the edit ClusterRole can perform a VMI reset.

        Steps:
            1. Perform VMI reset via API using the ServiceAccount with edit role

        Expected:
            - Reset operation succeeds
        """
        pass


class TestVMIResetNegative:
    """
    [NEGATIVE] Tests for VMI reset failure scenarios.

    Preconditions:
        - Namespace with sufficient permissions for VMI operations
    """

    def test_reset_fails_on_stopped_vmi(self):
        """
        [NEGATIVE] Test that reset fails on a stopped VMI with an appropriate error.

        Preconditions:
            - VMI in stopped state

        Steps:
            1. Attempt to reset the stopped VMI via API

        Expected:
            - Reset operation fails with an error indicating VMI is not running
        """
        pass

    def test_reset_fails_on_nonexistent_vmi(self):
        """
        [NEGATIVE] Test that reset fails on a non-existent VMI with an appropriate error.

        Steps:
            1. Attempt to reset a non-existent VMI name via API

        Expected:
            - Reset operation fails with a "not found" error
        """
        pass

    def test_reset_fails_on_paused_vmi(self):
        """
        [NEGATIVE] Test that reset fails on a paused VMI with an appropriate error.

        Preconditions:
            - VMI in paused state

        Steps:
            1. Attempt to reset the paused VMI via API

        Expected:
            - Reset operation fails with an error indicating VMI is paused
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Tier | STP Scenarios |
| --- | --- | --- | --- | --- |
| `test_vmi_reset.py` | `TestVMIResetViaAPI` | 4 | Tier 2 (End-to-End) | TS-01, TS-03, TS-11 |
| `test_vmi_reset.py` | `TestVMIResetViaVirtctl` | 1 | Tier 1 (Functional) | TS-02 |
| `test_vmi_reset.py` | `TestVMIResetRBAC` | 1 | Tier 1 (Functional) | TS-04 |
| `test_vmi_reset.py` | `TestVMIResetNegative` | 3 | Tier 1 (Functional) | TS-05, TS-06, TS-12 |
| **Total** | | **9** | | |

---

## Acceptance Criteria Traceability

| AC ID | Description | Covered By |
| --- | --- | --- |
| AC-1 | VM owner can perform reset of VMI | `test_guest_accessible_after_api_reset`, `test_virtctl_reset_reboots_guest` |
| AC-2 | Reset does not require new pod scheduling | `test_pod_not_rescheduled_after_reset`, `test_vmi_uid_unchanged_after_reset` |
| AC-3 | Reset exposed via subresource API | `test_guest_accessible_after_api_reset` |
| AC-4 | Reset accessible via virtctl | `test_virtctl_reset_reboots_guest` |
| AC-5 | RBAC permissions enforced | `test_edit_role_user_can_reset_vmi` |
| AC-6 | Reset fails gracefully on non-running VMIs | `test_reset_fails_on_stopped_vmi`, `test_reset_fails_on_nonexistent_vmi`, `test_reset_fails_on_paused_vmi` |

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass`
- [x] All STP scenarios (TS-01, TS-02, TS-03, TS-04, TS-05, TS-06, TS-11, TS-12) covered
- [x] All acceptance criteria (AC-1 through AC-6) traced
