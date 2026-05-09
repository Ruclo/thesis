# Software Test Description (STD)

## Feature: CPU Hotplug MaxSockets Limit Enforcement

**STP Reference:** [stps/6.md](/home/fedora/thesis/stps/6.md)
**Jira ID:** [CNV-61263](https://issues.redhat.com/browse/CNV-61263) / [CNV-57352](https://issues.redhat.com/browse/CNV-57352)
**PR:** [kubevirt/kubevirt#14511](https://github.com/kubevirt/kubevirt/pull/14511)
**Generated:** 2026-02-23

---

## Summary

Tests verifying that CPU hotplug MaxSockets is properly capped based on the maximum allowed vCPUs (512) to prevent resource overcommit. The fix ensures that `MaxSockets * Cores * Threads` never exceeds the machine type's vCPU ceiling. When the calculated MaxSockets (from the hotplug ratio) would result in exceeding 512 total vCPUs, MaxSockets is automatically reduced to `512 / (Cores * Threads)`, but never below the originally configured socket count.

This STD covers four scenarios:
- MaxSockets calculation verification (capping logic)
- Hotplug rejection when exceeding MaxSockets
- Error message clarity when limits are violated
- Full hotplug cycle within capped limits

---

## Test Files

### File: `tests/virt/node/hotplug/test_cpu_hotplug_max_sockets.py`

```python
"""
CPU Hotplug MaxSockets Limit Tests

STP Reference: stps/6.md
Jira: CNV-61263 / CNV-57352
PR: https://github.com/kubevirt/kubevirt/pull/14511

This module contains tests verifying that CPU hotplug MaxSockets is properly
limited based on the maximum allowed vCPUs to prevent exceeding machine type
limits. The fix caps MaxSockets so that total vCPUs (MaxSockets * Cores * Threads)
never exceeds 512.
"""

import pytest


class TestCPUHotplugMaxSocketsLimit:
    """
    Tests for CPU hotplug MaxSockets limit enforcement.

    Markers:
        - s390x

    Preconditions:
        - Running RHEL VM with CPU hotplug enabled
        - VM configured with multi-core, multi-thread CPU topology
          where uncapped MaxSockets would exceed 512 total vCPUs
        - VMX CPU feature disabled on AMD64 clusters (workaround for CNV-62851)
    """

    def test_max_sockets_capped_to_respect_vcpu_limit(self):
        """
        Test that MaxSockets is automatically capped so total vCPUs do not exceed 512.

        Steps:
            1. Inspect the VMI spec for the calculated MaxSockets value

        Expected:
            - MaxSockets multiplied by cores multiplied by threads is less than or equal to 512
        """
        pass

    def test_hotplug_cpu_beyond_max_sockets_rejected(self):
        """
        [NEGATIVE] Test that hotplugging CPUs beyond the capped MaxSockets is rejected.

        Preconditions:
            - VM sockets set to MaxSockets value (at the limit)

        Steps:
            1. Attempt to set VM sockets to a value exceeding MaxSockets

        Expected:
            - Hotplug operation is rejected with an error
        """
        pass

    def test_error_message_indicates_limit_violation(self):
        """
        [NEGATIVE] Test that exceeding MaxSockets produces a clear error message.

        Preconditions:
            - VM sockets set to MaxSockets value (at the limit)

        Steps:
            1. Attempt to set VM sockets to a value exceeding MaxSockets
            2. Capture the error response

        Expected:
            - Error message contains indication that the socket count exceeds the maximum allowed
        """
        pass


class TestCPUHotplugFullCycleWithinLimits:
    """
    Tests for complete CPU hotplug cycle respecting MaxSockets cap.

    Markers:
        - s390x

    Preconditions:
        - Running RHEL VM with CPU hotplug enabled
        - VM starting with 2 CPU sockets
        - MaxSockets capped based on 512 vCPU limit
        - VMX CPU feature disabled on AMD64 clusters (workaround for CNV-62851)
    """

    def test_hotplug_cpu_to_max_sockets_succeeds(self):
        """
        Test that CPU can be hotplugged up to the capped MaxSockets value.

        Steps:
            1. Hotplug VM sockets from initial count to the capped MaxSockets value

        Expected:
            - Guest OS CPU count equals MaxSockets multiplied by cores multiplied by threads
        """
        pass

    def test_guest_cpu_count_correct_at_max_sockets(self):
        """
        Test that the guest OS reports the correct CPU count after hotplugging to max.

        Preconditions:
            - VM sockets hotplugged to MaxSockets value

        Steps:
            1. Query CPU count inside the guest OS

        Expected:
            - Guest OS CPU count equals the total vCPUs at MaxSockets
        """
        pass

    def test_further_hotplug_rejected_after_reaching_max(self):
        """
        [NEGATIVE] Test that no further CPU hotplug is allowed after reaching MaxSockets.

        Preconditions:
            - VM sockets hotplugged to MaxSockets value

        Steps:
            1. Attempt to hotplug one additional socket beyond MaxSockets

        Expected:
            - Hotplug operation is rejected with an error
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --- | --- | --- | --- | --- |
| `test_cpu_hotplug_max_sockets.py` | `TestCPUHotplugMaxSocketsLimit` | 3 | P0/P1 | Tier 1 |
| `test_cpu_hotplug_max_sockets.py` | `TestCPUHotplugFullCycleWithinLimits` | 3 | P1 | Tier 2 |

### STP Scenario Traceability

| STP Scenario | Test Method | Priority |
| --- | --- | --- |
| Scenario 1: MaxSockets Calculation | `test_max_sockets_capped_to_respect_vcpu_limit` | P0 |
| Scenario 2: Hotplug at Limit | `test_hotplug_cpu_beyond_max_sockets_rejected` | P0 |
| Scenario 3: Error Message for Limit | `test_error_message_indicates_limit_violation` | P1 |
| Scenario 4: Full Hotplug Cycle | `test_hotplug_cpu_to_max_sockets_succeeds`, `test_guest_cpu_count_correct_at_max_sockets`, `test_further_hotplug_rejected_after_reaching_max` | P1 |

---

## Checklist

- [x] STP link in module docstring
- [x] All STP scenarios covered (4 scenarios mapped to 6 tests)
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/cpu_hotplug_max_sockets/std_cnv_61263.md`
