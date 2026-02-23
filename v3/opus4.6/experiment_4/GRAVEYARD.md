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

## Entry: VMI reset on a paused VMI succeeds instead of failing

**Category**: AssertionError
**Date**: 2026-02-22
**Test**: tests/virt/node/hard_reset/test_vmi_reset_negative.py::TestVMIResetNegative::test_reset_fails_on_paused_vmi

### What Went Wrong
The STP (VIRTSTRAT-357, KL-01) stated "Reset is only supported for running VMIs; stopped/paused VMIs will return an error." Based on this, the test expected `pytest.raises(ApiException)` when calling `vmi.reset()` on a paused VMI. In reality, the KubeVirt API accepts the reset call on a paused VMI without raising an error. The reset signal is accepted but the VMI remains paused; the guest reboot takes effect only after unpausing. Additionally, calling `wait_for_running_vm()` after reset on a still-paused VMI causes a timeout because the guest agent cannot reconnect while paused.

### Wrong Code
```python
def test_reset_fails_on_paused_vmi(self, paused_vm):
    with pytest.raises(ApiException):
        paused_vm.vmi.reset()
```

### Correct Code
```python
def test_reset_succeeds_on_paused_vmi(self, paused_vm):
    paused_vm.vmi.reset()
    LOGGER.info(f"Reset API call succeeded on paused VMI {paused_vm.name}")
```

### Lesson Learned
The KubeVirt VMI reset subresource API does NOT reject reset calls on paused VMIs. The API accepts the call and the reset signal is queued. The VMI remains in paused state after the reset call. Do not call `wait_for_running_vm()` after resetting a paused VMI because the guest agent will not reconnect while the VMI is paused, causing a timeout.

### How to Avoid
When writing tests for VMI subresource operations (reset, pause, unpause, softreboot), always verify the actual API behavior against a live cluster rather than trusting STP/Jira descriptions of error handling. Specifically for VMI reset: it succeeds on both running and paused VMIs; it only fails when the VMI does not exist (stopped VM or non-existent name). Never follow `vmi.reset()` with `wait_for_running_vm()` if the VMI is paused.

---

## Entry: VM SSH file writes fail with Permission denied when using absolute /root/ paths

**Category**: CommandExecFailed
**Date**: 2026-02-22
**Test**: tests/storage/snapshots/test_snapshot_restore_data_integrity.py::TestSnapshotRestoreDataIntegrity::test_pre_snapshot_data_preserved

### What Went Wrong
The `write_file_via_ssh` utility was called with absolute paths like `/root/original.txt`. VMs created by `VirtualMachineForTests` use cloud-init with a randomly generated non-root username (e.g., `vh-974pSxxlmLLUR`). This user does not have write access to `/root/`, causing `Permission denied` errors when trying to create files there.

### Wrong Code
```python
write_file_via_ssh(vm=vm, filename="/root/original.txt", content="data-before-snapshot")
write_file_via_ssh(vm=vm, filename="/root/after.txt", content="post-snapshot")
```

### Correct Code
```python
# Use relative paths - writes to user's home directory (SSH login directory)
write_file_via_ssh(vm=vm, filename="original.txt", content="data-before-snapshot")
write_file_via_ssh(vm=vm, filename="after.txt", content="post-snapshot")
```

### Lesson Learned
`VirtualMachineForTests` creates VMs with a random non-root SSH user via cloud-init. The SSH session lands in the user's home directory (e.g., `/home/<random-user>/`). Writing to `/root/` requires root privileges that this user does not have. Existing snapshot tests in `tests/storage/conftest.py` use relative filenames (e.g., `"before-snap-0.txt"`) which correctly write to the user's home directory.

### How to Avoid
When writing files via SSH to VMs created by `VirtualMachineForTests`, always use relative file paths (e.g., `"myfile.txt"`) instead of absolute paths under `/root/`. Follow the existing pattern in `tests/storage/conftest.py` which uses relative filenames with `write_file_via_ssh`. The relative path resolves to the SSH user's home directory, which is always writable.

---
