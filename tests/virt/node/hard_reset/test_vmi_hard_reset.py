"""
VMI Hard Reset Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains tests for the VMI hard reset subresource API,
verifying that a running VMI can be reset in-place without pod
rescheduling, preserving VMI UID and triggering an actual guest reboot.
"""

import logging

import pytest

from tests.virt.node.hard_reset.conftest import get_vm_boot_count, wait_for_boot_count_increment

LOGGER = logging.getLogger(__name__)

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

    @pytest.mark.polarion("CNV-12374")
    def test_guest_reboots_after_reset(
        self,
        hard_reset_vm,
        boot_count_before_reset,
        hard_reset_vm_after_reset,
    ):
        """
        Test that a VMI hard reset triggers an actual guest reboot.

        Steps:
            1. Compare boot count after reset with boot count before reset

        Expected:
            - Boot count after reset equals boot count before reset plus 1
        """
        boot_count_after_reset = wait_for_boot_count_increment(
            vm=hard_reset_vm,
            boot_count_before=boot_count_before_reset,
        )
        LOGGER.info(
            f"Boot count before reset: {boot_count_before_reset}, after reset: {boot_count_after_reset}"
        )
        assert boot_count_after_reset - boot_count_before_reset == 1, (
            f"Expected boot count to increment by 1 after reset, "
            f"but got before={boot_count_before_reset} after={boot_count_after_reset}"
        )

    @pytest.mark.polarion("CNV-12375")
    def test_pod_preserved_after_reset(
        self,
        hard_reset_vm,
        pod_name_before_reset,
        hard_reset_vm_after_reset,
    ):
        """
        Test that the virt-launcher pod is not rescheduled after a VMI reset.

        Steps:
            1. Compare pod name after reset with pod name before reset

        Expected:
            - Pod name after reset equals pod name before reset
        """
        pod_name_after_reset = hard_reset_vm.privileged_vmi.virt_launcher_pod.name
        LOGGER.info(
            f"Pod name before reset: {pod_name_before_reset}, after reset: {pod_name_after_reset}"
        )
        assert pod_name_after_reset == pod_name_before_reset, (
            f"Pod was rescheduled after reset: before={pod_name_before_reset} after={pod_name_after_reset}"
        )

    @pytest.mark.polarion("CNV-12376")
    def test_vmi_uid_unchanged_after_reset(
        self,
        hard_reset_vm,
        vmi_uid_before_reset,
        hard_reset_vm_after_reset,
    ):
        """
        Test that the VMI UID remains unchanged after a hard reset.

        Steps:
            1. Compare VMI UID after reset with VMI UID before reset

        Expected:
            - VMI UID after reset equals VMI UID before reset
        """
        vmi_uid_after_reset = hard_reset_vm.vmi.instance.metadata.uid
        LOGGER.info(
            f"VMI UID before reset: {vmi_uid_before_reset}, after reset: {vmi_uid_after_reset}"
        )
        assert vmi_uid_after_reset == vmi_uid_before_reset, (
            f"VMI UID changed after reset: before={vmi_uid_before_reset} after={vmi_uid_after_reset}"
        )
