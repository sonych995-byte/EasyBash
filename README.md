# EasyBash v6.2

![python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

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

### 🧪 Dry‑run mode – Preview commands without executing

```bash
dry on
dry off
```

When dry-run is **ON**, all commands are printed with a `[DRY-RUN]` prefix but not executed. File operations (`copy`, `move`) and shell commands (parallel, chain, for) are all affected. Use this to safely verify what will happen before running for real.

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

v6.2

---

## 📝 Quick Reference

When you run EasyBash, you'll see:

```
EasyBash v6.2 🚀
EasyBash>
```

Quick reference:

```bash
help                           # show all commands
help copy                      # show help for a specific command
copy report.txt to backup|archive
move data.csv to processed|archive
find *.log ./logs
for f in *.txt => echo f
for f in *.py => python {abs}
src|tests|docs git status      # parallel (up to 8 threads)
dir1>dir2>dir3 make build      # chain (stops on failure)
dry on                         # enable dry-run
dry off                        # disable dry-run
exit                           # quit
```

---

## License

This project is licensed under the [MIT License](LICENSE).
