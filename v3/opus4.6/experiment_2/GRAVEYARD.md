# GRAVEYARD - Test Generation Lessons Learned

This file documents mistakes made during automated test generation and how to avoid them.
It is read during the exploration phase to prevent repeating past errors.

---

## Entry: HCO CRD field name uses PascalCase, not camelCase

**Category**: ResourceError
**Date**: 2026-02-22
**Test**: tests/install_upgrade_operators/common_instancetypes_deployment/test_common_instancetypes_deployment.py::TestCommonInstancetypesDeployment::test_disable_common_instancetypes_removes_instancetype_resources

### What Went Wrong
The STP described the HCO field as `commonInstancetypesDeployment` (camelCase) with string values `"Enabled"` and `"Disabled"`. The actual CRD field is `CommonInstancetypesDeployment` (PascalCase) with an object value containing `{"enabled": <bool>}`. Kubernetes silently ignored the incorrectly-cased field, so HCO reconciled successfully but the setting had no effect.

### Wrong Code
```python
COMMON_INSTANCETYPES_DEPLOYMENT_SPEC_KEY = "commonInstancetypesDeployment"
DEPLOYMENT_DISABLED = "Disabled"
DEPLOYMENT_ENABLED = "Enabled"

# Patch: {"spec": {"commonInstancetypesDeployment": "Disabled"}}
```

### Correct Code
```python
COMMON_INSTANCETYPES_DEPLOYMENT_SPEC_KEY = "CommonInstancetypesDeployment"
DEPLOYMENT_DISABLED = {"enabled": False}
DEPLOYMENT_ENABLED = {"enabled": True}

# Patch: {"spec": {"CommonInstancetypesDeployment": {"enabled": False}}}
```

### Lesson Learned
STP documents may describe API fields inaccurately. Always verify the actual CRD schema on the cluster using `kubectl get crd <crd-name> -o jsonpath='{.spec.versions[0].schema.openAPIV3Schema.properties.spec.properties.<FieldName>}'` before generating test code. Kubernetes CRDs use case-sensitive field names and silently ignore unknown fields.

### How to Avoid
Before writing any HCO spec patch, verify the exact field name and value type from the CRD schema using `kubectl get crd hyperconvergeds.hco.kubevirt.io -o jsonpath='{.spec.versions[0].schema.openAPIV3Schema.properties.spec.properties}'`. Never trust STP field names verbatim.

---

## Entry: HCO reconciliation completes before downstream resources are fully created or deleted

**Category**: AssertionError
**Date**: 2026-02-22
**Test**: tests/install_upgrade_operators/common_instancetypes_deployment/test_common_instancetypes_deployment.py::TestCommonInstancetypesDeployment::test_enable_common_instancetypes_deploys_preference_resources

### What Went Wrong
After modifying the HCO CR `CommonInstancetypesDeployment` field and waiting for HCO conditions to stabilize (Available=True, Progressing=False, ReconcileComplete=True), the downstream VirtualMachineClusterInstancetype and VirtualMachineClusterPreference resources had not yet been fully created or deleted. The HCO operator reports reconciliation complete before the downstream controller (common-instancetypes) finishes processing.

### Wrong Code
```python
# Immediate assertion after HCO reconciliation
common_preferences = list(
    VirtualMachineClusterPreference.get(
        client=admin_client,
        label_selector=COMMON_INSTANCETYPE_VENDOR_LABEL,
    )
)
assert common_preferences, "No common preferences found after re-enabling"
```

### Correct Code
```python
# Poll with TimeoutSampler for async resource creation/deletion
from timeout_sampler import TimeoutSampler
from utilities.constants import TIMEOUT_2MIN

for sample in TimeoutSampler(
    wait_timeout=TIMEOUT_2MIN,
    sleep=5,
    func=lambda: list(
        VirtualMachineClusterPreference.get(
            client=admin_client,
            label_selector=COMMON_INSTANCETYPE_VENDOR_LABEL,
        )
    ),
):
    if sample:  # For creation: wait until resources exist
        break
    # For deletion: use `if not sample: break`
```

### Lesson Learned
HCO reconciliation completing does NOT mean downstream resources are immediately available. The common-instancetypes controller processes changes asynchronously. Always use `TimeoutSampler` to poll for the actual expected resource state rather than asserting immediately after HCO reconciliation.

### How to Avoid
When testing resource creation or deletion triggered by HCO CR changes, always use `TimeoutSampler` to poll for the expected resource state. Never assume resources are immediately available after `wait_for_hco_conditions` returns. This applies to any HCO-managed downstream resources (instancetypes, preferences, templates, etc.).

---
