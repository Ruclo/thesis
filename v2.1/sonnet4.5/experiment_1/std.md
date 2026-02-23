# Software Test Description (STD)

## Feature: CommonInstancetypesDeployment Configuration in HCO

**STP Reference:** /thesis/stps/1.md
**Jira ID:** CNV-61256
**Bug Fix:** CNV-59564
**Generated:** 2026-02-10

---

## Summary

This STD defines automated tests for the CommonInstancetypesDeployment configuration feature in the HyperConverged Cluster Operator (HCO). The feature allows users to control whether common instancetypes are deployed in their OpenShift Virtualization cluster through the HCO CR spec field `commonInstancetypesDeployment`.

The tests verify:
- Disabling common-instancetypes deployment
- Enabling common-instancetypes deployment
- Default behavior (enabled)
- Configuration persistence across HCO reconciliation
- Upgrade compatibility

---

## Test Files

### File: `tests/infrastructure/hco/test_common_instancetypes_deployment.py`

```python
"""
CommonInstancetypesDeployment Configuration Tests

STP Reference: /thesis/stps/1.md

This module contains tests for the CommonInstancetypesDeployment field in the
HyperConverged CR, which controls whether common VM instancetypes are deployed
in the cluster.

Related Jira:
- CNV-61256: Feature request
- CNV-59564: Bug fix implementation
"""

import pytest
from timeout_sampler import TimeoutSampler


class TestCommonInstancetypesDeployment:
    """
    Tests for CommonInstancetypesDeployment configuration in HCO CR.

    Markers:
        - tier1
        - gating

    Preconditions:
        - OpenShift Virtualization deployed with HCO
        - HCO version supports commonInstancetypesDeployment field
    """

    def test_default_instancetypes_enabled(self):
        """
        Test that common-instancetypes are deployed by default.

        Steps:
            1. Retrieve HCO CR spec
            2. Check commonInstancetypesDeployment field value (or absence)
            3. List VirtualMachineClusterInstancetype resources

        Expected:
            - commonInstancetypesDeployment is Enabled or unset (defaults to Enabled)
            - Common VirtualMachineClusterInstancetype resources exist
        """
        pass

    def test_disable_common_instancetypes(self):
        """
        Test that setting commonInstancetypesDeployment to Disabled removes instancetypes.

        Preconditions:
            - Common-instancetypes currently deployed (default state)

        Steps:
            1. Verify common-instancetype resources exist
            2. Edit HCO CR: set spec.commonInstancetypesDeployment to Disabled
            3. Wait for HCO reconciliation to complete
            4. List VirtualMachineClusterInstancetype resources

        Expected:
            - All common VirtualMachineClusterInstancetype resources are removed
        """
        pass

    def test_enable_common_instancetypes(self):
        """
        Test that setting commonInstancetypesDeployment to Enabled deploys instancetypes.

        Preconditions:
            - Common-instancetypes disabled via spec.commonInstancetypesDeployment: Disabled

        Steps:
            1. Verify common-instancetype resources do NOT exist
            2. Edit HCO CR: set spec.commonInstancetypesDeployment to Enabled
            3. Wait for HCO reconciliation to complete
            4. List VirtualMachineClusterInstancetype resources

        Expected:
            - Common VirtualMachineClusterInstancetype resources are deployed
        """
        pass

    def test_persistence_after_reconciliation(self):
        """
        Test that commonInstancetypesDeployment setting persists across HCO reconciliation.

        Preconditions:
            - spec.commonInstancetypesDeployment set to Disabled

        Steps:
            1. Set spec.commonInstancetypesDeployment to Disabled
            2. Verify common-instancetype resources removed
            3. Edit HCO CR to trigger reconciliation (modify unrelated field)
            4. Wait for reconciliation to complete
            5. Check commonInstancetypesDeployment field value
            6. Verify common-instancetype resources still absent

        Expected:
            - commonInstancetypesDeployment remains Disabled
            - Common VirtualMachineClusterInstancetype resources do NOT exist
        """
        pass

    def test_hco_status_reflects_configuration(self):
        """
        Test that HCO status conditions reflect commonInstancetypesDeployment state.

        Parametrize:
            - deployment_state: [Enabled, Disabled]

        Steps:
            1. Set spec.commonInstancetypesDeployment to deployment_state
            2. Wait for HCO reconciliation
            3. Check HCO status conditions

        Expected:
            - HCO status shows Available condition as True
            - No error conditions related to instancetypes deployment
        """
        pass


class TestCommonInstancetypesFieldValidation:
    """
    Tests for commonInstancetypesDeployment field validation.

    Markers:
        - tier1

    Preconditions:
        - OpenShift Virtualization deployed with HCO
    """

    def test_valid_enabled_value(self):
        """
        Test that setting commonInstancetypesDeployment to Enabled is accepted.

        Steps:
            1. Edit HCO CR: set spec.commonInstancetypesDeployment to Enabled
            2. Verify HCO CR update succeeds

        Expected:
            - HCO CR update succeeds without validation error
        """
        pass

    def test_valid_disabled_value(self):
        """
        Test that setting commonInstancetypesDeployment to Disabled is accepted.

        Steps:
            1. Edit HCO CR: set spec.commonInstancetypesDeployment to Disabled
            2. Verify HCO CR update succeeds

        Expected:
            - HCO CR update succeeds without validation error
        """
        pass

    def test_invalid_value_rejected(self):
        """
        [NEGATIVE] Test that invalid commonInstancetypesDeployment values are rejected.

        Parametrize:
            - invalid_value: [Invalid, true, false, 1, 0, enabled, disabled]

        Steps:
            1. Attempt to set spec.commonInstancetypesDeployment to invalid_value
            2. Check for validation error

        Expected:
            - HCO CR update fails with validation error
            - Error message indicates invalid value for commonInstancetypesDeployment
        """
        pass


class TestCommonInstancetypesUpgrade:
    """
    Tests for commonInstancetypesDeployment behavior during CNV upgrade.

    Markers:
        - tier2
        - upgrade

    Preconditions:
        - OpenShift Virtualization deployed
        - CNV version ready for upgrade
    """

    def test_disabled_setting_preserved_after_upgrade(self):
        """
        Test that commonInstancetypesDeployment: Disabled persists through CNV upgrade.

        Preconditions:
            - spec.commonInstancetypesDeployment set to Disabled
            - Common-instancetype resources removed
            - CNV upgrade available

        Steps:
            1. Verify commonInstancetypesDeployment is Disabled
            2. Verify common-instancetype resources do NOT exist
            3. Trigger CNV upgrade
            4. Wait for upgrade to complete
            5. Check HCO CR spec.commonInstancetypesDeployment value
            6. Verify common-instancetype resources still absent

        Expected:
            - commonInstancetypesDeployment remains Disabled after upgrade
            - Common VirtualMachineClusterInstancetype resources do NOT exist
        """
        pass

    def test_enabled_setting_preserved_after_upgrade(self):
        """
        Test that commonInstancetypesDeployment: Enabled persists through CNV upgrade.

        Preconditions:
            - spec.commonInstancetypesDeployment set to Enabled
            - Common-instancetype resources deployed
            - CNV upgrade available

        Steps:
            1. Verify commonInstancetypesDeployment is Enabled
            2. Verify common-instancetype resources exist
            3. Trigger CNV upgrade
            4. Wait for upgrade to complete
            5. Check HCO CR spec.commonInstancetypesDeployment value
            6. Verify common-instancetype resources still exist

        Expected:
            - commonInstancetypesDeployment remains Enabled after upgrade
            - Common VirtualMachineClusterInstancetype resources exist
        """
        pass


class TestCommonInstancetypesSSPIntegration:
    """
    Tests for SSP operator integration with commonInstancetypesDeployment.

    Markers:
        - tier2

    Preconditions:
        - OpenShift Virtualization deployed
        - SSP operator running
    """

    def test_ssp_reconciles_when_disabled(self):
        """
        Test that SSP operator handles commonInstancetypesDeployment: Disabled correctly.

        Steps:
            1. Set spec.commonInstancetypesDeployment to Disabled
            2. Wait for HCO reconciliation
            3. Check SSP CR status
            4. Verify no common-instancetype resources deployed by SSP

        Expected:
            - SSP CR shows Available condition as True
            - No VirtualMachineClusterInstancetype resources created by SSP
        """
        pass

    def test_ssp_deploys_when_enabled(self):
        """
        Test that SSP operator deploys instancetypes when commonInstancetypesDeployment is Enabled.

        Preconditions:
            - Common-instancetypes previously disabled

        Steps:
            1. Set spec.commonInstancetypesDeployment to Enabled
            2. Wait for HCO reconciliation
            3. Check SSP CR status
            4. List VirtualMachineClusterInstancetype resources

        Expected:
            - SSP CR shows Available condition as True
            - VirtualMachineClusterInstancetype resources exist
        """
        pass


class TestCommonInstancetypesVMCreation:
    """
    Tests for VM creation behavior with different commonInstancetypesDeployment states.

    Markers:
        - tier2

    Preconditions:
        - OpenShift Virtualization deployed
        - Namespace for testing VMs
    """

    def test_vm_creation_with_instancetype_when_enabled(self):
        """
        Test that VMs can use common instancetypes when deployment is Enabled.

        Preconditions:
            - spec.commonInstancetypesDeployment set to Enabled
            - Common-instancetype resources exist

        Steps:
            1. Create VM referencing a common instancetype (e.g., u1.medium)
            2. Wait for VM to become ready
            3. Verify VM spec reflects instancetype resources

        Expected:
            - VM is created successfully
            - VM CPU and memory match instancetype specification
        """
        pass

    def test_vm_creation_fails_with_missing_instancetype_when_disabled(self):
        """
        [NEGATIVE] Test that VM creation fails when referencing non-existent instancetype.

        Preconditions:
            - spec.commonInstancetypesDeployment set to Disabled
            - Common-instancetype resources removed

        Steps:
            1. Attempt to create VM referencing a common instancetype (e.g., u1.medium)
            2. Check for creation error

        Expected:
            - VM creation fails with error indicating instancetype not found
        """
        pass
```

---

### File: `tests/infrastructure/hco/conftest.py`

```python
"""
Shared fixtures for HCO tests.

This module provides fixtures for HCO CR manipulation and common-instancetypes testing.
"""

import pytest
from ocp_resources.hyperconverged import HyperConverged
from ocp_resources.virtual_machine_cluster_instancetype import VirtualMachineClusterInstancetype


@pytest.fixture(scope="class")
def hco_cr(admin_client):
    """
    HyperConverged CR instance for testing.

    Returns:
        HyperConverged: The HCO CR instance
    """
    pass


@pytest.fixture(scope="function")
def restore_hco_instancetypes_config(hco_cr):
    """
    Restore HCO commonInstancetypesDeployment configuration after test.

    This fixture captures the current commonInstancetypesDeployment value
    and restores it after the test completes.

    Yields:
        HyperConverged: The HCO CR instance
    """
    pass


@pytest.fixture(scope="function")
def common_instancetypes_disabled(hco_cr, restore_hco_instancetypes_config):
    """
    Common-instancetypes in disabled state.

    Sets spec.commonInstancetypesDeployment to Disabled and waits for
    reconciliation to complete.

    Preconditions:
        - HCO CR exists

    Yields:
        HyperConverged: HCO CR with instancetypes disabled
    """
    pass


@pytest.fixture(scope="function")
def common_instancetypes_enabled(hco_cr, restore_hco_instancetypes_config):
    """
    Common-instancetypes in enabled state.

    Sets spec.commonInstancetypesDeployment to Enabled and waits for
    reconciliation to complete.

    Preconditions:
        - HCO CR exists

    Yields:
        HyperConverged: HCO CR with instancetypes enabled
    """
    pass


@pytest.fixture(scope="function")
def common_instancetype_resources(admin_client):
    """
    List of common VirtualMachineClusterInstancetype resources.

    Returns:
        list[VirtualMachineClusterInstancetype]: Common instancetype resources
    """
    pass
```

---

## Test Coverage Summary

| Test File                                    | Test Class                                   | Test Count | Priority | Tier       |
| :------------------------------------------- | :------------------------------------------- | :--------- | :------- | :--------- |
| `test_common_instancetypes_deployment.py`    | `TestCommonInstancetypesDeployment`          | 5          | P0       | T1 (Gating)|
| `test_common_instancetypes_deployment.py`    | `TestCommonInstancetypesFieldValidation`     | 3          | P1       | T1         |
| `test_common_instancetypes_deployment.py`    | `TestCommonInstancetypesUpgrade`             | 2          | P2       | T2         |
| `test_common_instancetypes_deployment.py`    | `TestCommonInstancetypesSSPIntegration`      | 2          | P1       | T2         |
| `test_common_instancetypes_deployment.py`    | `TestCommonInstancetypesVMCreation`          | 2          | P1       | T2         |
| `conftest.py`                                | N/A (Fixtures)                               | 5 fixtures | N/A      | N/A        |

**Total Test Scenarios:** 14 tests + 5 fixtures

---

## Requirements Traceability

| Jira ID    | Requirement                      | Test Method(s)                                                    | Coverage |
| :--------- | :------------------------------- | :---------------------------------------------------------------- | :------- |
| CNV-61256  | Disable instancetypes            | `test_disable_common_instancetypes`                               | ✓        |
| CNV-61256  | Enable instancetypes             | `test_enable_common_instancetypes`                                | ✓        |
| CNV-61256  | Default behavior                 | `test_default_instancetypes_enabled`                              | ✓        |
| CNV-61256  | Persistence                      | `test_persistence_after_reconciliation`                           | ✓        |
| CNV-61256  | Field validation                 | `TestCommonInstancetypesFieldValidation` (3 tests)                | ✓        |
| CNV-61256  | Upgrade compatibility            | `TestCommonInstancetypesUpgrade` (2 tests)                        | ✓        |
| CNV-61256  | SSP integration                  | `TestCommonInstancetypesSSPIntegration` (2 tests)                 | ✓        |
| CNV-61256  | VM creation behavior             | `TestCommonInstancetypesVMCreation` (2 tests)                     | ✓        |

---

## Test Execution Strategy

### Tier 1 Tests (Gating)
Run in CI for every PR and merge:
- `TestCommonInstancetypesDeployment` - Core functionality
- `TestCommonInstancetypesFieldValidation` - API validation

### Tier 2 Tests
Run in extended CI and nightly builds:
- `TestCommonInstancetypesUpgrade` - Upgrade scenarios
- `TestCommonInstancetypesSSPIntegration` - SSP integration
- `TestCommonInstancetypesVMCreation` - E2E VM workflows

---

## Dependencies

| Component | Version | Notes |
| :-------- | :------ | :---- |
| OpenShift Virtualization | 4.17+ | Requires HCO with commonInstancetypesDeployment support |
| HyperConverged Operator | PR #3471+ | Feature implementation |
| SSP Operator | Latest | Manages instancetype deployment |
| OpenShift | 4.17+ | Platform requirement |

---

## Checklist

- [x] All STP scenarios covered (4 main scenarios + validations)
- [x] Each test verifies ONE thing
- [x] Negative tests marked with `[NEGATIVE]`
- [x] Markers documented (tier1, tier2, gating, upgrade)
- [x] Parametrization documented where needed
- [x] STP reference in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Fixtures for setup/teardown defined
- [x] Each test has: description, Preconditions, Steps, Expected
- [x] Test methods contain only `pass`
- [x] Coverage summary table included
- [x] Requirements traceability matrix included

---

## Implementation Notes

### Key Testing Patterns

1. **HCO CR Manipulation**: Tests modify `spec.commonInstancetypesDeployment` field
2. **Resource Verification**: Check for presence/absence of `VirtualMachineClusterInstancetype` resources
3. **Reconciliation Waiting**: Use `timeout_sampler` to wait for HCO reconciliation
4. **State Restoration**: Fixtures ensure HCO config is restored after tests

### Expected Resource Names

Common instancetypes deployed by SSP typically include:
- `u1.nano`, `u1.micro`, `u1.small`, `u1.medium`, `u1.large`, `u1.xlarge`, `u1.2xlarge`
- Similar patterns for other series (cx1, gn1, etc.)

### API Field Details

```yaml
apiVersion: hco.kubevirt.io/v1beta1
kind: HyperConverged
metadata:
  name: kubevirt-hyperconverged
spec:
  commonInstancetypesDeployment: Enabled  # or Disabled
```

Valid values:
- `Enabled` - Deploy common instancetypes (default)
- `Disabled` - Remove common instancetypes

---

**End of STD**
