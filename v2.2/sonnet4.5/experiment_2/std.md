# Software Test Description (STD)

## Feature: VNC Console Stability with Screenshot API

**STP Reference:** [CNV-61271 - VNC Console Disconnect Due to Thumbnail/Full Screen Competition](https://issues.redhat.com/browse/CNV-61271)
**Bug Fix:** [CNV-60117](https://issues.redhat.com/browse/CNV-60117)
**Implementation PR:** [kubevirt/kubevirt#15238](https://github.com/kubevirt/kubevirt/pull/15238)
**QE Owner:** Matan Schatzman
**SIG:** sig-compute, sig-ui
**Generated:** 2026-02-10

---

## Summary

This STD covers testing for the VNC console stability fix where the screenshot/thumbnail functionality was changed from using VNC connections to using libvirt's `virDomainScreenshot` API. This eliminates connection competition between the VM overview thumbnail and full-screen VNC console.

**Test Coverage:**
- VNC connection stability with concurrent thumbnail display
- Screenshot API functionality without VNC connection
- Screenshot quality verification
- Multi-guest OS compatibility
- Extended usage scenarios

**Key Change:** The `vnc/screenshot` API endpoint backend now uses libvirt's screenshot API instead of establishing a VNC connection, preventing VNC disconnects when both thumbnail and full-screen console are active.

---

## Test Files

### File: `tests/virt/console/test_vnc_screenshot_stability.py`

```python
"""
VNC Console Stability with Screenshot API Tests

STP Reference: https://issues.redhat.com/browse/CNV-61271
Bug Fix: https://issues.redhat.com/browse/CNV-60117
Implementation: https://github.com/kubevirt/kubevirt/pull/15238

This module contains tests verifying that the screenshot API (used for VM overview
thumbnails) no longer interferes with VNC console connections. The fix changed the
screenshot implementation from using VNC to using libvirt's virDomainScreenshot API.
"""

import pytest


class TestVNCScreenshotStability:
    """
    Tests for VNC console stability when screenshot API is used.

    Markers:
        - gating
        - tier1

    Preconditions:
        - Running VM with graphical display (VNC or SPICE configured)
        - VM accessible via VNC console
    """

    def test_vnc_connection_stable_with_concurrent_screenshot_api_calls(self):
        """
        Test that VNC connection remains stable when screenshot API is called.

        This test verifies the core bug fix: screenshot API no longer creates
        a competing VNC connection that would disconnect the active console.

        Steps:
            1. Establish VNC console connection to the VM
            2. Call vnc/screenshot API endpoint 10 times
            3. Check VNC connection status

        Expected:
            - VNC connection remains active (no disconnects)
        """
        pass

    def test_screenshot_api_works_without_vnc_connection(self):
        """
        Test that screenshot API returns image without establishing VNC connection.

        This verifies the new implementation uses libvirt's virDomainScreenshot
        instead of VNC.

        Steps:
            1. Ensure no VNC clients are connected to the VM
            2. Call vnc/screenshot API endpoint
            3. Verify screenshot data is returned
            4. Check that no VNC connection was established

        Expected:
            - Screenshot data is returned successfully
            - No VNC connection is created
        """
        pass

    def test_screenshot_quality_shows_vm_display_content(self):
        """
        Test that screenshot image quality is acceptable and shows VM content.

        Steps:
            1. Display known content on VM screen (e.g., login prompt with distinctive text)
            2. Call vnc/screenshot API endpoint
            3. Decode screenshot image data
            4. Verify screenshot shows expected content

        Expected:
            - Screenshot clearly shows VM display content
        """
        pass

    def test_multiple_sequential_screenshot_calls_do_not_affect_vnc(self):
        """
        Test that multiple rapid screenshot API calls do not disconnect VNC.

        This simulates the scenario where the overview page refreshes the
        thumbnail multiple times while VNC console is open.

        Steps:
            1. Establish VNC console connection
            2. Call vnc/screenshot API endpoint 20 times in rapid succession
            3. Check VNC connection status after each call

        Expected:
            - VNC connection remains stable throughout all screenshot calls
        """
        pass


class TestScreenshotAPIFunctionality:
    """
    Tests for screenshot API endpoint functionality.

    Markers:
        - tier1

    Preconditions:
        - Running VM with graphical display configured
    """

    def test_screenshot_api_returns_valid_image_format(self):
        """
        Test that screenshot API returns a valid image in expected format.

        Steps:
            1. Call vnc/screenshot API endpoint
            2. Verify response content type is image format
            3. Verify image data is decodable

        Expected:
            - Response content type is valid image format (PNG/JPEG)
            - Image data can be decoded
        """
        pass

    def test_screenshot_api_fails_for_vm_without_graphics_device(self):
        """
        [NEGATIVE] Test that screenshot API fails gracefully for VM without graphics.

        Steps:
            1. Create VM without VNC or SPICE graphics device
            2. Start the VM
            3. Call vnc/screenshot API endpoint

        Expected:
            - API returns error indicating graphics device not available
        """
        pass

    def test_screenshot_api_fails_for_stopped_vm(self):
        """
        [NEGATIVE] Test that screenshot API fails for stopped VM.

        Preconditions:
            - VM is in stopped state

        Steps:
            1. Call vnc/screenshot API endpoint for stopped VM

        Expected:
            - API returns error indicating VM is not running
        """
        pass


class TestExtendedVNCUsage:
    """
    Tests for extended VNC usage scenarios with screenshot functionality.

    Markers:
        - tier2

    Preconditions:
        - Running VM with VNC console available
    """

    def test_vnc_remains_connected_during_extended_thumbnail_usage(self):
        """
        Test that VNC connection remains stable during extended period with active thumbnail.

        This simulates real-world usage where a user has both the VM overview page
        (with auto-refreshing thumbnail) and full-screen VNC console open.

        Steps:
            1. Establish VNC console connection
            2. Simulate thumbnail updates by calling screenshot API every 5 seconds
            3. Continue for 5 minutes (60 screenshot calls)
            4. Check VNC connection status

        Expected:
            - VNC connection remains active throughout the test duration
        """
        pass

    def test_vnc_usability_unaffected_by_screenshot_calls(self):
        """
        Test that VNC console interaction is not degraded by screenshot API calls.

        Steps:
            1. Establish VNC console connection
            2. Send keyboard input to VM via VNC
            3. Call screenshot API 10 times
            4. Send additional keyboard input via VNC
            5. Verify all input was received by VM

        Expected:
            - All keyboard input successfully sent via VNC
            - No input lag or connection interruption
        """
        pass


class TestMultiGuestOSCompatibility:
    """
    Tests for screenshot API compatibility across different guest operating systems.

    Markers:
        - tier2

    Parametrize:
        - guest_os: [fedora, rhel9, windows-server-2022]

    Preconditions:
        - Running VM with guest OS from parameter
        - VM has graphical display configured
    """

    def test_screenshot_works_for_different_guest_os(self):
        """
        Test that screenshot API works correctly for different guest operating systems.

        Steps:
            1. Call vnc/screenshot API endpoint for VM with parameterized guest OS
            2. Verify screenshot data is returned
            3. Verify screenshot shows guest OS display

        Expected:
            - Screenshot successfully captured for all guest OS types
        """
        pass

    def test_vnc_stable_with_screenshot_for_different_guest_os(self):
        """
        Test that VNC stability with screenshots works for all guest OS types.

        Steps:
            1. Establish VNC connection to VM with parameterized guest OS
            2. Call screenshot API 5 times
            3. Check VNC connection status

        Expected:
            - VNC connection remains stable for all guest OS types
        """
        pass
```

---

### File: `tests/virt/console/conftest.py`

```python
"""
Shared fixtures for VNC and console tests.

This conftest provides fixtures for:
- VMs with VNC/SPICE graphics devices
- VNC connection management
- Screenshot API helpers
"""

import pytest
from ocp_resources.virtual_machine import VirtualMachine


@pytest.fixture()
def vm_with_vnc_graphics():
    """
    Running VM with VNC graphics device configured.

    Yields:
        VirtualMachine: Running VM with VNC console accessible
    """
    pass


@pytest.fixture()
def vm_with_spice_graphics():
    """
    Running VM with SPICE graphics device configured.

    Yields:
        VirtualMachine: Running VM with SPICE graphics
    """
    pass


@pytest.fixture()
def vm_without_graphics():
    """
    Running VM without any graphics device (headless).

    Yields:
        VirtualMachine: Running VM without VNC or SPICE
    """
    pass


@pytest.fixture()
def stopped_vm_with_graphics():
    """
    Stopped VM with VNC graphics device configured.

    Yields:
        VirtualMachine: Stopped VM with VNC configured
    """
    pass


@pytest.fixture()
def vnc_connection():
    """
    VNC connection manager for establishing and monitoring VNC connections.

    Yields:
        VNCConnectionManager: Helper for VNC connection operations
    """
    pass


@pytest.fixture()
def screenshot_api_client():
    """
    Client for calling the vnc/screenshot API endpoint.

    Yields:
        ScreenshotAPIClient: Helper for screenshot API operations
    """
    pass
```

---

## Test Coverage Summary

| Test File                           | Test Class                       | Test Count | Priority | Tier |
| ----------------------------------- | -------------------------------- | ---------- | -------- | ---- |
| `test_vnc_screenshot_stability.py`  | `TestVNCScreenshotStability`     | 4          | P0       | T1   |
| `test_vnc_screenshot_stability.py`  | `TestScreenshotAPIFunctionality` | 3          | P0/P1    | T1   |
| `test_vnc_screenshot_stability.py`  | `TestExtendedVNCUsage`           | 2          | P1       | T2   |
| `test_vnc_screenshot_stability.py`  | `TestMultiGuestOSCompatibility`  | 2          | P2       | T2   |
| **Total**                           | **4 classes**                    | **11**     | -        | -    |

---

## Requirements Traceability

| Requirement       | Test Method(s)                                                          | Coverage |
| ----------------- | ----------------------------------------------------------------------- | -------- |
| CNV-61271 (VNC Stability) | `test_vnc_connection_stable_with_concurrent_screenshot_api_calls` | ✓ |
| CNV-61271 (Screenshot without VNC) | `test_screenshot_api_works_without_vnc_connection` | ✓ |
| CNV-61271 (Screenshot Quality) | `test_screenshot_quality_shows_vm_display_content` | ✓ |
| CNV-61271 (Multi-Guest Support) | `test_screenshot_works_for_different_guest_os` | ✓ |
| Regression (VNC Functionality) | `test_vnc_usability_unaffected_by_screenshot_calls` | ✓ |
| Extended Usage | `test_vnc_remains_connected_during_extended_thumbnail_usage` | ✓ |

---

## Test Scenarios Mapped to STP

| STP Scenario | Test Method | Status |
| ------------ | ----------- | ------ |
| Scenario 1: VNC Stability with Concurrent Thumbnail | `test_vnc_connection_stable_with_concurrent_screenshot_api_calls` | ✓ |
| Scenario 2: Screenshot API Without VNC Connection | `test_screenshot_api_works_without_vnc_connection` | ✓ |
| Scenario 3: Screenshot Quality Verification | `test_screenshot_quality_shows_vm_display_content` | ✓ |
| Scenario 4: Thumbnail Updates Without VNC Impact | `test_multiple_sequential_screenshot_calls_do_not_affect_vnc` | ✓ |
| Scenario 5: Extended Dual-Tab Usage | `test_vnc_remains_connected_during_extended_thumbnail_usage` | ✓ |
| Scenario 6: Multiple Guest OS Types | `test_screenshot_works_for_different_guest_os`, `test_vnc_stable_with_screenshot_for_different_guest_os` | ✓ |

---

## Implementation Notes

### Key Testing Considerations

1. **VNC Connection Monitoring**: Tests need a mechanism to detect VNC disconnects. This could be:
   - Monitoring VNC connection state via virt-viewer or similar
   - Checking virt-launcher logs for VNC connection/disconnection events
   - Using VNC client library to maintain connection and detect drops

2. **Screenshot API Endpoint**: The vnc/screenshot API endpoint path will be:
   - `/apis/subresources.kubevirt.io/v1/namespaces/{namespace}/virtualmachineinstances/{name}/vnc/screenshot`

3. **VNC Connection Detection**: To verify no VNC connection is created, check:
   - virt-launcher process connections (no new VNC connections on port 5900+)
   - libvirt domain XML for active VNC clients
   - virt-launcher logs for VNC connection attempts

4. **Screenshot Validation**: For quality verification:
   - Screenshot should be PNG or JPEG format
   - Image should be decodable and non-empty
   - For content verification, could use OCR or image comparison with expected screen state

5. **Multi-Guest Testing**: Parameterize tests with:
   - Fedora (Linux, modern graphics)
   - RHEL 9 (Enterprise Linux)
   - Windows Server 2022 (Windows guest)

### Fixture Implementation Guidance

**`vm_with_vnc_graphics` fixture should:**
- Create VM with VNC graphics device in spec
- Wait for VM to be running
- Wait for VNC console to be accessible
- Yield the VM object
- Clean up VM on teardown

**`vnc_connection` fixture should:**
- Provide methods to establish VNC connection
- Monitor connection state
- Detect disconnections
- Close connection on teardown

**`screenshot_api_client` fixture should:**
- Provide method to call screenshot API with VM reference
- Return screenshot data (bytes)
- Handle API errors
- Provide helper to decode/validate image format

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] Parametrization documented where needed
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Requirements traceability documented
- [x] Implementation notes provided
