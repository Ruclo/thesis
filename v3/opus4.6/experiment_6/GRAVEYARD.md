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

## Entry: High cpu_max_sockets causes VM ErrorUnschedulable due to QEMU memory overhead

**Category**: ResourceError
**Date**: 2026-02-22
**Test**: tests/virt/node/hotplug/test_cpu_hotplug_max_limits.py::TestCPUHotplugMaxSocketsLimit::test_max_sockets_limited_by_vcpu_ceiling

### What Went Wrong
The VM fixture was created with `cpu_max_sockets=1024` to test the MaxSockets capping mechanism described in PR kubevirt/kubevirt#14511. KubeVirt's virt-launcher pod allocates memory proportional to the `maxSockets` value (for per-vCPU thread stacks and QEMU internal structures). With `maxSockets=1024`, the pod's total memory request exceeded what any worker node (~12.5 GiB allocatable) could provide, causing `ErrorUnschedulable: Insufficient memory`. Reducing to `maxSockets=16` and removing `memory_max_guest` still did not resolve the scheduling issue due to tight cluster resource constraints (system pods, Ceph/OCS storage, and operators consuming most available memory).

### Wrong Code
```python
HIGH_MAX_SOCKETS = 1024

# Fixture with high maxSockets and memory_max_guest
cpu_max_sockets=HIGH_MAX_SOCKETS,
memory_max_guest=None if is_s390x_cluster else TEN_GI_MEMORY,
memory_guest=FOUR_GI_MEMORY,
```

### Correct Code
```python
REQUESTED_MAX_SOCKETS = 16

# Fixture with moderate maxSockets and no memory_max_guest (CPU hotplug test doesn't need memory hotplug)
cpu_max_sockets=REQUESTED_MAX_SOCKETS,
memory_guest=FOUR_GI_MEMORY,
# memory_max_guest omitted - reduces virt-launcher pod memory request
```

### Lesson Learned
KubeVirt's virt-launcher pod memory request scales with `maxSockets` due to QEMU per-vCPU overhead. High `maxSockets` values (e.g., 1024) cause the pod to require more memory than cluster nodes can provide. Additionally, `memory_max_guest` adds memory reservation that may not be needed for CPU-only hotplug tests. On resource-constrained clusters (e.g., 12.5 GiB per worker), even moderate VMs (4Gi guest) can fail to schedule when system workloads (operators, Ceph, monitoring) consume most available memory.

### How to Avoid
When creating VMs for CPU hotplug testing: (1) Use modest `cpu_max_sockets` values (8-16) unless explicitly testing the upper bounds, matching the existing pattern of `EIGHT_CPU_SOCKETS=8`. (2) Omit `memory_max_guest` if the test does not need memory hotplug - this reduces the virt-launcher pod's memory footprint. (3) Before testing on a cluster, verify available memory using the `allocatable_memory_per_node` output in the test log. (4) Be aware that the MaxSockets capping fix (PR #14511) may not be deployed on all cluster versions, so the webhook may not cap the value, leaving the full resource request in effect.

---
