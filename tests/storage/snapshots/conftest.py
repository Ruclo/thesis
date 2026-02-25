# -*- coding: utf-8 -*-

"""
Pytest conftest file for CNV Storage snapshots tests
"""

import logging
import shlex

import pytest
from ocp_resources.datavolume import DataVolume
from ocp_resources.resource import ResourceEditor
from ocp_resources.role_binding import RoleBinding
from ocp_resources.storage_class import StorageClass
from ocp_resources.storage_profile import StorageProfile
from ocp_resources.virtual_machine_snapshot import VirtualMachineSnapshot
from ocp_resources.volume_snapshot_class import VolumeSnapshotClass
from pyhelper_utils.shell import run_ssh_commands

from tests.storage.snapshots.constants import WINDOWS_DIRECTORY_PATH
from tests.storage.utils import (
    assert_windows_directory_existence,
    create_windows19_vm,
    create_windows_directory,
    set_permissions,
)
from utilities.constants import TIMEOUT_10MIN, UNPRIVILEGED_USER

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def permissions_for_dv(namespace, admin_client):
    """
    Sets DV permissions for an unprivileged client
    """
    with set_permissions(
        client=admin_client,
        role_name="datavolume-cluster-role",
        role_api_groups=[DataVolume.api_group],
        verbs=["*"],
        permissions_to_resources=["datavolumes", "datavolumes/source"],
        binding_name="role-bind-data-volume",
        namespace=namespace.name,
        subjects_kind="User",
        subjects_name=UNPRIVILEGED_USER,
        subjects_api_group=RoleBinding.api_group,
    ):
        yield


@pytest.fixture()
def windows_vm_for_snapshot(
    request,
    namespace,
    unprivileged_client,
    modern_cpu_for_migration,
    storage_class_matrix_snapshot_matrix__module__,
):
    with create_windows19_vm(
        dv_name=request.param["dv_name"],
        namespace=namespace.name,
        client=unprivileged_client,
        vm_name=request.param["vm_name"],
        cpu_model=modern_cpu_for_migration,
        storage_class=[*storage_class_matrix_snapshot_matrix__module__][0],
    ) as vm:
        yield vm


@pytest.fixture()
def snapshot_windows_directory(windows_vm_for_snapshot):
    create_windows_directory(windows_vm=windows_vm_for_snapshot, directory_path=WINDOWS_DIRECTORY_PATH)


@pytest.fixture()
def windows_snapshot(
    snapshot_windows_directory,
    windows_vm_for_snapshot,
):
    with VirtualMachineSnapshot(
        name="windows-snapshot",
        namespace=windows_vm_for_snapshot.namespace,
        vm_name=windows_vm_for_snapshot.name,
    ) as snapshot:
        yield snapshot


@pytest.fixture()
def snapshot_dirctory_removed(windows_vm_for_snapshot, windows_snapshot):
    windows_snapshot.wait_ready_to_use(timeout=TIMEOUT_10MIN)
    cmd = shlex.split(
        f'powershell -command "Remove-Item -Path {WINDOWS_DIRECTORY_PATH} -Recurse"',
    )
    run_ssh_commands(host=windows_vm_for_snapshot.ssh_exec, commands=cmd)
    assert_windows_directory_existence(
        expected_result=False,
        windows_vm=windows_vm_for_snapshot,
        directory_path=WINDOWS_DIRECTORY_PATH,
    )
    windows_vm_for_snapshot.stop(wait=True)


@pytest.fixture()
def file_created_during_snapshot(windows_vm_for_snapshot, windows_snapshot):
    file = f"{WINDOWS_DIRECTORY_PATH}\\file.txt"
    cmd = shlex.split(
        f'powershell -command "for($i=1; $i -le 100; $i++){{$i| Out-File -FilePath {file} -Append}}"',
    )
    run_ssh_commands(host=windows_vm_for_snapshot.ssh_exec, commands=cmd)
    windows_snapshot.wait_snapshot_done(timeout=TIMEOUT_10MIN)
    windows_vm_for_snapshot.stop(wait=True)


@pytest.fixture()
def storageprofile_with_snapshot_class(
    admin_client,
    snapshot_storage_class_name_scope_module,
):
    """StorageProfile patched with snapshotClass set to the matching VolumeSnapshotClass.

    Finds the VolumeSnapshotClass whose driver matches the StorageClass provisioner,
    then patches the StorageProfile spec.snapshotClass to that VolumeSnapshotClass name.
    Restores the original StorageProfile on teardown via ResourceEditor context manager.
    """
    storage_class_instance = StorageClass(
        client=admin_client,
        name=snapshot_storage_class_name_scope_module,
    ).instance
    provisioner = storage_class_instance.provisioner

    matching_vsc_name = None
    for volume_snapshot_class in VolumeSnapshotClass.get(client=admin_client):
        if volume_snapshot_class.instance.driver == provisioner:
            matching_vsc_name = volume_snapshot_class.name
            break

    if not matching_vsc_name:
        pytest.skip(
            f"No VolumeSnapshotClass found with driver matching provisioner '{provisioner}'"
        )

    storage_profile = StorageProfile(
        name=snapshot_storage_class_name_scope_module,
        client=admin_client,
    )
    LOGGER.info(
        f"Patching StorageProfile '{storage_profile.name}' with "
        f"snapshotClass='{matching_vsc_name}'"
    )
    with ResourceEditor(
        patches={storage_profile: {"spec": {"snapshotClass": matching_vsc_name}}}
    ):
        yield storage_profile
