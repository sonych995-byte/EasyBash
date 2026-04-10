# 📦 EasyBash

![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

---

## 📌 Description

EasyBash is a Python CLI tool that simplifies shell workflows by adding higher-level commands for file management, batch automation, and multi-directory execution.

It acts as a productivity layer over traditional shell commands.

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

`python easybash.py`

Or run from path:

python /path/to/easybash.py

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

### 🔁 for
Run command across multiple directories.

Syntax:
```bash
for <file_pattern> in <path1|path2> <command>
```

Example:
```bash
for *.py in src|tests python {}
```

---

### ⚡ rush
Run commands in parallel directories.

Syntax:
```bash
rush <path1|path2> <command>
```

Example:
```bash
rush src|tests git status
```

---

### 📁 copy
Copy files by pattern.

Syntax:
```bash
copy <pattern> to <dest1|dest2> <mode>
```

Modes:
dir  -> copy into each folder
flat -> copy into single folder

Example:
```bash
copy *.log to backup|archive dir
```

---

### 📦 move
Move files safely (copy then delete).

Syntax:
```bash
move <pattern> to <dest1|dest2> <mode>
```

Example:
```bash
move *.tmp to logs|archive flat
```

---

### 🔍 find
Search files recursively.

Syntax:
```bash
find <pattern> in <path1|path2>
```

Example:
```bash
find *.py in src|lib
```

---

### 📜 batch
Execute commands from file.

Syntax:
```bash
batch <file>
```

Example:
```bash
batch commands.txt
```

---

## 🧠 How it works

1. Parse command
2. Expand paths
3. Execute via subprocess
4. Return output

---

## 🧩 Architecture

- CommandParser
- PathManager
- CommandExecutor

---

## 🌐 Compatibility

- Linux     -> full support
- macOS     -> full support
- Termux    -> full support
- Windows   -> partial (needs .bat)
- PowerShell-> partial

---

## 🔒 Safety

- move only deletes after success
- batch uses trusted files only
- parallel execution is limited
- recursion is controlled

---

## 📦 Version

v3.2.0

---

# EasyBash v3.2 – Improvements

## New Features
- Chain execution (`>`): run commands sequentially across directories, stop on failure  
  `dir1>dir2>dir3 ls -la`
- Parallel execution (`|`): replaces `rush` – run commands concurrently  
  `src|tests|docs git status`
- Interactive dry-run toggle: `dry on` / `dry off`
- Simpler copy/move syntax: `copy file.txt to dest1|dest2|dest3`
- Automatic quote stripping for paths with spaces
- Inline help on startup (examples displayed)

## Fixed Issues
| Original (v3.0) | Improved (v3.2) |
|----------------|----------------|
| Quotes in paths caused parsing errors | Proper quote handling with `shlex.split()` + `_strip_quotes()` |
| Dry-run only via environment variable | Real-time `dry on`/`off` commands |
| Complex `for` with `{}` replacement | Simplified `for` on directories |
| Separate `rush` command | Unified `path1\|path2` syntax for parallelism |

## Removed Features (for simplicity)
- `batch` command (execute from file)
- `flat` mode in copy/move
- Command history, signal handler, batch depth limit
- Environment variables (`EASYBASH_VERBOSE`, `EASYBASH_MAX_WORKERS`)
