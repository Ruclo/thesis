# Software Test Description (STD)

## Feature: CPU Hotplug Logic Exceeding Maximum Limits

**STP Reference:** [CNV-61263](https://issues.redhat.com/browse/CNV-61263)
**Jira ID:** CNV-61263
**Bug Fix Tracking:** [CNV-57352](https://issues.redhat.com/browse/CNV-57352)

---

## Summary

This STD covers tests for the CPU hotplug MaxSockets limiting fix. The fix ensures that MaxSockets is properly limited based on the maximum allowed vCPUs, preventing users from hotplugging CPUs beyond safe limits. Tests verify the MaxSockets calculation, the enforcement of limits during hotplug operations, appropriate error handling, and a full hotplug cycle within limits.

---

## Test Files

### File: `tests/virt/node/hotplug/test_cpu_hotplug_max_sockets.py`

```python
"""
CPU Hotplug MaxSockets Limit Tests

STP Reference: https://issues.redhat.com/browse/CNV-61263

This module contains tests verifying that MaxSockets is properly limited
based on the maximum allowed vCPUs, preventing CPU hotplug from exceeding
safe limits.

Related PR: https://github.com/kubevirt/kubevirt/pull/14511
"""

import pytest


class TestMaxSocketsCalculation:
    """
    Tests for MaxSockets calculation based on maximum vCPUs.

    Preconditions:
        - Running VM with CPU hotplug enabled
        - VM created with a specific maxSockets value
    """

    def test_max_sockets_does_not_exceed_max_vcpus(self):
        """
        Test that MaxSockets is limited to not exceed the maximum allowed vCPUs.

        Steps:
            1. Read the VM spec to get the configured maxSockets value

        Expected:
            - maxSockets is less than or equal to the maximum allowed vCPUs
        """
        pass

    def test_vm_reports_correct_max_sockets_in_status(self):
        """
        Test that the VM status reflects the correctly calculated MaxSockets value.

        Steps:
            1. Read the VM status CPU topology

        Expected:
            - VM status maxSockets equals the configured maxSockets from the VM spec
        """
        pass


class TestCPUHotplugAtLimit:
    """
    Tests for CPU hotplug behavior when approaching and at the MaxSockets limit.

    Preconditions:
        - Running VM with CPU hotplug enabled
        - VM created with maxSockets set to maximum allowed value
        - VM started with sockets less than maxSockets
    """

    def test_hotplug_cpu_up_to_max_sockets(self):
        """
        Test that CPU hotplug succeeds when increasing sockets up to maxSockets.

        Steps:
            1. Hotplug VM CPU sockets to the maxSockets value

        Expected:
            - Guest OS CPU count equals maxSockets value
        """
        pass

    def test_hotplug_cpu_beyond_max_sockets_is_rejected(self):
        """
        [NEGATIVE] Test that CPU hotplug is rejected when attempting to exceed maxSockets.

        Steps:
            1. Attempt to hotplug VM CPU sockets to a value greater than maxSockets

        Expected:
            - API returns an error indicating the socket count exceeds the maximum allowed
        """
        pass


class TestCPUHotplugErrorHandling:
    """
    Tests for error handling when CPU hotplug limit is exceeded.

    Preconditions:
        - Running VM with CPU hotplug enabled
        - VM created with a defined maxSockets limit
    """

    def test_error_message_when_exceeding_max_sockets(self):
        """
        [NEGATIVE] Test that a clear error message is returned when exceeding maxSockets.

        Steps:
            1. Attempt to set CPU sockets to a value exceeding maxSockets via VM spec patch

        Expected:
            - Error message contains indication that requested sockets exceed the maximum allowed
        """
        pass


class TestCPUHotplugFullCycle:
    """
    Tests for a full CPU hotplug cycle within MaxSockets limits.

    Preconditions:
        - Running VM with CPU hotplug enabled
        - VM created with initial sockets of 2 and maxSockets set to maximum allowed
    """

    def test_hotplug_to_max_and_guest_sees_all_cpus(self):
        """
        Test that hotplugging to the maximum allowed sockets results in the guest OS seeing all CPUs.

        Steps:
            1. Hotplug VM CPU sockets incrementally to maxSockets value

        Expected:
            - Guest OS CPU count equals maxSockets value
        """
        pass

    def test_no_further_hotplug_allowed_at_max(self):
        """
        [NEGATIVE] Test that no further CPU hotplug is allowed once maxSockets is reached.

        Preconditions:
            - VM CPU sockets already at maxSockets value

        Steps:
            1. Attempt to hotplug one additional CPU socket beyond maxSockets

        Expected:
            - API returns an error rejecting the request
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --- | --- | --- | --- | --- |
| `test_cpu_hotplug_max_sockets.py` | `TestMaxSocketsCalculation` | 2 | P0 | Tier 1 |
| `test_cpu_hotplug_max_sockets.py` | `TestCPUHotplugAtLimit` | 2 | P0 | Tier 1 |
| `test_cpu_hotplug_max_sockets.py` | `TestCPUHotplugErrorHandling` | 1 | P1 | Tier 1 |
| `test_cpu_hotplug_max_sockets.py` | `TestCPUHotplugFullCycle` | 2 | P1 | Tier 2 |

---

## Requirements Traceability

| Requirement | STP Scenario | Test Method | Priority |
| --- | --- | --- | --- |
| MaxSockets limited based on max vCPUs | Scenario 1 | `test_max_sockets_does_not_exceed_max_vcpus` | P0 |
| MaxSockets reflected in VM status | Scenario 1 | `test_vm_reports_correct_max_sockets_in_status` | P0 |
| Hotplug succeeds up to limit | Scenario 2 | `test_hotplug_cpu_up_to_max_sockets` | P0 |
| Hotplug blocked beyond limit | Scenario 2 | `test_hotplug_cpu_beyond_max_sockets_is_rejected` | P0 |
| Clear error message at limit | Scenario 3 | `test_error_message_when_exceeding_max_sockets` | P1 |
| Full cycle within limits | Scenario 4 | `test_hotplug_to_max_and_guest_sees_all_cpus` | P1 |
| No further hotplug at max | Scenario 4 | `test_no_further_hotplug_allowed_at_max` | P1 |

---

## Checklist

- [x] All STP scenarios covered
- [x] Each test verifies ONE thing
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Markers documented
- [x] Parametrization documented where needed
- [x] STP link in module docstring
- [x] Tests grouped in class with shared preconditions
- [x] Each test has: description, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Test methods contain only `pass`
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/cpu_hotplug_max_limits/std_cnv_61263.md`
