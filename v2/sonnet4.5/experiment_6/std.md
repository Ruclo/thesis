# Software Test Description (STD)

## **CPU Hotplug Logic Exceeding Maximum Limits - Detailed Test Descriptions**

---

### Metadata & Tracking

| Field                  | Details                                                           |
| :--------------------- | :---------------------------------------------------------------- |
| **Enhancement(s)**     | N/A - Bug Fix                                                     |
| **Feature in Jira**    | [CNV-61263](https://issues.redhat.com/browse/CNV-61263)           |
| **Jira Tracking**      | [CNV-57352](https://issues.redhat.com/browse/CNV-57352) (Bug Fix) |
| **QE Owner(s)**        | Victor Millac                                                     |
| **Owning SIG**         | sig-compute                                                       |
| **Document Type**      | Software Test Description (STD)                                   |
| **Current Status**     | Draft                                                             |
| **Related STP**        | `/home/mvavrine/cnv/thesis/stps/6.md`                             |

### Related GitHub Pull Requests

| PR Link                                                                    | Repository        | Source Jira Issue | Description                                                        |
| :------------------------------------------------------------------------- | :---------------- | :---------------- | :----------------------------------------------------------------- |
| [kubevirt/kubevirt#14511](https://github.com/kubevirt/kubevirt/pull/14511) | kubevirt/kubevirt | CNV-57352         | [release-1.5] defaults: Limit MaxSockets based on maximum of vcpus |

---

## Document Purpose

This Software Test Description (STD) provides detailed, step-by-step test procedures for validating the CPU Hotplug MaxSockets limiting functionality. It expands the test scenarios outlined in the corresponding Software Test Plan (STP) with specific technical implementation details, exact commands, API calls, validation points, and cleanup procedures.

---

## Test Scenario 1: MaxSockets Calculation Verification

**Test ID:** TS-01
**Priority:** P0
**Type:** Functional/Tier 1
**Feature:** CPU Hotplug MaxSockets Limiting
**Automation Required:** Yes

### Description

This test validates that the MaxSockets value is correctly calculated and limited based on the maximum vCPUs allowed for a VirtualMachine. It ensures that the default calculation logic properly sets MaxSockets to prevent exceeding the vCPU limit through CPU hotplug operations.

The test verifies the fix implemented in PR #14511, which ensures MaxSockets is derived from the maximum allowed vCPUs rather than being set independently, preventing resource overcommit scenarios.

### Preconditions

- OpenShift Virtualization operator is installed and operational (version 4.17+)
- Cluster has nodes with CPU virtualization enabled (VT-x or AMD-V)
- Test namespace exists and is accessible
- User has permissions to create and manage VirtualMachines
- CPU hotplug feature gate is enabled (if required for the version)
- At least one node has 8+ CPUs available for testing

### Test Steps

#### Step 1: Create VirtualMachine with CPU Hotplug Enabled

Create a VirtualMachine definition with specific CPU configuration and hotplug enabled.

**Command:**
```bash
oc apply -f - <<EOF
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: test-maxsockets-vm
  namespace: test-cpu-hotplug
spec:
  running: false
  template:
    metadata:
      labels:
        kubevirt.io/vm: test-maxsockets-vm
    spec:
      domain:
        cpu:
          sockets: 2
          cores: 1
          threads: 1
          maxSockets: 8
        resources:
          requests:
            memory: 2Gi
        devices:
          disks:
          - name: containerdisk
            disk:
              bus: virtio
          - name: cloudinitdisk
            disk:
              bus: virtio
      volumes:
      - name: containerdisk
        containerDisk:
          image: quay.io/kubevirt/fedora-cloud-container-disk-demo:latest
      - name: cloudinitdisk
        cloudInitNoCloud:
          userData: |
            #cloud-config
            password: fedora
            chpasswd: { expire: False }
EOF
```

**Expected:** VirtualMachine resource is created successfully.

**Validation:**
```bash
oc get vm test-maxsockets-vm -n test-cpu-hotplug -o yaml
```

Verify the VM exists and status shows `Created: true`.

#### Step 2: Retrieve VirtualMachine Specification

Extract the CPU configuration from the VirtualMachine spec to verify MaxSockets calculation.

**Command:**
```bash
oc get vm test-maxsockets-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu}' | jq .
```

**Expected:** Output shows the CPU configuration with fields:
- `sockets: 2`
- `cores: 1`
- `threads: 1`
- `maxSockets: 8`

**Validation:**
```bash
# Extract individual CPU fields
SOCKETS=$(oc get vm test-maxsockets-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.sockets}')
CORES=$(oc get vm test-maxsockets-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.cores}')
THREADS=$(oc get vm test-maxsockets-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.threads}')
MAX_SOCKETS=$(oc get vm test-maxsockets-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.maxSockets}')

echo "Sockets: $SOCKETS"
echo "Cores: $CORES"
echo "Threads: $THREADS"
echo "MaxSockets: $MAX_SOCKETS"
```

#### Step 3: Calculate Maximum vCPUs

Calculate the theoretical maximum vCPUs based on the configured values.

**Command:**
```bash
# Maximum vCPUs = maxSockets * cores * threads
MAX_VCPUS=$((MAX_SOCKETS * CORES * THREADS))
echo "Maximum vCPUs allowed: $MAX_VCPUS"
```

**Expected:** `Maximum vCPUs allowed: 8` (8 sockets * 1 core * 1 thread)

**Validation:** Verify that MAX_VCPUS equals the expected limit.

#### Step 4: Verify MaxSockets Constraint

Verify that MaxSockets does not exceed the maximum vCPUs that can be allocated.

**Command:**
```bash
# MaxSockets should be <= maximum vCPUs allowed
# In this case, MaxSockets (8) should be <= 8
if [ "$MAX_SOCKETS" -le "$MAX_VCPUS" ]; then
  echo "PASS: MaxSockets ($MAX_SOCKETS) is within limit (max vCPUs: $MAX_VCPUS)"
else
  echo "FAIL: MaxSockets ($MAX_SOCKETS) exceeds limit (max vCPUs: $MAX_VCPUS)"
fi
```

**Expected:** Output shows `PASS: MaxSockets (8) is within limit (max vCPUs: 8)`

**Validation:** Test assertion passes if MaxSockets <= MAX_VCPUS.

#### Step 5: Verify VirtualMachineInstance Configuration

Start the VM and verify the VirtualMachineInstance reflects the correct MaxSockets configuration.

**Command:**
```bash
# Start the VM
oc patch vm test-maxsockets-vm -n test-cpu-hotplug --type merge -p '{"spec":{"running":true}}'

# Wait for VMI to be ready
oc wait vmi test-maxsockets-vm -n test-cpu-hotplug --for=condition=Ready --timeout=300s
```

**Expected:** VMI starts successfully and reaches Ready state.

**Validation:**
```bash
# Retrieve VMI CPU configuration
oc get vmi test-maxsockets-vm -n test-cpu-hotplug -o jsonpath='{.spec.domain.cpu}' | jq .

# Verify MaxSockets in VMI matches VM spec
VMI_MAX_SOCKETS=$(oc get vmi test-maxsockets-vm -n test-cpu-hotplug -o jsonpath='{.spec.domain.cpu.maxSockets}')

if [ "$VMI_MAX_SOCKETS" -eq "$MAX_SOCKETS" ]; then
  echo "PASS: VMI MaxSockets ($VMI_MAX_SOCKETS) matches VM spec ($MAX_SOCKETS)"
else
  echo "FAIL: VMI MaxSockets ($VMI_MAX_SOCKETS) does not match VM spec ($MAX_SOCKETS)"
fi
```

#### Step 6: Inspect virt-launcher Pod Domain XML

Verify that the libvirt domain XML contains the correct CPU topology with MaxSockets limit.

**Command:**
```bash
# Get virt-launcher pod name
LAUNCHER_POD=$(oc get pod -n test-cpu-hotplug -l kubevirt.io/vm=test-maxsockets-vm -o jsonpath='{.items[0].metadata.name}')

# Extract domain XML
oc exec -n test-cpu-hotplug "$LAUNCHER_POD" -c compute -- virsh dumpxml 1 > /tmp/domain.xml

# Check CPU topology in domain XML
grep -A 5 "<cpu " /tmp/domain.xml
```

**Expected:** Domain XML shows CPU topology with correct socket configuration.

**Validation:**
```bash
# Verify topology element shows maxSockets
cat /tmp/domain.xml | grep -E "<topology sockets=.*maxSockets="
```

The topology should show sockets="2" and indicate maxSockets capability.

### Expected Results

- VirtualMachine is created successfully with specified CPU configuration
- MaxSockets value is correctly set and does not exceed maximum vCPUs
- MaxSockets calculation: `maxSockets <= (maxSockets * cores * threads)`
- VirtualMachineInstance reflects the same MaxSockets configuration as VirtualMachine
- Domain XML contains correct CPU topology with socket limits
- All validation assertions pass

### Postconditions

**Cleanup Steps:**

```bash
# Stop the VM
oc patch vm test-maxsockets-vm -n test-cpu-hotplug --type merge -p '{"spec":{"running":false}}'

# Wait for VMI termination
oc wait vmi test-maxsockets-vm -n test-cpu-hotplug --for=delete --timeout=120s

# Delete the VirtualMachine
oc delete vm test-maxsockets-vm -n test-cpu-hotplug

# Verify deletion
oc get vm test-maxsockets-vm -n test-cpu-hotplug 2>&1 | grep "NotFound"

# Clean up temporary files
rm -f /tmp/domain.xml
```

### Implementation Notes

- **Test Framework Integration:** This test should be implemented in the OpenShift Virtualization test framework under the CPU hotplug test suite.
- **Edge Cases:**
  - Test with different CPU topologies (multiple cores, multiple threads)
  - Verify behavior when maxSockets is not explicitly set (should use default calculation)
  - Test with very high maxSockets values to ensure proper limiting
- **API Fields:**
  - `spec.template.spec.domain.cpu.sockets` - Initial socket count
  - `spec.template.spec.domain.cpu.cores` - Cores per socket
  - `spec.template.spec.domain.cpu.threads` - Threads per core
  - `spec.template.spec.domain.cpu.maxSockets` - Maximum sockets for hotplug
- **Assertions:**
  - MaxSockets must be a positive integer
  - MaxSockets must be >= current sockets
  - MaxSockets * cores * threads must not exceed cluster limits
- **Dependencies:** Requires CPU hotplug feature support in libvirt and QEMU

---

## Test Scenario 2: CPU Hotplug at Maximum Limit

**Test ID:** TS-02
**Priority:** P0
**Type:** Functional/Tier 1
**Feature:** CPU Hotplug MaxSockets Limiting
**Automation Required:** Yes

### Description

This test validates that CPU hotplug operations are properly blocked or limited when a VirtualMachine reaches its maximum vCPU capacity. It ensures that attempting to add CPUs beyond the MaxSockets limit is prevented, protecting against resource overcommit and unpredictable guest behavior.

This test directly validates the core bug fix: preventing vCPU count from exceeding the maximum allowed through hotplug operations.

### Preconditions

- OpenShift Virtualization operator is installed and operational (version 4.17+)
- Test namespace exists and is accessible
- User has permissions to create and manage VirtualMachines
- CPU hotplug feature is enabled
- Cluster nodes have sufficient CPU resources (minimum 8 CPUs)
- Guest OS supports CPU hotplug (Fedora/RHEL recommended)

### Test Steps

#### Step 1: Create VirtualMachine with CPU Hotplug Near Limit

Create a VM with initial CPUs close to the maximum limit.

**Command:**
```bash
oc apply -f - <<EOF
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: test-hotplug-limit-vm
  namespace: test-cpu-hotplug
spec:
  running: false
  template:
    metadata:
      labels:
        kubevirt.io/vm: test-hotplug-limit-vm
    spec:
      domain:
        cpu:
          sockets: 6
          cores: 1
          threads: 1
          maxSockets: 8
        resources:
          requests:
            memory: 2Gi
        devices:
          disks:
          - name: containerdisk
            disk:
              bus: virtio
          - name: cloudinitdisk
            disk:
              bus: virtio
      volumes:
      - name: containerdisk
        containerDisk:
          image: quay.io/kubevirt/fedora-cloud-container-disk-demo:latest
      - name: cloudinitdisk
        cloudInitNoCloud:
          userData: |
            #cloud-config
            password: fedora
            chpasswd: { expire: False }
EOF
```

**Expected:** VirtualMachine is created with 6 sockets, maxSockets of 8 (leaving 2 sockets for hotplug).

**Validation:**
```bash
oc get vm test-hotplug-limit-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu}' | jq .
```

#### Step 2: Start the VirtualMachine

Start the VM and wait for it to be ready.

**Command:**
```bash
# Start the VM
oc patch vm test-hotplug-limit-vm -n test-cpu-hotplug --type merge -p '{"spec":{"running":true}}'

# Wait for VMI to be ready
oc wait vmi test-hotplug-limit-vm -n test-cpu-hotplug --for=condition=Ready --timeout=300s

# Verify VMI is running
oc get vmi test-hotplug-limit-vm -n test-cpu-hotplug
```

**Expected:** VMI reaches Running state with Ready condition.

**Validation:**
```bash
VMI_STATUS=$(oc get vmi test-hotplug-limit-vm -n test-cpu-hotplug -o jsonpath='{.status.phase}')
if [ "$VMI_STATUS" = "Running" ]; then
  echo "PASS: VMI is running"
else
  echo "FAIL: VMI status is $VMI_STATUS"
fi
```

#### Step 3: Verify Initial CPU Count in Guest OS

Connect to the guest and verify the initial CPU count.

**Command:**
```bash
# Use virtctl to connect to the VM console (or SSH if configured)
virtctl console test-hotplug-limit-vm -n test-cpu-hotplug << 'CONSOLE_EOF'
# Login as fedora/fedora

# Check CPU count
nproc

# Detailed CPU info
lscpu | grep "^CPU(s):"

exit
CONSOLE_EOF
```

**Alternative using SSH (if SSH is configured):**
```bash
# Get VM IP
VM_IP=$(oc get vmi test-hotplug-limit-vm -n test-cpu-hotplug -o jsonpath='{.status.interfaces[0].ipAddress}')

# SSH and check CPUs
ssh fedora@$VM_IP "nproc"
```

**Expected:** Guest OS shows 6 CPUs (6 sockets * 1 core * 1 thread).

**Validation:** CPU count in guest matches initial socket configuration.

#### Step 4: Hotplug CPUs to Near Maximum

Increase sockets to approach the maximum limit (7 out of 8).

**Command:**
```bash
# Patch VM to increase sockets to 7
oc patch vm test-hotplug-limit-vm -n test-cpu-hotplug --type merge -p '{"spec":{"template":{"spec":{"domain":{"cpu":{"sockets":7}}}}}}'

# Wait for the change to propagate
sleep 10

# Verify the patch was applied to VM
oc get vm test-hotplug-limit-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.sockets}'
```

**Expected:** VM spec shows sockets updated to 7.

**Validation:**
```bash
CURRENT_SOCKETS=$(oc get vm test-hotplug-limit-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.sockets}')
if [ "$CURRENT_SOCKETS" -eq 7 ]; then
  echo "PASS: Sockets updated to 7"
else
  echo "FAIL: Sockets are $CURRENT_SOCKETS, expected 7"
fi
```

#### Step 5: Verify CPU Hotplug in Guest OS

Check that the guest OS recognizes the additional CPU.

**Command:**
```bash
# Allow time for hotplug to take effect
sleep 15

# Check CPU count in guest
virtctl ssh fedora@test-hotplug-limit-vm -n test-cpu-hotplug "nproc"
```

**Expected:** Guest OS now shows 7 CPUs.

**Validation:**
```bash
CPU_COUNT=$(virtctl ssh fedora@test-hotplug-limit-vm -n test-cpu-hotplug "nproc")
if [ "$CPU_COUNT" -eq 7 ]; then
  echo "PASS: Guest OS shows 7 CPUs after hotplug"
else
  echo "FAIL: Guest OS shows $CPU_COUNT CPUs, expected 7"
fi
```

#### Step 6: Hotplug CPUs to Maximum Limit

Increase sockets to the maximum limit (8).

**Command:**
```bash
# Patch VM to increase sockets to maximum (8)
oc patch vm test-hotplug-limit-vm -n test-cpu-hotplug --type merge -p '{"spec":{"template":{"spec":{"domain":{"cpu":{"sockets":8}}}}}}'

# Wait for the change to propagate
sleep 10

# Verify the patch was applied
oc get vm test-hotplug-limit-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.sockets}'
```

**Expected:** VM spec shows sockets updated to 8 (maximum).

**Validation:**
```bash
CURRENT_SOCKETS=$(oc get vm test-hotplug-limit-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.sockets}')
if [ "$CURRENT_SOCKETS" -eq 8 ]; then
  echo "PASS: Sockets updated to maximum (8)"
else
  echo "FAIL: Sockets are $CURRENT_SOCKETS, expected 8"
fi
```

#### Step 7: Verify Maximum CPU Count in Guest OS

Verify that the guest OS recognizes the maximum number of CPUs.

**Command:**
```bash
# Allow time for hotplug to take effect
sleep 15

# Check CPU count in guest
virtctl ssh fedora@test-hotplug-limit-vm -n test-cpu-hotplug "nproc"
```

**Expected:** Guest OS shows 8 CPUs (maximum limit).

**Validation:**
```bash
CPU_COUNT=$(virtctl ssh fedora@test-hotplug-limit-vm -n test-cpu-hotplug "nproc")
if [ "$CPU_COUNT" -eq 8 ]; then
  echo "PASS: Guest OS shows maximum 8 CPUs"
else
  echo "FAIL: Guest OS shows $CPU_COUNT CPUs, expected 8"
fi
```

#### Step 8: Attempt to Exceed Maximum Limit

Attempt to hotplug beyond the maximum limit and verify it is blocked.

**Command:**
```bash
# Attempt to patch VM to increase sockets beyond maximum (9)
oc patch vm test-hotplug-limit-vm -n test-cpu-hotplug --type merge -p '{"spec":{"template":{"spec":{"domain":{"cpu":{"sockets":9}}}}}}' 2>&1 | tee /tmp/hotplug_error.log
```

**Expected:** The patch operation should either:
1. Be rejected by the API with a validation error, OR
2. Be accepted but not take effect (sockets remain at 8)

**Validation:**
```bash
# Check if patch was rejected
if grep -q "error\|Error\|invalid\|Invalid\|exceed" /tmp/hotplug_error.log; then
  echo "PASS: Patch was rejected with error"
  cat /tmp/hotplug_error.log
else
  # Check if sockets remained at maximum
  CURRENT_SOCKETS=$(oc get vm test-hotplug-limit-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.sockets}')
  if [ "$CURRENT_SOCKETS" -eq 8 ]; then
    echo "PASS: Sockets remain at maximum (8), patch did not take effect"
  else
    echo "FAIL: Sockets changed to $CURRENT_SOCKETS, should remain at 8"
  fi
fi
```

#### Step 9: Verify Guest OS CPU Count Unchanged

Verify that the guest OS still shows the maximum allowed CPUs and did not exceed the limit.

**Command:**
```bash
# Wait and verify CPU count in guest
sleep 10
CPU_COUNT=$(virtctl ssh fedora@test-hotplug-limit-vm -n test-cpu-hotplug "nproc")
echo "Final CPU count in guest: $CPU_COUNT"
```

**Expected:** Guest OS still shows 8 CPUs (no change).

**Validation:**
```bash
if [ "$CPU_COUNT" -eq 8 ]; then
  echo "PASS: Guest OS CPU count remains at maximum (8)"
else
  echo "FAIL: Guest OS shows $CPU_COUNT CPUs, expected 8"
fi
```

#### Step 10: Verify VirtualMachineInstance Status

Check VMI events and conditions for any errors or warnings related to CPU hotplug.

**Command:**
```bash
# Check VMI events
oc get events -n test-cpu-hotplug --field-selector involvedObject.name=test-hotplug-limit-vm --sort-by='.lastTimestamp'

# Check VMI conditions
oc get vmi test-hotplug-limit-vm -n test-cpu-hotplug -o jsonpath='{.status.conditions}' | jq .
```

**Expected:** No error conditions related to CPU configuration; VM remains healthy.

**Validation:** Review events and conditions for any unexpected errors.

### Expected Results

- VirtualMachine starts successfully with initial CPU configuration (6 sockets)
- CPU hotplug to 7 sockets succeeds and is reflected in guest OS
- CPU hotplug to maximum limit (8 sockets) succeeds and is reflected in guest OS
- Attempt to exceed maximum limit (9 sockets) is blocked or prevented
- Guest OS CPU count never exceeds the maximum limit (8 CPUs)
- VirtualMachineInstance remains healthy throughout the test
- No errors or crashes occur in the guest OS or hypervisor

### Postconditions

**Cleanup Steps:**

```bash
# Stop the VM
oc patch vm test-hotplug-limit-vm -n test-cpu-hotplug --type merge -p '{"spec":{"running":false}}'

# Wait for VMI termination
oc wait vmi test-hotplug-limit-vm -n test-cpu-hotplug --for=delete --timeout=120s

# Delete the VirtualMachine
oc delete vm test-hotplug-limit-vm -n test-cpu-hotplug

# Verify deletion
oc get vm test-hotplug-limit-vm -n test-cpu-hotplug 2>&1 | grep "NotFound"

# Clean up temporary files
rm -f /tmp/hotplug_error.log
```

### Implementation Notes

- **Test Framework Integration:** Implement in the CPU hotplug test suite with retry logic for guest OS verification.
- **Guest OS Verification:** Use virtctl or SSH to verify CPU counts; account for delays in CPU hotplug detection.
- **API Behavior:** The exact error handling may vary - test should handle both API rejection and silent limiting.
- **Edge Cases:**
  - Test with different CPU topologies (cores > 1, threads > 1)
  - Verify behavior when hotplugging multiple sockets at once
  - Test rapid sequential hotplug attempts
- **Timeout Considerations:** CPU hotplug in guest OS may take 5-30 seconds; adjust timeouts accordingly.
- **Guest OS Requirements:** Fedora/RHEL guests handle CPU hotplug automatically; other OSes may require manual online operations.
- **Monitoring:** Consider adding metrics collection for CPU hotplug latency and success rates.

---

## Test Scenario 3: Error Handling for Limit Violations

**Test ID:** TS-03
**Priority:** P1
**Type:** Functional/Tier 1
**Feature:** CPU Hotplug MaxSockets Limiting
**Automation Required:** Yes

### Description

This test validates that appropriate error messages are displayed when attempting to configure or hotplug CPUs beyond the maximum allowed limits. It ensures that users receive clear, actionable error messages that explain the constraint violation, rather than experiencing silent failures or cryptic errors.

This test verifies proper validation and user feedback mechanisms for the MaxSockets limiting feature.

### Preconditions

- OpenShift Virtualization operator is installed and operational (version 4.17+)
- Test namespace exists and is accessible
- User has permissions to create and manage VirtualMachines
- CPU hotplug feature is enabled
- No existing VirtualMachine with the test name exists

### Test Steps

#### Step 1: Attempt to Create VM with Invalid MaxSockets Configuration

Try to create a VirtualMachine with sockets exceeding maxSockets.

**Command:**
```bash
# Attempt to create VM with sockets (10) > maxSockets (8)
oc apply -f - <<EOF 2>&1 | tee /tmp/create_error.log
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: test-error-handling-vm
  namespace: test-cpu-hotplug
spec:
  running: false
  template:
    metadata:
      labels:
        kubevirt.io/vm: test-error-handling-vm
    spec:
      domain:
        cpu:
          sockets: 10
          cores: 1
          threads: 1
          maxSockets: 8
        resources:
          requests:
            memory: 2Gi
        devices:
          disks:
          - name: containerdisk
            disk:
              bus: virtio
      volumes:
      - name: containerdisk
        containerDisk:
          image: quay.io/kubevirt/fedora-cloud-container-disk-demo:latest
EOF
```

**Expected:** API should reject the creation with a validation error.

**Validation:**
```bash
# Check for validation error in output
if grep -q -i "error\|invalid\|validation\|exceed\|socket" /tmp/create_error.log; then
  echo "PASS: API rejected invalid configuration with error message"
  cat /tmp/create_error.log
else
  echo "FAIL: No error message found"
fi

# Verify VM was not created
VM_EXISTS=$(oc get vm test-error-handling-vm -n test-cpu-hotplug 2>&1)
if echo "$VM_EXISTS" | grep -q "NotFound"; then
  echo "PASS: VM was not created"
else
  echo "WARNING: VM may have been created despite invalid config"
fi
```

#### Step 2: Extract and Analyze Error Message

Parse the error message to verify it contains useful information.

**Command:**
```bash
# Extract error message details
ERROR_MSG=$(cat /tmp/create_error.log)

echo "Error message analysis:"
echo "$ERROR_MSG" | grep -i "socket" || echo "No socket-related message"
echo "$ERROR_MSG" | grep -i "maximum\|limit\|exceed" || echo "No limit-related message"
echo "$ERROR_MSG" | grep -i "cpu" || echo "No CPU-related message"
```

**Expected:** Error message should contain references to:
- Sockets/MaxSockets
- CPU limits or maximum values
- Clear indication of the constraint violation

**Validation:** Error message is informative and actionable.

#### Step 3: Create Valid VM for Subsequent Testing

Create a VM with valid configuration to test runtime validation.

**Command:**
```bash
oc apply -f - <<EOF
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: test-error-handling-vm
  namespace: test-cpu-hotplug
spec:
  running: false
  template:
    metadata:
      labels:
        kubevirt.io/vm: test-error-handling-vm
    spec:
      domain:
        cpu:
          sockets: 2
          cores: 1
          threads: 1
          maxSockets: 4
        resources:
          requests:
            memory: 2Gi
        devices:
          disks:
          - name: containerdisk
            disk:
              bus: virtio
          - name: cloudinitdisk
            disk:
              bus: virtio
      volumes:
      - name: containerdisk
        containerDisk:
          image: quay.io/kubevirt/fedora-cloud-container-disk-demo:latest
      - name: cloudinitdisk
        cloudInitNoCloud:
          userData: |
            #cloud-config
            password: fedora
            chpasswd: { expire: False }
EOF
```

**Expected:** VM is created successfully.

**Validation:**
```bash
oc get vm test-error-handling-vm -n test-cpu-hotplug
```

#### Step 4: Start the VM and Wait for Ready State

**Command:**
```bash
# Start the VM
oc patch vm test-error-handling-vm -n test-cpu-hotplug --type merge -p '{"spec":{"running":true}}'

# Wait for VMI to be ready
oc wait vmi test-error-handling-vm -n test-cpu-hotplug --for=condition=Ready --timeout=300s
```

**Expected:** VMI starts successfully.

**Validation:**
```bash
oc get vmi test-error-handling-vm -n test-cpu-hotplug -o jsonpath='{.status.phase}'
```

#### Step 5: Attempt to Hotplug Beyond MaxSockets While Running

Try to patch the running VM to exceed MaxSockets limit.

**Command:**
```bash
# Attempt to patch VM to 5 sockets (exceeding maxSockets of 4)
oc patch vm test-error-handling-vm -n test-cpu-hotplug --type merge -p '{"spec":{"template":{"spec":{"domain":{"cpu":{"sockets":5}}}}}}' 2>&1 | tee /tmp/hotplug_runtime_error.log
```

**Expected:** Operation should be rejected or not take effect.

**Validation:**
```bash
# Check for error in patch output
if grep -q -i "error\|invalid\|validation\|exceed" /tmp/hotplug_runtime_error.log; then
  echo "PASS: Runtime patch rejected with error"
  cat /tmp/hotplug_runtime_error.log
else
  # If no error, verify sockets didn't change
  CURRENT_SOCKETS=$(oc get vm test-error-handling-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.sockets}')
  if [ "$CURRENT_SOCKETS" -le 4 ]; then
    echo "PASS: Sockets remain within limit ($CURRENT_SOCKETS)"
  else
    echo "FAIL: Sockets exceeded limit ($CURRENT_SOCKETS)"
  fi
fi
```

#### Step 6: Check VirtualMachineInstance Events

Review VMI events for error messages related to the failed hotplug attempt.

**Command:**
```bash
# Get recent events for the VMI
oc get events -n test-cpu-hotplug --field-selector involvedObject.name=test-error-handling-vm --sort-by='.lastTimestamp' | tail -10

# Filter for Warning or Error events
oc get events -n test-cpu-hotplug --field-selector involvedObject.name=test-error-handling-vm,type=Warning --sort-by='.lastTimestamp'
```

**Expected:** Events may contain warnings or informational messages about CPU configuration constraints.

**Validation:** Review event messages for clarity and usefulness.

#### Step 7: Attempt to Modify MaxSockets Below Current Sockets

Try to reduce MaxSockets below the current socket count (invalid operation).

**Command:**
```bash
# Current sockets = 2, attempt to set maxSockets = 1
oc patch vm test-error-handling-vm -n test-cpu-hotplug --type merge -p '{"spec":{"template":{"spec":{"domain":{"cpu":{"maxSockets":1}}}}}}' 2>&1 | tee /tmp/maxsockets_error.log
```

**Expected:** Operation should be rejected with validation error.

**Validation:**
```bash
# Check for validation error
if grep -q -i "error\|invalid\|validation" /tmp/maxsockets_error.log; then
  echo "PASS: Invalid maxSockets change rejected"
  cat /tmp/maxsockets_error.log
else
  # Verify maxSockets didn't change to invalid value
  MAX_SOCKETS=$(oc get vm test-error-handling-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.maxSockets}')
  if [ "$MAX_SOCKETS" -ge 2 ]; then
    echo "PASS: maxSockets remains valid ($MAX_SOCKETS)"
  else
    echo "FAIL: maxSockets set to invalid value ($MAX_SOCKETS)"
  fi
fi
```

#### Step 8: Test Invalid CPU Topology Configuration

Attempt to create a VM with invalid CPU topology (e.g., negative values, zero values).

**Command:**
```bash
# Attempt to create VM with invalid CPU topology
oc apply -f - <<EOF 2>&1 | tee /tmp/invalid_topology_error.log
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: test-invalid-topology-vm
  namespace: test-cpu-hotplug
spec:
  running: false
  template:
    metadata:
      labels:
        kubevirt.io/vm: test-invalid-topology-vm
    spec:
      domain:
        cpu:
          sockets: 0
          cores: 1
          threads: 1
          maxSockets: 4
        resources:
          requests:
            memory: 2Gi
        devices:
          disks:
          - name: containerdisk
            disk:
              bus: virtio
      volumes:
      - name: containerdisk
        containerDisk:
          image: quay.io/kubevirt/fedora-cloud-container-disk-demo:latest
EOF
```

**Expected:** API should reject creation due to invalid socket count (0).

**Validation:**
```bash
# Check for validation error
if grep -q -i "error\|invalid\|validation" /tmp/invalid_topology_error.log; then
  echo "PASS: Invalid CPU topology rejected"
  cat /tmp/invalid_topology_error.log
else
  echo "FAIL: Invalid topology not rejected"
fi

# Verify VM was not created
oc get vm test-invalid-topology-vm -n test-cpu-hotplug 2>&1 | grep -q "NotFound" && echo "PASS: VM not created"
```

#### Step 9: Verify Error Message Consistency

Compare error messages from different validation points to ensure consistency.

**Command:**
```bash
echo "=== Error Message Analysis ==="
echo ""
echo "Create-time validation error:"
grep -i "error" /tmp/create_error.log | head -3
echo ""
echo "Runtime validation error:"
grep -i "error" /tmp/hotplug_runtime_error.log | head -3
echo ""
echo "MaxSockets validation error:"
grep -i "error" /tmp/maxsockets_error.log | head -3
echo ""
echo "Invalid topology error:"
grep -i "error" /tmp/invalid_topology_error.log | head -3
```

**Expected:** Error messages should be consistent in format and provide clear guidance.

**Validation:** Manual review of error message quality and consistency.

#### Step 10: Document Error Messages for User Documentation

Extract and format error messages for documentation purposes.

**Command:**
```bash
# Create error message summary
cat > /tmp/error_messages_summary.txt << 'EOF'
CPU Hotplug MaxSockets Error Messages Summary
==============================================

1. Sockets exceeding MaxSockets:
EOF

grep -A 2 "error" /tmp/create_error.log >> /tmp/error_messages_summary.txt

cat >> /tmp/error_messages_summary.txt << 'EOF'

2. Runtime hotplug exceeding limit:
EOF

grep -A 2 "error" /tmp/hotplug_runtime_error.log >> /tmp/error_messages_summary.txt

cat >> /tmp/error_messages_summary.txt << 'EOF'

3. MaxSockets below current sockets:
EOF

grep -A 2 "error" /tmp/maxsockets_error.log >> /tmp/error_messages_summary.txt

cat /tmp/error_messages_summary.txt
```

**Expected:** Summary document contains all error scenarios and messages.

**Validation:** Review for completeness and clarity.

### Expected Results

- VM creation with invalid CPU configuration is rejected with clear error message
- Error messages mention specific constraints (sockets, maxSockets, CPU limits)
- Runtime hotplug attempts beyond MaxSockets are blocked or rejected
- Reducing MaxSockets below current sockets is prevented
- Invalid CPU topology values (0, negative) are rejected at creation time
- All error messages are consistent, clear, and actionable
- Events and logs contain sufficient information for troubleshooting
- Error message format is suitable for user documentation

### Postconditions

**Cleanup Steps:**

```bash
# Stop and delete the test VM
oc patch vm test-error-handling-vm -n test-cpu-hotplug --type merge -p '{"spec":{"running":false}}' 2>/dev/null
oc wait vmi test-error-handling-vm -n test-cpu-hotplug --for=delete --timeout=120s 2>/dev/null
oc delete vm test-error-handling-vm -n test-cpu-hotplug 2>/dev/null

# Verify deletion
oc get vm test-error-handling-vm -n test-cpu-hotplug 2>&1 | grep "NotFound"

# Delete any invalid VMs that may have been created
oc delete vm test-invalid-topology-vm -n test-cpu-hotplug 2>/dev/null

# Clean up temporary files
rm -f /tmp/create_error.log
rm -f /tmp/hotplug_runtime_error.log
rm -f /tmp/maxsockets_error.log
rm -f /tmp/invalid_topology_error.log
rm -f /tmp/error_messages_summary.txt
```

### Implementation Notes

- **Error Message Format:** OpenShift/Kubernetes validation errors typically include field paths and constraint details.
- **API Validation Levels:**
  - Schema validation (basic type/range checks)
  - Webhook validation (custom business logic)
  - Admission controller validation
- **Test Variations:**
  - Test with different API versions (v1, v1alpha3, etc.)
  - Test with OpenShift Console UI (if applicable)
  - Test with virtctl commands
- **Error Message Requirements:**
  - Must clearly identify the constraint violation
  - Should suggest valid ranges or corrective actions
  - Must use consistent terminology
- **Documentation Impact:** Error messages should be included in troubleshooting documentation.
- **Localization:** If product supports multiple languages, error messages should be localization-ready.
- **Regression Testing:** Verify that error messages don't regress with future updates.

---

## Test Scenario 4: Full CPU Hotplug Lifecycle (E2E)

**Test ID:** TS-04
**Priority:** P1
**Type:** End-to-End/Tier 2
**Feature:** CPU Hotplug MaxSockets Limiting
**Automation Required:** Yes

### Description

This comprehensive end-to-end test validates the complete CPU hotplug lifecycle, from VM creation with minimal CPUs through progressive hotplug operations up to the maximum allowed limit, with full verification in the guest operating system. It ensures that the entire workflow functions correctly with proper limit enforcement at each stage.

This test provides comprehensive validation of the CPU hotplug feature with MaxSockets limiting in a realistic usage scenario.

### Preconditions

- OpenShift Virtualization operator is installed and operational (version 4.17+)
- Test namespace exists and is accessible
- User has permissions to create and manage VirtualMachines
- CPU hotplug feature is enabled in the cluster
- Cluster nodes have sufficient CPU resources (minimum 12 CPUs recommended)
- Guest OS image supports CPU hotplug (Fedora 38+ or RHEL 9+ recommended)
- Network connectivity for VM SSH access (if using SSH for verification)
- virtctl CLI is installed and configured

### Test Steps

#### Step 1: Create VirtualMachine with Minimal CPU Configuration

Create a VM starting with a low CPU count to maximize hotplug testing range.

**Command:**
```bash
oc apply -f - <<EOF
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: test-full-lifecycle-vm
  namespace: test-cpu-hotplug
  labels:
    test-type: cpu-hotplug-e2e
spec:
  running: false
  template:
    metadata:
      labels:
        kubevirt.io/vm: test-full-lifecycle-vm
    spec:
      domain:
        cpu:
          sockets: 2
          cores: 1
          threads: 1
          maxSockets: 8
        resources:
          requests:
            memory: 4Gi
          limits:
            memory: 4Gi
        devices:
          disks:
          - name: containerdisk
            disk:
              bus: virtio
          - name: cloudinitdisk
            disk:
              bus: virtio
          interfaces:
          - name: default
            masquerade: {}
      networks:
      - name: default
        pod: {}
      volumes:
      - name: containerdisk
        containerDisk:
          image: quay.io/kubevirt/fedora-cloud-container-disk-demo:latest
      - name: cloudinitdisk
        cloudInitNoCloud:
          userData: |
            #cloud-config
            password: fedora
            chpasswd: { expire: False }
            ssh_pwauth: True
            disable_root: false
            runcmd:
              - echo "CPU hotplug test VM ready" > /tmp/vm_ready
EOF
```

**Expected:** VirtualMachine resource is created successfully.

**Validation:**
```bash
# Verify VM exists
oc get vm test-full-lifecycle-vm -n test-cpu-hotplug

# Verify CPU configuration
oc get vm test-full-lifecycle-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu}' | jq .
```

Expected output:
```json
{
  "sockets": 2,
  "cores": 1,
  "threads": 1,
  "maxSockets": 8
}
```

#### Step 2: Start VirtualMachine and Verify Initial State

Start the VM and wait for it to be fully operational.

**Command:**
```bash
# Start the VM
oc patch vm test-full-lifecycle-vm -n test-cpu-hotplug --type merge -p '{"spec":{"running":true}}'

# Wait for VMI to be ready
oc wait vmi test-full-lifecycle-vm -n test-cpu-hotplug --for=condition=Ready --timeout=300s

# Verify VMI is running
oc get vmi test-full-lifecycle-vm -n test-cpu-hotplug -o wide
```

**Expected:** VMI reaches Running state with Ready condition within 5 minutes.

**Validation:**
```bash
# Check VMI phase
VMI_PHASE=$(oc get vmi test-full-lifecycle-vm -n test-cpu-hotplug -o jsonpath='{.status.phase}')
echo "VMI Phase: $VMI_PHASE"

if [ "$VMI_PHASE" = "Running" ]; then
  echo "PASS: VMI is running"
else
  echo "FAIL: VMI phase is $VMI_PHASE"
  exit 1
fi

# Check Ready condition
READY_CONDITION=$(oc get vmi test-full-lifecycle-vm -n test-cpu-hotplug -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
echo "Ready Condition: $READY_CONDITION"

if [ "$READY_CONDITION" = "True" ]; then
  echo "PASS: VMI is ready"
else
  echo "FAIL: VMI not ready"
  exit 1
fi
```

#### Step 3: Verify Initial CPU Count in Guest OS

Connect to the guest and verify the initial CPU count matches the configuration.

**Command:**
```bash
# Wait for guest to fully boot
sleep 30

# Use virtctl to access the guest
INITIAL_CPU_COUNT=$(virtctl ssh fedora@test-full-lifecycle-vm -n test-cpu-hotplug "nproc" 2>/dev/null || echo "0")

echo "Initial CPU count in guest: $INITIAL_CPU_COUNT"

# Get detailed CPU information
virtctl ssh fedora@test-full-lifecycle-vm -n test-cpu-hotplug "lscpu | grep -E '^CPU\(s\)|^Thread|^Core|^Socket'" 2>/dev/null
```

**Expected:** Guest OS shows 2 CPUs (2 sockets * 1 core * 1 thread).

**Validation:**
```bash
if [ "$INITIAL_CPU_COUNT" -eq 2 ]; then
  echo "PASS: Initial CPU count is correct (2)"
else
  echo "FAIL: Initial CPU count is $INITIAL_CPU_COUNT, expected 2"
fi
```

#### Step 4: First Hotplug Operation (2 to 4 CPUs)

Perform the first CPU hotplug operation, doubling the CPU count.

**Command:**
```bash
echo "=== First Hotplug: 2 -> 4 CPUs ==="

# Record timestamp
HOTPLUG_START=$(date +%s)

# Patch VM to increase sockets from 2 to 4
oc patch vm test-full-lifecycle-vm -n test-cpu-hotplug --type merge -p '{"spec":{"template":{"spec":{"domain":{"cpu":{"sockets":4}}}}}}'

# Verify patch applied to VM spec
sleep 5
CURRENT_SOCKETS=$(oc get vm test-full-lifecycle-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.sockets}')
echo "VM spec sockets: $CURRENT_SOCKETS"
```

**Expected:** VM spec updated to 4 sockets.

**Validation:**
```bash
if [ "$CURRENT_SOCKETS" -eq 4 ]; then
  echo "PASS: VM spec updated to 4 sockets"
else
  echo "FAIL: VM spec shows $CURRENT_SOCKETS sockets, expected 4"
fi
```

#### Step 5: Verify First Hotplug in Guest OS

Verify the guest OS recognizes the additional CPUs.

**Command:**
```bash
# Wait for hotplug to propagate
sleep 20

# Check CPU count in guest
CPU_COUNT=$(virtctl ssh fedora@test-full-lifecycle-vm -n test-cpu-hotplug "nproc")
echo "CPU count after first hotplug: $CPU_COUNT"

# Calculate hotplug latency
HOTPLUG_END=$(date +%s)
HOTPLUG_LATENCY=$((HOTPLUG_END - HOTPLUG_START))
echo "Hotplug latency: ${HOTPLUG_LATENCY}s"

# Verify CPUs are online
virtctl ssh fedora@test-full-lifecycle-vm -n test-cpu-hotplug "lscpu | grep 'On-line CPU(s)'"
virtctl ssh fedora@test-full-lifecycle-vm -n test-cpu-hotplug "grep -E 'processor|cpu MHz' /proc/cpuinfo | head -20"
```

**Expected:** Guest OS shows 4 CPUs, all online.

**Validation:**
```bash
if [ "$CPU_COUNT" -eq 4 ]; then
  echo "PASS: Guest OS shows 4 CPUs after first hotplug"
else
  echo "FAIL: Guest OS shows $CPU_COUNT CPUs, expected 4"
fi
```

#### Step 6: Second Hotplug Operation (4 to 6 CPUs)

Perform a second hotplug operation.

**Command:**
```bash
echo "=== Second Hotplug: 4 -> 6 CPUs ==="

HOTPLUG_START=$(date +%s)

# Patch VM to increase sockets from 4 to 6
oc patch vm test-full-lifecycle-vm -n test-cpu-hotplug --type merge -p '{"spec":{"template":{"spec":{"domain":{"cpu":{"sockets":6}}}}}}'

# Verify patch applied
sleep 5
CURRENT_SOCKETS=$(oc get vm test-full-lifecycle-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.sockets}')
echo "VM spec sockets: $CURRENT_SOCKETS"
```

**Expected:** VM spec updated to 6 sockets.

**Validation:**
```bash
if [ "$CURRENT_SOCKETS" -eq 6 ]; then
  echo "PASS: VM spec updated to 6 sockets"
else
  echo "FAIL: VM spec shows $CURRENT_SOCKETS sockets, expected 6"
fi
```

#### Step 7: Verify Second Hotplug in Guest OS

**Command:**
```bash
# Wait for hotplug to propagate
sleep 20

# Check CPU count in guest
CPU_COUNT=$(virtctl ssh fedora@test-full-lifecycle-vm -n test-cpu-hotplug "nproc")
echo "CPU count after second hotplug: $CPU_COUNT"

HOTPLUG_END=$(date +%s)
HOTPLUG_LATENCY=$((HOTPLUG_END - HOTPLUG_START))
echo "Hotplug latency: ${HOTPLUG_LATENCY}s"
```

**Expected:** Guest OS shows 6 CPUs.

**Validation:**
```bash
if [ "$CPU_COUNT" -eq 6 ]; then
  echo "PASS: Guest OS shows 6 CPUs after second hotplug"
else
  echo "FAIL: Guest OS shows $CPU_COUNT CPUs, expected 6"
fi
```

#### Step 8: Third Hotplug Operation to Maximum (6 to 8 CPUs)

Perform final hotplug to reach the maximum limit.

**Command:**
```bash
echo "=== Third Hotplug: 6 -> 8 CPUs (Maximum) ==="

HOTPLUG_START=$(date +%s)

# Patch VM to increase sockets to maximum (8)
oc patch vm test-full-lifecycle-vm -n test-cpu-hotplug --type merge -p '{"spec":{"template":{"spec":{"domain":{"cpu":{"sockets":8}}}}}}'

# Verify patch applied
sleep 5
CURRENT_SOCKETS=$(oc get vm test-full-lifecycle-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.sockets}')
echo "VM spec sockets: $CURRENT_SOCKETS"
```

**Expected:** VM spec updated to 8 sockets (maximum).

**Validation:**
```bash
if [ "$CURRENT_SOCKETS" -eq 8 ]; then
  echo "PASS: VM spec updated to maximum 8 sockets"
else
  echo "FAIL: VM spec shows $CURRENT_SOCKETS sockets, expected 8"
fi
```

#### Step 9: Verify Maximum CPUs in Guest OS

**Command:**
```bash
# Wait for hotplug to propagate
sleep 20

# Check CPU count in guest
CPU_COUNT=$(virtctl ssh fedora@test-full-lifecycle-vm -n test-cpu-hotplug "nproc")
echo "CPU count at maximum: $CPU_COUNT"

HOTPLUG_END=$(date +%s)
HOTPLUG_LATENCY=$((HOTPLUG_END - HOTPLUG_START))
echo "Hotplug latency: ${HOTPLUG_LATENCY}s"

# Verify all CPUs are online and functioning
virtctl ssh fedora@test-full-lifecycle-vm -n test-cpu-hotplug "lscpu"
```

**Expected:** Guest OS shows 8 CPUs, all online.

**Validation:**
```bash
if [ "$CPU_COUNT" -eq 8 ]; then
  echo "PASS: Guest OS shows maximum 8 CPUs"
else
  echo "FAIL: Guest OS shows $CPU_COUNT CPUs, expected 8"
fi
```

#### Step 10: Attempt to Exceed Maximum Limit

Try to add more CPUs beyond the maximum to verify limit enforcement.

**Command:**
```bash
echo "=== Attempting to Exceed Maximum Limit ==="

# Attempt to patch VM to 9 sockets (beyond maximum of 8)
oc patch vm test-full-lifecycle-vm -n test-cpu-hotplug --type merge -p '{"spec":{"template":{"spec":{"domain":{"cpu":{"sockets":9}}}}}}' 2>&1 | tee /tmp/exceed_limit_error.log

# Wait and check if sockets changed
sleep 10
FINAL_SOCKETS=$(oc get vm test-full-lifecycle-vm -n test-cpu-hotplug -o jsonpath='{.spec.template.spec.domain.cpu.sockets}')
echo "Final sockets value: $FINAL_SOCKETS"
```

**Expected:** Either patch is rejected, or sockets remain at 8.

**Validation:**
```bash
if grep -q -i "error\|invalid\|exceed" /tmp/exceed_limit_error.log; then
  echo "PASS: Patch was rejected with error"
  cat /tmp/exceed_limit_error.log
elif [ "$FINAL_SOCKETS" -eq 8 ]; then
  echo "PASS: Sockets remain at maximum (8), patch did not take effect"
else
  echo "FAIL: Sockets changed to $FINAL_SOCKETS, should be 8"
fi
```

#### Step 11: Verify Guest OS Stability at Maximum

Run stress tests in the guest to ensure stability with maximum CPUs.

**Command:**
```bash
echo "=== Testing Guest OS Stability ==="

# Verify CPU count hasn't changed
CPU_COUNT=$(virtctl ssh fedora@test-full-lifecycle-vm -n test-cpu-hotplug "nproc")
echo "Final CPU count in guest: $CPU_COUNT"

# Run a brief CPU stress test on all cores
virtctl ssh fedora@test-full-lifecycle-vm -n test-cpu-hotplug << 'STRESS_TEST'
# Simple CPU stress test
echo "Running CPU stress test on all cores..."
for i in $(seq 1 8); do
  taskset -c $((i-1)) dd if=/dev/zero of=/dev/null bs=1M count=100 &
done
wait
echo "CPU stress test completed"

# Verify all CPUs are still online
echo "CPUs online: $(nproc)"
lscpu | grep "On-line CPU(s)"
STRESS_TEST
```

**Expected:** Guest OS remains stable, all 8 CPUs functional under load.

**Validation:**
```bash
# Verify guest is still responsive
if virtctl ssh fedora@test-full-lifecycle-vm -n test-cpu-hotplug "echo 'Guest responsive'" | grep -q "Guest responsive"; then
  echo "PASS: Guest OS remains responsive after stress test"
else
  echo "FAIL: Guest OS not responsive"
fi
```

#### Step 12: Verify VirtualMachineInstance Status and Events

Check VMI health and review events for the entire lifecycle.

**Command:**
```bash
echo "=== VirtualMachineInstance Status ==="

# Check VMI conditions
oc get vmi test-full-lifecycle-vm -n test-cpu-hotplug -o jsonpath='{.status.conditions}' | jq .

# Check VMI CPU status
oc get vmi test-full-lifecycle-vm -n test-cpu-hotplug -o jsonpath='{.status.guestOSInfo.topology}' | jq .

# Review all events for the VM
echo "=== VM Events ==="
oc get events -n test-cpu-hotplug --field-selector involvedObject.name=test-full-lifecycle-vm --sort-by='.lastTimestamp'
```

**Expected:** VMI shows healthy status, no error conditions, events show successful hotplug operations.

**Validation:** Manual review of conditions and events.

#### Step 13: Verify Resource Metrics

Check CPU metrics and resource usage.

**Command:**
```bash
echo "=== Resource Metrics ==="

# Get VMI resource usage (requires metrics server)
oc get --raw "/apis/metrics.k8s.io/v1beta1/namespaces/test-cpu-hotplug/pods" | jq '.items[] | select(.metadata.name | contains("test-full-lifecycle-vm")) | .containers[].usage'

# Check virt-launcher pod resources
LAUNCHER_POD=$(oc get pod -n test-cpu-hotplug -l kubevirt.io/vm=test-full-lifecycle-vm -o jsonpath='{.items[0].metadata.name}')
echo "virt-launcher pod: $LAUNCHER_POD"

oc top pod "$LAUNCHER_POD" -n test-cpu-hotplug
```

**Expected:** Metrics reflect the CPU configuration (8 vCPUs).

**Validation:** Review resource usage is appropriate for 8 vCPUs.

#### Step 14: Test VM Lifecycle Operations at Maximum CPUs

Verify VM can be stopped and restarted while at maximum CPUs.

**Command:**
```bash
echo "=== Testing VM Stop/Restart ==="

# Stop the VM
oc patch vm test-full-lifecycle-vm -n test-cpu-hotplug --type merge -p '{"spec":{"running":false}}'

# Wait for VMI to terminate
oc wait vmi test-full-lifecycle-vm -n test-cpu-hotplug --for=delete --timeout=120s

# Verify VMI is deleted
if oc get vmi test-full-lifecycle-vm -n test-cpu-hotplug 2>&1 | grep -q "NotFound"; then
  echo "PASS: VMI terminated successfully"
else
  echo "FAIL: VMI still exists"
fi

# Restart the VM
oc patch vm test-full-lifecycle-vm -n test-cpu-hotplug --type merge -p '{"spec":{"running":true}}'

# Wait for VMI to be ready again
oc wait vmi test-full-lifecycle-vm -n test-cpu-hotplug --for=condition=Ready --timeout=300s
```

**Expected:** VM stops and restarts successfully with 8 CPUs.

**Validation:**
```bash
# Verify CPUs after restart
sleep 30
CPU_COUNT=$(virtctl ssh fedora@test-full-lifecycle-vm -n test-cpu-hotplug "nproc")

if [ "$CPU_COUNT" -eq 8 ]; then
  echo "PASS: VM restarted with 8 CPUs"
else
  echo "FAIL: VM shows $CPU_COUNT CPUs after restart, expected 8"
fi
```

#### Step 15: Document Complete Lifecycle Metrics

Collect and document performance metrics for the entire test.

**Command:**
```bash
cat > /tmp/lifecycle_metrics.txt << 'EOF'
CPU Hotplug Lifecycle Test Metrics
====================================
EOF

echo "Initial CPU Count: 2" >> /tmp/lifecycle_metrics.txt
echo "Maximum CPU Count: 8" >> /tmp/lifecycle_metrics.txt
echo "Total Hotplug Operations: 3" >> /tmp/lifecycle_metrics.txt
echo "Final CPU Count in Guest: $CPU_COUNT" >> /tmp/lifecycle_metrics.txt
echo "" >> /tmp/lifecycle_metrics.txt
echo "Hotplug Operations:" >> /tmp/lifecycle_metrics.txt
echo "  1. 2 -> 4 CPUs" >> /tmp/lifecycle_metrics.txt
echo "  2. 4 -> 6 CPUs" >> /tmp/lifecycle_metrics.txt
echo "  3. 6 -> 8 CPUs (Maximum)" >> /tmp/lifecycle_metrics.txt
echo "" >> /tmp/lifecycle_metrics.txt
echo "Limit Enforcement: Verified" >> /tmp/lifecycle_metrics.txt
echo "VM Stability: Passed" >> /tmp/lifecycle_metrics.txt
echo "Restart with Max CPUs: Passed" >> /tmp/lifecycle_metrics.txt

cat /tmp/lifecycle_metrics.txt
```

**Expected:** Complete metrics document generated.

**Validation:** Review metrics for completeness.

### Expected Results

- VirtualMachine is created successfully with initial configuration (2 CPUs, maxSockets: 8)
- VM starts successfully and guest OS shows correct initial CPU count (2)
- First hotplug operation (2 to 4 CPUs) succeeds and is reflected in guest OS
- Second hotplug operation (4 to 6 CPUs) succeeds and is reflected in guest OS
- Third hotplug operation (6 to 8 CPUs) succeeds, reaching maximum limit
- Guest OS correctly shows 8 CPUs at maximum configuration
- Attempt to exceed maximum (9 CPUs) is blocked or prevented
- Guest OS remains stable under CPU load with maximum CPUs
- VM can be stopped and restarted successfully while at maximum CPU configuration
- All CPUs remain functional and online throughout the lifecycle
- No errors or warnings in VMI events or conditions
- VirtualMachineInstance maintains healthy status throughout all operations
- Metrics accurately reflect CPU configuration at each stage

### Postconditions

**Cleanup Steps:**

```bash
echo "=== Cleanup ==="

# Stop the VM
oc patch vm test-full-lifecycle-vm -n test-cpu-hotplug --type merge -p '{"spec":{"running":false}}'

# Wait for VMI termination
oc wait vmi test-full-lifecycle-vm -n test-cpu-hotplug --for=delete --timeout=120s

# Delete the VirtualMachine
oc delete vm test-full-lifecycle-vm -n test-cpu-hotplug

# Verify deletion
if oc get vm test-full-lifecycle-vm -n test-cpu-hotplug 2>&1 | grep -q "NotFound"; then
  echo "PASS: VM deleted successfully"
else
  echo "WARNING: VM may still exist"
fi

# Clean up temporary files
rm -f /tmp/exceed_limit_error.log
rm -f /tmp/lifecycle_metrics.txt

echo "Cleanup complete"
```

### Implementation Notes

- **Test Duration:** This E2E test may take 10-15 minutes to complete due to VM boot times and hotplug propagation delays.
- **Guest OS Requirements:**
  - Must support CPU hotplug (Fedora 38+, RHEL 9+, Ubuntu 22.04+ recommended)
  - udev rules should automatically online hotplugged CPUs
  - acpid daemon should be running for proper ACPI event handling
- **Timing Considerations:**
  - Allow 20-30 seconds after each hotplug for guest OS detection
  - VM initial boot may take 60-120 seconds
  - Adjust timeouts based on cluster performance
- **Metrics Collection:**
  - Requires Prometheus and metrics server for resource metrics
  - Consider adding custom metrics for hotplug latency
- **Stress Testing:**
  - Consider using stress-ng or similar tools for more comprehensive CPU stress testing
  - Monitor guest OS logs during stress tests for any errors
- **Variations to Test:**
  - Different CPU topologies (cores > 1, threads > 1)
  - Different guest operating systems
  - Different initial to maximum ratios
  - Multiple VMs with hotplug simultaneously
- **Performance Metrics:**
  - Track hotplug latency (time from patch to guest recognition)
  - Monitor resource overhead of hotplug operations
  - Document any performance degradation at maximum CPU count
- **Error Recovery:**
  - Test should handle temporary network issues when accessing guest
  - Implement retries for SSH/virtctl connections
  - Verify VM remains functional even if individual hotplug operations fail
- **Regression Testing:**
  - This test should be run regularly to catch regressions
  - Include in nightly or weekly automated test runs
  - Compare metrics across test runs to identify performance trends

---

## Appendix A: Common Commands Reference

### VirtualMachine CPU Operations

```bash
# Get VM CPU configuration
oc get vm <vm-name> -n <namespace> -o jsonpath='{.spec.template.spec.domain.cpu}' | jq .

# Update VM sockets (hotplug)
oc patch vm <vm-name> -n <namespace> --type merge -p '{"spec":{"template":{"spec":{"domain":{"cpu":{"sockets":<count>}}}}}}'

# Update VM maxSockets
oc patch vm <vm-name> -n <namespace> --type merge -p '{"spec":{"template":{"spec":{"domain":{"cpu":{"maxSockets":<count>}}}}}}'

# Get VMI CPU status
oc get vmi <vm-name> -n <namespace> -o jsonpath='{.status.guestOSInfo.topology}' | jq .
```

### Guest OS Verification Commands

```bash
# Check CPU count
virtctl ssh <user>@<vm-name> -n <namespace> "nproc"

# Detailed CPU information
virtctl ssh <user>@<vm-name> -n <namespace> "lscpu"

# Check online CPUs
virtctl ssh <user>@<vm-name> -n <namespace> "lscpu | grep 'On-line CPU(s)'"

# CPU info from /proc
virtctl ssh <user>@<vm-name> -n <namespace> "cat /proc/cpuinfo"
```

### Diagnostic Commands

```bash
# Check VM events
oc get events -n <namespace> --field-selector involvedObject.name=<vm-name> --sort-by='.lastTimestamp'

# Get virt-launcher pod
oc get pod -n <namespace> -l kubevirt.io/vm=<vm-name>

# Check domain XML
LAUNCHER_POD=$(oc get pod -n <namespace> -l kubevirt.io/vm=<vm-name> -o jsonpath='{.items[0].metadata.name}')
oc exec -n <namespace> "$LAUNCHER_POD" -c compute -- virsh dumpxml 1

# Check VMI conditions
oc get vmi <vm-name> -n <namespace> -o jsonpath='{.status.conditions}' | jq .
```

---

## Appendix B: Validation Matrix

| Validation Point | Expected Behavior | Test Scenario(s) |
|:-----------------|:------------------|:-----------------|
| MaxSockets calculation | maxSockets <= max vCPUs allowed | TS-01 |
| Initial CPU config | Guest shows correct initial CPU count | TS-01, TS-04 |
| Hotplug within limit | CPUs added successfully, guest recognizes | TS-02, TS-04 |
| Hotplug at limit | Can reach but not exceed maximum | TS-02, TS-04 |
| Hotplug beyond limit | Operation blocked or rejected | TS-02, TS-03, TS-04 |
| Error messages | Clear, actionable errors for violations | TS-03 |
| Invalid configs | API rejects invalid CPU configurations | TS-03 |
| Guest OS stability | VM remains stable at maximum CPUs | TS-04 |
| VM lifecycle | Stop/restart works with max CPUs | TS-04 |
| VMI status | VMI maintains healthy status throughout | TS-02, TS-04 |

---

## Appendix C: Test Environment Setup

### Prerequisites Installation

```bash
# Create test namespace
oc create namespace test-cpu-hotplug

# Verify OpenShift Virtualization operator
oc get csv -n openshift-cnv | grep kubevirt-hyperconverged

# Check CPU virtualization on nodes
oc debug node/<node-name> -- chroot /host lscpu | grep Virtualization

# Install virtctl (if not already installed)
export VERSION=v1.3.0
wget https://github.com/kubevirt/kubevirt/releases/download/${VERSION}/virtctl-${VERSION}-linux-amd64
chmod +x virtctl-${VERSION}-linux-amd64
sudo mv virtctl-${VERSION}-linux-amd64 /usr/local/bin/virtctl
```

### Feature Gate Verification

```bash
# Check if CPU hotplug feature gate is enabled
oc get kubevirt -n openshift-cnv kubevirt-kubevirt-hyperconverged -o jsonpath='{.spec.configuration.developerConfiguration.featureGates}' | grep -i cpu
```

---

## Appendix D: Troubleshooting Guide

### Issue: Guest OS doesn't recognize hotplugged CPUs

**Possible Causes:**
- Guest OS doesn't support CPU hotplug
- CPUs are offline and need manual onlining
- Delay in ACPI event processing

**Troubleshooting Steps:**
```bash
# Check if CPUs are offline
virtctl ssh <user>@<vm-name> -n <namespace> "lscpu | grep 'Off-line CPU(s)'"

# Manually online CPUs (if needed)
virtctl ssh <user>@<vm-name> -n <namespace> "echo 1 | sudo tee /sys/devices/system/cpu/cpu*/online"

# Check dmesg for ACPI events
virtctl ssh <user>@<vm-name> -n <namespace> "dmesg | grep -i cpu"
```

### Issue: Hotplug operation times out

**Possible Causes:**
- libvirt/QEMU issue
- Resource constraints on host
- VMI not responsive

**Troubleshooting Steps:**
```bash
# Check virt-launcher pod logs
LAUNCHER_POD=$(oc get pod -n <namespace> -l kubevirt.io/vm=<vm-name> -o jsonpath='{.items[0].metadata.name}')
oc logs -n <namespace> "$LAUNCHER_POD" -c compute

# Check node resources
oc describe node <node-name> | grep -A 10 "Allocated resources"

# Check VMI events
oc get events -n <namespace> --field-selector involvedObject.name=<vm-name>
```

### Issue: MaxSockets validation not working

**Possible Causes:**
- Webhook not configured
- API version mismatch
- Bug in validation logic

**Troubleshooting Steps:**
```bash
# Check webhook configuration
oc get validatingwebhookconfigurations | grep virt

# Check kubevirt-api-server logs
oc logs -n openshift-cnv deployment/virt-api

# Verify KubeVirt version
oc get kubevirt -n openshift-cnv -o jsonpath='{.status.observedKubeVirtVersion}'
```

---

## Sign-off and Approval

This Software Test Description requires review and approval:

- **Author:** [QE Engineer Name]
- **Reviewers:**
  - [QE Team Lead]
  - [Compute SIG Representative]
  - [Automation Engineer]
- **Approvers:**
  - [QE Manager]
  - [Product Owner]

**Review Date:** _______________
**Approval Date:** _______________

---

**Document Version:** 1.0
**Last Updated:** 2026-02-04
**Next Review Date:** [30 days after approval]
