"""
VMI Hard Reset via virtctl Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains tests for the VMI hard reset functionality
accessed through the virtctl CLI command.
"""

import logging

import pytest

from tests.virt.node.hard_reset.conftest import get_vm_boot_count, wait_for_boot_count_increment
from utilities.constants import TIMEOUT_10MIN
from utilities.infra import run_virtctl_command
from utilities.virt import wait_for_running_vm

LOGGER = logging.getLogger(__name__)

pytestmark = pytest.mark.virt


class TestVirtctlReset:
    """
    Tests for VMI hard reset via the virtctl reset command.

    Preconditions:
        - Running Fedora virtual machine with SSH access
    """

    @pytest.mark.polarion("CNV-12377")
    def test_virtctl_reset_command_succeeds(self, virtctl_reset_vm):
        """
        Test that the 'virtctl reset' command completes successfully.

        Steps:
            1. Execute 'virtctl reset <vmi-name>' command

        Expected:
            - Command exit code equals 0
        """
        command_success, output, error = run_virtctl_command(
            command=["reset", virtctl_reset_vm.vmi.name],
            namespace=virtctl_reset_vm.namespace,
            verify_stderr=False,
        )
        LOGGER.info(f"virtctl reset output: {output}, stderr: {error}")
        assert command_success, f"virtctl reset command failed: {error}"
        wait_for_running_vm(vm=virtctl_reset_vm, ssh_timeout=TIMEOUT_10MIN)

    @pytest.mark.polarion("CNV-12378")
    def test_virtctl_reset_triggers_guest_reboot(self, virtctl_reset_vm):
        """
        Test that running 'virtctl reset' on a running VMI triggers a guest reboot.

        Steps:
            1. Record boot count before reset
            2. Execute 'virtctl reset <vmi-name>' command
            3. Wait for VM to become running and SSH accessible
            4. Compare boot count after reset with boot count before reset

        Expected:
            - Boot count after reset equals boot count before reset plus 1
        """
        boot_count_before = get_vm_boot_count(vm=virtctl_reset_vm)
        LOGGER.info(f"Boot count before virtctl reset: {boot_count_before}")

        command_success, output, error = run_virtctl_command(
            command=["reset", virtctl_reset_vm.vmi.name],
            namespace=virtctl_reset_vm.namespace,
            verify_stderr=False,
        )
        assert command_success, f"virtctl reset command failed: {error}"

        wait_for_running_vm(vm=virtctl_reset_vm, ssh_timeout=TIMEOUT_10MIN)

        boot_count_after = wait_for_boot_count_increment(
            vm=virtctl_reset_vm,
            boot_count_before=boot_count_before,
        )
        LOGGER.info(f"Boot count after virtctl reset: {boot_count_after}")
        assert boot_count_after - boot_count_before == 1, (
            f"Expected boot count to increment by 1 after virtctl reset, "
            f"but got before={boot_count_before} after={boot_count_after}"
        )
