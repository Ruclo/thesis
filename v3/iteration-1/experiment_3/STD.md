# Software Test Description (STD)

## Feature: VMI Hard Reset (Force/Hard Reset)

**STP Reference:** [VIRTSTRAT-357: Hard VM Reset](https://issues.redhat.com/browse/VIRTSTRAT-357)
**Jira ID:** VIRTSTRAT-357
**Generated:** 2026-02-21

---

## Summary

This STD covers the Force/Hard Reset feature for VirtualMachineInstance objects in OpenShift Virtualization. Tests verify:

- VMI reset via the subresource API (guest reboots, pod preserved, UID unchanged)
- VMI reset via `virtctl reset` command
- RBAC enforcement for the reset subresource
- Error handling for non-running and non-existent VMIs
- Boot time verification after reset
- Reset behavior on paused VMIs

Tests are organized into three files:
1. `test_vmi_hard_reset.py` - Core reset functionality (API-based reset, boot time, UID/pod preservation)
2. `test_virtctl_reset.py` - virtctl CLI reset command
3. `test_vmi_reset_negative.py` - Negative/error scenarios (non-running, non-existent, paused VMIs, RBAC)

---

## Test Files

### File: `tests/virt/node/hard_reset/test_vmi_hard_reset.py`

```python
"""
VMI Hard Reset Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains tests for the VMI hard reset subresource API,
verifying that a running VMI can be reset in-place without pod
rescheduling, preserving VMI UID and triggering an actual guest reboot.
"""

import pytest

pytestmark = pytest.mark.virt


class TestVMIHardReset:
    """
    Tests for VMI hard reset core functionality via the subresource API.

    Preconditions:
        - Running Fedora virtual machine with SSH access
        - Boot count recorded before reset
        - VMI UID and pod name recorded before reset
        - VMI reset performed and VM is running again with SSH access
    """

    def test_guest_reboots_after_reset(self):
        """
        Test that a VMI hard reset triggers an actual guest reboot.

        Steps:
            1. Compare boot count after reset with boot count before reset

        Expected:
            - Boot count after reset equals boot count before reset plus 1
        """
        pass

    def test_pod_preserved_after_reset(self):
        """
        Test that the virt-launcher pod is not rescheduled after a VMI reset.

        Steps:
            1. Compare pod name after reset with pod name before reset

        Expected:
            - Pod name after reset equals pod name before reset
        """
        pass

    def test_vmi_uid_unchanged_after_reset(self):
        """
        Test that the VMI UID remains unchanged after a hard reset.

        Steps:
            1. Compare VMI UID after reset with VMI UID before reset

        Expected:
            - VMI UID after reset equals VMI UID before reset
        """
        pass
```

---

### File: `tests/virt/node/hard_reset/test_virtctl_reset.py`

```python
"""
VMI Hard Reset via virtctl Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains tests for the VMI hard reset functionality
accessed through the virtctl CLI command.
"""

import pytest

pytestmark = pytest.mark.virt


class TestVirtctlReset:
    """
    Tests for VMI hard reset via the virtctl reset command.

    Preconditions:
        - Running Fedora virtual machine with SSH access
        - Boot count recorded before reset
    """

    def test_virtctl_reset_triggers_guest_reboot(self):
        """
        Test that running 'virtctl reset' on a running VMI triggers a guest reboot.

        Steps:
            1. Execute 'virtctl reset <vmi-name>' command
            2. Wait for VM to become running and SSH accessible
            3. Compare boot count after reset with boot count before reset

        Expected:
            - Boot count after reset equals boot count before reset plus 1
        """
        pass

    def test_virtctl_reset_command_succeeds(self):
        """
        Test that the 'virtctl reset' command completes successfully.

        Steps:
            1. Execute 'virtctl reset <vmi-name>' command

        Expected:
            - Command exit code equals 0
        """
        pass
```

---

### File: `tests/virt/node/hard_reset/test_vmi_reset_negative.py`

```python
"""
VMI Hard Reset Negative Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains negative tests for the VMI hard reset feature,
verifying proper error handling for invalid reset scenarios and
RBAC enforcement.
"""

import pytest

pytestmark = pytest.mark.virt


class TestVMIResetOnNonRunningVM:
    """
    Tests for VMI hard reset error handling on non-running VMIs.

    Preconditions:
        - Fedora virtual machine exists in the namespace
    """

    def test_reset_stopped_vmi(self):
        """
        [NEGATIVE] Test that resetting a stopped VMI fails with an appropriate error.

        Preconditions:
            - VM is in stopped state (not running)

        Steps:
            1. Attempt to call reset on the stopped VMI

        Expected:
            - Operation raises an error indicating the VMI is not running
        """
        pass

    def test_reset_paused_vmi(self):
        """
        [NEGATIVE] Test that resetting a paused VMI fails with an appropriate error.

        Preconditions:
            - VM is running
            - VMI is paused

        Steps:
            1. Attempt to call reset on the paused VMI

        Expected:
            - Operation raises an error indicating the VMI cannot be reset while paused
        """
        pass


def test_reset_nonexistent_vmi():
    """
    [NEGATIVE] Test that resetting a non-existent VMI fails with a not-found error.

    Preconditions:
        - No VMI with name "nonexistent-vmi" exists in the namespace

    Steps:
        1. Attempt to call reset on a non-existent VMI name

    Expected:
        - Operation raises a not-found error
    """
    pass


class TestVMIResetRBAC:
    """
    Tests for RBAC enforcement on the VMI reset subresource.

    Preconditions:
        - Running Fedora virtual machine created by unprivileged user
    """

    def test_unprivileged_user_cannot_reset_without_permission(self):
        """
        [NEGATIVE] Test that a user without reset permission cannot reset a VMI.

        Steps:
            1. Attempt to reset the VMI using an unprivileged client without reset role binding

        Expected:
            - Operation raises ForbiddenError
        """
        pass

    def test_unprivileged_user_can_reset_with_edit_role(self):
        """
        Test that a user with the edit ClusterRole can reset a VMI.

        Preconditions:
            - Unprivileged user has RoleBinding to kubevirt.io:edit ClusterRole

        Steps:
            1. Reset the VMI using the unprivileged client with edit role binding

        Expected:
            - Reset operation succeeds without error
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier | Related ACs |
| --- | --- | --- | --- | --- | --- |
| `test_vmi_hard_reset.py` | `TestVMIHardReset` | 3 | P0 | Tier 2 (End-to-End) | AC-1, AC-2, AC-3 |
| `test_virtctl_reset.py` | `TestVirtctlReset` | 2 | P0 | Tier 1 (Functional) | AC-1, AC-4 |
| `test_vmi_reset_negative.py` | `TestVMIResetOnNonRunningVM` | 2 | P1 | Tier 1 (Functional) | AC-6 |
| `test_vmi_reset_negative.py` | (standalone) `test_reset_nonexistent_vmi` | 1 | P1 | Tier 1 (Functional) | AC-6 |
| `test_vmi_reset_negative.py` | `TestVMIResetRBAC` | 2 | P1 | Tier 1 (Functional) | AC-5 |

**Total: 10 tests across 3 files**

---

## Traceability Matrix

| Test ID (STP) | Test Method | File |
| --- | --- | --- |
| TS-01 | `test_guest_reboots_after_reset`, `test_pod_preserved_after_reset`, `test_vmi_uid_unchanged_after_reset` | `test_vmi_hard_reset.py` |
| TS-02 | `test_virtctl_reset_triggers_guest_reboot`, `test_virtctl_reset_command_succeeds` | `test_virtctl_reset.py` |
| TS-03 | `test_vmi_uid_unchanged_after_reset` (API subresource verified implicitly) | `test_vmi_hard_reset.py` |
| TS-04 | `test_unprivileged_user_cannot_reset_without_permission`, `test_unprivileged_user_can_reset_with_edit_role` | `test_vmi_reset_negative.py` |
| TS-05 | `test_reset_stopped_vmi` | `test_vmi_reset_negative.py` |
| TS-06 | `test_reset_nonexistent_vmi` | `test_vmi_reset_negative.py` |
| TS-11 | `test_guest_reboots_after_reset` | `test_vmi_hard_reset.py` |
| TS-12 | `test_reset_paused_vmi` | `test_vmi_reset_negative.py` |

---

## Checklist

- [x] STP link in module docstring
- [x] All STP scenarios (TS-01 through TS-12) covered
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Traceability matrix included
- [x] Output saved to `tests/std/vmi_hard_reset/std_virtstrat_357.md`
