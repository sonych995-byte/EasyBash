# EasyBash v6.1

![python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🆕 Updates (v6.1)

### 1. Help System
A built-in help system has been added to improve usability and make the CLI self-documenting.

- `help`  
  Displays all available commands with short descriptions.

- `help <command>`  
  Shows detailed usage, description, and an example for a specific command.

This allows users to understand and use EasyBash without needing external documentation.

---

### 2. Safer Move Operation (Data Loss Prevention)
The `move` command has been improved to prevent accidental data loss.

- Files are only deleted from the source **after all copy operations succeed**.
- If any copy operation fails, the original file is preserved.

This ensures safer file handling and aligns with production-grade behavior.

---

### 3. Placeholder Warning System
The `for` loop engine now detects unknown placeholders.

- If an unrecognized placeholder is used (e.g. `{unknown}`), a warning is displayed.
- Prevents silent failures and improves debugging.

---

### 4. Thread Limiting for Parallel Execution
Parallel execution now uses a controlled number of threads.

- `ThreadPoolExecutor` is limited with `max_workers=8`.
- Prevents system overload when running commands across many paths.

This improves stability and performance under heavy workloads.

---

### Summary
This update focuses on:

- Improving user experience (help system)
- Increasing safety (move operation)
- Enhancing debugging (placeholder warnings)
- Ensuring stability (thread limits)

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

v6.1

---

## 📝 Examples (startup prompt)

When you run EasyBash, you'll see:

```
EasyBash v6.0 🚀
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
