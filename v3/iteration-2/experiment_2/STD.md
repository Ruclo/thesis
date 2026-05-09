# Software Test Description (STD)

## Feature: VNC Screenshot via libvirt API

**STP Reference:** [CNV-61271](https://issues.redhat.com/browse/CNV-61271)
**Jira ID:** CNV-61271
**Generated:** 2026-02-23

---

## Summary

Tests for the VNC screenshot functionality that uses libvirt's `virDomainScreenshot` API instead of VNC connections. This change (PR [kubevirt/kubevirt#15238](https://github.com/kubevirt/kubevirt/pull/15238)) eliminates the competition between VM overview thumbnail previews and full-screen VNC sessions that caused VNC disconnections (bug [CNV-60117](https://issues.redhat.com/browse/CNV-60117)).

Tests cover:

- Screenshot API functionality without requiring a VNC connection
- Screenshot image validity (valid PNG output)
- VNC connection stability during concurrent screenshot operations
- VNC stability during repeated screenshot requests
- Extended-duration concurrent VNC and screenshot usage
- Screenshot compatibility across different guest operating systems (RHEL, Windows)

---

## Test Files

### File: `tests/virt/screenshot/test_vnc_screenshot.py`

```python
"""
VNC Screenshot via libvirt API Tests

STP Reference: https://issues.redhat.com/browse/CNV-61271

This module contains tests verifying that the VMI screenshot endpoint
uses libvirt's virDomainScreenshot API, eliminating VNC connection
competition between thumbnail previews and full-screen VNC sessions.
"""

import pytest


class TestScreenshotAPI:
    """
    Tests for the VMI screenshot API endpoint functionality.

    Markers:
        - arm64
        - s390x
        - virt

    Preconditions:
        - Running Fedora VM with VNC graphics device configured
        - No active VNC client connections to the VM
    """

    def test_screenshot_without_vnc_connection(self):
        """
        Test that the screenshot API returns successfully without requiring a VNC connection.

        Steps:
            1. Call the VMI screenshot command via virtctl

        Expected:
            - Screenshot command succeeds and produces a non-empty image file
        """
        pass

    def test_screenshot_returns_valid_image(self):
        """
        Test that the screenshot API returns a valid PNG image.

        Steps:
            1. Call the VMI screenshot command via virtctl and save to a file

        Expected:
            - Saved file starts with a valid PNG signature header
        """
        pass


class TestVNCStabilityDuringScreenshot:
    """
    Tests for VNC connection stability during concurrent screenshot operations.

    Markers:
        - arm64
        - s390x
        - virt

    Preconditions:
        - Running Fedora VM with VNC graphics device configured
        - Active VNC connection established to the VM via virtctl
    """

    def test_vnc_connection_stable_during_screenshot(self):
        """
        Test that a VNC connection remains active when a screenshot is taken concurrently.

        Steps:
            1. Call the VMI screenshot command via virtctl while VNC connection is active

        Expected:
            - VNC connection remains open and responsive after the screenshot completes
        """
        pass

    def test_vnc_unaffected_by_repeated_screenshots(self):
        """
        Test that a VNC connection is unaffected by multiple consecutive screenshot requests.

        Steps:
            1. Call the VMI screenshot command via virtctl multiple times in succession while VNC connection is active

        Expected:
            - VNC connection remains open and responsive after all screenshot requests complete
        """
        pass


class TestScreenshotExtendedUsage:
    """
    Tests for VNC connection stability during extended concurrent screenshot usage.

    Markers:
        - tier3
        - arm64
        - s390x
        - virt

    Preconditions:
        - Running Fedora VM with VNC graphics device configured
        - Active VNC connection established to the VM via virtctl
    """

    def test_vnc_stable_during_extended_screenshot_usage(self):
        """
        Test that a VNC connection remains stable during prolonged concurrent screenshot operations.

        Steps:
            1. Periodically call the VMI screenshot command over an extended duration while VNC connection is active

        Expected:
            - VNC connection remains open and responsive throughout the entire duration
        """
        pass


class TestScreenshotRhelGuest:
    """
    Tests for screenshot functionality with RHEL guest operating system.

    Markers:
        - tier3
        - arm64
        - s390x
        - virt

    Preconditions:
        - Running RHEL VM with VNC graphics device configured
    """

    def test_screenshot_with_rhel_guest(self):
        """
        Test that the screenshot API returns a valid image for a RHEL guest.

        Steps:
            1. Call the VMI screenshot command via virtctl

        Expected:
            - Screenshot command succeeds and produces a non-empty image file
        """
        pass


class TestScreenshotWindowsGuest:
    """
    Tests for screenshot functionality with Windows guest operating system.

    Markers:
        - tier3
        - high_resource_vm
        - virt

    Preconditions:
        - Running Windows VM with VNC graphics device configured
    """

    def test_screenshot_with_windows_guest(self):
        """
        Test that the screenshot API returns a valid image for a Windows guest.

        Steps:
            1. Call the VMI screenshot command via virtctl

        Expected:
            - Screenshot command succeeds and produces a non-empty image file
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier | STP Scenario |
| --- | --- | --- | --- | --- | --- |
| `test_vnc_screenshot.py` | `TestScreenshotAPI` | 2 | P0, P1 | T1 | Scenarios 2, 3 |
| `test_vnc_screenshot.py` | `TestVNCStabilityDuringScreenshot` | 2 | P0 | T1 | Scenarios 1, 4 |
| `test_vnc_screenshot.py` | `TestScreenshotExtendedUsage` | 1 | P1 | T3 | Scenario 5 |
| `test_vnc_screenshot.py` | `TestScreenshotRhelGuest` | 1 | P2 | T3 | Scenario 6 (RHEL) |
| `test_vnc_screenshot.py` | `TestScreenshotWindowsGuest` | 1 | P2 | T3 | Scenario 6 (Windows) |

**Total: 7 tests** (all 6 STP scenarios covered)

---

## Design Decisions

1. **Separate classes for different guest OS fixtures**: Per GRAVEYARD lesson, tests using different class-scoped VM fixtures (Fedora, RHEL, Windows) are placed in separate classes to prevent simultaneous VM scheduling and `ErrorUnschedulable` failures on resource-constrained clusters.

2. **No parametrization for guest OS**: Instead of a parametrized test across guest OS types, each OS gets its own class. This avoids the class-scoped fixture collision documented in GRAVEYARD entry "Class-scoped fixtures from different VMs in same test class cause scheduling failures."

3. **Tier 3 for extended and multi-OS tests**: Extended duration (Scenario 5) and multi-guest (Scenario 6) tests are marked `tier3` because they are time-consuming and/or require additional resources.

4. **Windows test excludes s390x and arm64 markers**: Windows VMs are only supported on x86_64 architecture in KubeVirt, so architecture markers are omitted.

5. **Main tests use Fedora VM**: Scenarios 1-4 use a Fedora VM as the default, matching the repository convention for standard VM tests.

---

## Checklist

- [x] All STP scenarios covered
- [x] Each test verifies ONE thing
- [x] Negative tests marked with `[NEGATIVE]` (none required for this feature)
- [x] Markers documented
- [x] Parametrization documented (N/A - separate classes per GRAVEYARD lesson)
- [x] STP link in module docstring
- [x] Tests grouped in class with shared preconditions
- [x] Test methods contain only `pass`
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/vnc_screenshot/std_cnv_61271.md`
