# Software Test Description (STD)

## Feature: Windows Guest Agent OS/Hostname Info Display

**STP Reference:** /home/jzo/thesis/stps/7.md
**Jira ID:** CNV-61262 (Bug Fix: CNV-56888)
**Generated:** 2026-02-11

---

## Summary

This STD covers tests for verifying that Windows VMs correctly display OS info and hostname via the guest agent. The bug fix (CNV-56888) ensures `domain.Status.OSInfo` is not empty when the QEMU guest agent is running. Tests verify OS info display through the VMI status API, hostname correctness, persistence after guest reboot, and dynamic detection when the guest agent service starts.

---

## Test Files

### File: `tests/virt/cluster/guest_agent/test_windows_guest_agent_osinfo.py`

```python
"""
Windows Guest Agent OS/Hostname Info Display Tests

STP Reference: /home/jzo/thesis/stps/7.md

This module contains tests for verifying that Windows VMs correctly report
OS information and hostname through the QEMU guest agent. The bug fix
(CNV-56888) addresses a race condition where domain.Status.OSInfo was
sometimes empty despite the guest agent running.
"""

import pytest


pytestmark = [pytest.mark.special_infra, pytest.mark.high_resource_vm]


class TestWindowsGuestAgentOSInfo:
    """
    Tests for Windows guest agent OS and hostname info display.

    Preconditions:
        - Running Windows VM with QEMU guest agent installed and active
        - VM is SSH accessible
    """

    def test_vmi_os_info_populated(self):
        """
        Test that VMI status contains OS info when Windows guest agent is running.

        Steps:
            1. Query VMI status guestOSInfo field

        Expected:
            - guestOSInfo contains a non-empty OS id (e.g., "mswindows")
        """
        pass

    def test_os_version_matches_guest(self):
        """
        Test that VMI-reported OS version matches the actual Windows OS version.

        Steps:
            1. Compare VMI guestOSInfo OS fields against Windows CIM instance data

        Expected:
            - VMI OS info matches Windows-reported OS info with no data mismatches
        """
        pass

    def test_hostname_matches_guest(self):
        """
        Test that VMI-reported hostname matches the actual Windows hostname.

        Steps:
            1. Compare virtctl guestosinfo hostname against Windows CIM instance hostname

        Expected:
            - Hostname from virtctl equals hostname from Windows OS
        """
        pass

    def test_guest_agent_version_reported(self):
        """
        Test that the guest agent version is correctly reported via virtctl.

        Steps:
            1. Compare virtctl guestosinfo guest agent version against version reported inside Windows

        Expected:
            - Guest agent version from virtctl equals version from Windows OS
        """
        pass


class TestWindowsGuestAgentInfoPersistence:
    """
    Tests for Windows guest agent info persistence across VM lifecycle events.

    Preconditions:
        - Running Windows VM with QEMU guest agent installed and active
        - VM is SSH accessible
        - VMI guestOSInfo is confirmed populated before lifecycle event
    """

    def test_os_info_persists_after_guest_reboot(self):
        """
        Test that OS info is correctly reported after a Windows guest reboot.

        Steps:
            1. Reboot the Windows VM from within the guest and wait for agent reconnection

        Expected:
            - Guest agent data is available over time after reboot
        """
        pass

    def test_guest_agent_data_stable_over_time(self):
        """
        Test that guest agent data remains consistently available over time.

        Steps:
            1. Poll virtctl guestosinfo repeatedly over a time window

        Expected:
            - Guest agent OS info does not become empty during polling
        """
        pass


class TestWindowsGuestAgentDetection:
    """
    Tests for dynamic detection of Windows guest agent service state changes.

    Preconditions:
        - Running Windows VM with QEMU guest agent installed
        - VM is SSH accessible
    """

    def test_os_info_appears_when_agent_starts(self):
        """
        Test that OS info appears in VMI status when guest agent service starts.

        Preconditions:
            - QEMU guest agent service is initially stopped inside the Windows guest

        Steps:
            1. Start the QEMU guest agent service inside the Windows guest
            2. Wait for VMI guestOSInfo to be populated

        Expected:
            - guestOSInfo contains a non-empty OS id after agent service starts
        """
        pass

    def test_no_os_info_when_agent_stopped(self):
        """
        [NEGATIVE] Test that OS info is not available when guest agent service is stopped.

        Steps:
            1. Stop the QEMU guest agent service inside the Windows guest
            2. Wait for VMI guestOSInfo to reflect agent absence

        Expected:
            - guestOSInfo does not contain OS id
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --------- | ---------- | ---------- | -------- | ---- |
| `test_windows_guest_agent_osinfo.py` | `TestWindowsGuestAgentOSInfo` | 4 | P0 | Tier 1 |
| `test_windows_guest_agent_osinfo.py` | `TestWindowsGuestAgentInfoPersistence` | 2 | P1 | Tier 1 |
| `test_windows_guest_agent_osinfo.py` | `TestWindowsGuestAgentDetection` | 2 | P1 | Tier 1 |

---

## Requirements-to-Tests Mapping

| Requirement | Test(s) |
| ----------- | ------- |
| OS info displays correctly | `test_vmi_os_info_populated`, `test_os_version_matches_guest` |
| Hostname displays correctly | `test_hostname_matches_guest` |
| No false "Guest Agent Required" message | `test_os_info_appears_when_agent_starts`, `test_no_os_info_when_agent_stopped` |
| Info persists after reboot | `test_os_info_persists_after_guest_reboot`, `test_guest_agent_data_stable_over_time` |
| Guest agent version reported | `test_guest_agent_version_reported` |

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/windows_guest_agent_osinfo/std_cnv_61262.md`
