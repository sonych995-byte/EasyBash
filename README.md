# EasyBash v3.2

![python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

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

### 🔁 for – Run a command in multiple directories

```bash
for ITEM in PATH1|PATH2|PATH3... COMMAND...
```

Example:

```bash
for f in src|tests|docs ls -la
```

---

### ⚡ Parallel execution (|) – Run same command in multiple directories concurrently

```bash
PATH1|PATH2|PATH3... COMMAND...
```

Example:

```bash
src|tests|docs git status
```

---

### 🔗 Chain execution (>) – Run command sequentially across directories, stop on failure

```bash
PATH1>PATH2>PATH3... COMMAND...
```

Example:

```bash
dir1>dir2>dir3 ls -la
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

### 📦 move – Move a file (copy + delete source)

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

If ROOT is omitted, searches current directory (.).

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

When dry-run is ON, all commands are printed with [DRY-RUN] prefix but not executed.

---

## 🧠 How it works

1. Parse command line
2. Expand glob patterns (*, ?, [])
3. Validate that paths exist
4. Execute via subprocess.run() in the specified directory
5. Show colored output

---

##🌐 Compatibility

### Platform Status
- Linux ✅ Full
- macOS ✅ Full
- Termux ✅ Full
- Windows ⚠️ Partial (needs Python + terminal)

---

## 📦 Version

v3.2 – Improved parsing, dry-run toggle, parallel + chain execution, quote handling

---

## 📝 Examples (startup help)

When you run EasyBash, you’ll see:

```
EasyBash v3.2 (Improved)
Type 'exit' to quit
Examples:
  copy report.txt to backup|archive
  move data.csv to processed|archive
  find '*.log' ./logs
  for f in dir1|dir2 ls -la
  dir1|dir2 ls -la         (parallel)
  dir1>dir2>dir3 ls -la    (chain)
```

---

## ⚠️ Notes

- for loop currently ignores the ITEM variable (no {} replacement). It simply runs the command inside each directory.
- Parallel execution uses ThreadPoolExecutor – commands run concurrently, not in true parallel processes.
- Chain stops at the first directory where the command returns a non‑zero exit code.
- Always quote paths or patterns that contain spaces or special characters.

---

## License

This project is licensed under the [MIT License](LICENSE).
