import logging

import pytest
from kubernetes.dynamic import DynamicClient
from ocp_resources.resource import Resource
from ocp_resources.virtual_machine_cluster_instancetype import (
    VirtualMachineClusterInstancetype,
)
from ocp_resources.virtual_machine_cluster_preference import (
    VirtualMachineClusterPreference,
)
from timeout_sampler import TimeoutSampler

from utilities.constants import TIMEOUT_5MIN
from utilities.hco import ResourceEditorValidateHCOReconcile, wait_for_hco_conditions

LOGGER = logging.getLogger(__name__)

COMMON_INSTANCETYPE_VENDOR_LABEL = f"{Resource.ApiGroup.INSTANCETYPE_KUBEVIRT_IO}/vendor=redhat.com"
COMMON_INSTANCETYPES_DEPLOYMENT_KEY = "CommonInstancetypesDeployment"
COMMON_INSTANCETYPES_DEPLOYMENT_SPEC_ENABLED = {COMMON_INSTANCETYPES_DEPLOYMENT_KEY: {"enabled": True}}
COMMON_INSTANCETYPES_DEPLOYMENT_SPEC_DISABLED = {COMMON_INSTANCETYPES_DEPLOYMENT_KEY: {"enabled": False}}


def get_common_cluster_instancetypes(admin_client: DynamicClient) -> list[VirtualMachineClusterInstancetype]:
    """Get all common VirtualMachineClusterInstancetype resources with vendor label.

    Args:
        admin_client: Kubernetes dynamic client.

    Returns:
        List of VirtualMachineClusterInstancetype resources with Red Hat vendor label.
    """
    return list(
        VirtualMachineClusterInstancetype.get(
            client=admin_client,
            label_selector=COMMON_INSTANCETYPE_VENDOR_LABEL,
        )
    )


def get_common_cluster_preferences(admin_client: DynamicClient) -> list[VirtualMachineClusterPreference]:
    """Get all common VirtualMachineClusterPreference resources with vendor label.

    Args:
        admin_client: Kubernetes dynamic client.

    Returns:
        List of VirtualMachineClusterPreference resources with Red Hat vendor label.
    """
    return list(
        VirtualMachineClusterPreference.get(
            client=admin_client,
            label_selector=COMMON_INSTANCETYPE_VENDOR_LABEL,
        )
    )


def wait_for_common_instancetypes_absent(admin_client: DynamicClient, wait_timeout: int = TIMEOUT_5MIN) -> None:
    """Wait until no common VirtualMachineClusterInstancetype resources exist.

    Args:
        admin_client: Kubernetes dynamic client.
        wait_timeout: Maximum time to wait in seconds.
    """
    LOGGER.info("Waiting for common instancetypes to be removed")
    for sample in TimeoutSampler(
        wait_timeout=wait_timeout,
        sleep=5,
        func=get_common_cluster_instancetypes,
        admin_client=admin_client,
    ):
        if not sample:
            return


def wait_for_common_preferences_absent(admin_client: DynamicClient, wait_timeout: int = TIMEOUT_5MIN) -> None:
    """Wait until no common VirtualMachineClusterPreference resources exist.

    Args:
        admin_client: Kubernetes dynamic client.
        wait_timeout: Maximum time to wait in seconds.
    """
    LOGGER.info("Waiting for common preferences to be removed")
    for sample in TimeoutSampler(
        wait_timeout=wait_timeout,
        sleep=5,
        func=get_common_cluster_preferences,
        admin_client=admin_client,
    ):
        if not sample:
            return


def wait_for_common_instancetypes_present(admin_client: DynamicClient, wait_timeout: int = TIMEOUT_5MIN) -> None:
    """Wait until common VirtualMachineClusterInstancetype resources exist.

    Args:
        admin_client: Kubernetes dynamic client.
        wait_timeout: Maximum time to wait in seconds.
    """
    LOGGER.info("Waiting for common instancetypes to be deployed")
    for sample in TimeoutSampler(
        wait_timeout=wait_timeout,
        sleep=5,
        func=get_common_cluster_instancetypes,
        admin_client=admin_client,
    ):
        if sample:
            return


def wait_for_common_preferences_present(admin_client: DynamicClient, wait_timeout: int = TIMEOUT_5MIN) -> None:
    """Wait until common VirtualMachineClusterPreference resources exist.

    Args:
        admin_client: Kubernetes dynamic client.
        wait_timeout: Maximum time to wait in seconds.
    """
    LOGGER.info("Waiting for common preferences to be deployed")
    for sample in TimeoutSampler(
        wait_timeout=wait_timeout,
        sleep=5,
        func=get_common_cluster_preferences,
        admin_client=admin_client,
    ):
        if sample:
            return


@pytest.fixture()
def disabled_common_instancetypes_deployment(
    admin_client,
    hco_namespace,
    hyperconverged_resource_scope_function,
):
    """HCO CR with commonInstancetypesDeployment set to Disabled.

    Patches the HCO CR to disable common-instancetypes deployment and waits
    for reconciliation. On teardown, restores the original value and waits
    for common resources to be redeployed.
    """
    with ResourceEditorValidateHCOReconcile(
        patches={
            hyperconverged_resource_scope_function: {
                "spec": COMMON_INSTANCETYPES_DEPLOYMENT_SPEC_DISABLED
            }
        },
        list_resource_reconcile=[],
        wait_for_reconcile_post_update=True,
    ):
        wait_for_common_instancetypes_absent(admin_client=admin_client)
        wait_for_common_preferences_absent(admin_client=admin_client)
        LOGGER.info("Common instancetypes deployment disabled successfully")
        yield
    wait_for_common_instancetypes_present(admin_client=admin_client)
    wait_for_common_preferences_present(admin_client=admin_client)
    LOGGER.info("Common instancetypes deployment re-enabled after teardown")


@pytest.fixture()
def enabled_common_instancetypes_deployment_after_disable(
    admin_client,
    hco_namespace,
    hyperconverged_resource_scope_function,
    disabled_common_instancetypes_deployment,
):
    """HCO CR with commonInstancetypesDeployment set to Enabled after being Disabled.

    Requires disabled_common_instancetypes_deployment to run first to put
    the system in a disabled state, then patches to Enabled and waits for
    common resources to be redeployed.
    """
    with ResourceEditorValidateHCOReconcile(
        patches={
            hyperconverged_resource_scope_function: {
                "spec": COMMON_INSTANCETYPES_DEPLOYMENT_SPEC_ENABLED
            }
        },
        action="replace",
        list_resource_reconcile=[],
        wait_for_reconcile_post_update=True,
    ):
        wait_for_common_instancetypes_present(admin_client=admin_client)
        wait_for_common_preferences_present(admin_client=admin_client)
        LOGGER.info("Common instancetypes deployment re-enabled successfully")
        yield


@pytest.fixture()
def disabled_common_instancetypes_with_reconciliation_trigger(
    admin_client,
    hco_namespace,
    hyperconverged_resource_scope_function,
    disabled_common_instancetypes_deployment,
):
    """HCO CR with disabled commonInstancetypesDeployment that has been reconciled.

    After disabling common-instancetypes deployment, triggers an additional
    HCO reconciliation by forcing a conditions check, confirming the disabled
    setting persists.
    """
    LOGGER.info("Triggering additional HCO reconciliation to verify persistence")
    wait_for_hco_conditions(
        admin_client=admin_client,
        hco_namespace=hco_namespace,
    )
    yield
