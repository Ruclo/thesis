# Software Test Description (STD)

## Feature: StorageProfile snapshotClass Honored for VM Snapshot

**STP Reference:** [/home/fedora/thesis/stps/5.md](/home/fedora/thesis/stps/5.md)
**Jira ID:** [CNV-61266](https://issues.redhat.com/browse/CNV-61266)
**Bug Fix:** [CNV-54866](https://issues.redhat.com/browse/CNV-54866)
**Generated:** 2026-02-23

---

## Summary

This STD covers tests verifying that VM snapshots honor the `snapshotClass` field defined in StorageProfile resources. The bug fix (CNV-54866) modifies the snapshot controller to check `StorageProfile.Status.SnapshotClass` before falling back to annotation-based or label-based VolumeSnapshotClass selection.

Tests validate:

1. VM snapshots use the snapshotClass from StorageProfile when configured
2. Fallback to default VolumeSnapshotClass selection works when StorageProfile has no snapshotClass
3. VM restore succeeds when the snapshot was created with a StorageProfile-specified snapshotClass
4. Snapshot and restore cycle works end-to-end with correct VolumeSnapshotClass

---

## Test Files

### File: `tests/storage/snapshots/test_storage_profile_snapshot_class.py`

```python
"""
StorageProfile snapshotClass Honored for VM Snapshot Tests

STP Reference: /home/fedora/thesis/stps/5.md
Jira: https://issues.redhat.com/browse/CNV-61266

This module contains tests verifying that VM snapshots honor the snapshotClass
field defined in StorageProfile resources, rather than ignoring it and falling
back to annotation-based VolumeSnapshotClass selection.
"""

import pytest


class TestStorageProfileSnapshotClassHonored:
    """
    Tests for StorageProfile snapshotClass being honored during VM snapshot creation.

    Markers:
        - storage

    Preconditions:
        - Snapshot-capable storage class available on the cluster
        - StorageProfile resource exists for the storage class
        - StorageProfile configured with a specific snapshotClass value pointing
          to an existing VolumeSnapshotClass
        - Running VM created using the storage class with a data volume
    """

    @pytest.mark.polarion("CNV-61266")
    def test_vm_snapshot_uses_storage_profile_snapshot_class(self):
        """
        Test that a VM snapshot uses the snapshotClass defined in StorageProfile.

        Steps:
            1. Create a VMSnapshot from the running VM
            2. Wait for the VMSnapshot to reach ready state
            3. Retrieve the VolumeSnapshot created by the VMSnapshot
            4. Read the volumeSnapshotClassName from the VolumeSnapshot spec

        Expected:
            - VolumeSnapshot's volumeSnapshotClassName equals the snapshotClass
              configured in StorageProfile
        """
        pass

    @pytest.mark.polarion("CNV-61266")
    def test_vm_restore_succeeds_with_storage_profile_snapshot_class(self):
        """
        Test that a VM can be restored from a snapshot created with
        StorageProfile-specified snapshotClass.

        Preconditions:
            - VMSnapshot created from the VM using StorageProfile snapshotClass
            - VMSnapshot is in ready state
            - VM is stopped

        Steps:
            1. Create a VirtualMachineRestore from the snapshot
            2. Wait for the restore to complete
            3. Start the VM and wait for it to reach Running status

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
        - VolumeSnapshotClass with matching provisioner driver exists
        - Running VM created using the storage class with a data volume
    """

    @pytest.mark.polarion("CNV-61266")
    def test_vm_snapshot_falls_back_to_default_selection(self):
        """
        Test that VM snapshot falls back to default VolumeSnapshotClass selection
        when StorageProfile has no snapshotClass configured.

        Steps:
            1. Create a VMSnapshot from the running VM
            2. Wait for the VMSnapshot to reach ready state
            3. Retrieve the VolumeSnapshot created by the VMSnapshot
            4. Read the volumeSnapshotClassName from the VolumeSnapshot spec

        Expected:
            - VolumeSnapshot's volumeSnapshotClassName equals the default
              VolumeSnapshotClass for the storage provisioner
        """
        pass


class TestSnapshotRestoreCycleWithStorageProfileSnapshotClass:
    """
    Tests for end-to-end snapshot and restore cycle verifying data integrity
    when StorageProfile snapshotClass is configured.

    Markers:
        - storage

    Preconditions:
        - Snapshot-capable storage class available on the cluster
        - StorageProfile configured with a specific snapshotClass value
        - Running VM created using the storage class with a data volume
        - File path="/data/pre-snapshot.txt", content="before-snapshot" written to VM
        - VMSnapshot created from the VM and in ready state
        - File path="/data/post-snapshot.txt", content="after-snapshot" written to VM
          (after snapshot creation)
        - VM stopped
        - VM restored from the snapshot
        - VM started, running, and SSH accessible
    """

    @pytest.mark.polarion("CNV-61266")
    def test_pre_snapshot_file_preserved_after_restore(self):
        """
        Test that files created before the snapshot are preserved after restore.

        Steps:
            1. Read file /data/pre-snapshot.txt from the restored VM via SSH

        Expected:
            - File content equals "before-snapshot"
        """
        pass

    @pytest.mark.polarion("CNV-61266")
    def test_post_snapshot_file_removed_after_restore(self):
        """
        Test that files created after the snapshot are removed after restore.

        Steps:
            1. Check if file /data/post-snapshot.txt exists on the restored VM via SSH

        Expected:
            - File /data/post-snapshot.txt does NOT exist
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --------- | ---------- | ---------- | -------- | ---- |
| `test_storage_profile_snapshot_class.py` | `TestStorageProfileSnapshotClassHonored` | 2 | P0, P1 | Tier 1 |
| `test_storage_profile_snapshot_class.py` | `TestStorageProfileSnapshotClassFallback` | 1 | P0 | Tier 1 |
| `test_storage_profile_snapshot_class.py` | `TestSnapshotRestoreCycleWithStorageProfileSnapshotClass` | 2 | P1 | Tier 1 |

---

## Requirements-to-Tests Traceability

| Requirement ID | Requirement Summary | Test Method | Priority |
| -------------- | ------------------- | ----------- | -------- |
| CNV-61266 | Honor snapshotClass from StorageProfile | `test_vm_snapshot_uses_storage_profile_snapshot_class` | P0 |
| CNV-61266 | Fallback when no snapshotClass configured | `test_vm_snapshot_falls_back_to_default_selection` | P0 |
| CNV-61266 | Restore with StorageProfile-specified class | `test_vm_restore_succeeds_with_storage_profile_snapshot_class` | P1 |
| CNV-61266 | Data preserved through snapshot/restore cycle | `test_pre_snapshot_file_preserved_after_restore` | P1 |
| CNV-61266 | Post-snapshot data removed after restore | `test_post_snapshot_file_removed_after_restore` | P1 |

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Requirements-to-tests traceability table included
- [x] Output saved to `tests/std/storage_profile_snapshot_class/std_cnv_61266.md`
