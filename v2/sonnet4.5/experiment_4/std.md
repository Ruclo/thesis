# Software Test Description (STD)

## Feature: VM Snapshot Restore with runStrategy RerunOnFailure

**STP Reference:** ../thesis/stps/4.md
**Jira ID:** CNV-63819
**Generated:** 2026-02-03

---

## Summary

This STD contains test cases for verifying that VM snapshot restore operations complete successfully when VMs use the `runStrategy: RerunOnFailure` setting. The bug CNV-63819 reports that snapshot restore gets stuck because virt-controller immediately tries to start the VM, blocking the restore operation from completing.

The test suite covers:
- Primary bug fix verification (snapshot restore with RerunOnFailure)
- VM lifecycle during restore (ensuring VM doesn't auto-start prematurely)
- Data integrity validation after restore
- Regression testing for other run strategies
- End-to-end restore workflows

---

## Test Files

### File: `tests/virt/snapshot/test_snapshot_restore_rerun_on_failure.py`

```python
"""
VM Snapshot Restore with runStrategy RerunOnFailure Tests

STP Reference: ../thesis/stps/4.md
Jira: https://issues.redhat.com/browse/CNV-63819

This module contains tests for verifying snapshot restore functionality
when VMs use runStrategy: RerunOnFailure. Tests verify that the restore
operation completes successfully without getting stuck due to the VM
auto-starting during the restore process.
"""

import pytest


class TestSnapshotRestoreRerunOnFailure:
    """
    Tests for VM snapshot restore with runStrategy: RerunOnFailure.

    Markers:
        - gating
        - tier1

    Preconditions:
        - Storage class with snapshot support (e.g., ocs-storagecluster-ceph-rbd)
        - VirtualMachineSnapshot CRD installed
        - VirtualMachineRestore CRD installed
    """

    def test_restore_completes_with_rerun_on_failure(self):
        """
        Test that snapshot restore completes successfully for VM with runStrategy: RerunOnFailure.

        This is the primary test case for CNV-63819. The bug reports that snapshot restore
        gets stuck indefinitely because virt-controller tries to start the VM during restore.

        Preconditions:
            - VM with runStrategy: RerunOnFailure
            - VM is running
            - VirtualMachineSnapshot created from running VM
            - Snapshot is Ready
            - VM is stopped

        Steps:
            1. Create VirtualMachineRestore resource targeting the snapshot
            2. Wait for restore operation to complete (timeout: 5 minutes)
            3. Check VirtualMachineRestore status

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_vm_does_not_start_during_restore(self):
        """
        Test that VM does not auto-start while restore is in progress.

        This verifies the core issue in CNV-63819 - virt-controller should NOT
        attempt to start the VM while restore is ongoing.

        Preconditions:
            - VM with runStrategy: RerunOnFailure
            - VM is running
            - VirtualMachineSnapshot created from running VM
            - Snapshot is Ready
            - VM is stopped

        Steps:
            1. Create VirtualMachineRestore resource targeting the snapshot
            2. During restore operation, query for VirtualMachineInstance resources
            3. Monitor virt-controller logs for VM start attempts

        Expected:
            - No VirtualMachineInstance exists during restore
        """
        pass

    def test_manual_start_succeeds_after_restore(self):
        """
        Test that VM can be manually started after restore completes.

        Preconditions:
            - VM with runStrategy: RerunOnFailure
            - VirtualMachineSnapshot created
            - VirtualMachineRestore completed successfully
            - VM is stopped

        Steps:
            1. Start the VM manually
            2. Wait for VM to reach Running state

        Expected:
            - VM is "Running"
        """
        pass

    def test_restore_preserves_vm_configuration(self):
        """
        Test that restored VM has the same configuration as the snapshot.

        Preconditions:
            - VM with runStrategy: RerunOnFailure
            - VM configuration includes: 2 vCPUs, 2Gi memory, specific labels
            - VirtualMachineSnapshot created from VM
            - VirtualMachineRestore completed successfully

        Steps:
            1. Query restored VM specification
            2. Compare vCPU count, memory, and labels with original configuration

        Expected:
            - VM vCPU count equals 2
        """
        pass


class TestSnapshotRestoreDataIntegrity:
    """
    Tests for data integrity during snapshot restore with RerunOnFailure.

    Markers:
        - tier2

    Preconditions:
        - Storage class with snapshot support
        - VM with runStrategy: RerunOnFailure
        - VM is running with SSH access
    """

    def test_restore_preserves_data_written_before_snapshot(self):
        """
        Test that files created before snapshot are preserved after restore.

        Preconditions:
            - VM with runStrategy: RerunOnFailure running
            - File path="/data/before-snapshot.txt", content="original-data" created in VM
            - VirtualMachineSnapshot created
            - Snapshot is Ready
            - File path="/data/after-snapshot.txt", content="new-data" created after snapshot
            - VM stopped
            - VirtualMachineRestore completed successfully
            - VM started and SSH accessible

        Steps:
            1. SSH to restored VM
            2. Read file /data/before-snapshot.txt

        Expected:
            - File content equals "original-data"
        """
        pass

    def test_restore_removes_data_written_after_snapshot(self):
        """
        Test that files created after snapshot are removed after restore.

        Preconditions:
            - VM with runStrategy: RerunOnFailure running
            - File path="/data/before-snapshot.txt", content="original-data" created in VM
            - VirtualMachineSnapshot created
            - Snapshot is Ready
            - File path="/data/after-snapshot.txt", content="new-data" created after snapshot
            - VM stopped
            - VirtualMachineRestore completed successfully
            - VM started and SSH accessible

        Steps:
            1. SSH to restored VM
            2. Check if file /data/after-snapshot.txt exists

        Expected:
            - File /data/after-snapshot.txt does NOT exist
        """
        pass

    def test_complete_restore_workflow_with_data_validation(self):
        """
        Test complete end-to-end snapshot restore workflow with data validation.

        This is a comprehensive Tier 2 test covering the full user workflow.

        Preconditions:
            - VM with runStrategy: RerunOnFailure created but not started
            - Storage class with snapshot support

        Steps:
            1. Start VM and wait for Running state
            2. SSH to VM and write test data to /data/test-file.txt
            3. Create VirtualMachineSnapshot
            4. Wait for snapshot Ready state
            5. SSH to VM and write different data to /data/modified.txt
            6. Stop VM
            7. Create VirtualMachineRestore
            8. Wait for restore Complete state
            9. Start VM manually
            10. Wait for VM Running state
            11. SSH to VM and verify /data/test-file.txt exists and has original content
            12. SSH to VM and verify /data/modified.txt does NOT exist

        Expected:
            - File /data/test-file.txt contains original test data
        """
        pass


class TestSnapshotRestoreRunStrategies:
    """
    Regression tests for snapshot restore with different run strategies.

    These tests ensure the fix for RerunOnFailure doesn't break existing
    functionality for other run strategies.

    Markers:
        - tier1
        - gating

    Parametrize:
        - run_strategy: [Always, Manual, Halted, Once]

    Preconditions:
        - Storage class with snapshot support
    """

    def test_restore_completes_with_various_run_strategies(self):
        """
        Test that snapshot restore completes for VMs with different run strategies.

        This is a regression test to ensure the fix doesn't break other run strategies.

        Parametrize:
            - run_strategy: [Always, Manual, Halted, Once]

        Preconditions:
            - VM with runStrategy from parameter
            - VM is running (if strategy allows)
            - VirtualMachineSnapshot created
            - Snapshot is Ready
            - VM is stopped (if applicable)

        Steps:
            1. Create VirtualMachineRestore resource
            2. Wait for restore operation to complete

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_restore_with_always_strategy(self):
        """
        Test that snapshot restore completes for VM with runStrategy: Always.

        Preconditions:
            - VM with runStrategy: Always
            - VM is running
            - VirtualMachineSnapshot created
            - Snapshot is Ready
            - VM is stopped

        Steps:
            1. Create VirtualMachineRestore resource
            2. Wait for restore operation to complete

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_restore_with_manual_strategy(self):
        """
        Test that snapshot restore completes for VM with runStrategy: Manual.

        Preconditions:
            - VM with runStrategy: Manual
            - VM is running
            - VirtualMachineSnapshot created
            - Snapshot is Ready
            - VM is stopped

        Steps:
            1. Create VirtualMachineRestore resource
            2. Wait for restore operation to complete

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass

    def test_restore_with_halted_strategy(self):
        """
        Test that snapshot restore completes for VM with runStrategy: Halted.

        Preconditions:
            - VM with runStrategy: Halted
            - VirtualMachineSnapshot created (VM never started)
            - Snapshot is Ready

        Steps:
            1. Create VirtualMachineRestore resource
            2. Wait for restore operation to complete

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        pass


class TestSnapshotRestoreMultipleOperations:
    """
    Tests for multiple snapshot and restore operations.

    Markers:
        - tier2

    Preconditions:
        - Storage class with snapshot support
        - VM with runStrategy: RerunOnFailure
    """

    def test_restore_from_multiple_snapshots(self):
        """
        Test that VM can be restored from different snapshots.

        Preconditions:
            - VM with runStrategy: RerunOnFailure running
            - File /data/snapshot1.txt created
            - VirtualMachineSnapshot snap1 created
            - File /data/snapshot2.txt created
            - VirtualMachineSnapshot snap2 created
            - VM stopped

        Steps:
            1. Create VirtualMachineRestore from snap1
            2. Wait for restore Complete
            3. Start VM and verify /data/snapshot1.txt exists
            4. Verify /data/snapshot2.txt does NOT exist
            5. Stop VM
            6. Create VirtualMachineRestore from snap2
            7. Wait for restore Complete
            8. Start VM and verify both files exist

        Expected:
            - Both /data/snapshot1.txt and /data/snapshot2.txt exist after second restore
        """
        pass

    def test_sequential_restore_operations(self):
        """
        Test that multiple restore operations can be performed sequentially.

        Preconditions:
            - VM with runStrategy: RerunOnFailure
            - VirtualMachineSnapshot created
            - Snapshot is Ready

        Steps:
            1. Stop VM
            2. Create VirtualMachineRestore (first restore)
            3. Wait for restore Complete
            4. Start VM, make changes, stop VM
            5. Create VirtualMachineRestore (second restore from same snapshot)
            6. Wait for restore Complete

        Expected:
            - Second VirtualMachineRestore status is "Complete"
        """
        pass


class TestSnapshotRestoreNegative:
    """
    Negative tests for snapshot restore error handling.

    Markers:
        - tier2
    """

    def test_restore_from_nonexistent_snapshot(self):
        """
        [NEGATIVE] Test that restore fails gracefully when referencing non-existent snapshot.

        Preconditions:
            - VM with runStrategy: RerunOnFailure

        Steps:
            1. Create VirtualMachineRestore referencing snapshot name "does-not-exist"
            2. Wait for restore to process
            3. Check VirtualMachineRestore status

        Expected:
            - VirtualMachineRestore status is "Failed" or error condition set
        """
        pass

    def test_restore_while_vm_running(self):
        """
        [NEGATIVE] Test that restore operation handles running VM appropriately.

        Preconditions:
            - VM with runStrategy: RerunOnFailure
            - VirtualMachineSnapshot created
            - VM is running

        Steps:
            1. Attempt to create VirtualMachineRestore while VM is running
            2. Check VirtualMachineRestore status

        Expected:
            - VirtualMachineRestore either fails or VM is automatically stopped first
        """
        pass


class TestSnapshotRestoreMonitoring:
    """
    Tests for monitoring and observability during snapshot restore.

    Markers:
        - tier2

    Preconditions:
        - VM with runStrategy: RerunOnFailure
        - Prometheus metrics available
    """

    def test_restore_progress_monitoring(self):
        """
        Test that restore progress can be monitored via VirtualMachineRestore status.

        Preconditions:
            - VM with runStrategy: RerunOnFailure running
            - VirtualMachineSnapshot created and Ready
            - VM stopped

        Steps:
            1. Create VirtualMachineRestore
            2. Poll VirtualMachineRestore status conditions
            3. Monitor status progression from Progressing to Complete

        Expected:
            - VirtualMachineRestore transitions through expected status phases
        """
        pass

    def test_no_controller_errors_during_restore(self):
        """
        Test that virt-controller logs no errors during restore operation.

        Preconditions:
            - VM with runStrategy: RerunOnFailure
            - VirtualMachineSnapshot created
            - VM stopped

        Steps:
            1. Create VirtualMachineRestore
            2. Wait for restore Complete
            3. Query virt-controller pod logs for ERROR level messages related to this VM

        Expected:
            - No ERROR messages in virt-controller logs for this VM during restore
        """
        pass
```

---

### File: `tests/virt/snapshot/conftest.py`

```python
"""
Shared fixtures for snapshot restore tests.

This module provides common fixtures for VM snapshot and restore testing,
including VM creation with different run strategies, snapshot creation,
and data validation utilities.
"""

import pytest


@pytest.fixture
def vm_with_rerun_on_failure(namespace, unprivileged_client):
    """
    Create a VM with runStrategy: RerunOnFailure.

    Yields:
        VirtualMachine: VM resource with RerunOnFailure run strategy
    """
    pass


@pytest.fixture
def vm_with_run_strategy(namespace, unprivileged_client, request):
    """
    Create a VM with specified run strategy.

    Args:
        request.param (str): Run strategy (Always, Manual, Halted, RerunOnFailure, Once)

    Yields:
        VirtualMachine: VM resource with specified run strategy
    """
    pass


@pytest.fixture
def running_vm_with_rerun_on_failure(vm_with_rerun_on_failure):
    """
    Start VM with RerunOnFailure and wait for Running state.

    Yields:
        VirtualMachine: Running VM with RerunOnFailure strategy
    """
    pass


@pytest.fixture
def vm_snapshot(running_vm_with_rerun_on_failure):
    """
    Create VirtualMachineSnapshot from running VM.

    Yields:
        VirtualMachineSnapshot: Ready snapshot resource
    """
    pass


@pytest.fixture
def stopped_vm_with_snapshot(running_vm_with_rerun_on_failure, vm_snapshot):
    """
    VM with snapshot, in stopped state.

    Yields:
        tuple: (VirtualMachine, VirtualMachineSnapshot) - VM stopped, snapshot ready
    """
    pass


@pytest.fixture
def vm_snapshot_restore(stopped_vm_with_snapshot):
    """
    Create and complete VirtualMachineRestore operation.

    Yields:
        VirtualMachineRestore: Completed restore resource
    """
    pass


@pytest.fixture
def ssh_connection(running_vm_with_rerun_on_failure):
    """
    SSH connection to running VM.

    Yields:
        SSHClient: Active SSH connection to VM
    """
    pass


@pytest.fixture
def vm_with_test_data(running_vm_with_rerun_on_failure, ssh_connection):
    """
    Running VM with test data file written.

    Yields:
        tuple: (VirtualMachine, str) - VM and path to test data file
    """
    pass


@pytest.fixture
def snapshot_capable_storage_class(admin_client):
    """
    Get or verify snapshot-capable storage class.

    Returns:
        str: Name of storage class supporting VolumeSnapshots
    """
    pass
```

---

## Test Coverage Summary

| Test File                                  | Test Class                             | Test Count | Priority | Tier |
| ------------------------------------------ | -------------------------------------- | ---------- | -------- | ---- |
| `test_snapshot_restore_rerun_on_failure.py` | `TestSnapshotRestoreRerunOnFailure`    | 4          | P1       | T1   |
| `test_snapshot_restore_rerun_on_failure.py` | `TestSnapshotRestoreDataIntegrity`     | 3          | P1       | T2   |
| `test_snapshot_restore_rerun_on_failure.py` | `TestSnapshotRestoreRunStrategies`     | 5          | P1       | T1   |
| `test_snapshot_restore_rerun_on_failure.py` | `TestSnapshotRestoreMultipleOperations`| 2          | P2       | T2   |
| `test_snapshot_restore_rerun_on_failure.py` | `TestSnapshotRestoreNegative`          | 2          | P2       | T2   |
| `test_snapshot_restore_rerun_on_failure.py` | `TestSnapshotRestoreMonitoring`        | 2          | P2       | T2   |
| **Total**                                  |                                        | **18**     |          |      |

---

## Test Coverage Mapping to STP Requirements

| STP Requirement                            | Test Coverage                                      | Status |
| ------------------------------------------ | -------------------------------------------------- | ------ |
| Snapshot restore with RerunOnFailure       | `test_restore_completes_with_rerun_on_failure`     | ✓      |
| VM doesn't auto-start during restore       | `test_vm_does_not_start_during_restore`            | ✓      |
| VirtualMachineRestore reaches Complete     | All restore completion tests                       | ✓      |
| Manual start after restore                 | `test_manual_start_succeeds_after_restore`         | ✓      |
| Restored VM has correct configuration      | `test_restore_preserves_vm_configuration`          | ✓      |
| Data integrity after restore               | `TestSnapshotRestoreDataIntegrity` class           | ✓      |
| Regression for other run strategies        | `TestSnapshotRestoreRunStrategies` class           | ✓      |
| Complete E2E workflow                      | `test_complete_restore_workflow_with_data_validation` | ✓   |
| Multiple restore operations                | `TestSnapshotRestoreMultipleOperations` class      | ✓      |
| Error handling                             | `TestSnapshotRestoreNegative` class                | ✓      |
| Monitoring and observability               | `TestSnapshotRestoreMonitoring` class              | ✓      |

---

## Checklist

- [x] All STP scenarios covered
- [x] Each test verifies ONE thing
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Markers documented (gating, tier1, tier2)
- [x] Parametrization documented where applicable
- [x] STP reference in module docstring
- [x] Tests grouped logically in classes
- [x] Shared preconditions in class docstrings
- [x] Test-specific preconditions in test docstrings
- [x] All test methods contain only `pass`
- [x] Fixtures defined in conftest.py
- [x] Coverage summary table included
- [x] Output saved to `tests/std/vm_snapshot_restore_rerun_on_failure/std_cnv_63819.md`

---

## Notes

1. **Primary Bug Fix Tests**: The core tests for CNV-63819 are in `TestSnapshotRestoreRerunOnFailure`, focusing on restore completion and VM lifecycle behavior.

2. **Data Integrity**: `TestSnapshotRestoreDataIntegrity` verifies that snapshot restore correctly preserves state, which is critical for backup/recovery workflows.

3. **Regression Coverage**: `TestSnapshotRestoreRunStrategies` ensures the fix doesn't break existing functionality for Always, Manual, Halted, and Once strategies.

4. **Fixtures Design**: The `conftest.py` provides layered fixtures that build on each other, allowing tests to start from the exact precondition state they need.

5. **Tier Assignment**:
   - **Tier 1**: Core functionality and regression tests (fast, must pass)
   - **Tier 2**: E2E workflows, multiple operations, monitoring (comprehensive)

6. **Gating Tests**: Critical tests marked with `@pytest.mark.gating` for CI/CD pipelines.

7. **Negative Tests**: Error handling tests ensure graceful failure for invalid operations.

8. **Monitoring**: Tests verify observability through status conditions and controller logs.
