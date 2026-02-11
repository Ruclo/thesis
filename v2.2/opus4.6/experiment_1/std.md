# Software Test Description (STD)

## Feature: Common-Instancetypes Deployment Configuration

**STP Reference:** [CNV-61256](https://issues.redhat.com/browse/CNV-61256)
**Jira ID:** CNV-61256
**Bug Fix Tracking:** [CNV-59564](https://issues.redhat.com/browse/CNV-59564)

---

## Summary

This STD covers tests for the `commonInstancetypesDeployment` field in the HyperConverged (HCO) CR spec. The feature allows users to enable or disable the deployment of common instance types via HCO configuration. Tests verify that disabling removes common-instancetype resources, enabling deploys them, the default behavior is enabled, and the setting persists across HCO reconciliation cycles.

---

## Test Files

### File: `tests/install_upgrade_operators/common_instancetypes_deployment/test_common_instancetypes_deployment.py`

```python
"""
Common-Instancetypes Deployment Configuration Tests

STP Reference: https://issues.redhat.com/browse/CNV-61256

This module contains tests for the commonInstancetypesDeployment field
in the HCO CR spec. Verifies that common instance type resources can be
enabled or disabled through HCO configuration and that the setting
persists across reconciliation cycles.
"""

import pytest


pytestmark = [pytest.mark.iuo, pytest.mark.arm64, pytest.mark.s390x]


class TestCommonInstancetypesDeployment:
    """
    Tests for commonInstancetypesDeployment HCO CR configuration.

    Preconditions:
        - OpenShift cluster with OpenShift Virtualization installed
        - HCO CR accessible and reconciling
    """

    @pytest.mark.polarion("CNV-61256")
    def test_common_instancetypes_deployed_by_default(self):
        """
        Test that common instance types are deployed by default
        when commonInstancetypesDeployment is not explicitly set.

        Steps:
            1. Verify the HCO CR does not have commonInstancetypesDeployment
               explicitly set, or that its value is "Enabled"
            2. List common instance type resources in the cluster

        Expected:
            - Common instance type resources exist in the cluster
        """
        pass

    @pytest.mark.polarion("CNV-61256")
    def test_disable_common_instancetypes_deployment(self):
        """
        Test that setting commonInstancetypesDeployment to Disabled
        removes common instance type resources.

        Preconditions:
            - Common instance type resources are deployed (default state)

        Steps:
            1. Set commonInstancetypesDeployment to "Disabled" in HCO CR
            2. Wait for HCO reconciliation to complete
            3. List common instance type resources in the cluster

        Expected:
            - Common instance type resources do NOT exist in the cluster
        """
        pass

    @pytest.mark.polarion("CNV-61256")
    def test_enable_common_instancetypes_deployment(self):
        """
        Test that setting commonInstancetypesDeployment to Enabled
        deploys common instance type resources.

        Preconditions:
            - commonInstancetypesDeployment is set to "Disabled"
            - Common instance type resources are not deployed

        Steps:
            1. Set commonInstancetypesDeployment to "Enabled" in HCO CR
            2. Wait for HCO reconciliation to complete
            3. List common instance type resources in the cluster

        Expected:
            - Common instance type resources exist in the cluster
        """
        pass

    @pytest.mark.polarion("CNV-61256")
    def test_disabled_setting_persists_after_reconciliation(self):
        """
        Test that the Disabled setting for commonInstancetypesDeployment
        persists after an HCO reconciliation cycle.

        Preconditions:
            - commonInstancetypesDeployment is set to "Disabled"

        Steps:
            1. Trigger HCO reconciliation by modifying an unrelated HCO CR field
            2. Wait for reconciliation to complete
            3. Read commonInstancetypesDeployment value from HCO CR
            4. List common instance type resources in the cluster

        Expected:
            - commonInstancetypesDeployment equals "Disabled"
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --------- | ---------- | ---------- | -------- | ---- |
| `test_common_instancetypes_deployment.py` | `TestCommonInstancetypesDeployment` | 4 | P0-P1 | Tier 1 |

---

## Requirements-to-Tests Traceability

| Requirement | Test Method | Priority |
| ----------- | ----------- | -------- |
| Default behavior is Enabled | `test_common_instancetypes_deployed_by_default` | P0 |
| Disable instancetypes | `test_disable_common_instancetypes_deployment` | P0 |
| Enable instancetypes | `test_enable_common_instancetypes_deployment` | P0 |
| Setting persists after reconcile | `test_disabled_setting_persists_after_reconciliation` | P1 |

---

## Out of Scope (per STP)

| Scenario | Reason |
| -------- | ------ |
| Upgrade with disabled setting (Scenario 5) | Tier 2 / E2E - separate upgrade test suite |
| Custom instancetype functionality | Separate feature |
| Instancetype performance | Not relevant |

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in class with shared preconditions
- [x] Each test has: description, Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] No negative tests needed (all are positive verification)
- [x] Test methods contain only `pass`
- [x] Appropriate pytest markers documented
- [x] Coverage summary table included
- [x] All STP Tier 1 scenarios covered
- [x] Output saved to `tests/std/common_instancetypes_deployment/std_cnv_61256.md`
