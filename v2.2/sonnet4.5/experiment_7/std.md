# Software Test Description (STD)

## Feature: Windows Guest Agent OS/Hostname Info Display

**STP Reference:** [/thesis/stps/7.md](/thesis/stps/7.md)
**Jira ID:** CNV-61262
**Bug Fix:** CNV-56888
**Generated:** 2026-02-10

---

## Summary

This STD covers automated tests for verifying that Windows VM operating system information and hostname are displayed correctly when the QEMU guest agent is running. The tests validate the bug fix that ensures `domain.Status.OSInfo` is properly populated and prevents false "Guest Agent Required" messages from appearing when the guest agent is actually running.

The tests focus on:
- OS version display accuracy for Windows VMs
- Hostname display accuracy
- Information persistence across VM reboots
- Detection of guest agent start/stop events
- Compatibility across different Windows versions

---

## Test Files

### File: `tests/virt/guest_agent/test_windows_osinfo_display.py`

```python
"""
Windows Guest Agent OS and Hostname Info Display Tests

STP Reference: /thesis/stps/7.md
Jira: CNV-61262
Bug Fix: CNV-56888

This module contains tests for verifying that Windows VM operating system
information and hostname are displayed correctly when qemu-guest-agent is running.

Tests validate the fix for CNV-56888 which ensures domain.Status.OSInfo is
properly populated and prevents false "Guest Agent Required" messages.
"""

import pytest


class TestWindowsGuestAgentInfo:
    """
    Tests for Windows VM guest agent OS and hostname information display.

    Markers:
        - tier1
        - gating

    Preconditions:
        - Windows VM with qemu-guest-agent installed
        - virtio-serial driver installed in Windows guest
        - qemu-guest-agent service running in Windows guest
        - VMI is in Running status
    """

    def test_windows_os_version_displayed_correctly(self):
        """
        Test that Windows OS version is displayed correctly when guest agent is running.

        Steps:
            1. Start Windows VM with qemu-guest-agent running
            2. Wait for guest agent to report to virt-handler
            3. Get VMI status and check domain.Status.OSInfo field
            4. Extract OS version from OSInfo

        Expected:
            - domain.Status.OSInfo is not empty
            - OS version matches actual Windows version running in guest
            - No "Guest Agent Required" message is shown
        """
        pass

    def test_windows_hostname_displayed_correctly(self):
        """
        Test that Windows hostname is displayed correctly when guest agent is running.

        Steps:
            1. Start Windows VM with specific hostname configured in guest
            2. Wait for guest agent to report to virt-handler
            3. Get VMI status and check domain.Status.OSInfo field
            4. Extract hostname from OSInfo

        Expected:
            - domain.Status.OSInfo contains hostname field
            - Hostname matches the configured hostname in Windows guest
        """
        pass

    def test_osinfo_persists_after_vm_reboot(self):
        """
        Test that OS and hostname info persists after VM reboot.

        Preconditions:
            - Windows VM is running with OS info already displayed

        Steps:
            1. Verify domain.Status.OSInfo is populated with OS version and hostname
            2. Initiate guest reboot from within Windows VM
            3. Wait for VM to shutdown and restart
            4. Wait for guest agent to reconnect after reboot
            5. Check domain.Status.OSInfo again

        Expected:
            - domain.Status.OSInfo is populated before reboot
            - domain.Status.OSInfo is populated after reboot
            - OS version and hostname remain correct after reboot
        """
        pass

    def test_osinfo_appears_when_guest_agent_starts(self):
        """
        Test that OS info appears when guest agent service starts.

        Preconditions:
            - Windows VM is running with qemu-guest-agent service stopped

        Steps:
            1. Start Windows VM
            2. Stop qemu-guest-agent service inside Windows guest
            3. Verify domain.Status.OSInfo is empty or shows "Guest Agent Required"
            4. Start qemu-guest-agent service inside Windows guest
            5. Wait for guest agent to report to virt-handler
            6. Check domain.Status.OSInfo

        Expected:
            - domain.Status.OSInfo is empty when agent is stopped
            - domain.Status.OSInfo is populated after agent starts
            - OS version and hostname are displayed correctly after agent starts
        """
        pass


class TestWindowsGuestAgentInfoMultipleVersions:
    """
    Tests for Windows guest agent info display across different Windows versions.

    Markers:
        - tier2

    Parametrize:
        - windows_version: [windows-10, windows-server-2019, windows-server-2022]

    Preconditions:
        - Windows VM of specified version with qemu-guest-agent installed
        - virtio-serial driver installed in Windows guest
        - qemu-guest-agent service running
    """

    def test_osinfo_display_for_windows_version(self):
        """
        Test that OS info displays correctly for different Windows versions.

        Steps:
            1. Start Windows VM of specified version
            2. Wait for guest agent to report
            3. Get VMI status and check domain.Status.OSInfo
            4. Verify OS version string matches expected format for Windows version

        Expected:
            - domain.Status.OSInfo is populated for all Windows versions
            - OS version string correctly identifies Windows 10, Server 2019, or Server 2022
        """
        pass


class TestWindowsGuestAgentInfoEdgeCases:
    """
    Tests for edge cases and race conditions in guest agent info reporting.

    Markers:
        - tier2

    Preconditions:
        - Windows VM with qemu-guest-agent installed
    """

    def test_osinfo_after_rapid_vm_restarts(self):
        """
        Test that OS info remains consistent after rapid VM restarts.

        Steps:
            1. Start Windows VM and verify domain.Status.OSInfo is populated
            2. Stop VM
            3. Immediately start VM again
            4. Repeat steps 2-3 for 3 cycles
            5. Verify domain.Status.OSInfo after final start

        Expected:
            - domain.Status.OSInfo is consistently populated after each restart
            - No race condition causes OSInfo to remain empty
        """
        pass

    def test_osinfo_after_guest_agent_crash_and_recovery(self):
        """
        Test that OS info recovers after guest agent process crashes and restarts.

        Steps:
            1. Start Windows VM with guest agent running
            2. Verify domain.Status.OSInfo is populated
            3. Kill qemu-guest-agent process inside guest (simulating crash)
            4. Wait for Windows service manager to restart qemu-ga
            5. Check domain.Status.OSInfo

        Expected:
            - domain.Status.OSInfo is populated initially
            - domain.Status.OSInfo may become empty after crash
            - domain.Status.OSInfo is repopulated after service recovery
        """
        pass

    def test_osinfo_not_empty_on_first_boot(self):
        """
        Test that domain.Status.OSInfo is populated on first VM boot (regression test for CNV-56888).

        Steps:
            1. Create new Windows VM with guest agent pre-installed
            2. Start VM for the first time
            3. Wait for guest agent to report
            4. Check domain.Status.OSInfo immediately after agent reports

        Expected:
            - domain.Status.OSInfo is not empty on first boot
            - No race condition prevents OSInfo from being populated initially
        """
        pass
```

---

### File: `tests/virt/guest_agent/conftest.py`

```python
"""
Shared fixtures for Windows guest agent tests.

This module provides fixtures for Windows VMs with guest agent configurations.
"""

import pytest


@pytest.fixture(scope="class")
def windows_vm_with_guest_agent(request):
    """
    Provide a Windows VM with qemu-guest-agent installed and running.

    Yields:
        VirtualMachine: Windows VM with guest agent service running

    Teardown:
        - Stops and deletes the Windows VM
    """
    pass


@pytest.fixture(scope="class")
def windows_vm_guest_agent_stopped(request):
    """
    Provide a Windows VM with qemu-guest-agent installed but service stopped.

    Yields:
        VirtualMachine: Windows VM with guest agent service stopped

    Teardown:
        - Stops and deletes the Windows VM
    """
    pass


@pytest.fixture(scope="module")
def windows_10_vm(request):
    """
    Provide a Windows 10 VM with qemu-guest-agent.

    Yields:
        VirtualMachine: Windows 10 VM with guest agent

    Teardown:
        - Stops and deletes the VM
    """
    pass


@pytest.fixture(scope="module")
def windows_server_2019_vm(request):
    """
    Provide a Windows Server 2019 VM with qemu-guest-agent.

    Yields:
        VirtualMachine: Windows Server 2019 VM with guest agent

    Teardown:
        - Stops and deletes the VM
    """
    pass


@pytest.fixture(scope="module")
def windows_server_2022_vm(request):
    """
    Provide a Windows Server 2022 VM with qemu-guest-agent.

    Yields:
        VirtualMachine: Windows Server 2022 VM with guest agent

    Teardown:
        - Stops and deletes the VM
    """
    pass
```

---

### File: `tests/virt/guest_agent/utils.py`

```python
"""
Utility functions for Windows guest agent tests.
"""


def get_osinfo_from_vmi(vmi):
    """
    Extract OSInfo from VMI domain status.

    Args:
        vmi: VirtualMachineInstance resource

    Returns:
        dict: OSInfo data containing OS version, hostname, etc.
              Empty dict if OSInfo is not populated.
    """
    pass


def wait_for_guest_agent_reporting(vmi, timeout=300):
    """
    Wait for guest agent to start reporting to virt-handler.

    Args:
        vmi: VirtualMachineInstance resource
        timeout: Maximum time to wait in seconds

    Returns:
        bool: True if guest agent starts reporting within timeout

    Raises:
        TimeoutError: If guest agent does not report within timeout
    """
    pass


def stop_guest_agent_service(vm):
    """
    Stop qemu-guest-agent service inside Windows guest.

    Args:
        vm: VirtualMachine resource with SSH access

    Returns:
        bool: True if service stopped successfully
    """
    pass


def start_guest_agent_service(vm):
    """
    Start qemu-guest-agent service inside Windows guest.

    Args:
        vm: VirtualMachine resource with SSH access

    Returns:
        bool: True if service started successfully
    """
    pass


def get_windows_hostname_from_guest(vm):
    """
    Get the configured hostname from inside Windows guest.

    Args:
        vm: VirtualMachine resource with SSH/WinRM access

    Returns:
        str: Hostname configured in Windows
    """
    pass


def set_windows_hostname_in_guest(vm, hostname):
    """
    Set hostname inside Windows guest.

    Args:
        vm: VirtualMachine resource with SSH/WinRM access
        hostname: New hostname to set

    Returns:
        bool: True if hostname set successfully
    """
    pass


def reboot_windows_guest(vm):
    """
    Initiate reboot from within Windows guest OS.

    Args:
        vm: VirtualMachine resource with SSH/WinRM access

    Returns:
        bool: True if reboot initiated successfully
    """
    pass


def kill_guest_agent_process(vm):
    """
    Kill qemu-guest-agent process inside Windows guest (simulate crash).

    Args:
        vm: VirtualMachine resource with SSH/WinRM access

    Returns:
        bool: True if process killed successfully
    """
    pass
```

---

## Test Coverage Summary

| Test File                          | Test Class                                  | Test Count | Priority | Tier  |
| :--------------------------------- | :------------------------------------------ | :--------- | :------- | :---- |
| `test_windows_osinfo_display.py`   | `TestWindowsGuestAgentInfo`                 | 4          | P0/P1    | T1    |
| `test_windows_osinfo_display.py`   | `TestWindowsGuestAgentInfoMultipleVersions` | 1          | P2       | T2    |
| `test_windows_osinfo_display.py`   | `TestWindowsGuestAgentInfoEdgeCases`        | 3          | P1/P2    | T2    |
| **Total**                          |                                             | **8**      |          |       |

---

## Requirements Traceability

| Requirement ID | Test(s)                                                      | Coverage |
| :------------- | :----------------------------------------------------------- | :------- |
| CNV-61262      | `test_windows_os_version_displayed_correctly`                | ✓        |
| CNV-61262      | `test_windows_hostname_displayed_correctly`                  | ✓        |
| CNV-61262      | `test_osinfo_persists_after_vm_reboot`                       | ✓        |
| CNV-61262      | `test_osinfo_appears_when_guest_agent_starts`                | ✓        |
| CNV-56888      | `test_osinfo_not_empty_on_first_boot` (regression test)      | ✓        |

---

## Checklist

- [x] All STP scenarios covered (Scenarios 1-5)
- [x] Each test verifies ONE thing
- [x] Negative tests marked with `[NEGATIVE]` (none in this STD - all positive tests)
- [x] Markers documented (tier1, tier2, gating)
- [x] Parametrization documented (windows_version for multi-version test)
- [x] Tests grouped in classes with shared preconditions
- [x] Module docstring with STP reference
- [x] Utility functions defined for common operations
- [x] Fixtures defined for Windows VMs with guest agent
- [x] All tests have: description, Preconditions, Steps, Expected
- [x] Test methods contain only `pass` (implementation pending)

---

## Implementation Notes

### Key Implementation Considerations

1. **Windows VM Setup:**
   - Requires Windows VM images with qemu-guest-agent pre-installed
   - virtio-serial driver must be present for guest-host communication
   - Consider using pre-configured Windows images to reduce test setup time

2. **Guest Agent Communication:**
   - Tests should wait for guest agent to report (not just VM Running status)
   - Use `wait_for_guest_agent_reporting()` utility to avoid race conditions
   - Monitor `domain.Status.OSInfo` field in VMI resource

3. **Windows-Specific Operations:**
   - Implement WinRM or SSH access for in-guest operations
   - Service management uses Windows service control (sc.exe or PowerShell)
   - Hostname operations use PowerShell cmdlets

4. **Test Data Validation:**
   - OS version strings vary by Windows version (e.g., "Microsoft Windows 10", "Microsoft Windows Server 2019")
   - Hostname validation should be case-insensitive
   - Empty OSInfo field vs. missing OSInfo field should be handled

5. **Timing Considerations:**
   - Guest agent may take time to start after VM boot
   - After service restart, allow time for agent to reconnect
   - Use appropriate timeouts in wait functions (suggested: 300s for first boot, 60s for service restart)

6. **Markers:**
   - Tier 1 tests are gating tests (P0/P1 priority)
   - Tier 2 tests cover additional scenarios and edge cases
   - Consider adding Windows-specific marker if needed

---

## Future Enhancements

- Add UI validation tests to verify info display in OpenShift Console
- Add tests for partial OSInfo scenarios (e.g., hostname present but OS version missing)
- Add performance tests for guest agent reporting latency
- Add tests for guest agent version compatibility
