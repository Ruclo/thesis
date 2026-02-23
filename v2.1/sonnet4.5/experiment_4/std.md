# Software Test Description (STD)

## Feature: VM Snapshot Restore with runStrategy RerunOnFailure

**STP Reference:** [CNV-63819 - VM snapshot restore stuck with runStrategy RerunOnFailure](https://issues.redhat.com/browse/CNV-63819)

**Jira ID:** CNV-63819

**Generated:** 2026-02-10

---

## Summary

This STD covers testing for the bug fix addressing VM snapshot restore getting stuck when VMs have `runStrategy: RerunOnFailure`. The tests verify that:

1. Snapshot restore completes successfully for VMs with RerunOnFailure run strategy
2. VMs do not auto-start during the restore process (which was blocking restore completion)
3. VirtualMachineRestore resources reach Complete state
4. Restored VMs can be manually started after restore completes
5. Restored VMs have correct state and data
6. Regression testing ensures other run strategies still work correctly

The test suite includes:
- **Tier 1 tests**: Functional tests for specific snapshot restore behaviors
- **Tier 2 tests**: End-to-end workflows with data validation

---

## Test Files

### File: `tests/virt/storage/snapshot/test_vm_snapshot_restore_runstrategy.py`

```python
"""
VM Snapshot Restore with runStrategy Tests

STP Reference: https://issues.redhat.com/browse/CNV-63819

This module contains tests for verifying snapshot restore functionality
works correctly with different VM run strategies, particularly fixing
the issue where snapshot restore gets stuck with runStrategy: RerunOnFailure.
"""

import pytest


class TestSnapshotRestoreRerunOnFailure:
    """
    Tests for VM snapshot restore with runStrategy: RerunOnFailure.

    Markers:
        - gating
        - polarion: CNV-63819

    Preconditions:
        - Storage class with snapshot support (e.g., ODF Ceph RBD)
        - VM with runStrategy: RerunOnFailure
        - VM is running
        - VirtualMachineSnapshot created from running VM
        - VM is stopped
    """

    def test_restore_completes_successfully(self):
        """
        Test that snapshot restore completes for VM with runStrategy: RerunOnFailure.

        Steps:
            1. Create VirtualMachineRestore resource from snapshot
            2. Wait for restore operation to complete

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_vm_does_not_start_during_restore(self):
        """
        Test that VM does not auto-start during snapshot restore operation.

        Steps:
            1. Create VirtualMachineRestore resource from snapshot
            2. Monitor for VirtualMachineInstance creation during restore
            3. Wait for restore to complete

        Expected:
            - VirtualMachineInstance does NOT exist during restore operation
        """
        pass

    def test_vm_can_start_after_restore(self):
        """
        Test that VM can be manually started after snapshot restore completes.

        Preconditions:
            - Snapshot restore has completed successfully
            - VM is in stopped state

        Steps:
            1. Manually start the VM
            2. Wait for VM to reach Running status

        Expected:
            - VM is "Running" and SSH accessible
        """
        pass


class TestSnapshotRestoreRunStrategyRegression:
    """
    Regression tests for snapshot restore with other run strategies.

    Markers:
        - gating
        - polarion: CNV-63819

    Parametrize:
        - run_strategy: [Always, Manual, Halted]

    Preconditions:
        - Storage class with snapshot support
        - VM with runStrategy from parameter
        - VirtualMachineSnapshot created
        - VM is in appropriate state for restore
    """

    def test_restore_completes_with_run_strategy(self):
        """
        Test that snapshot restore completes for VMs with various run strategies.

        Steps:
            1. Create VirtualMachineRestore resource from snapshot
            2. Wait for restore operation to complete

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_vm_behavior_after_restore(self):
        """
        Test that VM exhibits correct behavior after restore based on run strategy.

        Steps:
            1. Wait for restore to complete
            2. Observe VM state based on run strategy

        Expected:
            - VM behavior matches run strategy (Always: auto-starts, Manual/Halted: stays stopped)
        """
        pass


class TestSnapshotRestoreDataIntegrity:
    """
    End-to-end tests for snapshot restore with data validation.

    Markers:
        - tier2
        - polarion: CNV-63819

    Preconditions:
        - Storage class with snapshot support
        - VM with runStrategy: RerunOnFailure
        - VM is running and SSH accessible
    """

    def test_complete_restore_workflow_preserves_data(self):
        """
        Test that complete snapshot restore workflow preserves VM data.

        Steps:
            1. Write test data to VM disk (/tmp/test-data.txt with content "snapshot-test")
            2. Create VirtualMachineSnapshot
            3. Wait for snapshot to be ready
            4. Stop the VM
            5. Create VirtualMachineRestore from snapshot
            6. Wait for restore to complete
            7. Manually start the VM
            8. Wait for VM to be SSH accessible
            9. Read test data from VM disk

        Expected:
            - File /tmp/test-data.txt content equals "snapshot-test"
        """
        pass

    def test_restore_removes_post_snapshot_changes(self):
        """
        Test that snapshot restore removes changes made after snapshot was taken.

        Steps:
            1. Create VirtualMachineSnapshot
            2. Wait for snapshot to be ready
            3. Write new file to VM (/tmp/after-snapshot.txt)
            4. Stop the VM
            5. Create VirtualMachineRestore from snapshot
            6. Wait for restore to complete
            7. Manually start the VM
            8. Wait for VM to be SSH accessible
            9. Check if /tmp/after-snapshot.txt exists

        Expected:
            - File /tmp/after-snapshot.txt does NOT exist
        """
        pass


class TestSnapshotRestoreMultipleOperations:
    """
    Tests for multiple snapshot restore operations.

    Markers:
        - tier2
        - polarion: CNV-63819

    Preconditions:
        - Storage class with snapshot support
        - VM with runStrategy: RerunOnFailure
        - VM is running
        - Multiple VirtualMachineSnapshots created at different times
    """

    def test_restore_from_different_snapshots(self):
        """
        Test that VM can be restored from different snapshots sequentially.

        Steps:
            1. Create first snapshot (snapshot-1)
            2. Modify VM state
            3. Create second snapshot (snapshot-2)
            4. Stop VM
            5. Restore from snapshot-2
            6. Wait for restore to complete
            7. Stop VM
            8. Restore from snapshot-1
            9. Wait for restore to complete

        Expected:
            - Both VirtualMachineRestore operations complete successfully
        """
        pass

    def test_multiple_restores_in_sequence(self):
        """
        Test that multiple restore operations can be performed in sequence.

        Steps:
            1. Restore VM from snapshot
            2. Wait for restore to complete
            3. Start VM
            4. Stop VM
            5. Restore VM from same snapshot again
            6. Wait for second restore to complete

        Expected:
            - Second VirtualMachineRestore status is "Complete"
        """
        pass


class TestSnapshotRestoreNegative:
    """
    Negative tests for snapshot restore operations.

    Markers:
        - polarion: CNV-63819

    Preconditions:
        - Storage class with snapshot support
        - VM with runStrategy: RerunOnFailure
    """

    def test_restore_fails_for_nonexistent_snapshot(self):
        """
        [NEGATIVE] Test that restore fails gracefully for non-existent snapshot.

        Steps:
            1. Create VirtualMachineRestore referencing non-existent snapshot
            2. Wait for restore to process

        Expected:
            - VirtualMachineRestore status is "Failed" or contains error condition
        """
        pass

    def test_restore_cannot_proceed_with_running_vm(self):
        """
        [NEGATIVE] Test that restore cannot proceed while VM is running.

        Preconditions:
            - VM is in running state
            - Valid snapshot exists

        Steps:
            1. Attempt to create VirtualMachineRestore while VM is running
            2. Monitor restore status

        Expected:
            - VirtualMachineRestore fails or waits until VM is stopped
        """
        pass
```

---

### File: `tests/virt/storage/snapshot/conftest.py`

```python
"""
Shared fixtures for VM snapshot restore tests.

This module provides fixtures for creating VMs with different run strategies,
taking snapshots, and managing restore operations.
"""

import pytest


@pytest.fixture()
def vm_with_rerun_on_failure(
    namespace,
    unprivileged_client,
    data_volume_scope_function,
):
    """
    Running VM with runStrategy: RerunOnFailure.

    Yields:
        VirtualMachine: VM with RerunOnFailure run strategy, in running state
    """
    pass


@pytest.fixture()
def vm_with_run_strategy(
    request,
    namespace,
    unprivileged_client,
    data_volume_scope_function,
):
    """
    VM with specified run strategy.

    Parametrize via request.param with dict:
        - run_strategy: RunStrategy value (Always, Manual, Halted, RerunOnFailure)

    Yields:
        VirtualMachine: VM with specified run strategy
    """
    pass


@pytest.fixture()
def vm_snapshot(
    vm_with_rerun_on_failure,
    namespace,
    unprivileged_client,
):
    """
    VirtualMachineSnapshot of running VM.

    Yields:
        VirtualMachineSnapshot: Ready snapshot of VM
    """
    pass


@pytest.fixture()
def stopped_vm_with_snapshot(
    vm_with_rerun_on_failure,
    vm_snapshot,
):
    """
    Stopped VM with existing snapshot.

    Preconditions:
        - VM has snapshot created while running
        - VM is stopped

    Yields:
        tuple: (VirtualMachine, VirtualMachineSnapshot)
    """
    pass


@pytest.fixture()
def vm_with_test_data(
    vm_with_rerun_on_failure,
):
    """
    Running VM with test data written to disk.

    Creates file /tmp/test-data.txt with content "snapshot-test"

    Yields:
        VirtualMachine: VM with test data file
    """
    pass


@pytest.fixture()
def multiple_snapshots(
    vm_with_rerun_on_failure,
    namespace,
    unprivileged_client,
):
    """
    Multiple VirtualMachineSnapshots of same VM.

    Creates 3 snapshots at different points in time

    Yields:
        list[VirtualMachineSnapshot]: List of ready snapshots
    """
    pass


@pytest.fixture()
def snapshot_capable_storage_class(
    admin_client,
):
    """
    Storage class with VolumeSnapshot support.

    Yields:
        StorageClass: Storage class supporting snapshots (e.g., ODF Ceph RBD)
    """
    pass


@pytest.fixture()
def vm_restore(
    request,
    vm_snapshot,
    namespace,
    unprivileged_client,
):
    """
    VirtualMachineRestore resource.

    Parametrize via request.param with dict:
        - snapshot: VirtualMachineSnapshot to restore from

    Yields:
        VirtualMachineRestore: Restore resource (may be in progress or completed)
    """
    pass
```

---

## Test Coverage Summary

| Test File                                      | Test Class                             | Test Count | Priority | Tier |
| ---------------------------------------------- | -------------------------------------- | ---------- | -------- | ---- |
| `test_vm_snapshot_restore_runstrategy.py`      | `TestSnapshotRestoreRerunOnFailure`    | 3          | P1       | T1   |
| `test_vm_snapshot_restore_runstrategy.py`      | `TestSnapshotRestoreRunStrategyRegression` | 2      | P1       | T1   |
| `test_vm_snapshot_restore_runstrategy.py`      | `TestSnapshotRestoreDataIntegrity`     | 2          | P1       | T2   |
| `test_vm_snapshot_restore_runstrategy.py`      | `TestSnapshotRestoreMultipleOperations`| 2          | P2       | T2   |
| `test_vm_snapshot_restore_runstrategy.py`      | `TestSnapshotRestoreNegative`          | 2          | P2       | T1   |
| **Total**                                      |                                        | **11**     |          |      |

---

## Requirements Traceability

| Requirement ID | Test Class                             | Test Method                               | Coverage |
| -------------- | -------------------------------------- | ----------------------------------------- | -------- |
| CNV-63819      | TestSnapshotRestoreRerunOnFailure      | test_restore_completes_successfully       | ✓        |
| CNV-63819      | TestSnapshotRestoreRerunOnFailure      | test_vm_does_not_start_during_restore     | ✓        |
| CNV-63819      | TestSnapshotRestoreRerunOnFailure      | test_vm_can_start_after_restore           | ✓        |
| CNV-63819      | TestSnapshotRestoreRunStrategyRegression | test_restore_completes_with_run_strategy | ✓        |
| CNV-63819      | TestSnapshotRestoreRunStrategyRegression | test_vm_behavior_after_restore          | ✓        |
| CNV-63819      | TestSnapshotRestoreDataIntegrity       | test_complete_restore_workflow_preserves_data | ✓    |
| CNV-63819      | TestSnapshotRestoreDataIntegrity       | test_restore_removes_post_snapshot_changes | ✓       |
| CNV-63819      | TestSnapshotRestoreMultipleOperations  | test_restore_from_different_snapshots     | ✓        |
| CNV-63819      | TestSnapshotRestoreMultipleOperations  | test_multiple_restores_in_sequence        | ✓        |
| CNV-63819      | TestSnapshotRestoreNegative            | test_restore_fails_for_nonexistent_snapshot | ✓      |
| CNV-63819      | TestSnapshotRestoreNegative            | test_restore_cannot_proceed_with_running_vm | ✓      |

---

## Test Scenarios Mapped to STP

### Tier 1 Functional Tests

1. **Verify restore with RerunOnFailure** → `test_restore_completes_successfully`
   - Validates VirtualMachineRestore reaches Complete status

2. **Verify VM doesn't auto-start during restore** → `test_vm_does_not_start_during_restore`
   - Ensures no VMI is created during restore (root cause of bug)

3. **Verify manual start after restore** → `test_vm_can_start_after_restore`
   - Confirms VM can be started after restore completes

4. **Regression: Restore with other run strategies** → `test_restore_completes_with_run_strategy`
   - Tests Always, Manual, Halted run strategies

5. **Regression: VM behavior after restore** → `test_vm_behavior_after_restore`
   - Validates run strategy behavior is preserved

### Tier 2 End-to-End Tests

1. **Complete restore workflow with data validation** → `test_complete_restore_workflow_preserves_data`
   - End-to-end workflow: Create VM → Add data → Snapshot → Stop → Restore → Start → Verify data

2. **Post-snapshot changes removed** → `test_restore_removes_post_snapshot_changes`
   - Validates snapshot point-in-time restore

3. **Multiple snapshots** → `test_restore_from_different_snapshots`
   - Tests restoring from different snapshots sequentially

4. **Sequential restores** → `test_multiple_restores_in_sequence`
   - Validates multiple restore operations

### Negative Tests

1. **Non-existent snapshot** → `test_restore_fails_for_nonexistent_snapshot`
   - Error handling for invalid snapshot reference

2. **Restore with running VM** → `test_restore_cannot_proceed_with_running_vm`
   - Validates restore constraints

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Preconditions (where needed), Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented (gating, tier2, polarion)
- [x] Parametrization documented where needed
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/vm_snapshot_restore_runstrategy/std_cnv_63819.md`

---

## Implementation Notes

### Key Testing Focus

1. **Primary Bug Validation**: Ensure VirtualMachineRestore completes (not stuck indefinitely)
2. **Root Cause Verification**: VM must not auto-start during restore (RerunOnFailure behavior)
3. **Regression Coverage**: All run strategies must still work correctly
4. **Data Integrity**: Restored VMs must have correct state matching snapshot

### Fixture Design

- `vm_with_rerun_on_failure`: Primary fixture for RerunOnFailure testing
- `vm_with_run_strategy`: Parametrized fixture for regression testing
- `vm_snapshot`: Snapshot creation and lifecycle management
- `stopped_vm_with_snapshot`: Common state for restore tests
- `vm_with_test_data`: Data validation scenarios

### Expected Test Execution

1. **Tier 1 tests** run in gating (CI/CD pipeline)
2. **Tier 2 tests** run in nightly or release validation
3. **Negative tests** validate error handling
4. All tests independent, can run in parallel

### Automation Priority

1. P1: Core snapshot restore with RerunOnFailure (gating)
2. P1: Regression tests for other run strategies (gating)
3. P2: End-to-end data validation (tier2)
4. P2: Multiple restore operations (tier2)
