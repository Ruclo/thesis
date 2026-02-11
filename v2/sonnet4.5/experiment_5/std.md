# Software Test Description (STD)

## Feature: StorageProfile snapshotClass Not Honored for VM Snapshot

**STP Reference:** [../thesis/stps/5.md](../../../thesis/stps/5.md)
**Jira ID:** CNV-61266 (Bug: CNV-54866)
**Generated:** 2026-02-03

---

## Summary

This STD covers tests for the bug fix where StorageProfile's snapshotClass field was being ignored during VM snapshot creation. The fix ensures that when creating a VMSnapshot, the system honors the snapshotClass specified in the StorageProfile resource, and falls back to label-based VolumeSnapshotClass selection only when the StorageProfile does not specify a snapshotClass.

**Test Coverage:**
- Verify VMSnapshot uses snapshotClass from StorageProfile when specified
- Verify fallback to label-based VolumeSnapshotClass selection when StorageProfile has no snapshotClass
- Verify snapshot creation and restore cycle with StorageProfile-specified snapshotClass
- Verify behavior with multiple StorageClasses having different snapshotClass configurations

---

## Test Files

### File: `tests/storage/snapshots/test_storageprofile_snapshotclass.py`

```python
"""
StorageProfile snapshotClass Honored for VM Snapshot Tests

STP Reference: ../thesis/stps/5.md
Jira: CNV-61266 (Bug: CNV-54866)

This module contains tests verifying that VMSnapshot correctly honors the snapshotClass
field in StorageProfile resources, with proper fallback behavior when not specified.

Related PRs:
- https://github.com/kubevirt/kubevirt/pull/13711
- https://github.com/kubevirt/kubevirt/pull/13723
"""

import pytest
from ocp_resources.datavolume import DataVolume
from ocp_resources.storage_class import StorageClass
from ocp_resources.storage_profile import StorageProfile
from ocp_resources.virtual_machine_restore import VirtualMachineRestore
from ocp_resources.virtual_machine_snapshot import VirtualMachineSnapshot
from ocp_resources.volume_snapshot import VolumeSnapshot
from ocp_resources.volume_snapshot_class import VolumeSnapshotClass

from utilities.storage import (
    create_cirros_dv_for_snapshot_dict,
    is_snapshot_supported_by_sc,
    wait_for_volume_snapshot_ready_to_use,
)
from utilities.virt import VirtualMachineForTests, running_vm

pytestmark = pytest.mark.usefixtures(
    "namespace",
    "skip_if_no_storage_class_for_snapshot",
)


class TestStorageProfileSnapshotClass:
    """
    Tests for StorageProfile snapshotClass field honored during VM snapshot creation.

    Markers:
        - gating
        - tier1

    Preconditions:
        - Cluster with snapshot-capable storage backend (ODF, Ceph, etc.)
        - VolumeSnapshotClass resources configured for storage provisioners
        - StorageProfile resources exist for storage classes
    """

    @pytest.mark.polarion("CNV-61266")
    @pytest.mark.gating
    def test_snapshot_uses_storageprofile_snapshotclass(self):
        """
        Test that VMSnapshot uses snapshotClass from StorageProfile when specified.

        Preconditions:
            - StorageProfile resource with snapshotClass field set to specific VolumeSnapshotClass
            - VM created with DataVolume using the StorageClass
            - VM is in stopped state

        Steps:
            1. Get StorageProfile and verify snapshotClass is configured
            2. Create VMSnapshot for the VM
            3. Wait for VMSnapshot to complete
            4. Get the VolumeSnapshot created by the VMSnapshot
            5. Inspect VolumeSnapshot's volumeSnapshotClassName field

        Expected:
            - VolumeSnapshot.spec.volumeSnapshotClassName equals StorageProfile.spec.snapshotClass
        """
        pass

    @pytest.mark.polarion("CNV-54866")
    @pytest.mark.gating
    def test_snapshot_fallback_without_storageprofile_snapshotclass(self):
        """
        Test that VMSnapshot falls back to label-based selection when StorageProfile has no snapshotClass.

        Preconditions:
            - StorageProfile resource without snapshotClass field (or set to empty/null)
            - VM created with DataVolume using the StorageClass
            - VolumeSnapshotClass with matching driver/provisioner labels exists
            - VM is in stopped state

        Steps:
            1. Get StorageProfile and verify snapshotClass is NOT configured
            2. Create VMSnapshot for the VM
            3. Wait for VMSnapshot to complete
            4. Get the VolumeSnapshot created by the VMSnapshot
            5. Verify VolumeSnapshotClass was selected via label matching

        Expected:
            - VolumeSnapshot is created successfully using label-based VolumeSnapshotClass selection
        """
        pass

    @pytest.mark.polarion("CNV-61266-02")
    def test_restore_from_snapshot_with_storageprofile_snapshotclass(self):
        """
        Test that VM restore works correctly when snapshot was created using StorageProfile snapshotClass.

        Preconditions:
            - StorageProfile with snapshotClass configured
            - VM created and file /data/before-snapshot.txt written with content "original-data"
            - VMSnapshot created using StorageProfile snapshotClass
            - File /data/after-snapshot.txt written with content "post-snapshot-data"
            - VM is in stopped state

        Steps:
            1. Create VirtualMachineRestore from the VMSnapshot
            2. Wait for restore to complete
            3. Start the VM
            4. Read file /data/before-snapshot.txt
            5. Check if file /data/after-snapshot.txt exists

        Expected:
            - File /data/before-snapshot.txt content equals "original-data"
            - File /data/after-snapshot.txt does NOT exist
        """
        pass

    @pytest.mark.polarion("CNV-61266-03")
    def test_online_snapshot_uses_storageprofile_snapshotclass(self):
        """
        Test that online VMSnapshot (VM running) uses StorageProfile snapshotClass.

        Preconditions:
            - StorageProfile with snapshotClass configured
            - VM created with DataVolume using the StorageClass
            - VM is in running state

        Steps:
            1. Verify VM is running
            2. Create VMSnapshot while VM is running
            3. Wait for VMSnapshot to complete
            4. Get the VolumeSnapshot created by the VMSnapshot
            5. Inspect VolumeSnapshot's volumeSnapshotClassName field

        Expected:
            - VolumeSnapshot.spec.volumeSnapshotClassName equals StorageProfile.spec.snapshotClass
            - VMSnapshot succeeds despite VM being running
        """
        pass

    @pytest.mark.polarion("CNV-61266-04")
    def test_snapshot_storageprofile_snapshotclass_precedence(self):
        """
        Test that StorageProfile snapshotClass takes precedence over label-based selection.

        Preconditions:
            - Multiple VolumeSnapshotClass resources with same driver
            - One VolumeSnapshotClass with matching labels (would be selected by label-based logic)
            - StorageProfile snapshotClass configured to different VolumeSnapshotClass
            - VM created with DataVolume using the StorageClass

        Steps:
            1. Verify multiple VolumeSnapshotClass options exist
            2. Create VMSnapshot
            3. Wait for VMSnapshot to complete
            4. Get the VolumeSnapshot created by the VMSnapshot
            5. Verify volumeSnapshotClassName matches StorageProfile.spec.snapshotClass

        Expected:
            - VolumeSnapshot uses StorageProfile.spec.snapshotClass, NOT the label-based match
        """
        pass


class TestStorageProfileSnapshotClassMultiStorage:
    """
    Tests for StorageProfile snapshotClass with multiple storage backends.

    Markers:
        - tier2

    Preconditions:
        - Multiple StorageClass resources with snapshot support
        - Each StorageClass has corresponding StorageProfile
        - Different snapshotClass configured per StorageProfile
    """

    @pytest.mark.polarion("CNV-61266-05")
    @pytest.mark.tier2
    def test_multiple_storages_different_snapshotclasses(self):
        """
        Test that VMs on different StorageClasses use their respective StorageProfile snapshotClass.

        Parametrize:
            - storage_configs: List of (StorageClass, VolumeSnapshotClass) pairs

        Preconditions:
            - Storage-A with StorageProfile.snapshotClass = VSC-A
            - Storage-B with StorageProfile.snapshotClass = VSC-B
            - VM-A created using Storage-A
            - VM-B created using Storage-B

        Steps:
            1. Create VMSnapshot for VM-A
            2. Create VMSnapshot for VM-B
            3. Wait for both VMSnapshots to complete
            4. Get VolumeSnapshots for VM-A and VM-B
            5. Verify VM-A's VolumeSnapshot uses VSC-A
            6. Verify VM-B's VolumeSnapshot uses VSC-B

        Expected:
            - VM-A VolumeSnapshot.spec.volumeSnapshotClassName equals VSC-A
            - VM-B VolumeSnapshot.spec.volumeSnapshotClassName equals VSC-B
        """
        pass


class TestStorageProfileSnapshotClassNegative:
    """
    Negative tests for StorageProfile snapshotClass validation.

    Markers:
        - tier2

    Preconditions:
        - Cluster with snapshot-capable storage
    """

    @pytest.mark.polarion("CNV-61266-06")
    @pytest.mark.tier2
    def test_snapshot_fails_with_invalid_snapshotclass(self):
        """
        [NEGATIVE] Test that VMSnapshot fails when StorageProfile snapshotClass references non-existent VolumeSnapshotClass.

        Preconditions:
            - StorageProfile with snapshotClass set to "non-existent-vsc"
            - VM created with DataVolume using the StorageClass
            - VolumeSnapshotClass "non-existent-vsc" does NOT exist

        Steps:
            1. Create VMSnapshot for the VM
            2. Wait and observe VMSnapshot status

        Expected:
            - VMSnapshot creation fails or enters error state
            - Error message indicates VolumeSnapshotClass not found
        """
        pass

    @pytest.mark.polarion("CNV-61266-07")
    @pytest.mark.tier2
    def test_snapshot_fails_with_incompatible_snapshotclass(self):
        """
        [NEGATIVE] Test that VMSnapshot fails when StorageProfile snapshotClass has incompatible driver.

        Preconditions:
            - StorageClass using provisioner "driver-A"
            - StorageProfile snapshotClass referencing VolumeSnapshotClass with driver "driver-B"
            - VM created with DataVolume using the StorageClass

        Steps:
            1. Create VMSnapshot for the VM
            2. Wait and observe VMSnapshot status

        Expected:
            - VMSnapshot creation fails or enters error state
            - Error indicates driver mismatch or incompatible snapshot class
        """
        pass


class TestStorageProfileSnapshotClassBackwardCompatibility:
    """
    Tests for backward compatibility with existing StorageProfiles.

    Markers:
        - tier1

    Preconditions:
        - Existing cluster with StorageProfiles created before this fix
    """

    @pytest.mark.polarion("CNV-61266-08")
    @pytest.mark.tier1
    def test_existing_storageprofiles_without_snapshotclass_work(self):
        """
        Test that existing StorageProfiles without snapshotClass field continue to work.

        Preconditions:
            - StorageProfile exists without snapshotClass field (legacy configuration)
            - VolumeSnapshotClass with matching driver exists
            - VM created with DataVolume using the StorageClass

        Steps:
            1. Verify StorageProfile has no snapshotClass field
            2. Create VMSnapshot
            3. Wait for VMSnapshot to complete

        Expected:
            - VMSnapshot succeeds using label-based VolumeSnapshotClass selection
            - Backward compatibility maintained
        """
        pass

    @pytest.mark.polarion("CNV-61266-09")
    @pytest.mark.tier1
    def test_storageprofile_update_snapshotclass_affects_new_snapshots(self):
        """
        Test that updating StorageProfile snapshotClass affects only new snapshots, not existing ones.

        Preconditions:
            - StorageProfile with snapshotClass = VSC-OLD
            - VM created and VMSnapshot-1 created (uses VSC-OLD)
            - StorageProfile updated to snapshotClass = VSC-NEW

        Steps:
            1. Verify VMSnapshot-1 still references VSC-OLD
            2. Create VMSnapshot-2 after StorageProfile update
            3. Wait for VMSnapshot-2 to complete
            4. Get VolumeSnapshot for VMSnapshot-2

        Expected:
            - VMSnapshot-1 VolumeSnapshot still uses VSC-OLD (unchanged)
            - VMSnapshot-2 VolumeSnapshot uses VSC-NEW (new behavior)
        """
        pass
```

---

### File: `tests/storage/snapshots/conftest.py`

```python
"""
Shared fixtures for StorageProfile snapshotClass tests.

This conftest provides fixtures for setting up StorageProfiles with specific
snapshotClass configurations for testing purposes.
"""

import pytest
from ocp_resources.resource import ResourceEditor
from ocp_resources.storage_profile import StorageProfile
from ocp_resources.volume_snapshot_class import VolumeSnapshotClass

from utilities.constants import SPEC_STR


@pytest.fixture()
def storage_profile_with_snapshotclass(admin_client, storage_class_for_snapshot):
    """
    Configure StorageProfile with snapshotClass field.

    Yields:
        tuple: (StorageProfile, VolumeSnapshotClass) - configured resources
    """
    pass


@pytest.fixture()
def storage_profile_without_snapshotclass(admin_client, storage_class_for_snapshot):
    """
    Ensure StorageProfile does not have snapshotClass field configured.

    Yields:
        StorageProfile: StorageProfile with snapshotClass removed or unset
    """
    pass


@pytest.fixture()
def multiple_volume_snapshot_classes(admin_client, storage_class_for_snapshot):
    """
    Create multiple VolumeSnapshotClass resources for the same storage driver.

    Yields:
        list: List of VolumeSnapshotClass instances
    """
    pass


@pytest.fixture()
def vm_with_storageprofile_snapshotclass(
    admin_client,
    namespace,
    storage_profile_with_snapshotclass,
    artifactory_secret_scope_module,
    artifactory_config_map_scope_module,
):
    """
    Create VM using StorageClass with StorageProfile that has snapshotClass configured.

    Yields:
        VirtualMachineForTests: VM instance ready for snapshot operations
    """
    pass


@pytest.fixture()
def vm_snapshot_with_storageprofile_class(
    admin_client,
    namespace,
    vm_with_storageprofile_snapshotclass,
):
    """
    Create VMSnapshot for VM using StorageProfile snapshotClass.

    Yields:
        VirtualMachineSnapshot: Snapshot instance with snapshotClass honored
    """
    pass
```

---

### File: `tests/storage/snapshots/utils.py` (additions)

```python
"""
Utility functions for StorageProfile snapshotClass testing.
"""


def get_volume_snapshot_class_name_from_volume_snapshot(volume_snapshot):
    """
    Extract VolumeSnapshotClass name from VolumeSnapshot resource.

    Args:
        volume_snapshot: VolumeSnapshot resource instance

    Returns:
        str: VolumeSnapshotClass name used by the snapshot
    """
    pass


def verify_storageprofile_has_snapshotclass(storage_profile):
    """
    Verify that StorageProfile has snapshotClass field configured.

    Args:
        storage_profile: StorageProfile resource instance

    Returns:
        str: The snapshotClass value if configured, None otherwise
    """
    pass


def get_volume_snapshots_for_vm_snapshot(vm_snapshot, namespace):
    """
    Get all VolumeSnapshot resources created by a VMSnapshot.

    Args:
        vm_snapshot: VirtualMachineSnapshot instance
        namespace: Namespace name

    Returns:
        list: List of VolumeSnapshot instances
    """
    pass


def verify_volume_snapshot_uses_expected_class(volume_snapshot, expected_vsc_name):
    """
    Verify that VolumeSnapshot uses the expected VolumeSnapshotClass.

    Args:
        volume_snapshot: VolumeSnapshot instance
        expected_vsc_name: Expected VolumeSnapshotClass name

    Raises:
        AssertionError: If VolumeSnapshotClass does not match expected
    """
    pass
```

---

## Test Coverage Summary

| Test File                                 | Test Class/Function                                    | Test Count | Priority | Tier |
| ----------------------------------------- | ------------------------------------------------------ | ---------- | -------- | ---- |
| `test_storageprofile_snapshotclass.py`    | `TestStorageProfileSnapshotClass`                      | 5          | P0       | T1   |
| `test_storageprofile_snapshotclass.py`    | `TestStorageProfileSnapshotClassMultiStorage`          | 1          | P1       | T2   |
| `test_storageprofile_snapshotclass.py`    | `TestStorageProfileSnapshotClassNegative`              | 2          | P1       | T2   |
| `test_storageprofile_snapshotclass.py`    | `TestStorageProfileSnapshotClassBackwardCompatibility` | 2          | P0       | T1   |
| **Total Tests**                           | **4 Test Classes**                                     | **10**     | -        | -    |
| **Fixtures** (`conftest.py`)              | Shared setup fixtures                                  | 5          | -        | -    |
| **Utilities** (`utils.py` additions)      | Helper functions                                       | 4          | -        | -    |

---

## Test Scenarios Coverage Matrix

| STP Scenario | Test Function(s)                                                | Status |
| ------------ | --------------------------------------------------------------- | ------ |
| Scenario 1   | `test_snapshot_uses_storageprofile_snapshotclass`               | ✓      |
| Scenario 2   | `test_snapshot_fallback_without_storageprofile_snapshotclass`   | ✓      |
| Scenario 3   | `test_restore_from_snapshot_with_storageprofile_snapshotclass`  | ✓      |
| Scenario 4   | `test_multiple_storages_different_snapshotclasses`              | ✓      |
| Additional   | `test_online_snapshot_uses_storageprofile_snapshotclass`        | ✓      |
| Additional   | `test_snapshot_storageprofile_snapshotclass_precedence`         | ✓      |
| Additional   | `test_snapshot_fails_with_invalid_snapshotclass`                | ✓      |
| Additional   | `test_snapshot_fails_with_incompatible_snapshotclass`           | ✓      |
| Additional   | `test_existing_storageprofiles_without_snapshotclass_work`      | ✓      |
| Additional   | `test_storageprofile_update_snapshotclass_affects_new_snapshots`| ✓      |

---

## Pytest Markers Used

| Marker        | Purpose                                  | Applied To                       |
| ------------- | ---------------------------------------- | -------------------------------- |
| `@pytest.mark.polarion` | Link to Polarion test case    | All test functions               |
| `@pytest.mark.gating`   | Critical CI/CD pipeline tests | Core functionality tests         |
| `@pytest.mark.tier1`    | Tier 1 functional tests       | Primary test scenarios           |
| `@pytest.mark.tier2`    | Tier 2 extended tests         | Edge cases and multi-storage     |
| `pytestmark` (module)   | Skip if no snapshot storage   | All tests in module              |

---

## Implementation Notes

### Key Design Decisions

1. **Test Independence**: Each test verifies ONE specific behavior with ONE expected outcome
2. **Fixture-Based Setup**: Complex setup (StorageProfile configuration, VM creation) isolated in fixtures
3. **Class Grouping**: Related tests grouped in classes with shared preconditions in class docstrings
4. **Negative Tests**: Failure scenarios marked with `[NEGATIVE]` tag for clarity
5. **Backward Compatibility**: Dedicated test class ensures existing configurations continue to work

### Repository Patterns Applied

- **Module-level markers**: `pytestmark` for `skip_if_no_storage_class_for_snapshot`
- **Fixture indirection**: Parametrized fixtures for different configurations
- **Context managers**: VirtualMachineSnapshot, VirtualMachineRestore with auto-cleanup
- **Utility functions**: Dedicated helpers for snapshot class verification
- **Wait patterns**: `.wait_snapshot_done()`, `.wait_restore_done()` for async operations

### Test Execution Strategy

1. **Gating Tests** (T1, P0): Run on every PR
   - `test_snapshot_uses_storageprofile_snapshotclass`
   - `test_snapshot_fallback_without_storageprofile_snapshotclass`
   - `test_existing_storageprofiles_without_snapshotclass_work`

2. **Extended Tests** (T2, P1): Run in nightly builds
   - Multi-storage scenarios
   - Negative test cases
   - StorageProfile update scenarios

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Preconditions, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented (`@pytest.mark.polarion`, `@pytest.mark.gating`, `@pytest.mark.tier1/tier2`)
- [x] Parametrization documented where needed
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/storageprofile_snapshotclass/std_cnv_61266.md`
- [x] Follows openshift-virtualization-tests patterns and conventions
- [x] Fixtures separated in `conftest.py`
- [x] Utility functions in `utils.py`
- [x] Module-level `pytestmark` for skip conditions
- [x] All STP scenarios covered with traceability

---

## Next Steps

1. **Review STD**: Review test descriptions, preconditions, and expected outcomes
2. **Implement Fixtures**: Implement the fixture functions in `conftest.py`
3. **Implement Utilities**: Implement helper functions in `utils.py`
4. **Implement Tests**: Replace `pass` with actual test implementation
5. **Run Tests**: Execute tests against test environment
6. **Validate**: Ensure all tests pass and coverage is complete
