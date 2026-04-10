# EasyBash

![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Goal

EasyBash is a CLI tool designed to make Bash commands **simpler, faster, and more powerful** using Python.  
It reduces repetitive `cd` usage, simplifies long paths, and improves developer workflow speed.

---

## Purpose

- Reduce repetitive `cd` commands
- Simplify complex file paths
- Separate file operations and folder operations
- Improve developer workflow speed
- Make Bash easier and more intuitive

---

## Core Concept

EasyBash separates commands into two main categories:

| Command | Target | Purpose |
|---------|--------|---------|
| `for`   | Files  | Perform actions on files in multiple directories |
| `rush`  | Folders| Navigate and execute commands in multiple directories |
| `exit`  | CLI    | Exit EasyBash |
| `help`  | CLI    | Show this command guide |

---

## Installation

### Basic Usage

```bash
git clone https://github.com/sonych995-byte/EasyBash.git
chmod +x easybash
python easybash.py
```

## Global Command Setup (Use Anywhere)

Make EasyBash accessible from any directory by installing the launcher script.

Termux

```bash
chmod +x easybash
mv easybash $PREFIX/bin/
```

Linux

```bash
chmod +x easybash
sudo mv easybash /usr/local/bin/
```

macOS

```bash
chmod +x easybash
sudo mv easybash /usr/local/bin/
```

Windows

1. Create a file easybash.bat with the following content:
   ```batch
   @echo off
   python C:\path\to\easybash.py %*
   ```
2. Add the directory containing easybash.bat to your PATH:
   · Open Start Menu → Search "Environment Variables"
   · Click "Edit the system environment variables"
   · Go to "Environment Variables" → Select Path → Edit → Add the directory

## Dependencies

EasyBash uses only Python standard library modules, so no external installation is required.

Built-in Modules

```
shlex
subprocess
pathlib
glob
typing
```

---

## Commands

1. for - Operate on a single file in multiple directories

```bash
for (filename) in (path1|path2|path3) (bash command)
```

Example:

```bash
for test.txt in /tmp|/home "rm"
```

This runs:

```bash
cd /tmp && rm test.txt
cd /home && rm test.txt
```

2. rush - Operate on directories

```bash
rush (path1|path2|path3) (bash command)
```

Example:

```bash
rush /tmp|/home "ls -la"
```

This runs:

```bash
cd /tmp && ls -la
cd /home && ls -la
```

3. exit - Quit EasyBash

```bash
exit
```

4. help - Show command guide

```bash
help
```

---

## Notes

· You can provide as many paths as you want using |:
  ```bash
  for target.txt in path1|path2|path3|... rm
  ```
· Use quotes for commands with spaces:
  ```bash
  rush /tmp|/home "ls -la"
  ```
· Invalid paths will be skipped with a warning; execution continues.
· EasyBash works cross-platform: Linux, macOS, Windows, and Termux.

---

## Why EasyBash?

EasyBash makes command-line workflows faster by:

· Eliminating repetitive cd commands
· Simplifying long paths
· Providing intuitive syntax for file and folder operations

Example Comparison:

Traditional Bash:

```bash
cd web && cd myweb && rm logic.py
```

EasyBash:

```bash
for logic.py in web|myweb rm
```
