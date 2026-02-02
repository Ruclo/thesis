Act as a Senior SDET. I am going to provide you with a **Software Test Plan (STP)**. Your task is to translate this plan into an executable Python test file using `pytest`.

You are currently in the root of the openshift-virtualization-tests repository. You must follow this strict three-phase workflow:

**Phase 1: Context Exploration**
1.  **Scan Documentation:** Read `docs/` to understand testing conventions.
2.  **Map Utilities:** Analyze `libs/` and `utilities/`. specificially look for:
3.  **Check Precedents:** Look at existing tests in `tests/` to see valid import patterns and fixture usage.

**Phase 2: Code Generation (Drafting)**
* Generate a single `.py` file implementing the scenarios from the STP provided below.
* **Strict Constraint:** Do not hallucinate utilities. You MUST use the exact class names, method signatures, and constants found during Phase 1. If a helper is missing, implement it locally using the base Kubernetes client.

**Phase 3: Validation & Self-Healing (Pyright Loop)**
* After generating the draft, **you must run `uv run pyright <test_file_path>` on the new file** to check for type safety and attribute errors.
* **If `pyright` reports errors:**
    1.  Read the error output carefully.
    2.  Re-read the actual source code of the utility/class involved to find the correct attribute or method.
    3.  **Apply the fix** to your code by editing the test file.
    4.  Run `pyright <test_file_path>` again.
* **Repeat this loop until `pyright` passes with 0 errors.** No attempt limit - keep iterating until clean.

**Input STP:**
${STP_CONTENT}