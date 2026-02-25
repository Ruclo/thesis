"""
Pytest conftest for VM snapshot restore with runStrategy tests.

CNV-63819: VM snapshot restore stuck with runStrategy RerunOnFailure
"""

import logging

import pytest
from ocp_resources.virtual_machine import VirtualMachine
from ocp_resources.virtual_machine_cluster_instancetype import (
    VirtualMachineClusterInstancetype,
)
from ocp_resources.virtual_machine_cluster_preference import (
    VirtualMachineClusterPreference,
)
from ocp_resources.virtual_machine_restore import VirtualMachineRestore
from ocp_resources.virtual_machine_snapshot import VirtualMachineSnapshot

from utilities.constants import OS_FLAVOR_RHEL, RHEL10_PREFERENCE, U1_SMALL
from utilities.storage import data_volume_template_with_source_ref_dict, write_file_via_ssh
from utilities.virt import VirtualMachineForTests, running_vm

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def vm_for_snapshot_restore(
    request,
    admin_client,
    namespace,
    rhel10_data_source_scope_session,
    snapshot_storage_class_name_scope_module,
):
    """VM with specified runStrategy for snapshot restore testing."""
    run_strategy = request.param.get("run_strategy", VirtualMachine.RunStrategy.RERUNONFAILURE)
    with VirtualMachineForTests(
        name=request.param["vm_name"],
        namespace=namespace.name,
        client=admin_client,
        os_flavor=OS_FLAVOR_RHEL,
        run_strategy=run_strategy,
        vm_instance_type=VirtualMachineClusterInstancetype(client=admin_client, name=U1_SMALL),
        vm_preference=VirtualMachineClusterPreference(client=admin_client, name=RHEL10_PREFERENCE),
        data_volume_template=data_volume_template_with_source_ref_dict(
            data_source=rhel10_data_source_scope_session,
            storage_class=snapshot_storage_class_name_scope_module,
        ),
    ) as vm:
        running_vm(vm=vm)
        yield vm


@pytest.fixture()
def vm_snapshot_for_restore(admin_client, vm_for_snapshot_restore):
    """Offline snapshot of VM, with VM stopped after snapshot is ready."""
    vm_for_snapshot_restore.stop(wait=True)
    with VirtualMachineSnapshot(
        name=f"snapshot-{vm_for_snapshot_restore.name}",
        namespace=vm_for_snapshot_restore.namespace,
        vm_name=vm_for_snapshot_restore.name,
        client=admin_client,
    ) as snapshot:
        snapshot.wait_snapshot_done()
        yield snapshot


@pytest.fixture()
def snapshot_with_data_for_restore(admin_client, vm_for_snapshot_restore):
    """Snapshot with pre/post-snapshot data written for data integrity testing.

    Writes data before snapshot, takes offline snapshot, writes data after snapshot.
    VM is stopped and ready for restore after this fixture completes.
    """
    write_file_via_ssh(
        vm=vm_for_snapshot_restore,
        filename="before-snapshot.txt",
        content="pre-snapshot-data",
    )
    vm_for_snapshot_restore.stop(wait=True)
    with VirtualMachineSnapshot(
        name=f"snapshot-data-{vm_for_snapshot_restore.name}",
        namespace=vm_for_snapshot_restore.namespace,
        vm_name=vm_for_snapshot_restore.name,
        client=admin_client,
    ) as snapshot:
        snapshot.wait_snapshot_done()
        running_vm(vm=vm_for_snapshot_restore)
        write_file_via_ssh(
            vm=vm_for_snapshot_restore,
            filename="after-snapshot.txt",
            content="post-snapshot-data",
        )
        vm_for_snapshot_restore.stop(wait=True)
        yield snapshot


@pytest.fixture()
def restored_vm_with_data(admin_client, vm_for_snapshot_restore, snapshot_with_data_for_restore):
    """VM restored from snapshot and started, ready for data integrity checks."""
    with VirtualMachineRestore(
        name=f"restore-data-{vm_for_snapshot_restore.name}",
        namespace=vm_for_snapshot_restore.namespace,
        vm_name=vm_for_snapshot_restore.name,
        snapshot_name=snapshot_with_data_for_restore.name,
        client=admin_client,
    ) as restore:
        restore.wait_restore_done()
        running_vm(vm=vm_for_snapshot_restore)
        yield vm_for_snapshot_restore


@pytest.fixture()
def multiple_snapshots_for_restore(admin_client, vm_for_snapshot_restore):
    """Two offline snapshots with different data states for multi-snapshot testing.

    Returns list of two snapshots. VM is stopped after both snapshots are taken.
    """
    vm_snapshots = []

    write_file_via_ssh(vm=vm_for_snapshot_restore, filename="state1.txt", content="first-state")
    vm_for_snapshot_restore.stop(wait=True)
    with VirtualMachineSnapshot(
        name=f"snapshot-1-{vm_for_snapshot_restore.name}",
        namespace=vm_for_snapshot_restore.namespace,
        vm_name=vm_for_snapshot_restore.name,
        client=admin_client,
        teardown=False,
    ) as snapshot_1:
        snapshot_1.wait_snapshot_done()
        vm_snapshots.append(snapshot_1)

    running_vm(vm=vm_for_snapshot_restore)
    write_file_via_ssh(vm=vm_for_snapshot_restore, filename="state2.txt", content="second-state")
    vm_for_snapshot_restore.stop(wait=True)
    with VirtualMachineSnapshot(
        name=f"snapshot-2-{vm_for_snapshot_restore.name}",
        namespace=vm_for_snapshot_restore.namespace,
        vm_name=vm_for_snapshot_restore.name,
        client=admin_client,
        teardown=False,
    ) as snapshot_2:
        snapshot_2.wait_snapshot_done()
        vm_snapshots.append(snapshot_2)

    yield vm_snapshots

    for vm_snapshot in vm_snapshots:
        vm_snapshot.clean_up()
