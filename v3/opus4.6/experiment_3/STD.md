# Software Test Description (STD)

## Feature: Hard VM Reset (Force Reset)

**STP Reference:** [VIRTSTRAT-357: Hard VM Reset](https://issues.redhat.com/browse/VIRTSTRAT-357)
**Jira ID:** VIRTSTRAT-357
**Generated:** 2026-02-17

---

## Summary

This STD covers the Force/Hard Reset feature for VirtualMachineInstance (VMI) objects in OpenShift Virtualization. Tests verify the reset subresource API endpoint, `virtctl reset` command, RBAC enforcement, pod preservation after reset, and error handling for non-running/non-existent VMIs. The existing `test_vmi_reset.py` at `tests/virt/node/general/` covers the basic reset success scenario (boot count verification). This STD covers the remaining test scenarios from the STP that are not yet implemented.

---

## Test Files

### File: `tests/virt/node/general/test_vmi_reset.py`

```python
"""
VMI Hard Reset Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains tests for the VMI force/hard reset functionality,
verifying API-based reset, virtctl command, pod preservation, UID stability,
RBAC enforcement, and error handling for invalid reset targets.
"""

import logging
import shlex

import pytest
from pyhelper_utils.shell import run_ssh_commands

from utilities.virt import wait_for_running_vm

LOGGER = logging.getLogger(__name__)

pytestmark = pytest.mark.tier2


def get_vm_boot_count(vm):
    reboot_count = run_ssh_commands(
        host=vm.ssh_exec,
        commands=[shlex.split("journalctl --list-boots | wc -l")],
    )[0].strip()

    return int(reboot_count)


@pytest.fixture(scope="class")
def boot_count_before_reset(vm_for_test):
    return get_vm_boot_count(vm=vm_for_test)


@pytest.fixture(scope="class")
def vm_reset_and_running(vm_for_test):
    vm_for_test.vmi.reset()
    wait_for_running_vm(vm=vm_for_test)


@pytest.mark.parametrize("vm_for_test", [pytest.param("vm-for-reset-test")], indirect=True)
class TestVMIReset:
    """
    Tests for VMI reset via API subresource.

    Preconditions:
        - Running Fedora VM
        - Boot count recorded before reset
        - VMI reset performed via API and VM returned to Running state
    """

    @pytest.mark.polarion("CNV-12373")
    def test_reset_success(
        self,
        vm_for_test,
        boot_count_before_reset,
        vm_reset_and_running,
    ):
        """
        Test that VMI boot count increments by one after API reset.

        Steps:
            1. Get the current boot count from journalctl after reset

        Expected:
            - Boot count increased by exactly 1 compared to before reset
        """
        assert get_vm_boot_count(vm=vm_for_test) - boot_count_before_reset == 1, (
            "Expected 1 boot entry after VMI reset"
        )

    def test_vmi_uid_unchanged_after_reset(
        self,
        vm_for_test,
        boot_count_before_reset,
        vm_reset_and_running,
    ):
        """
        Test that the VMI UID remains the same after a reset.

        Steps:
            1. Compare the VMI UID after reset with the UID recorded before reset

        Expected:
            - VMI UID equals the UID from before the reset
        """
        pass

    def test_pod_not_rescheduled_after_reset(
        self,
        vm_for_test,
        boot_count_before_reset,
        vm_reset_and_running,
    ):
        """
        Test that the virt-launcher pod is not rescheduled after a VMI reset.

        Steps:
            1. Compare the virt-launcher pod name after reset with the pod name recorded before reset

        Expected:
            - Pod name equals the pod name from before the reset
        """
        pass


class TestVMIResetVirtctl:
    """
    Tests for VMI reset via virtctl command.

    Preconditions:
        - Running Fedora VM
    """

    def test_reset_via_virtctl(self):
        """
        Test that a running VMI can be reset using the virtctl reset command.

        Steps:
            1. Execute `virtctl reset <vm-name> -n <namespace>`
            2. Wait for VMI to return to Running state

        Expected:
            - VM is Running and SSH accessible after virtctl reset
        """
        pass


class TestVMIResetNegative:
    """
    Tests for VMI reset error handling on invalid targets.

    Preconditions:
        - Namespace available for test resources
    """

    def test_reset_fails_on_stopped_vmi(self):
        """
        [NEGATIVE] Test that resetting a stopped VMI returns an appropriate error.

        Preconditions:
            - VM created and in Stopped state (not started)

        Steps:
            1. Attempt to reset the stopped VMI via API

        Expected:
            - Reset operation raises an error indicating VMI is not running
        """
        pass

    def test_reset_fails_on_nonexistent_vmi(self):
        """
        [NEGATIVE] Test that resetting a non-existent VMI returns a not-found error.

        Steps:
            1. Attempt to reset a VMI name that does not exist in the namespace

        Expected:
            - Reset operation raises a not-found error
        """
        pass

    def test_reset_fails_on_paused_vmi(self):
        """
        [NEGATIVE] Test that resetting a paused VMI returns an appropriate error.

        Preconditions:
            - Running Fedora VM
            - VMI paused via pause API

        Steps:
            1. Attempt to reset the paused VMI via API

        Expected:
            - Reset operation raises an error indicating VMI is paused
        """
        pass


class TestVMIResetRBAC:
    """
    Tests for RBAC enforcement on VMI reset operations.

    Preconditions:
        - Running Fedora VM
        - ServiceAccount with edit ClusterRole bound in the test namespace
    """

    def test_edit_role_can_reset_vmi(self):
        """
        Test that a user with the edit ClusterRole can perform a VMI reset.

        Steps:
            1. Perform VMI reset using a client authenticated as the edit-role ServiceAccount

        Expected:
            - Reset operation succeeds without authorization error
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Method | Test ID | Tier | STP Scenario |
| --- | --- | --- | --- | --- | --- |
| `test_vmi_reset.py` | `TestVMIReset` | `test_reset_success` | CNV-12373 | Tier 2 | TS-01, TS-11 |
| `test_vmi_reset.py` | `TestVMIReset` | `test_vmi_uid_unchanged_after_reset` | TBD | Tier 2 | TS-03 |
| `test_vmi_reset.py` | `TestVMIReset` | `test_pod_not_rescheduled_after_reset` | TBD | Tier 2 | TS-01 (AC-2) |
| `test_vmi_reset.py` | `TestVMIResetVirtctl` | `test_reset_via_virtctl` | TBD | Tier 1 | TS-02 |
| `test_vmi_reset.py` | `TestVMIResetNegative` | `test_reset_fails_on_stopped_vmi` | TBD | Tier 1 | TS-05 |
| `test_vmi_reset.py` | `TestVMIResetNegative` | `test_reset_fails_on_nonexistent_vmi` | TBD | Tier 1 | TS-06 |
| `test_vmi_reset.py` | `TestVMIResetNegative` | `test_reset_fails_on_paused_vmi` | TBD | Tier 1 | TS-12 |
| `test_vmi_reset.py` | `TestVMIResetRBAC` | `test_edit_role_can_reset_vmi` | TBD | Tier 1 | TS-04 |

---

## Acceptance Criteria Traceability

| AC ID | Description | Test(s) |
| --- | --- | --- |
| AC-1 | VM owner can perform a reset of a VMI | `test_reset_success`, `test_reset_via_virtctl` |
| AC-2 | Reset does not require a new pod to be scheduled | `test_pod_not_rescheduled_after_reset`, `test_vmi_uid_unchanged_after_reset` |
| AC-3 | Reset exposed via subresource API | `test_reset_success`, `test_vmi_uid_unchanged_after_reset`, `test_pod_not_rescheduled_after_reset` |
| AC-4 | Reset accessible via virtctl command | `test_reset_via_virtctl` |
| AC-5 | RBAC permissions enforced | `test_edit_role_can_reset_vmi` |
| AC-6 | Reset fails gracefully on non-running VMIs | `test_reset_fails_on_stopped_vmi`, `test_reset_fails_on_nonexistent_vmi`, `test_reset_fails_on_paused_vmi` |

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Preconditions (where needed), Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass` (except existing `test_reset_success`)
- [x] Appropriate pytest markers documented
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/hard_vm_reset/std_virtstrat_357.md`
