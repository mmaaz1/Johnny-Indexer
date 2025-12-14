# Type Hints Implementation Checklist

## Phase 1: Foundation (Quick Wins) ✅ COMPLETED

- [x] **Set up type checking configuration**
  - [x] Add pyright config to `pyproject.toml` or create one
  - [x] Set `typeCheckingMode` to `basic` initially
  - [x] Configure ignore patterns for third-party libs if needed

- [x] **Type the `File` class** (`utils/file/file.py`)
  - [x] Add parameter types to all methods
  - [x] Add return types to all methods
  - [x] Import necessary types from `typing` module
  - [x] Document special return types (Optional, Union, etc.)
  - [x] Resolved circular import issue with `ProperIndexType` using `TYPE_CHECKING`
  - [x] Added TODO comment for future refactoring

- [x] **Type `ConfigHelper`** (`utils/config/config_helper.py`)
  - [x] Add parameter and return types
  - [x] Define type for config dict (Dict[str, Any])
  - [x] Simple, straightforward module - quick to complete

- [x] **Run type checker on Phase 1 modules**
  - [x] Verify no errors in File class
  - [x] Verify no errors in ConfigHelper
  - [x] Fix any issues that arise
  - [x] All checks pass: 0 errors, 0 warnings

### Phase 1 Summary

**Completed:**
- Created `pyproject.toml` with pyright configuration
- Created `requirements.txt` with dependencies (pyright, pyyaml, pytest)
- Set up virtual environment (`venv/`)
- Fully typed File class with proper type annotations
- Typed ConfigHelper with parameter and return types
- Resolved circular import using TYPE_CHECKING pattern
- Updated DEVELOPMENT.md with setup instructions

**Key Implementation Details:**
- File class attributes: `name: str`, `dir_path: str`, `level: int`
- Default level changed from `None` to `0` for better type safety
- Used `TYPE_CHECKING` to handle circular imports while maintaining type safety
- Documented tech debt and provided pattern for future developers

## Phase 2: Core Utilities (High Priority)

- [x] **Type `IndexHelper`** (`utils/index/index_helper.py`)
  - [x] Add all parameter types
  - [x] Add all return types
  - [x] Use File types from Phase 1
  - [x] Define types for index operations (List[str], etc.)
  - [x] Handle circular imports using TYPE_CHECKING
  - [x] All checks pass: 0 errors, 0 warnings

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
