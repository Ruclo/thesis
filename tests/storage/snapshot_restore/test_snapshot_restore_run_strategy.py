"""
VM Snapshot Restore with runStrategy Tests

STP Reference: stps/4.md
Jira: https://issues.redhat.com/browse/CNV-63819

This module contains Tier 1 functional tests verifying that VM snapshot restore
completes correctly for VMs with different runStrategy values, with primary focus
on the RerunOnFailure run strategy fix.
"""

import logging

import pytest
from ocp_resources.virtual_machine import VirtualMachine
from ocp_resources.virtual_machine_restore import VirtualMachineRestore

from utilities.virt import running_vm

LOGGER = logging.getLogger(__name__)


pytestmark = [
    pytest.mark.usefixtures("namespace", "skip_if_no_storage_class_for_snapshot"),
    pytest.mark.tier3,
]


class TestSnapshotRestoreRerunOnFailure:
    """
    Tests for snapshot restore with runStrategy: RerunOnFailure.

    Verifies the fix for CNV-63819 where virt-controller prematurely started
    the VM during restore, blocking the restore from completing.
    """

    @pytest.mark.parametrize(
        "vm_for_snapshot_restore",
        [
            pytest.param(
                {"vm_name": "vm-63819-rerun-restore"},
                marks=pytest.mark.jira("CNV-63819"),
                id="rerun_on_failure",
            ),
        ],
        indirect=True,
    )
    def test_restore_completes(
        self,
        admin_client,
        vm_for_snapshot_restore,
        vm_snapshot_for_restore,
    ):
        """
        Test that snapshot restore completes for VM with RerunOnFailure run strategy.

        Steps:
            1. Create VirtualMachineRestore from the snapshot and wait for it to reach terminal state

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        LOGGER.info(
            f"Restoring VM {vm_for_snapshot_restore.name} from snapshot {vm_snapshot_for_restore.name}"
        )
        with VirtualMachineRestore(
            client=admin_client,
            name=f"restore-{vm_for_snapshot_restore.name}",
            namespace=vm_for_snapshot_restore.namespace,
            vm_name=vm_for_snapshot_restore.name,
            snapshot_name=vm_snapshot_for_restore.name,
        ) as vm_restore:
            vm_restore.wait_restore_done()
            assert vm_restore.instance.status.complete, (
                f"VirtualMachineRestore {vm_restore.name} did not reach Complete status"
            )

    @pytest.mark.parametrize(
        "vm_for_snapshot_restore",
        [
            pytest.param(
                {"vm_name": "vm-63819-rerun-nostart"},
                marks=pytest.mark.jira("CNV-63819"),
                id="rerun_on_failure",
            ),
        ],
        indirect=True,
    )
    def test_vm_not_auto_started_during_restore(
        self,
        admin_client,
        vm_for_snapshot_restore,
        vm_snapshot_for_restore,
    ):
        """
        Test that VM does not auto-start during snapshot restore with RerunOnFailure.

        Steps:
            1. Create VirtualMachineRestore from the snapshot
            2. After restore completes, check VM is not running

        Expected:
            - No VirtualMachineInstance exists for the VM during the restore process
        """
        LOGGER.info(
            f"Restoring VM {vm_for_snapshot_restore.name} and verifying no auto-start"
        )
        with VirtualMachineRestore(
            client=admin_client,
            name=f"restore-{vm_for_snapshot_restore.name}",
            namespace=vm_for_snapshot_restore.namespace,
            vm_name=vm_for_snapshot_restore.name,
            snapshot_name=vm_snapshot_for_restore.name,
        ) as vm_restore:
            vm_restore.wait_restore_done()
            assert not vm_for_snapshot_restore.ready, (
                f"VM {vm_for_snapshot_restore.name} was auto-started during/after restore"
                f" with RerunOnFailure strategy"
            )

    @pytest.mark.parametrize(
        "vm_for_snapshot_restore",
        [
            pytest.param(
                {"vm_name": "vm-63819-rerun-start"},
                marks=pytest.mark.jira("CNV-63819"),
                id="rerun_on_failure",
            ),
        ],
        indirect=True,
    )
    def test_vm_starts_after_restore(
        self,
        admin_client,
        vm_for_snapshot_restore,
        vm_snapshot_for_restore,
    ):
        """
        Test that VM can be manually started after snapshot restore completes.

        Steps:
            1. Create VirtualMachineRestore and wait for completion
            2. Start the VM and wait for it to reach Running state

        Expected:
            - VM is "Running" and SSH accessible
        """
        LOGGER.info(
            f"Restoring VM {vm_for_snapshot_restore.name} and starting after restore"
        )
        with VirtualMachineRestore(
            client=admin_client,
            name=f"restore-{vm_for_snapshot_restore.name}",
            namespace=vm_for_snapshot_restore.namespace,
            vm_name=vm_for_snapshot_restore.name,
            snapshot_name=vm_snapshot_for_restore.name,
        ) as vm_restore:
            vm_restore.wait_restore_done()
            running_vm(vm=vm_for_snapshot_restore)
            assert vm_for_snapshot_restore.ready, (
                f"VM {vm_for_snapshot_restore.name} failed to start after restore"
            )


class TestSnapshotRestoreRunStrategies:
    """
    Regression tests for snapshot restore across different run strategies.

    Ensures the fix for CNV-63819 does not regress snapshot restore behavior
    for other runStrategy values.
    """

    @pytest.mark.parametrize(
        "vm_for_snapshot_restore",
        [
            pytest.param(
                {
                    "vm_name": "vm-63819-always-restore",
                    "run_strategy": VirtualMachine.RunStrategy.ALWAYS,
                },
                id="always_strategy",
            ),
            pytest.param(
                {
                    "vm_name": "vm-63819-manual-restore",
                    "run_strategy": VirtualMachine.RunStrategy.MANUAL,
                },
                id="manual_strategy",
            ),
            pytest.param(
                {
                    "vm_name": "vm-63819-halted-restore",
                    "run_strategy": VirtualMachine.RunStrategy.HALTED,
                },
                id="halted_strategy",
            ),
        ],
        indirect=True,
    )
    def test_restore_completes(
        self,
        admin_client,
        vm_for_snapshot_restore,
        vm_snapshot_for_restore,
    ):
        """
        Test that snapshot restore completes for VM with the given run strategy.

        Steps:
            1. Create VirtualMachineRestore from the snapshot and wait for it to reach terminal state

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        LOGGER.info(
            f"Restoring VM {vm_for_snapshot_restore.name} from snapshot {vm_snapshot_for_restore.name}"
        )
        with VirtualMachineRestore(
            client=admin_client,
            name=f"restore-{vm_for_snapshot_restore.name}",
            namespace=vm_for_snapshot_restore.namespace,
            vm_name=vm_for_snapshot_restore.name,
            snapshot_name=vm_snapshot_for_restore.name,
        ) as vm_restore:
            vm_restore.wait_restore_done()
            assert vm_restore.instance.status.complete, (
                f"VirtualMachineRestore {vm_restore.name} did not reach Complete status"
            )

    @pytest.mark.parametrize(
        "vm_for_snapshot_restore",
        [
            pytest.param(
                {
                    "vm_name": "vm-63819-always-start",
                    "run_strategy": VirtualMachine.RunStrategy.ALWAYS,
                },
                id="always_strategy",
            ),
            pytest.param(
                {
                    "vm_name": "vm-63819-manual-start",
                    "run_strategy": VirtualMachine.RunStrategy.MANUAL,
                },
                id="manual_strategy",
            ),
            pytest.param(
                {
                    "vm_name": "vm-63819-halted-start",
                    "run_strategy": VirtualMachine.RunStrategy.HALTED,
                },
                id="halted_strategy",
            ),
        ],
        indirect=True,
    )
    def test_vm_starts_after_restore(
        self,
        admin_client,
        vm_for_snapshot_restore,
        vm_snapshot_for_restore,
    ):
        """
        Test that VM can be started after snapshot restore completes with the given run strategy.

        Steps:
            1. Create VirtualMachineRestore and wait for completion
            2. Start the VM and wait for it to reach Running state

        Expected:
            - VM is "Running" and SSH accessible
        """
        LOGGER.info(
            f"Restoring VM {vm_for_snapshot_restore.name} and starting after restore"
        )
        with VirtualMachineRestore(
            client=admin_client,
            name=f"restore-{vm_for_snapshot_restore.name}",
            namespace=vm_for_snapshot_restore.namespace,
            vm_name=vm_for_snapshot_restore.name,
            snapshot_name=vm_snapshot_for_restore.name,
        ) as vm_restore:
            vm_restore.wait_restore_done()
            running_vm(vm=vm_for_snapshot_restore)
            assert vm_for_snapshot_restore.ready, (
                f"VM {vm_for_snapshot_restore.name} failed to start after restore"
            )
