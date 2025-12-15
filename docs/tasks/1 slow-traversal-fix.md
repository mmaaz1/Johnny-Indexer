# Slow Traversal Fix - Reference Scanning Optimization

## Problem Statement

When renaming files, the application scans the entire directory tree for references for **each** file rename. This results in O(n*m) file system operations where:
- `n` = number of files being renamed
- `m` = total number of files in the tree

For a directory with 100+ files, renaming 10 files would scan the tree 10 times, checking all `.md` files each time.

## Root Cause Analysis

**Location**: `utils/obsidian/obsidian_fixer.py:14-35` (`update_weblinks()` method)

The `update_weblinks()` function:
1. Is called for **each** file rename in `fix_indexes.py:102`
2. Recursively traverses the **entire** directory tree from root
3. Checks all `.md` files for references to the old file
4. Has no optimization, caching, or batching

Current call pattern in `fix_indexes.py:79-104`:
```python
for proposal in proposed_changes:  # For EACH file rename
    if ch.load_from_config("fix_weblinks"):
        of.update_weblinks(root_file, old_file, new_file)  # Scans entire tree
    old_file.rename(new_file)
```

## Proposed Solution

### Option 1: Batch Reference Scanning (Recommended)
**Approach**: Scan the entire tree once, collect all references for all files being renamed, then apply changes in a single pass.

**Changes**:
1. Create `update_weblinks_batch()` in `ObsidianFixer` that takes a list of proposed changes
2. Traverse the tree once, collecting all reference updates needed
3. Apply all updates in a single pass per file

**Implementation**:
- Add method: `ObsidianFixer.update_weblinks_batch(root_file: File, proposals: list[ProposedChange]) -> None`
- Refactor: `_update_weblinks_for_file()` to build a list of replacements instead of immediately writing
- Modify: `fix_indexes.py` to call batch method before any renames

**Time Complexity**: O(m) for scanning + O(m) for updates = O(m), a massive improvement from O(n*m)

**Files to Modify**:
- `utils/obsidian/obsidian_fixer.py` - Add batch method
- `fix_indexes.py` - Call batch method instead of per-file method

### Option 2: Index-Based Reference Tracking
**Approach**: Build an index of file references while traversing, lookup references instead of scanning.

**More Complex**: Requires caching and invalidation logic

## Implementation Plan

- [x] Review `ObsidianFixer` class structure and `ProposedChange` class
- [x] Understand exact reference pattern matching needs
- [x] Design and implement `update_weblinks_batch()` method
- [x] Refactor existing `update_weblinks()` logic to support batching
- [x] Modify `fix_indexes.py` to use batch method instead of per-file calls
- [x] Test with single file rename (verify behavior is identical)
- [x] Test with multiple file renames (verify all references are updated)
- [x] Verify no files are corrupted
- [x] Update code comments explaining batch logic

## Implementation Summary

### Changes Made

**1. `utils/obsidian/obsidian_fixer.py`**
- Added `update_weblinks_batch(file: File, file_changes: dict[File, File]) -> None`
  - Public method that scans the entire tree once with a dictionary of all file changes
  - Calls `_update_weblinks_for_file_batch()` instead of `_update_weblinks_for_file()`
  - Time complexity: O(m) instead of O(n*m)

- Added `_update_weblinks_for_file_batch(file: File, file_changes: dict[File, File]) -> None`
  - Private helper that updates a single markdown file for multiple renames
  - Applies all replacements in sequence before writing the file once
  - Only writes to disk if changes were actually made
  - Prints summary of which files were updated

**2. `fix_indexes.py`**
- Modified `bfs_fix_indexes()` to use batch updates:
  - Collects all `proposed_changes` first (as before)
  - Applies all renames in the loop (as before)
  - After all renames are complete, builds a `file_changes` dictionary mapping old → new files
  - Calls `of.update_weblinks_batch(root_file, file_changes)` once for all changes
  - Ensures references point to the newly renamed files that now exist on disk

### Key Benefits

1. **Performance**: Single tree traversal instead of n traversals
2. **Efficiency**: Each markdown file written once instead of n times
3. **Backward Compatible**: Old `update_weblinks()` method unchanged, used for single-file updates if needed
4. **Type Safe**: Full type annotations added

## Expected Outcome

**Before**: Renaming 10 files in a 100-file tree = 10 full tree scans
**After**: Renaming 10 files = 1 full tree scan + updates

**Performance Improvement**: ~10x faster for typical operations

## Related Code

- **Entry point**: `fix_indexes.py:79-104` - where `update_weblinks()` is called
- **Reference scanner**: `utils/obsidian/obsidian_fixer.py:14-59` - recursive traversal and regex logic
- **Data structure**: `ProposedChange` class in `fix_indexes.py` - contains old_file and new_file

## Notes

- Only `.md` files are checked for references
- Pattern matching uses Obsidian wiki link format: `[[filename]]`
- Config check: `ConfigHelper.load_from_config("fix_weblinks")` determines if this runs
- The BFS algorithm in `fix_indexes.py` already collects all proposed changes before applying them, making batching straightforward
