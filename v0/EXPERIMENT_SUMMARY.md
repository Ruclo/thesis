# AI-Powered E2E Test Generation: Phase 0 Baseline Experiments

**Author:** Michal Vavrinec
**Date:** January 2026

---

## Executive Summary

This document summarizes the baseline experiments for my bachelor's thesis: **"Bridging the Gap: An Agentic Architecture for Translating Natural Language Test Plans into Executable E2E Code."**

The goal is to evaluate whether state-of-the-art Large Language Models (LLMs) can generate compilable, compliant End-to-End tests for OpenShift Virtualization directly from written Software Test Plans (STPs).

## Research Question
Can AI agents translate natural language test plans into executable E2E test code for complex enterprise software?

## Research Methodology
Naive LLM generation using Claude Code which was instructed to study the repo docs and library functions in the prompt itself.

---

## Experimental Structure

### Repository Layout
```
thesis/
├── README.md                  # Project overview
└── v0/                        # Phase 0: Baseline experiments
    ├── experiment_1_common_instancetypes/
    ├── experiment_2_vnc_screenshot/
    ├── experiment_3_reset_vm/
    ├── experiment_4_snapshot_failure/
    └── experiment_5_video_config/
```

### Standard Experiment Structure
Each experiment directory contains:
- `prompt.md` - The exact input prompt (STP + instructions)
- `claude.log` - Full conversation log with Claude Code CLI
- `changes.patch` - Git diff showing file placement in the repository
- `test_run.log` - Pytest execution logs (the "result")
- `notes.txt` - Summary of failures and observations

---

## Workflow & Methodology

### Test Generation Workflow
1. **Prepare STP**: Select a real-world Software Test Plan from OpenShift Virtualization Jira tickets
2. **Embed STP into Prompt**: Add standardized instructions for context exploration and code generation
3. **Run Claude Code CLI**: Execute the AI agent with the prepared prompt
4. **Save Artifacts**: Log the full conversation (`claude.log`) and code changes (`changes.patch`)
5. **Execute Tests**: Run pytest on a local CRC (CodeReady Containers) cluster
6. **Capture Results**: Save pytest output to `test_run.log`
7. **Analyze & Document**: Record errors, failures, and insights in `notes.txt`

### Test Environment
- **Platform**: Local CRC (OpenShift Local) cluster

---

## Experiment Results

### Experiment 1: Common Instancetypes Deployment
**Feature**: [CNV-61256] Unable to Disable Common-Instancetypes Deployment from HCO
**Status**: ⚠️ Partial Failure

**Test Scenarios**:
- Disable common-instancetypes via HCO CR
- Enable common-instancetypes
- Verify default behavior
- Test setting persistence

**Key Issues**:
- TimeoutExpiredError: Tests timed out waiting for common-instancetype resources to be deleted (300s timeout)
- Generated code correctly identified fixtures and utilities
- Test logic appears sound but cluster behavior didn't match expectations - A field in the STP did not match the field
  which was later implemented.

**Lines of Test Output**: 1,533

---

### Experiment 2: VNC Console Screenshot Stability
**Feature**: [CNV-60117] VNC Console Disconnect Due to Thumbnail/Full Screen Competition
**Status**: ❌ Multiple Failures

**Test Scenarios**:
- VNC stability with concurrent thumbnail
- Screenshot API without VNC connection
- Screenshot quality verification
- Thumbnail updates without VNC impact

**Key Issues**:
- **AttributeError**: Attempted to access `.child` attribute of `vnc_connection` object (doesn't exist)
- Referenced unknown `win` preference variable
- **pytest.mark.tier1**: Unknown pytest marker warning (custom marks need registration)

**Attempts**: 2 test runs (`test_run.log`, `test_run2.log`)
**Lines of Test Output**: 7,125 + 5,213 = 12,338

---

### Experiment 3: VM Reset Functionality
**Feature**: [VIRTSTRAT-357] GA: Force/hard reset
**Status**: ⚠️ Mixed Results

**Test Scenarios**:
- Reset running VMI via API
- Reset via virtctl command
- VMI UID persistence after reset
- RBAC permissions validation
- Error handling for non-running VMs

**Key Issues**:
- **ValueError**: "too many values to unpack (expected 2)" - `run_virtctl_command` returned 3 values instead of 2
- **RBAC Test Failure**: Test environment had overprivileged user (could perform actions they shouldn't be able to)
- **Timeout**: VM failed to boot within 120 seconds after reset
- **ApiException vs NotFoundError**: Test expected `NotFoundError` but received `ApiException(404)` instead

**Lines of Test Output**: 3,725

---

### Experiment 4: Snapshot Restore with RerunOnFailure
**Feature**: [CNV-63819] VM Snapshot Restore Stuck with runStrategy RerunOnFailure
**Status**: ❌ Critical Failure

**Test Scenarios**:
- Snapshot restore with RerunOnFailure run strategy
- VirtualMachineRestore status verification
- VM auto-start prevention during restore
- Complete workflow with data validation

**Key Issues**:
- **AttributeError**: Referenced invalid `RunStrategy` enum value while creating VM
- Code attempted to use a RunStrategy that doesn't exist in the API

**Lines of Test Output**: 257 (early termination)

---

### Experiment 5: Video Device Configuration
**Feature**: [CNV-70742] [Tech Preview] Allow VM-owners to explicitly set video device type
**Status**: ❌ Collection Error

**Test Scenarios**:
- VideoConfig feature gate validation
- VM creation with different video types (virtio, vga, bochs, cirrus, ramfb)
- Architecture-specific video type support
- Firmware configuration (EFI/BIOS)
- Persistence across restart/migration

**Key Issues**:
- **Collection Error**: Pytest failed to collect tests
- Function used fixture `golden_image_data_source_for_test_scope_class` that wasn't properly declared
- Test collection failed before any tests could run

**Lines of Test Output**: 224 (collection phase only)

---

## Error Category Analysis


1. **AttributeError** (Experiments 2, 4)
   - Accessing non-existent object attributes
   - Incorrect enum values
   - Pre-commit only checks syntax, not runtime behavior

2. **ValueError** (Experiment 3)
   - Incorrect unpacking of function return values
   - Type mismatches at runtime
   - Pre-commit can't validate function signatures from external libraries

3. **TimeoutExpiredError** (Experiment 1)
   - Test logic timeouts
   - Cluster behavior doesn't match expectations
   - Pre-commit has no knowledge of cluster state

4. **API Mismatches** (Experiment 3)
   - Expected `NotFoundError` but got `ApiException(404)`
   - Different exception types from Kubernetes client
   - Pre-commit can't validate against live API behavior

5. **Fixture Issues** (Experiment 5)
   - Missing or incorrectly scoped pytest fixtures
   - Dependency injection problems
   - Pre-commit can't resolve pytest's dynamic fixture system

After testing with pre-commit, pre-commit was not able to catch many of these errors.
---

## Success Metrics

### Code Generation Quality

| Metric | Result |
|--------|--------|
| **Proper File Placement** | 5/5 (100%) - All tests placed in correct directories |
| **Used Existing Utilities** | 5/5 (100%) - No hallucinated functions |
| **Pytest Markers Applied** | 5/5 (100%) - Polarion IDs, tiers properly marked |
| **Docstrings & Documentation** | 5/5 (100%) - Comprehensive documentation |
| **Tests Executed Successfully** | 0/5 (0%) - All had runtime/environment issues |

---

## Key Findings

### Strengths of AI-Generated Tests

1. **Correct File Placement**: Tests placed in appropriate directories matching repository conventions

2. **Proper Structure**: All tests follow pytest conventions with:
   - Class-based organization
   - Proper fixture usage
   - Correct import statements
   - Google-style docstrings

### Weaknesses & Challenges

1. **Runtime Error Blind Spots**:
   - Cannot validate against live API behavior
   - No understanding of object structure at runtime
   - Guesses at function signatures and return values

2. **API Version Mismatches**:
   - Exception type mismatches (Experiment 3)
   - Enum value errors (Experiment 4)

3. **Fixture Complexity**:
   - Struggled with pytest's dynamic fixture system
   - Incorrect fixture scoping (Experiment 5)

4. **Zero Test Execution Success**: Despite 80% compilable code, **0% of test suites executed successfully** due to runtime issues

---

## Limitations of Pre-commit Hooks

Pre-commit hooks are valuable for catching syntax and style issues but **fundamentally cannot detect** the types of errors encountered in these experiments:

### What Pre-commit Catches
- Missing imports
- Syntax errors (missing colons, unmatched parentheses)
- PEP 8 violations (formatting)
- Unused variables (with flake8)
- Basic type errors (with mypy)

### What Pre-commit Misses
- **AttributeError**: Object doesn't have the expected attribute
- **ValueError**: Function returns wrong number of values
- **API Exceptions**: Wrong exception type for API calls
- **Fixture Errors**: pytest fixture scope/dependency issues
- **Timeout Issues**: Test environment performance problems

### The Gap
**Pre-commit operates at compile-time; these errors occur at runtime.**
---

## Conclusions

### Research Contributions

1. **Baseline Established**: Phase 0 demonstrates that LLMs can generate **structurally correct** E2E tests.

2. **The Gap Identified**:
   - 80% of code compiles correctly
   - 0% of test suites execute successfully
   - The gap is **runtime behavior**, not syntax

3. **Pre-commit Limitations Confirmed**: Static analysis tools cannot catch the types of errors that prevent test execution

---

## References

- **Thesis Repository**: `github.com/Ruclo/thesis`
- **Test Repository**: `github.com/RedHatQE/openshift-virtualization-tests`
- **Cluster**: Local CRC (CodeReady Containers)
- **AI Tool**: Claude Code CLI (Sonnet 4.5)
- **Test Framework**: pytest 9.0.2

---

## Questions for Feedback

1. **Methodology**: Is the Phase 0 baseline approach (zero context) valuable?

2. **Error Classification**: Are the error categories (AttributeError, ValueError, etc.) useful for analyzing AI limitations?

3. **Success Metrics**: What additional metrics would help evaluate AI-generated test quality?

4. **Phase 1 Priorities**: Should the input be solely STPs, STDs or both? How do I provide more context to the AI? Is an intermediate format necessary?

5. **Workflow**: Do you have any ideas for improving my workflow in the future?
---

**Document Version**: 1.0
**Last Updated**: January 27, 2026
**Status**: Ready for Review
