# Type Hints Implementation Checklist

## Phase 1: Foundation (Quick Wins)

- [ ] **Set up type checking configuration**
  - [ ] Add pyright config to `pyproject.toml` or create one
  - [ ] Set `typeCheckingMode` to `basic` initially
  - [ ] Configure ignore patterns for third-party libs if needed

- [ ] **Type the `File` class** (`utils/file/file.py`)
  - [ ] Add parameter types to all methods
  - [ ] Add return types to all methods
  - [ ] Import necessary types from `typing` module
  - [ ] Document special return types (Optional, Union, etc.)

- [ ] **Type `ConfigHelper`** (`utils/config/config_helper.py`)
  - [ ] Add parameter and return types
  - [ ] Define type for config dict (Dict[str, Any])
  - [ ] Simple, straightforward module - quick to complete

- [ ] **Run type checker on Phase 1 modules**
  - [ ] Verify no errors in File class
  - [ ] Verify no errors in ConfigHelper
  - [ ] Fix any issues that arise

## Phase 2: Core Utilities (High Priority)

- [ ] **Type `IndexHelper`** (`utils/index/index_helper.py`)
  - [ ] Add all parameter types
  - [ ] Add all return types
  - [ ] Use File types from Phase 1
  - [ ] Define types for index operations (List[str], Dict, etc.)

- [ ] **Type `ObsidianFixer`** (`utils/obsidian/obsidian_fixer.py`)
  - [ ] Add types to all methods
  - [ ] File operation signatures
  - [ ] String replacement return types

- [ ] **Type `IndexFixer`** (`utils/index/index_fixer.py`)
  - [ ] Add parameter and return types
  - [ ] Index modification signatures

- [ ] **Run type checker on Phase 2 modules**
  - [ ] Verify no errors
  - [ ] Update configuration if needed

## Phase 3: Complex Logic (Can Be Gradual)

- [ ] **Type `IndexFormatConfig`** (`utils/index/index_format_config.py`)
  - [ ] Define TypedDict for index portion dicts
  - [ ] Create Union types for enum values
  - [ ] Type the Proper class with its equality logic
  - [ ] Type regex pattern fields
  - [ ] This is the most complex module - may require iterations

- [ ] **Type entry points**
  - [ ] `create_jdex.py` - Type all functions and ProposedChange class
  - [ ] `fix_indexes.py` - Type main function and BFS algorithm
  - [ ] Consider dataclass for ProposedChange with types

- [ ] **Type related scripts**
  - [ ] `related_scripts/commit_daily.py` - If still in use

- [ ] **Run type checker on Phase 3 modules**
  - [ ] Verify no errors
  - [ ] Fix any complex type issues

## Phase 4: Testing & Documentation

- [ ] **Type test file** (`tests/test_index_helper.py`)
  - [ ] Add types to test functions
  - [ ] Verify test coverage still passes

- [ ] **Add type checking to CI/CD** (if applicable)
  - [ ] Add pyright/mypy to pre-commit hooks
  - [ ] Add to GitHub Actions or similar

- [ ] **Document typing decisions**
  - [ ] Note any `# type: ignore` comments and why
  - [ ] Document complex types (Union, TypedDict, etc.)
  - [ ] Create typing guide for new contributors

## Notes

- **Start with Phase 1** - File class is the foundation, everything depends on it
- **Use `TYPE_CHECKING`** if circular imports arise
- **Keep return types explicit** - helps with IDE autocomplete
- **Consider using `Optional[]`** carefully - be explicit about None cases
- **Document the `Proper` class** - it has unusual equality logic
- **Watch for duck typing** - some methods expect file-like objects
