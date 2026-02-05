# Software Test Description (STD)

## Feature: Windows Guest Agent OS/Hostname Info Display

**STP Reference:** ../thesis/stps/7.md
**Jira ID:** CNV-61262 (Enhancement), CNV-56888 (Bug Fix)
**Related PR:** [kubevirt/kubevirt#14232](https://github.com/kubevirt/kubevirt/pull/14232)
**Generated:** 2026-02-04

---

## Summary

This STD covers comprehensive testing for the Windows guest agent OS and hostname information display issue. The bug fix ensures that `domain.Status.OSInfo` is correctly populated when the qemu-guest-agent is running, preventing false "Guest Agent Required" messages in the UI.

**Test Coverage:**
- OS version display verification for Windows VMs
- Hostname display verification for Windows VMs
- Guest agent detection when starting after VM boot
- Information persistence across VM reboots
- Compatibility across different Windows versions (Windows 10, Server 2019, Server 2022)

**Priority:** P0 (Critical bug fix affecting user experience)

---

## Test Files

### File: `tests/virt/node/general/test_windows_guest_agent_osinfo.py`

```python
"""
Windows Guest Agent OS/Hostname Info Display Tests

STP Reference: ../thesis/stps/7.md
Jira: CNV-61262, CNV-56888
PR: https://github.com/kubevirt/kubevirt/pull/14232

This module contains tests verifying that Windows VMs correctly display
OS version and hostname information when qemu-guest-agent is running.

Bug Fix: Ensures domain.Status.OSInfo is not empty despite guest agent
reporting correctly, preventing false "Guest Agent Required" messages.
"""

import logging

import pytest

from utilities.ssp import validate_os_info_vmi_vs_windows_os
from utilities.virt import get_guest_os_info, running_vm

LOGGER = logging.getLogger(__name__)


pytestmark = [
    pytest.mark.gating,
    pytest.mark.post_upgrade,
    pytest.mark.special_infra,
    pytest.mark.high_resource_vm,
]


class TestWindowsGuestAgentOSInfo:
    """
    Tests for Windows guest agent OS and hostname information display.

    Markers:
        - gating
        - post_upgrade

    Preconditions:
        - Windows VM with qemu-guest-agent installed
        - virtio-serial driver installed for guest-host communication
        - Guest agent service running
    """

    def test_windows_os_version_display(self, windows_vm_with_guest_agent):
        """
        Test that Windows OS version is displayed correctly when guest agent is running.

        Steps:
            1. Get VMI status guestOSInfo field
            2. Verify OS info is populated (not empty)
            3. Compare VMI OS info with actual Windows OS version from guest

        Expected:
            - VMI guestOSInfo field is not empty
            - OS version matches Windows version reported by guest OS
            - No "Guest Agent Required" message displayed
        """
        pass

    def test_windows_hostname_display(self, windows_vm_with_guest_agent):
        """
        Test that Windows hostname is displayed correctly when guest agent is running.

        Steps:
            1. Get VMI status guestOSInfo field
            2. Verify hostname is populated
            3. Get actual hostname from Windows guest OS
            4. Compare VMI hostname with guest OS hostname

        Expected:
            - VMI guestOSInfo contains hostname field
            - Hostname matches the actual Windows hostname
        """
        pass

    def test_osinfo_persistence_after_vm_reboot(self, windows_vm_with_guest_agent):
        """
        Test that OS and hostname info persists and is restored after VM reboot.

        Preconditions:
            - Windows VM running with OS/hostname info displayed

        Steps:
            1. Verify OS info is displayed before reboot
            2. Reboot the Windows VM (guest restart)
            3. Wait for VM to become running
            4. Wait for guest agent to reconnect
            5. Verify OS info is displayed again

        Expected:
            - OS info is displayed before reboot
            - OS info is restored and displayed after reboot
            - No "Guest Agent Required" message after reboot
        """
        pass

    def test_osinfo_after_guest_agent_restart(self, windows_vm_with_guest_agent):
        """
        Test that OS info appears when guest agent service is started.

        Preconditions:
            - Windows VM running with qemu-guest-agent service stopped

        Steps:
            1. Stop qemu-guest-agent service in guest
            2. Verify VMI guestOSInfo is empty or shows "Guest Agent Required"
            3. Start qemu-guest-agent service in guest
            4. Wait for agent to report
            5. Verify OS info is now displayed

        Expected:
            - OS info appears after agent starts
            - VMI guestOSInfo is populated with correct OS version and hostname
        """
        pass


class TestWindowsGuestAgentOSInfoMultipleVersions:
    """
    Tests for Windows guest agent OS info across different Windows versions.

    Markers:
        - post_upgrade

    Parametrize:
        - windows_version: [windows10, windows-server-2019, windows-server-2022]

    Preconditions:
        - Windows VM with specified version
        - qemu-guest-agent installed
        - virtio-serial driver installed
    """

    def test_os_version_display_windows_10(self, windows_10_vm_with_guest_agent):
        """
        Test that Windows 10 OS version is displayed correctly.

        Steps:
            1. Get VMI status guestOSInfo field
            2. Verify OS info contains Windows 10 version

        Expected:
            - VMI guestOSInfo shows correct Windows 10 version
        """
        pass

    def test_os_version_display_windows_server_2019(self, windows_server_2019_vm_with_guest_agent):
        """
        Test that Windows Server 2019 OS version is displayed correctly.

        Steps:
            1. Get VMI status guestOSInfo field
            2. Verify OS info contains Windows Server 2019 version

        Expected:
            - VMI guestOSInfo shows correct Windows Server 2019 version
        """
        pass

    def test_os_version_display_windows_server_2022(self, windows_server_2022_vm_with_guest_agent):
        """
        Test that Windows Server 2022 OS version is displayed correctly.

        Steps:
            1. Get VMI status guestOSInfo field
            2. Verify OS info contains Windows Server 2022 version

        Expected:
            - VMI guestOSInfo shows correct Windows Server 2022 version
        """
        pass


class TestWindowsGuestAgentOSInfoNegative:
    """
    Negative tests for Windows guest agent OS info display.

    Markers:
        - gating

    Preconditions:
        - Windows VM without guest agent installed or running
    """

    def test_osinfo_empty_without_guest_agent(self, windows_vm_without_guest_agent):
        """
        [NEGATIVE] Test that VMI shows "Guest Agent Required" when agent is not running.

        Preconditions:
            - Windows VM running
            - qemu-guest-agent service stopped or not installed

        Steps:
            1. Get VMI status guestOSInfo field
            2. Verify field is empty or not populated with OS details

        Expected:
            - VMI guestOSInfo is empty or minimal
            - "Guest Agent Required" message is appropriate
        """
        pass

    def test_osinfo_empty_without_virtio_serial(self, windows_vm_without_virtio_serial):
        """
        [NEGATIVE] Test that VMI shows no OS info when virtio-serial driver is missing.

        Preconditions:
            - Windows VM running
            - virtio-serial driver not installed
            - qemu-guest-agent installed but cannot communicate

        Steps:
            1. Get VMI status guestOSInfo field
            2. Verify communication channel is not established

        Expected:
            - VMI guestOSInfo is empty
            - Guest agent cannot report due to missing communication channel
        """
        pass
```

---

### File: `tests/virt/node/general/conftest.py` (additions)

```python
"""
Shared fixtures for Windows guest agent OS info tests.

These fixtures should be added to the existing conftest.py in tests/virt/node/general/
"""

import pytest
from ocp_resources.virtual_machine import VirtualMachine
from utilities.virt import running_vm, VirtualMachineForTests


@pytest.fixture(scope="class")
def windows_vm_with_guest_agent(
    request,
    unprivileged_client,
    namespace,
):
    """
    Creates a Windows VM with qemu-guest-agent and virtio-serial driver installed.

    The VM is created from a Windows template and includes:
    - qemu-guest-agent installed and running
    - virtio-serial driver for guest-host communication
    - Network configuration for SSH/RDP access
    """
    # Fixture implementation would create a Windows VM
    # with guest agent pre-configured
    pass


@pytest.fixture(scope="function")
def windows_vm_without_guest_agent(
    unprivileged_client,
    namespace,
):
    """
    Creates a Windows VM without qemu-guest-agent installed.

    Used for negative testing scenarios.
    """
    # Fixture implementation would create a Windows VM
    # without guest agent
    pass


@pytest.fixture(scope="function")
def windows_vm_without_virtio_serial(
    unprivileged_client,
    namespace,
):
    """
    Creates a Windows VM without virtio-serial driver.

    Used for testing scenarios where communication channel is unavailable.
    """
    # Fixture implementation would create a Windows VM
    # without virtio-serial driver
    pass


@pytest.fixture(scope="function")
def windows_10_vm_with_guest_agent(
    unprivileged_client,
    namespace,
):
    """
    Creates a Windows 10 VM with qemu-guest-agent installed.
    """
    # Fixture implementation for Windows 10
    pass


@pytest.fixture(scope="function")
def windows_server_2019_vm_with_guest_agent(
    unprivileged_client,
    namespace,
):
    """
    Creates a Windows Server 2019 VM with qemu-guest-agent installed.
    """
    # Fixture implementation for Windows Server 2019
    pass


@pytest.fixture(scope="function")
def windows_server_2022_vm_with_guest_agent(
    unprivileged_client,
    namespace,
):
    """
    Creates a Windows Server 2022 VM with qemu-guest-agent installed.
    """
    # Fixture implementation for Windows Server 2022
    pass
```

---

## Test Coverage Summary

| Test File                              | Test Class                                  | Test Count | Priority | Tier |
| -------------------------------------- | ------------------------------------------- | ---------- | -------- | ---- |
| `test_windows_guest_agent_osinfo.py`   | `TestWindowsGuestAgentOSInfo`               | 4          | P0       | T1   |
| `test_windows_guest_agent_osinfo.py`   | `TestWindowsGuestAgentOSInfoMultipleVersions` | 3          | P2       | T2   |
| `test_windows_guest_agent_osinfo.py`   | `TestWindowsGuestAgentOSInfoNegative`       | 2          | P1       | T1   |
| **Total**                              |                                             | **9**      |          |      |

---

## Requirements Traceability

| Requirement ID | Test Method                                     | Coverage |
| -------------- | ----------------------------------------------- | -------- |
| CNV-61262      | `test_windows_os_version_display`               | ✓        |
| CNV-61262      | `test_windows_hostname_display`                 | ✓        |
| CNV-61262      | `test_osinfo_persistence_after_vm_reboot`       | ✓        |
| CNV-61262      | `test_osinfo_after_guest_agent_restart`         | ✓        |
| CNV-61262      | `test_os_version_display_windows_10`            | ✓        |
| CNV-61262      | `test_os_version_display_windows_server_2019`   | ✓        |
| CNV-61262      | `test_os_version_display_windows_server_2022`   | ✓        |
| CNV-61262      | `test_osinfo_empty_without_guest_agent`         | ✓        |
| CNV-61262      | `test_osinfo_empty_without_virtio_serial`       | ✓        |

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Preconditions (if needed), Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented (`gating`, `post_upgrade`)
- [x] Parametrization documented for Windows version matrix
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/windows_guest_agent_osinfo/std_cnv_61262.md`

---

## Implementation Notes

### Key Utilities to Use

Based on the openshift-virtualization-tests repository patterns:

1. **`utilities.ssp.validate_os_info_vmi_vs_windows_os(vm)`** - Validates VMI OS info against actual Windows OS info
2. **`utilities.virt.get_guest_os_info(vmi)`** - Retrieves guest OS info from VMI status
3. **`utilities.virt.running_vm(vm)`** - Ensures VM is in running state
4. **`utilities.ssp.get_windows_os_info(ssh_exec)`** - Gets OS info directly from Windows guest

### Existing Test Patterns

Reference tests in `tests/virt/cluster/common_templates/windows/test_windows_os_support.py`:
- Line 66-68: `test_vmi_guest_agent_info` - validates OS info VMI vs Windows OS
- Line 73-74: `test_virtctl_guest_agent_os_info` - validates OS info via virtctl

### Fixture Patterns

Windows VMs with guest agent should follow the pattern in existing Windows tests:
- Use `matrix_windows_os_vm_from_template` fixture or similar
- Ensure guest agent is installed and running
- Include virtio-win drivers

### Bug Fix Verification

The bug fix in PR #14232 ensures `domain.Status.OSInfo` is not empty. Tests should:
1. Verify the field is populated when guest agent is running
2. Confirm no race condition where field is sometimes empty
3. Validate across multiple VM reboots and agent restarts

---

## Next Steps

1. **Review STD** - Ensure all STP scenarios are covered
2. **Implement Fixtures** - Create Windows VM fixtures with guest agent configurations
3. **Implement Test Logic** - Fill in test method implementations using utilities
4. **Add to CI Pipeline** - Ensure tests run in Windows VM lane
5. **Document Windows Image Setup** - Provide guidance for Windows VM preparation with guest agent
