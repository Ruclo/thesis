# GRAVEYARD - Test Generation Lessons Learned

This file documents mistakes made during automated test generation and how to avoid them.
It is read during the exploration phase to prevent repeating past errors.

---

## Entry: VirtualMachineInstance import path

**Category**: ImportError
**Date**: 2026-02-16
**Test**: tests/virt/node/general/test_vmi_reset.py

### What Went Wrong
Generated import `from ocp_resources.virtual_machine import VirtualMachineInstance`. The class lives in its own module.

### Wrong Code
```python
from ocp_resources.virtual_machine import VirtualMachineInstance
```

### Correct Code
```python
from ocp_resources.virtual_machine_instance import VirtualMachineInstance
```

### Lesson Learned
Each ocp_resources class has its own module file matching the class name in snake_case.

### How to Avoid
Always verify import paths by checking the actual module file exists under `.venv/lib/.../ocp_resources/`.

---

## Entry: Class-scoped fixture lazy evaluation ordering

**Category**: LogicError
**Date**: 2026-02-16
**Test**: tests/virt/node/general/test_vmi_reset.py::TestVMIReset::test_boot_time_changes_after_reset

### What Went Wrong
Class-scoped fixtures `boot_time_before_reset`, `vmi_uid_before_reset`, and `boot_count_before_reset` were lazily evaluated by pytest. The `vm_reset_and_running` fixture (which performs the reset) did not depend on them, so pytest could evaluate it first. This caused "before" measurements to actually be taken after the reset.

### Wrong Code
```python
@pytest.fixture(scope="class")
def vm_reset_and_running(vm_for_test):
    vm_for_test.vmi.reset()
    wait_for_running_vm(vm=vm_for_test)
```

### Correct Code
```python
@pytest.fixture(scope="class")
def vm_reset_and_running(
    vm_for_test,
    boot_count_before_reset,
    vmi_uid_before_reset,
    boot_time_before_reset,
):
    vm_for_test.vmi.reset()
    wait_for_running_vm(vm=vm_for_test)
```

### Lesson Learned
When a class-scoped "action" fixture must run AFTER "measurement" fixtures, declare the measurement fixtures as dependencies of the action fixture. Pytest evaluates fixtures lazily based on the dependency graph, not parameter order.

### How to Avoid
Any fixture that performs a state-changing action (reset, restart, migrate) must declare all "before state" measurement fixtures as its dependencies to force correct evaluation order.

---

## Entry: run_virtctl_command verify_stderr default causes false failures

**Category**: AssertionError
**Date**: 2026-02-16
**Test**: tests/virt/node/general/test_vmi_reset.py::TestVMIResetVirtctl::test_reset_running_vmi_via_virtctl

### What Went Wrong
`run_virtctl_command` has `verify_stderr=True` by default. The `virtctl reset` command writes an INFO-level JSON log to stderr even on success. This caused `run_virtctl_command` to return `False` (failure) despite the command succeeding.

### Wrong Code
```python
result, output, err = run_virtctl_command(
    command=["reset", vm_for_test.name],
    namespace=vm_for_test.namespace,
)
```

### Correct Code
```python
result, output, err = run_virtctl_command(
    command=["reset", vm_for_test.name],
    namespace=vm_for_test.namespace,
    verify_stderr=False,
)
```

### Lesson Learned
Many virtctl subcommands write informational logs to stderr. When using `run_virtctl_command`, always consider whether the command might produce stderr output that is not an error.

### How to Avoid
Pass `verify_stderr=False` when calling `run_virtctl_command` for commands that are known to write non-error output to stderr (e.g., `reset`, `vnc`, `console`).

---

## Entry: VMI subresource API raises ApiException not NotFoundError

**Category**: TypeError
**Date**: 2026-02-16
**Test**: tests/virt/node/general/test_vmi_reset.py::TestVMIResetNegative::test_reset_fails_on_stopped_vmi

### What Went Wrong
Expected `kubernetes.dynamic.exceptions.NotFoundError` when calling `vmi.reset()` on a non-existent VMI. The `reset()` method uses `api_request(method="PUT", action="reset")` which goes through the raw REST client, not the dynamic client. The raw client raises `kubernetes.client.rest.ApiException`.

### Wrong Code
```python
from kubernetes.dynamic.exceptions import NotFoundError

with pytest.raises(NotFoundError):
    stopped_vm.vmi.reset()
```

### Correct Code
```python
from kubernetes.client.rest import ApiException

with pytest.raises(ApiException, match="404"):
    stopped_vm.vmi.reset()
```

### Lesson Learned
ocp_resources subresource API methods (`pause()`, `unpause()`, `reset()`, etc.) use `api_request()` which goes through the raw Kubernetes REST client. These raise `kubernetes.client.rest.ApiException`, not `kubernetes.dynamic.exceptions.NotFoundError`. Use `match="404"` or `match="409"` to check the HTTP status code.

### How to Avoid
When catching exceptions from VMI subresource operations (`reset()`, `pause()`, `unpause()`), always use `kubernetes.client.rest.ApiException` with a status code match, not dynamic client exceptions.

---

## Entry: Resetting a paused VMI succeeds but keeps VM paused

**Category**: LogicError
**Date**: 2026-02-16
**Test**: tests/virt/node/general/test_vmi_reset.py::TestVMIResetNegative::test_reset_succeeds_on_paused_vmi

### What Went Wrong
Initially assumed resetting a paused VMI would fail with a ConflictError (409). In reality, KubeVirt allows resetting a paused VMI - the reset API call succeeds. However, after reset, the VMI remains in a paused state at the hypervisor level. Calling `wait_for_running_vm()` after reset times out because the guest agent cannot connect while the VM is paused.

### Wrong Code
```python
# First attempt: expected it to fail
with pytest.raises(ConflictError):
    paused_vm.vmi.reset()

# Second attempt: expected it to fully recover
paused_vm.vmi.reset()
wait_for_running_vm(vm=paused_vm)  # times out - VM is still paused
```

### Correct Code
```python
# Reset succeeds on paused VMI, but VM stays paused
paused_vm.vmi.reset()
# Do NOT call wait_for_running_vm - VM is still paused after reset
```

### Lesson Learned
KubeVirt allows resetting a paused VMI. The reset resets the guest at the QEMU level, but the pause state is maintained. After reset, the VMI phase shows Running but the Paused condition remains True. The guest agent cannot reconnect while paused, so `wait_for_running_vm()` will timeout.

### How to Avoid
When testing reset on a paused VMI, only verify the API call succeeds. Do not wait for the VM to be fully operational unless you also unpause it first.

---

## Entry: wait_for_running_vm SSH timeout after hard reset on container disk VMs

**Category**: TimeoutError
**Date**: 2026-02-17
**Test**: tests/virt/node/general/test_vmi_reset.py::TestVMIResetRBAC::test_edit_role_can_reset_vmi

### What Went Wrong
After calling `vmi.reset()` on a container disk VM, `wait_for_running_vm()` was called to verify the VM recovered. SSH connectivity never recovered even after 4 minutes (TIMEOUT_4MIN). The SSH service on the Fedora container disk image fails to re-establish connections after a hard reset, raising `SSHException: Error reading SSH protocol banner` indefinitely.

### Wrong Code
```python
def test_edit_role_can_reset_vmi(self, vm_for_test):
    vm_for_test.vmi.reset()
    wait_for_running_vm(vm=vm_for_test)  # times out - SSH never recovers
```

### Correct Code
```python
def test_edit_role_can_reset_vmi(self, vm_for_test):
    # Only verify the API call succeeds (no ForbiddenError).
    # Do NOT wait for SSH - container disk VMs may not recover SSH after hard reset.
    vm_for_test.vmi.reset()
```

### Lesson Learned
Container disk VMs use ephemeral filesystems. After a hard reset (equivalent to pressing the hardware reset button), the SSH service may fail to restart properly because the filesystem state is inconsistent. Only tests that specifically need to verify guest recovery after reset (like boot count checks) should call `wait_for_running_vm()`. Tests verifying API behavior (RBAC, permissions) should only assert the API call succeeds without waiting for SSH.

### How to Avoid
When testing reset for non-functional purposes (RBAC, API validation), only verify the API call does not raise an exception. Reserve `wait_for_running_vm()` for tests that explicitly verify guest-level recovery (boot count, data persistence).

---
