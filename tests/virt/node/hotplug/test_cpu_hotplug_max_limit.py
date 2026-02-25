"""
CPU Hotplug Maximum Limit Tests

STP Reference: https://issues.redhat.com/browse/CNV-61263

This module contains tests verifying that CPU hotplug correctly enforces
MaxSockets limits based on maximum allowed vCPUs, preventing VMs from
exceeding their CPU allocation via hotplug operations.

The fix (kubevirt/kubevirt#14511) ensures that when MaxSockets is not
explicitly set, the calculated default is capped so that
MaxSockets * cores * threads <= 512 (maximum vCPUs per machine type).
"""

import logging

import pytest
from kubernetes.dynamic.exceptions import UnprocessibleEntityError
from ocp_resources.template import Template

from tests.os_params import RHEL_LATEST, RHEL_LATEST_LABELS
from tests.utils import (
    clean_up_migration_jobs,
    hotplug_spec_vm,
    hotplug_spec_vm_and_verify_hotplug,
    wait_for_guest_os_cpu_count,
)
from utilities.constants import (
    FOUR_CPU_SOCKETS,
    ONE_CPU_CORE,
    ONE_CPU_THREAD,
    SIX_CPU_SOCKETS,
    TWO_CPU_SOCKETS,
    VM_MEMORY_GUEST,
)
from utilities.virt import VirtualMachineForTestsFromTemplate, running_vm

LOGGER = logging.getLogger(__name__)

pytestmark = pytest.mark.rwx_default_storage

MAX_VCPUS = 512


@pytest.fixture(autouse=True)
def migration_jobs_cleanup(request, admin_client):
    """Clean up migration jobs created by hotplug operations after each test."""
    yield
    vm_fixture_name = "max_limit_vm" if "max_limit_vm" in request.fixturenames else "full_cycle_vm"
    if vm_fixture_name in request.fixturenames:
        clean_up_migration_jobs(client=admin_client, vm=request.getfixturevalue(vm_fixture_name))


@pytest.fixture(scope="class")
def max_limit_vm(
    request,
    namespace,
    unprivileged_client,
    golden_image_data_volume_template_for_test_scope_class,
    modern_cpu_for_migration,
    vmx_disabled_flag,
):
    """VM with explicit maxSockets for testing limit enforcement.

    Creates a VM with cpu_max_sockets=FOUR_CPU_SOCKETS and initial
    cpu_sockets=TWO_CPU_SOCKETS to test that hotplug operations
    respect the configured maximum.
    """
    with VirtualMachineForTestsFromTemplate(
        name=request.param["vm_name"],
        labels=Template.generate_template_labels(**request.param["template_labels"]),
        namespace=namespace.name,
        client=unprivileged_client,
        data_volume_template=golden_image_data_volume_template_for_test_scope_class,
        cpu_max_sockets=FOUR_CPU_SOCKETS,
        cpu_sockets=TWO_CPU_SOCKETS,
        cpu_threads=ONE_CPU_THREAD,
        cpu_cores=ONE_CPU_CORE,
        memory_guest=VM_MEMORY_GUEST,
        cpu_model=modern_cpu_for_migration,
        cpu_flags=vmx_disabled_flag,
    ) as vm:
        running_vm(vm=vm)
        yield vm


@pytest.fixture(scope="class")
def full_cycle_vm(
    request,
    namespace,
    unprivileged_client,
    golden_image_data_volume_template_for_test_scope_class,
    modern_cpu_for_migration,
    vmx_disabled_flag,
):
    """VM for full hotplug cycle testing with low initial sockets.

    Creates a VM with cpu_max_sockets=FOUR_CPU_SOCKETS and initial
    cpu_sockets=TWO_CPU_SOCKETS to test the full hotplug range.
    """
    with VirtualMachineForTestsFromTemplate(
        name=request.param["vm_name"],
        labels=Template.generate_template_labels(**request.param["template_labels"]),
        namespace=namespace.name,
        client=unprivileged_client,
        data_volume_template=golden_image_data_volume_template_for_test_scope_class,
        cpu_max_sockets=FOUR_CPU_SOCKETS,
        cpu_sockets=TWO_CPU_SOCKETS,
        cpu_threads=ONE_CPU_THREAD,
        cpu_cores=ONE_CPU_CORE,
        memory_guest=VM_MEMORY_GUEST,
        cpu_model=modern_cpu_for_migration,
        cpu_flags=vmx_disabled_flag,
    ) as vm:
        running_vm(vm=vm)
        yield vm


@pytest.mark.parametrize(
    "golden_image_data_source_for_test_scope_class, max_limit_vm",
    [
        pytest.param(
            {"os_dict": RHEL_LATEST},
            {"template_labels": RHEL_LATEST_LABELS, "vm_name": "rhel-cpu-hotplug-max-limit-vm"},
            id="RHEL-VM",
            marks=pytest.mark.s390x,
        ),
    ],
    indirect=True,
)
class TestCPUHotplugMaxSocketsLimit:
    """Tests for CPU hotplug MaxSockets limit enforcement.

    Verifies that MaxSockets is properly limited and that hotplug operations
    cannot exceed the configured maximum CPU sockets.
    """

    @pytest.mark.polarion("CNV-61263")
    def test_max_sockets_limited_by_max_vcpus(self, max_limit_vm):
        """Test that MaxSockets is calculated to not exceed the maximum allowed vCPUs.

        Steps:
            1. Inspect the VM spec for the calculated MaxSockets value

        Expected:
            - MaxSockets is less than or equal to the maximum allowed vCPUs
        """
        vmi_cpu = max_limit_vm.vmi.instance.spec.domain.cpu
        max_sockets = vmi_cpu.maxSockets
        cores = vmi_cpu.cores
        threads = vmi_cpu.threads
        total_vcpus = max_sockets * cores * threads

        LOGGER.info(
            f"VM {max_limit_vm.name}: maxSockets={max_sockets}, cores={cores}, "
            f"threads={threads}, total_vcpus={total_vcpus}"
        )
        assert total_vcpus <= MAX_VCPUS, (
            f"Total vCPUs ({total_vcpus}) exceeds maximum ({MAX_VCPUS}). "
            f"maxSockets={max_sockets}, cores={cores}, threads={threads}"
        )

    @pytest.mark.polarion("CNV-61263")
    def test_hotplug_cpu_up_to_max_sockets(self, max_limit_vm, unprivileged_client):
        """Test that CPU hotplug succeeds when increasing sockets up to the MaxSockets limit.

        Steps:
            1. Hotplug CPU sockets to the MaxSockets limit value

        Expected:
            - Guest OS CPU count equals the MaxSockets limit
        """
        hotplug_spec_vm_and_verify_hotplug(
            vm=max_limit_vm,
            client=unprivileged_client,
            sockets=FOUR_CPU_SOCKETS,
        )
        wait_for_guest_os_cpu_count(vm=max_limit_vm, spec_cpu_amount=FOUR_CPU_SOCKETS)

    @pytest.mark.polarion("CNV-61263")
    def test_hotplug_cpu_beyond_max_sockets_rejected(self, max_limit_vm):
        """[NEGATIVE] Test that CPU hotplug is rejected when attempting to exceed MaxSockets.

        Steps:
            1. Attempt to hotplug CPU sockets to a value exceeding MaxSockets

        Expected:
            - Operation is rejected with an error indicating the CPU limit has been exceeded
        """
        with pytest.raises(UnprocessibleEntityError):
            hotplug_spec_vm(vm=max_limit_vm, sockets=SIX_CPU_SOCKETS)

    @pytest.mark.polarion("CNV-61263")
    def test_error_message_when_exceeding_cpu_limit(self, max_limit_vm):
        """[NEGATIVE] Test that a clear error message is returned when attempting to exceed the CPU limit.

        Steps:
            1. Attempt to set CPU sockets above the MaxSockets limit via VM spec patch

        Expected:
            - Error message contains reference to the maximum CPU or socket limit
        """
        with pytest.raises(UnprocessibleEntityError, match=r"(maxSockets|maximum|number of sockets|exceeds)"):
            hotplug_spec_vm(vm=max_limit_vm, sockets=SIX_CPU_SOCKETS)


@pytest.mark.parametrize(
    "golden_image_data_source_for_test_scope_class, full_cycle_vm",
    [
        pytest.param(
            {"os_dict": RHEL_LATEST},
            {"template_labels": RHEL_LATEST_LABELS, "vm_name": "rhel-cpu-hotplug-full-cycle-vm"},
            id="RHEL-VM",
            marks=pytest.mark.s390x,
        ),
    ],
    indirect=True,
)
@pytest.mark.tier2
class TestCPUHotplugFullCycleWithinLimits:
    """Tests for end-to-end CPU hotplug operations within enforced limits.

    Verifies that the full hotplug cycle from initial sockets to maximum
    operates correctly, and that further hotplug is blocked at the limit.
    """

    @pytest.mark.polarion("CNV-61263")
    def test_hotplug_from_initial_to_max_within_limits(self, full_cycle_vm, unprivileged_client):
        """Test that CPUs can be hotplugged from initial count to maximum allowed within limits.

        Steps:
            1. Hotplug CPU sockets from initial count to the MaxSockets limit
            2. Verify guest OS sees all hotplugged CPUs

        Expected:
            - Guest OS CPU count equals the MaxSockets limit
        """
        hotplug_spec_vm_and_verify_hotplug(
            vm=full_cycle_vm,
            client=unprivileged_client,
            sockets=FOUR_CPU_SOCKETS,
        )
        wait_for_guest_os_cpu_count(vm=full_cycle_vm, spec_cpu_amount=FOUR_CPU_SOCKETS)

    @pytest.mark.polarion("CNV-61263")
    def test_no_further_hotplug_after_reaching_max(self, full_cycle_vm):
        """[NEGATIVE] Test that no additional CPUs can be hotplugged after reaching the maximum limit.

        Preconditions:
            - VM CPU sockets already hotplugged to MaxSockets limit

        Steps:
            1. Attempt to hotplug one additional CPU socket beyond MaxSockets

        Expected:
            - Operation is rejected and CPU count remains at MaxSockets limit
        """
        with pytest.raises(UnprocessibleEntityError):
            hotplug_spec_vm(vm=full_cycle_vm, sockets=SIX_CPU_SOCKETS)
