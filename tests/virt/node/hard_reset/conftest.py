import logging
import shlex

import pytest
from pyhelper_utils.shell import run_ssh_commands
from timeout_sampler import TimeoutSampler

from utilities.constants import TIMEOUT_2MIN, TIMEOUT_10MIN
from utilities.virt import VirtualMachineForTests, fedora_vm_body, running_vm, wait_for_running_vm

LOGGER = logging.getLogger(__name__)


def get_vm_boot_count(vm: VirtualMachineForTests) -> int:
    """Returns the number of boots recorded by systemd journal.

    Args:
        vm: Virtual machine to query boot count from.

    Returns:
        Number of boots as reported by journalctl --list-boots.
    """
    boot_count_output = run_ssh_commands(
        host=vm.ssh_exec,
        commands=[shlex.split("journalctl --list-boots | wc -l")],
    )[0].strip()
    return int(boot_count_output)


def wait_for_boot_count_increment(
    vm: VirtualMachineForTests,
    boot_count_before: int,
) -> int:
    """Wait until the boot count increments beyond the given value.

    Args:
        vm: Virtual machine to query boot count from.
        boot_count_before: Boot count recorded before the reset.

    Returns:
        New boot count after increment is detected.
    """
    for sample in TimeoutSampler(
        wait_timeout=TIMEOUT_2MIN,
        sleep=5,
        func=get_vm_boot_count,
        vm=vm,
    ):
        if sample > boot_count_before:
            return sample
    return get_vm_boot_count(vm=vm)


@pytest.fixture(scope="class")
def hard_reset_vm(unprivileged_client, namespace):
    """Running Fedora VM for hard reset tests."""
    name = "fedora-vm-hard-reset"
    with VirtualMachineForTests(
        client=unprivileged_client,
        name=name,
        namespace=namespace.name,
        body=fedora_vm_body(name=name),
    ) as vm:
        running_vm(vm=vm)
        yield vm


@pytest.fixture(scope="class")
def boot_count_before_reset(hard_reset_vm):
    """Boot count recorded before VMI reset."""
    return get_vm_boot_count(vm=hard_reset_vm)


@pytest.fixture(scope="class")
def vmi_uid_before_reset(hard_reset_vm):
    """VMI UID recorded before reset."""
    return hard_reset_vm.vmi.instance.metadata.uid


@pytest.fixture(scope="class")
def pod_name_before_reset(hard_reset_vm):
    """Virt-launcher pod name recorded before reset."""
    return hard_reset_vm.privileged_vmi.virt_launcher_pod.name


@pytest.fixture(scope="class")
def hard_reset_vm_after_reset(hard_reset_vm, boot_count_before_reset, vmi_uid_before_reset, pod_name_before_reset):
    """Perform VMI reset and wait for VM to be running again.

    Depends on boot_count_before_reset, vmi_uid_before_reset, and pod_name_before_reset
    to ensure those values are captured before the reset is performed.
    """
    LOGGER.info(f"Performing hard reset on VMI {hard_reset_vm.vmi.name}")
    hard_reset_vm.vmi.reset()
    wait_for_running_vm(vm=hard_reset_vm, ssh_timeout=TIMEOUT_10MIN)


@pytest.fixture(scope="class")
def non_running_vm(unprivileged_client, namespace):
    """Fedora VM in stopped state (not started)."""
    name = "fedora-vm-stopped"
    with VirtualMachineForTests(
        client=unprivileged_client,
        name=name,
        namespace=namespace.name,
        body=fedora_vm_body(name=name),
    ) as vm:
        yield vm


@pytest.fixture(scope="class")
def paused_vm(unprivileged_client, namespace):
    """Running Fedora VM with paused VMI."""
    name = "fedora-vm-paused"
    with VirtualMachineForTests(
        client=unprivileged_client,
        name=name,
        namespace=namespace.name,
        body=fedora_vm_body(name=name),
    ) as vm:
        running_vm(vm=vm)
        LOGGER.info(f"Pausing VMI {vm.vmi.name}")
        vm.privileged_vmi.pause(wait=True)
        yield vm


@pytest.fixture(scope="class")
def virtctl_reset_vm(unprivileged_client, namespace):
    """Running Fedora VM for virtctl reset tests."""
    name = "fedora-vm-virtctl-reset"
    with VirtualMachineForTests(
        client=unprivileged_client,
        name=name,
        namespace=namespace.name,
        body=fedora_vm_body(name=name),
    ) as vm:
        running_vm(vm=vm)
        yield vm
