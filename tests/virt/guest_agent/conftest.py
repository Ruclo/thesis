import logging

import pytest

from tests.virt.cluster.common_templates.utils import (
    get_matrix_os_golden_image_data_source,
    matrix_os_vm_from_template,
)
from tests.virt.utils import get_data_volume_template_dict_with_default_storage_class
from utilities.constants import TIMEOUT_2MIN
from utilities.virt import (
    run_os_command,
    running_vm,
    wait_for_user_agent_down,
)

LOGGER = logging.getLogger(__name__)

STOP_GUEST_AGENT_CMD = "powershell -command \"Stop-Service -Name 'QEMU-GA'\""
START_GUEST_AGENT_CMD = "powershell -command \"Start-Service -Name 'QEMU-GA'\""


@pytest.fixture(scope="class")
def windows_guest_agent_golden_image_data_source(admin_client, golden_images_namespace, windows_os_matrix__class__):
    yield from get_matrix_os_golden_image_data_source(
        admin_client=admin_client,
        golden_images_namespace=golden_images_namespace,
        os_matrix=windows_os_matrix__class__,
    )


@pytest.fixture(scope="class")
def windows_guest_agent_vm(
    unprivileged_client,
    namespace,
    windows_os_matrix__class__,
    windows_guest_agent_golden_image_data_source,
    modern_cpu_for_migration,
):
    windows_vm = matrix_os_vm_from_template(
        unprivileged_client=unprivileged_client,
        namespace=namespace,
        os_matrix=windows_os_matrix__class__,
        data_source_object=windows_guest_agent_golden_image_data_source,
        data_volume_template=get_data_volume_template_dict_with_default_storage_class(
            data_source=windows_guest_agent_golden_image_data_source
        ),
        cpu_model=modern_cpu_for_migration,
    )
    windows_vm.create(wait=True)
    running_vm(vm=windows_vm, check_ssh_connectivity=True)
    yield windows_vm
    windows_vm.clean_up()


@pytest.fixture()
def stopped_guest_agent_service(windows_guest_agent_vm):
    """Windows VM with qemu-guest-agent service stopped.

    Stops the QEMU-GA service inside the Windows guest and waits for the
    AgentConnected condition to go down before yielding. Restarts the
    service after the test completes.
    """
    LOGGER.info(f"Stopping QEMU guest agent service on {windows_guest_agent_vm.name}")
    run_os_command(vm=windows_guest_agent_vm, command=STOP_GUEST_AGENT_CMD)
    wait_for_user_agent_down(vm=windows_guest_agent_vm, timeout=TIMEOUT_2MIN)
    yield
    LOGGER.info(f"Ensuring QEMU guest agent is running on {windows_guest_agent_vm.name}")
    run_os_command(vm=windows_guest_agent_vm, command=START_GUEST_AGENT_CMD)
