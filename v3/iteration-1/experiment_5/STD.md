# Software Test Description (STD)

## Feature: StorageProfile snapshotClass Honored for VM Snapshot

**STP Reference:** [/home/fedora/thesis/stps/5.md](/home/fedora/thesis/stps/5.md)
**Jira ID:** [CNV-61266](https://issues.redhat.com/browse/CNV-61266) / [CNV-54866](https://issues.redhat.com/browse/CNV-54866)
**Generated:** 2026-02-21

---

## Summary

This STD covers tests verifying that the VMSnapshot controller honors the `snapshotClass` field from `StorageProfile` when selecting a `VolumeSnapshotClass` for VM snapshots. Tests cover the primary behavior (snapshotClass honored), fallback behavior (label-based selection when no snapshotClass is set), and snapshot restore using the correct VolumeSnapshotClass.

---

## Test Files

### File: `tests/storage/snapshots/test_storageprofile_snapshot_class.py`

```python
"""
StorageProfile snapshotClass Honored for VM Snapshot Tests

STP Reference: /home/fedora/thesis/stps/5.md

This module contains tests verifying that VMSnapshot honors the snapshotClass
field from StorageProfile when selecting a VolumeSnapshotClass. Covers both
the primary path (snapshotClass set) and the fallback path (label-based
selection), as well as snapshot restore with the correct VolumeSnapshotClass.
"""

import pytest


class TestStorageProfileSnapshotClass:
    """
    Tests for StorageProfile snapshotClass selection during VM snapshot creation.

    Markers:
        - storage

    Preconditions:
        - Cluster with snapshot-capable storage backend (e.g., ODF/Ceph)
        - At least one VolumeSnapshotClass available for the storage provisioner
        - Running VM with a data volume backed by a snapshot-capable StorageClass
    """

    def test_snapshot_uses_storageprofile_snapshot_class(self):
        """
        Test that VMSnapshot uses the snapshotClass specified in the StorageProfile.

        Preconditions:
            - StorageProfile for the VM's StorageClass has snapshotClass set
              to a specific VolumeSnapshotClass name

        Steps:
            1. Create a VMSnapshot of the running VM
            2. Wait for VMSnapshot to become ready
            3. Retrieve the VolumeSnapshot created by the VMSnapshot
            4. Read the volumeSnapshotClassName from the VolumeSnapshot spec

        Expected:
            - VolumeSnapshot's volumeSnapshotClassName equals the snapshotClass
              value from the StorageProfile
        """
        pass

    def test_snapshot_falls_back_to_label_based_selection(self):
        """
        Test that VMSnapshot falls back to label-based VolumeSnapshotClass
        selection when StorageProfile has no snapshotClass set.

        Preconditions:
            - StorageProfile for the VM's StorageClass does NOT have
              snapshotClass set (field is empty or absent)

        Steps:
            1. Create a VMSnapshot of the running VM
            2. Wait for VMSnapshot to become ready
            3. Retrieve the VolumeSnapshot created by the VMSnapshot
            4. Read the volumeSnapshotClassName from the VolumeSnapshot spec

        Expected:
            - VolumeSnapshot's volumeSnapshotClassName equals the
              VolumeSnapshotClass whose driver matches the StorageClass
              provisioner (label-based fallback selection)
        """
        pass

    def test_restore_vm_from_snapshot_with_storageprofile_snapshot_class(self):
        """
        Test that a VM can be successfully restored from a snapshot created
        using the StorageProfile-specified snapshotClass.

        Preconditions:
            - StorageProfile for the VM's StorageClass has snapshotClass set
            - VMSnapshot created and ready (using StorageProfile snapshotClass)
            - VM is stopped

        Steps:
            1. Create a VirtualMachineRestore from the VMSnapshot
            2. Wait for restore to complete
            3. Start the VM and wait for it to become running and SSH accessible

        Expected:
            - VM is "Running" and SSH accessible after restore
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --- | --- | --- | --- | --- |
| `test_storageprofile_snapshot_class.py` | `TestStorageProfileSnapshotClass` | 3 | P0, P0, P1 | Tier 1 |

---

## Traceability Matrix

| Requirement ID | Requirement Summary | Test Method | Priority |
| --- | --- | --- | --- |
| CNV-61266 | Honor snapshotClass from StorageProfile | `test_snapshot_uses_storageprofile_snapshot_class` | P0 |
| CNV-61266 | Fallback to label-based selection | `test_snapshot_falls_back_to_label_based_selection` | P0 |
| CNV-61266 | Restore with correct VolumeSnapshotClass | `test_restore_vm_from_snapshot_with_storageprofile_snapshot_class` | P1 |

---

## Design Decisions

1. **Scenario 4 (Multiple Storage Classes) excluded from Tier 1**: The STP lists this as Tier 2 / P2. The three Tier 1 scenarios fully cover the core fix (honor snapshotClass, fallback, restore). Multi-StorageClass coverage can be added separately if needed.

2. **Single test class**: All three tests share the same preconditions (snapshot-capable cluster, running VM) and are closely related, so they are grouped under one class.

3. **StorageProfile modification as fixture concern**: The snapshotClass configuration on StorageProfile is a precondition, not a test step. The implementation phase will use a fixture (with `ResourceEditor` or equivalent) to set/unset the snapshotClass field, keeping test bodies focused on verification.

4. **Fallback verification approach**: The fallback test verifies that the selected VolumeSnapshotClass matches the one whose driver corresponds to the StorageClass provisioner, which is the label-based selection mechanism.

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in class with shared preconditions
- [x] Each test has: description, Preconditions, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]` (none applicable)
- [x] Test methods contain only `pass`
- [x] Markers documented (storage)
- [x] Parametrization documented where needed (none needed for Tier 1)
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/storageprofile_snapshot_class/std_cnv_61266.md`
