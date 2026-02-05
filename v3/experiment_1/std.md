# Software Test Description (STD)

## Feature: CommonInstancetypesDeployment Configuration

**STP Reference:** ../thesis/stps/1.md
**Jira ID:** CNV-61256 (Feature), CNV-59564 (Bug Fix)
**PR Reference:** [kubevirt/hyperconverged-cluster-operator#3471](https://github.com/kubevirt/hyperconverged-cluster-operator/pull/3471)
**Generated:** 2026-02-03

---

## Summary

This STD covers automated tests for the new `CommonInstancetypesDeployment` configuration field in the HyperConverged Cluster Operator (HCO). The feature enables users to disable the deployment of common-instancetypes via HCO configuration.

The tests verify:
- Default behavior (common-instancetypes enabled by default)
- Disabling common-instancetypes deployment
- Enabling common-instancetypes deployment
- Setting persistence across HCO reconciliations
- Upgrade scenarios with disabled setting

---

## Test Files

### File: `tests/virt/hco/test_common_instancetypes_deployment.py`

```python
"""
CommonInstancetypesDeployment Configuration Tests

STP Reference: ../thesis/stps/1.md
Jira: CNV-61256, CNV-59564
PR: https://github.com/kubevirt/hyperconverged-cluster-operator/pull/3471

This module contains tests for the CommonInstancetypesDeployment field in HCO,
which allows users to control whether common-instancetypes are deployed.
"""

import pytest


class TestCommonInstancetypesDeployment:
    """
    Tests for CommonInstancetypesDeployment field in HCO CR.

    Markers:
        - gating
        - tier1

    Preconditions:
        - OpenShift Virtualization 4.17+ installed
        - HyperConverged CR exists and is ready
        - Access to edit HCO CR
    """

    def test_default_behavior_enables_instancetypes(self):
        """
        Test that common-instancetypes are deployed by default.

        Steps:
            1. Get HCO CR without explicit commonInstancetypesDeployment setting
            2. Check for common-instancetype resources in cluster

        Expected:
            - Common-instancetype resources exist
        """
        pass

    def test_disable_common_instancetypes(self):
        """
        Test that setting commonInstancetypesDeployment to Disabled removes common-instancetypes.

        Steps:
            1. Verify common-instancetype resources exist (initial state)
            2. Edit HCO CR to set spec.commonInstancetypesDeployment: Disabled
            3. Wait for HCO reconciliation to complete
            4. Check for common-instancetype resources

        Expected:
            - Common-instancetype resources do NOT exist
        """
        pass

    def test_enable_common_instancetypes(self):
        """
        Test that setting commonInstancetypesDeployment to Enabled deploys common-instancetypes.

        Preconditions:
            - HCO CR has spec.commonInstancetypesDeployment: Disabled
            - Common-instancetype resources do not exist

        Steps:
            1. Edit HCO CR to set spec.commonInstancetypesDeployment: Enabled
            2. Wait for HCO reconciliation to complete
            3. Check for common-instancetype resources

        Expected:
            - Common-instancetype resources exist
        """
        pass

    def test_setting_persists_across_reconciliation(self):
        """
        Test that commonInstancetypesDeployment setting persists across HCO reconciliations.

        Preconditions:
            - HCO CR has spec.commonInstancetypesDeployment: Disabled
            - Common-instancetype resources do not exist

        Steps:
            1. Edit HCO CR to modify a different field (trigger reconciliation)
            2. Wait for HCO reconciliation to complete
            3. Verify commonInstancetypesDeployment field value
            4. Check for common-instancetype resources

        Expected:
            - commonInstancetypesDeployment equals Disabled
            - Common-instancetype resources do NOT exist
        """
        pass


class TestCommonInstancetypesDeploymentValidation:
    """
    Tests for field validation of CommonInstancetypesDeployment.

    Markers:
        - tier1

    Preconditions:
        - OpenShift Virtualization 4.17+ installed
        - HyperConverged CR exists and is ready
    """

    def test_accepts_enabled_value(self):
        """
        Test that commonInstancetypesDeployment accepts "Enabled" value.

        Steps:
            1. Edit HCO CR to set spec.commonInstancetypesDeployment: Enabled
            2. Verify HCO CR is updated successfully

        Expected:
            - HCO CR spec.commonInstancetypesDeployment equals Enabled
        """
        pass

    def test_accepts_disabled_value(self):
        """
        Test that commonInstancetypesDeployment accepts "Disabled" value.

        Steps:
            1. Edit HCO CR to set spec.commonInstancetypesDeployment: Disabled
            2. Verify HCO CR is updated successfully

        Expected:
            - HCO CR spec.commonInstancetypesDeployment equals Disabled
        """
        pass

    def test_rejects_invalid_value(self):
        """
        [NEGATIVE] Test that commonInstancetypesDeployment rejects invalid values.

        Steps:
            1. Attempt to edit HCO CR with spec.commonInstancetypesDeployment: InvalidValue
            2. Capture validation error

        Expected:
            - HCO CR update fails with validation error
        """
        pass


class TestCommonInstancetypesUpgrade:
    """
    Tests for CommonInstancetypesDeployment behavior during upgrades.

    Markers:
        - tier2
        - upgrade

    Preconditions:
        - OpenShift Virtualization installed (pre-upgrade version)
        - HyperConverged CR exists and is ready
    """

    def test_upgrade_preserves_disabled_setting(self):
        """
        Test that commonInstancetypesDeployment: Disabled persists through upgrade.

        Preconditions:
            - HCO CR has spec.commonInstancetypesDeployment: Disabled (before upgrade)
            - Common-instancetype resources do not exist (before upgrade)
            - CNV upgrade has completed successfully

        Steps:
            1. Verify commonInstancetypesDeployment field value after upgrade
            2. Check for common-instancetype resources after upgrade

        Expected:
            - commonInstancetypesDeployment equals Disabled
            - Common-instancetype resources do NOT exist
        """
        pass

    def test_upgrade_preserves_enabled_setting(self):
        """
        Test that commonInstancetypesDeployment: Enabled persists through upgrade.

        Preconditions:
            - HCO CR has spec.commonInstancetypesDeployment: Enabled (before upgrade)
            - Common-instancetype resources exist (before upgrade)
            - CNV upgrade has completed successfully

        Steps:
            1. Verify commonInstancetypesDeployment field value after upgrade
            2. Check for common-instancetype resources after upgrade

        Expected:
            - commonInstancetypesDeployment equals Enabled
            - Common-instancetype resources exist
        """
        pass

    def test_upgrade_without_field_maintains_default(self):
        """
        Test that upgrade without explicit commonInstancetypesDeployment maintains default behavior.

        Preconditions:
            - HCO CR does not have spec.commonInstancetypesDeployment set (before upgrade)
            - Common-instancetype resources exist (default behavior, before upgrade)
            - CNV upgrade has completed successfully

        Steps:
            1. Check for common-instancetype resources after upgrade

        Expected:
            - Common-instancetype resources exist
        """
        pass


class TestCommonInstancetypesSSPIntegration:
    """
    Tests for integration between HCO CommonInstancetypesDeployment and SSP operator.

    Markers:
        - tier2

    Preconditions:
        - OpenShift Virtualization 4.17+ installed
        - HyperConverged CR exists and is ready
        - SSP (Scheduling, Scale and Performance) operator is running
    """

    def test_ssp_reflects_disabled_state(self):
        """
        Test that SSP operator respects HCO commonInstancetypesDeployment: Disabled.

        Preconditions:
            - HCO CR has spec.commonInstancetypesDeployment: Disabled

        Steps:
            1. Get SSP CR configuration
            2. Check SSP status for common-instancetypes deployment state

        Expected:
            - SSP does not manage common-instancetype resources
        """
        pass

    def test_ssp_reflects_enabled_state(self):
        """
        Test that SSP operator respects HCO commonInstancetypesDeployment: Enabled.

        Preconditions:
            - HCO CR has spec.commonInstancetypesDeployment: Enabled

        Steps:
            1. Get SSP CR configuration
            2. Check SSP status for common-instancetypes deployment state

        Expected:
            - SSP manages common-instancetype resources
        """
        pass


class TestCommonInstancetypesHCOStatus:
    """
    Tests for HCO status conditions related to CommonInstancetypesDeployment.

    Markers:
        - tier2

    Preconditions:
        - OpenShift Virtualization 4.17+ installed
        - HyperConverged CR exists and is ready
    """

    def test_hco_status_reflects_disabled_state(self):
        """
        Test that HCO status conditions reflect commonInstancetypesDeployment: Disabled.

        Preconditions:
            - HCO CR has spec.commonInstancetypesDeployment: Disabled
            - HCO reconciliation has completed

        Steps:
            1. Get HCO CR status
            2. Check status conditions for common-instancetypes state

        Expected:
            - HCO status indicates common-instancetypes are disabled
        """
        pass

    def test_hco_status_reflects_enabled_state(self):
        """
        Test that HCO status conditions reflect commonInstancetypesDeployment: Enabled.

        Preconditions:
            - HCO CR has spec.commonInstancetypesDeployment: Enabled
            - HCO reconciliation has completed

        Steps:
            1. Get HCO CR status
            2. Check status conditions for common-instancetypes state

        Expected:
            - HCO status indicates common-instancetypes are enabled
        """
        pass
```

---

## Test Coverage Summary

| Test File                                 | Test Class                                    | Test Count | Priority | Tier       |
| ----------------------------------------- | --------------------------------------------- | ---------- | -------- | ---------- |
| `test_common_instancetypes_deployment.py` | `TestCommonInstancetypesDeployment`           | 4          | P0       | Tier 1     |
| `test_common_instancetypes_deployment.py` | `TestCommonInstancetypesDeploymentValidation` | 3          | P1       | Tier 1     |
| `test_common_instancetypes_deployment.py` | `TestCommonInstancetypesUpgrade`              | 3          | P2       | Tier 2     |
| `test_common_instancetypes_deployment.py` | `TestCommonInstancetypesSSPIntegration`       | 2          | P1       | Tier 2     |
| `test_common_instancetypes_deployment.py` | `TestCommonInstancetypesHCOStatus`            | 2          | P1       | Tier 2     |
| **TOTAL**                                 |                                               | **14**     |          | **T1: 7, T2: 7** |

---

## Test Scenario Mapping

| STP Scenario                      | Test Method                                          | Status |
| --------------------------------- | ---------------------------------------------------- | ------ |
| Scenario 1: Disable instancetypes | `test_disable_common_instancetypes`                  | ✓      |
| Scenario 2: Enable instancetypes  | `test_enable_common_instancetypes`                   | ✓      |
| Scenario 3: Default behavior      | `test_default_behavior_enables_instancetypes`        | ✓      |
| Scenario 4: Setting persistence   | `test_setting_persists_across_reconciliation`        | ✓      |
| Scenario 5: Upgrade with disabled | `test_upgrade_preserves_disabled_setting`            | ✓      |
| Field validation (Enabled)        | `test_accepts_enabled_value`                         | ✓      |
| Field validation (Disabled)       | `test_accepts_disabled_value`                        | ✓      |
| Field validation (Invalid)        | `test_rejects_invalid_value`                         | ✓      |
| SSP integration (disabled)        | `test_ssp_reflects_disabled_state`                   | ✓      |
| SSP integration (enabled)         | `test_ssp_reflects_enabled_state`                    | ✓      |
| HCO status (disabled)             | `test_hco_status_reflects_disabled_state`            | ✓      |
| HCO status (enabled)              | `test_hco_status_reflects_enabled_state`             | ✓      |
| Upgrade (enabled preserved)       | `test_upgrade_preserves_enabled_setting`             | ✓      |
| Upgrade (default maintained)      | `test_upgrade_without_field_maintains_default`       | ✓      |

---

## Checklist

- [x] All STP scenarios covered
- [x] Each test verifies ONE thing
- [x] Negative test marked with `[NEGATIVE]`
- [x] Markers documented (gating, tier1, tier2, upgrade)
- [x] Tests grouped in logical classes with shared preconditions
- [x] Module docstring includes STP reference
- [x] Each test has: description, Steps, Expected
- [x] Test methods contain only `pass`
- [x] Coverage summary table included
- [x] Output saved to `tests/std/common_instancetypes_deployment/std_cnv_61256.md`

---

## Implementation Notes

### Key Test Resources

The tests will need to verify the presence/absence of these resources:

- **HyperConverged CR**: `kubectl get hyperconverged -n openshift-cnv`
- **Common-instancetype resources**: `kubectl get virtualmachineinstancetypes` and `kubectl get virtualmachinepreferences`
- **SSP CR**: `kubectl get ssp -n openshift-cnv`

### Expected Common-Instancetype Resources

When enabled, the following resources should exist:
- VirtualMachineInstanceType resources (e.g., `cx1.medium`, `cx1.large`, etc.)
- VirtualMachinePreference resources (e.g., `rhel.9`, `fedora`, etc.)

### HCO Field Path

The new field is located at:
```yaml
apiVersion: hco.kubevirt.io/v1beta1
kind: HyperConverged
metadata:
  name: kubevirt-hyperconverged
  namespace: openshift-cnv
spec:
  commonInstancetypesDeployment: Enabled  # or Disabled
```

### Validation Strategy

Tests should use polling with timeout to wait for:
1. HCO reconciliation completion (check HCO status conditions)
2. Resource creation/deletion (common-instancetype resources)
3. SSP operator status updates

### Test Dependencies

These tests require:
- `pytest-kubernetes` utilities for CR manipulation
- HCO status condition checking utilities
- Resource existence verification helpers
- Timeouts for reconciliation waits (typically 2-5 minutes)
