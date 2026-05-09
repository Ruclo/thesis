# Software Test Description (STD)

## Feature: CPU Hotplug Logic Exceeding Maximum Limits

**STP Reference:** [stps/6.md](/home/fedora/thesis/stps/6.md)
**Jira ID:** [CNV-61263](https://issues.redhat.com/browse/CNV-61263)
**Bug Fix:** [CNV-57352](https://issues.redhat.com/browse/CNV-57352)
**Generated:** 2026-02-21

---

## Summary

Tests verifying that CPU hotplug correctly enforces MaxSockets limits based on maximum allowed vCPUs. The fix (kubevirt/kubevirt#14511) ensures MaxSockets is capped so that hotplugging CPUs cannot exceed the maximum vCPU count, preventing resource overcommit and unpredictable guest behavior.

Coverage includes:
- MaxSockets calculation respects maximum vCPU limits
- Hotplug operations are blocked when at the CPU limit
- Appropriate error messages are returned when attempting to exceed limits
- Full hotplug cycle operates correctly within enforced limits

---

## Test Files

### File: `tests/virt/node/hotplug/test_cpu_hotplug_max_limit.py`

```python
"""
CPU Hotplug Maximum Limit Tests

STP Reference: https://issues.redhat.com/browse/CNV-61263

This module contains tests verifying that CPU hotplug correctly enforces
MaxSockets limits based on maximum allowed vCPUs, preventing VMs from
exceeding their CPU allocation via hotplug operations.
"""

import pytest


class TestCPUHotplugMaxSocketsLimit:
    """
    Tests for CPU hotplug MaxSockets limit enforcement.

    Preconditions:
        - Running VM with CPU hotplug enabled
        - VM configured with a specific maximum vCPU count
        - VM started with initial CPU sockets below the maximum
    """

    def test_max_sockets_limited_by_max_vcpus(self):
        """
        Test that MaxSockets is calculated to not exceed the maximum allowed vCPUs.

        Steps:
            1. Inspect the VM spec for the calculated MaxSockets value

        Expected:
            - MaxSockets is less than or equal to the maximum allowed vCPUs
        """
        pass

    def test_hotplug_cpu_up_to_max_sockets(self):
        """
        Test that CPU hotplug succeeds when increasing sockets up to the MaxSockets limit.

        Steps:
            1. Hotplug CPU sockets to the MaxSockets limit value

        Expected:
            - Guest OS CPU count equals the MaxSockets limit
        """
        pass

    def test_hotplug_cpu_beyond_max_sockets_rejected(self):
        """
        [NEGATIVE] Test that CPU hotplug is rejected when attempting to exceed MaxSockets.

        Steps:
            1. Attempt to hotplug CPU sockets to a value exceeding MaxSockets

        Expected:
            - Operation is rejected with an error indicating the CPU limit has been exceeded
        """
        pass

    def test_error_message_when_exceeding_cpu_limit(self):
        """
        [NEGATIVE] Test that a clear error message is returned when attempting to exceed the CPU limit.

        Steps:
            1. Attempt to set CPU sockets above the MaxSockets limit via VM spec patch

        Expected:
            - Error message contains reference to the maximum CPU or socket limit
        """
        pass


class TestCPUHotplugFullCycleWithinLimits:
    """
    Tests for end-to-end CPU hotplug operations within enforced limits.

    Preconditions:
        - Running VM with CPU hotplug enabled
        - VM configured with 2 initial CPU sockets
        - VM MaxSockets set to the maximum allowed value
    """

    def test_hotplug_from_initial_to_max_within_limits(self):
        """
        Test that CPUs can be hotplugged from initial count to maximum allowed within limits.

        Steps:
            1. Hotplug CPU sockets from initial count to the MaxSockets limit
            2. Verify guest OS sees all hotplugged CPUs

        Expected:
            - Guest OS CPU count equals the MaxSockets limit
        """
        pass

    def test_no_further_hotplug_after_reaching_max(self):
        """
        [NEGATIVE] Test that no additional CPUs can be hotplugged after reaching the maximum limit.

        Preconditions:
            - VM CPU sockets already hotplugged to MaxSockets limit

        Steps:
            1. Attempt to hotplug one additional CPU socket beyond MaxSockets

        Expected:
            - Operation is rejected and CPU count remains at MaxSockets limit
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --- | --- | --- | --- | --- |
| `test_cpu_hotplug_max_limit.py` | `TestCPUHotplugMaxSocketsLimit` | 4 | P0/P1 | Tier 1 |
| `test_cpu_hotplug_max_limit.py` | `TestCPUHotplugFullCycleWithinLimits` | 2 | P1 | Tier 2 |

---

## Requirements Traceability

| Requirement ID | Requirement Summary | Test Method | Priority |
| --- | --- | --- | --- |
| CNV-61263 | MaxSockets limited based on max vCPUs | `test_max_sockets_limited_by_max_vcpus` | P0 |
| CNV-61263 | Hotplug succeeds up to limit | `test_hotplug_cpu_up_to_max_sockets` | P0 |
| CNV-61263 | Hotplug blocked beyond limit | `test_hotplug_cpu_beyond_max_sockets_rejected` | P0 |
| CNV-61263 | Error message for limit violation | `test_error_message_when_exceeding_cpu_limit` | P1 |
| CNV-61263 | Full hotplug cycle within limits | `test_hotplug_from_initial_to_max_within_limits` | P1 |
| CNV-61263 | No further hotplug at max | `test_no_further_hotplug_after_reaching_max` | P1 |

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] All STP scenarios covered (Scenarios 1-4)
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/cpu_hotplug_max_limit/std_cnv_61263.md`
