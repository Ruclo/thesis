# Software Test Description (STD)

## Feature: VM Snapshot Restore with runStrategy RerunOnFailure

**STP Reference:** [stps/4.md](/home/fedora/thesis/stps/4.md)
**Jira ID:** [CNV-63819](https://issues.redhat.com/browse/CNV-63819)
**Generated:** 2026-02-21

---

## Summary

This STD covers tests for the bug fix ensuring VM snapshot restore completes successfully when the VM uses `runStrategy: RerunOnFailure`. The core issue was that `virt-controller` immediately tried to start the VM during the restore process, blocking it from completing. Tests are organized into:

- **Tier 1 (Functional):** Verify restore completes with RerunOnFailure, VM does not auto-start during restore, VM can start after restore, and regression tests across other run strategies (Always, Manual, Halted).
- **Tier 2 (End-to-End):** Verify data integrity after restore and multiple snapshot restore operations.

---

## Test Files

### File: `tests/storage/snapshot_restore/test_snapshot_restore_run_strategy.py`

```python
"""
VM Snapshot Restore with runStrategy Tests

STP Reference: stps/4.md
Jira: https://issues.redhat.com/browse/CNV-63819

This module contains Tier 1 functional tests verifying that VM snapshot restore
completes correctly for VMs with different runStrategy values, with primary focus
on the RerunOnFailure run strategy fix.
"""

import pytest


pytestmark = [
    pytest.mark.usefixtures("namespace", "skip_if_no_storage_class_for_snapshot"),
    pytest.mark.tier3,
]


class TestSnapshotRestoreRerunOnFailure:
    """
    Tests for snapshot restore with runStrategy: RerunOnFailure.

    Verifies the fix for CNV-63819 where virt-controller prematurely started
    the VM during restore, blocking the restore from completing.

    Preconditions:
        - VM created with runStrategy: RerunOnFailure
        - VM started and SSH accessible
        - VirtualMachineSnapshot taken from VM
        - Snapshot is in readyToUse state
        - VM stopped
    """

    def test_restore_completes(self):
        """
        Test that snapshot restore completes for VM with RerunOnFailure run strategy.

        Steps:
            1. Create VirtualMachineRestore from the snapshot and wait for it to reach terminal state

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_vm_not_auto_started_during_restore(self):
        """
        Test that VM does not auto-start during snapshot restore with RerunOnFailure.

        Steps:
            1. Create VirtualMachineRestore from the snapshot
            2. While restore is in progress, check for VirtualMachineInstance existence

        Expected:
            - No VirtualMachineInstance exists for the VM during the restore process
        """
        pass

    def test_vm_starts_after_restore(self):
        """
        Test that VM can be manually started after snapshot restore completes.

        Preconditions:
            - VM restored from snapshot (VirtualMachineRestore is Complete)

        Steps:
            1. Start the VM and wait for it to reach Running state

        Expected:
            - VM is "Running" and SSH accessible
        """
        pass


class TestSnapshotRestoreRunStrategies:
    """
    Regression tests for snapshot restore across different run strategies.

    Ensures the fix for CNV-63819 does not regress snapshot restore behavior
    for other runStrategy values.

    Parametrize:
        - run_strategy: [Always, Manual, Halted]

    Preconditions:
        - VM created with the parametrized runStrategy value
        - VM started and SSH accessible (or in appropriate initial state for the strategy)
        - VirtualMachineSnapshot taken from VM
        - Snapshot is in readyToUse state
        - VM stopped
    """

    def test_restore_completes(self):
        """
        Test that snapshot restore completes for VM with the given run strategy.

        Steps:
            1. Create VirtualMachineRestore from the snapshot and wait for it to reach terminal state

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_vm_starts_after_restore(self):
        """
        Test that VM can be started after snapshot restore completes with the given run strategy.

        Preconditions:
            - VM restored from snapshot (VirtualMachineRestore is Complete)

        Steps:
            1. Start the VM and wait for it to reach Running state

        Expected:
            - VM is "Running" and SSH accessible
        """
        pass
```

---

### File: `tests/storage/snapshot_restore/test_snapshot_restore_data_integrity.py`

```python
"""
VM Snapshot Restore Data Integrity Tests

STP Reference: stps/4.md
Jira: https://issues.redhat.com/browse/CNV-63819

This module contains Tier 2 end-to-end tests verifying data integrity after
VM snapshot restore with runStrategy: RerunOnFailure, and tests for restoring
from multiple snapshots.
"""

import pytest


pytestmark = [
    pytest.mark.usefixtures("namespace", "skip_if_no_storage_class_for_snapshot"),
    pytest.mark.tier3,
]


class TestSnapshotRestoreDataIntegrity:
    """
    End-to-end tests for data integrity after snapshot restore with RerunOnFailure.

    Verifies that the restored VM's disk state matches the point-in-time when
    the snapshot was taken: data written before the snapshot is preserved, and
    data written after the snapshot is removed.

    Preconditions:
        - VM created with runStrategy: RerunOnFailure
        - VM started and SSH accessible
        - File written to VM disk: path="/data/before-snapshot.txt", content="pre-snapshot-data"
        - VirtualMachineSnapshot taken from VM
        - Snapshot is in readyToUse state
        - File written to VM disk after snapshot: path="/data/after-snapshot.txt", content="post-snapshot-data"
        - VM stopped
        - VM restored from snapshot (VirtualMachineRestore is Complete)
        - VM started and SSH accessible
    """

    def test_preserves_pre_snapshot_data(self):
        """
        Test that data written before the snapshot is preserved after restore.

        Steps:
            1. Read file /data/before-snapshot.txt from the restored VM

        Expected:
            - File content equals "pre-snapshot-data"
        """
        pass

    def test_removes_post_snapshot_data(self):
        """
        Test that data written after the snapshot is removed after restore.

        Steps:
            1. Check if file /data/after-snapshot.txt exists on the restored VM

        Expected:
            - File /data/after-snapshot.txt does NOT exist
        """
        pass


class TestMultipleSnapshotRestore:
    """
    Tests for restoring from multiple snapshots with RerunOnFailure run strategy.

    Verifies that when multiple snapshots exist, restore operations complete
    successfully regardless of which snapshot is selected.

    Preconditions:
        - VM created with runStrategy: RerunOnFailure
        - VM started and SSH accessible
        - File written to VM: path="/data/state1.txt", content="first-state"
        - First VirtualMachineSnapshot (snapshot-1) taken from VM
        - First snapshot is in readyToUse state
        - File written to VM: path="/data/state2.txt", content="second-state"
        - Second VirtualMachineSnapshot (snapshot-2) taken from VM
        - Second snapshot is in readyToUse state
        - VM stopped
    """

    def test_restore_from_earlier_snapshot_completes(self):
        """
        Test that restore from the earlier snapshot completes when multiple snapshots exist.

        Steps:
            1. Create VirtualMachineRestore from snapshot-1 and wait for it to reach terminal state

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_restore_from_latest_snapshot_completes(self):
        """
        Test that restore from the latest snapshot completes when multiple snapshots exist.

        Steps:
            1. Create VirtualMachineRestore from snapshot-2 and wait for it to reach terminal state

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --- | --- | --- | --- | --- |
| `test_snapshot_restore_run_strategy.py` | `TestSnapshotRestoreRerunOnFailure` | 3 | P1 | T1 |
| `test_snapshot_restore_run_strategy.py` | `TestSnapshotRestoreRunStrategies` | 2 (x3 strategies = 6) | P1/P2 | T1 |
| `test_snapshot_restore_data_integrity.py` | `TestSnapshotRestoreDataIntegrity` | 2 | P1 | T2 |
| `test_snapshot_restore_data_integrity.py` | `TestMultipleSnapshotRestore` | 2 | P2 | T2 |
| **Total** | | **9 unique (12 with parametrization)** | | |

---

## STP Traceability

| STP Scenario | Test Method | File |
| --- | --- | --- |
| Restore with RerunOnFailure (P1) | `TestSnapshotRestoreRerunOnFailure::test_restore_completes` | `test_snapshot_restore_run_strategy.py` |
| VirtualMachineRestore status (P1) | `TestSnapshotRestoreRerunOnFailure::test_restore_completes` | `test_snapshot_restore_run_strategy.py` |
| VM doesn't auto-start (P1) | `TestSnapshotRestoreRerunOnFailure::test_vm_not_auto_started_during_restore` | `test_snapshot_restore_run_strategy.py` |
| Manual start after restore (P1) | `TestSnapshotRestoreRerunOnFailure::test_vm_starts_after_restore` | `test_snapshot_restore_run_strategy.py` |
| Restore with Always (P1) | `TestSnapshotRestoreRunStrategies::test_restore_completes` [Always] | `test_snapshot_restore_run_strategy.py` |
| Restore with Manual/Halted (P2) | `TestSnapshotRestoreRunStrategies::test_restore_completes` [Manual, Halted] | `test_snapshot_restore_run_strategy.py` |
| Complete workflow with data (P1) | `TestSnapshotRestoreDataIntegrity::test_preserves_pre_snapshot_data`, `test_removes_post_snapshot_data` | `test_snapshot_restore_data_integrity.py` |
| Multiple restore operations (P2) | `TestMultipleSnapshotRestore::test_restore_from_earlier_snapshot_completes`, `test_restore_from_latest_snapshot_completes` | `test_snapshot_restore_data_integrity.py` |

---

## Checklist

- [x] STP link in module docstring
- [x] All STP scenarios covered
- [x] Tests grouped in class with shared preconditions
- [x] Each test has: description, Preconditions (if needed), Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]` (none required for this feature)
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented (tier3, usefixtures)
- [x] Parametrization documented where needed (run strategies)
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/vm_snapshot_restore_run_strategy/std_cnv_63819.md`
