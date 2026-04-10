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
- Default timeout: 30 seconds
- Displays an error message if a command exceeds the limit

---

### 5. Parallel Execution Summary
Parallel execution now provides a result summary.

- Tracks number of successful and failed executions
- Displays a summary after completion:
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

Linux / macOS:
```bash
chmod +x easybash
sudo mv easybash /usr/local/bin/
```

Windows:
```bash
@echo off
python C:\path\to\easybash.py %*
```

(Add to PATH)

Termux:
```bash
chmod +x easybash
mv easybash $PREFIX/bin/
```

---

## ⚙️ Commands

### ⚡ Parallel execution (`|`) – Run same command in multiple directories concurrently

```bash
PATH1|PATH2|PATH3... COMMAND...
```

Example:

```bash
src|tests|docs git status
```

---

### 🔗 Chain execution (`>`) – Run command sequentially across directories, stop on failure

```bash
PATH1>PATH2>PATH3... COMMAND...
```

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

Examples:

```bash
for f in *.txt => echo f
for f in *.py => python f
for f in src/*.txt => copy {} backup/{/}
```

---

### 🧩 Placeholder System

When using `for`, you can use these placeholders in `COMMAND`:

| Placeholder | Description               | Example result        |
|-------------|---------------------------|-----------------------|
| `{}`        | Full path (quoted)        | `./src/main.py`       |
| `{/}`       | Filename only             | `main.py`             |
| `{.}`       | Filename without extension| `main`                |
| `{..}`      | Parent folder name        | `src`                 |
| `{abs}`     | Absolute path             | `/home/user/src/main.py` |

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

Example:

```bash
move data.csv to processed|archive
```

---

### 🔍 find – Search files recursively

```bash
find PATTERN [ROOT]
```

If ROOT is omitted, searches current directory (`.`).

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

When dry-run is ON, all commands are printed with `[DRY-RUN]` prefix but not executed.

---

## 🧠 How it works

1. Parse command line
2. Expand glob patterns (`*`, `?`, `[]`, `**`)
3. Validate that paths exist
4. Execute via `subprocess.run()` in the specified directory
5. Show colored output

---

## 🌐 Compatibility

### Platform Status
- Linux ✅ Full
- macOS ✅ Full
- Termux ✅ Full
- Windows ⚠️ Partial (needs Python + terminal)

---

## 📦 Version

v6.2

---

## 📝 Examples (startup prompt)

When you run EasyBash, you'll see:

```
EasyBash v6.2 🚀
EasyBash>
```

Quick reference:

```bash
copy report.txt to backup|archive
move data.csv to processed|archive
find *.log ./logs
for f in *.txt => echo f
for f in *.py => python {abs}
src|tests|docs git status      # parallel
dir1>dir2>dir3 make build      # chain
dry on                         # enable dry-run
dry off                        # disable dry-run
exit                           # quit
```

---

## License

This project is licensed under the [MIT License](LICENSE).
