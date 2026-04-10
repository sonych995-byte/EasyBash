# EasyBash

![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Repo Description
### What it is

EasyBash is a Python-based CLI tool that simplifies Bash workflows by introducing higher-level commands for file and directory operations.

### Key Highlights

1. Simplifies repetitive terminal commands
2. Adds batch processing for files and directories
3. Works across Linux, macOS, Windows, and Termux
4. Lightweight and built using only Python standard libraries

---

## Purpose
### What it is for
EasyBash is designed to improve terminal productivity by reducing repetitive navigation and command execution patterns in Bash environments.

---

## Installation
### git clone
```bash
git clone https://github.com/sonych995-byte/EasyBash.git
chmod +x easybash
```

#### Run Directly
```bash
python easybash.py
```

### Load File (Manual Setup)
If running from another location:
```bash
python /path/to/easybash.py
```

---

## Global Access Setup (All Platforms)
### Linux / macOS
```bash
chmod +x easybash
sudo mv easybash /usr/local/bin/
```

### Windows
1. Create easybash.bat
```bash
@echo off
python C:\path\to\easybash.py %*
```
2. Add the folder to PATH environment variables

### termux
```bash
chmod +x easybash
mv easybash $PREFIX/bin/
```

## Commands Overview

### for
#### Description
Run a command on a single file across multiple directories.
#### syntax
```bash
for <filename> in <path1>|<path2> <command>
```
#### Usage
```bash
for test.txt in /tmp|/home "rm"
```

---

### rush
#### Description
Run a command across multiple directories.
#### Syntax
```bash
rush <path1>|<path2> <command>
```
#### Usage
```bash
rush /tmp|/home "ls -la"
```

---

### copy
#### Description
Copy files matching a pattern to multiple destinations.
#### Syntax
```bash
copy <pattern> <dest1>|<dest2>
```
#### Usage
```bash
copy *.log src|backup
```

---

### move
#### Description
Move files matching a pattern to multiple destinations.
#### Syntax
```bash
move <pattern> <dest1>|<dest2>
```
#### Usage
```bash
move *.tmp logs|archive
```

## How EasyBash Works
### Core Principle
EasyBash acts as a command interpreter that:
1. Parses custom commands
2. Converts them into shell operations
3. Executes them using Python subprocess
4. Handles multi-path execution logic
### Core Engine (Conceptual Code)
```python
while True:
    command = input("EasyBash> ")
    parsed = parse_command(command)
    execute(parsed)
```
### Execution Flow
1. Read user input
2. Parse command type
3. Extract paths / files / actions
4. Execute system commands
5. Return output

## EasyBash & Shell Compatibility
EasyBash converts custom EasyBash commands into standard system shell commands before execution.
### Important Behavior
EasyBash does not directly execute commands itself.
It relies on the operating system’s available shell to run the final output.
### Compatibility

| Environment | Result |
|------------|--------|
| Bash (Linux) | Fully supported |
| Zsh (macOS / Linux) | Mostly compatible |
| Termux | Fully supported |
| Windows CMD | Not supported (requires conversion) |
| PowerShell | Partially supported (needs adaptation or translation layer) |

### Key Limitation
EasyBash generates Bash-style commands, so it requires a compatible shell environment to execute correctly. If the system does not support Bash syntax, commands may fail unless additional translation support is implemented.

## version
v2.0.1

# update 2.0.1
## 🔒 Security & Critical Bug Fixes

### 🚨 Data Loss Prevention
- **CVE-like issue**: `move` command deleted source files even when copy failed
  - Fixed: Now only removes successfully copied files
  - Added rollback protection for partial failures
  
### 🐛 Major Bugs Fixed

1. **Broken 'dirs' mode in copy/move**
   - Logic was completely wrong (concatenating unrelated paths)
   - Removed mode entirely to prevent confusion

2. **Missing exception handling**
   - `shutil.copy2()` without try-catch caused crashes
   - Now gracefully handles permission denied, disk full, etc.

3. **Race condition in parallel output**
   - Multiple commands writing to stdout simultaneously caused interleaved text
   - Now captures output per command and displays sequentially

4. **Directory move not supported**
   - `source.unlink()` fails on directories (IsADirectoryError)
   - Added `shutil.rmtree()` for directory removal

5. **KeyboardInterrupt during parallel execution**
   - Thread pool not properly shutdown
   - Added graceful shutdown with `executor.shutdown(wait=False)`

6. **Batch file recursion**
   - No depth limit could cause stack overflow
   - Added MAX_DEPTH = 10 protection

7. **UnicodeDecodeError in batch files**
   - Used system default encoding instead of UTF-8
   - Fixed with explicit `encoding='utf-8'`

8. **Find command truncation**
   - Only showed first 20 results without warning
   - Now displays all matching files

9. **Flat mode counter reset**
   - Counter reset per file causing potential overwrites
   - Changed to global counter for unique naming

## ✅ Improvements
- Added signal handler for Ctrl+C
- Added validation for max_workers (minimum 1)
- Better error messages for permission denied in find
- Enhanced help text with safety notes
