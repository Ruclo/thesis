"""
Windows Guest Agent OS/Hostname Info Display Tests

STP Reference: stps/7.md
Jira: CNV-61262 / CNV-56888

This module verifies that Windows VMs correctly report OS information
and hostname through the QEMU guest agent, ensuring domain.Status.OSInfo
is populated when the agent is running.
"""

import logging

import pytest

from tests.virt.cluster.common_templates.utils import validate_os_info_virtctl_vs_windows_os
from utilities.constants import OS_FLAVOR_WINDOWS
from utilities.ssp import validate_os_info_vmi_vs_windows_os
from utilities.virt import (
    run_os_command,
    validate_virtctl_guest_agent_after_guest_reboot,
)

LOGGER = logging.getLogger(__name__)

START_GUEST_AGENT_CMD = "powershell -command \"Start-Service -Name 'QEMU-GA'\""

pytestmark = [pytest.mark.virt, pytest.mark.high_resource_vm]


@pytest.mark.jira("CNV-61262")
class TestWindowsGuestAgentOSInfo:
    """Tests for Windows guest agent OS and hostname info display.

    Verifies that Windows VMs correctly display OS information and hostname
    through the guest agent, addressing the bug where domain.Status.OSInfo
    was sometimes empty despite the guest agent running (CNV-56888).
    """

    def test_vmi_guest_os_info_displayed(self, windows_guest_agent_vm):
        """Test that VMI status guestOSInfo contains correct Windows OS information.

        Steps:
            1. Query VMI status guestOSInfo and compare against OS data
               retrieved from inside the Windows guest

        Expected:
            - VMI guestOSInfo matches the Windows OS information reported
              from inside the guest
        """
        validate_os_info_vmi_vs_windows_os(vm=windows_guest_agent_vm)

    def test_virtctl_hostname_displayed(self, windows_guest_agent_vm):
        """Test that virtctl guestosinfo reports the correct Windows hostname.

        Steps:
            1. Query virtctl guestosinfo and compare hostname against
               hostname retrieved from inside the Windows guest

        Expected:
            - Virtctl reported hostname matches the hostname reported
              from inside the guest
        """
        validate_os_info_virtctl_vs_windows_os(vm=windows_guest_agent_vm)

    def test_guest_agent_info_available_after_reboot(self, windows_guest_agent_vm):
        """Test that guest agent OS info remains available after a Windows VM
        guest reboot.

        Steps:
            1. Reboot the Windows VM from inside the guest and wait for the
               VM to become SSH accessible
            2. Validate that virtctl guest agent data is consistently
               available over time

        Expected:
            - Guest agent OS info is consistently available after reboot
        """
        validate_virtctl_guest_agent_after_guest_reboot(
            vm=windows_guest_agent_vm, os_type=OS_FLAVOR_WINDOWS
        )

    @pytest.mark.usefixtures("stopped_guest_agent_service")
    def test_os_info_appears_after_guest_agent_service_start(self, windows_guest_agent_vm):
        """Test that OS info appears in VMI status after starting the
        qemu-guest-agent service.

        Preconditions:
            - qemu-guest-agent service is stopped inside the Windows VM
            - VMI status guestOSInfo is empty (agent is not reporting)

        Steps:
            1. Start the qemu-guest-agent service inside the Windows VM
            2. Wait for VMI status guestOSInfo to be populated

        Expected:
            - VMI guestOSInfo is populated with correct Windows OS
              information
        """
        LOGGER.info(f"Starting QEMU guest agent service on {windows_guest_agent_vm.name}")
        run_os_command(vm=windows_guest_agent_vm, command=START_GUEST_AGENT_CMD)
        validate_os_info_vmi_vs_windows_os(vm=windows_guest_agent_vm)
