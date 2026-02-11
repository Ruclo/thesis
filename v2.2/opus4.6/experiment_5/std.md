# Software Test Description (STD)

## Feature: StorageProfile snapshotClass Honored for VM Snapshot

**STP Reference:** [/home/jzo/thesis/stps/5.md](/home/jzo/thesis/stps/5.md)
**Jira ID:** [CNV-61266](https://issues.redhat.com/browse/CNV-61266)
**Bug Fix:** [CNV-54866](https://issues.redhat.com/browse/CNV-54866)

---

## Summary

This STD covers tests verifying that VM snapshots honor the `snapshotClass` field defined in StorageProfile resources. The bug fix (CNV-54866) adds a check for `StorageProfile.snapshotClass` before falling back to label-based VolumeSnapshotClass selection. Tests validate:

1. VM snapshots use the snapshotClass from StorageProfile when configured
2. Fallback to label-based selection works when StorageProfile has no snapshotClass
3. VM restore succeeds when snapshot was created with StorageProfile-specified snapshotClass
4. Multiple storage classes each use their respective snapshotClass

---

## Test Files

### File: `tests/storage/snapshots/test_storage_profile_snapshot_class.py`

```python
"""
StorageProfile snapshotClass Honored for VM Snapshot Tests

STP Reference: /home/jzo/thesis/stps/5.md
Jira: https://issues.redhat.com/browse/CNV-61266

This module contains tests verifying that VM snapshots honor the snapshotClass
field defined in StorageProfile resources, rather than ignoring it and falling
back to label-based VolumeSnapshotClass selection.
"""

import pytest


pytestmark = pytest.mark.usefixtures(
    "namespace",
    "skip_if_no_storage_class_for_snapshot",
)


class TestStorageProfileSnapshotClassHonored:
    """
    Tests for StorageProfile snapshotClass being honored during VM snapshot creation.

    Markers:
        - storage

    Preconditions:
        - Snapshot-capable storage class available on the cluster
        - StorageProfile resource exists for the storage class
        - StorageProfile configured with a specific snapshotClass value
        - VolumeSnapshotClass matching the snapshotClass value exists
        - Running VM created using the storage class with a data disk
    """

    @pytest.mark.polarion("CNV-61266")
    def test_vm_snapshot_uses_storage_profile_snapshot_class(self):
        """
        Test that a VM snapshot uses the snapshotClass defined in StorageProfile.

        Steps:
            1. Create a VMSnapshot from the running VM
            2. Wait for the VMSnapshot to become ready
            3. Retrieve the VolumeSnapshot created by the VMSnapshot
            4. Read the volumeSnapshotClassName from the VolumeSnapshot

        Expected:
            - VolumeSnapshot's volumeSnapshotClassName equals the snapshotClass from StorageProfile
        """
        pass

    @pytest.mark.polarion("CNV-61266")
    def test_vm_restore_succeeds_with_storage_profile_snapshot_class(self):
        """
        Test that a VM can be restored from a snapshot created with StorageProfile snapshotClass.

        Preconditions:
            - VMSnapshot created from the VM (using StorageProfile snapshotClass)
            - VMSnapshot is in ready state

        Steps:
            1. Restore the VM from the snapshot
            2. Wait for the restore to complete and VM to be running

        Expected:
            - VM is "Running" and SSH accessible after restore
        """
        pass


class TestStorageProfileSnapshotClassFallback:
    """
    Tests for fallback behavior when StorageProfile has no snapshotClass set.

    Markers:
        - storage

    Preconditions:
        - Snapshot-capable storage class available on the cluster
        - StorageProfile resource exists for the storage class
        - StorageProfile does NOT have snapshotClass configured
        - VolumeSnapshotClass with matching driver label exists
        - Running VM created using the storage class with a data disk
    """

    @pytest.mark.polarion("CNV-61266")
    def test_vm_snapshot_falls_back_to_label_based_selection(self):
        """
        Test that VM snapshot falls back to label-based VolumeSnapshotClass selection
        when StorageProfile has no snapshotClass configured.

        Steps:
            1. Create a VMSnapshot from the running VM
            2. Wait for the VMSnapshot to become ready
            3. Retrieve the VolumeSnapshot created by the VMSnapshot
            4. Read the volumeSnapshotClassName from the VolumeSnapshot

        Expected:
            - VolumeSnapshot's volumeSnapshotClassName equals the label-selected VolumeSnapshotClass
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --------- | ---------- | ---------- | -------- | ---- |
| `test_storage_profile_snapshot_class.py` | `TestStorageProfileSnapshotClassHonored` | 2 | P0, P1 | Tier 1 |
| `test_storage_profile_snapshot_class.py` | `TestStorageProfileSnapshotClassFallback` | 1 | P0 | Tier 1 |

---

## Requirements-to-Tests Traceability

| Requirement ID | Requirement Summary | Test Method | Priority |
| -------------- | ------------------- | ----------- | -------- |
| CNV-61266 | Honor snapshotClass | `test_vm_snapshot_uses_storage_profile_snapshot_class` | P0 |
| CNV-61266 | Fallback behavior | `test_vm_snapshot_falls_back_to_label_based_selection` | P0 |
| CNV-61266 | Restore with correct class | `test_vm_restore_succeeds_with_storage_profile_snapshot_class` | P1 |

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Preconditions (where needed), Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/storage_profile_snapshot_class/std_cnv_61266.md`
