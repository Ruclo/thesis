# -*- coding: utf-8 -*-

"""
StorageProfile snapshotClass Honored for VM Snapshot Tests

STP Reference: /home/fedora/thesis/stps/5.md

This module contains tests verifying that VMSnapshot honors the snapshotClass
field from StorageProfile when selecting a VolumeSnapshotClass. Covers both
the primary path (snapshotClass set) and the fallback path (label-based
selection), as well as snapshot restore with the correct VolumeSnapshotClass.
"""

import logging

import pytest
from kubernetes.dynamic import DynamicClient
from ocp_resources.storage_class import StorageClass
from ocp_resources.virtual_machine_restore import VirtualMachineRestore
from ocp_resources.virtual_machine_snapshot import VirtualMachineSnapshot
from ocp_resources.volume_snapshot import VolumeSnapshot
from ocp_resources.volume_snapshot_class import VolumeSnapshotClass

from utilities.constants import TIMEOUT_8MIN
from utilities.virt import running_vm

LOGGER = logging.getLogger(__name__)

pytestmark = pytest.mark.usefixtures(
    "skip_if_no_storage_class_for_snapshot",
)


def get_volume_snapshot_class_for_sc_provisioner(
    storage_class_name: str,
    admin_client: DynamicClient,
) -> str:
    """Find the VolumeSnapshotClass whose driver matches the StorageClass provisioner.

    Args:
        storage_class_name: Name of the StorageClass to match.
        admin_client: Kubernetes dynamic client.

    Returns:
        Name of the matching VolumeSnapshotClass.
    """
    storage_class_instance = StorageClass(client=admin_client, name=storage_class_name).instance
    provisioner = storage_class_instance.provisioner
    for volume_snapshot_class in VolumeSnapshotClass.get(client=admin_client):
        if volume_snapshot_class.instance.driver == provisioner:
            return volume_snapshot_class.name
    raise ValueError(f"No VolumeSnapshotClass found with driver matching provisioner '{provisioner}'")


def get_volume_snapshot_class_name_from_vm_snapshot(
    vm_snapshot: VirtualMachineSnapshot,
    admin_client: DynamicClient,
) -> str:
    """Retrieve the volumeSnapshotClassName from the VolumeSnapshot created by a VMSnapshot.

    The VirtualMachineSnapshot status contains a virtualMachineSnapshotContentName
    that references a VirtualMachineSnapshotContent. That content has volumeBackups
    with volumeSnapshotName entries pointing to the actual VolumeSnapshot objects.

    Args:
        vm_snapshot: A ready VirtualMachineSnapshot.
        admin_client: Kubernetes dynamic client.

    Returns:
        The volumeSnapshotClassName from the first VolumeSnapshot.
    """
    snapshot_content_name = vm_snapshot.instance.status.virtualMachineSnapshotContentName
    LOGGER.info(f"VMSnapshot content name: {snapshot_content_name}")

    volume_snapshots = list(VolumeSnapshot.get(
        client=admin_client,
        namespace=vm_snapshot.namespace,
    ))
    LOGGER.info(f"Found {len(volume_snapshots)} VolumeSnapshots in namespace {vm_snapshot.namespace}")

    for volume_snapshot in volume_snapshots:
        volume_snapshot_class_name = volume_snapshot.instance.spec.get("volumeSnapshotClassName")
        if volume_snapshot_class_name:
            LOGGER.info(
                f"VolumeSnapshot '{volume_snapshot.name}' uses "
                f"volumeSnapshotClassName: '{volume_snapshot_class_name}'"
            )
            return volume_snapshot_class_name

    raise ValueError(
        f"No VolumeSnapshot with volumeSnapshotClassName found in namespace '{vm_snapshot.namespace}'"
    )


class TestStorageProfileSnapshotClassHonored:
    """
    Tests for StorageProfile snapshotClass selection during VM snapshot creation.

    Preconditions:
        - Cluster with snapshot-capable storage backend (e.g., ODF/Ceph)
        - At least one VolumeSnapshotClass available for the storage provisioner
        - Running VM with a data volume backed by a snapshot-capable StorageClass
        - StorageProfile for the VM's StorageClass has snapshotClass set
          to a specific VolumeSnapshotClass name
    """

    @pytest.mark.parametrize(
        "rhel_vm_name",
        [
            pytest.param(
                {"vm_name": "vm-cnv-61266-sp-honored"},
                marks=pytest.mark.polarion("CNV-61266"),
            ),
        ],
        indirect=True,
    )
    def test_snapshot_uses_storageprofile_snapshot_class(
        self,
        admin_client,
        rhel_vm_for_snapshot,
        snapshot_storage_class_name_scope_module,
        storageprofile_with_snapshot_class,
    ):
        """
        Test that VMSnapshot uses the snapshotClass specified in the StorageProfile.

        Steps:
            1. Create a VMSnapshot of the running VM
            2. Wait for VMSnapshot to become ready
            3. Retrieve the VolumeSnapshot created by the VMSnapshot
            4. Read the volumeSnapshotClassName from the VolumeSnapshot spec

        Expected:
            - VolumeSnapshot's volumeSnapshotClassName equals the snapshotClass
              value from the StorageProfile
        """
        expected_snapshot_class = storageprofile_with_snapshot_class.snapshotclass
        LOGGER.info(f"Expected snapshotClass from StorageProfile: {expected_snapshot_class}")

        with VirtualMachineSnapshot(
            name="vm-snapshot-sp-honored",
            namespace=rhel_vm_for_snapshot.namespace,
            vm_name=rhel_vm_for_snapshot.name,
            client=admin_client,
        ) as vm_snapshot:
            vm_snapshot.wait_snapshot_done(timeout=TIMEOUT_8MIN)

            actual_snapshot_class = get_volume_snapshot_class_name_from_vm_snapshot(
                vm_snapshot=vm_snapshot,
                admin_client=admin_client,
            )
            assert actual_snapshot_class == expected_snapshot_class, (
                f"VolumeSnapshot used '{actual_snapshot_class}' but StorageProfile "
                f"specified '{expected_snapshot_class}'"
            )

    @pytest.mark.parametrize(
        "rhel_vm_name",
        [
            pytest.param(
                {"vm_name": "vm-cnv-61266-sp-restore"},
                marks=pytest.mark.polarion("CNV-61266"),
            ),
        ],
        indirect=True,
    )
    def test_restore_vm_from_snapshot_with_storageprofile_snapshot_class(
        self,
        admin_client,
        rhel_vm_for_snapshot,
        storageprofile_with_snapshot_class,
    ):
        """
        Test that a VM can be successfully restored from a snapshot created
        using the StorageProfile-specified snapshotClass.

        Steps:
            1. Create a VMSnapshot and wait for it to become ready
            2. Stop the VM
            3. Create a VirtualMachineRestore from the VMSnapshot
            4. Wait for restore to complete
            5. Start the VM and wait for it to become running and SSH accessible

        Expected:
            - VM is "Running" and SSH accessible after restore
        """
        with VirtualMachineSnapshot(
            name="vm-snapshot-sp-restore",
            namespace=rhel_vm_for_snapshot.namespace,
            vm_name=rhel_vm_for_snapshot.name,
            client=admin_client,
        ) as vm_snapshot:
            vm_snapshot.wait_snapshot_done(timeout=TIMEOUT_8MIN)

            rhel_vm_for_snapshot.stop(wait=True)

            with VirtualMachineRestore(
                name="vm-restore-sp-snapshot-class",
                namespace=rhel_vm_for_snapshot.namespace,
                vm_name=rhel_vm_for_snapshot.name,
                snapshot_name=vm_snapshot.name,
                client=admin_client,
            ) as vm_restore:
                vm_restore.wait_restore_done()

                running_vm(vm=rhel_vm_for_snapshot)
                LOGGER.info("VM is running and SSH accessible after restore")


class TestStorageProfileSnapshotClassFallback:
    """
    Tests for StorageProfile snapshotClass fallback behavior.

    Preconditions:
        - Cluster with snapshot-capable storage backend (e.g., ODF/Ceph)
        - At least one VolumeSnapshotClass available for the storage provisioner
        - Running VM with a data volume backed by a snapshot-capable StorageClass
        - StorageProfile for the VM's StorageClass does NOT have snapshotClass set
    """

    @pytest.mark.parametrize(
        "rhel_vm_name",
        [
            pytest.param(
                {"vm_name": "vm-cnv-61266-fallback"},
                marks=pytest.mark.polarion("CNV-61266"),
            ),
        ],
        indirect=True,
    )
    def test_snapshot_falls_back_to_label_based_selection(
        self,
        admin_client,
        rhel_vm_for_snapshot,
        snapshot_storage_class_name_scope_module,
    ):
        """
        Test that VMSnapshot falls back to label-based VolumeSnapshotClass
        selection when StorageProfile has no snapshotClass set.

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
        expected_snapshot_class = get_volume_snapshot_class_for_sc_provisioner(
            storage_class_name=snapshot_storage_class_name_scope_module,
            admin_client=admin_client,
        )
        LOGGER.info(f"Expected fallback VolumeSnapshotClass (by driver match): {expected_snapshot_class}")

        with VirtualMachineSnapshot(
            name="vm-snapshot-fallback",
            namespace=rhel_vm_for_snapshot.namespace,
            vm_name=rhel_vm_for_snapshot.name,
            client=admin_client,
        ) as vm_snapshot:
            vm_snapshot.wait_snapshot_done(timeout=TIMEOUT_8MIN)

            actual_snapshot_class = get_volume_snapshot_class_name_from_vm_snapshot(
                vm_snapshot=vm_snapshot,
                admin_client=admin_client,
            )
            assert actual_snapshot_class == expected_snapshot_class, (
                f"VolumeSnapshot used '{actual_snapshot_class}' but expected fallback "
                f"VolumeSnapshotClass '{expected_snapshot_class}' (driver-based selection)"
            )
