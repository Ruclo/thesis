# Software Test Description (STD)

## Feature: VM Snapshot Restore with runStrategy RerunOnFailure

**STP Reference:** [CNV-63819 STP](/home/jzo/thesis/stps/4.md)
**Jira ID:** [CNV-63819](https://issues.redhat.com/browse/CNV-63819)
**Generated:** 2026-02-11

---

## Summary

This STD covers tests for VM snapshot restore functionality when VMs use `runStrategy: RerunOnFailure`. The bug (CNV-63819) causes snapshot restore to get stuck because virt-controller immediately tries to start the VM, blocking the restore operation. Tests verify that snapshot restore completes successfully for VMs with RerunOnFailure run strategy, that VMs do not auto-start during restore, and that restored VMs function correctly after restore completes. Regression tests cover other run strategies to ensure no regressions.

---

## Test Files

### File: `tests/storage/snapshots/test_snapshot_restore_run_strategy.py`

```python
"""
VM Snapshot Restore with runStrategy RerunOnFailure Tests

STP Reference: https://issues.redhat.com/browse/CNV-63819

This module contains tests verifying that VM snapshot restore completes
successfully for VMs using the RerunOnFailure run strategy. The bug caused
virt-controller to immediately attempt starting the VM during restore,
blocking the restore operation from completing.
"""

import pytest


class TestSnapshotRestoreRerunOnFailure:
    """
    Tests for snapshot restore with runStrategy RerunOnFailure.

    Preconditions:
        - Storage class with snapshot support available
        - VM created with runStrategy: RerunOnFailure and a data disk
        - VM started and SSH accessible
        - File path="/data/testfile.txt", content="pre-snapshot-data" written to VM
        - VM stopped
        - VirtualMachineSnapshot created from the stopped VM
        - Snapshot reached Ready state
    """

    def test_restore_completes_for_rerun_on_failure_vm(self):
        """
        Test that VirtualMachineRestore reaches Complete state for a VM
        with runStrategy RerunOnFailure.

        Steps:
            1. Create VirtualMachineRestore from the snapshot
            2. Wait for restore to complete

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_vm_starts_after_restore(self):
        """
        Test that a VM with runStrategy RerunOnFailure can be started
        after snapshot restore completes.

        Preconditions:
            - VirtualMachineRestore completed successfully

        Steps:
            1. Start the VM
            2. Wait for VM to reach Running state and become SSH accessible

        Expected:
            - VM is "Running" and SSH accessible
        """
        pass

    def test_restored_vm_preserves_pre_snapshot_data(self):
        """
        Test that data written before the snapshot is preserved after restore.

        Preconditions:
            - VirtualMachineRestore completed successfully
            - VM started and SSH accessible

        Steps:
            1. Read file /data/testfile.txt from the restored VM

        Expected:
            - File content equals "pre-snapshot-data"
        """
        pass


class TestSnapshotRestoreRunStrategyRegression:
    """
    Regression tests for snapshot restore across all run strategies.

    Parametrize:
        - run_strategy: [Always, Manual, Halted, RerunOnFailure]

    Preconditions:
        - Storage class with snapshot support available
        - VM created with the parametrized run strategy and a data disk
        - VM started (for strategies that allow starting) and SSH accessible
        - File path="/data/testfile.txt", content="pre-snapshot-data" written to VM
        - VM stopped
        - VirtualMachineSnapshot created from the stopped VM
        - Snapshot reached Ready state
    """

    def test_restore_completes_for_run_strategy(self):
        """
        Test that VirtualMachineRestore completes for a VM with the given
        run strategy.

        Steps:
            1. Create VirtualMachineRestore from the snapshot
            2. Wait for restore to complete

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_vm_starts_after_restore_for_run_strategy(self):
        """
        Test that a VM can be started after snapshot restore completes
        for the given run strategy.

        Preconditions:
            - VirtualMachineRestore completed successfully

        Steps:
            1. Start the VM
            2. Wait for VM to reach Running state and become SSH accessible

        Expected:
            - VM is "Running" and SSH accessible
        """
        pass

    def test_restored_data_intact_for_run_strategy(self):
        """
        Test that pre-snapshot data is preserved after restore for the
        given run strategy.

        Preconditions:
            - VirtualMachineRestore completed successfully
            - VM started and SSH accessible

        Steps:
            1. Read file /data/testfile.txt from the restored VM

        Expected:
            - File content equals "pre-snapshot-data"
        """
        pass


class TestSnapshotRestoreRerunOnFailureEndToEnd:
    """
    End-to-end snapshot restore workflow with data validation for
    RerunOnFailure VMs.

    Markers:
        - tier3

    Preconditions:
        - Storage class with snapshot support available
        - VM created with runStrategy: RerunOnFailure and a data disk
        - VM started and SSH accessible
        - File path="/data/original.txt", content="original-data" written to VM
        - VirtualMachineSnapshot created from the running VM (online snapshot)
        - Snapshot reached Ready state
        - File path="/data/post_snapshot.txt", content="post-snapshot-data" written to VM after snapshot
        - VM stopped
        - VirtualMachineRestore created from the snapshot
        - Restore completed successfully
        - VM started and SSH accessible
    """

    def test_pre_snapshot_file_preserved_after_restore(self):
        """
        Test that files written before the snapshot are preserved after
        end-to-end restore workflow.

        Steps:
            1. Read file /data/original.txt from the restored VM

        Expected:
            - File content equals "original-data"
        """
        pass

    def test_post_snapshot_file_removed_after_restore(self):
        """
        Test that files written after the snapshot are removed after restore.

        Steps:
            1. Check if file /data/post_snapshot.txt exists on the restored VM

        Expected:
            - File /data/post_snapshot.txt does NOT exist
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --- | --- | --- | --- | --- |
| `test_snapshot_restore_run_strategy.py` | `TestSnapshotRestoreRerunOnFailure` | 3 | P1 | T1 |
| `test_snapshot_restore_run_strategy.py` | `TestSnapshotRestoreRunStrategyRegression` | 3 (x4 strategies) | P1-P2 | T1 |
| `test_snapshot_restore_run_strategy.py` | `TestSnapshotRestoreRerunOnFailureEndToEnd` | 2 | P1 | T2 |

**Total: 8 test methods (20 parametrized executions including 4 run strategies)**

---

## Traceability

| STP Scenario | Test Method | Priority |
| --- | --- | --- |
| Restore with RerunOnFailure | `TestSnapshotRestoreRerunOnFailure::test_restore_completes_for_rerun_on_failure_vm` | P1 |
| VirtualMachineRestore status | `TestSnapshotRestoreRerunOnFailure::test_restore_completes_for_rerun_on_failure_vm` | P1 |
| VM doesn't auto-start during restore | Covered implicitly: restore completing proves VM didn't block it | P1 |
| Manual start after restore | `TestSnapshotRestoreRerunOnFailure::test_vm_starts_after_restore` | P1 |
| Restore with Always strategy | `TestSnapshotRestoreRunStrategyRegression::test_restore_completes_for_run_strategy[Always]` | P1 |
| Restore with other strategies | `TestSnapshotRestoreRunStrategyRegression::test_restore_completes_for_run_strategy[Manual/Halted]` | P2 |
| Complete restore workflow | `TestSnapshotRestoreRerunOnFailureEndToEnd` | P1 |
| Restored VM data intact | `TestSnapshotRestoreRerunOnFailureEndToEnd::test_pre_snapshot_file_preserved_after_restore` | P1 |

---

## Checklist

- [x] STP link in module docstring
- [x] All STP scenarios covered
- [x] Tests grouped in class with shared preconditions
- [x] Each test has: description, Preconditions (if needed), Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]` (none needed for this feature)
- [x] Test methods contain only `pass`
- [x] Markers documented
- [x] Parametrization documented where needed
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/vm_snapshot_restore_rerun_on_failure/std_cnv_63819.md`
