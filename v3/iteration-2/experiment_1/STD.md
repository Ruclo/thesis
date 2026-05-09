# Software Test Description (STD)

## Feature: Disable Common-Instancetypes Deployment from HCO

**STP Reference:** [stps/1.md](/home/fedora/thesis/stps/1.md)
**Jira ID:** [CNV-61256](https://issues.redhat.com/browse/CNV-61256)
**Bug Fix:** [CNV-59564](https://issues.redhat.com/browse/CNV-59564)
**Generated:** 2026-02-23

---

## Summary

Tests for the `CommonInstancetypesDeployment` field in the HyperConverged (HCO) CR spec, which allows users to enable or disable the deployment of common VM instance types. The field uses a nested object structure with an `enabled` boolean property (`{"CommonInstancetypesDeployment": {"enabled": true/false}}`). Tests cover disabling, enabling, default behavior, and persistence across HCO reconciliation.

---

## Test Files

### File: `tests/install_upgrade_operators/common_instancetypes_deployment/test_common_instancetypes_deployment.py`

```python
"""
Common-Instancetypes Deployment Configuration Tests

STP Reference: https://issues.redhat.com/browse/CNV-61256

This module contains tests for the CommonInstancetypesDeployment field in the
HyperConverged CR spec, verifying that users can enable or disable the deployment
of common VM instance types.
"""

import pytest


class TestCommonInstancetypesDeploymentDisabled:
    """
    Tests for disabling common-instancetypes deployment via HCO CR.

    Preconditions:
        - HCO CR patched with CommonInstancetypesDeployment.enabled set to false
        - HCO reconciliation completed after patching
    """

    def test_common_cluster_instancetypes_absent_when_disabled(self):
        """
        Test that VirtualMachineClusterInstancetype resources are removed when
        CommonInstancetypesDeployment is disabled.

        Steps:
            1. List all VirtualMachineClusterInstancetype resources in the cluster

        Expected:
            - No VirtualMachineClusterInstancetype resources exist
        """
        pass

    def test_common_cluster_preferences_absent_when_disabled(self):
        """
        Test that VirtualMachineClusterPreference resources are removed when
        CommonInstancetypesDeployment is disabled.

        Steps:
            1. List all VirtualMachineClusterPreference resources in the cluster

        Expected:
            - No VirtualMachineClusterPreference resources exist
        """
        pass


class TestCommonInstancetypesDeploymentEnabled:
    """
    Tests for enabling common-instancetypes deployment via HCO CR.

    Preconditions:
        - HCO CR previously had CommonInstancetypesDeployment.enabled set to false
        - HCO CR patched with CommonInstancetypesDeployment.enabled set to true
        - HCO reconciliation completed after patching
    """

    def test_common_cluster_instancetypes_present_when_enabled(self):
        """
        Test that VirtualMachineClusterInstancetype resources are deployed when
        CommonInstancetypesDeployment is enabled.

        Steps:
            1. List all VirtualMachineClusterInstancetype resources in the cluster

        Expected:
            - VirtualMachineClusterInstancetype resources exist
        """
        pass

    def test_common_cluster_preferences_present_when_enabled(self):
        """
        Test that VirtualMachineClusterPreference resources are deployed when
        CommonInstancetypesDeployment is enabled.

        Steps:
            1. List all VirtualMachineClusterPreference resources in the cluster

        Expected:
            - VirtualMachineClusterPreference resources exist
        """
        pass


class TestCommonInstancetypesDeploymentDefault:
    """
    Tests for default CommonInstancetypesDeployment behavior.

    Preconditions:
        - Fresh CNV installation with no explicit CommonInstancetypesDeployment setting
    """

    def test_common_instancetypes_deployed_by_default(self):
        """
        Test that common-instancetypes are deployed by default when
        CommonInstancetypesDeployment is not explicitly set.

        Steps:
            1. List all VirtualMachineClusterInstancetype resources in the cluster

        Expected:
            - VirtualMachineClusterInstancetype resources exist
        """
        pass

    def test_common_preferences_deployed_by_default(self):
        """
        Test that common preferences are deployed by default when
        CommonInstancetypesDeployment is not explicitly set.

        Steps:
            1. List all VirtualMachineClusterPreference resources in the cluster

        Expected:
            - VirtualMachineClusterPreference resources exist
        """
        pass


class TestCommonInstancetypesDeploymentPersistence:
    """
    Tests for CommonInstancetypesDeployment setting persistence across HCO reconciliation.

    Preconditions:
        - HCO CR patched with CommonInstancetypesDeployment.enabled set to false
        - HCO reconciliation completed after patching
        - Common-instancetypes confirmed absent
    """

    def test_disabled_setting_persists_after_reconciliation(self):
        """
        Test that CommonInstancetypesDeployment disabled setting persists after
        triggering HCO reconciliation by modifying an unrelated HCO field.

        Steps:
            1. Trigger HCO reconciliation by modifying an unrelated spec field
            2. Wait for HCO reconciliation to complete
            3. List all VirtualMachineClusterInstancetype resources in the cluster

        Expected:
            - No VirtualMachineClusterInstancetype resources exist
        """
        pass
```

---

## Test Coverage Summary

| Test File | Test Class | Test Count | Priority | Tier |
| --------- | ---------- | ---------- | -------- | ---- |
| `test_common_instancetypes_deployment.py` | `TestCommonInstancetypesDeploymentDisabled` | 2 | P0 | Tier 1 |
| `test_common_instancetypes_deployment.py` | `TestCommonInstancetypesDeploymentEnabled` | 2 | P0 | Tier 1 |
| `test_common_instancetypes_deployment.py` | `TestCommonInstancetypesDeploymentDefault` | 2 | P0 | Tier 1 |
| `test_common_instancetypes_deployment.py` | `TestCommonInstancetypesDeploymentPersistence` | 1 | P1 | Tier 1 |

**Total: 7 tests across 4 classes**

**Note:** Scenario 5 (Upgrade with Disabled Setting) from the STP is Tier 2/P2 and involves CNV upgrade testing, which is typically handled by separate upgrade test infrastructure and is excluded from this STD.

---

## Checklist

- [x] STP link in module docstring
- [x] Tests grouped in classes with shared preconditions
- [x] Each test has: description, Preconditions (class-level), Steps, Expected
- [x] Each test verifies ONE thing with ONE Expected
- [x] Negative tests marked with `[NEGATIVE]` (none applicable)
- [x] Test methods contain only `pass`
- [x] Markers documented (class-level where applicable)
- [x] Parametrization documented where needed (none applicable)
- [x] All files in single markdown output
- [x] Coverage summary table included
