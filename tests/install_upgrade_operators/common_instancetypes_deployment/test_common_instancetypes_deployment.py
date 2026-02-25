"""
Common-Instancetypes Deployment Configuration Tests

STP Reference: https://issues.redhat.com/browse/CNV-61256

This module contains tests for the commonInstancetypesDeployment field
in the HyperConverged CR, verifying that users can enable or disable
the deployment of common instance types and preferences.
"""

import logging

import pytest

from tests.install_upgrade_operators.common_instancetypes_deployment.conftest import (
    get_common_cluster_instancetypes,
    get_common_cluster_preferences,
)

LOGGER = logging.getLogger(__name__)

pytestmark = [pytest.mark.iuo, pytest.mark.gating]


class TestCommonInstancetypesDeploymentDefault:
    """Tests for default commonInstancetypesDeployment behavior.

    Preconditions:
        - OpenShift Virtualization installed with HCO version supporting commonInstancetypesDeployment
        - HCO CR in default state (commonInstancetypesDeployment not explicitly set)
    """

    @pytest.mark.polarion("CNV-61256")
    def test_common_instancetypes_deployed_by_default(self, admin_client):
        """Test that common instance types are deployed by default when
        commonInstancetypesDeployment is not explicitly set.

        Steps:
            1. Query for VirtualMachineClusterInstancetype resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - Common VirtualMachineClusterInstancetype resources exist
        """
        LOGGER.info("Verifying common instancetypes are deployed by default")
        common_instancetypes = get_common_cluster_instancetypes(admin_client=admin_client)
        assert common_instancetypes, "Common VirtualMachineClusterInstancetype resources should exist by default"

    @pytest.mark.polarion("CNV-61256")
    def test_common_preferences_deployed_by_default(self, admin_client):
        """Test that common VM preferences are deployed by default when
        commonInstancetypesDeployment is not explicitly set.

        Steps:
            1. Query for VirtualMachineClusterPreference resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - Common VirtualMachineClusterPreference resources exist
        """
        LOGGER.info("Verifying common preferences are deployed by default")
        common_preferences = get_common_cluster_preferences(admin_client=admin_client)
        assert common_preferences, "Common VirtualMachineClusterPreference resources should exist by default"


class TestCommonInstancetypesDeploymentDisable:
    """Tests for disabling commonInstancetypesDeployment.

    Preconditions:
        - OpenShift Virtualization installed with HCO version supporting commonInstancetypesDeployment
        - HCO CR patched with spec.commonInstancetypesDeployment set to "Disabled"
        - HCO reconciliation completed
    """

    @pytest.mark.polarion("CNV-61256")
    @pytest.mark.usefixtures("disabled_common_instancetypes_deployment")
    def test_disable_removes_common_instancetypes(self, admin_client):
        """Test that setting commonInstancetypesDeployment to Disabled removes
        common instance type resources.

        Steps:
            1. Query for VirtualMachineClusterInstancetype resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - No common VirtualMachineClusterInstancetype resources exist
        """
        LOGGER.info("Verifying common instancetypes are removed after disabling")
        common_instancetypes = get_common_cluster_instancetypes(admin_client=admin_client)
        assert not common_instancetypes, (
            f"Common VirtualMachineClusterInstancetype resources should not exist when disabled, "
            f"found: {[instancetype.name for instancetype in common_instancetypes]}"
        )

    @pytest.mark.polarion("CNV-61256")
    @pytest.mark.usefixtures("disabled_common_instancetypes_deployment")
    def test_disable_removes_common_preferences(self, admin_client):
        """Test that setting commonInstancetypesDeployment to Disabled removes
        common VM preference resources.

        Steps:
            1. Query for VirtualMachineClusterPreference resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - No common VirtualMachineClusterPreference resources exist
        """
        LOGGER.info("Verifying common preferences are removed after disabling")
        common_preferences = get_common_cluster_preferences(admin_client=admin_client)
        assert not common_preferences, (
            f"Common VirtualMachineClusterPreference resources should not exist when disabled, "
            f"found: {[preference.name for preference in common_preferences]}"
        )


class TestCommonInstancetypesDeploymentEnable:
    """Tests for re-enabling commonInstancetypesDeployment after disabling.

    Preconditions:
        - OpenShift Virtualization installed with HCO version supporting commonInstancetypesDeployment
        - HCO CR previously had spec.commonInstancetypesDeployment set to "Disabled"
        - HCO CR patched with spec.commonInstancetypesDeployment set to "Enabled"
        - HCO reconciliation completed
    """

    @pytest.mark.polarion("CNV-61256")
    @pytest.mark.usefixtures("enabled_common_instancetypes_deployment_after_disable")
    def test_enable_deploys_common_instancetypes(self, admin_client):
        """Test that setting commonInstancetypesDeployment to Enabled deploys
        common instance type resources after they were previously disabled.

        Steps:
            1. Query for VirtualMachineClusterInstancetype resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - Common VirtualMachineClusterInstancetype resources exist
        """
        LOGGER.info("Verifying common instancetypes are deployed after re-enabling")
        common_instancetypes = get_common_cluster_instancetypes(admin_client=admin_client)
        assert common_instancetypes, (
            "Common VirtualMachineClusterInstancetype resources should exist after re-enabling"
        )

    @pytest.mark.polarion("CNV-61256")
    @pytest.mark.usefixtures("enabled_common_instancetypes_deployment_after_disable")
    def test_enable_deploys_common_preferences(self, admin_client):
        """Test that setting commonInstancetypesDeployment to Enabled deploys
        common VM preference resources after they were previously disabled.

        Steps:
            1. Query for VirtualMachineClusterPreference resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - Common VirtualMachineClusterPreference resources exist
        """
        LOGGER.info("Verifying common preferences are deployed after re-enabling")
        common_preferences = get_common_cluster_preferences(admin_client=admin_client)
        assert common_preferences, (
            "Common VirtualMachineClusterPreference resources should exist after re-enabling"
        )


class TestCommonInstancetypesDeploymentPersistence:
    """Tests for commonInstancetypesDeployment setting persistence.

    Preconditions:
        - OpenShift Virtualization installed with HCO version supporting commonInstancetypesDeployment
        - HCO CR patched with spec.commonInstancetypesDeployment set to "Disabled"
        - HCO reconciliation completed
        - Additional HCO reconciliation triggered
    """

    @pytest.mark.polarion("CNV-61256")
    @pytest.mark.usefixtures("disabled_common_instancetypes_with_reconciliation_trigger")
    def test_disabled_setting_persists_after_reconciliation(self, admin_client):
        """Test that the Disabled setting for commonInstancetypesDeployment persists
        after triggering an HCO reconciliation.

        Steps:
            1. Query for VirtualMachineClusterInstancetype resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - No common VirtualMachineClusterInstancetype resources exist
        """
        LOGGER.info("Verifying disabled setting persists after reconciliation")
        common_instancetypes = get_common_cluster_instancetypes(admin_client=admin_client)
        assert not common_instancetypes, (
            f"Common VirtualMachineClusterInstancetype resources should remain absent after reconciliation, "
            f"found: {[instancetype.name for instancetype in common_instancetypes]}"
        )
