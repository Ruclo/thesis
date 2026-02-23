# Software Test Description (STD)

## Feature: VNC Console Disconnect Due to Thumbnail/Full Screen Competition

**STP Reference:** /home/jzo/thesis/stps/2.md
**Jira ID:** CNV-61271
**Bug Fix Jira:** CNV-60117

---

## Summary

This STD covers tests for the fix that eliminates VNC console disconnections caused by competition between VM overview thumbnail requests and full-screen VNC connections. The fix changes the screenshot backend from VNC to libvirt's `virDomainScreenshot` API, so that taking a screenshot no longer requires establishing a VNC connection. Tests verify that screenshots work independently of VNC, that VNC connections remain stable when screenshots are taken concurrently, and that screenshot output quality is acceptable.

---

## Test Files

### File: `tests/virt/cluster/vnc_screenshot/test_vnc_screenshot.py`

```python
"""
VNC Screenshot via libvirt virDomainScreenshot Tests

STP Reference: /home/jzo/thesis/stps/2.md
Jira: CNV-61271 (Feature), CNV-60117 (Bug Fix)
PR: https://github.com/kubevirt/kubevirt/pull/15238

This module contains tests verifying that the vnc/screenshot subresource uses
libvirt's virDomainScreenshot API instead of VNC, ensuring screenshots do not
compete with active VNC connections.
"""

import pytest


@pytest.mark.virt
class TestVncScreenshotIndependence:
    """
    Tests that the vnc/screenshot subresource works independently of VNC connections.

    Preconditions:
        - Running VM with a graphical console device configured
        - VM is SSH accessible
    """

    def test_screenshot_without_vnc_connection(self):
        """
        Test that a screenshot can be taken without any active VNC connection.

        Steps:
            1. Call virtctl vnc screenshot for the VM

        Expected:
            - Screenshot file is created and is a valid image with non-zero size
        """
        pass

    def test_screenshot_returns_valid_image(self):
        """
        Test that the screenshot produces a recognizable image of the VM display.

        Steps:
            1. Call virtctl vnc screenshot for the VM
            2. Read the resulting screenshot file

        Expected:
            - Screenshot file has a valid PNG header
        """
        pass


@pytest.mark.virt
class TestVncStabilityWithScreenshot:
    """
    Tests that VNC connections remain stable when screenshots are taken concurrently.

    Preconditions:
        - Running VM with a graphical console device configured
        - VM is SSH accessible
    """

    def test_vnc_connection_survives_concurrent_screenshot(self):
        """
        Test that an active VNC connection is not disconnected when a screenshot is taken.

        Steps:
            1. Establish a VNC proxy connection to the VM
            2. While VNC is connected, call virtctl vnc screenshot for the VM
            3. Verify the VNC proxy connection is still alive

        Expected:
            - VNC proxy connection remains open after screenshot is taken
        """
        pass

    def test_vnc_connection_survives_repeated_screenshots(self):
        """
        Test that an active VNC connection remains stable through multiple consecutive screenshots.

        Steps:
            1. Establish a VNC proxy connection to the VM
            2. Take 5 consecutive screenshots while VNC is connected
            3. Verify the VNC proxy connection is still alive after all screenshots

        Expected:
            - VNC proxy connection remains open after all screenshots complete
        """
        pass

    def test_screenshot_succeeds_with_active_vnc(self):
        """
        Test that a screenshot is successfully captured while a VNC connection is active.

        Steps:
            1. Establish a VNC proxy connection to the VM
            2. Call virtctl vnc screenshot for the VM

        Expected:
            - Screenshot file is created and is a valid image with non-zero size
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --- | --- | --- | --- | --- |
| `test_vnc_screenshot.py` | `TestVncScreenshotIndependence` | 2 | P0 | Tier 1 |
| `test_vnc_screenshot.py` | `TestVncStabilityWithScreenshot` | 3 | P0 | Tier 1 |

---

## Checklist

- [x] STP link in module docstring
- [x] Each test verifies ONE thing
- [x] Negative tests marked with `[NEGATIVE]` (none applicable)
- [x] Markers documented
- [x] Parametrization documented (none needed)
- [x] All STP scenarios covered
- [x] Test methods contain only `pass`
- [x] Tests grouped in classes with shared preconditions
