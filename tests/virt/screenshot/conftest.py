import logging

import pytest
from ocp_resources.virtual_machine import VirtualMachine
from ocp_resources.virtual_machine_cluster_instancetype import (
    VirtualMachineClusterInstancetype,
)
from ocp_resources.virtual_machine_cluster_preference import (
    VirtualMachineClusterPreference,
)

from utilities.constants import (
    OS_FLAVOR_RHEL,
    RHEL10_PREFERENCE,
    U1_SMALL,
    Images,
)
from utilities.virt import VirtualMachineForTests, fedora_vm_body, wait_for_running_vm

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def screenshot_fedora_vm(unprivileged_client, namespace):
    """Running Fedora VM using container disk for screenshot tests."""
    name = "fedora-vm-screenshot"
    with VirtualMachineForTests(
        name=name,
        namespace=namespace.name,
        client=unprivileged_client,
        body=fedora_vm_body(name=name),
        run_strategy=VirtualMachine.RunStrategy.ALWAYS,
    ) as vm:
        wait_for_running_vm(vm=vm, check_ssh_connectivity=False)
        yield vm


@pytest.fixture(scope="class")
def screenshot_rhel_vm(unprivileged_client, namespace):
    """Running RHEL VM using instance type and preference for screenshot tests."""
    with VirtualMachineForTests(
        name="rhel-vm-screenshot",
        image=Images.Rhel.RHEL10_REGISTRY_GUEST_IMG,
        namespace=namespace.name,
        client=unprivileged_client,
        vm_instance_type=VirtualMachineClusterInstancetype(
            name=U1_SMALL,
            client=unprivileged_client,
        ),
        vm_preference=VirtualMachineClusterPreference(
            name=RHEL10_PREFERENCE,
            client=unprivileged_client,
        ),
        os_flavor=OS_FLAVOR_RHEL,
        run_strategy=VirtualMachine.RunStrategy.ALWAYS,
    ) as vm:
        wait_for_running_vm(vm=vm, check_ssh_connectivity=False)
        yield vm
