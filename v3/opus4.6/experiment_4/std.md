# Software Test Description (STD)

## Feature: VM Snapshot Restore with runStrategy RerunOnFailure

**STP Reference:** [../stps/4.md](../../../stps/4.md)
**Jira ID:** [CNV-63819](https://issues.redhat.com/browse/CNV-63819)
**Generated:** 2026-02-16

---

## Summary

Tests for CNV-63819: VM snapshot restore gets stuck when the VM has `runStrategy: RerunOnFailure`. The root cause is that `virt-controller` immediately attempts to start the VM during the restore operation, blocking restore completion.

Tests are organized into:

- **Tier 1**: Core fix validation (RerunOnFailure restore completes, VM not auto-started during restore, VM starts after restore) and regression testing across other run strategies (Always, Manual, Halted)
- **Tier 2**: End-to-end data integrity validation and multiple snapshot restore operations

---

## Test Files

### File: `tests/storage/snapshots/test_snapshot_restore_run_strategy.py`

```python
"""
VM Snapshot Restore with runStrategy RerunOnFailure Tests

STP Reference: ../stps/4.md
Jira: CNV-63819

This module contains tests for VM snapshot restore across different run strategies,
with focus on the RerunOnFailure strategy where restore previously got stuck due to
virt-controller prematurely starting the VM during the restore operation.
"""

import pytest


class TestSnapshotRestoreRerunOnFailure:
    """
    Tests for snapshot restore with runStrategy: RerunOnFailure.

    Validates the fix for CNV-63819 where snapshot restore gets stuck because
    virt-controller attempts to start the VM during the restore operation.

    Preconditions:
        - Storage class with snapshot support available
        - VM created with runStrategy: RerunOnFailure
        - VM started and SSH accessible
        - VirtualMachineSnapshot taken from the running VM
        - Snapshot is in readyToUse state
        - VM stopped
    """

    def test_snapshot_restore_completes(self):
        """
        Test that snapshot restore completes for VM with runStrategy RerunOnFailure.

        Steps:
            1. Create VirtualMachineRestore from the snapshot
            2. Wait for restore to reach terminal state

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
            - No VirtualMachineInstance resource exists for the VM during restore
        """
        pass

    def test_vm_starts_after_restore(self):
        """
        Test that VM can be manually started after snapshot restore completes.

        Preconditions:
            - VirtualMachineRestore has completed successfully

        Steps:
            1. Start the VM manually
            2. Wait for VM to reach Running state

        Expected:
            - VM is "Running" and SSH accessible
        """
        pass


class TestSnapshotRestoreRunStrategyRegression:
    """
    Regression tests for snapshot restore across different run strategies.

    Validates that the fix for CNV-63819 does not break snapshot restore
    for other run strategies.

    Parametrize:
        - run_strategy: [Always, Manual, Halted]

    Preconditions:
        - Storage class with snapshot support available
        - VM created with the parametrized run strategy
        - VM started and SSH accessible
        - VirtualMachineSnapshot taken
        - Snapshot is in readyToUse state
        - VM stopped
    """

    def test_snapshot_restore_completes(self):
        """
        Test that snapshot restore completes for VM with the given run strategy.

        Steps:
            1. Create VirtualMachineRestore from the snapshot
            2. Wait for restore to reach terminal state

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_vm_starts_after_restore(self):
        """
        Test that VM can be started after snapshot restore with the given run strategy.

        Preconditions:
            - VirtualMachineRestore has completed successfully

        Steps:
            1. Start the VM
            2. Wait for VM to reach Running state

        Expected:
            - VM is "Running" and SSH accessible
        """
        pass


class TestSnapshotRestoreDataIntegrity:
    """
    End-to-end tests for snapshot restore data integrity with RerunOnFailure.

    Validates that a restored VM has correct data state matching the snapshot point-in-time.

    Preconditions:
        - Storage class with snapshot support available
        - VM created with runStrategy: RerunOnFailure
        - VM started and SSH accessible
        - File path="/data/original.txt", content="data-before-snapshot"
        - VirtualMachineSnapshot taken
        - Snapshot is in readyToUse state
        - File path="/data/after.txt", content="post-snapshot-data" written after snapshot
        - VM stopped
        - VirtualMachineRestore completed successfully
        - VM started and SSH accessible
    """

    def test_preserves_pre_snapshot_data(self):
        """
        Test that files created before snapshot are preserved after restore.

        Steps:
            1. Read file /data/original.txt from the restored VM

        Expected:
            - File content equals "data-before-snapshot"
        """
        pass

    def test_removes_post_snapshot_data(self):
        """
        Test that files created after snapshot are removed after restore.

        Steps:
            1. Check if file /data/after.txt exists on the restored VM

        Expected:
            - File /data/after.txt does NOT exist
        """
        pass


def test_multiple_snapshot_restores_complete():
    """
    Test that multiple snapshots can be restored sequentially.

    Preconditions:
        - Storage class with snapshot support available
        - VM created with runStrategy: RerunOnFailure
        - VM started and SSH accessible
        - Three VirtualMachineSnapshots taken at different points
        - All snapshots in readyToUse state
        - VM stopped

    Steps:
        1. Restore from first snapshot and wait for completion
        2. Restore from third snapshot and wait for completion

    Expected:
        - Both VirtualMachineRestore operations reach "Complete" status
    """
    pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| :--- | :--- | :--- | :--- | :--- |
| `test_snapshot_restore_run_strategy.py` | `TestSnapshotRestoreRerunOnFailure` | 3 | P1 | T1 |
| `test_snapshot_restore_run_strategy.py` | `TestSnapshotRestoreRunStrategyRegression` | 2 (x3 params) | P1/P2 | T1 |
| `test_snapshot_restore_run_strategy.py` | `TestSnapshotRestoreDataIntegrity` | 2 | P1 | T2 |
| `test_snapshot_restore_run_strategy.py` | (standalone) | 1 | P2 | T2 |

**Total: 8 test functions (12 with parametrization)**

---

## STP Traceability

| STP Scenario | STD Test | Coverage |
| :--- | :--- | :--- |
| Restore with RerunOnFailure (T1, P1) | `TestSnapshotRestoreRerunOnFailure::test_snapshot_restore_completes` | Full |
| VirtualMachineRestore reaches Complete (T1, P1) | `TestSnapshotRestoreRerunOnFailure::test_snapshot_restore_completes` | Merged with above (same assertion) |
| VM doesn't auto-start during restore (T1, P1) | `TestSnapshotRestoreRerunOnFailure::test_vm_not_auto_started_during_restore` | Full |
| Manual start after restore (T1, P1) | `TestSnapshotRestoreRerunOnFailure::test_vm_starts_after_restore` | Full |
| Restore with Always strategy (T1, P1) | `TestSnapshotRestoreRunStrategyRegression::test_snapshot_restore_completes[Always]` | Full |
| Restore with Manual/Halted strategies (T1, P2) | `TestSnapshotRestoreRunStrategyRegression::test_snapshot_restore_completes[Manual/Halted]` | Full |
| Complete restore workflow with data validation (T2, P1) | `TestSnapshotRestoreDataIntegrity` (both tests) | Full |
| Multiple restore operations (T2, P2) | `test_multiple_snapshot_restores_complete` | Full |

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in class with shared preconditions
- [x] Each test has: description, Preconditions (if needed), Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]` (none needed - all verify correct behavior)
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] Parametrization documented where needed
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/vm_snapshot_restore_rerun_on_failure/std_cnv_63819.md`
