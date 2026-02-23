# Software Test Description (STD)

## Feature: StorageProfile snapshotClass Not Honored for VM Snapshot

**STP Reference:** /thesis/stps/5.md
**Jira ID:** CNV-54866
**Enhancement:** CNV-61266
**Generated:** 2026-02-10

---

## Summary

This STD covers functional testing for the bug fix ensuring that VM snapshots honor the `snapshotClass` field specified in StorageProfile resources. Previously, the StorageProfile's snapshotClass setting was ignored when creating VM snapshots, causing snapshots to use incorrect VolumeSnapshotClass resources. This fix adds proper checking of StorageProfile.snapshotClass before falling back to label-based selection.

The tests verify:
1. VM snapshots use the snapshotClass defined in StorageProfile
2. Fallback to label-based selection when StorageProfile lacks snapshotClass
3. Snapshot restore works correctly with StorageProfile-specified snapshotClass
4. Multiple storage classes with different snapshotClasses work independently

---

## Test Files

### File: `tests/storage/snapshot/test_storageprofile_snapshot_class.py`

```python
"""
StorageProfile snapshotClass Honored for VM Snapshot Tests

STP Reference: /thesis/stps/5.md
Jira: CNV-54866 (Bug Fix)
Enhancement: CNV-61266

This module contains tests verifying that VM snapshots correctly honor the
snapshotClass field specified in StorageProfile resources. Previously, this
field was ignored, causing snapshots to use incorrect VolumeSnapshotClasses.

The fix adds proper checking of StorageProfile.snapshotClass before falling
back to label-based VolumeSnapshotClass selection.
"""

import pytest


class TestStorageProfileSnapshotClass:
    """
    Tests for StorageProfile snapshotClass honored during VM snapshot creation.

    Markers:
        - tier1
        - gating

    Preconditions:
        - Cluster with snapshot-capable storage backend (ODF, Ceph, etc.)
        - StorageClass with snapshot support exists
        - VolumeSnapshotClass resources configured
        - CDI operator installed and running
    """

    def test_snapshot_uses_storageprofile_snapshot_class(self):
        """
        Test that VM snapshot uses snapshotClass from StorageProfile.

        This is the primary test case verifying the bug fix. When a StorageProfile
        has a snapshotClass field configured, VM snapshots created from VMs using
        that StorageClass MUST use the specified VolumeSnapshotClass.

        Steps:
            1. Configure StorageProfile with specific snapshotClass
            2. Create VM using that StorageClass
            3. Create VMSnapshot for the VM
            4. Inspect created VolumeSnapshot's volumeSnapshotClassName field

        Expected:
            - VolumeSnapshot volumeSnapshotClassName equals StorageProfile snapshotClass
        """
        pass

    def test_snapshot_fallback_without_storageprofile_snapshot_class(self):
        """
        Test that VM snapshot falls back to label-based selection when StorageProfile lacks snapshotClass.

        This verifies backward compatibility - existing StorageProfiles without
        snapshotClass configured should continue to work using the label-based
        VolumeSnapshotClass selection mechanism.

        Steps:
            1. Ensure StorageProfile has no snapshotClass field configured
            2. Create VM using that StorageClass
            3. Create VMSnapshot for the VM
            4. Verify VolumeSnapshot created with VolumeSnapshotClass selected via labels

        Expected:
            - VolumeSnapshot is created successfully using label-based VolumeSnapshotClass selection
        """
        pass

    def test_restore_vm_from_snapshot_with_storageprofile_snapshot_class(self):
        """
        Test that VM restore from snapshot works with StorageProfile-specified snapshotClass.

        This end-to-end test verifies the complete snapshot/restore cycle works
        correctly when using StorageProfile's snapshotClass field.

        Preconditions:
            - VM snapshot created using StorageProfile snapshotClass

        Steps:
            1. Create VM snapshot using StorageProfile snapshotClass (verified in test_snapshot_uses_storageprofile_snapshot_class)
            2. Restore VM from the snapshot
            3. Wait for VM to reach Running state
            4. Verify VM boots successfully and is SSH accessible

        Expected:
            - VM restoration succeeds
            - Restored VM is Running and SSH accessible
        """
        pass


class TestMultipleStorageClassesSnapshotClass:
    """
    Tests for multiple StorageClasses with different snapshotClasses.

    Markers:
        - tier2

    Preconditions:
        - Cluster with snapshot-capable storage backend
        - Multiple StorageClasses configured
        - Each StorageClass has corresponding StorageProfile with different snapshotClass
        - Multiple VolumeSnapshotClass resources configured
    """

    def test_multiple_storage_classes_use_correct_snapshot_classes(self):
        """
        Test that VMs on different StorageClasses use their respective snapshotClasses.

        This test verifies that the fix works correctly when multiple StorageClasses
        are configured with different snapshotClasses in their StorageProfiles.
        Each VM snapshot must use the correct VolumeSnapshotClass for its storage.

        Parametrize:
            - storage_class_configs: List of (StorageClass, snapshotClass) tuples

        Steps:
            1. Create VMs on different StorageClasses (each with configured snapshotClass)
            2. Create VMSnapshot for each VM
            3. Verify each VolumeSnapshot uses the correct snapshotClass from its StorageProfile

        Expected:
            - All VolumeSnapshots use correct volumeSnapshotClassName matching their StorageProfile
        """
        pass


class TestStorageProfileSnapshotClassNegative:
    """
    Negative tests for StorageProfile snapshotClass configuration.

    Markers:
        - tier2

    Preconditions:
        - Cluster with snapshot-capable storage backend
        - StorageClass configured
    """

    def test_snapshot_fails_with_nonexistent_snapshot_class(self):
        """
        [NEGATIVE] Test that VM snapshot fails when StorageProfile references nonexistent snapshotClass.

        This verifies error handling when StorageProfile is misconfigured with
        a snapshotClass that doesn't exist in the cluster.

        Steps:
            1. Configure StorageProfile with nonexistent snapshotClass
            2. Create VM using that StorageClass
            3. Attempt to create VMSnapshot

        Expected:
            - VMSnapshot creation fails with error indicating VolumeSnapshotClass not found
        """
        pass

    def test_snapshot_with_empty_snapshot_class_field(self):
        """
        Test that VM snapshot falls back correctly when snapshotClass field is empty string.

        This edge case verifies that an empty string in snapshotClass is treated
        the same as a missing field, triggering fallback to label-based selection.

        Steps:
            1. Configure StorageProfile with snapshotClass set to empty string ""
            2. Create VM using that StorageClass
            3. Create VMSnapshot

        Expected:
            - VolumeSnapshot created successfully using label-based selection (fallback behavior)
        """
        pass
```

---

### File: `tests/storage/snapshot/conftest.py`

```python
"""
Shared fixtures for StorageProfile snapshotClass tests.

This module provides pytest fixtures for setting up test resources
needed for StorageProfile snapshotClass testing.
"""

import pytest


@pytest.fixture(scope="class")
def storage_profile_with_snapshot_class():
    """
    StorageProfile configured with specific snapshotClass.

    Provides a StorageProfile resource with snapshotClass field set to
    a valid VolumeSnapshotClass.

    Yields:
        StorageProfile: StorageProfile resource with snapshotClass configured
    """
    pass


@pytest.fixture(scope="class")
def storage_profile_without_snapshot_class():
    """
    StorageProfile without snapshotClass field.

    Provides a StorageProfile resource without snapshotClass configured,
    for testing fallback behavior to label-based selection.

    Yields:
        StorageProfile: StorageProfile resource without snapshotClass
    """
    pass


@pytest.fixture(scope="class")
def volume_snapshot_class_primary():
    """
    Primary VolumeSnapshotClass for StorageProfile snapshotClass testing.

    Provides a VolumeSnapshotClass resource configured for the test storage backend.

    Yields:
        VolumeSnapshotClass: VolumeSnapshotClass resource
    """
    pass


@pytest.fixture(scope="class")
def volume_snapshot_class_secondary():
    """
    Secondary VolumeSnapshotClass for multi-class testing.

    Provides an additional VolumeSnapshotClass resource for testing
    multiple StorageClasses with different snapshotClasses.

    Yields:
        VolumeSnapshotClass: VolumeSnapshotClass resource
    """
    pass


@pytest.fixture(scope="function")
def vm_with_storage_profile_snapshot_class(storage_profile_with_snapshot_class):
    """
    Running VM using StorageClass with StorageProfile snapshotClass configured.

    Provides a running VM whose boot disk uses a StorageClass that has
    a StorageProfile with snapshotClass field set.

    Yields:
        VirtualMachine: Running VM with StorageProfile-configured storage
    """
    pass


@pytest.fixture(scope="function")
def vm_snapshot_from_storageprofile(vm_with_storage_profile_snapshot_class):
    """
    VM snapshot created using StorageProfile snapshotClass.

    Provides a VMSnapshot created from a VM using StorageProfile snapshotClass.
    Used for restore testing.

    Yields:
        VirtualMachineSnapshot: Snapshot created with StorageProfile snapshotClass
    """
    pass
```

---

## Test Coverage Summary

| Test File                             | Test Class                              | Test Count | Priority | Tier       |
| ------------------------------------- | --------------------------------------- | ---------- | -------- | ---------- |
| `test_storageprofile_snapshot_class.py` | `TestStorageProfileSnapshotClass`       | 3          | P0       | Tier 1     |
| `test_storageprofile_snapshot_class.py` | `TestMultipleStorageClassesSnapshotClass` | 1          | P2       | Tier 2     |
| `test_storageprofile_snapshot_class.py` | `TestStorageProfileSnapshotClassNegative` | 2          | P1       | Tier 2     |
| **Total**                             |                                         | **6**      |          | **T1-T2**  |

---

## Requirements Traceability

| Requirement ID | Requirement Summary        | Test Method(s)                                          | Coverage |
| -------------- | -------------------------- | ------------------------------------------------------- | -------- |
| CNV-61266      | Honor snapshotClass        | `test_snapshot_uses_storageprofile_snapshot_class`      | ✓        |
| CNV-61266      | Fallback behavior          | `test_snapshot_fallback_without_storageprofile_snapshot_class` | ✓        |
| CNV-61266      | Restore with correct class | `test_restore_vm_from_snapshot_with_storageprofile_snapshot_class` | ✓        |
| CNV-61266      | Multiple storage classes   | `test_multiple_storage_classes_use_correct_snapshot_classes` | ✓        |

---

## Test Dependencies

### Resource Dependencies
- **StorageClass**: Must support volume snapshots
- **StorageProfile**: CDI resource defining storage characteristics
- **VolumeSnapshotClass**: Kubernetes snapshot provisioner settings
- **VMSnapshot**: KubeVirt VM snapshot resource

### Operator Dependencies
- CDI operator (provides StorageProfile)
- Snapshot controller (manages VolumeSnapshots)
- Storage backend driver (ODF, Ceph, etc.)

---

## Checklist

- [x] All STP scenarios covered (Scenarios 1-4)
- [x] Each test verifies ONE thing
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Markers documented (tier1, tier2, gating)
- [x] Parametrization documented where needed
- [x] STP reference in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Preconditions (if needed), Steps, Expected
- [x] Test methods contain only `pass`
- [x] Fixtures defined in conftest.py
- [x] Coverage summary table included
- [x] Requirements traceability documented

---

## Implementation Notes

### Key Assumptions
1. Tests assume snapshot-capable storage backend (ODF recommended)
2. StorageProfile resources are managed by CDI operator
3. VolumeSnapshotClass resources must exist before testing

### Testing Strategy
1. **Tier 1 (Gating)**: Core functionality - StorageProfile snapshotClass honored, fallback works, restore succeeds
2. **Tier 2**: Extended scenarios - multiple storage classes, negative cases

### Fixture Design
- **Class-scoped**: StorageProfile, VolumeSnapshotClass (expensive to create)
- **Function-scoped**: VMs, VMSnapshots (must be isolated per test)

### Expected Behavior
- When StorageProfile has snapshotClass → use that VolumeSnapshotClass
- When StorageProfile lacks snapshotClass → fallback to label-based selection
- Invalid snapshotClass → VMSnapshot creation fails with clear error

---

## Related PRs

| PR | Repository | Description |
|----|------------|-------------|
| [kubevirt/kubevirt#13711](https://github.com/kubevirt/kubevirt/pull/13711) | kubevirt/kubevirt | VMSnapshot: honor StorageProfile snapshotClass when choosing volumesnapshotclass |
| [kubevirt/kubevirt#13723](https://github.com/kubevirt/kubevirt/pull/13723) | kubevirt/kubevirt | [release-1.4] VMSnapshot: honor StorageProfile snapshotClass (backport) |

---

**End of Software Test Description**
