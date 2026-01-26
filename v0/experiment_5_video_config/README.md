# VideoConfig Feature Tests

This directory contains tests for the VideoConfig feature gate in OpenShift Virtualization, which allows VM owners to explicitly set the video device type.

## Feature Overview

The VideoConfig feature enables configuration of `spec.template.spec.domain.devices.video.type` in VirtualMachine specifications. Supported video types include:
- `virtio` - VirtIO GPU (better performance, multi-head support)
- `vga` - VGA graphics adapter (legacy, wide compatibility)
- `bochs` - Bochs display device (efficient for EFI)
- `cirrus` - Cirrus Logic graphics (legacy)
- `ramfb` - RAM framebuffer (minimal)

## Test Coverage

### Feature Gate Tests (P0 - Gating)
- `test_videoconfig_feature_gate_enabled_by_default` - Verify VideoConfig is enabled by default
- `test_hco_videoconfig_default_value` - Verify HCO has videoConfig=true by default
- `test_hco_videoconfig_propagates_to_kubevirt` - Verify HCO propagates feature gate to KubeVirt CR

### Basic Functionality Tests (P0 - Gating)
**Class: TestVideoConfigBasicFunctionality**
- `test_vm_with_virtio_video_type` (CNV-11301) - VM creation with virtio video device
- `test_vm_with_vga_video_type` (CNV-11302) - VM creation with VGA video device
- `test_vm_with_bochs_video_type` (CNV-11303) - VM creation with bochs video device
- `test_vm_with_cirrus_video_type` (CNV-11304) - VM creation with cirrus video device
- `test_vm_with_ramfb_video_type` (CNV-11305) - VM creation with ramfb video device
- `test_vm_without_video_type_uses_default` (CNV-11306) - Default behavior when video.type not specified

### Firmware Configuration Tests (P1)
**Class: TestVideoConfigEFIBIOS**
- `test_efi_vm_with_bochs_video_type` (CNV-11307) - EFI VM with bochs video
- `test_bios_vm_with_vga_video_type` (CNV-11308) - BIOS VM with VGA video

### Persistence Tests (P1)
**Class: TestVideoConfigPersistence**
- `test_video_type_persists_across_vm_restart` (CNV-11309) - Video config preserved after VM restart
- `test_video_type_persists_across_live_migration` (CNV-11310) - Video config preserved after live migration

### Windows VM Tests (P1)
**Class: TestVideoConfigWindows**
- `test_windows_vm_with_vga_video_type` (CNV-11311) - Windows VM with VGA video device

### Negative Tests (P1)
**Class: TestVideoConfigNegative**
- `test_invalid_video_type_rejected` (CNV-11312) - Invalid video type validation
- `test_vm_creation_with_feature_gate_disabled` (CNV-11313) - Backward compatibility when FG disabled

## Running Tests

### Run all VideoConfig tests:
```bash
pytest tests/virt/node/video_config/
```

### Run only gating tests:
```bash
pytest tests/virt/node/video_config/ -m gating
```

### Run specific test class:
```bash
pytest tests/virt/node/video_config/test_video_config.py::TestVideoConfigBasicFunctionality
```

### Run specific test:
```bash
pytest tests/virt/node/video_config/test_video_config.py::TestVideoConfigBasicFunctionality::test_vm_with_virtio_video_type
```

### Run with Polarion marker:
```bash
pytest tests/virt/node/video_config/ -m "polarion('CNV-11301')"
```

## Test Requirements

### Infrastructure
- Multi-node cluster for migration tests (automatically skipped on single-node)
- Common CPU model for migration tests (automatically skipped if not available)
- Hardware virtualization enabled (VT-x/AMD-V)

### Test Images
- RHEL latest golden image (for most tests)
- Windows latest golden image (for Windows-specific tests)

### Pytest Markers
- `@pytest.mark.gating` - Gating test (runs in CI)
- `@pytest.mark.high_resource_vm` - Requires high resources (Windows VMs)
- `@pytest.mark.polarion("CNV-XXXXX")` - Linked to Polarion test case

## Architecture-Specific Support

### AMD64/x86_64
- **BIOS**: virtio, vga (default), bochs, cirrus, ramfb
- **EFI**: virtio, vga, bochs (default), cirrus, ramfb

### ARM64/aarch64
- Supports: virtio (default), ramfb
- **Note**: Limited test infrastructure availability

### s390x
- Supports: virtio only (default)
- **Note**: Limited test infrastructure availability

## Known Limitations

1. **Multi-head configuration**: Not exposed via VideoConfig FG in this release
2. **Driver requirements**: virtio requires virtio-gpu drivers in guest OS
3. **cirrus**: Legacy device, not recommended for new deployments
4. **Tech Preview**: Feature may change in future releases

## Test Fixtures

### From conftest.py
- `video_config_vm` - VM instance with custom video configuration (class scope)
- `video_config_vm_for_migration` - VM instance for migration tests (function scope)

### From tests/conftest.py
- `admin_client` - Admin Kubernetes client
- `unprivileged_client` - Unprivileged Kubernetes client
- `namespace` - Test namespace with auto-cleanup
- `hco_namespace` - HCO namespace
- `hyperconverged_resource_scope_function` - HCO resource (function scope)
- `kubevirt_resource_scope_session` - KubeVirt resource (session scope)
- `kubevirt_feature_gates` - List of enabled KubeVirt feature gates
- `golden_image_data_source_for_test_scope_class` - Golden image data source (class scope)
- `golden_image_data_volume_template_for_test_scope_class` - DV template (class scope)

## Utility Functions

### get_video_model_from_domain_xml(vm)
Extracts video model type from VM domain XML.

**Returns**: str (e.g., 'vga', 'virtio', 'bochs')

### create_vm_spec_with_video_type(video_type)
Creates VM spec dict with specified video device type.

**Args**: video_type (str | None) - Video device type or None for default
**Returns**: dict - VM spec with video configuration

## Related Documentation

- [KubeVirt Enhancement VEP-87](https://github.com/kubevirt/enhancements/pull/87)
- Jira Epic: [CNV-70742](https://issues.redhat.com/browse/CNV-70742)
- Test Plan: `../thesis/v0/experiment_5_video_config/prompt.md`

## Maintainer

- QE Owner: Akriti Gupta
- Owning SIG: sig-compute
