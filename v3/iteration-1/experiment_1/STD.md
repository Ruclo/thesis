# Software Test Description (STD)

## Feature: Common-Instancetypes Deployment Configuration

**STP Reference:** [CNV-61256](https://issues.redhat.com/browse/CNV-61256)
**Jira ID:** CNV-61256
**Generated:** 2026-02-21

---

## Summary

Tests for the `commonInstancetypesDeployment` field in the HyperConverged CR, which allows users to enable or disable deployment of common instance types and preferences. Covers default behavior verification, disabling/enabling common-instancetypes, and setting persistence across HCO reconciliation.

---

## Test Files

### File: `tests/install_upgrade_operators/common_instancetypes_deployment/test_common_instancetypes_deployment.py`

```python
"""
Common-Instancetypes Deployment Configuration Tests

STP Reference: https://issues.redhat.com/browse/CNV-61256

This module contains tests for the commonInstancetypesDeployment field
in the HyperConverged CR, verifying that users can enable or disable
the deployment of common instance types and preferences.
"""

import pytest


class TestCommonInstancetypesDeployment:
    """
    Tests for commonInstancetypesDeployment HCO CR field.

    Markers:
        - iuo
        - gating

    Preconditions:
        - OpenShift Virtualization installed with HCO version supporting commonInstancetypesDeployment
        - HCO CR in default state (commonInstancetypesDeployment not explicitly set)
    """

    def test_common_instancetypes_deployed_by_default(self):
        """
        Test that common instance types are deployed by default when
        commonInstancetypesDeployment is not explicitly set.

        Steps:
            1. Query for VirtualMachineClusterInstancetype resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - Common VirtualMachineClusterInstancetype resources exist
        """
        pass

    def test_common_preferences_deployed_by_default(self):
        """
        Test that common VM preferences are deployed by default when
        commonInstancetypesDeployment is not explicitly set.

        Steps:
            1. Query for VirtualMachineClusterPreference resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - Common VirtualMachineClusterPreference resources exist
        """
        pass

    def test_disable_removes_common_instancetypes(self):
        """
        Test that setting commonInstancetypesDeployment to Disabled removes
        common instance type resources.

        Preconditions:
            - HCO CR patched with spec.commonInstancetypesDeployment set to "Disabled"
            - HCO reconciliation completed

        Steps:
            1. Query for VirtualMachineClusterInstancetype resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - No common VirtualMachineClusterInstancetype resources exist
        """
        pass

    def test_disable_removes_common_preferences(self):
        """
        Test that setting commonInstancetypesDeployment to Disabled removes
        common VM preference resources.

        Preconditions:
            - HCO CR patched with spec.commonInstancetypesDeployment set to "Disabled"
            - HCO reconciliation completed

        Steps:
            1. Query for VirtualMachineClusterPreference resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - No common VirtualMachineClusterPreference resources exist
        """
        pass

    def test_enable_deploys_common_instancetypes(self):
        """
        Test that setting commonInstancetypesDeployment to Enabled deploys
        common instance type resources after they were previously disabled.

        Preconditions:
            - HCO CR previously had spec.commonInstancetypesDeployment set to "Disabled"
            - HCO CR patched with spec.commonInstancetypesDeployment set to "Enabled"
            - HCO reconciliation completed

        Steps:
            1. Query for VirtualMachineClusterInstancetype resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - Common VirtualMachineClusterInstancetype resources exist
        """
        pass

    def test_enable_deploys_common_preferences(self):
        """
        Test that setting commonInstancetypesDeployment to Enabled deploys
        common VM preference resources after they were previously disabled.

        Preconditions:
            - HCO CR previously had spec.commonInstancetypesDeployment set to "Disabled"
            - HCO CR patched with spec.commonInstancetypesDeployment set to "Enabled"
            - HCO reconciliation completed

        Steps:
            1. Query for VirtualMachineClusterPreference resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - Common VirtualMachineClusterPreference resources exist
        """
        pass

    def test_disabled_setting_persists_after_reconciliation(self):
        """
        Test that the Disabled setting for commonInstancetypesDeployment persists
        after triggering an HCO reconciliation.

        Preconditions:
            - HCO CR patched with spec.commonInstancetypesDeployment set to "Disabled"
            - HCO reconciliation completed
            - HCO reconciliation triggered again by modifying an unrelated HCO field

        Steps:
            1. Query for VirtualMachineClusterInstancetype resources with vendor label
               "instancetype.kubevirt.io/vendor=redhat.com"

        Expected:
            - No common VirtualMachineClusterInstancetype resources exist
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --------- | ---------- | ---------- | -------- | ---- |
| `test_common_instancetypes_deployment.py` | `TestCommonInstancetypesDeployment` | 7 | P0/P1 | T1 |

---

## STP Scenario-to-Test Traceability

| STP Scenario | Test Method(s) | Priority |
| ------------ | -------------- | -------- |
| Scenario 3: Default Behavior | `test_common_instancetypes_deployed_by_default`, `test_common_preferences_deployed_by_default` | P0 |
| Scenario 1: Disable Common-Instancetypes | `test_disable_removes_common_instancetypes`, `test_disable_removes_common_preferences` | P0 |
| Scenario 2: Enable Common-Instancetypes | `test_enable_deploys_common_instancetypes`, `test_enable_deploys_common_preferences` | P0 |
| Scenario 4: Setting Persistence | `test_disabled_setting_persists_after_reconciliation` | P1 |

---

## Checklist

- [x] STP link in module docstring
- [x] All STP scenarios covered
- [x] Tests grouped in class with shared preconditions
- [x] Each test has: description, Preconditions (where needed), Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]` (none applicable)
- [x] Test methods contain only `pass`
- [x] Markers documented
- [x] Parametrization documented where needed (none required)
- [x] All files in single markdown output
- [x] Coverage summary table included
- [x] Output saved to `tests/std/common_instancetypes_deployment/std_cnv_61256.md`
