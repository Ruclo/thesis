# Software Test Description (STD)

## Feature: VM Snapshot Restore with runStrategy RerunOnFailure

**STP Reference:** [/home/fedora/thesis/stps/4.md](/home/fedora/thesis/stps/4.md)
**Jira ID:** [CNV-63819](https://issues.redhat.com/browse/CNV-63819)
**Generated:** 2026-02-23

---

## Summary

This STD covers test scenarios for verifying that VM snapshot restore completes successfully
for VMs using the `runStrategy: RerunOnFailure` setting (bug fix CNV-63819), along with
regression tests for other run strategies (Always, Manual, Halted). It includes Tier 1
functional tests for restore completion, VM auto-start prevention during restore, and
post-restore VM startup, as well as Tier 2 end-to-end tests for data integrity validation
and multiple snapshot restore operations.

---

## Test Files

### File: `tests/storage/snapshots/test_snapshot_restore_run_strategy.py`

```python
"""
VM Snapshot Restore with runStrategy Tests

STP Reference: /home/fedora/thesis/stps/4.md
Jira: https://issues.redhat.com/browse/CNV-63819

This module contains tests verifying that VM snapshot restore completes
successfully across all run strategies, with focus on the RerunOnFailure
strategy fix (CNV-63819). Previously, virt-controller would immediately
attempt to start the VM during restore, blocking the restore operation.
"""

import pytest


pytestmark = [
    pytest.mark.usefixtures("skip_if_no_storage_class_for_snapshot"),
    pytest.mark.storage,
]


class TestSnapshotRestoreRerunOnFailure:
    """
    Tests for VM snapshot restore with runStrategy: RerunOnFailure.

    Verifies the fix for CNV-63819 where snapshot restore would get stuck
    because virt-controller immediately tried to start the VM, blocking
    the restore operation.

    Markers:
        - gating
        - storage

    Preconditions:
        - VM with runStrategy: RerunOnFailure
        - VM started and running
        - VirtualMachineSnapshot created from VM and ready to use
        - VM stopped
    """

    def test_restore_completes(self):
        """
        Test that snapshot restore completes for a VM with runStrategy RerunOnFailure.

        Steps:
            1. Create VirtualMachineRestore from snapshot and wait for completion

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_vm_not_auto_started_during_restore(self):
        """
        Test that VM does not auto-start during snapshot restore with RerunOnFailure.

        Steps:
            1. Create VirtualMachineRestore from snapshot
            2. While restore is in progress, check for VirtualMachineInstance existence

        Expected:
            - No VirtualMachineInstance exists for the VM during restore
        """
        pass

    def test_vm_starts_after_restore(self):
        """
        Test that a VM with RerunOnFailure can be started after snapshot restore.

        Preconditions:
            - VirtualMachineRestore completed successfully

        Steps:
            1. Start the VM manually and wait for it to reach Running state

        Expected:
            - VM is "Running" and SSH accessible
        """
        pass


class TestSnapshotRestoreRunStrategies:
    """
    Regression tests for snapshot restore across run strategies.

    Verifies that snapshot restore continues to work for all run strategies
    after the RerunOnFailure fix (CNV-63819).

    Markers:
        - storage

    Parametrize:
        - run_strategy: [Always, Manual, Halted]

    Preconditions:
        - VM with parametrized runStrategy value
        - VirtualMachineSnapshot created from VM and ready to use
        - VM stopped
    """

    def test_restore_completes(self):
        """
        Test that snapshot restore completes for a VM with the given run strategy.

        Steps:
            1. Create VirtualMachineRestore from snapshot and wait for completion

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_vm_starts_after_restore(self):
        """
        Test that a VM can be started after snapshot restore with the given run strategy.

        Preconditions:
            - VirtualMachineRestore completed successfully

        Steps:
            1. Start the VM manually and wait for it to reach Running state

        Expected:
            - VM is "Running"
        """
        pass


class TestSnapshotRestoreDataIntegrity:
    """
    End-to-end tests for snapshot restore data integrity with RerunOnFailure.

    Validates that snapshot restore correctly preserves pre-snapshot data
    and removes post-snapshot data for VMs using RerunOnFailure strategy.

    Markers:
        - storage

    Preconditions:
        - Running VM with runStrategy: RerunOnFailure
        - File path="/data/original.txt", content="data-before-snapshot" written to VM
        - VirtualMachineSnapshot created from VM and ready to use
        - File path="/data/after.txt", content="post-snapshot" written to VM after snapshot
        - VM stopped
        - VirtualMachineRestore created from snapshot and completed
        - VM started and SSH accessible
    """

    def test_preserves_pre_snapshot_data(self):
        """
        Test that files created before a snapshot are preserved after restore.

        Steps:
            1. Read file /data/original.txt from the restored VM

        Expected:
            - File content equals "data-before-snapshot"
        """
        pass

    def test_removes_post_snapshot_data(self):
        """
        Test that files created after a snapshot are removed after restore.

        Steps:
            1. Check if file /data/after.txt exists on the restored VM

        Expected:
            - File /data/after.txt does NOT exist
        """
        pass


class TestMultipleSnapshotRestore:
    """
    Tests for restoring from multiple snapshots with RerunOnFailure strategy.

    Verifies that multiple snapshot and restore operations all complete
    successfully for VMs using RerunOnFailure run strategy.

    Markers:
        - storage

    Preconditions:
        - Running VM with runStrategy: RerunOnFailure
        - File path="/data/state1.txt", content="first-snapshot" written to VM
        - First VirtualMachineSnapshot (snapshot-1) created and ready to use
        - File path="/data/state2.txt", content="second-snapshot" written to VM
        - Second VirtualMachineSnapshot (snapshot-2) created and ready to use
        - VM stopped
    """

    def test_restore_from_first_snapshot(self):
        """
        Test that restore from the first of multiple snapshots completes.

        Steps:
            1. Create VirtualMachineRestore from snapshot-1 and wait for completion

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_restore_from_second_snapshot(self):
        """
        Test that restore from the second of multiple snapshots completes.

        Steps:
            1. Create VirtualMachineRestore from snapshot-2 and wait for completion

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
| `test_snapshot_restore_run_strategy.py` | `TestSnapshotRestoreRunStrategies` | 2 (x3 params) | P1/P2 | T1 |
| `test_snapshot_restore_run_strategy.py` | `TestSnapshotRestoreDataIntegrity` | 2 | P1 | T2 |
| `test_snapshot_restore_run_strategy.py` | `TestMultipleSnapshotRestore` | 2 | P2 | T2 |

**Total:** 9 test methods (15 including parametrized expansions)

---

## Traceability

| STP Scenario | Test Method | Covered |
| --- | --- | --- |
| Restore with RerunOnFailure | `TestSnapshotRestoreRerunOnFailure.test_restore_completes` | Yes |
| VirtualMachineRestore status | `TestSnapshotRestoreRerunOnFailure.test_restore_completes` | Yes |
| VM doesn't auto-start during restore | `TestSnapshotRestoreRerunOnFailure.test_vm_not_auto_started_during_restore` | Yes |
| Manual start after restore | `TestSnapshotRestoreRerunOnFailure.test_vm_starts_after_restore` | Yes |
| Restore with Always strategy | `TestSnapshotRestoreRunStrategies.test_restore_completes` (Always param) | Yes |
| Restore with other strategies | `TestSnapshotRestoreRunStrategies.test_restore_completes` (Manual, Halted params) | Yes |
| Complete restore workflow | `TestSnapshotRestoreDataIntegrity` (both tests) | Yes |
| Multiple restore operations | `TestMultipleSnapshotRestore` (both tests) | Yes |

---

## Checklist

- [x] STP link in module docstring
- [x] All STP scenarios covered
- [x] Tests grouped in class with shared preconditions
- [x] Each test has: description, Preconditions (if needed), Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]` (none in this STD)
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] Parametrization documented where needed
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/vm_snapshot_restore/std_cnv_63819.md`
