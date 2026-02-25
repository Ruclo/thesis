"""
VMI Hard Reset Negative and Edge Case Tests

STP Reference: https://issues.redhat.com/browse/VIRTSTRAT-357

This module contains negative tests for the VMI hard reset feature,
verifying proper error handling for invalid reset scenarios,
and edge case behavior for paused VMIs.
"""

import logging

import pytest
from kubernetes.client.exceptions import ApiException
from ocp_resources.virtual_machine_instance import VirtualMachineInstance

LOGGER = logging.getLogger(__name__)

pytestmark = pytest.mark.virt


class TestVMIResetOnStoppedVM:
    """
    Tests for VMI hard reset error handling on a stopped VMI.

    Preconditions:
        - Fedora virtual machine in stopped state (not started)
    """

    @pytest.mark.polarion("CNV-12379")
    def test_reset_stopped_vmi(self, non_running_vm):
        """
        [NEGATIVE] Test that resetting a stopped VMI fails with an appropriate error.

        Preconditions:
            - VM is in stopped state (not running)

        Steps:
            1. Attempt to call reset on the stopped VMI

        Expected:
            - Operation raises an error indicating the VMI is not running
        """
        LOGGER.info(f"Attempting to reset stopped VM {non_running_vm.name}")
        with pytest.raises(ApiException, match="404"):
            vmi = VirtualMachineInstance(
                name=non_running_vm.name,
                namespace=non_running_vm.namespace,
                client=non_running_vm.client,
            )
            vmi.reset()


class TestVMIResetOnPausedVM:
    """
    Tests for VMI hard reset behavior on a paused VMI.

    Preconditions:
        - Running Fedora virtual machine with paused VMI
    """

    @pytest.mark.polarion("CNV-12380")
    def test_reset_paused_vmi_succeeds(self, paused_vm):
        """
        Test that the reset API call succeeds on a paused VMI.

        Preconditions:
            - VM is running
            - VMI is paused

        Steps:
            1. Call reset on the paused VMI

        Expected:
            - Reset operation completes without raising an error
        """
        LOGGER.info(f"Resetting paused VMI {paused_vm.vmi.name}")
        paused_vm.vmi.reset()
        LOGGER.info(f"Reset API call succeeded for paused VMI {paused_vm.vmi.name}")


@pytest.mark.polarion("CNV-12381")
def test_reset_nonexistent_vmi(admin_client, namespace):
    """
    [NEGATIVE] Test that resetting a non-existent VMI fails with a not-found error.

    Preconditions:
        - No VMI with name "nonexistent-vmi" exists in the namespace

    Steps:
        1. Attempt to call reset on a non-existent VMI name

    Expected:
        - Operation raises a not-found error
    """
    nonexistent_vmi_name = "nonexistent-vmi-for-reset"
    LOGGER.info(f"Attempting to reset non-existent VMI {nonexistent_vmi_name}")
    vmi = VirtualMachineInstance(
        name=nonexistent_vmi_name,
        namespace=namespace.name,
        client=admin_client,
    )
    with pytest.raises(ApiException, match="404"):
        vmi.reset()
