# EasyBash v6.3

![python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🆕 Updates (v6.3)

### 1. New Command: `finddup` – Duplicate File Detection and Cleanup

A new `finddup` command has been added for finding and handling duplicate files.

- Scans a directory recursively for files with identical content
- Detection uses a two-stage approach: group by file size first (fast), then verify by MD5 hash (accurate)
- Each group of confirmed duplicates is presented interactively; for each group the user may:
  - **`k`** – Keep all files (do nothing)
  - **`d`** – Delete duplicates, keeping only the first file in the group
  - **`m`** – Move duplicates to a destination folder (folder is created automatically)
- Respects dry-run mode: delete and move operations print `[DRY-RUN]` messages and are not executed when `dry on` is active
- Two new internal helpers added to `FileOps`: `delete_file()` and `move_file()`, both accepting a `dry_run` parameter

```bash
finddup               # scan current directory
finddup /home/user/docs
```

---

### 2. New Command: `tree` – Detailed Directory Tree

A new `tree` command has been added for visualizing directory structure with full file metadata.

- Prints a recursive tree with `├──` / `└──` connectors (consistent with standard `tree(1)` style)
- Each entry displays inline metadata: `size`, `perms`, `owner`, `group`, and `modified` timestamp
- Symlinks are marked with `@` and show their link target; symlink directories are not descended into (prevents infinite loops from circular links)
- Entries are sorted within each directory: real directories → symlinks → regular files, each group alphabetically
- Permission string formatted as 9 characters (`rwxr-xr-x`), covering user/group/other
- Gracefully handles unreadable directories with a `[Permission denied]` notice

```bash
tree               # tree of current directory
tree /home/user/docs
```

---

### 3. Extended Dry-Run Support

Dry-run mode now covers `finddup` file operations in addition to the existing shell-command scope.

- `finddup` delete and move operations are suppressed when `dry on` is active
- `copy`, `move`, `find`, and `tree` remain unaffected by dry-run (as before)

---

### Summary

v6.3 focuses on expanding built-in file management capabilities:

- **Duplicate detection** (`finddup`) — content-aware, interactive, dry-run-safe
- **Directory inspection** (`tree`) — metadata-rich recursive view
- **Dry-run coverage** extended to `finddup` file operations

---

## 🆕 Updates (v6.2)

### 1. Command Parsing Improvements
Command parsing has been refactored to use token-based detection instead of `startswith()`.

- Prevents incorrect matches (e.g. `copycat` no longer triggers `copy`)
- Improves reliability and correctness of command execution
- Provides a more scalable foundation for future commands

---

### 2. Safer Copy Return Handling
The `copy` function now consistently returns a boolean result.

- Returns `True` only if all copy operations succeed
- Returns `False` if any operation fails or source is missing

This ensures predictable behavior and allows dependent operations (like `move`) to work correctly.

---

### 3. Safe Move Operation (Improved)
The `move` command has been further hardened.

- Source file is deleted **only if all copy operations succeed**
- Deletion is wrapped in `try/except` to prevent crashes
- Clear error messages are shown if deletion fails

This eliminates potential data loss and improves reliability.

---

### 4. Command Timeout Protection
All executed commands now include a timeout.

- Prevents the system from hanging on long-running or stuck processes
- Default timeout: **30 seconds**
- Displays an error message if a command exceeds the limit

---

### 5. Parallel Execution Summary
Parallel execution now provides a result summary.

- Tracks number of successful and failed executions
- Displays a summary after completion:

```
[SUMMARY] success=3, fail=1
```

This improves visibility when running commands across multiple paths.

---

### 6. Stability and Error Handling Improvements
General improvements across the system:

- Better exception handling in file operations
- More consistent error reporting
- Reduced risk of silent failures

---

### Summary
This update focuses on:

- Improving correctness (command parsing)
- Increasing safety (copy/move operations)
- Preventing hangs (timeouts)
- Enhancing observability (execution summary)
- Strengthening overall system stability

---

## 📌 Description

EasyBash is a Python CLI tool that simplifies shell workflows by adding parallel and sequential execution across multiple directories, plus simple file copy/move/find commands.

---

## 🎯 Purpose

- Reduce repetitive terminal commands
- Improve workflow speed
- Enable batch automation
- Support multi-directory execution

---

## 📥 Installation

```bash
git clone https://github.com/sonych995-byte/EasyBash.git
cd EasyBash
chmod +x easybash
```

---

## 🚀 Run

```bash
python easybash.py
```

---

## 🌍 Global Setup

**Linux / macOS:**
```bash
chmod +x easybash
sudo mv easybash /usr/local/bin/
```

**Windows:**
```bat
@echo off
python C:\path\to\easybash.py %*
```

> Add the script's directory to your system `PATH`.

**Termux:**
```bash
chmod +x easybash
mv easybash $PREFIX/bin/
```

---

## ⚙️ Commands

### ❓ help – Show available commands or details for a specific command

```bash
help
help <command>
```

Examples:

```bash
help
help copy
help for
```

Running `help` alone lists all available commands. Running `help <command>` shows the usage, description, and an example for that specific command.

---

### ⚡ Parallel execution (`|`) – Run same command in multiple directories concurrently

```bash
PATH1|PATH2|PATH3... COMMAND...
```

Runs `COMMAND` in all specified directories at the same time using up to **8 threads**. Non-existent paths are skipped with a warning. A summary is printed after all executions complete.

Example:

```bash
src|tests|docs git status
```

---

### 🔗 Chain execution (`>`) – Run command sequentially across directories, stop on failure

```bash
PATH1>PATH2>PATH3... COMMAND...
```

Runs `COMMAND` in each directory one by one. If any execution fails (non-zero exit code), the chain stops immediately.

Example:

```bash
dir1>dir2>dir3 ls -la
```

---

### 🔁 for – Run a command for each file matching a glob pattern

```bash
for VAR in PATTERN => COMMAND
```

`VAR` is a variable name you can use in `COMMAND` to refer to each matched path. If `COMMAND` contains `{}` placeholders, they are used instead of `VAR`.

Glob patterns support `*`, `?`, `[]`, and `**` (recursive). If no files match the pattern, a warning is shown and the loop is skipped.

Examples:

```bash
for f in *.txt => echo f
for f in *.py => python f
for f in src/*.txt => copy {} backup/{/}
for f in **/*.log => rm {}
```

---

### 🧩 Placeholder System

When using `for`, you can use these placeholders in `COMMAND`:

| Placeholder | Description                | Example result             |
|-------------|----------------------------|----------------------------|
| `{}`        | Full path (quoted)         | `'./src/main.py'`          |
| `{/}`       | Filename only              | `'main.py'`                |
| `{.}`       | Filename without extension | `'main'`                   |
| `{..}`      | Parent folder name         | `'src'`                    |
| `{abs}`     | Absolute path              | `'/home/user/src/main.py'` |

All placeholder values are automatically shell-quoted to handle spaces safely.

Example:

```bash
for f in *.txt => copy {} backup/{/}
```

If no placeholder is used, `VAR` is substituted with the matched path:

```bash
for f in *.log => rm f
```

---

### 📁 copy – Copy a file to multiple destinations

```bash
copy SRC to DST1|DST2|DST3...
```

If a destination is an existing directory, the file is placed inside it with its original name. If the destination path does not exist, it is used as the full target filename.

Example:

```bash
copy report.txt to backup|archive|external
```

Paths with spaces? Use quotes:

```bash
copy "my file.txt" to "my folder"|"another folder"
```

---

### 📦 move – Move a file (copy to all destinations + delete source)

```bash
move SRC to DST1|DST2|DST3...
```

Copies the source file to all destinations first. The source is deleted **only if every copy succeeds**. If any copy fails, the move is aborted and the source is preserved.

Example:

```bash
move data.csv to processed|archive
```

---

### 🔍 find – Search files recursively

```bash
find PATTERN [ROOT]
```

Searches for files matching `PATTERN` under `ROOT` (recursive). If `ROOT` is omitted, searches the current directory (`.`). Uses Python's `Path.rglob()` internally.

Examples:

```bash
find *.log
find *.py ./src
```

---

### 🔎 finddup – Find and handle duplicate files

```bash
finddup [ROOT]
```

Scans `ROOT` (defaults to `.`) recursively for files with identical content. Files are first grouped by size, then verified by MD5 hash to confirm true duplicates. After scanning, each duplicate group is presented interactively with three options:

- **`k`** – Keep all files in the group (do nothing)
- **`d`** – Delete all duplicates, keeping only the first file in the group
- **`m`** – Move duplicates to a folder you specify (destination is created automatically)

Respects dry-run mode: when `dry on` is active, deletions and moves are printed but not executed.

Examples:

```bash
finddup
finddup /home/user/docs
```

---

### 🌳 tree – Display a detailed directory tree

```bash
tree [PATH]
```

Prints a recursive directory tree starting at `PATH` (defaults to `.`). Each entry shows the following metadata inline:

| Field | Description |
|-------|-------------|
| `size` | File size in bytes |
| `perms` | Permission string (e.g. `rwxr-xr-x`) |
| `owner` | Owning user name |
| `group` | Owning group name |
| `modified` | Last modification timestamp (`YYYY-MM-DD HH:MM:SS`) |

Directories are listed before symlinks, which are listed before regular files. Symlinks are marked with `@` and display their link target. Directories are marked with `/`. Descends into real directories only; symlink directories are not followed.

Examples:

```bash
tree
tree /home/user/docs
```

---

### 🧪 Dry‑run mode – Preview commands without executing

```bash
dry on
dry off
```

When dry-run is **ON**, all commands are printed with a `[DRY-RUN]` prefix but not executed. Shell commands (parallel, chain, for) and `finddup` file operations (delete/move) are all affected. `copy`, `move`, and `find` are not affected. Use this to safely verify what will happen before running for real.

---

### 🚪 exit – Quit EasyBash

```bash
exit
```

Exits the EasyBash interactive session. You can also press `Ctrl+C` at any time to quit.

---

## 🧠 How it works

1. Parse the command line using `shlex.split()` for correct quote handling
2. Expand glob patterns (`*`, `?`, `[]`, `**`) in paths and `for` patterns
3. Validate that paths exist; skip and warn on missing ones
4. Execute via `subprocess.run()` in the specified directory with a 30-second timeout
5. Show colored output (green = success, red = error, yellow = warning, cyan = info)

---

## 🌐 Compatibility

| Platform | Status  | Notes                        |
|----------|---------|------------------------------|
| Linux    | ✅ Full  |                              |
| macOS    | ✅ Full  |                              |
| Termux   | ✅ Full  |                              |
| Windows  | ⚠️ Partial | Requires Python + terminal |

---

## 📦 Version

v6.3

---

## 📝 Quick Reference

When you run EasyBash, you'll see:

```
EasyBash v6.3 🚀
EasyBash>
```

Quick reference:

```bash
help                           # show all commands
help copy                      # show help for a specific command
copy report.txt to backup|archive
move data.csv to processed|archive
find *.log ./logs
finddup /home/user/docs        # find and handle duplicate files
tree /home/user/docs           # display directory tree with file info
for f in *.txt => echo f
for f in *.py => python {abs}
src|tests|docs git status      # parallel (up to 8 threads)
dir1>dir2>dir3 make build      # chain (stops on failure)
dry on                         # enable dry-run
dry off                        # disable dry-run
exit                           # quit
```

---

## Commands (Complete information)

This section provides complete reference documentation for every built-in command in EasyBash. Each entry covers syntax, parameters, internal behavior (as implemented in the source), important notes, usage examples, and edge cases.

---

### copy

**Description**

Copies a single source file to one or more destination paths. Each destination is processed independently; a failure on one destination does not stop the remaining destinations from being attempted.

**Syntax**

```
copy SRC to DST1|DST2|DST3...
```

**Parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `SRC` | Yes | Path to the source file to copy. Must exist at the time of execution. Supports quoted paths for names containing spaces. |
| `to` | Yes | Literal keyword. Must appear as the third token. Omitting it causes a usage error. |
| `DST1\|DST2...` | Yes | One or more destination paths separated by `\|`. Each destination is processed individually. |

**Behavior**

1. The raw input line is tokenized with `shlex.split()`, preserving quoted strings as single tokens.
2. The third token is validated to be the literal string `to`. If it is not, an error is printed and the command aborts.
3. The fourth token is split on `|` to produce the list of destination paths.
4. Each destination path has surrounding single or double quotes stripped before use.
5. For each destination:
   - If the destination path is an existing directory, the source filename is appended to it (`dst / src.name`).
   - If the destination path does not point to an existing directory, it is treated as the full target file path (allowing rename-on-copy).
   - The copy is performed with `shutil.copy2()`, which preserves file metadata (modification time, permissions).
   - On success, a green `[COPY] SRC -> TARGET` line is printed.
   - On failure, a red `[ERROR]` line is printed and that destination is marked failed.
6. Returns `True` if all destinations succeeded, `False` if any failed.

**Notes**

- `SRC` must exist. If it does not, the command immediately prints an error and returns without attempting any copies.
- Destination directories are not created automatically. If a destination directory does not exist and is not an existing directory, it is used as a literal file path.
- Dry-run mode does **not** affect `copy`. The `copy` command calls `FileOps.copy()` directly, which is not routed through `Executor.run_cmd()`. Dry-run applies only to shell command execution, not to built-in file operations.
- Destination paths are split on `|` at the string level, before any glob expansion. Glob patterns in destinations are not expanded.

**Examples**

```bash
# Copy to a single directory
copy report.txt to backup/

# Copy to multiple directories at once
copy report.txt to backup/|archive/|external/

# Copy with rename (destination treated as full file path)
copy report.txt to archive/report_2026.txt

# Quoted paths for names containing spaces
copy "my file.txt" to "my backup folder"|"another folder"
```

**Edge Cases**

- If `SRC` is missing, no destinations are attempted and the function returns `False` immediately.
- If one of multiple destinations fails (e.g., permission denied), the remaining destinations still proceed. The return value will be `False` but partial copies will have occurred.
- Providing fewer than 4 tokens (e.g., `copy file.txt backup/`) triggers a usage error because the `to` keyword is absent.
- An empty destination string (e.g., `copy a.txt to |backup/`) will produce an empty path, which will likely cause an OS-level error at copy time.

---

### move

**Description**

Moves a source file to one or more destinations. Internally, `move` is implemented as a copy-then-delete: the source file is deleted only after all copy operations have succeeded. If any copy fails, the source is preserved and the move is aborted.

**Syntax**

```
move SRC to DST1|DST2|DST3...
```

**Parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `SRC` | Yes | Path to the source file to move. Must exist at the time of execution. |
| `to` | Yes | Literal keyword. Must be the third token. |
| `DST1\|DST2...` | Yes | One or more destination paths separated by `\|`. |

**Behavior**

1. Input is tokenized with `shlex.split()`, and the `to` keyword is validated as the third token.
2. The fourth token is split on `|` to produce the destination list.
3. `FileOps.copy()` is called with the full destination list (see `copy` command for copy behavior).
4. If `copy()` returns `True` (all destinations succeeded):
   - `Path(src).unlink()` is called to delete the source file.
   - On success, a green `[MOVE] removed SRC` line is printed.
   - If deletion raises an exception, a red `[ERROR]` line is printed but the already-completed copies are not rolled back.
5. If `copy()` returns `False` (any destination failed):
   - Deletion is skipped entirely.
   - A red `[MOVE] aborted due to copy failure` message is printed.
   - The source file is preserved.

**Notes**

- The source is never deleted if any destination copy fails, making the operation safe with respect to data loss.
- If source deletion itself fails after a successful copy, the file will exist in both the source location and all destinations. There is no automatic rollback of the copies.
- Like `copy`, this command is not affected by dry-run mode.
- Multiple destinations are supported: the source file will exist in every destination after a successful move (and will be deleted from the source).

**Examples**

```bash
# Move to a single directory
move data.csv to processed/

# Move to multiple destinations (file ends up in both; source is deleted)
move data.csv to processed/|archive/

# Move with rename
move data.csv to archive/data_final.csv

# Quoted paths
move "old report.txt" to "final reports/"
```

**Edge Cases**

- If the source file does not exist, `FileOps.copy()` returns `False`, and deletion is never attempted.
- If the source file is deleted externally between the copy and the unlink call, `Path.unlink()` will raise a `FileNotFoundError`, which is caught and reported as an error.
- Providing fewer than 4 tokens triggers a usage error identical to `copy`.

---

### find

**Description**

Recursively searches a directory tree for files matching a given glob pattern and prints each match. Defaults to searching the current directory if no root is specified.

**Syntax**

```
find PATTERN [ROOT]
```

**Parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `PATTERN` | Yes | A glob pattern used to match filenames (e.g., `*.py`, `*.log`, `data_*`). |
| `ROOT` | No | The root directory to search from. Defaults to `.` (current directory) if omitted. |

**Behavior**

1. The input line is tokenized with `shlex.split()`. At least 2 tokens are required.
2. `Finder.find()` is called with the pattern and root.
3. Internally, `Path(root).rglob(pattern)` is used. This performs a full recursive traversal of the directory tree from `ROOT`.
4. If no files are matched, a yellow `[FIND] No matches for 'PATTERN' in 'ROOT'` message is printed.
5. Each matched path is printed in cyan with a `[FIND]` prefix.
6. The list of matched `Path` objects is returned (though not displayed further than the printed lines).

**Notes**

- `rglob()` matches files at any depth beneath `ROOT`, not just the immediate children.
- The pattern is matched against filenames and paths relative to `ROOT`, consistent with Python's `pathlib.Path.rglob()` semantics.
- `ROOT` must exist as a directory. If it does not, Python will raise an `OSError` at `rglob()` time.
- No glob expansion is applied to `PATTERN` before passing to `rglob()`; the pattern is used as-is.

**Examples**

```bash
# Find all Python files in the current directory tree
find *.py

# Find all log files under a specific directory
find *.log ./logs

# Find all text files starting from the root of a project
find *.txt ./project

# Find files with a specific prefix
find data_*.csv ./datasets
```

**Edge Cases**

- If `ROOT` does not exist, an unhandled `OSError` or `FileNotFoundError` from `Path.rglob()` will propagate to the top-level exception handler in the REPL, printing a red `[ERROR]` and continuing.
- If `PATTERN` is provided without a wildcard (e.g., `find README.md`), `rglob()` will look for exact filename matches recursively.
- Providing only 1 token (just `find`) triggers a usage error.

---

### finddup

**Description**

Scans a directory recursively for files with identical content. Duplicate detection is performed in two stages: files are first grouped by size (fast), then by MD5 hash (accurate). Each group of confirmed duplicates is presented interactively, allowing the user to keep, delete, or relocate the duplicates.

**Syntax**

```
finddup [ROOT]
```

**Parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `ROOT` | No | The root directory to scan. Defaults to `.` (current directory) if omitted. The path is resolved to an absolute path before scanning. |

**Behavior**

1. The input line is tokenized with `shlex.split()`. If a second token is present it is used as `ROOT`; otherwise `.` is used.
2. `ROOT` is resolved with `Path.expanduser().resolve()`. If the resolved path is not a directory, an error is printed and the command aborts.
3. `DuplicateFinder.find_duplicates()` scans `ROOT` recursively:
   - All files are grouped by byte size (`st_size`). Size groups with fewer than 2 files are discarded.
   - For each remaining size group, each file is hashed with MD5 (reading in 8 192-byte chunks). Files that cannot be read emit a yellow `[WARN]` and are skipped.
   - Files sharing both size and MD5 hash are collected into a duplicate group. Only groups of 2 or more are returned.
4. `DuplicateFinder.interactive_handle_duplicates()` presents each group in turn. For each group the user chooses:
   - **`k`** – Keep all. No action taken.
   - **`d`** – Delete duplicates. The first file in the group is kept; all others are deleted via `FileOps.delete_file()`.
   - **`m`** – Move duplicates. The user enters a destination folder path. The first file is kept in place; all others are moved via `FileOps.move_file()`. The destination folder is created if it does not exist (unless dry-run is active).
5. Respects dry-run mode: `FileOps.delete_file()` and `FileOps.move_file()` print `[DRY-RUN]` messages and skip actual filesystem operations when `executor.dry_run` is `True`.

**Notes**

- MD5 is used for speed, not cryptographic security. The probability of a false positive collision between two different files is negligible for practical use cases.
- The first file in each group is always kept regardless of the chosen action. The order within a group is determined by `rglob()` traversal order, which is not guaranteed to be alphabetical or by modification time.
- If no duplicates are found, a green `No duplicate files found.` message is printed and the command exits immediately.
- Unlike `copy` and `move`, `finddup` does respect dry-run mode for its internal file operations.

**Examples**

```bash
# Scan the current directory
finddup

# Scan a specific directory
finddup /home/user/docs

# Preview what would be deleted without making changes
dry on
finddup /home/user/docs
dry off
```

**Edge Cases**

- Files that cannot be read (e.g., permission denied) are skipped with a warning and excluded from duplicate groups.
- An invalid choice at the interactive prompt (`k`, `d`, or `m` only) causes the prompt to repeat until a valid answer is given.
- If the user provides an empty destination when choosing `m`, the group is skipped with a yellow warning.
- Providing a path to a file (rather than a directory) produces an error.

---

### tree

**Description**

Displays a recursive visual directory tree rooted at a given path. Each entry is annotated with detailed file metadata: size, permission bits, owner, group, and last-modification timestamp. Symlinks are identified and their targets shown. Directories are not followed through symlinks.

**Syntax**

```
tree [PATH]
```

**Parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `PATH` | No | Root path for the tree. Defaults to `.` (current directory) if omitted. Resolved via `Path.expanduser().resolve()`. |

**Behavior**

1. The input line is tokenized with `shlex.split()`. If a second token is present it is used as `PATH`; otherwise `.` is used.
2. `PATH` is resolved to an absolute path. If it does not exist, an error is printed and the command aborts.
3. `TreeDisplay.display()` prints the root node with its metadata, then recursively prints all children using `TreeDisplay._tree_lines()`.
4. Within each directory, entries are sorted: real directories first, then symlinks, then regular files. Each tier is sorted alphabetically (case-insensitive).
5. Symlink directories are **not** descended into, preventing infinite loops from circular links.
6. If a directory cannot be listed (e.g., permission denied), a `[Permission denied]` notice is printed in place of its children.
7. Each node line includes inline metadata in the format:

```
[size=N, perms=rwxr-xr-x, owner=user, group=group, modified=YYYY-MM-DD HH:MM:SS]
```

Symlink entries additionally include `link -> TARGET` before the other fields.

**Notes**

- Metadata is read with `Path.lstat()` (does not follow symlinks), so symlink entries reflect the link itself, not the target.
- Owner and group names are resolved via `pwd` and `grp` modules. On systems where resolution fails, the numeric UID/GID is used instead.
- Permission bits are formatted as a 9-character string (`rwxrwxrwx`) covering user, group, and other, matching the output style of `ls -l`. The leading type character (e.g., `d` for directory) is not included.
- The tree uses `├──` and `└──` connectors with `│` continuation lines, consistent with the standard `tree(1)` utility style.

**Examples**

```bash
# Display tree of the current directory
tree

# Display tree of a specific path
tree /home/user/docs

# Display tree of the root directory (may be large)
tree /
```

**Edge Cases**

- If `PATH` does not exist, a red `[ERROR] Path does not exist: PATH` is printed and the command returns without output.
- On a system where `pwd` or `grp` modules are unavailable (e.g., minimal environments), numeric IDs are displayed instead of names.
- Very deep or large directory trees will produce proportionally long output. There is no depth limit.

---

### for

**Description**

Iterates over all files matching a glob pattern and executes a shell command for each match. Supports a rich set of path placeholders for flexible command construction. This is the primary batch-processing command in EasyBash.

**Syntax**

```
for VAR in PATTERN => COMMAND
```

**Parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `VAR` | Yes | A variable name. Used as a word-boundary substitution target in `COMMAND` if no `{}` placeholders are present. |
| `in` | Yes | Literal keyword. Must be the third token of the left-hand side. |
| `PATTERN` | Yes | A glob pattern (supports `*`, `?`, `[]`, and `**` for recursive matching). Expanded with `glob.glob(..., recursive=True)`. |
| `=>` | Yes | Literal separator between the loop header and the command template. Must appear somewhere in the raw input. |
| `COMMAND` | Yes | The command template to execute for each matched file. May contain placeholders or the variable name `VAR`. |

**Behavior**

1. The raw input is split on `=>` into a left part (loop header) and a right part (command template). Only the first `=>` is used.
2. The left part is tokenized with `shlex.split()`. Exactly 4 tokens are expected: `for`, `VAR`, `in`, `PATTERN`. Any other count causes a usage error.
3. `glob.glob(PATTERN, recursive=True)` is called to expand the pattern. If no files match, a yellow warning is printed and execution stops.
4. For each matched file:
   - The matched path is wrapped in a `Path` object.
   - If `COMMAND` contains any `{...}` placeholder (detected by regex `\{[^}]+\}`), placeholder substitution is performed using the table below.
   - If no placeholder is detected, word-boundary substitution is performed: all occurrences of `VAR` (as a whole word) in `COMMAND` are replaced with the shell-quoted matched path.
   - The final command string is parsed with `shlex.split()` into a list of arguments.
   - `Executor.run_cmd()` is called with those arguments (subject to dry-run mode and the 30-second timeout).

**Placeholder Reference**

| Placeholder | Resolves To | Shell-Quoted |
|-------------|-------------|--------------|
| `{}` | Full relative path | Yes |
| `{/}` | Filename only (with extension) | Yes |
| `{.}` | Filename stem (without extension) | Yes |
| `{..}` | Parent directory name | Yes |
| `{abs}` | Absolute path | Yes |

All placeholder values are automatically passed through `shlex.quote()` to safely handle filenames containing spaces or special characters.

**Notes**

- Placeholder detection takes priority over variable substitution. If any `{...}` pattern is present in `COMMAND`, placeholder mode is used exclusively. Variable name substitution is not performed in that case.
- Unknown placeholders (e.g., `{foo}`) trigger a yellow `[WARN]` message but are left as-is in the command string.
- Commands are executed sequentially, one file at a time, in the order returned by `glob.glob()`. There is no parallelism within `for`.
- Each command is subject to the 30-second timeout enforced by `Executor.run_cmd()`.
- If dry-run mode is active, each iteration prints a `[DRY-RUN]` line instead of executing.

**Examples**

```bash
# Echo each matched filename using variable substitution
for f in *.txt => echo f

# Run a Python script on each .py file using the {} placeholder
for f in *.py => python {}

# Use the absolute path placeholder
for f in src/*.py => python {abs}

# Use the filename stem (no extension) as an output name
for f in *.md => pandoc {} -o {.}.html

# Use the parent directory name
for f in **/*.log => echo {..}

# Recursive match across all subdirectories
for f in **/*.log => rm {}
```

**Edge Cases**

- If `PATTERN` matches no files, a warning is printed and the loop body is never executed.
- If the substituted command string cannot be parsed by `shlex.split()` (e.g., unmatched quotes), the iteration prints a red `[ERROR]` and skips to the next file without stopping the loop.
- Variable substitution uses word-boundary regex (`\bVAR\b`), so a variable named `f` will not accidentally match partial words like `for` or `info`.
- The `=>` separator is matched at the raw string level before any tokenization. A `=>` appearing inside a quoted argument would still split the command incorrectly.
- If `COMMAND` is empty (e.g., `for f in *.txt =>`), `shlex.split()` will produce an empty list and `Executor.run_cmd()` will be called with an empty command, resulting in a subprocess error.

---

### dry

**Description**

Enables or disables dry-run mode for the current EasyBash session. When active, shell command execution is suppressed and commands are printed instead. This allows safe inspection of what would be executed without making any changes.

**Syntax**

```
dry on
dry off
```

**Parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `on` | Conditional | Activates dry-run mode. Sets `executor.dry_run = True`. |
| `off` | Conditional | Deactivates dry-run mode. Sets `executor.dry_run = False`. |

**Behavior**

1. The raw input is matched as a complete string against the exact values `"dry on"` and `"dry off"` (after stripping leading/trailing whitespace).
2. On `dry on`: the `Executor` instance's `dry_run` attribute is set to `True`. A yellow `[DRY RUN ON]` confirmation is printed.
3. On `dry off`: `dry_run` is set to `False`. A yellow `[DRY RUN OFF]` confirmation is printed.
4. When `dry_run` is `True`, `Executor.run_cmd()` prints `[DRY-RUN] cd CWD && COMMAND` in yellow and returns `0` without calling `subprocess.run()`.

**Scope of Dry-Run**

Dry-run affects all commands routed through `Executor.run_cmd()`:

| Command | Affected by Dry-Run |
|---------|---------------------|
| Parallel execution (`\|`) | Yes |
| Chain execution (`>`) | Yes |
| `for` loop body | Yes |
| Single shell command | Yes |
| `finddup` (delete/move operations) | Yes |
| `copy` | No |
| `move` | No |
| `find` | No |
| `tree` | No |

`copy`, `move`, and `find` use their own internal Python implementations (`shutil`, `pathlib`) and are not routed through `Executor`, so they are not suppressed by dry-run mode. `finddup` is a special case: its internal `FileOps.delete_file()` and `FileOps.move_file()` helpers accept the `dry_run` flag directly, so deletions and moves are suppressed when dry-run is active. `tree` is read-only and unaffected by dry-run.

**Notes**

- Dry-run state persists for the entire session until explicitly toggled. It is initialized to `False` at startup.
- The command is matched as a complete string, not tokenized. `dry  on` (extra spaces) or `DRY ON` (uppercase) will not match and will instead be interpreted as a bare shell command.
- There is no `dry` command without a subcommand; typing just `dry` will be passed to `Executor.single()` as a raw shell command.

**Examples**

```bash
# Enable dry-run to preview parallel execution
dry on
src|tests|docs git pull

# Disable dry-run to execute for real
dry off
src|tests|docs git pull

# Preview a for loop without running anything
dry on
for f in *.sh => bash {}
dry off
```

**Edge Cases**

- `dry ON`, `Dry on`, or `dry  on` (extra whitespace between words) will not activate dry-run. The match is exact against the full trimmed input string.
- Dry-run has no effect on `copy` and `move`. Even with `dry on` active, those commands will perform real file operations.

---

### help

**Description**

Displays information about available commands. When called without arguments, lists all commands and their short descriptions. When called with a command name, prints that command's usage syntax, description, and an example.

**Syntax**

```
help
help <command>
```

**Parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<command>` | No | The name of the command to look up. Must match a key in the internal `HELP` dictionary. |

**Behavior**

1. The raw input is tokenized with `shlex.split()`.
2. If only 1 token is present (just `help`):
   - Prints `Available commands:` in cyan.
   - Iterates over the `HELP` dictionary and prints each command name and its `desc` field in green.
   - Prints `Use: help <command>` in yellow as a usage hint.
3. If 2 or more tokens are present (e.g., `help copy`):
   - The second token is used as the command name to look up.
   - If found in `HELP`, prints the command name in cyan, its `usage` in green, its `desc` in blue, and its `example` in yellow.
   - If not found, prints a red `[ERROR] No help for '<cmd>'`.

**The HELP Dictionary**

The following commands have registered help entries:

| Command | Registered |
|---------|------------|
| `copy` | Yes |
| `move` | Yes |
| `find` | Yes |
| `finddup` | Yes |
| `for` | Yes |
| `dry` | Yes |
| `exit` | Yes |
| `tree` | Yes |

**Notes**

- The `help` command itself does not have a help entry in the `HELP` dictionary. `help help` will print an error.
- Parallel (`|`) and chain (`>`) execution modes do not have help entries.
- The HELP dictionary is static and defined at module level. It is not dynamically updated.

**Examples**

```bash
# List all commands
help

# Show usage for copy
help copy

# Show usage for the for loop
help for

# Show dry-run help
help dry
```

**Edge Cases**

- `help help` prints `[ERROR] No help for 'help'` because `help` is not a key in the `HELP` dictionary.
- Any token beyond the second is silently ignored (e.g., `help copy move` looks up only `copy`).
- The lookup is case-sensitive. `help Copy` will not find `copy`.

---

### exit

**Description**

Terminates the EasyBash interactive session and returns to the system shell.

**Syntax**

```
exit
```

**Parameters**

None.

**Behavior**

1. The REPL's input loop checks whether the stripped input equals the string `"exit"` before passing it to `EasyBash.run()`.
2. If matched, the `while True` loop is broken and the process exits normally.
3. Pressing `Ctrl+C` at any prompt triggers a `KeyboardInterrupt`, which is caught by the REPL, prints a blank line, and also breaks the loop — equivalent to `exit`.

**Notes**

- `exit` is handled in the REPL loop directly, not inside `EasyBash.run()`. It is not possible to use `exit` as a shell command or within a `for` loop body.
- Matching is exact and case-sensitive after stripping whitespace. `Exit`, `EXIT`, or `exit ` (trailing space without stripping) will be passed to `EasyBash.run()` as a raw shell command instead of terminating the session. (The REPL does call `.strip()` before comparison, so trailing spaces are safe.)
- There is no unsaved-state prompt. The session exits immediately.
- Any in-progress parallel execution (`ThreadPoolExecutor`) will be allowed to complete or time out before the program terminates, as the executor context manager waits for futures.

**Examples**

```bash
# Quit the session
exit

# Equivalent keyboard shortcut
Ctrl+C
```

**Edge Cases**

- `exit` typed inside a `for` loop command template (e.g., `for f in *.txt => exit`) will be passed to the OS as a shell command, not interpreted by EasyBash. Most shells will exit the subprocess spawned for that command only.
- If the terminal is closed directly (SIGHUP), Python will raise an `EOFError` on `input()`, which is not explicitly caught. This will propagate and terminate the process with an unhandled exception traceback.

---

## License

This project is licensed under the [MIT License](LICENSE).
