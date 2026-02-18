# Software Test Description (STD)

## Feature: StorageProfile snapshotClass Honored for VM Snapshot

**STP Reference:** [../stps/5.md](../stps/5.md)
**Jira ID:** [CNV-61266](https://issues.redhat.com/browse/CNV-61266) / [CNV-54866](https://issues.redhat.com/browse/CNV-54866)
**Generated:** 2026-02-17

---

## Summary

This STD covers tests verifying that VMSnapshot honors the `snapshotClass` field from
StorageProfile when choosing which VolumeSnapshotClass to use. The bug fix
([kubevirt/kubevirt#13711](https://github.com/kubevirt/kubevirt/pull/13711)) adds a check
for `StorageProfile.snapshotClass` before falling back to label-based VolumeSnapshotClass
selection.

Tests cover three Tier 1 scenarios:
1. Snapshot uses the snapshotClass specified in StorageProfile
2. Fallback to label-based selection when StorageProfile has no snapshotClass
3. Restore succeeds when snapshot was created with StorageProfile-specified snapshotClass

---

## Test Files

### File: `tests/storage/snapshots/test_storage_profile_snapshot_class.py`

```python
"""
StorageProfile snapshotClass Honored for VM Snapshot Tests

STP Reference: ../stps/5.md
Jira: CNV-61266 / CNV-54866

This module contains tests verifying that VMSnapshot honors the snapshotClass
field from StorageProfile when selecting a VolumeSnapshotClass for snapshot
creation. Prior to the fix, the snapshotClass setting was ignored and snapshots
would use a VolumeSnapshotClass selected via labels instead.
"""

import pytest


pytestmark = pytest.mark.usefixtures(
    "skip_if_no_storage_class_for_snapshot",
)


class TestStorageProfileSnapshotClass:
    """
    Tests for StorageProfile snapshotClass selection during VM snapshot creation.

    Preconditions:
        - Cluster has snapshot-capable storage backend
        - StorageClass exists with a matching VolumeSnapshotClass
        - StorageProfile for the StorageClass has snapshotClass field set
          to a specific VolumeSnapshotClass name
        - Running RHEL VM created using the StorageClass
    """

    def test_snapshot_uses_storage_profile_snapshot_class(self):
        """
        Test that VMSnapshot uses the snapshotClass defined in StorageProfile.

        Steps:
            1. Create a VMSnapshot of the running VM
            2. Wait for the snapshot to become ready
            3. Retrieve the VolumeSnapshot created by the VMSnapshot
            4. Read the volumeSnapshotClassName from the VolumeSnapshot spec

        Expected:
            - VolumeSnapshot volumeSnapshotClassName equals the snapshotClass
              value from StorageProfile
        """
        pass

    def test_restore_vm_from_snapshot_with_storage_profile_snapshot_class(self):
        """
        Test that a VM can be restored from a snapshot created with
        StorageProfile-specified snapshotClass.

        Preconditions:
            - VMSnapshot created using StorageProfile snapshotClass (ready)

        Steps:
            1. Stop the VM
            2. Restore the VM from the snapshot
            3. Wait for restore to complete
            4. Start the VM and wait for it to become running and SSH accessible

        Expected:
            - VM is "Running" and SSH accessible after restore
        """
        pass


class TestStorageProfileSnapshotClassFallback:
    """
    Tests for fallback VolumeSnapshotClass selection when StorageProfile
    has no snapshotClass configured.

    Preconditions:
        - Cluster has snapshot-capable storage backend
        - StorageClass exists with a matching VolumeSnapshotClass
        - StorageProfile for the StorageClass does NOT have snapshotClass set
        - Running RHEL VM created using the StorageClass
    """

    def test_snapshot_falls_back_to_label_based_selection(self):
        """
        Test that VMSnapshot falls back to label-based VolumeSnapshotClass
        selection when StorageProfile has no snapshotClass.

        Steps:
            1. Create a VMSnapshot of the running VM
            2. Wait for the snapshot to become ready
            3. Retrieve the VolumeSnapshot created by the VMSnapshot
            4. Read the volumeSnapshotClassName from the VolumeSnapshot spec

        Expected:
            - VolumeSnapshot volumeSnapshotClassName equals the
              VolumeSnapshotClass whose driver matches the StorageClass
              provisioner (label-based default selection)
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --------- | ---------- | ---------- | -------- | ---- |
| `test_storage_profile_snapshot_class.py` | `TestStorageProfileSnapshotClass` | 2 | P0, P1 | T1 |
| `test_storage_profile_snapshot_class.py` | `TestStorageProfileSnapshotClassFallback` | 1 | P0 | T1 |

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in class with shared preconditions
- [x] Each test has: description, Preconditions (where needed), Steps, Expected
- [x] Each test verifies ONE thing
- [x] Negative tests marked with `[NEGATIVE]` (none in this STD)
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/storage_profile_snapshot_class/std_cnv_61266.md`
