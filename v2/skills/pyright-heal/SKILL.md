# Skill: /pyright-heal

**Purpose**: Universal Python type checker and self-healing fixer for ANY Python file

## Input
- **Required**: Path to Python file (`.py` or `.ipynb`)
- **Optional**: `--max-iterations N` - Maximum fix attempts (default: 10)
- **Optional**: `--strict` - Use strict type checking mode

## Output
- **Modified File**: Same file, edited in-place
- **Exit Code**: 0 if clean, 1 if max iterations reached with errors
- **Log**: Summary of fixes applied

## Implementation

### Iterative Healing Loop

```
1. RUN pyright on file
2. IF pyright returns 0 errors:
     RETURN success
3. ELSE:
     a. PARSE error output
     b. FOR each error:
          - READ source file at error location
          - ANALYZE root cause
          - DETERMINE fix strategy
          - APPLY fix via Edit tool
     c. INCREMENT iteration counter
     d. IF iteration > max_iterations:
          RETURN failure with error report
     e. GOTO step 1 (re-run pyright)
```

### Error Categories & Fix Strategies

#### 1. **Attribute/Method Not Found**
```
Error: "VirtualMachine" has no attribute "reset"
Fix Strategy:
  1. READ actual class definition
  2. FIND correct attribute name
  3. UPDATE code to use correct attribute
```

#### 2. **Import Errors**
```
Error: Cannot find module "ocp_resources.vm"
Fix Strategy:
  1. SEARCH for correct module path
  2. UPDATE import statement
  3. If not found, REMOVE import and find alternative
```

#### 3. **Type Mismatches**
```
Error: Expected "str", got "int"
Fix Strategy:
  1. ANALYZE context
  2. ADD type conversion OR
  3. UPDATE type annotation
```

#### 4. **Undefined Variables**
```
Error: "foo" is not defined
Fix Strategy:
  1. SEARCH for variable definition
  2. ADD missing import OR
  3. DEFINE variable locally
```

#### 5. **Argument Mismatches**
```
Error: Too many arguments for "method"
Fix Strategy:
  1. READ actual method signature
  2. ADJUST arguments to match
  3. UPDATE keyword args if needed
```

## Algorithm

```python
iteration = 0
max_iterations = args.max_iterations ?? 10

while iteration < max_iterations:
    # Run pyright
    result = bash(f"uv run pyright {file_path}")

    if "0 errors" in result:
        log(f"✓ Pyright clean after {iteration} iterations")
        return SUCCESS

    # Parse errors
    errors = parse_pyright_output(result)

    for error in errors:
        # Read context around error
        file_content = read_file(file_path,
                                  offset=error.line - 5,
                                  limit=10)

        # Determine fix
        fix = analyze_and_generate_fix(error, file_content)

        # Apply fix
        edit_file(file_path,
                  old_string=error.context,
                  new_string=fix.new_code)

        log(f"  Fix {iteration}.{error.id}: {fix.description}")

    iteration++

log(f"✗ Failed to heal after {max_iterations} iterations")
return FAILURE
```

## Fix Decision Tree

```
pyright error
    ├─ "has no attribute"
    │   └─→ Read actual class → Find correct attribute → Edit
    │
    ├─ "Cannot find module"
    │   └─→ Search repo → Find correct import → Edit
    │
    ├─ "is not defined"
    │   └─→ Search for definition → Add import OR define → Edit
    │
    ├─ "Type mismatch"
    │   └─→ Analyze context → Add conversion OR fix annotation → Edit
    │
    ├─ "Argument mismatch"
    │   └─→ Read signature → Adjust call → Edit
    │
    └─ "Unknown error"
        └─→ Log warning → Skip (manual review needed)
```

## Example Session

**Input File** (`test_example.py`):
```python
from ocp_resources.vm import VirtualMachine  # Wrong import path

def test_vm_reset(namespace):
    vm = VirtualMachine(name="test")
    vm.reset()  # Method doesn't exist
```

**Iteration 1**:
```
$ uv run pyright test_example.py
Error: Cannot find module "ocp_resources.vm"

[FIX] Search for correct import...
[FOUND] ocp_resources.virtual_machine.VirtualMachine
[EDIT] Change import path
```

**Iteration 2**:
```
$ uv run pyright test_example.py
Error: "VirtualMachine" has no attribute "reset"

[FIX] Read VirtualMachine class definition...
[FOUND] Correct method is vm.vmi.reset()
[EDIT] Update method call
```

**Iteration 3**:
```
$ uv run pyright test_example.py
0 errors, 0 warnings, 0 informations

[SUCCESS] File is type-safe ✓
```

**Final File**:
```python
from ocp_resources.virtual_machine import VirtualMachine

def test_vm_reset(namespace):
    vm = VirtualMachine(name="test")
    vm.vmi.reset()
```

## Output Format

```
🔧 Pyright Self-Healing: test_example.py

Iteration 1:
  ✓ Fixed import path: ocp_resources.vm → ocp_resources.virtual_machine

Iteration 2:
  ✓ Fixed method call: vm.reset() → vm.vmi.reset()

Result: ✓ Clean (2 iterations, 2 fixes applied)
```

## Usage

```bash
# Standard usage
/pyright-heal tests/test_new_feature.py

# With max iterations limit
/pyright-heal utilities/helper.py --max-iterations 5

# Strict mode
/pyright-heal conftest.py --strict

# Works on ANY Python file!
/pyright-heal scripts/automation.py
/pyright-heal fixtures/base_fixtures.py
/pyright-heal utilities/custom_helper.py
```

## Constraints

### 1. No Code Deletion
- Never delete functionality to "fix" errors
- If method doesn't exist, find the correct one
- Preserve original intent

### 2. Prefer Real Solutions
- Don't add `# type: ignore` comments
- Don't use `Any` types unless necessary
- Find actual fixes, not workarounds

### 3. Validate Fixes
- Must re-run pyright after each fix
- Don't assume fix worked
- Track iteration count to prevent infinite loops

### 4. Preserve Semantics
- Fixes must maintain original behavior
- Don't change test logic
- Only fix type/attribute errors

## Edge Cases

### Unfixable Errors
If error cannot be auto-fixed:
```
⚠ Could not auto-fix error at line 45:
  "ComplexType has incompatible generic variance"

Action: Skipping, manual review required
```

### Max Iterations Reached
```
✗ Failed to heal after 10 iterations
Remaining errors:
  - Line 23: Type inference issue
  - Line 45: Complex generic variance

Suggestion: Review errors manually or increase --max-iterations
```

### File Not Found
```
ERROR: File not found: tests/missing.py
HINT: Provide valid Python file path
```

## Reusability
**VERY HIGH** - Universal Python fixer:
- ✅ Test files
- ✅ Utility modules
- ✅ Fixtures
- ✅ Scripts
- ✅ Configuration files
- ✅ Any `.py` in the repository

This skill is **completely generic** and useful beyond just test generation!

## Dependencies
- Bash tool (run pyright)
- Read tool (read file context)
- Edit tool (apply fixes)
- `uv run pyright` must be available in environment
