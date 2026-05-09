# Software Test Description (STD)

## Feature: VNC Console Disconnect Due to Thumbnail/Full Screen Competition

**STP Reference:** [stps/2.md](/home/fedora/thesis/stps/2.md)
**Jira ID:** [CNV-61271](https://issues.redhat.com/browse/CNV-61271) / [CNV-60117](https://issues.redhat.com/browse/CNV-60117)
**Generated:** 2026-02-21

---

## Summary

Tests for the libvirt-based VM screenshot mechanism introduced in [kubevirt/kubevirt#15238](https://github.com/kubevirt/kubevirt/pull/15238). The fix replaces the VNC-based screenshot backend with libvirt's `virDomainScreenshot` API, eliminating the connection competition that caused VNC console disconnections when the VM overview thumbnail and full-screen VNC were used simultaneously.

The tests verify:
- Screenshot API returns valid image data without requiring a VNC connection
- Active VNC connections remain stable when screenshots are taken concurrently
- Multiple rapid screenshot requests do not degrade VNC stability
- Screenshot functionality works across different guest operating systems

---

## Test Files

### File: `tests/virt/screenshot/test_vm_screenshot.py`

```python
"""
VM Screenshot (libvirt virDomainScreenshot) Tests

STP Reference: https://issues.redhat.com/browse/CNV-61271

This module contains tests verifying that the VM screenshot API uses
libvirt's virDomainScreenshot instead of VNC, ensuring screenshots
do not disrupt active VNC connections.

PR: https://github.com/kubevirt/kubevirt/pull/15238
"""

import pytest


class TestVMScreenshotAPI:
    """
    Tests for the VM screenshot API backed by libvirt virDomainScreenshot.

    Preconditions:
        - Running Fedora VM with VNC graphics device
        - VM is SSH accessible
    """

    def test_screenshot_returns_valid_image(self):
        """
        Test that the screenshot API returns a valid, non-empty image file.

        Steps:
            1. Call virtctl vnc screenshot for the running VM

        Expected:
            - Screenshot file exists and has non-zero size
        """
        pass

    def test_screenshot_without_active_vnc_connection(self):
        """
        Test that a screenshot can be taken without any active VNC connection.

        Preconditions:
            - No VNC clients connected to the VM

        Steps:
            1. Call virtctl vnc screenshot for the running VM

        Expected:
            - Screenshot is returned successfully
        """
        pass

    def test_screenshot_image_is_valid_png(self):
        """
        Test that the screenshot image is a valid PNG file.

        Steps:
            1. Call virtctl vnc screenshot for the running VM
            2. Read the PNG file header bytes

        Expected:
            - File starts with PNG magic bytes (89 50 4E 47)
        """
        pass


class TestVNCStabilityDuringScreenshot:
    """
    Tests verifying VNC connection stability when screenshots are taken concurrently.

    Preconditions:
        - Running Fedora VM with VNC graphics device
        - VM is SSH accessible
    """

    def test_vnc_connection_stable_during_screenshot(self):
        """
        Test that an active VNC connection remains stable when a screenshot is taken.

        Steps:
            1. Establish a VNC connection to the VM
            2. Take a screenshot via virtctl vnc screenshot while VNC is connected
            3. Verify the VNC connection is still active

        Expected:
            - VNC connection remains open and functional after screenshot
        """
        pass

    def test_vnc_stable_after_multiple_consecutive_screenshots(self):
        """
        Test that an active VNC connection remains stable after multiple rapid screenshots.

        Steps:
            1. Establish a VNC connection to the VM
            2. Take 5 consecutive screenshots via virtctl vnc screenshot
            3. Verify the VNC connection is still active

        Expected:
            - VNC connection remains open and functional after all screenshots
        """
        pass

    def test_screenshot_succeeds_with_active_vnc(self):
        """
        Test that screenshots return valid data while a VNC connection is active.

        Steps:
            1. Establish a VNC connection to the VM
            2. Take a screenshot via virtctl vnc screenshot

        Expected:
            - Screenshot file exists and has non-zero size
        """
        pass


class TestVMScreenshotGuestCompatibility:
    """
    Tests for screenshot functionality across different guest operating systems.

    Markers:
        - tier3

    Parametrize:
        - vm_os: [fedora, rhel]

    Preconditions:
        - Running VM with the parametrized guest OS
        - VM has VNC graphics device configured
        - VM is SSH accessible
    """

    def test_screenshot_with_guest_os(self):
        """
        Test that the screenshot API works with the given guest operating system.

        Steps:
            1. Call virtctl vnc screenshot for the running VM

        Expected:
            - Screenshot file exists and has non-zero size
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --- | --- | --- | --- | --- |
| `test_vm_screenshot.py` | `TestVMScreenshotAPI` | 3 | P0 | Tier 1 |
| `test_vm_screenshot.py` | `TestVNCStabilityDuringScreenshot` | 3 | P0 | Tier 1 |
| `test_vm_screenshot.py` | `TestVMScreenshotGuestCompatibility` | 1 (parametrized) | P2 | Tier 3 |

---

## Traceability to STP Scenarios

| STP Scenario | STD Test(s) | Coverage |
| --- | --- | --- |
| Scenario 1: VNC Stability with Concurrent Thumbnail | `test_vnc_connection_stable_during_screenshot` | VNC stays connected when screenshot (thumbnail backend) is called |
| Scenario 2: Screenshot API Without VNC Connection | `test_screenshot_without_active_vnc_connection` | Screenshot works with no VNC clients connected |
| Scenario 3: Screenshot Quality Verification | `test_screenshot_returns_valid_image`, `test_screenshot_image_is_valid_png` | Screenshot is non-empty and valid PNG |
| Scenario 4: Thumbnail Updates Without VNC Impact | `test_vnc_stable_after_multiple_consecutive_screenshots`, `test_screenshot_succeeds_with_active_vnc` | Multiple screenshots don't disrupt VNC |
| Scenario 5: Extended Dual-Tab Usage | Covered by Scenario 4 tests (rapid consecutive screenshots) | Repeated screenshot calls with active VNC |
| Scenario 6: Multiple Guest OS Types | `test_screenshot_with_guest_os` (parametrized) | Fedora and RHEL guest OS coverage |

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] Parametrization documented where needed
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/vnc_screenshot_stability/std_cnv_61271.md`
- [x] All STP scenarios covered
