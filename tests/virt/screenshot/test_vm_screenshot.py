"""
VM Screenshot (libvirt virDomainScreenshot) Tests

STP Reference: https://issues.redhat.com/browse/CNV-61271

This module contains tests verifying that the VM screenshot API uses
libvirt's virDomainScreenshot instead of VNC, ensuring screenshots
do not disrupt active VNC connections.

PR: https://github.com/kubevirt/kubevirt/pull/15238
"""

import logging
import os
import shlex

import pytest

from utilities.infra import run_virtctl_command
from utilities.vnc_utils import VNCConnection

LOGGER = logging.getLogger(__name__)

PNG_MAGIC_BYTES = b"\x89PNG"
SCREENSHOT_CONSECUTIVE_COUNT = 5


def take_vm_screenshot(vm_name: str, vm_namespace: str, output_path: str) -> None:
    """Take a VM screenshot via virtctl and assert the command succeeds.

    Args:
        vm_name: Name of the virtual machine.
        vm_namespace: Namespace of the virtual machine.
        output_path: File path to write the screenshot PNG to.
    """
    result, output, err = run_virtctl_command(
        command=shlex.split(f"vnc screenshot {vm_name} -f {output_path}"),
        namespace=vm_namespace,
    )
    assert result, f"virtctl vnc screenshot failed: {err}"
    LOGGER.info(f"Screenshot saved to {output_path}")


@pytest.mark.virt
@pytest.mark.usefixtures("screenshot_fedora_vm")
class TestVMScreenshotAPI:
    """
    Tests for the VM screenshot API backed by libvirt virDomainScreenshot.

    Preconditions:
        - Running Fedora VM with VNC graphics device
    """

    @pytest.mark.polarion("CNV-61271")
    def test_screenshot_returns_valid_image(self, screenshot_fedora_vm, tmp_path):
        """
        Test that the screenshot API returns a valid, non-empty image file.

        Steps:
            1. Call virtctl vnc screenshot for the running VM

        Expected:
            - Screenshot file exists and has non-zero size
        """
        screenshot_path = str(tmp_path / "screenshot.png")
        take_vm_screenshot(
            vm_name=screenshot_fedora_vm.name,
            vm_namespace=screenshot_fedora_vm.namespace,
            output_path=screenshot_path,
        )
        file_size = os.path.getsize(screenshot_path)
        LOGGER.info(f"Screenshot file size: {file_size} bytes")
        assert file_size > 0, "Screenshot file is empty"

    @pytest.mark.polarion("CNV-61271")
    def test_screenshot_without_active_vnc_connection(self, screenshot_fedora_vm, tmp_path):
        """
        Test that a screenshot can be taken without any active VNC connection.

        Preconditions:
            - No VNC clients connected to the VM

        Steps:
            1. Call virtctl vnc screenshot for the running VM

        Expected:
            - Screenshot is returned successfully
        """
        screenshot_path = str(tmp_path / "screenshot_no_vnc.png")
        take_vm_screenshot(
            vm_name=screenshot_fedora_vm.name,
            vm_namespace=screenshot_fedora_vm.namespace,
            output_path=screenshot_path,
        )
        assert os.path.exists(screenshot_path), "Screenshot file was not created"

    @pytest.mark.polarion("CNV-61271")
    def test_screenshot_image_is_valid_png(self, screenshot_fedora_vm, tmp_path):
        """
        Test that the screenshot image is a valid PNG file.

        Steps:
            1. Call virtctl vnc screenshot for the running VM
            2. Read the PNG file header bytes

        Expected:
            - File starts with PNG magic bytes (89 50 4E 47)
        """
        screenshot_path = str(tmp_path / "screenshot_png_check.png")
        take_vm_screenshot(
            vm_name=screenshot_fedora_vm.name,
            vm_namespace=screenshot_fedora_vm.namespace,
            output_path=screenshot_path,
        )
        with open(screenshot_path, "rb") as screenshot_file:
            header = screenshot_file.read(4)
        LOGGER.info(f"Screenshot header bytes: {header.hex()}")
        assert header == PNG_MAGIC_BYTES, (
            f"Screenshot is not a valid PNG file. Header: {header.hex()}, expected: {PNG_MAGIC_BYTES.hex()}"
        )


@pytest.mark.virt
@pytest.mark.usefixtures("screenshot_fedora_vm")
class TestVNCStabilityDuringScreenshot:
    """
    Tests verifying VNC connection stability when screenshots are taken concurrently.

    Preconditions:
        - Running Fedora VM with VNC graphics device
    """

    @pytest.mark.polarion("CNV-61271")
    def test_vnc_connection_stable_during_screenshot(self, screenshot_fedora_vm, tmp_path):
        """
        Test that an active VNC connection remains stable when a screenshot is taken.

        Steps:
            1. Establish a VNC connection to the VM
            2. Take a screenshot via virtctl vnc screenshot while VNC is connected
            3. Verify the VNC connection is still active

        Expected:
            - VNC connection remains open and functional after screenshot
        """
        with VNCConnection(vm=screenshot_fedora_vm) as vnc_child:
            assert vnc_child is not None, "VNC connection was not established"
            LOGGER.info("VNC connection established, taking screenshot")
            screenshot_path = str(tmp_path / "screenshot_vnc_stable.png")
            take_vm_screenshot(
                vm_name=screenshot_fedora_vm.name,
                vm_namespace=screenshot_fedora_vm.namespace,
                output_path=screenshot_path,
            )
            assert vnc_child.isalive(), "VNC connection was disrupted after screenshot"
            LOGGER.info("VNC connection remains stable after screenshot")

    @pytest.mark.polarion("CNV-61271")
    def test_vnc_stable_after_multiple_consecutive_screenshots(self, screenshot_fedora_vm, tmp_path):
        """
        Test that an active VNC connection remains stable after multiple rapid screenshots.

        Steps:
            1. Establish a VNC connection to the VM
            2. Take 5 consecutive screenshots via virtctl vnc screenshot
            3. Verify the VNC connection is still active

        Expected:
            - VNC connection remains open and functional after all screenshots
        """
        with VNCConnection(vm=screenshot_fedora_vm) as vnc_child:
            assert vnc_child is not None, "VNC connection was not established"
            LOGGER.info("VNC connection established, taking multiple screenshots")
            for screenshot_index in range(SCREENSHOT_CONSECUTIVE_COUNT):
                screenshot_path = str(tmp_path / f"screenshot_{screenshot_index}.png")
                take_vm_screenshot(
                    vm_name=screenshot_fedora_vm.name,
                    vm_namespace=screenshot_fedora_vm.namespace,
                    output_path=screenshot_path,
                )
                LOGGER.info(f"Screenshot {screenshot_index + 1}/{SCREENSHOT_CONSECUTIVE_COUNT} completed")
            assert vnc_child.isalive(), (
                "VNC connection was disrupted after multiple consecutive screenshots"
            )
            LOGGER.info("VNC connection remains stable after all screenshots")

    @pytest.mark.polarion("CNV-61271")
    def test_screenshot_succeeds_with_active_vnc(self, screenshot_fedora_vm, tmp_path):
        """
        Test that screenshots return valid data while a VNC connection is active.

        Steps:
            1. Establish a VNC connection to the VM
            2. Take a screenshot via virtctl vnc screenshot

        Expected:
            - Screenshot file exists and has non-zero size
        """
        with VNCConnection(vm=screenshot_fedora_vm):
            LOGGER.info("VNC connection established, verifying screenshot content")
            screenshot_path = str(tmp_path / "screenshot_with_vnc.png")
            take_vm_screenshot(
                vm_name=screenshot_fedora_vm.name,
                vm_namespace=screenshot_fedora_vm.namespace,
                output_path=screenshot_path,
            )
            file_size = os.path.getsize(screenshot_path)
            LOGGER.info(f"Screenshot file size with active VNC: {file_size} bytes")
            assert file_size > 0, "Screenshot file is empty while VNC is active"


@pytest.mark.virt
@pytest.mark.tier3
class TestVMScreenshotFedoraGuest:
    """
    Tests for screenshot functionality with Fedora guest OS.

    Preconditions:
        - Running Fedora VM with VNC graphics device configured
    """

    @pytest.mark.polarion("CNV-61271")
    def test_screenshot_with_fedora_guest(self, screenshot_fedora_vm, tmp_path):
        """
        Test that the screenshot API works with a Fedora guest operating system.

        Steps:
            1. Call virtctl vnc screenshot for the running Fedora VM

        Expected:
            - Screenshot file exists and has non-zero size
        """
        screenshot_path = str(tmp_path / "screenshot_fedora.png")
        take_vm_screenshot(
            vm_name=screenshot_fedora_vm.name,
            vm_namespace=screenshot_fedora_vm.namespace,
            output_path=screenshot_path,
        )
        file_size = os.path.getsize(screenshot_path)
        LOGGER.info(f"Fedora screenshot file size: {file_size} bytes")
        assert file_size > 0, "Fedora screenshot file is empty"


@pytest.mark.virt
@pytest.mark.tier3
class TestVMScreenshotRhelGuest:
    """
    Tests for screenshot functionality with RHEL guest OS.

    Preconditions:
        - Running RHEL VM with VNC graphics device configured
    """

    @pytest.mark.polarion("CNV-61271")
    def test_screenshot_with_rhel_guest(self, screenshot_rhel_vm, tmp_path):
        """
        Test that the screenshot API works with a RHEL guest operating system.

        Steps:
            1. Call virtctl vnc screenshot for the running RHEL VM

        Expected:
            - Screenshot file exists and has non-zero size
        """
        screenshot_path = str(tmp_path / "screenshot_rhel.png")
        take_vm_screenshot(
            vm_name=screenshot_rhel_vm.name,
            vm_namespace=screenshot_rhel_vm.namespace,
            output_path=screenshot_path,
        )
        file_size = os.path.getsize(screenshot_path)
        LOGGER.info(f"RHEL screenshot file size: {file_size} bytes")
        assert file_size > 0, "RHEL screenshot file is empty"
