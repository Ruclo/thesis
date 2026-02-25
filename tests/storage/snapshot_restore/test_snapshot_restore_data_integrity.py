"""
VM Snapshot Restore Data Integrity Tests

STP Reference: stps/4.md
Jira: https://issues.redhat.com/browse/CNV-63819

This module contains Tier 2 end-to-end tests verifying data integrity after
VM snapshot restore with runStrategy: RerunOnFailure, and tests for restoring
from multiple snapshots.
"""

import logging
import shlex

import pytest
from ocp_resources.virtual_machine_restore import VirtualMachineRestore
from pyhelper_utils.shell import run_ssh_commands

from tests.storage.snapshots.utils import run_command_on_vm_and_check_output

LOGGER = logging.getLogger(__name__)


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
    """

    @pytest.mark.parametrize(
        "vm_for_snapshot_restore",
        [
            pytest.param(
                {"vm_name": "vm-63819-data-pre"},
                marks=pytest.mark.jira("CNV-63819"),
                id="rerun_on_failure",
            ),
        ],
        indirect=True,
    )
    def test_preserves_pre_snapshot_data(self, restored_vm_with_data):
        """
        Test that data written before the snapshot is preserved after restore.

        Steps:
            1. Read file before-snapshot.txt from the restored VM

        Expected:
            - File content equals "pre-snapshot-data"
        """
        LOGGER.info(f"Checking pre-snapshot data on restored VM {restored_vm_with_data.name}")
        run_command_on_vm_and_check_output(
            vm=restored_vm_with_data,
            command="cat before-snapshot.txt",
            expected_result="pre-snapshot-data",
        )

    @pytest.mark.parametrize(
        "vm_for_snapshot_restore",
        [
            pytest.param(
                {"vm_name": "vm-63819-data-post"},
                marks=pytest.mark.jira("CNV-63819"),
                id="rerun_on_failure",
            ),
        ],
        indirect=True,
    )
    def test_removes_post_snapshot_data(self, restored_vm_with_data):
        """
        Test that data written after the snapshot is removed after restore.

        Steps:
            1. Check if file after-snapshot.txt exists on the restored VM

        Expected:
            - File after-snapshot.txt does NOT exist
        """
        LOGGER.info(f"Checking post-snapshot data absence on restored VM {restored_vm_with_data.name}")
        file_listing = run_ssh_commands(
            host=restored_vm_with_data.ssh_exec,
            commands=shlex.split("ls -1"),
        )[0]
        assert "after-snapshot.txt" not in file_listing, (
            f"File after-snapshot.txt should not exist after restore, but found in listing: {file_listing}"
        )


class TestMultipleSnapshotRestore:
    """
    Tests for restoring from multiple snapshots with RerunOnFailure run strategy.

    Verifies that when multiple snapshots exist, restore operations complete
    successfully regardless of which snapshot is selected.
    """

    @pytest.mark.parametrize(
        "vm_for_snapshot_restore",
        [
            pytest.param(
                {"vm_name": "vm-63819-multi-earlier"},
                marks=pytest.mark.jira("CNV-63819"),
                id="rerun_on_failure",
            ),
        ],
        indirect=True,
    )
    def test_restore_from_earlier_snapshot_completes(
        self,
        admin_client,
        vm_for_snapshot_restore,
        multiple_snapshots_for_restore,
    ):
        """
        Test that restore from the earlier snapshot completes when multiple snapshots exist.

        Steps:
            1. Create VirtualMachineRestore from snapshot-1 and wait for it to reach terminal state

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        earlier_snapshot = multiple_snapshots_for_restore[0]
        LOGGER.info(
            f"Restoring VM {vm_for_snapshot_restore.name} from earlier snapshot {earlier_snapshot.name}"
        )
        with VirtualMachineRestore(
            client=admin_client,
            name=f"restore-earlier-{vm_for_snapshot_restore.name}",
            namespace=vm_for_snapshot_restore.namespace,
            vm_name=vm_for_snapshot_restore.name,
            snapshot_name=earlier_snapshot.name,
        ) as vm_restore:
            vm_restore.wait_restore_done()
            assert vm_restore.instance.status.complete, (
                f"VirtualMachineRestore {vm_restore.name} did not reach Complete status"
            )

    @pytest.mark.parametrize(
        "vm_for_snapshot_restore",
        [
            pytest.param(
                {"vm_name": "vm-63819-multi-latest"},
                marks=pytest.mark.jira("CNV-63819"),
                id="rerun_on_failure",
            ),
        ],
        indirect=True,
    )
    def test_restore_from_latest_snapshot_completes(
        self,
        admin_client,
        vm_for_snapshot_restore,
        multiple_snapshots_for_restore,
    ):
        """
        Test that restore from the latest snapshot completes when multiple snapshots exist.

        Steps:
            1. Create VirtualMachineRestore from snapshot-2 and wait for it to reach terminal state

        Expected:
            - VirtualMachineRestore status is "Complete"
        """
        latest_snapshot = multiple_snapshots_for_restore[1]
        LOGGER.info(
            f"Restoring VM {vm_for_snapshot_restore.name} from latest snapshot {latest_snapshot.name}"
        )
        with VirtualMachineRestore(
            client=admin_client,
            name=f"restore-latest-{vm_for_snapshot_restore.name}",
            namespace=vm_for_snapshot_restore.namespace,
            vm_name=vm_for_snapshot_restore.name,
            snapshot_name=latest_snapshot.name,
        ) as vm_restore:
            vm_restore.wait_restore_done()
            assert vm_restore.instance.status.complete, (
                f"VirtualMachineRestore {vm_restore.name} did not reach Complete status"
            )
