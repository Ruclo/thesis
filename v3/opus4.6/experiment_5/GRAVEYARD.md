# GRAVEYARD - Test Generation Lessons Learned

This file documents mistakes made during automated test generation and how to avoid them.
It is read during the exploration phase to prevent repeating past errors.

---

## Entry: StorageProfile status.snapshotClass not cleared by CDI when spec is emptied

**Category**: TimeoutError
**Date**: 2026-02-17
**Test**: tests/storage/snapshots/test_storage_profile_snapshot_class.py::TestStorageProfileSnapshotClassFallback::test_snapshot_falls_back_to_label_based_selection

### What Went Wrong
The `storage_profile_without_snapshot_class` fixture used ResourceEditor to set `spec.snapshotClass` to `""` and then waited (via TimeoutSampler) for `status.snapshotClass` to become falsy. The CDI controller does not clear `status.snapshotClass` when `spec.snapshotClass` is set to empty string. CDI may auto-populate `status.snapshotClass` via VolumeSnapshotClass driver matching regardless of the spec value. The wait timed out after 60 seconds.

### Wrong Code
```python
@pytest.fixture()
def storage_profile_without_snapshot_class(admin_client, snapshot_storage_class_name_scope_module):
    storage_profile = StorageProfile(
        name=snapshot_storage_class_name_scope_module,
        client=admin_client,
    )
    with ResourceEditor(
        patches={storage_profile: {"spec": {"snapshotClass": ""}}}
    ):
        for sample in TimeoutSampler(
            wait_timeout=TIMEOUT_1MIN,
            sleep=TIMEOUT_5SEC,
            func=lambda: not storage_profile.snapshotclass,
        ):
            if sample:
                break
        yield storage_profile
```

### Correct Code
```python
@pytest.fixture()
def storage_profile_without_snapshot_class(admin_client, snapshot_storage_class_name_scope_module):
    storage_profile = StorageProfile(
        name=snapshot_storage_class_name_scope_module,
        client=admin_client,
    )
    LOGGER.info(
        f"Clearing spec.snapshotClass on StorageProfile "
        f"{snapshot_storage_class_name_scope_module}"
    )
    with ResourceEditor(
        patches={storage_profile: {"spec": {"snapshotClass": ""}}}
    ):
        yield storage_profile
```

### Lesson Learned
CDI's StorageProfile `status.snapshotClass` is managed by the CDI controller and may be auto-populated based on VolumeSnapshotClass driver matching, independent of `spec.snapshotClass`. Setting `spec.snapshotClass` to `""` updates the spec synchronously (via ResourceEditor's `update()` call) but does NOT cause CDI to clear `status.snapshotClass`. Do not wait for `status.snapshotClass` to change when clearing the spec field.

### How to Avoid
When modifying StorageProfile `spec.snapshotClass` via ResourceEditor, do NOT wait for `status.snapshotClass` to reconcile when clearing the field. The `spec` update is synchronous. Only use TimeoutSampler to wait for `status.snapshotClass` when SETTING the field to a specific non-empty value (CDI does reconcile spec-to-status for non-empty values).

---
